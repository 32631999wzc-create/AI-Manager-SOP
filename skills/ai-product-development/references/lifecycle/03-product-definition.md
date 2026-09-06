# Product Definition & Scope

## Purpose

define who the product serves, the problem, why AI is appropriate, target state, current-to-target gap, and current assignment scope.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

原文未单列固定输入清单；按下述 Procedure 与当前任务的 required_inputs 获取相关材料。

## Capabilities

user/problem, current workflow, AI fit & boundary, value hypothesis, target state, gap analysis, priority, product success metrics.

## Procedure

**AI boundary rule:** choose among deterministic software, rule logic, retrieval, LLM, tool calling, workflow, Agent, Multi-Agent, and human involvement based on the actual need. Do not assume Agent.

## Outputs

`Product Definition & Scope`.

## Completion Criteria

原文未单列节点完成清单；按当前任务验收标准及 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria) 判断。

## Dependencies

按 [Execution Profile](../runtime/execution-profile.md) 的范围与依赖闭包决定所需深度。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。
