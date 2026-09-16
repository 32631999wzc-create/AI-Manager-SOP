# Operating Scorecard — Routing Suggestion

- Version: product v1.3 / model M2 / prompt P7。
- Current decision: 仅向低风险工单显示可编辑建议。

| Signal | Definition | Window / slice | Threshold | Action |
|---|---|---|---|---|
| Outcome | 首次分流中位时间 | weekly / 新坐席 | 至少下降 15% | 未达则重开价值假设 |
| Quality | 最终队列与建议一致且无后续转派 | weekly / 队列 | ≥85% | bad cases 入 eval |
| Risk | 安全类漏分数 | immediate / safety | 0 | 暂停建议并启动事件路径 |
| Cost | 每个被采纳建议成本 | weekly | ≤预算 | 超限评估降级模型 |
| Workflow | 人工纠正率 | weekly / 坐席经验 | ≤15% | 超限缩小 cohort |

- Feedback loop: 纠正、二次转派和安全升级关联版本，每周去重分诊；确认失败创建 EvidenceRecord 并进入 regression。
- Change control: 模型、队列定义或安全规则变化先运行基线与 canary。
- Reopen triggers: 任何安全漏分；纠正率连续两周超过 15%；首次分流时间不再改善。
