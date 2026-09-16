# Existing Product Feature Change

你负责现有客服产品中的“AI 队列建议”功能变更，交付目标是 Integrated MVP，本次仅负责该功能及受影响验证和受控 pilot，不负责无关导出功能。

固定输入：

- `SRC-E1`：当前架构与交互已核验；AI 仅给出可编辑建议，坐席确认后才提交，超时恢复手工选择。
- `SRC-E2`：当前离线评测覆盖 120 个真实去标识工单，建议准确率 88%，安全类召回 100%；相邻售后队列准确率只有 76%。
- `SRC-E3`：Privacy owner 已批准现有去标识、保留和访问方案，批准范围仅限内部受控 pilot。
- `SRC-E4`：业务刚把 8 个队列重组为 10 个；目标用户、产品目标、确认交互和无关导出功能不变。
- 当前任务：重新规划队列建议功能。既有任务为 `T-ROUTING-DESIGN`、`T-ROUTING-IMPLEMENT`、`T-ROUTING-EVAL`；新增影响分析任务必须叫 `T-TAXONOMY-IMPACT`；无关已验证任务为 `T-EXPORT`。

请判断 Profile、必要 Capability、Build Readiness Gate、Evidence，以及这次输入变化的最小 Replan。不要重新做已被当前证据覆盖的 Discovery、市场分析、路线图或发布传播。
