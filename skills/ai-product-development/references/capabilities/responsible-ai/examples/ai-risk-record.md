# AI Risk Record — Support Routing Suggestion

- Use case: 为低风险工单建议队列；不自动转派，不处理安全事件结论。
- Affected parties: 客户、坐席、安全专席。
- Owner: Support Operations；安全风险接受需 Security owner。

| Risk ID | Scenario | Evidence | Rating | Decision |
|---|---|---|---|---|
| R-01 | 安全类工单被建议到普通队列并延迟响应 | E-21：历史漏分后果高；eval 当前召回 100% | 高影响、可检测但时间敏感 | mitigate |
| R-02 | 工单正文包含敏感个人信息并进入外部模型日志 | 数据流审查；供应商保留条件待确认 | 高影响、暴露未知 | block pending review |

| Risk ID | Controls | Test | Residual risk |
|---|---|---|---|
| R-01 | 安全关键词前置规则、AI 不确定即人工、坐席确认 | adversarial 安全集零漏分 | 新型表达仍可能漏检 |
| R-02 | 去标识、禁止训练、最短保留、访问审计 | 数据流与供应商条款审查 | 待 Privacy owner 接受 |

- Release condition: R-02 审查完成；R-01 guardrail 持续通过；仅内部 pilot。
- Incident path: 暂停建议、恢复手工分流、通知 Security/Privacy、回放受影响工单并补救。
- Reopen trigger: 任何安全类漏分、数据处理条款变化或模型版本变化。
