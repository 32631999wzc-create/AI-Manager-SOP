# Qualification

## Purpose

determine delivery target, assignment scope, usable context, blocking gaps, and execution depth.

## Activation Conditions

Run Qualification before substantial work unless the required information is already explicit in the conversation or supplied materials.

Qualification 是生成初始 Profile 的前置检查；完成后由 [Execution Profile](../runtime/execution-profile.md) 记录节点深度。

## Required Inputs

原文未单列固定输入清单；按下述 Procedure 与当前任务的 required_inputs 获取相关材料。

## Capabilities

delivery target, assignment scope, context intake, completeness check, clarification, profile generation.

## Procedure

### 5.0 Initial Response Protocol

When starting a new project or major assignment:

1. If the delivery target is already explicit, do not ask again. Otherwise ask the user to choose `PROTOTYPE`, `DEMO`, `MVP`, `ENTERPRISE`, or `UNDECIDED`.
2. If product/project materials are already available, inspect them before asking detailed questions. Otherwise ask the user to provide the best available product context document, repository, prototype description, or equivalent source material.
3. Infer Assignment Scope from the request when clear. Ask only when ownership or expected deliverables are ambiguous enough to change the plan.
4. Perform completeness classification after inspection, then ask only blocking clarification questions.
5. Generate the Execution Profile and concise Plan Preview before substantial execution.

Do not repeat questions whose answers are already present in the conversation or supplied materials.

### Delivery Target

按 [Execution Profile — Delivery Target](../runtime/execution-profile.md) 判断交付目标。

### Assignment Scope

按 [Execution Profile — Assignment Scope](../runtime/execution-profile.md) 确定本次任务边界。

### 5.3 Inspect Product Context

Prefer existing source material over repeated questioning. Relevant inputs may include:

- PRD / BRD / project description
- prototype or design specification
- repository
- architecture or technical design
- API documentation
- database schema
- datasets or knowledge assets
- evaluation datasets or reports
- deployment configuration
- user research, feedback, or historical decisions

Build a concise `Product Context Snapshot` covering only known information that affects the task.

### 5.4 Classify Missing Information

Every important field is one of:

- `KNOWN`
- `MISSING_NON_BLOCKING`
- `MISSING_BLOCKING`

Blocking status depends on delivery target and current assignment. Do not use a fixed questionnaire.

Ask only the smallest set of questions required to unblock reliable planning.

### Qualification Gate

执行 [Qualification Gate](../runtime/gates.md#qualification-gate)。

## Outputs

`Product Context Snapshot`, `Execution Profile`, explicit assumptions if any.

## Completion Criteria

delivery target and scope are sufficiently clear; blocking inputs are resolved or explicitly block execution.

## Dependencies

执行深度由 [Execution Profile](../runtime/execution-profile.md) 计算。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。
