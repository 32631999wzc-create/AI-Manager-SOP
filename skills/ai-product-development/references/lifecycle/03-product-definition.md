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

## Required Decisions / State

本节点必须形成足以支持方案决策的：`target user`、`problem`、`desired outcome`、`value hypothesis`、`AI boundary`、`scope`、`non-goals`、`success measures`、`key risks`、`open assumptions`。当前 Assignment Scope 与整个产品需求必须分开。

## Capability Routing

根据尚未解决的决策选择[用户与机会发现](../capabilities/discovery/SKILL.md)、[市场与竞品情报](../capabilities/competitive-intelligence/SKILL.md)、[商业论证与优先级](../capabilities/business-case/SKILL.md)、[AI 可行性与原型](../capabilities/ai-feasibility/SKILL.md)或[产品需求定义](../capabilities/product-requirements/SKILL.md)。当输入变化使既有 scope、success measures 或 acceptance criteria 失效时，`Product Requirements` 是待执行的实际 gap，不能只用 Evaluation 或实现任务代替。跨版本取舍需要[路线图与版本规划](../capabilities/roadmap/SKILL.md)；需求已形成且要做跨职能确认时再调用[需求评审与决策](../capabilities/requirement-review/SKILL.md)。

## Outputs

**Primary output:** `Product Definition & Scope`.

该对象至少包含目标用户、问题、价值假设、AI 适用边界、目标状态、范围、非目标、优先级、成功指标、关键风险和外部项目要求。

## Completion Criteria

- 用户、问题、价值和目标状态能够支持方案决策；
- AI 与确定性软件、人工参与的边界明确；
- 当前 Assignment Scope、非目标和外部要求没有混淆；
- 成功指标或验收口径可被后续验证。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

按 [Execution Profile](../runtime/execution-profile.md) 的范围与依赖闭包决定所需深度；数据对象按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Boundaries

不要在证据不足时虚构用户或市场结论，不把 Agent 或其他 AI 架构作为默认答案，不在本节点展开专业研究方法或详细技术实现。
