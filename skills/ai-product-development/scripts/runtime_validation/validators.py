"""Deterministic validators traced to the Phase 2 validation contract."""

from dataclasses import fields
from typing import Any, Iterable
import re

from .errors import ValidationError
from .models import OBJECT_MODELS


NODES = [
    "Qualification", "Cognition", "Product Definition & Scope", "Solution Design",
    "Implementation", "Validation & Iteration", "Release & Operation", "Retrospective",
]
NODE_STATUS = {"NOT_STARTED", "ACTIVE", "SATISFIED", "BLOCKED", "SKIPPED", "OUTDATED"}
NODE_LEVEL = {"REQUIRED", "LIGHT", "OPTIONAL", "SKIP"}
NODE_DEPTH = {"FULL", "MINIMAL", "VERIFY", "SKIP"}
SCOPE_ROLE = {"PRIMARY", "SUPPORTING", "OUT_OF_SCOPE"}
TASK_STATUS = {"NOT_STARTED", "READY", "RUNNING", "COMPLETED", "BLOCKED", "WAITING_USER", "FAILED", "SKIPPED", "OUTDATED", "CANCELLED"}
PRIORITY = {"P0", "P1", "P2", "P3"}
DEPENDENCY_TYPES = {"HARD", "DATA", "DECISION", "GATE"}
DELIVERY_TARGETS = {"PROTOTYPE", "DEMO", "MVP", "ENTERPRISE", "UNDECIDED"}
PROJECT_MODES = {"GREENFIELD", "BROWNFIELD", "HYBRID"}
GATE_RESULTS = {"PASS", "PASS_WITH_ASSUMPTIONS", "BLOCKED"}

ENUMS = {
    "Task.status": TASK_STATUS,
    "Task.priority": PRIORITY,
    "Task.lifecycle_node": set(NODES),
    "Task.execution_depth": NODE_DEPTH,
    "ProjectRecord.type": {"FACT", "DECISION", "CONSTRAINT", "ASSUMPTION"},
    "ProjectRecord.status": {"ACTIVE", "SUPERSEDED", "REJECTED"},
    "Artifact.status": {"ACTIVE", "OUTDATED", "SUPERSEDED", "ARCHIVED"},
    "AssignmentScope.mode": {"FULL_PROJECT", "PARTIAL_PROJECT"},
    "NodeProfile.node": set(NODES),
    "NodeProfile.status": NODE_STATUS,
    "NodeProfile.level": NODE_LEVEL,
    "NodeProfile.depth": NODE_DEPTH,
    "NodeProfile.scope_role": SCOPE_ROLE,
}

LIST_FIELDS = {
    "Task": {"dependencies", "required_inputs", "required_capabilities", "acceptance_criteria", "context_requirements", "artifact_requirements"},
    "ProjectRecord": {"affected_scope"},
    "Artifact": {"source_tasks", "source_records", "dependencies"},
    "AssignmentScope": {"requested_scope", "excluded_scope", "expected_deliverables", "ownership_boundary"},
    "NodeProfile": {"active_capabilities", "reused_artifacts", "gaps", "reasons"},
    "Plan": {"tasks", "dependencies", "critical_path", "assumptions"},
    "TaskContextPack": {"relevant_facts", "relevant_decisions", "relevant_constraints", "relevant_artifacts", "recent_changes", "assumptions", "unresolved_items", "allowed_actions", "available_tools"},
}


def _error(errors: list[ValidationError], code: str, path: str, message: str) -> None:
    errors.append(ValidationError(path=path, code=code, message=message))


def _mapping(value: Any, path: str, errors: list[ValidationError]) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        _error(errors, "TYPE_MAPPING", path, "must be a mapping")
        return None
    return value


def _string_set(value: Any, path: str, errors: list[ValidationError]) -> set[str]:
    """Return valid string entries while reporting malformed list values."""
    if not isinstance(value, list):
        _error(errors, "TYPE_LIST", path, "must be a list")
        return set()
    result = set()
    for index, item in enumerate(value):
        if not isinstance(item, str):
            _error(errors, "TYPE_LIST", f"{path}[{index}]", "list entries must be strings")
        else:
            result.add(item)
    return result


def _model(name: str, value: Any, path: str, errors: list[ValidationError]):
    data = _mapping(value, path, errors)
    if data is None:
        return None
    cls = OBJECT_MODELS[name]
    expected = {f.name for f in fields(cls)}
    for key in sorted(expected - set(data)):
        _error(errors, "FIELD_MISSING", f"{path}.{key}", "required field is missing")
    for key in sorted(set(data) - expected):
        _error(errors, "FIELD_UNKNOWN", f"{path}.{key}", "field is not defined by the canonical object")
    if expected - set(data):
        return None
    for key in LIST_FIELDS.get(name, set()):
        if not isinstance(data[key], list):
            _error(errors, "TYPE_LIST", f"{path}.{key}", "must be a list")
    for key, allowed in ENUMS.items():
        object_name, field = key.split(".")
        if object_name == name and (not isinstance(data[field], str) or data[field] not in allowed):
            _error(errors, "ENUM_INVALID", f"{path}.{field}", f"must be one of {sorted(allowed)}")
    return cls(**{key: data[key] for key in expected})


def validate_object(name: str, value: Any, path: str | None = None) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if name not in OBJECT_MODELS:
        return [ValidationError(path=path or name, code="OBJECT_UNKNOWN", message="unknown runtime object")]
    model = _model(name, value, path or name, errors)
    if model is None:
        return sorted(errors)
    root = path or name
    if name == "Artifact" and (not isinstance(model.version, str) or not re.fullmatch(r"v[1-9]\d*", model.version)):
        _error(errors, "VERSION_INVALID", f"{root}.version", "formal artifact version must use vN")
    if name == "Task":
        for field_name in ("id", "name", "goal", "expected_output"):
            if not isinstance(getattr(model, field_name), str) or not getattr(model, field_name).strip():
                _error(errors, "VALUE_EMPTY", f"{root}.{field_name}", "must be a non-empty string")
        if not model.acceptance_criteria:
            _error(errors, "ACCEPTANCE_REQUIRED", f"{root}.acceptance_criteria", "task requires explicit acceptance criteria")
    return sorted(errors)


def _active(node) -> bool:
    return node.level != "SKIP" and node.depth != "SKIP" and node.scope_role != "OUT_OF_SCOPE"


def validate_profile(document: dict[str, Any]) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if _mapping(document, "$", errors) is None:
        return sorted(errors)
    allowed = {"delivery_target", "project_mode", "assignment_scope", "nodes", "validation_context"}
    for key in sorted(allowed - set(document)):
        _error(errors, "FIELD_MISSING", key, "profile validation input requires this field")
    for key in sorted(set(document) - allowed):
        _error(errors, "FIELD_UNKNOWN", key, "unknown profile validation input field")
    if errors:
        return sorted(errors)
    if not isinstance(document["delivery_target"], str) or document["delivery_target"] not in DELIVERY_TARGETS:
        _error(errors, "ENUM_INVALID", "delivery_target", f"must be one of {sorted(DELIVERY_TARGETS)}")
    if not isinstance(document["project_mode"], str) or document["project_mode"] not in PROJECT_MODES:
        _error(errors, "ENUM_INVALID", "project_mode", f"must be one of {sorted(PROJECT_MODES)}")
    errors.extend(validate_object("AssignmentScope", document["assignment_scope"], "assignment_scope"))
    if not isinstance(document["nodes"], list):
        _error(errors, "TYPE_LIST", "nodes", "must be a list")
        return sorted(errors)
    nodes = []
    for index, value in enumerate(document["nodes"]):
        before = len(errors)
        node = _model("NodeProfile", value, f"nodes[{index}]", errors)
        if node is not None and len(errors) == before:
            nodes.append(node)
    names = [node.node for node in nodes]
    if len(document["nodes"]) != len(NODES) or names != NODES:
        _error(errors, "PROFILE_NODE_SET", "nodes", "must contain the eight lifecycle nodes exactly once in canonical order")
    for index, node in enumerate(nodes):
        if (node.level == "SKIP" or node.depth == "SKIP") and not node.reasons:
            _error(errors, "SKIP_REASON_REQUIRED", f"nodes[{index}].reasons", "every SKIP requires a reason")
    context = _mapping(document["validation_context"], "validation_context", errors)
    if context is None:
        return sorted(errors)
    context_fields = {
        "existing_repository_modification", "verified_design", "acceptance_criteria_defined",
        "production_release", "release_execution", "monitoring_covered", "release_readiness",
    }
    for key in sorted(context_fields - set(context)):
        _error(errors, "FIELD_MISSING", f"validation_context.{key}", "validation context requires this field")
    for key in sorted(set(context) - context_fields):
        _error(errors, "FIELD_UNKNOWN", f"validation_context.{key}", "unknown validation context field")
    if errors or len(nodes) != len(NODES):
        return sorted(errors)
    by_name = {node.node: node for node in nodes}
    if not isinstance(context["release_readiness"], str) or context["release_readiness"] not in GATE_RESULTS:
        _error(errors, "ENUM_INVALID", "validation_context.release_readiness", f"must be one of {sorted(GATE_RESULTS)}")
    if context["existing_repository_modification"] and by_name["Cognition"].level != "REQUIRED":
        _error(errors, "PROFILE_COGNITION_REQUIRED", "nodes[1]", "existing repository modification requires Cognition")
    design = by_name["Solution Design"]
    design_at_least_light = design.level in {"LIGHT", "REQUIRED"} and design.depth != "SKIP"
    if _active(by_name["Implementation"]) and not context["verified_design"] and not design_at_least_light:
        _error(errors, "PROFILE_DESIGN_REQUIRED", "nodes[3]", "active Implementation requires at least minimal Solution Design when design is unverified")
    if _active(by_name["Validation & Iteration"]) and not context["acceptance_criteria_defined"]:
        evaluation_depth = design.depth in {"MINIMAL", "FULL"}
        capabilities = {
            item.strip().casefold()
            for item in design.active_capabilities
            if isinstance(item, str)
        }
        evaluation_components = {
            "evaluation task", "cases / dataset", "metrics", "judge strategy", "pass criteria",
        }
        evaluation_active = (
            capabilities & {"evaluation design", "评估设计"}
            or evaluation_components <= capabilities
        )
        if not design_at_least_light or not evaluation_depth or not evaluation_active:
            _error(errors, "PROFILE_EVALUATION_DESIGN_REQUIRED", "nodes[3].active_capabilities", "Validation without acceptance criteria requires active Evaluation Design")
    if context["production_release"]:
        if not _active(by_name["Validation & Iteration"]):
            _error(errors, "PROFILE_RELEASE_VALIDATION_REQUIRED", "nodes[5]", "production release requires Validation & Iteration")
        if not _active(by_name["Release & Operation"]):
            _error(errors, "PROFILE_RELEASE_NODE_REQUIRED", "nodes[6]", "production release requires Release & Operation")
        release_node = by_name["Release & Operation"]
        monitoring_planned = any(
            "monitor" in str(item).casefold() or "监控" in str(item)
            for item in release_node.active_capabilities + release_node.gaps
        )
        if not context["monitoring_covered"] and not monitoring_planned and not release_node.external_project_requirement:
            _error(errors, "PROFILE_MONITORING_REQUIRED", "nodes[6]", "production monitoring must be covered, planned in the active release node, or externalized")
        if context["release_execution"] and context["release_readiness"] == "BLOCKED":
            _error(errors, "PROFILE_RELEASE_GATE_BLOCKED", "validation_context.release_readiness", "production release cannot proceed through a blocked Release Readiness gate")
    return sorted(errors)


def _dependency_edges(plan, tasks, errors: list[ValidationError]):
    edges = []
    ids = {task.id for task in tasks}
    for index, dep in enumerate(plan.dependencies):
        path = f"plan.dependencies[{index}]"
        if not isinstance(dep, dict) or set(dep) != {"from", "to", "type"}:
            _error(errors, "DEPENDENCY_SHAPE", path, "must contain exactly from, to and type")
            continue
        if not isinstance(dep["type"], str) or dep["type"] not in DEPENDENCY_TYPES:
            _error(errors, "DEPENDENCY_TYPE_INVALID", f"{path}.type", f"must be one of {sorted(DEPENDENCY_TYPES)}")
        if not isinstance(dep["to"], str) or dep["to"] not in ids:
            _error(errors, "DEPENDENCY_REFERENCE_UNKNOWN", f"{path}.to", "references an unknown task")
        if dep["type"] == "GATE":
            if not isinstance(dep["from"], str) or not dep["from"].strip():
                _error(errors, "DEPENDENCY_REFERENCE_UNKNOWN", f"{path}.from", "gate dependency requires a gate name")
        elif not isinstance(dep["from"], str) or dep["from"] not in ids:
            _error(errors, "DEPENDENCY_REFERENCE_UNKNOWN", f"{path}.from", "references an unknown task")
        if isinstance(dep["to"], str) and dep["to"] in ids and (
            dep["type"] == "GATE" or isinstance(dep["from"], str) and dep["from"] in ids
        ):
            edges.append((dep["from"], dep["to"], dep["type"]))
    return edges


def _has_path(start: str, target: str, edges: Iterable[tuple[str, str, str]]) -> bool:
    graph: dict[str, set[str]] = {}
    for source, destination, _ in edges:
        graph.setdefault(source, set()).add(destination)
    pending, seen = [start], set()
    while pending:
        current = pending.pop()
        if current == target:
            return True
        if current not in seen:
            seen.add(current)
            pending.extend(graph.get(current, ()))
    return False


def validate_plan(document: dict[str, Any]) -> list[ValidationError]:
    errors: list[ValidationError] = []
    if _mapping(document, "$", errors) is None:
        return sorted(errors)
    allowed = {"plan", "available_inputs", "artifacts", "gates", "blocked_inputs", "write_targets"}
    for key in sorted(allowed - set(document)):
        _error(errors, "FIELD_MISSING", key, "plan validation input requires this field")
    for key in sorted(set(document) - allowed):
        _error(errors, "FIELD_UNKNOWN", key, "unknown plan validation input field")
    if errors:
        return sorted(errors)
    plan = _model("Plan", document["plan"], "plan", errors)
    if plan is None:
        return sorted(errors)
    if not isinstance(plan.version, (str, int)) or str(plan.version).strip() == "":
        _error(errors, "PLAN_VERSION_REQUIRED", "plan.version", "plan version is required")
    if not isinstance(plan.objective, str) or not plan.objective.strip():
        _error(errors, "PLAN_OBJECTIVE_REQUIRED", "plan.objective", "plan objective is required")
    tasks = []
    for index, value in enumerate(plan.tasks if isinstance(plan.tasks, list) else []):
        task_errors = validate_object("Task", value, f"plan.tasks[{index}]")
        errors.extend(task_errors)
        if not task_errors:
            tasks.append(OBJECT_MODELS["Task"](**value))
    ids = [task.id for task in tasks]
    for duplicate in sorted({task_id for task_id in ids if ids.count(task_id) > 1}):
        _error(errors, "TASK_ID_DUPLICATE", "plan.tasks", f"duplicate task id: {duplicate}")
    edges = _dependency_edges(plan, tasks, errors)
    for source, destination, _ in edges:
        if _has_path(destination, source, edges):
            _error(errors, "PLAN_CYCLE", "plan.dependencies", f"cycle includes {source} -> {destination}")
            break
    by_id = {task.id: task for task in tasks}
    available_inputs = _string_set(document["available_inputs"], "available_inputs", errors)
    blocked_inputs = _string_set(document["blocked_inputs"], "blocked_inputs", errors)
    artifacts = {}
    if not isinstance(document["artifacts"], list):
        _error(errors, "TYPE_LIST", "artifacts", "must be a list")
    else:
        for index, value in enumerate(document["artifacts"]):
            artifact_errors = validate_object("Artifact", value, f"artifacts[{index}]")
            errors.extend(artifact_errors)
            if not artifact_errors and isinstance(value["id"], str) and value["id"].strip():
                artifacts[value["id"]] = value
            elif not artifact_errors:
                _error(errors, "VALUE_EMPTY", f"artifacts[{index}].id", "must be a non-empty string")
    gates = _mapping(document["gates"], "gates", errors) or {}
    for gate, result in gates.items():
        if not isinstance(result, str) or result not in GATE_RESULTS:
            _error(errors, "ENUM_INVALID", f"gates.{gate}", f"must be one of {sorted(GATE_RESULTS)}")
    for index, task in enumerate(tasks):
        incoming = [(source, kind) for source, destination, kind in edges if destination == task.id]
        declared = _string_set(task.dependencies, f"plan.tasks[{index}].dependencies", errors)
        edge_ids = {source for source, _ in incoming}
        if declared != edge_ids:
            _error(errors, "TASK_DEPENDENCY_MISMATCH", f"plan.tasks[{index}].dependencies", "must match incoming Plan dependencies")
        if task.status == "READY":
            for source, kind in incoming:
                if kind in {"HARD", "DATA", "DECISION"} and by_id[source].status != "COMPLETED":
                    _error(errors, "READY_DEPENDENCY_UNMET", f"plan.tasks[{index}].status", f"blocking dependency is not completed: {source}")
                if kind == "GATE" and gates.get(source) not in {"PASS", "PASS_WITH_ASSUMPTIONS"}:
                    _error(errors, "READY_GATE_UNMET", f"plan.tasks[{index}].status", f"gate is not passed: {source}")
            required_inputs = _string_set(task.required_inputs, f"plan.tasks[{index}].required_inputs", errors)
            if required_inputs - available_inputs or required_inputs & blocked_inputs:
                _error(errors, "READY_INPUT_UNMET", f"plan.tasks[{index}].status", "required input is missing or blocked")
            artifact_requirements = _string_set(task.artifact_requirements, f"plan.tasks[{index}].artifact_requirements", errors)
            missing_artifacts = [artifact_id for artifact_id in artifact_requirements if artifact_id not in artifacts or artifacts[artifact_id]["status"] != "ACTIVE"]
            if missing_artifacts:
                _error(errors, "READY_ARTIFACT_UNMET", f"plan.tasks[{index}].status", f"required ACTIVE artifact missing: {sorted(missing_artifacts)}")
        if not task.acceptance_criteria:
            _error(errors, "ACCEPTANCE_REQUIRED", f"plan.tasks[{index}].acceptance_criteria", "task requires explicit acceptance criteria")
    write_targets = _mapping(document["write_targets"], "write_targets", errors) or {}
    target_sets = {}
    for task_id, targets in write_targets.items():
        if task_id not in by_id:
            _error(errors, "DEPENDENCY_REFERENCE_UNKNOWN", f"write_targets.{task_id}", "references an unknown task")
        target_sets[task_id] = _string_set(targets, f"write_targets.{task_id}", errors)
    for index, left in enumerate(tasks):
        for right in tasks[index + 1:]:
            shared_targets = target_sets.get(left.id, set()) & target_sets.get(right.id, set())
            if left.status in {"READY", "RUNNING"} and right.status in {"READY", "RUNNING"} and shared_targets:
                if not _has_path(left.id, right.id, edges) and not _has_path(right.id, left.id, edges):
                    _error(errors, "PARALLEL_ARTIFACT_CONFLICT", "write_targets", f"parallel tasks write the same formal artifact version: {left.id}, {right.id}")
    for index, task_id in enumerate(plan.critical_path):
        if not isinstance(task_id, str) or task_id not in by_id:
            _error(errors, "CRITICAL_PATH_UNKNOWN", f"plan.critical_path[{index}]", "references an unknown task")
    return sorted(set(errors))


def validate_document(document: dict[str, Any], mode: str) -> list[ValidationError]:
    if not isinstance(document, dict):
        return [ValidationError(path="$", code="TYPE_MAPPING", message="must be a mapping")]
    if mode == "profile":
        return validate_profile(document)
    if mode == "plan":
        return validate_plan(document)
    if mode == "combined":
        if set(document) != {"profile", "plan"}:
            return [ValidationError(path="$", code="COMBINED_SHAPE", message="combined document must contain exactly profile and plan")]
        return sorted(validate_profile(document["profile"]) + validate_plan(document["plan"]))
    if mode == "objects":
        errors = []
        for name, value in document.items():
            errors.extend(validate_object(name, value))
        return sorted(errors)
    return [ValidationError(path="$", code="MODE_UNKNOWN", message="unknown validation mode")]
