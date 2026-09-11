# Cognition

## Purpose

understand the current product, assets, repository, system, and implementation state before changing it.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

- 已确认的请求、Assignment Scope 与相关 Node Profile；
- 与受影响范围有关的产品材料、用户证据、仓库、系统或数据资料；
- 当前要回答的问题或准备修改的路径。

## Capabilities

product-context inspection, existing-asset inspection, repository inspection, system/data/state-flow cognition, current-state modeling.

## Procedure

1. 先限定本次需要理解的产品、流程、系统或代码范围。
2. 检查与该范围直接相关的证据和现有资产，不做无目标的全量盘点。
3. 标记资产状态、关键依赖、当前行为和已知约束。
4. 只在有助于后续决策时建立流程图、System Map 或数据流。
5. 分开记录事实、推断、冲突和未决问题。

**Rules:**

- Greenfield: skip repository cognition.
- Existing repository change: inspect the relevant code path before redesigning or editing it.
- Prefer native search, structured inspection, and dependency tracing before introducing specialized cognition infrastructure.

## Outputs

**Primary outputs:** `Current State`, `Existing Asset Inventory`; `System Map` only when useful.

- 关键依赖、约束、冲突和未知问题。

## Completion Criteria

- 已有证据足以支持当前范围内的产品或实现决策；
- 相关资产已区分为可复用、待验证、部分可用、过期或冲突；
- 受影响路径、关键依赖和阻塞未知项已明确；
- 没有把推断写成事实。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

仓库变更的 Cognition 下限见 [Project Mode / Dependency Closure](../runtime/execution-profile.md)。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。不要为“全面了解”而扫描无关仓库或材料，也不要在本节点提前重做产品定义或方案。
