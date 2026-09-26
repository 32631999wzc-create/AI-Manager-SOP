"""Strict output shape for the planning-only behavioral trace.

This constrains JSON syntax and canonical fields, not scenario decisions.
Business values are still checked by the runtime validator and grader.
"""

from runtime_validation.validators import (
    DELIVERY_TARGETS, PROJECT_MODES, NODE_STATUS, NODE_LEVEL, NODE_DEPTH,
    SCOPE_ROLE, TASK_STATUS, PRIORITY, DEPENDENCY_TYPES, NODES, GATE_RESULTS,
)


def _object(properties):
    return {
        "type": "object",
        "properties": properties,
        "required": list(properties),
        "additionalProperties": False,
    }


def _array(item):
    return {"type": "array", "items": item}


def _enum(values):
    return {"type": "string", "enum": sorted(values)}


def output_schema():
    string = {"type": "string"}
    boolean = {"type": "boolean"}
    strings = _array(string)
    scope = _object({
        "mode": string, "requested_scope": strings, "excluded_scope": strings,
        "expected_deliverables": strings, "ownership_boundary": strings,
    })
    node = _object({
        "node": _enum(NODES), "status": _enum(NODE_STATUS),
        "level": _enum(NODE_LEVEL), "depth": _enum(NODE_DEPTH),
        "scope_role": _enum(SCOPE_ROLE), "active_capabilities": strings,
        "reused_artifacts": strings, "gaps": strings, "reasons": strings,
        "external_project_requirement": {"type": ["string", "null"]},
    })
    context = _object({
        "existing_repository_modification": boolean, "verified_design": boolean,
        "acceptance_criteria_defined": boolean, "production_release": boolean,
        "release_execution": boolean, "monitoring_covered": boolean,
        "release_readiness": _enum(GATE_RESULTS),
    })
    profile = _object({
        "delivery_target": _enum(DELIVERY_TARGETS),
        "project_mode": _enum(PROJECT_MODES),
        "assignment_scope": scope, "nodes": _array(node),
        "validation_context": context,
    })
    task = _object({
        "id": string, "name": string, "goal": string, "type": string,
        "status": _enum(TASK_STATUS), "priority": _enum(PRIORITY),
        "lifecycle_node": _enum(NODES),
        "execution_depth": _enum(NODE_DEPTH), "dependencies": strings,
        "required_inputs": strings, "required_capabilities": strings,
        "expected_output": string, "acceptance_criteria": strings,
        "context_requirements": strings, "artifact_requirements": strings,
        "retry_policy": string,
    })
    dependency = _object({
        "from": string, "to": string, "type": _enum(DEPENDENCY_TYPES),
    })
    plan = _object({
        "version": string, "objective": string, "tasks": _array(task),
        "dependencies": _array(dependency), "critical_path": strings,
        "assumptions": strings,
    })
    plan_document = _object({
        "plan": plan, "available_inputs": strings, "artifacts": _array(string),
        "gates": _object({}), "blocked_inputs": strings,
        "write_targets": _object({}),
    })
    return _object({
        "document": _object({"profile": profile, "plan": plan_document}),
        "claims": _object({
            "assignment_complete": boolean, "external_write_performed": boolean,
        }),
    })
