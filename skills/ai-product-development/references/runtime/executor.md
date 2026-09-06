# Executor

The Executor performs a ready task without changing project scope.

## 10.1 Worker Types

Use the minimum necessary abstraction:

- `CODE`
- `TOOL`
- `SKILL`
- `LLM`
- `HUMAN`

Do not create permanent specialist Agents when capability metadata or a normal task instruction is sufficient.

## 10.2 Worker Selection

Prefer the lowest-complexity reliable method:

`deterministic code/rule → existing tool/skill → LLM → human when authorization, high-risk judgment, or unresolved conflict requires it`

A task normally has one primary worker. If different capabilities are independently required, split the task instead of making workers freely negotiate.

## 10.3 Execution

`READY Task → Build Context → Select Worker → Execute → Validate → Task Result`

Workers must not directly:

- change assignment scope;
- change the plan;
- turn assumptions into facts;
- overwrite formal artifacts;
- write long-term project records without validation/commit.

## 10.4 Validation

Use two layers only:

### Structural Validation

Prefer deterministic checks for schema, required fields, file existence, tests, formats, and explicit constraints.

### Acceptance Validation

Check the task's acceptance criteria using the simplest adequate method: rule/code, LLM review, or human review.

Do not use LLM Judge when deterministic validation is sufficient.

## 10.5 Failure

Classify only:

- `EXECUTION_ERROR`
- `VALIDATION_ERROR`
- `BLOCKED`

Allow a small local retry only for clearly retryable failures. Do not create a separate recovery workflow or retry indefinitely.
