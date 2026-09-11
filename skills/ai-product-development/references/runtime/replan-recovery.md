# Replan and Recovery

Do not use project-wide rollback as the default recovery model.

When a material change or non-retryable failure occurs:

`Change → Replan → Preserve valid work → Invalidate affected work → Add/Cancel tasks → Continue`

## 12.1 Change Types

Use only:

- `INPUT_CHANGE`
- `ARTIFACT_CHANGE`
- `TASK_FAILURE`
- `DECISION_CHANGE`
- `SCOPE_CHANGE`

This is a logical event structure, not a requirement for an event bus.

## 12.2 Replan Actions

Replan may only apply these basic actions:

- `PRESERVE`
- `OUTDATE`
- `ADD`
- `CANCEL`

Preserve unaffected work by default.

## 12.3 Local vs Profile Replan

Use `LOCAL REPLAN` for task failure, artifact changes, debugging fixes, and local requirement changes.

Use `PROFILE REPLAN` when delivery target, assignment scope, or a major project constraint changes. Recalculate affected node profiles, but continue to reuse valid existing records and artifacts.

Create a new plan version only when the task DAG structure materially changes. Normal state changes such as `RUNNING → COMPLETED` do not require a new plan version.

If user input is required, create one clear `HUMAN_CONFIRM` task, block only the affected tasks, and resume when answered.

## Load With

- 调整任务或 DAG 前读取 [Planner](planner.md)；构造对象时按 Kernel 读取相应 schema。
- 判断正式产物失效、替代或版本建议时读取 [Registry and Versioning](registry-versioning.md#112-artifact-commit-rules)，包括只提出变更建议而不实际提交的情况。
- 交付目标、范围或主要约束变化而触发 Profile Replan 时读取 [Execution Profile](execution-profile.md)；Local Replan 不自动加载全部节点。

## Local Persistence

持久项目的变更使用 [Continuous Project Runtime](../../scripts/project_runtime/README.md) `replan` 输入完整新计划及 change/action 清单。运行时校验每个任务变化都有对应 action，并执行本节的计划版本规则；它不自行判断产品影响范围。
