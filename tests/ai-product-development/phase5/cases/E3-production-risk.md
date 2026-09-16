# Production Quality / Risk Issue

你负责已经生产运行的客服 AI 队列建议。交付目标为 Enterprise，本次只处理生产质量/风险问题及受影响发布工作。

当前有效决策：

- Decision ID：`D-P1`
- 选择：低风险工单显示 AI 建议；安全类依赖零漏分 guardrail 并由人工确认。
- `reopen_trigger`：`safety escalation recall falls below 100%`

固定生产输入：

- `SRC-P1`：版本 product v1.3 / model M2 / prompt P7 的最近 7 天监控显示，安全升级召回率从 100% 降至 97%（3/100 被漏分）。
- `SRC-P2`：其中 1 个漏分导致安全专席响应延迟 42 分钟；事件已 containment，系统已临时降级为全部人工分流。
- 当前受影响任务：`T-ROUTING-EVAL`、`T-ROUTING-ROLLOUT`；新增事件诊断任务必须叫 `T-ROUTING-INCIDENT`。
- 无关且仍有效的计费任务：`T-BILLING`。

请判断 Profile、必要 Capability、Release Readiness Gate、Production Evidence、是否重新打开 `D-P1`，以及只影响必要范围的 Replan。不要重新启动一般用户 Discovery、竞品、商业论证、路线图或常规 pilot。
