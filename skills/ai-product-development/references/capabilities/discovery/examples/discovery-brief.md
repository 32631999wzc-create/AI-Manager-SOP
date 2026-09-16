# Discovery Brief — Support Triage

## Decision

- Decision to inform: 是否优先减少客服工单首次分流时间。
- Decision owner: Support PM
- Decision rule: 重复分流占主要处理时间，且高风险工单可保留人工控制。
- Result: `conditional`

## Evidence

| Evidence ID | Source / time | Observation | Supports / contradicts | Confidence / limitations |
|---|---|---|---|---|
| E-01 | 6 次情境观察 / 2026-09 | 4 名坐席重复复制工单并手工选择队列 | supports | MEDIUM；单一区域 |
| E-02 | 工单日志 / 2026-08 | 18% 工单被二次转派 | supports | HIGH；原因码不完整 |
| E-03 | 专家坐席访谈 / 2026-09 | 安全类工单依赖隐性判断 | contradicts 全自动化 | MEDIUM |

## Synthesis and Handoff

- Problem: 常规工单首次分流包含重复操作，但高风险类别需要人工判断。
- Opportunity: 先为低风险类别提供可编辑建议，不自动转派。
- Rationale: E-01/E-02 支持效率机会，E-03 限制自动化边界。
- Remaining assumption: 建议准确率和人工复核成本尚未验证。
- Next: 触发 AI Feasibility 与 Human-AI；若低风险类别误分率超过既定阈值，重新打开范围决策。
