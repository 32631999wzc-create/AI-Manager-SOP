---
name: retrospective-portfolio-learning
description: Turn a completed version, pilot, incident, or project stage into evidence-backed learning, or compare multiple opportunities for continued investment. Do not create a ceremonial timeline or generalize one project's preferences into global rules.
---
# Retrospective & Portfolio Learning
## Purpose
区分结果、决策质量和运气，保留能改变下一轮决策的学习与可复用资产。
## When to use
版本/pilot/事件/阶段结束，或需跨用例比较继续投资时使用。
## When NOT to use
没有新证据或决策价值；只想写流水账；当前仍在执行且尚不能形成结论。
## Decision / Unknown
- `decision_to_inform`：保持/改变什么，继续/停止/扩大什么，哪些决策需重开。
- `unknown_to_reduce`：结果差距、决策质量、根因、债务、可复用杠杆和组合价值。
- `risk_to_reduce`：事后改目标、相关当因果、结果运气代替决策质量、过度泛化。
## Required Inputs
- `blocking`：原始目标/范围/Decision、最终证据和版本。
- `reusable`：计划、eval、pilot、生产/事件、成本和风险 Evidence。
- `optional`：跨产品基线、资产 registry、团队反馈。
## Method
单项目学习使用[retrospective](retrospective.md)；跨用例投资与杠杆判断使用[portfolio learning](portfolio-learning.md)；两者分开输出，避免局部经验自动升级为组合规则。
## Evidence Rules
对照原始目标和当时证据；事实/解释分开；保留 dissent、反事实和限制；跨项目结论需共同口径与多场景证据；旧学习受新证据重开。
## Decision Rules
- `proceed`：学习可改变明确后续决策且证据充分。
- `conditional`：保留为待验证假设而非规则。
- `stop / block`：无证据、无法归因或只剩叙事。
- `escalate`：组合投资、重大事件责任或组织流程变更超权限。
## Output Contract
输出 Retrospective 和/或 Portfolio Learning：目标/结果、Evidence、Decision、假设、根因、债务、资产、继续/停止条件、owner 与 reopen trigger。
## Handoff
- `reads_from`：原始 Decision/Plan、最终 Evidence、Registry。
- `writes_to`：学习、行动、资产和重开建议。
- `supports_lifecycle`：Retrospective、Product Definition、Qualification。
- `may_trigger`：Discovery、Business Case、Roadmap、PRD、Replan。
- `reopen_when`：行动触发、新证据推翻根因/假设或组合约束变化。
## Completion Criteria
学习可追溯且不混淆相关/因果；行动改变后续决策；资产/债务有 owner；局部经验未过度泛化；需重开决策明确。
## Boundaries
不写流水账，不追责个人，不把未经验证偏好写入全局 Skill。
