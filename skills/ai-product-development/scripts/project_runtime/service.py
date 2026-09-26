"""Deterministic project state operations built on the Phase 2 validators."""

from __future__ import annotations

from copy import deepcopy
import hashlib
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
        self.evidence_path = self.state / "registry" / "evidence.yaml"
        self.decisions_path = self.state / "registry" / "decisions.yaml"
        self.artifacts_path = self.state / "registry" / "artifacts.yaml"
        self.latest_snapshot_path = self.state / "snapshots" / "latest.yaml"
        self.context_path = self.state / "context" / "current.yaml"
        self.reviews_path = self.state / "reviews"

    def _review_path(self, task_id: str) -> Path:
        digest = hashlib.sha256(task_id.encode("utf-8")).hexdigest()
        return self.reviews_path / f"task-{digest}.yaml"

    def _review(self, task_id: str) -> dict[str, Any] | None:
        path = self._review_path(task_id)
        if not path.is_file():
            return None
        review = _require_mapping(self._read(path, "task review"), "task review")
        attempts = review.get("attempts")
        if review.get("task_id") != task_id or not isinstance(attempts, list) or not attempts:
            _fail("REVIEW_INVALID", f"invalid review record for {task_id}")
        required = {"submitted_result", "submitted_files", "decision", "reviewer", "feedback",
                    "reviewed_result", "reviewed_files", "changed", "impact"}
        for attempt in attempts:
            if not isinstance(attempt, dict) or set(attempt) != required:
                _fail("REVIEW_INVALID", f"malformed review attempt for {task_id}")
            if attempt["decision"] not in {"PENDING", "APPROVED", "REJECTED"}:
                _fail("REVIEW_INVALID", f"unknown review decision for {task_id}")
            if not isinstance(attempt["impact"], dict) or attempt["impact"].get("status") not in {"PENDING", "CLEARED", "REPLAN_REQUIRED"}:
                _fail("REVIEW_INVALID", f"invalid review impact for {task_id}")
            for field in ("submitted_files", "reviewed_files"):
                files = attempt[field]
                if not isinstance(files, list) or any(
                    not isinstance(item, dict) or set(item) != {"path", "sha256"}
                    or not all(isinstance(value, str) for value in item.values())
                    for item in files
                ):
                    _fail("REVIEW_INVALID", f"invalid {field} for {task_id}")
        return review

    def _file_snapshots(self, paths: Any) -> list[dict[str, str]]:
        if not isinstance(paths, list) or any(not isinstance(item, str) for item in paths):
            _fail("REVIEW_INVALID", "output_files must be a list of paths")
        snapshots = []
        for item in paths:
            resolved = (self.root / item).resolve()
            if not resolved.is_relative_to(self.root) or not resolved.is_file():
                _fail("REVIEW_FILE_INVALID", f"output file must exist inside product root: {item}")
            relative = resolved.relative_to(self.root).as_posix()
            snapshots.append({"path": relative, "sha256": hashlib.sha256(resolved.read_bytes()).hexdigest()})
        if len({item["path"] for item in snapshots}) != len(snapshots):
            _fail("REVIEW_INVALID", "output_files contains duplicate paths")
        return snapshots

    @staticmethod
    def _review_digest(attempt: dict[str, Any]) -> str:
        return sha256_document({key: value for key, value in attempt.items() if key != "impact"})

    def _read(self, path: Path, label: str) -> Any:
        if not path.is_file():
            _fail("STATE_MISSING", f"missing {label}: {path}")
        try:
            return load_yaml(path)
        except StoreError as exc:
            _fail("STATE_INVALID", str(exc))

    def _registry_document(self, path: Path, key: str) -> dict[str, Any]:
        if not path.is_file():
            return {key: []}
        return _require_mapping(self._read(path, key), key)

    def _parts(self) -> tuple[
        dict[str, Any], dict[str, Any], dict[str, Any], list[Any],
        list[Any], list[Any], list[Any],
    ]:
        manifest = _require_mapping(self._read(self.manifest_path, "manifest"), "manifest")
        profile = _require_mapping(self._read(self.profile_path, "profile"), "profile")
        plan = _require_mapping(self._read(self.plan_path, "plan"), "plan")
        records_doc = self._registry_document(self.records_path, "records")
        evidence_doc = self._registry_document(self.evidence_path, "evidence")
        decisions_doc = self._registry_document(self.decisions_path, "decisions")
        artifacts_doc = self._registry_document(self.artifacts_path, "artifacts")
        if set(manifest) != {"format_version", "project_id", "current_plan_version", "source_sha256", "snapshot_sequence"}:
            _fail("MANIFEST_INVALID", "manifest fields do not match format version 1")
        if manifest["format_version"] != FORMAT_VERSION:
            _fail("FORMAT_UNSUPPORTED", f"unsupported format version: {manifest['format_version']}")
        records = records_doc.get("records")
        evidence = evidence_doc.get("evidence")
        decisions = decisions_doc.get("decisions")
        artifacts = artifacts_doc.get("artifacts")
        if set(records_doc) != {"records"} or not isinstance(records, list):
            _fail("STATE_INVALID", "records.yaml must contain only a records list")
        if set(artifacts_doc) != {"artifacts"} or not isinstance(artifacts, list):
            _fail("STATE_INVALID", "artifacts.yaml must contain only an artifacts list")
        if set(evidence_doc) != {"evidence"} or not isinstance(evidence, list):
            _fail("STATE_INVALID", "evidence.yaml must contain only an evidence list")
        if set(decisions_doc) != {"decisions"} or not isinstance(decisions, list):
            _fail("STATE_INVALID", "decisions.yaml must contain only a decisions list")
        for artifact in artifacts:
            if isinstance(artifact, dict):
                artifact.setdefault("evidence_refs", [])
                artifact.setdefault("decision_refs", [])
        return manifest, profile, plan, records, evidence, decisions, artifacts

    @staticmethod
    def _validation_plan(plan: dict[str, Any], artifacts: list[Any]) -> dict[str, Any]:
        required = {"plan", "available_inputs", "gates", "blocked_inputs", "write_targets"}
        if set(plan) != required:
            _fail("STATE_INVALID", f"plan.yaml must contain exactly {sorted(required)}")
        return {**deepcopy(plan), "artifacts": deepcopy(artifacts)}

    def validate(self, require_artifact_files: bool = True) -> dict[str, Any]:
        manifest, profile, plan, records, evidence, decisions, artifacts = self._parts()
        _validation_failure(validate_document(profile, "profile"), "profile")
        _validation_failure(validate_document(self._validation_plan(plan, artifacts), "plan"), "plan")
        for index, record in enumerate(records):
            _validation_failure(validate_object("ProjectRecord", record, f"records[{index}]"), "records")
        for index, item in enumerate(evidence):
            _validation_failure(validate_object("EvidenceRecord", item, f"evidence[{index}]"), "evidence")
        for index, decision in enumerate(decisions):
            _validation_failure(validate_object("DecisionRecord", decision, f"decisions[{index}]"), "decisions")
        for index, artifact in enumerate(artifacts):
            _validation_failure(validate_object("Artifact", artifact, f"artifacts[{index}]"), "artifacts")
        record_ids = [item.get("id") for item in records if isinstance(item, dict)]
        evidence_ids = [item.get("id") for item in evidence if isinstance(item, dict)]
        decision_ids = [item.get("id") for item in decisions if isinstance(item, dict)]
        artifact_ids = [item.get("id") for item in artifacts if isinstance(item, dict)]
        if len(record_ids) != len(set(record_ids)):
            _fail("REGISTRY_DUPLICATE", "record ids must be unique")
        if len(artifact_ids) != len(set(artifact_ids)):
            _fail("REGISTRY_DUPLICATE", "artifact ids must be unique")
        if len(evidence_ids) != len(set(evidence_ids)):
            _fail("REGISTRY_DUPLICATE", "evidence ids must be unique")
        if len(decision_ids) != len(set(decision_ids)):
            _fail("REGISTRY_DUPLICATE", "decision ids must be unique")
        evidence_set = set(evidence_ids)
        decision_set = set(decision_ids)
        for decision in decisions:
            missing = set(decision["evidence_refs"]) - evidence_set
            if missing:
                _fail("DECISION_EVIDENCE_UNKNOWN", f"decision {decision['id']} references unknown evidence: {sorted(missing)}")
            if decision["supersedes"] is not None and decision["supersedes"] not in decision_set:
                _fail("DECISION_SUPERSEDES_UNKNOWN", f"decision {decision['id']} supersedes an unknown decision")
            if decision["supersedes"] == decision["id"]:
                _fail("DECISION_SUPERSEDES_SELF", f"decision {decision['id']} cannot supersede itself")
        for artifact in artifacts:
            missing_evidence = set(artifact["evidence_refs"]) - evidence_set
            missing_decisions = set(artifact["decision_refs"]) - decision_set
            if missing_evidence or missing_decisions:
                _fail("ARTIFACT_TRACE_UNKNOWN", f"artifact {artifact['id']} has unknown evidence/decision refs")
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
            "evidence": len(evidence),
            "decisions": len(decisions),
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
            (temporary / "reviews").mkdir(parents=True)
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
            atomic_write(temporary / "registry" / "evidence.yaml", {"evidence": []})
            atomic_write(temporary / "registry" / "decisions.yaml", {"decisions": []})
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
        _, profile, plan, _, _, _, _ = self._parts()
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
            "review_blockers": self._review_blockers(tasks, plan),
        }

    def update_profile(self, profile: dict[str, Any]) -> dict[str, Any]:
        _validation_failure(validate_document(profile, "profile"), "profile")
        self.validate()
        atomic_write(self.profile_path, deepcopy(profile))
        return {"status": "updated", "delivery_target": profile["delivery_target"]}

    def complete(self) -> dict[str, Any]:
        self.validate()
        _, profile, plan, _, _, _, artifacts = self._parts()
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
            "review_blockers": self._review_blockers(plan["plan"]["tasks"], plan),
        }
        return {"complete": not any(reasons.values()), "reasons": reasons}
    def _active_registry(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
        _, _, _, records, evidence, decisions, artifacts = self._parts()
        return (
            [item for item in records if item["status"] == "ACTIVE"],
            evidence,
            decisions,
            [item for item in artifacts if item["status"] == "ACTIVE"],
        )

    def _review_blockers(self, tasks: list[dict[str, Any]], plan: dict[str, Any]) -> list[dict[str, str]]:
        blockers = []
        plan_digest = sha256_document(plan)
        for task in tasks:
            task_id = task["id"]
            review = self._review(task_id)
            latest = review["attempts"][-1] if review else None
            if task["status"] == "WAITING_USER" or (latest and latest["decision"] == "PENDING"):
                blockers.append({"task_id": task_id, "reason": "WAITING_USER"})
                continue
            if not latest or latest["decision"] != "APPROVED":
                continue
            for item in latest["reviewed_files"]:
                path = self.root / item["path"]
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
                    blockers.append({"task_id": task_id, "reason": "APPROVED_OUTPUT_CHANGED"})
                    break
            impact = latest.get("impact", {})
            if impact.get("status") == "PENDING":
                blockers.append({"task_id": task_id, "reason": "REVIEW_IMPACT_PENDING"})
            elif impact.get("status") == "REPLAN_REQUIRED" and impact.get("plan_sha256") == plan_digest:
                blockers.append({"task_id": task_id, "reason": "REVIEW_REPLAN_REQUIRED"})
        return blockers

    def next(self) -> dict[str, Any]:
        self.validate()
        _, _, plan, _, _, _, _ = self._parts()
        tasks = plan["plan"]["tasks"]
        blockers = self._review_blockers(tasks, plan)
        if blockers:
            return {"status": "review_blocked", "blockers": blockers}
        running = [task["id"] for task in tasks if task["status"] == "RUNNING"]
        if running:
            return {"status": "task_in_progress", "task_ids": running}
        critical = {task_id: index for index, task_id in enumerate(plan["plan"]["critical_path"])}
        ready = [task for task in tasks if task["status"] == "READY"]
        if not ready:
            unfinished = [task["id"] for task in tasks if task["status"] not in {"COMPLETED", "SKIPPED", "CANCELLED"}]
            return {"status": "no_ready_task", "unfinished_tasks": unfinished}
        rework = [
            task for task in ready
            if (review := self._review(task["id"])) and review["attempts"][-1]["decision"] == "REJECTED"
        ]
        candidates = rework or ready
        task = min(candidates, key=lambda item: (PRIORITY_ORDER[item["priority"]], critical.get(item["id"], len(tasks)), tasks.index(item)))
        records, evidence, decisions, artifacts = self._active_registry()
        record_ids = set(task["context_requirements"])
        artifact_ids = set(task["artifact_requirements"]) | set(task["context_requirements"])
        relevant_records = [item for item in records if not item["affected_scope"] or item["id"] in record_ids or task["id"] in item["affected_scope"] or task["lifecycle_node"] in item["affected_scope"]]
        relevant_artifacts = [item for item in artifacts if item["id"] in artifact_ids]
        replacements = {
            item["supersedes"]: item["id"]
            for item in decisions
            if item["supersedes"] is not None
        }

        def current_decision(decision_id: str) -> str:
            seen = set()
            while decision_id in replacements and decision_id not in seen:
                seen.add(decision_id)
                decision_id = replacements[decision_id]
            return decision_id

        requested_decisions = record_ids | {item for artifact in relevant_artifacts for item in artifact["decision_refs"]}
        decision_ids = {current_decision(item) for item in requested_decisions}
        relevant_decision_records = [item for item in decisions if item["id"] in decision_ids]
        evidence_ids = record_ids | {item for artifact in relevant_artifacts for item in artifact["evidence_refs"]}
        evidence_ids |= {item for decision in relevant_decision_records for item in decision["evidence_refs"]}
        relevant_evidence = [item for item in evidence if item["id"] in evidence_ids]
        snapshot = load_yaml(self.latest_snapshot_path) if self.latest_snapshot_path.is_file() else {"unresolved_items": []}
        context = {
            "task": task["id"],
            "relevant_facts": [item["id"] for item in relevant_records if item["type"] == "FACT"],
            "relevant_decisions": [item["id"] for item in relevant_records if item["type"] == "DECISION"] + [item["id"] for item in relevant_decision_records],
            "relevant_evidence": [item["id"] for item in relevant_evidence],
            "relevant_constraints": [item["id"] for item in relevant_records if item["type"] == "CONSTRAINT"],
            "relevant_artifacts": [item["id"] for item in relevant_artifacts],
            "recent_changes": [],
            "assumptions": list(plan["plan"]["assumptions"]) + [item["id"] for item in relevant_records if item["type"] == "ASSUMPTION"],
            "unresolved_items": list(snapshot.get("unresolved_items", [])) if isinstance(snapshot, dict) else [],
            "allowed_actions": ["execute", "validate"],
            "available_tools": [],
        }
        review_inputs = []
        for task_id in [*task["dependencies"], task["id"]]:
            review = self._review(task_id)
            if not review:
                continue
            latest = review["attempts"][-1]
            if latest["decision"] not in {"APPROVED", "REJECTED"}:
                continue
            review_inputs.append({
                "task_id": task_id,
                "decision": latest["decision"],
                "result": latest["reviewed_result"],
                "files": latest["reviewed_files"],
                "feedback": latest["feedback"],
                "changed": latest["changed"],
                "review_record": self._review_path(task_id).relative_to(self.root).as_posix(),
            })
        context["recent_changes"] = [
            f"Human review for {item['task_id']}: {item['decision']}; read {item['review_record']} and current output files"
            for item in review_inputs
        ]
        _validation_failure(validate_object("TaskContextPack", context), "context")
        atomic_write(self.context_path, context)
        return {"status": "ready", "task": task, "context": context, "review_inputs": review_inputs}

    def checkpoint(self, unresolved_items: list[str] | None = None) -> dict[str, Any]:
        self.validate()
        manifest, _, plan, records, _, _, artifacts = self._parts()
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
        _, _, plan, records, _, _, artifacts = self._parts()
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
        if status in {"COMPLETED", "WAITING_USER", "SKIPPED", "OUTDATED", "CANCELLED"}:
            _fail("REVIEW_REQUIRED", "submit-result and human review are required; skip/cancel/outdate through Replan")
        self.validate()
        _, _, plan, _, _, _, artifacts = self._parts()
        matches = [task for task in plan["plan"]["tasks"] if task["id"] == task_id]
        if not matches:
            _fail("TASK_UNKNOWN", f"unknown task: {task_id}")
        previous = matches[0]["status"]
        if previous in {"WAITING_USER", "COMPLETED", "SKIPPED", "OUTDATED", "CANCELLED"}:
            _fail("TASK_TRANSITION_INVALID", f"cannot directly change task from {previous}")
        if self._review_blockers(plan["plan"]["tasks"], plan):
            _fail("REVIEW_BLOCKED", "resolve pending review before starting another task")
        if status == "RUNNING" and any(
            task["id"] != task_id and task["status"] == "RUNNING"
            for task in plan["plan"]["tasks"]
        ):
            _fail("TASK_IN_PROGRESS", "another task is already running")
        matches[0]["status"] = status
        _validation_failure(validate_document(self._validation_plan(plan, artifacts), "plan"), "updated plan")
        atomic_write(self.plan_path, plan)
        return {"status": "updated", "task_id": task_id, "from": previous, "to": status}

    def submit_result(self, task_id: str, document: dict[str, Any], validation_pass: bool = False) -> dict[str, Any]:
        if not validation_pass:
            _fail("VALIDATION_REQUIRED", "review submission requires explicit validation PASS")
        if set(document) != {"result", "output_files"} or not isinstance(document["result"], str):
            _fail("REVIEW_INVALID", "submission requires result and output_files")
        files = self._file_snapshots(document["output_files"])
        if not document["result"].strip() and not files:
            _fail("REVIEW_INVALID", "submission needs a result or output file")
        self.validate()
        _, _, plan, _, _, _, artifacts = self._parts()
        tasks = {item["id"]: item for item in plan["plan"]["tasks"]}
        if task_id not in tasks or tasks[task_id]["status"] not in {"READY", "RUNNING"}:
            _fail("TASK_TRANSITION_INVALID", "only a READY or RUNNING task may submit for review")
        review = self._review(task_id) or {"task_id": task_id, "attempts": []}
        if review["attempts"] and review["attempts"][-1]["decision"] == "PENDING":
            pending = review["attempts"][-1]
            if pending["submitted_result"] != document["result"] or pending["submitted_files"] != files:
                _fail("REVIEW_PENDING", "a different submission is already awaiting review")
            tasks[task_id]["status"] = "WAITING_USER"
            _validation_failure(validate_document(self._validation_plan(plan, artifacts), "plan"), "review pending plan")
            atomic_write(self.plan_path, plan)
            self.checkpoint()
            return {"status": "waiting_for_review", "task_id": task_id, "recovered": True}
        if self._review_blockers(plan["plan"]["tasks"], plan):
            _fail("REVIEW_BLOCKED", "another review must be resolved first")
        review["attempts"].append({
            "submitted_result": document["result"],
            "submitted_files": files,
            "decision": "PENDING",
            "reviewer": None,
            "feedback": "",
            "reviewed_result": None,
            "reviewed_files": [],
            "changed": False,
            "impact": {"status": "PENDING"},
        })
        tasks[task_id]["status"] = "WAITING_USER"
        _validation_failure(validate_document(self._validation_plan(plan, artifacts), "plan"), "review pending plan")
        atomic_write(self._review_path(task_id), review)
        atomic_write(self.plan_path, plan)
        self.checkpoint()
        return {"status": "waiting_for_review", "task_id": task_id, "review_record": self._review_path(task_id).relative_to(self.root).as_posix()}

    def review_task(self, document: dict[str, Any]) -> dict[str, Any]:
        required = {"task_id", "decision", "reviewer", "feedback"}
        if not required.issubset(document) or set(document) - required - {"result", "output_files"}:
            _fail("REVIEW_INVALID", "review requires task_id, decision, reviewer, feedback and optional result/output_files")
        task_id, decision, reviewer, feedback = (document[key] for key in ("task_id", "decision", "reviewer", "feedback"))
        if not all(isinstance(value, str) for value in (task_id, decision, reviewer, feedback)):
            _fail("REVIEW_INVALID", "review fields must be strings")
        if decision not in {"APPROVED", "REJECTED"} or not reviewer.strip():
            _fail("REVIEW_INVALID", "review needs an explicit decision and reviewer")
        self.validate()
        _, _, plan, _, _, _, artifacts = self._parts()
        tasks = {item["id"]: item for item in plan["plan"]["tasks"]}
        if task_id not in tasks:
            _fail("TASK_UNKNOWN", f"unknown task: {task_id}")
        review = self._review(task_id)
        if not review:
            _fail("REVIEW_MISSING", "task has no submitted result")
        latest = review["attempts"][-1]
        if tasks[task_id]["status"] == "WAITING_USER" and latest["decision"] in {"APPROVED", "REJECTED"}:
            if decision != latest["decision"] or reviewer != latest["reviewer"] or feedback != latest["feedback"]:
                _fail("REVIEW_RECOVERY_MISMATCH", "pending state has a different recorded human decision")
            if "result" in document and document["result"] != latest["reviewed_result"]:
                _fail("REVIEW_RECOVERY_MISMATCH", "reviewed result differs from recorded decision")
            if "output_files" in document and self._file_snapshots(document["output_files"]) != latest["reviewed_files"]:
                _fail("REVIEW_RECOVERY_MISMATCH", "reviewed files differ from recorded decision")
            tasks[task_id]["status"] = "COMPLETED" if decision == "APPROVED" else "READY"
            _validation_failure(validate_document(self._validation_plan(plan, artifacts), "plan"), "recovered review plan")
            atomic_write(self.plan_path, plan)
            self.checkpoint()
            return {"status": "approved" if decision == "APPROVED" else "rework_required",
                    "task_id": task_id, "recovered": True, "review_sha256": self._review_digest(latest),
                    "impact_required": latest["impact"]["status"] == "PENDING"}
        if tasks[task_id]["status"] in {"WAITING_USER", "READY", "RUNNING"} and latest["decision"] == "PENDING":
            attempt = latest
        elif tasks[task_id]["status"] == "COMPLETED" and latest["decision"] == "APPROVED" and decision == "APPROVED":
            attempt = {
                "submitted_result": latest["reviewed_result"],
                "submitted_files": latest["reviewed_files"],
                "decision": "PENDING",
                "reviewer": None,
                "feedback": "",
                "reviewed_result": None,
                "reviewed_files": [],
                "changed": False,
                "impact": {"status": "PENDING"},
            }
            review["attempts"].append(attempt)
        else:
            _fail("TASK_TRANSITION_INVALID", "task is not awaiting this review decision")
        paths = document.get("output_files", [item["path"] for item in attempt["submitted_files"]])
        files = self._file_snapshots(paths)
        # A human-edited file supersedes an old inline summary unless the reviewer supplied a revised summary.
        result = document.get("result", "" if files != attempt["submitted_files"] else attempt["submitted_result"])
        if not isinstance(result, str):
            _fail("REVIEW_INVALID", "reviewed result must be a string")
        if not result.strip() and not files:
            _fail("REVIEW_INVALID", "approved/rejected content cannot be empty")
        changed = result != attempt["submitted_result"] or files != attempt["submitted_files"]
        if decision == "REJECTED" and not feedback.strip() and not changed:
            _fail("REVIEW_INVALID", "rejection needs feedback or edited content")
        attempt.update({
            "decision": decision,
            "reviewer": reviewer,
            "feedback": feedback,
            "reviewed_result": result,
            "reviewed_files": files,
            "changed": changed,
            "impact": {"status": "PENDING" if decision == "APPROVED" and (changed or feedback.strip()) else "CLEARED"},
        })
        review_digest = self._review_digest(attempt)
        tasks[task_id]["status"] = "COMPLETED" if decision == "APPROVED" else "READY"
        _validation_failure(validate_document(self._validation_plan(plan, artifacts), "plan"), "reviewed plan")
        atomic_write(self._review_path(task_id), review)
        atomic_write(self.plan_path, plan)
        self.checkpoint()
        return {
            "status": "approved" if decision == "APPROVED" else "rework_required",
            "task_id": task_id,
            "changed": changed,
            "feedback": feedback,
            "review_sha256": review_digest,
            "impact_required": attempt["impact"]["status"] == "PENDING",
            "authoritative_result": result,
            "authoritative_files": files,
        }

    def assess_review_impact(self, document: dict[str, Any]) -> dict[str, Any]:
        if set(document) != {"task_id", "review_sha256", "assessment", "reason"}:
            _fail("REVIEW_INVALID", "impact assessment requires task_id, review_sha256, assessment, reason")
        task_id, digest, assessment, reason = (document[key] for key in ("task_id", "review_sha256", "assessment", "reason"))
        if not all(isinstance(value, str) for value in (task_id, digest, assessment, reason)):
            _fail("REVIEW_INVALID", "impact assessment fields must be strings")
        if assessment not in {"CONTINUE", "REPLAN"} or not reason.strip():
            _fail("REVIEW_INVALID", "impact assessment needs CONTINUE or REPLAN with reason")
        self.validate()
        _, _, plan, _, _, _, _ = self._parts()
        review = self._review(task_id)
        if not review or review["attempts"][-1]["decision"] != "APPROVED":
            _fail("REVIEW_MISSING", "no approved review to assess")
        latest = review["attempts"][-1]
        if latest["impact"]["status"] != "PENDING" or digest != self._review_digest(latest):
            _fail("REVIEW_STALE", "impact assessment must match the latest unassessed human review")
        latest["impact"] = {
            "status": "CLEARED" if assessment == "CONTINUE" else "REPLAN_REQUIRED",
            "assessment": assessment,
            "reason": reason,
            "plan_sha256": sha256_document(plan),
        }
        atomic_write(self._review_path(task_id), review)
        return {"status": latest["impact"]["status"], "task_id": task_id, "assessment": assessment}

    def register_record(self, record: dict[str, Any]) -> dict[str, Any]:
        _validation_failure(validate_object("ProjectRecord", record), "record")
        self.validate()
        _, _, _, records, _, _, _ = self._parts()
        if any(item["id"] == record["id"] for item in records):
            _fail("REGISTRY_DUPLICATE", f"record id already exists: {record['id']}")
        records.append(deepcopy(record))
        atomic_write(self.records_path, {"records": records})
        return {"status": "registered", "record_id": record["id"]}

    def register_evidence(self, evidence_record: dict[str, Any]) -> dict[str, Any]:
        _validation_failure(validate_object("EvidenceRecord", evidence_record), "evidence")
        self.validate()
        _, _, _, _, evidence, _, _ = self._parts()
        if any(item["id"] == evidence_record["id"] for item in evidence):
            _fail("REGISTRY_DUPLICATE", f"evidence id already exists: {evidence_record['id']}")
        evidence.append(deepcopy(evidence_record))
        atomic_write(self.evidence_path, {"evidence": evidence})
        return {"status": "registered", "evidence_id": evidence_record["id"], "version": evidence_record["version"]}

    def register_decision(self, decision: dict[str, Any]) -> dict[str, Any]:
        _validation_failure(validate_object("DecisionRecord", decision), "decision")
        self.validate()
        _, _, _, _, evidence, decisions, _ = self._parts()
        if any(item["id"] == decision["id"] for item in decisions):
            _fail("REGISTRY_DUPLICATE", f"decision id already exists: {decision['id']}")
        missing_evidence = set(decision["evidence_refs"]) - {item["id"] for item in evidence}
        if missing_evidence:
            _fail("DECISION_EVIDENCE_UNKNOWN", f"decision references unknown evidence: {sorted(missing_evidence)}")
        if decision["supersedes"] is not None:
            prior = [item for item in decisions if item["id"] == decision["supersedes"]]
            if not prior:
                _fail("DECISION_SUPERSEDES_UNKNOWN", "supersedes references an unknown decision")
            already_superseded = {item["supersedes"] for item in decisions if item["supersedes"] is not None}
            if decision["supersedes"] in already_superseded:
                _fail("DECISION_SUPERSEDES_INACTIVE", "supersedes must reference the active decision in the chain")
            if prior[0]["question"] != decision["question"]:
                _fail("DECISION_QUESTION_MISMATCH", "a replacement decision must answer the same question")
        decisions.append(deepcopy(decision))
        atomic_write(self.decisions_path, {"decisions": decisions})
        return {"status": "registered", "decision_id": decision["id"], "supersedes": decision["supersedes"]}

    def commit_artifact(self, artifact: dict[str, Any], validation_pass: bool = False) -> dict[str, Any]:
        if not validation_pass:
            _fail("VALIDATION_REQUIRED", "artifact commit requires explicit validation PASS")
        _validation_failure(validate_object("Artifact", artifact), "artifact")
        if artifact["status"] != "ACTIVE":
            _fail("ARTIFACT_STATUS_INVALID", "newly committed artifact must be ACTIVE")
        self.validate()
        _, _, plan, records, evidence, decisions, artifacts = self._parts()
        tasks = {task["id"]: task for task in plan["plan"]["tasks"]}
        incomplete = [task_id for task_id in artifact["source_tasks"] if task_id not in tasks or tasks[task_id]["status"] != "COMPLETED"]
        if incomplete:
            _fail("ARTIFACT_SOURCE_INVALID", f"source tasks are not completed: {incomplete}")
        location = Path(str(artifact["location"]))
        resolved = (location if location.is_absolute() else self.root / location).resolve()
        reviewed_sources = 0
        approved_output_match = False
        for task_id in artifact["source_tasks"]:
            review = self._review(task_id)
            if not review:
                continue  # Imported, already-completed tasks predate the review contract.
            reviewed_sources += 1
            latest = review["attempts"][-1]
            if latest["decision"] != "APPROVED":
                _fail("REVIEW_REQUIRED", f"source task {task_id} lacks approval")
            approved = {item["path"]: item["sha256"] for item in latest["reviewed_files"]}
            if not resolved.is_relative_to(self.root):
                _fail("REVIEW_OUTPUT_MISMATCH", "artifact must use the reviewed output inside the product root")
            relative = resolved.relative_to(self.root).as_posix()
            if relative in approved:
                approved_output_match = True
                if not resolved.is_file() or hashlib.sha256(resolved.read_bytes()).hexdigest() != approved[relative]:
                    _fail("REVIEW_OUTPUT_CHANGED", f"approved output changed after review: {relative}")
        if reviewed_sources and not approved_output_match:
            _fail("REVIEW_OUTPUT_MISMATCH", "artifact location is not among the approved source-task outputs")
        if set(artifact["evidence_refs"]) - {item["id"] for item in evidence}:
            _fail("ARTIFACT_SOURCE_INVALID", "artifact references unknown evidence")
        if set(artifact["decision_refs"]) - {item["id"] for item in decisions}:
            _fail("ARTIFACT_SOURCE_INVALID", "artifact references unknown decisions")
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
        allowed_fields = {"change_type", "actions", "plan"}
        if frozenset(change) not in {frozenset(allowed_fields), frozenset(allowed_fields | {"reopen_trigger"})}:
            _fail("REPLAN_INVALID", "replan input must contain change_type, actions, plan and optional reopen_trigger")
        if change["change_type"] not in CHANGE_TYPES or not isinstance(change["actions"], list):
            _fail("REPLAN_INVALID", "unknown change type or malformed actions")
        self.validate()
        manifest, _, old_plan, _, evidence, decisions, artifacts = self._parts()
        reopened_decision = None
        if "reopen_trigger" in change:
            trigger = change["reopen_trigger"]
            if not isinstance(trigger, dict) or set(trigger) != {"decision_id", "trigger", "evidence_refs"}:
                _fail("REOPEN_TRIGGER_INVALID", "reopen_trigger must contain decision_id, trigger and evidence_refs")
            if change["change_type"] != "DECISION_CHANGE":
                _fail("REOPEN_TRIGGER_INVALID", "reopen_trigger requires DECISION_CHANGE")
            superseded = {item["supersedes"] for item in decisions if item["supersedes"] is not None}
            active = [item for item in decisions if item["id"] == trigger["decision_id"] and item["id"] not in superseded]
            if not active:
                _fail("REOPEN_DECISION_INACTIVE", "reopen_trigger must reference an active decision")
            if not isinstance(trigger["trigger"], str) or trigger["trigger"] != active[0]["reopen_trigger"]:
                _fail("REOPEN_TRIGGER_UNDECLARED", "trigger is not declared by the decision")
            if not isinstance(trigger["evidence_refs"], list) or any(not isinstance(item, str) for item in trigger["evidence_refs"]):
                _fail("REOPEN_TRIGGER_INVALID", "reopen_trigger.evidence_refs must be a list of ids")
            missing_evidence = set(trigger["evidence_refs"]) - {item["id"] for item in evidence}
            if missing_evidence:
                _fail("REOPEN_EVIDENCE_UNKNOWN", f"reopen trigger references unknown evidence: {sorted(missing_evidence)}")
            reopened_decision = trigger["decision_id"]
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
            if kind == "ADD" and new_tasks[target]["status"] in {"COMPLETED", "WAITING_USER", "RUNNING"}:
                _fail("REVIEW_REQUIRED", f"new task {target} cannot bypass execution and human review")
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
        return {
            "status": "replanned",
            "change_type": change["change_type"],
            "reopened_decision": reopened_decision,
            "dag_changed": dag_changed,
            "plan_version": new_plan["plan"]["version"],
        }
