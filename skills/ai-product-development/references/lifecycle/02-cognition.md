# Cognition

## Purpose

understand the current product, assets, repository, system, and implementation state before changing it.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

原文未单列固定输入清单；按下述 Procedure 与当前任务的 required_inputs 获取相关材料。

## Capabilities

product-context inspection, existing-asset inspection, repository inspection, system/data/state-flow cognition, current-state modeling.

## Procedure

**Rules:**

- Greenfield: skip repository cognition.
- Existing repository change: inspect the relevant code path before redesigning or editing it.
- Prefer native search, structured inspection, and dependency tracing before introducing specialized cognition infrastructure.

## Outputs

`Current State`, `Existing Asset Inventory`; `System Map` only when useful.

## Completion Criteria

原文未单列节点完成清单；按当前任务验收标准及 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria) 判断。

## Dependencies

仓库变更的 Cognition 下限见 [Project Mode / Dependency Closure](../runtime/execution-profile.md)。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。
