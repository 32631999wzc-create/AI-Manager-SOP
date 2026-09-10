"""Lightweight models for the eight canonical runtime objects."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Task:
    id: Any
    name: Any
    goal: Any
    type: Any
    status: Any
    priority: Any
    lifecycle_node: Any
    execution_depth: Any
    dependencies: Any
    required_inputs: Any
    required_capabilities: Any
    expected_output: Any
    acceptance_criteria: Any
    context_requirements: Any
    artifact_requirements: Any
    retry_policy: Any


@dataclass(frozen=True)
class ProjectRecord:
    id: Any
    type: Any
    topic: Any
    content: Any
    status: Any
    source: Any
    version: Any
    affected_scope: Any


@dataclass(frozen=True)
class Artifact:
    id: Any
    type: Any
    name: Any
    version: Any
    status: Any
    summary: Any
    location: Any
    source_tasks: Any
    source_records: Any
    dependencies: Any


@dataclass(frozen=True)
class RuntimeSnapshot:
    plan_version: Any
    task_states: Any
    active_artifacts: Any
    active_records: Any
    unresolved_items: Any


@dataclass(frozen=True)
class AssignmentScope:
    mode: Any
    requested_scope: Any
    excluded_scope: Any
    expected_deliverables: Any
    ownership_boundary: Any


@dataclass(frozen=True)
class NodeProfile:
    node: Any
    status: Any
    level: Any
    depth: Any
    scope_role: Any
    active_capabilities: Any
    reused_artifacts: Any
    gaps: Any
    reasons: Any
    external_project_requirement: Any


@dataclass(frozen=True)
class Plan:
    version: Any
    objective: Any
    tasks: Any
    dependencies: Any
    critical_path: Any
    assumptions: Any


@dataclass(frozen=True)
class TaskContextPack:
    task: Any
    relevant_facts: Any
    relevant_decisions: Any
    relevant_constraints: Any
    relevant_artifacts: Any
    recent_changes: Any
    assumptions: Any
    unresolved_items: Any
    allowed_actions: Any
    available_tools: Any


OBJECT_MODELS = {
    cls.__name__: cls for cls in (
        Task, ProjectRecord, Artifact, RuntimeSnapshot, AssignmentScope,
        NodeProfile, Plan, TaskContextPack,
    )
}
