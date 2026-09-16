---
name: delivery-collaboration
description: Coordinate cross-functional delivery of an approved AI product slice when responsibilities, dependencies, evidence, and change decisions span product, design, engineering, data, evaluation, risk, or operations. Do not add ceremony for work one owner can complete independently.
---
# Delivery Collaboration
## Purpose
把已评审范围转成可交付、可验证且责任清晰的端到端增量。
## When to use
多职能共同交付、依赖复杂、决策频繁变化或 readiness/DoD 需对齐时使用。
## When NOT to use
单一 owner 可独立完成；需求尚未评审；仅需 Planner 排一个局部 DAG。
## Decision / Unknown
- `decision_to_inform`：切片、owner、依赖、节奏、ready/done 与升级路径。
- `unknown_to_reduce`：容量、接口、阻塞、版本一致性和变更影响。
- `risk_to_reduce`：职能孤岛、会议替代交付、工程静默补需求。
## Required Inputs
- `blocking`：ACTIVE 范围/设计/eval、Build Readiness、owner 与依赖。
- `reusable`：backlog、团队约定、风险、版本和容量。
- `optional`：发布窗口、历史吞吐、外部审批。
## Method
按端到端用户切片拆解；建立责任和依赖；将 eval、instrumentation、failure handling 同排；同步只解决证据/阻塞/决策；变化做 impact analysis 并 Replan；完成按 DoD 与正式版本验证。
## Evidence Rules
任务关联目标、输入、owner、验收与版本；状态用产物/工具证据；假设和阻塞显式；保留范围变化与 dissent。
## Decision Rules
- `proceed`：READY 输入闭合且 owner/DoD 明确。
- `conditional`：非阻塞依赖有 owner 和期限。
- `stop / block`：readiness、接口或产品语义未决。
- `escalate`：跨团队优先级、重大风险或权限冲突。
## Output Contract
输出 backlog/Task DAG、责任、依赖、节奏、DoR/DoD、升级路径、状态摘要与变更影响。
## Handoff
- `reads_from`：PRD、Design、Eval、Roadmap、Risk。
- `writes_to`：Plan/Task 与交付状态。
- `supports_lifecycle`：Implementation、Validation、Release。
- `may_trigger`：Requirement Review、Replan、Evaluation、Launch。
- `reopen_when`：范围、依赖、容量、版本、风险或验收变化。
## Completion Criteria
READY 任务输入/验收明确；关键依赖有 owner；切片产生可验证增量；requirement→implementation→eval→release 版本一致。
## Boundaries
不以 RACI/会议数量当成果，不建设超出团队规模的流程，不让进度绕过风险和验收。
