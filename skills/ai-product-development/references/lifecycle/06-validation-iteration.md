# Validation & Iteration

## Purpose

determine whether the current version meets the acceptance criteria and make the smallest necessary correction when it does not.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

- 待验证的 Task Result、产品版本或 Artifact；
- 已确认的 acceptance criteria 与 Evaluation Design；
- 相关样例、数据、基线、测试环境和风险要求；
- 已知限制及上一轮失败证据（若有）。

## Required Decisions / State

- 待验证声明、acceptance criteria、Evaluation Design、版本和环境明确；
- 验证证据、覆盖范围、不确定性和限制可核验；
- 结果被判定为 PASS、条件通过或 FAIL；
- FAIL 已形成 bad case、根因和最小修复/阻塞/Replan 决策；
- 定向验证与必要回归完成后才重新判定。

控制循环保持为：`Evaluate → Bad Case → Root Cause → Minimal Fix → Targeted Evaluation → Regression → Evaluate Again`。该循环属于 Lifecycle；具体评测、实验与风险方法属于 Capability。

## Capability Routing

离线质量、eval run 与 regression 调用[评测与质量](../capabilities/evaluation/SKILL.md)；用户价值、可用性或真实流程适配调用[实验与试点](../capabilities/experimentation/SKILL.md)；高影响或滥用风险调用[责任 AI、安全与风险](../capabilities/responsible-ai/SKILL.md)。

## Outputs

验证结论与证据、覆盖范围和限制；失败时还包括 bad cases、根因、最小修复结果，以及必要的 Replan 建议。

## Completion Criteria

- 验证证据覆盖当前 acceptance criteria 和交付风险；
- 结论没有超出样例、数据或环境的覆盖范围；
- 失败已修复并回归，或明确阻塞/进入 Replan；
- 残余风险和未覆盖项已说明。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

验收标准依赖见 [Dependency Closure](../runtime/execution-profile.md)；执行与局部重试见 [Executor](../runtime/executor.md)，必要修复使用 [Replan](../runtime/replan-recovery.md)。

## Boundaries

不要在 Lifecycle 中复制评测方法，不在看到结果后降低标准，不把有限样例通过宣称为普遍有效，也不要无限迭代或把 prompt 修改当成通用修复。
