# Validation & Iteration

## Purpose

determine whether the current version meets the acceptance criteria and make the smallest necessary correction when it does not.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

原文未单列固定输入清单；按下述 Procedure 与当前任务的 required_inputs 获取相关材料。

## Capabilities

见下述 Procedure 中的原始能力组或流程；不新增能力。

## Procedure

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

原文未规定独立固定输出格式；遵循当前任务的 expected_output 和 acceptance_criteria。

## Completion Criteria

原文未单列节点完成清单；按当前任务验收标准及 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria) 判断。

## Dependencies

验收标准依赖见 [Dependency Closure](../runtime/execution-profile.md)；必要修复使用 [Replan](../runtime/replan-recovery.md)。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。
