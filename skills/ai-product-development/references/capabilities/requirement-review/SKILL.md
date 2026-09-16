---
name: requirement-review-decisions
description: Resolve cross-functional disagreements and approve, revise, defer, or reject product requirements when a versioned decision is needed. Do not schedule a review meeting when asynchronous comments can close all non-material issues.
---

# Requirement Review & Decisions

## Purpose
把需求分歧和 trade-off 转成可执行、可追溯且已同步到正式版本的决策。
## When to use
PRD、版本范围、AI 行为或验收需跨职能决定，存在阻塞或实质分歧时使用。
## When NOT to use
异步评论可解决；材料尚未达到评审条件；需要用户/技术验证而非利益相关者判断。
## Decision / Unknown
- `decision_to_inform`：`approve | approve with actions | revise | reject | defer`。
- `unknown_to_reduce`：分歧依据、影响、owner、依赖和阻塞性。
- `risk_to_reduce`：会议即通过、多数票绕过风险、旧版本继续执行。
## Required Inputs
- `blocking`：版本化材料、决策问题、decision owner、关键角色。
- `reusable`：Evidence、历史 Decision、风险/依赖、异步评论。
- `optional`：原型、eval、成本或运营证据。
## Method
预先区分 decision/feedback/information；异步合并意见；检查问题证据、范围、AI 边界、失败合同、eval、数据/风险/运营依赖；会议只处理阻塞 trade-off；按 claim→evidence→impact→options；记录结论、异议、owner、触发器并发布新版本。
## Evidence Rules
每项分歧引用材料版本和证据；保留 dissent；意见不等于事实；过期材料不能支持新版本结论。
## Decision Rules
- `proceed`：关键角色覆盖、阻塞关闭且正式版本已同步。
- `conditional`：明确 action、owner、触发器且不破坏 readiness。
- `stop / block`：核心证据/owner 缺失或重大风险未处理。
- `escalate`：权限冲突或残余风险需更高责任人决定。
## Output Contract
输出 Review Record：材料版本、角色、问题、结论、依据、dissent、行动、owner、触发器、阻塞状态及下一次评审条件。
## Handoff
- `reads_from`：PRD、Evidence、Risk、Eval Design。
- `writes_to`：Review Record、新 PRD 版本、Decision log。
- `supports_lifecycle`：Product Definition、Implementation、Build Readiness。
- `may_trigger`：PRD、Feasibility、Evaluation、Replan。
- `reopen_when`：新证据、范围/风险/依赖变化或 action 未满足。
## Completion Criteria
每个问题有结论或 owner；关键角色缺席影响已说明；结论同步到 PRD/计划/eval/风险记录；旧版本不再被误用。
## Boundaries
不把开会当通过，不用评审替代验证，不让润色问题长期阻塞，也不静默覆写正式文档。
