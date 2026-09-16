# Incident, Change and Decision Loop

## Use

当生产异常、严重风险、漂移、供应商/模型/数据变化可能使当前产品结论失效时读取。

## Incident Loop

1. `detect`：确认信号、影响范围、版本和受影响者；未知保持未知。
2. `contain`：限流、降级、禁用能力、撤销权限或人工接管，优先降低持续伤害。
3. `diagnose`：保存必要证据，区分能力、数据、配置、工具、权限、交互、流程和监控失败。
4. `correct + verify`：实施最小修复，执行定向与必要全量回归，在受控 rollout 中验证。
5. `communicate + remedy`：通知有权限的 owner 和受影响者，执行申诉、数据修复或业务补救。
6. `learn`：更新 Evidence、Decision、Risk、eval/regression、runbook 和监控；不只写事故叙述。

## Change and Drift

- 记录模型、prompt/tool、数据、权限、供应商、政策和用户结构变化；变更后按风险运行基线、canary 或回归。
- 漂移按输入、输出、性能、人工纠正、outcome 和风险切片判断；分布变化不自动等于质量下降，需连接任务结果。
- 当阈值、guardrail、严重事件或反证命中 DecisionRecord 的 `reopen_trigger`，创建新 EvidenceRecord，并用 `DECISION_CHANGE` Replan；新结论用 `supersedes` 连接旧决策。

## Completion

影响已控制、原因与未知项分开、修复经验证、沟通/补救完成，并有明确的继续、降级、暂停或重新决策结果。
