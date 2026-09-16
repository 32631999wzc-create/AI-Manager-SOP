---
name: production-observability-learning
description: Convert production usage, quality, reliability, cost, safety, feedback, and change signals into controlled product learning and reopened decisions. Do not use service uptime alone as evidence that an AI product is succeeding.
---
# Production Observability & Learning
## Purpose
持续观察产品声明和风险，把可信生产信号转成 requirement、eval、实验、路线图或重开决策。
## When to use
AI 产品进入真实使用，需管理价值、质量、可靠性、成本、风险或模型/数据变化时使用。
## When NOT to use
尚无真实运行；一次性离线 eval；收集的信号没有 owner 或决策用途。
## Decision / Unknown
- `decision_to_inform`：继续、降级、暂停、修复、扩展或重开何项决策。
- `unknown_to_reduce`：任务成功、silent failure、切片、漂移、单位成本、反馈偏差和事件根因。
- `risk_to_reduce`：uptime 代替质量、thumbs-up 当真值、无用途日志和线上线下脱节。
## Required Inputs
- `blocking`：发布版本、产品/guardrail 声明、owner、事件/回滚路径和数据授权。
- `reusable`：eval/pilot 基线、trace、反馈、工单、业务/成本数据。
- `optional`：dashboard、供应商变更、历史事件。
## Method
按生产信号与决策选择性读取：

- 需要定义 outcome、quality、reliability、cost、risk、adoption 的指标树和最小埋点时，读取 [Observability and Metric Tree](references/observability-metric-tree.md)；
- 需要把反馈、纠正、工单和生产 bad case 转成可审查证据与回归输入时，读取 [Feedback and Bad-case Loop](references/feedback-bad-case-loop.md)；
- 需要处理异常、漂移、事件或版本变化并形成产品学习时，读取 [Incident, Change and Decision Loop](references/incident-change-decision-loop.md)。

正式交付使用 [Operating Scorecard and Learning Loop](templates/operating-scorecard-learning-loop.md)；仅在校准具体程度时查看 [Example](examples/operating-scorecard.md)。
## Evidence Rules
指标定义、分母、切片、版本、owner 和动作完整；反馈与任务结果分开；原始敏感日志受控；保留选择性反馈与反证；模型/数据/配置变化标记 freshness。
## Decision Rules
- `proceed`：outcome 与 guardrail 稳定且变化可解释。
- `conditional`：限流/降级/人工接管并继续观察。
- `stop / block`：严重事件、不可控漂移或核心声明失效。
- `escalate`：incident、重大风险、隐私或供应商/预算决策。
## Output Contract
输出 [Operating Scorecard and Learning Loop](templates/operating-scorecard-learning-loop.md)：指标、查询/告警、review、反馈 taxonomy、bad-case intake、事件路径、变更门槛、下游去向和 owner。
## Handoff
- `reads_from`：版本、Eval/Pilot/Launch、事件和反馈。
- `writes_to`：生产 Evidence、bad cases、变更/重开建议。
- `supports_lifecycle`：Release、Validation、Retrospective、Product Definition。
- `may_trigger`：Discovery、PRD、Evaluation、Risk、Roadmap、Replan。
- `reopen_when`：阈值/guardrail 命中、严重事件、漂移或旧假设被反证。
## Completion Criteria
关键产品声明/风险/单位经济可观察；反馈可追踪到处理、eval、修复和发布；变化有版本/回归/rollout；重开或继续决定明确。
## Boundaries
不只监控 uptime，不把反馈当无偏真值，不收集无用途或无法治理的日志。
