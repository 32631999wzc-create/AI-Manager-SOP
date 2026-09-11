# Implementation

## Purpose

turn the approved scope and design into working product capability.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

- 通过 Build Readiness 的范围、设计和验收标准；
- 一个依赖已满足的 READY Task 与最小 TaskContextPack；
- 可复用资产、目标仓库约定以及完成任务所需的工具或授权。

## Capabilities

build planning, task decomposition, interface/schema contracts, incremental implementation, integration, local validation.

## Procedure

Do not treat these capabilities as fixed tasks. The Planner creates implementation tasks only for actual gaps.

1. 确认任务目标、输入、依赖、写入边界和验收标准。
2. 复用现有设计与资产，完成满足任务目标的最小可靠增量。
3. 遵循现有接口、schema、代码和文档约定；发现实质冲突时停止并 Replan。
4. 运行与变更相称的结构检查、测试或本地验证。
5. 返回 Task Result、验证证据、已知限制和待提交产物；验证通过后才进入正式 Artifact。

## Outputs

可运行或可审阅的产品增量、变更清单、Task Result、验证证据、已知限制，以及需要登记时的待提交 Artifact。

## Completion Criteria

- 当前 Task 的主要交付物已产生且满足验收标准；
- 必要检查通过，结果和限制有证据；
- 没有越过 Assignment Scope、写入边界或授权；
- 新发现的实质变化已触发 Replan，而非被隐藏。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

构建前检查 [Build Readiness](../runtime/gates.md#build-readiness)，再由 [Planner](../runtime/planner.md) 从缺口生成任务。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。不要顺手重构无关范围，不要把未验证结果提交为正式产物。
