# Solution Design

## Purpose

define enough technical/product design and evaluation criteria to build the requested scope reliably.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

原文未单列固定输入清单；按下述 Procedure 与当前任务的 required_inputs 获取相关材料。

## Capabilities

见下述 Procedure 中的原始能力组或流程；不新增能力。

## Procedure

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

原文未规定独立固定输出格式；遵循当前任务的 expected_output 和 acceptance_criteria。

## Completion Criteria

原文未单列节点完成清单；按当前任务验收标准及 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria) 判断。

## Dependencies

构建前检查 [Build Readiness](../runtime/gates.md#build-readiness)。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。
