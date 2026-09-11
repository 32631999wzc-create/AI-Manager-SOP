"""Deterministic project state operations built on the Phase 2 validators."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
import shutil
from typing import Any

from runtime_validation.validators import TASK_STATUS, validate_document, validate_object

from .store import StoreError, atomic_write, load_yaml, sha256_document


FORMAT_VERSION = 1
CHANGE_TYPES = {"INPUT_CHANGE", "ARTIFACT_CHANGE", "TASK_FAILURE", "DECISION_CHANGE", "SCOPE_CHANGE"}
REPLAN_ACTIONS = {"PRESERVE", "OUTDATE", "ADD", "CANCEL"}
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


class RuntimeFailure(ValueError):
    """A runtime operation would create or consume invalid project state."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def _fail(code: str, message: str) -> None:
    raise RuntimeFailure(code, message)


def _require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail("STATE_INVALID", f"{label} must be a mapping")
    return value


def _version_number(value: Any, label: str) -> int:
    match = re.fullmatch(r"v([1-9]\d*)", str(value))
    if not match:
        _fail("VERSION_INVALID", f"{label} must use vN")
    return int(match.group(1))


def _validation_failure(errors: list[Any], label: str) -> None:
    if errors:
        rendered = "; ".join(f"{error.code}@{error.path}" for error in errors)
        _fail("VALIDATION_FAILED", f"{label}: {rendered}")


class ProjectRuntime:
    """Manage one repository-local `.ai-product` directory."""

    def __init__(self, project_root: str | Path):
        self.root = Path(project_root).resolve()
        self.state = self.root / ".ai-product"
        self.manifest_path = self.state / "manifest.yaml"
        self.profile_path = self.state / "profile.yaml"
        self.plan_path = self.state / "plan.yaml"
        self.records_path = self.state / "registry" / "records.yaml"
        self.artifacts_path = self.state / "registry" / "artifacts.yaml"
        self.latest_snapshot_path = self.state / "snapshots" / "latest.yaml"
        self.context_path = self.state / "context" / "current.yaml"

    def _read(self, path: Path, label: str) -> Any:
        if not path.is_file():
            _fail("STATE_MISSING", f"missing {label}: {path}")
        try:
            return load_yaml(path)
        except StoreError as exc:
            _fail("STATE_INVALID", str(exc))

    def _parts(self) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], list[Any], list[Any]]:
        manifest = _require_mapping(self._read(self.manifest_path, "manifest"), "manifest")
        profile = _require_mapping(self._read(self.profile_path, "profile"), "profile")
        plan = _require_mapping(self._read(self.plan_path, "plan"), "plan")
        records_doc = _require_mapping(self._read(self.records_path, "records"), "records")
        artifacts_doc = _require_mapping(self._read(self.artifacts_path, "artifacts"), "artifacts")
        if set(manifest) != {"format_version", "project_id", "current_plan_version", "source_sha256", "snapshot_sequence"}:
            _fail("MANIFEST_INVALID", "manifest fields do not match format version 1")
        if manifest["format_version"] != FORMAT_VERSION:
            _fail("FORMAT_UNSUPPORTED", f"unsupported format version: {manifest['format_version']}")
        records = records_doc.get("records")
        artifacts = artifacts_doc.get("artifacts")
        if set(records_doc) != {"records"} or not isinstance(records, list):
            _fail("STATE_INVALID", "records.yaml must contain only a records list")
        if set(artifacts_doc) != {"artifacts"} or not isinstance(artifacts, list):
            _fail("STATE_INVALID", "artifacts.yaml must contain only an artifacts list")
        return manifest, profile, plan, records, artifacts

    @staticmethod
    def _validation_plan(plan: dict[str, Any], artifacts: list[Any]) -> dict[str, Any]:
        required = {"plan", "available_inputs", "gates", "blocked_inputs", "write_targets"}
        if set(plan) != required:
            _fail("STATE_INVALID", f"plan.yaml must contain exactly {sorted(required)}")
        return {**deepcopy(plan), "artifacts": deepcopy(artifacts)}

    def validate(self, require_artifact_files: bool = True) -> dict[str, Any]:
        manifest, profile, plan, records, artifacts = self._parts()
        _validation_failure(validate_document(profile, "profile"), "profile")
        _validation_failure(validate_document(self._validation_plan(plan, artifacts), "plan"), "plan")
        for index, record in enumerate(records):
            _validation_failure(validate_object("ProjectRecord", record, f"records[{index}]"), "records")
        for index, artifact in enumerate(artifacts):
            _validation_failure(validate_object("Artifact", artifact, f"artifacts[{index}]"), "artifacts")
        record_ids = [item.get("id") for item in records if isinstance(item, dict)]
        artifact_ids = [item.get("id") for item in artifacts if isinstance(item, dict)]
        if len(record_ids) != len(set(record_ids)):
            _fail("REGISTRY_DUPLICATE", "record ids must be unique")
        if len(artifact_ids) != len(set(artifact_ids)):
            _fail("REGISTRY_DUPLICATE", "artifact ids must be unique")
        plan_version = plan["plan"]["version"]
        if manifest["current_plan_version"] != plan_version:
            _fail("PLAN_VERSION_MISMATCH", "manifest and plan versions differ")
        if require_artifact_files:
            for artifact in artifacts:
                if artifact["status"] != "ACTIVE":
                    continue
                location = Path(str(artifact["location"]))
                resolved = location if location.is_absolute() else self.root / location
                if not resolved.is_file():
                    _fail("ARTIFACT_MISSING", f"ACTIVE artifact is missing: {artifact['id']} ({resolved})")
        return {
            "valid": True,
            "project_id": manifest["project_id"],
            "plan_version": plan_version,
            "records": len(records),
            "artifacts": len(artifacts),
        }

    def init(self, document: dict[str, Any], project_id: str) -> dict[str, Any]:
        if not project_id.strip():
            _fail("PROJECT_ID_REQUIRED", "project id must be non-empty")
        if set(document) != {"profile", "plan"}:
            _fail("INPUT_INVALID", "init input must contain exactly profile and plan")
        _validation_failure(validate_document(document, "combined"), "init input")
        digest = sha256_document(document)
        if self.state.exists():
            manifest = _require_mapping(self._read(self.manifest_path, "manifest"), "manifest")
            if manifest.get("source_sha256") == digest and manifest.get("project_id") == project_id:
                self.validate(require_artifact_files=False)
                return {"status": "already_initialized", "project_id": project_id}
            _fail("PROJECT_EXISTS", ".ai-product already exists with different initialization input")

        temporary = self.root / ".ai-product.init.tmp"
        if temporary.exists():
            shutil.rmtree(temporary)
        try:
            (temporary / "registry").mkdir(parents=True)
            (temporary / "snapshots" / "history").mkdir(parents=True)
            (temporary / "context").mkdir(parents=True)
            input_plan = deepcopy(document["plan"])
            artifacts = input_plan.pop("artifacts")
            manifest = {
                "format_version": FORMAT_VERSION,
                "project_id": project_id,
                "current_plan_version": input_plan["plan"]["version"],
                "source_sha256": digest,
                "snapshot_sequence": 0,
            }
            atomic_write(temporary / "manifest.yaml", manifest)
            atomic_write(temporary / "profile.yaml", document["profile"])
            atomic_write(temporary / "plan.yaml", input_plan)
            atomic_write(temporary / "registry" / "records.yaml", {"records": []})
            atomic_write(temporary / "registry" / "artifacts.yaml", {"artifacts": artifacts})
            temporary.replace(self.state)
        except Exception:
            if temporary.exists():
                shutil.rmtree(temporary)
            raise
        self.validate(require_artifact_files=False)
        return {"status": "initialized", "project_id": project_id, "plan_version": input_plan["plan"]["version"]}

    def status(self) -> dict[str, Any]:
        summary = self.validate()
        _, profile, plan, _, _ = self._parts()
        tasks = plan["plan"]["tasks"]
        counts: dict[str, int] = {}
        for task in tasks:
            counts[task["status"]] = counts.get(task["status"], 0) + 1
        blocked = [task["id"] for task in tasks if task["status"] in {"BLOCKED", "WAITING_USER", "FAILED"}]
        return {
            **summary,
            "objective": plan["plan"]["objective"],
            "delivery_target": profile["delivery_target"],
            "task_counts": counts,
            "blocked_tasks": blocked,
        }

    def update_profile(self, profile: dict[str, Any]) -> dict[str, Any]:
        _validation_failure(validate_document(profile, "profile"), "profile")
        self.validate()
        atomic_write(self.profile_path, deepcopy(profile))
        return {"status": "updated", "delivery_target": profile["delivery_target"]}

    def complete(self) -> dict[str, Any]:
        self.validate()
        _, profile, plan, _, artifacts = self._parts()
        required_nodes = [
            node["node"] for node in profile["nodes"]
            if node["level"] == "REQUIRED" and node["scope_role"] != "OUT_OF_SCOPE"
            and node["status"] != "SATISFIED"
        ]
        unfinished_tasks = [
            task["id"] for task in plan["plan"]["tasks"]
            if task["status"] not in {"COMPLETED", "SKIPPED", "CANCELLED"}
        ]
        blocking_tasks = [
            task["id"] for task in plan["plan"]["tasks"]
            if task["status"] in {"BLOCKED", "WAITING_USER", "FAILED", "OUTDATED"}
        ]
        inactive_required_artifacts = sorted({
            artifact_id
            for task in plan["plan"]["tasks"]
            if task["status"] == "COMPLETED"
            for artifact_id in task["artifact_requirements"]
            if not any(item["id"] == artifact_id and item["status"] == "ACTIVE" for item in artifacts)
        })
        blocked_gates = [name for name, result in plan["gates"].items() if result == "BLOCKED"]
        reasons = {
            "required_nodes_not_satisfied": required_nodes,
            "unfinished_tasks": unfinished_tasks,
            "blocking_tasks": blocking_tasks,
            "inactive_required_artifacts": inactive_required_artifacts,
            "blocked_gates": blocked_gates,
        }
        return {"complete": not any(reasons.values()), "reasons": reasons}
    def _active_registry(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        _, _, _, records, artifacts = self._parts()
        return (
            [item for item in records if item["status"] == "ACTIVE"],
            [item for item in artifacts if item["status"] == "ACTIVE"],
        )

    def next(self) -> dict[str, Any]:
        self.validate()
        _, _, plan, _, _ = self._parts()
        tasks = plan["plan"]["tasks"]
        critical = {task_id: index for index, task_id in enumerate(plan["plan"]["critical_path"])}
        ready = [task for task in tasks if task["status"] == "READY"]
        if not ready:
            unfinished = [task["id"] for task in tasks if task["status"] not in {"COMPLETED", "SKIPPED", "CANCELLED"}]
            return {"status": "no_ready_task", "unfinished_tasks": unfinished}
        task = min(ready, key=lambda item: (PRIORITY_ORDER[item["priority"]], critical.get(item["id"], len(tasks)), tasks.index(item)))
        records, artifacts = self._active_registry()
        record_ids = set(task["context_requirements"])
        artifact_ids = set(task["artifact_requirements"]) | set(task["context_requirements"])
        relevant_records = [item for item in records if not item["affected_scope"] or item["id"] in record_ids or task["id"] in item["affected_scope"] or task["lifecycle_node"] in item["affected_scope"]]
        relevant_artifacts = [item for item in artifacts if item["id"] in artifact_ids]
        snapshot = load_yaml(self.latest_snapshot_path) if self.latest_snapshot_path.is_file() else {"unresolved_items": []}
        context = {
            "task": task["id"],
            "relevant_facts": [item["id"] for item in relevant_records if item["type"] == "FACT"],
            "relevant_decisions": [item["id"] for item in relevant_records if item["type"] == "DECISION"],
            "relevant_constraints": [item["id"] for item in relevant_records if item["type"] == "CONSTRAINT"],
            "relevant_artifacts": [item["id"] for item in relevant_artifacts],
            "recent_changes": [],
            "assumptions": list(plan["plan"]["assumptions"]) + [item["id"] for item in relevant_records if item["type"] == "ASSUMPTION"],
            "unresolved_items": list(snapshot.get("unresolved_items", [])) if isinstance(snapshot, dict) else [],
            "allowed_actions": ["execute", "validate"],
            "available_tools": [],
        }
        _validation_failure(validate_object("TaskContextPack", context), "context")
        atomic_write(self.context_path, context)
        return {"status": "ready", "task": task, "context": context}

    def checkpoint(self, unresolved_items: list[str] | None = None) -> dict[str, Any]:
        self.validate()
        manifest, _, plan, records, artifacts = self._parts()
        snapshot = {
            "plan_version": plan["plan"]["version"],
            "task_states": {task["id"]: task["status"] for task in plan["plan"]["tasks"]},
            "active_artifacts": [item["id"] for item in artifacts if item["status"] == "ACTIVE"],
            "active_records": [item["id"] for item in records if item["status"] == "ACTIVE"],
            "unresolved_items": list(unresolved_items or []),
        }
        _validation_failure(validate_object("RuntimeSnapshot", snapshot), "snapshot")
        sequence = int(manifest["snapshot_sequence"]) + 1
        atomic_write(self.state / "snapshots" / "history" / f"snapshot-{sequence:04d}.yaml", snapshot)
        atomic_write(self.latest_snapshot_path, snapshot)
        manifest["snapshot_sequence"] = sequence
        atomic_write(self.manifest_path, manifest)
        return {"status": "checkpointed", "sequence": sequence, "snapshot": snapshot}

    def resume(self) -> dict[str, Any]:
        self.validate()
        snapshot = _require_mapping(self._read(self.latest_snapshot_path, "latest snapshot"), "snapshot")
        _validation_failure(validate_object("RuntimeSnapshot", snapshot), "snapshot")
        _, _, plan, records, artifacts = self._parts()
        expected_states = {task["id"]: task["status"] for task in plan["plan"]["tasks"]}
        if snapshot["plan_version"] != plan["plan"]["version"]:
            _fail("SNAPSHOT_PLAN_MISMATCH", "snapshot plan version differs from current plan")
        if snapshot["task_states"] != expected_states:
            _fail("SNAPSHOT_TASK_MISMATCH", "snapshot task states differ from current plan")
        active_records = {item["id"] for item in records if item["status"] == "ACTIVE"}
        active_artifacts = {item["id"] for item in artifacts if item["status"] == "ACTIVE"}
        if set(snapshot["active_records"]) != active_records or set(snapshot["active_artifacts"]) != active_artifacts:
            _fail("SNAPSHOT_REGISTRY_MISMATCH", "snapshot registry references differ from current registry")
        selection = self.next()
        return {"status": "resumed", "snapshot": snapshot, "selection": selection}

    def update_task(self, task_id: str, status: str, validation_pass: bool = False) -> dict[str, Any]:
        if status not in TASK_STATUS:
            _fail("TASK_STATUS_INVALID", f"unknown task status: {status}")
        if status == "COMPLETED" and not validation_pass:
            _fail("VALIDATION_REQUIRED", "COMPLETED requires explicit validation PASS")
        self.validate()
        _, _, plan, _, artifacts = self._parts()
        matches = [task for task in plan["plan"]["tasks"] if task["id"] == task_id]
        if not matches:
            _fail("TASK_UNKNOWN", f"unknown task: {task_id}")
        previous = matches[0]["status"]
        matches[0]["status"] = status
        _validation_failure(validate_document(self._validation_plan(plan, artifacts), "plan"), "updated plan")
        atomic_write(self.plan_path, plan)
        return {"status": "updated", "task_id": task_id, "from": previous, "to": status}

    def register_record(self, record: dict[str, Any]) -> dict[str, Any]:
        _validation_failure(validate_object("ProjectRecord", record), "record")
        self.validate()
        _, _, _, records, _ = self._parts()
        if any(item["id"] == record["id"] for item in records):
            _fail("REGISTRY_DUPLICATE", f"record id already exists: {record['id']}")
        records.append(deepcopy(record))
        atomic_write(self.records_path, {"records": records})
        return {"status": "registered", "record_id": record["id"]}

    def commit_artifact(self, artifact: dict[str, Any], validation_pass: bool = False) -> dict[str, Any]:
        if not validation_pass:
            _fail("VALIDATION_REQUIRED", "artifact commit requires explicit validation PASS")
        _validation_failure(validate_object("Artifact", artifact), "artifact")
        if artifact["status"] != "ACTIVE":
            _fail("ARTIFACT_STATUS_INVALID", "newly committed artifact must be ACTIVE")
        self.validate()
        _, _, plan, _, artifacts = self._parts()
        tasks = {task["id"]: task for task in plan["plan"]["tasks"]}
        incomplete = [task_id for task_id in artifact["source_tasks"] if task_id not in tasks or tasks[task_id]["status"] != "COMPLETED"]
        if incomplete:
            _fail("ARTIFACT_SOURCE_INVALID", f"source tasks are not completed: {incomplete}")
        if any(item["id"] == artifact["id"] for item in artifacts):
            _fail("REGISTRY_DUPLICATE", f"artifact id already exists: {artifact['id']}")
        active_same = [item for item in artifacts if item["name"] == artifact["name"] and item["type"] == artifact["type"] and item["status"] == "ACTIVE"]
        if active_same:
            expected = max(_version_number(item["version"], "artifact version") for item in active_same) + 1
            if _version_number(artifact["version"], "artifact version") != expected:
                _fail("ARTIFACT_VERSION_INVALID", f"next version must be v{expected}")
            for item in active_same:
                item["status"] = "SUPERSEDED"
        elif _version_number(artifact["version"], "artifact version") != 1:
            _fail("ARTIFACT_VERSION_INVALID", "first artifact version must be v1")
        artifacts.append(deepcopy(artifact))
        atomic_write(self.artifacts_path, {"artifacts": artifacts})
        return {"status": "committed", "artifact_id": artifact["id"], "version": artifact["version"]}

    @staticmethod
    def _dag_signature(plan: dict[str, Any]) -> tuple[Any, Any]:
        tasks = [(item["id"], item["lifecycle_node"], item["dependencies"]) for item in plan["plan"]["tasks"]]
        deps = [(item["from"], item["to"], item["type"]) for item in plan["plan"]["dependencies"]]
        return tasks, deps

    def replan(self, change: dict[str, Any]) -> dict[str, Any]:
        if set(change) != {"change_type", "actions", "plan"}:
            _fail("REPLAN_INVALID", "replan input must contain exactly change_type, actions and plan")
        if change["change_type"] not in CHANGE_TYPES or not isinstance(change["actions"], list):
            _fail("REPLAN_INVALID", "unknown change type or malformed actions")
        self.validate()
        manifest, _, old_plan, _, artifacts = self._parts()
        new_plan = _require_mapping(deepcopy(change["plan"]), "replan plan")
        _validation_failure(validate_document(self._validation_plan(new_plan, artifacts), "plan"), "replan plan")
        old_tasks = {item["id"]: item for item in old_plan["plan"]["tasks"]}
        new_tasks = {item["id"]: item for item in new_plan["plan"]["tasks"]}
        seen: set[tuple[str, str]] = set()
        for index, action in enumerate(change["actions"]):
            if not isinstance(action, dict) or set(action) != {"action", "target"}:
                _fail("REPLAN_INVALID", f"actions[{index}] must contain action and target")
            kind, target = action["action"], action["target"]
            if kind not in REPLAN_ACTIONS or not isinstance(target, str):
                _fail("REPLAN_INVALID", f"actions[{index}] is invalid")
            seen.add((kind, target))
            if kind == "ADD" and (target in old_tasks or target not in new_tasks):
                _fail("REPLAN_ACTION_MISMATCH", f"ADD does not describe new task {target}")
            if kind == "CANCEL" and (target not in old_tasks or target not in new_tasks or new_tasks[target]["status"] != "CANCELLED"):
                _fail("REPLAN_ACTION_MISMATCH", f"CANCEL does not cancel task {target}")
            if kind == "OUTDATE" and (target not in old_tasks or target not in new_tasks or new_tasks[target]["status"] != "OUTDATED"):
                _fail("REPLAN_ACTION_MISMATCH", f"OUTDATE does not outdate task {target}")
            if kind == "PRESERVE" and (target not in old_tasks or target not in new_tasks or old_tasks[target] != new_tasks[target]):
                _fail("REPLAN_ACTION_MISMATCH", f"PRESERVE changes task {target}")
        for task_id in set(old_tasks) | set(new_tasks):
            if old_tasks.get(task_id) != new_tasks.get(task_id) and not any(target == task_id for _, target in seen):
                _fail("REPLAN_ACTION_MISSING", f"task change lacks an action: {task_id}")
        dag_changed = self._dag_signature(old_plan) != self._dag_signature(new_plan)
        old_version = _version_number(old_plan["plan"]["version"], "old plan version")
        new_version = _version_number(new_plan["plan"]["version"], "new plan version")
        if dag_changed and new_version != old_version + 1:
            _fail("PLAN_VERSION_INVALID", f"DAG change requires plan version v{old_version + 1}")
        if not dag_changed and new_version != old_version:
            _fail("PLAN_VERSION_INVALID", "unchanged DAG must retain the current plan version")
        atomic_write(self.plan_path, new_plan)
        manifest["current_plan_version"] = new_plan["plan"]["version"]
        atomic_write(self.manifest_path, manifest)
        return {"status": "replanned", "change_type": change["change_type"], "dag_changed": dag_changed, "plan_version": new_plan["plan"]["version"]}
