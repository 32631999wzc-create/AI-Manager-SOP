---
name: roadmap-release-planning
description: Translate validated product outcomes and uncertainty into cross-version direction, learning milestones, dependencies, and releasable slices. Do not use when a single scoped task can be handled by the runtime Planner DAG.
---

# Roadmap & Release Planning

## Purpose
把已确认目标、优先级和不确定性转成跨版本方向与可验证发布切片，而不是功能日历。

## When to use
需要跨版本取舍、学习里程碑、承诺层级、依赖顺序或 release slice 时使用。

## When NOT to use
单个明确任务由 Planner DAG 足以管理；目标或优先级尚未决定；仅需部署执行。

## Decision / Unknown
- `decision_to_inform`：Now/Next/Later、版本切片、承诺程度和停止条件。
- `unknown_to_reduce`：能力阈值、学习依赖、容量、外部依赖和发布时间窗口。
- `risk_to_reduce`：远期虚假确定性、组件式版本、把路线图当销售承诺。

## Required Inputs
- `blocking`：产品 outcome、优先级、成功指标和硬约束。
- `reusable`：Business Case、Feasibility、依赖、风险和现有 roadmap。
- `optional`：容量、发布窗口、市场时机和历史吞吐。

## Method
跨版本方向使用[outcome roadmap](outcome-roadmap.md)；把方向转成可独立验证版本时使用[release slicing](release-slicing.md)；只加载当前需要的方法。

## Evidence Rules
主题与切片必须关联产品目标、Evidence、关键假设和依赖；承诺程度与证据成熟度一致；保留被推迟/不做项与反证。

## Decision Rules
- `proceed`：近期切片有清晰 outcome、依赖与退出证据。
- `conditional`：关键能力/市场假设需先过学习里程碑。
- `stop / block`：目标未定、依赖不闭合或版本只是技术组件集合。
- `escalate`：跨团队容量或外部承诺超出当前 owner 权限。

## Output Contract
输出 outcome roadmap 和/或 release plan：主题、目标、指标、证据、依赖、风险、切片、进入/退出条件、承诺程度、owner、更新与复议触发器。

## Handoff
- `reads_from`：Priority Decision、Product Definition、Feasibility、风险与容量证据。
- `writes_to`：Outcome Roadmap / Release Slices。
- `supports_lifecycle`：Product Definition & Scope、Release & Operation、Retrospective。
- `may_trigger`：PRD、Feasibility、Experimentation、Launch、Planner。
- `reopen_when`：优先级、能力证据、风险、容量、依赖或市场窗口变化。

## Completion Criteria
近期工作可追溯到目标与优先级；每个版本是可验证完整增量；不确定性、依赖和承诺可见；明确不做项与复议条件。

## Boundaries
不把路线图当精确排期或销售承诺，不为远期制造假确定性，不用功能数量衡量进展。
