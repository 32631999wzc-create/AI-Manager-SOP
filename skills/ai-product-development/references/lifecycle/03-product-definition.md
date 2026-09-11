# Product Definition & Scope

## Purpose

define who the product serves, the problem, why AI is appropriate, target state, current-to-target gap, and current assignment scope.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

- Qualification 输出与当前 Assignment Scope；
- 用户、业务目标、现有流程和可用证据；
- Cognition 结论（存在相关现状或资产时）；
- 交付目标、约束、风险和已知成功条件。

## Capabilities

user/problem, current workflow, AI fit & boundary, value hypothesis, target state, gap analysis, priority, product success metrics.

## Procedure

1. 明确目标用户、核心问题、使用场景和当前替代流程。
2. 说明价值假设、预期行为变化，以及为何需要或不需要 AI。
3. 定义目标状态、当前差距、范围内、范围外和非目标。
4. 选择能反映产品结果的成功指标，并给出当前交付深度所需的验收口径。
5. 按用户价值、依赖、风险和交付约束确定当前优先范围。

**AI boundary rule:** choose among deterministic software, rule logic, retrieval, LLM, tool calling, workflow, Agent, Multi-Agent, and human involvement based on the actual need. Do not assume Agent.

## Outputs

**Primary output:** `Product Definition & Scope`.

该对象至少包含目标用户、问题、价值假设、AI 适用边界、目标状态、范围、非目标、优先级、成功指标、关键风险和外部项目要求。

## Completion Criteria

- 用户、问题、价值和目标状态能够支持方案决策；
- AI 与确定性软件、人工参与的边界明确；
- 当前 Assignment Scope、非目标和外部要求没有混淆；
- 成功指标或验收口径可被后续验证。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

按 [Execution Profile](../runtime/execution-profile.md) 的范围与依赖闭包决定所需深度。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。不要在证据不足时虚构用户需求或市场结论，也不要在本节点展开详细技术实现。
