# Replan and Recovery

Do not use project-wide rollback as the default recovery model.

When a material change or non-retryable failure occurs:

`Change → Replan → Preserve valid work → Invalidate affected work → Add/Cancel tasks → Continue`

本文件只在 [Planner 的 Replan Trigger Contract](planner.md#replan-trigger-contract) 已得到 `LOCAL_REPLAN` 或 `PROFILE_REPLAN` 后加载。`INPUT_CHANGE` 必须是有效 Profile 与 Plan baseline 建立后的新输入，并且已证明影响既有工作；初始请求、初始上下文、初始证据、首次 Profile 或首次 Plan 均不是 `INPUT_CHANGE`。

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

### Decision Reopen Trigger

当新证据或时效条件命中当前 DecisionRecord 的 `reopen_trigger` 时，以 `DECISION_CHANGE` 触发 Replan。持久运行时的可选 `reopen_trigger` 输入包含：

```yaml
reopen_trigger:
  decision_id:
  trigger:
  evidence_refs: []
```

`decision_id` 必须是当前未被 supersede 的决策，`trigger` 必须与该决策预先声明的 `reopen_trigger` 完全一致，`evidence_refs` 必须指向已登记证据。按本次 Replan 的 `change_type` 判定：只有 `DECISION_CHANGE` 且命中既有决策声明的触发条件时，`reopen_trigger` 才能是上述对象；所有其他 change type（包括 `SCOPE_CHANGE`）一律为 `null`。交付目标或范围变化需要重算 Profile，不等于自动重开 Decision。Replan 只重新打开受影响问题并调整任务；新的选择完成后另建 DecisionRecord 并以 `supersedes` 连接旧决策。未命中触发条件时，不为追求“重新评审”而机械推翻有效决策。
