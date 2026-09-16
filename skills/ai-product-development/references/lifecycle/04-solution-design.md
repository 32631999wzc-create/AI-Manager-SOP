# Solution Design

## Purpose

define enough technical/product design and evaluation criteria to build the requested scope reliably.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

- 已确认的 `Product Definition & Scope` 与交付目标；
- 相关 Current State、可复用资产和技术/运营约束；
- 成功指标、验收标准、数据与集成条件；
- 当前风险底线和必须满足的依赖。

## Required Decisions / State

- 产品与 AI 工作流、组件责任、接口、数据与状态边界达到当前交付深度；
- 模型、检索、工具、Agent、记忆与人工参与仅在需求触发时使用；
- 关键失败路径、控制、可观测性、约束、假设与风险明确；
- Evaluation Design 能验证已声明的成功标准；
- Build Readiness 已基于证据判定。

## Capability Routing

根据实际设计 gap 调用[AI 可行性与原型](../capabilities/ai-feasibility/SKILL.md)、[数据策略与治理](../capabilities/data-strategy/SKILL.md)、[Human-AI 体验](../capabilities/human-ai-experience/SKILL.md)、[评测与质量](../capabilities/evaluation/SKILL.md)或[责任 AI、安全与风险](../capabilities/responsible-ai/SKILL.md)。Data、Evaluation 与 Responsible AI 可跨阶段调用；不要因为产品使用 AI 就机械加载全部 domain。

## Outputs

`Solution Design`，按交付深度记录产品/AI 流程、组件边界、接口、数据与状态、关键决策、失败处理、风险控制和 `Evaluation Design`。简单任务可用简短设计说明，不强制固定模板。

## Completion Criteria

- 当前范围已经具体到可以拆分和实现；
- 数据、接口、状态、失败路径和人工边界达到交付目标所需深度；
- Evaluation Design 能验证已声明的成功标准；
- 关键依赖、风险与假设明确，Build Readiness 已判定。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

构建前检查 [Build Readiness](../runtime/gates.md#build-readiness)；评估方法选择遵循 [Executor — Validation](../runtime/executor.md#104-validation)；数据对象按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Boundaries

不要把可选架构当作默认基础设施，不在 Lifecycle 中复制专业设计或评测方法，也不要在 Build Readiness 未通过时开始大规模实现。
