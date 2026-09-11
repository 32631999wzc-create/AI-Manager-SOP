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

## Capabilities

outcome review, key-decision review, failed assumptions, debt, reusable assets, SOP update, skill update.

## Procedure

1. 对照目标和成功指标说明实际结果与差距。
2. 识别关键决策、有效做法、失败假设和主要根因。
3. 区分一次性经验、可复用资产、待处理债务和下一步机会。
4. 仅把有证据且可复用的结论写入 Registry、SOP 或 Skill。

Keep the output concise unless the user explicitly requests a formal retrospective.

## Outputs

简洁 Retrospective：目标结果、关键学习、失败假设、遗留债务、可复用资产，以及确有价值的后续行动。

## Completion Criteria

- 结果与学习有证据支撑，不把相关性写成因果；
- 可复用内容已正确登记或版本化；
- 未完成债务、风险和后续行动明确；
- 只保留会改变未来决策的经验。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

历史信息读取遵循 [Context](../runtime/context.md)，正式更新遵循 [Registry](../runtime/registry-versioning.md)。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。不要制造无决策价值的复盘文档，也不要把单一项目经验升级为通用 Skill 规则。
