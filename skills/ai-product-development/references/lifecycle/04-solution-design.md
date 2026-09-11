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

## Capabilities

见下述 Procedure 中的原始能力组或流程；不新增能力。

## Procedure

1. 从最低复杂度的可行产品/AI 流程开始，明确组件和责任边界。
2. 定义必要的接口、数据与状态流、失败处理、人工参与和关键决策。
3. 仅在需求触发时加入模型、检索、Agent、记忆、权限或可观测能力。
4. 同步设计与交付目标匹配的评估任务、样例、指标、判定方式和通过标准。
5. 检查每项设计是否可追溯到范围、成功标准、依赖或风险。

Two capability groups may run in parallel when independent:

### Solution Architecture capabilities

- product / AI workflow
- model / LLM / Agent only if needed
- retrieval / RAG only if needed
- tools and integrations
- data and state
- context and memory only if needed
- guardrails / reliability
- observability / traceability

### Evaluation Design capabilities

- evaluation task
- cases / dataset
- baseline when useful
- metrics
- judge strategy
- pass criteria

评估方法选择遵循 [Executor — Validation](../runtime/executor.md#104-validation)。

执行 [Build Readiness](../runtime/gates.md#build-readiness)。

## Outputs

`Solution Design`，按交付深度记录产品/AI 流程、组件边界、接口、数据与状态、关键决策、失败处理、风险控制和 `Evaluation Design`。简单任务可用简短设计说明，不强制固定模板。

## Completion Criteria

- 当前范围已经具体到可以拆分和实现；
- 数据、接口、状态、失败路径和人工边界达到交付目标所需深度；
- Evaluation Design 能验证已声明的成功标准；
- 关键依赖、风险与假设明确，Build Readiness 已判定。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

构建前检查 [Build Readiness](../runtime/gates.md#build-readiness)。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。不要把可选架构当作默认基础设施，也不要在 Build Readiness 未通过时开始大规模实现。
