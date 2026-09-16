# Implementation

## Purpose

turn the approved scope and design into working product capability.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

- 通过 Build Readiness 的范围、设计和验收标准；
- 一个依赖已满足的 READY Task 与最小 TaskContextPack；
- 可复用资产、目标仓库约定以及完成任务所需的工具或授权。

## Required Decisions / State

- 当前 READY Task 的目标、输入、依赖、写入边界和验收标准明确；
- Build Readiness 已通过，所依赖的设计与资产有效；
- 实现增量与 Assignment Scope 一致，冲突和实质变化已进入 Replan；
- Task Result、验证证据、限制和待提交 Artifact 状态明确。

## Capability Routing

跨角色交付、backlog、依赖和 Definition of Done 需要专业处理时调用[跨职能交付协作](../capabilities/delivery/SKILL.md)。实现中出现需求解释冲突时调用[需求评审与决策](../capabilities/requirement-review/SKILL.md)，不得在代码中静默选择产品语义。

## Outputs

可运行或可审阅的产品增量、变更清单、Task Result、验证证据、已知限制，以及需要登记时的待提交 Artifact。

## Completion Criteria

- 当前 Task 的主要交付物已产生且满足验收标准；
- 必要检查通过，结果和限制有证据；
- 没有越过 Assignment Scope、写入边界或授权；
- 新发现的实质变化已触发 Replan，而非被隐藏。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

构建前检查 [Build Readiness](../runtime/gates.md#build-readiness)，再由 [Planner](../runtime/planner.md) 从缺口生成任务；执行边界见 [Executor](../runtime/executor.md)，数据对象按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Boundaries

不要在 Lifecycle 中复制工程执行方法，不顺手重构无关范围，不把未验证结果提交为正式产物，也不让 Capability catalog 自动生成实现任务。
