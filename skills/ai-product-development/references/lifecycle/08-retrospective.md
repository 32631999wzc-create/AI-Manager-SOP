# Retrospective

## Purpose

retain reusable value from the project without creating unnecessary reporting work.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

- 原始目标、范围、成功指标与最终交付结果；
- 验证、发布或使用证据；
- 关键决策、变化、失败、假设和当前技术/产品债务；
- Active Records 与 Artifacts。

## Required Decisions / State

- 实际结果与原始目标、成功指标和范围的差距明确；
- 关键决策、当时证据、后来证据和失败假设可追溯；
- 一次性事实、产品债务、可复用资产、后续机会和跨项目学习分开；
- 每项后续行动有 owner、触发器或验证方式；
- 需要重新打开的产品决策或 Lifecycle 状态明确。

## Capability Routing

正式复盘、跨版本学习或继续投资判断调用[复盘与组合学习](../capabilities/retrospective/SKILL.md)；生产信号需要转入新机会、requirement、eval 或 backlog 时调用[生产观测与学习闭环](../capabilities/production-learning/SKILL.md)，必要时重新调用[用户与机会发现](../capabilities/discovery/SKILL.md)。

## Outputs

简洁 Retrospective：目标结果、关键学习、失败假设、遗留债务、可复用资产，以及确有价值的后续行动。

## Completion Criteria

- 结果与学习有证据支撑，不把相关性写成因果；
- 可复用内容已正确登记或版本化；
- 未完成债务、风险和后续行动明确；
- 只保留会改变未来决策的经验。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

历史信息读取遵循 [Context](../runtime/context.md)，正式更新遵循 [Registry](../runtime/registry-versioning.md)，决策重新打开使用 [Replan](../runtime/replan-recovery.md)。

## Boundaries

默认保持输出简洁。不要在 Lifecycle 中复制复盘或组合管理方法，不制造无决策价值的总结，不用复盘追责个人，也不把单一项目经验升级为通用 Skill 规则。
