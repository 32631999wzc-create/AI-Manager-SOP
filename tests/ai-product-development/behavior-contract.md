# 行为回归共用契约

八组 case 都从 [Skill Kernel](../../skills/ai-product-development/SKILL.md) 开始，根据活动任务和依赖按需读取 reference。场景描述是测试输入，不自动视为已核实事实；实际执行必须检查相应证据。

行为回归必须记录实际工具或文件读取 trace。不得根据模型自述认定已读取模块，也不得为了覆盖清单而加载全部 lifecycle/runtime references。规划、Gate、Context、Executor、Registry 或 Replan 仅在当前操作需要时读取。

场景只授权生成测试要求的结果，不授权部署、发布或其他外部写入。完成状态统一按 [Kernel Completion Criteria](../../skills/ai-product-development/SKILL.md#17-completion-criteria) 判断；Plan 或 Profile 本身不代表产品交付完成。

expected 文件只记录场景特有断言，不保存执行结果。实际结果应由测试运行产生，并与固定输入和 trace 一起保存。
