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

每个已确定的 Planner Task 产出并完成必要验证后，向用户或指定审核人提交该 Task 的结果、验证结论、未决项及需要确认的下一步，并停止执行；不得在同一轮继续其他 READY Task（包括可并行的 Task）。明确获准后才将该 Task 记为 `COMPLETED`、按规则提交正式产物并继续下一 Task。等待期间如使用持续项目 Runtime，将当前 Task 记为 `WAITING_USER` 并 checkpoint；未收到回复不推定通过。若审核要求修改，先在该 Task 内返工并重新交审；只有范围或依赖发生实质变化时才按 Replan 合同调整计划。此处审核是 Task 交接，不新增顶层 Gate 或审批工作流引擎。

审核决定必须来自真实用户或其指定责任人，执行者不得代写批准回执。批准后重新读取审核回执与当前输出，对比提交时快照；人工修改的内容和新观点优先于旧草稿，禁止用执行者先前版本覆盖。批准附带修改或意见时，先判断对现有 Task、Decision、Artifact、验收或范围的影响：无实质影响则记录原因并继续；有实质影响则按 Replan 合同只调整受影响工作。驳回时读取全部修改意见，在同一 Task 上返工并重新提交，不启动后续 Task。若已批准文件又发生变化，暂停并请人工确认最新版，不能静默回滚或继续使用旧版。

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
