# Evaluation Readout — Routing Suggestion v1

- Decision: 是否允许低风险工单显示 AI 路由建议。
- Versions: plan EP-1, run ER-3, system v1, dataset DS-2, rubric GR-1。
- Run validity: 120 cases × 3 trials 完整，无计划偏离。
- Primary: 总体准确率 88%，达到建议模式阈值 85%。
- Guardrail: 安全类召回 100%，达到零漏分要求；P95 1.4s，成本达标。
- Slice: 相邻售后队列仅 76%，不得自动转派。
- Bad cases: 9 例术语歧义、4 例正文缺少产品线；尚未证明由模型或输入设计单独导致。
- Result: `conditional`——仅显示可编辑建议，安全类与低置信输入转人工。
- Next: 将 13 个 bad cases 去重进入 regression；补充产品线澄清交互后重测。
- Reopen trigger: 安全类出现漏分、相邻队列纠正率超过阈值或模型版本变化。
