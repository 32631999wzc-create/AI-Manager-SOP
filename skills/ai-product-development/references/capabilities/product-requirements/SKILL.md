---
name: product-requirements
description: Define an approved opportunity or release slice as an implementable and evaluable product contract. Do not use a full PRD for an exploratory prototype that only needs a one-page hypothesis brief.
---

# Product Requirements

## Purpose
把已选择机会定义为对产品、设计、工程、数据、评测和运营具有一致含义的需求合同。
## When to use
机会或版本切片已选定，需要明确范围、行为、失败、验收、依赖和观测时使用。
## When NOT to use
问题/机会未验证；单一探索假设用 one-page brief 足够；需要的是技术设计或评测执行。
## Decision / Unknown
- `decision_to_inform`：做什么、不做什么、行为边界和何时算好。
- `unknown_to_reduce`：场景变体、失败合同、权限/数据、验收、依赖和 owner。
- `risk_to_reduce`：愿望包装成需求、方案伪装成需求、不可判定措辞和范围漂移。
## Required Inputs
- `blocking`：用户/问题证据、目标 outcome、版本、Assignment Scope。
- `reusable`：Discovery、市场、优先级、Feasibility、设计/风险约束。
- `optional`：流程、原型、历史 PRD、指标与运营要求。
## Method
定义 why now、用户、问题、基线、outcome；覆盖主路径与空/错/不确定/超时/拒绝/升级；用可观察行为写要求；明确 AI 能/不能、错误成本、控制和反馈；把每项重要 requirement 连接验收证据；检查 problem→requirement→eval→production traceability。
## Evidence Rules
背景和要求引用来源；事实/假设分开；冲突与反证进入 open question；版本、owner、freshness 可见；不得把未验证技术能力写成承诺。
## Decision Rules
- `proceed`：范围、行为和验收对各职能解释一致。
- `conditional`：非阻塞假设有 owner 和触发条件。
- `stop / block`：核心问题、AI 边界或验收仍不可判定。
- `escalate`：重大范围、风险或资源取舍交 decision owner。
## Output Contract
输出版本化 PRD/brief：背景证据、目标/非目标、用户场景、范围、要求、AI 行为与失败合同、数据/权限/风险、指标/验收、依赖、开放项、决策与观测要求。
## Handoff
- `reads_from`：Discovery、Priority、Roadmap、Feasibility 与风险 Evidence。
- `writes_to`：PRD/brief。
- `supports_lifecycle`：Product Definition & Scope、Solution Design。
- `may_trigger`：Requirement Review、Data、Human-AI、Evaluation、Responsible AI。
- `reopen_when`：用户问题、范围、能力、风险、验收或版本假设变化。
## Completion Criteria
做什么、为什么、何时算好解释一致；关键 AI 行为和失败可验证；非目标明确；开放项有 owner/触发器；阻塞未隐藏。
## Boundaries
不虚构证据，不堆砌实现规格，不用“准确率高/体验好/响应快”等不可判定措辞，不静默覆写正式版本。
