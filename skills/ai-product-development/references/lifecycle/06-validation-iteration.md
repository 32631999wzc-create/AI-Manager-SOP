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

## Capabilities

见下述 Procedure 中的原始能力组或流程；不新增能力。

## Procedure

1. 选择能覆盖当前声明和风险的最小充分验证方法。
2. 执行验证并保存可核验结果，不以模型自述代替工具或产物证据。
3. 按预先确认的 acceptance criteria 判断，并限制结论适用范围。
4. 失败时定位根因，只修改真正导致失败的层。
5. 对修复做定向验证和必要回归，再重新判定。

Flow:

`Evaluate → PASS` or `Evaluate → Bad Case → Root Cause → Minimal Fix → Targeted Evaluation → Regression → Evaluate Again`

Root-cause categories are diagnostic labels, not lifecycle nodes:

- requirement
- data / knowledge
- context / prompt
- model
- tool / integration
- workflow / state
- guardrail
- code
- evaluation

Prefer fixing the layer that actually caused the failure; do not use prompt changes as a universal repair mechanism.

## Outputs

验证结论与证据、覆盖范围和限制；失败时还包括 bad cases、根因、最小修复结果，以及必要的 Replan 建议。

## Completion Criteria

- 验证证据覆盖当前 acceptance criteria 和交付风险；
- 结论没有超出样例、数据或环境的覆盖范围；
- 失败已修复并回归，或明确阻塞/进入 Replan；
- 残余风险和未覆盖项已说明。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

验收标准依赖见 [Dependency Closure](../runtime/execution-profile.md)；必要修复使用 [Replan](../runtime/replan-recovery.md)。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。不要在看到结果后静默降低标准，不要把有限样例通过宣称为普遍有效，也不要无限迭代。
