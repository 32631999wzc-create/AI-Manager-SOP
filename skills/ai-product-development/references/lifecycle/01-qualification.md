# Qualification

## Purpose

determine delivery target, assignment scope, usable context, blocking gaps, and execution depth.

## Activation Conditions

Run Qualification before substantial work unless the required information is already explicit in the conversation or supplied materials.

Qualification 是生成初始 Profile 的前置检查；完成后由 [Execution Profile](../runtime/execution-profile.md) 记录节点深度。

## Required Inputs

至少需要当前请求或目标，以及用户已经提供的材料。可用输入包括交付物期望、交付目标、Assignment Scope、现有资产、约束和风险；缺失项在本节点分类，不要求先填写固定问卷。

## Required Decisions / State

- 交付目标为 `PROTOTYPE | DEMO | MVP | ENTERPRISE | UNDECIDED`；
- Assignment Scope、预期交付物、排除项和 ownership boundary 明确；
- 相关材料与资产按 [Execution Profile](../runtime/execution-profile.md) 分类；
- 重要输入标记为 `KNOWN | MISSING_NON_BLOCKING | MISSING_BLOCKING`，事实与假设分开；
- 风险筛查、依赖闭包和 Qualification Gate 已得到可解释结论。

## Capability Routing

仅当 Qualification 的 gap 需要专业判断时调用：价值或投资合理性使用[商业论证与优先级](../capabilities/business-case/SKILL.md)；问题仍不清楚时使用[用户与机会发现](../capabilities/discovery/SKILL.md)；AI 是否适用不清楚时使用[AI 可行性与原型](../capabilities/ai-feasibility/SKILL.md)；存在敏感、高影响或滥用风险时使用[责任 AI、安全与风险](../capabilities/responsible-ai/SKILL.md)。若当前范围已明确排除敏感、高影响、外部工具和自动行动，且没有相反证据，不得仅为重述该边界而调用 Responsible AI。Capability 提供证据，Qualification Gate 负责推进判断。

## Outputs

**Primary outputs:** `Product Context Snapshot`, `Execution Profile`, explicit assumptions if any.

- Qualification Gate 结果；
- 明确的假设、阻塞输入和最少澄清问题；
- Gate 允许继续时的简短 Plan Preview。

## Completion Criteria

**Completion:** delivery target and scope are sufficiently clear; blocking inputs are resolved or explicitly block execution.

- 重要信息均已分类，假设与事实分离；
- Qualification Gate 已记录为 `PASS`、`PASS_WITH_ASSUMPTIONS` 或 `BLOCKED`；
- 后续节点、执行深度和必要依赖已明确。

## Dependencies

执行深度、资产状态和依赖闭包由 [Execution Profile](../runtime/execution-profile.md) 计算；Gate 规则见 [Qualification Gate](../runtime/gates.md#qualification-gate)。数据对象按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Boundaries

不要重复询问已有答案，不使用固定问卷替代 gap 判断，不在目标或范围仍会实质改变计划时开始构建，也不把 Capability 分析结果直接当作 Gate 结论。
