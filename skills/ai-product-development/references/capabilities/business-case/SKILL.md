---
name: business-case-prioritization
description: Decide whether an AI product opportunity merits investment and how competing opportunities should be prioritized when value, cost, risk, evidence, and timing must be compared. Do not use for a single already-approved task with no resource trade-off.
---

# Business Case & Prioritization

## Purpose
把机会的价值机制、成本、风险、证据强度和时机转成可解释的投资与优先级决策。

## When to use
投入合理性待证明、多个机会竞争资源、MVP 边界待定，或 AI 成本/风险可能抵消用户价值时使用。

## When NOT to use
单个任务已获批准且没有资源取舍；缺少问题证据时先 Discovery；只需安排依赖顺序时使用 Planner。

## Decision / Unknown
- `decision_to_inform`：`invest | test | defer | reject` 及候选项顺序。
- `unknown_to_reduce`：价值机制、受益规模、采用、成本、可行性、风险和敏感参数。
- `risk_to_reduce`：虚假精确 ROI、不同粒度混排、公式掩盖风险与证据弱项。

## Required Inputs
- `blocking`：决策单位、候选项、业务目标与资源/风险约束。
- `reusable`：Discovery、市场证据、成本数据、可行性和历史结果。
- `optional`：使用量、转化、收入、工时、战略窗口与容量。

## Method
先按当前 gap 选择[商业论证](business-case.md)、[优先级决策](prioritization.md)或两者；不要把两个输出机械合并为一个总分。

## Evidence Rules
每个价值链节点、成本输入和风险判断标明证据/假设、owner、范围和时效；展示原始输入与敏感性；保留反证和不可比较项。

## Decision Rules
- `proceed`：价值机制可信、成本/风险可接受且相对选择稳健。
- `conditional`：关键假设可用低成本实验消除，先 `test`。
- `stop / block`：输入不可比、风险 floor 未处理或结论依赖捏造数据。
- `escalate`：财务承诺、重大残余风险或战略取舍超出当前 owner 权限。

## Output Contract
输出 Business Case、Priority Decision 或二者：决策、价值机制、证据/假设、成本、风险、比较、敏感性、推荐与复议条件。

## Handoff
- `reads_from`：Discovery、Competitive Intelligence、Feasibility、成本与风险 Evidence。
- `writes_to`：Business Case / Priority Decision。
- `supports_lifecycle`：Qualification、Product Definition & Scope、Retrospective。
- `may_trigger`：Roadmap、Experimentation、AI Feasibility、PRD。
- `reopen_when`：关键假设、成本、采用、风险、容量或战略窗口变化。

## Completion Criteria
能解释为什么现在做及为什么不是其他项；价值、成本、风险和证据强度可追溯；高风险未被平均；`invest/test/defer/reject` 与复议条件明确。

## Boundaries
不捏造规模/转化/成本，不用公式代替判断，不把战略口号当用户价值证据，不替有权限者接受重大风险。
