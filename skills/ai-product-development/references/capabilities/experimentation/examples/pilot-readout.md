# Pilot Readout — Routing Suggestion

- Hypothesis: 对低风险工单显示可编辑建议，会减少首次分流时间，而不增加安全漏分或总人工负担。
- Design: 两周、12 名坐席、同类工单 before/after；非随机，因此只支持受限关联结论。
- Exposure: 624 个合格工单中 581 个显示建议，坐席采用率 71%。
- Primary: 首次分流中位时间下降 24%，超过 15% 阈值。
- Guardrails: 安全漏分 0；二次转派率从 18% 降至 15%；人工纠正率 22%，高于扩大目标 15%。
- Counterevidence: 新坐席收益明显，专家坐席无显著变化；两周内有额外培训。
- Decision: `narrow`——继续新坐席 cohort，先修复相邻队列混淆，不扩大至自动转派。
- Next: 13 个确认 bad cases 进入 Evaluation/Regression；四周后复测纠正率。
- Reopen trigger: 出现安全漏分、纠正率不降或支持负担超过基线。
