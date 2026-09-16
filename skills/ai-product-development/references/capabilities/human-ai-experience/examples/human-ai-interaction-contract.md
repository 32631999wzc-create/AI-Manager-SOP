# Human-AI Interaction Contract — Routing Suggestion

- Scope: AI 建议低风险客服队列；坐席决定是否采用，安全类永不自动转派。
- Capability boundary: 建议可能混淆相邻售后队列；不判断安全事件处置。

| Step | AI role | Human role | Control |
|---|---|---|---|
| 生成建议 | 输出队列与支持片段 | 核验工单语义 | 可编辑、拒绝 |
| 应用路由 | 不直接执行 | 坐席确认后提交 | 提交前显示目标队列 |
| 安全类 | 标记不确定并停止 | 升级安全专席 | 无自动继续 |

| Failure | Detection | Recovery |
|---|---|---|
| 相邻队列混淆 | 坐席发现或二次转派 | 修改队列并记录纠正 |
| 服务超时 | 无建议状态 | 恢复手工选择 |

- Feedback: 纠正记录关联工单、模型版本和最终队列，进入每周 bad-case review 与回归集。
- Verification: 新坐席能说明建议不是自动决定，并在错误、安全、超时三个场景完成恢复。
- Reopen trigger: 误分导致高风险工单延迟，或人工纠正率超过阈值。
