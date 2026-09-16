# Feasibility Note — Ticket Routing Suggestion

- Decision: 是否以单次分类调用支持低风险工单路由建议。
- Task: 从标题与正文选择 8 个业务队列之一；安全类工单必须转人工。
- Largest unknown: 小样本真实工单上的严重误分率。
- Baseline: 关键词规则。
- Candidate: 单次结构化模型调用 v1，无检索、无 Agent。
- Evidence: E-11，120 个去标识工单、每例 3 trials；总体准确率 88%，安全类召回 100%，P95 1.4s，单位成本在预算内。
- Counterevidence: 两个相邻售后队列混淆，优于规则但未达到自动转派标准。
- Conclusion: `constrained`。
- Recommendation: 仅提供可编辑建议，安全类强制人工；不引入 RAG/Agent。
- Reopen trigger: 安全类召回低于 100%，或队列定义/模型版本变化。
