---
name: market-competitive-intelligence
description: Investigate competitors, substitutes, and market conditions when external evidence could change product positioning, scope, priority, or entry decisions. Do not use only for visual inspiration or to copy a competitor feature list.
---

# Market & Competitive Intelligence

## Purpose
用可复核的外部证据判断替代方案、竞争差异、威胁和进入条件如何改变产品决策。

## When to use
当竞品、替代流程、定价、市场变化或差异化会影响定位、范围、优先级或 go/no-go 时使用。

## When NOT to use
只需要 UI 灵感、已有新鲜证据足以支持当前决策，或问题实质是用户发现/市场规模/详细商业论证时不使用。

## Decision / Unknown
- `decision_to_inform`：进入、差异化、追平、避让或放弃什么。
- `unknown_to_reduce`：真实替代方案、任务表现、切换成本、可复制性和变化速度。
- `risk_to_reduce`：营销声明当事实、选择性比较、版本/地区/套餐失配和抄袭式需求。

## Required Inputs
- `blocking`：决策问题、目标用户/场景、比较边界与时间点。
- `reusable`：已有竞品研究、用户替代方案证据、产品实测、官方资料。
- `optional`：定价、案例、状态页、发布说明和领域专家判断。

## Method
定义比较问题与直接/间接/人工/自建/不行动基线；优先用一手且有日期的证据；对同一真实任务做 scenario teardown；分开事实、亲测、声明和推断；把差异转成定位、范围、验证或 no-go 决策。

## Evidence Rules
关键结论必须记录来源、日期、版本、套餐、地区和测试条件；二手资料只作线索；保留反例、竞品优势和不确定项；外部快速变化后旧证据降级。

## Decision Rules
- `proceed`：多源证据支持可行动差异且与目标用户价值相关。
- `conditional`：方向成立但能力、定价或切换行为仍需实测。
- `stop / block`：只有功能表、营销页或无来源份额，无法支持决策。
- `escalate`：涉及法律、知识产权、采购或战略权限时交给相应 owner。

## Output Contract
输出 `Competitive Intelligence Brief`：决策问题、比较集、证据台账、场景矩阵、事实/推断、差异与威胁、建议、置信度、时效和刷新触发器。

## Handoff
- `reads_from`：Discovery、Product Definition、已有市场 Evidence。
- `writes_to`：Competitive Intelligence Brief；后续接入 EvidenceRecord/DecisionRecord。
- `supports_lifecycle`：Product Definition & Scope、Retrospective。
- `may_trigger`：Business Case、PRD、Roadmap、AI Feasibility。
- `reopen_when`：竞品版本、定价、市场边界或用户替代行为实质变化。

## Completion Criteria
比较集覆盖真实替代方案；关键结论可复核且有时效；用户价值与功能存在性分开；结果实际改变或确认了范围、定位、优先级、验证计划或 no-go。

## Boundaries
不复制竞品文案，不用无来源市场份额，不把竞品已有功能自动变成本产品需求，不越权执行采购或战略承诺。
