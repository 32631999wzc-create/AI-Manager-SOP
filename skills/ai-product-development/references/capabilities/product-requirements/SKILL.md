---
name: product-requirements
description: Draft, revise, or verify a cross-industry PRD from an approved opportunity or release slice, with traceable evidence, requirements, and acceptance criteria. Do not use a full PRD for an exploratory prototype that only needs a one-page hypothesis brief.
---

# Product Requirements

## Purpose
把已选择机会或版本切片自动撰写为对产品、设计、工程、数据、评测和运营具有一致含义的需求合同。行业、客户类型和交付格式由当前任务决定，不预设智慧城市、政企或招投标场景。
## When to use
机会或版本切片已选定，需要从材料起草、修订或核验 PRD，并明确范围、行为、失败、验收、依赖和观测时使用。
## When NOT to use
问题/机会尚未选定且当前任务是机会发现；单一探索假设用 one-page brief 足够；用户要的是解决方案报告、技术设计、报价或评测执行，而不是产品需求合同。
## Decision / Unknown
- `decision_to_inform`：做什么、不做什么、行为边界和何时算好。
- `unknown_to_reduce`：场景变体、失败合同、权限/数据、验收、依赖和 owner。
- `risk_to_reduce`：愿望包装成需求、方案伪装成需求、不可判定措辞和范围漂移。
## Required Inputs
- `blocking`：目标用户/使用角色、待解决问题、目标 outcome、版本或交付切片、Assignment Scope；缺少决定范围与验收的关键输入时先澄清或明确阻塞，不能补造事实。
- `reusable`：Discovery、市场、优先级、Feasibility、设计/风险约束。
- `optional`：流程、原型、历史 PRD、指标与运营要求。
## Method
自动起草或实质修订 PRD 前，必须读取[跨行业 PRD 自动撰写方法](references/prd-drafting.md)；仅核验既有 PRD 时按核验缺口决定是否读取。先盘点现有证据、决策、旧版 PRD 与未确认假设；可从已有方案发现待核实问题，但不得用方案倒填证据。无用户指定模板时，交付物的一级结构为 `Why → What → How`，其余内容放在对应部分：Why 说明特定用户/组织的现状、痛点、目标和证据；What 把痛点转为场景、范围、可观察需求及优先级，不预设技术实现；How 说明验收、交付依赖和运营观测，技术选型与报价仅在委托范围内或经独立决策后写入。按需读取并裁剪[PRD 模板](templates/prd.md)，不要求填满所有栏目。
## Evidence Rules
背景和要求引用来源；事实/假设分开；冲突与反证进入 open question；版本、owner、freshness 可见；不得把未验证技术能力写成承诺。不能把功能动机、潜在收益或场景推断写成已证实痛点；没有正式 EvidenceRecord ID 时用材料名称引用，不编造正式记录编号。
## Decision Rules
- `proceed`：范围、行为和验收对各职能解释一致。
- `conditional`：非阻塞假设有 owner 和触发条件。
- `stop / block`：核心问题、AI 边界或验收仍不可判定。
- `escalate`：重大范围、风险或资源取舍交 decision owner。
## Output Contract
输出版本化 PRD/brief：背景证据、目标/非目标、用户场景、范围、要求、适用时的 AI 行为与失败合同、数据/权限/风险、指标/验收、依赖、开放项、决策与观测要求。每个核心痛点应能追溯到需求、验收和预期收益；未获证据支持的收益只能标为待验证假设。
## Handoff
- `reads_from`：Discovery、Priority、Roadmap、Feasibility 与风险 Evidence。
- `writes_to`：PRD/brief。
- `supports_lifecycle`：Product Definition & Scope、Solution Design。
- `may_trigger`：Requirement Review、Data、Human-AI、Evaluation、Responsible AI。
- `reopen_when`：用户问题、范围、能力、风险、验收或版本假设变化。
## Completion Criteria
做什么、为什么、何时算好解释一致；Why 的核心痛点、What 的需求、How 的验收与收益对应；关键 AI 行为和失败可验证；非目标明确；开放项有 owner/触发器；阻塞未隐藏。按撰写方法中的交付检查逐项自查。
## Boundaries
不虚构证据，不堆砌实现规格，不用“准确率高/体验好/响应快”等不可判定措辞，不静默覆写正式版本。
