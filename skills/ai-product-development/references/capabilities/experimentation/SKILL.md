---
name: experimentation-pilot
description: Test product value, usability, behavior change, or real-environment quality with the lowest-cost experiment or controlled pilot. Do not run a user pilot for a purely technical question that offline evaluation can answer.
---
# Experimentation & Pilot
## Purpose
用相称实验验证产品机制和真实环境价值，并形成 scale、iterate、narrow 或 stop 决策。
## When to use
problem/solution fit、可用性、行为改变、流程价值或真实环境表现待验证时使用。
## When NOT to use
纯技术质量由离线 eval 可回答；无退出/支持/风险控制；没有待决定假设。
## Decision / Unknown
- `decision_to_inform`：`scale | iterate | narrow | stop`。
- `unknown_to_reduce`：机制、采用、任务结果、人工负担、质量、成本和风险。
- `risk_to_reduce`：demo applause、新奇效应、选择偏差、事后挑指标。
## Required Inputs
- `blocking`：假设/决策、版本、人群/环境、指标/阈值、退出和风险控制。
- `reusable`：Discovery、Prototype、Eval、基线、telemetry。
- `optional`：样本设计、支持资源、历史实验。
## Method
按未知项和环境选择性读取：

- 需要选择实验设计、指标、样本、归因方式和决策规则时，读取 [Experiment Design](references/experiment-design.md)；
- 需要在真实环境管理招募、启用、支持、风险、退出与扩大时，读取 [Pilot Operations](references/pilot-operations.md)。

正式交付使用 [Experiment / Pilot Plan and Readout](templates/experiment-pilot-plan-readout.md)；仅在校准具体程度时查看 [Example](examples/pilot-readout.md)。纯技术质量问题仍交给 Evaluation。
## Evidence Rules
记录版本、样本、环境、分群、指标定义和偏差；行为与态度分开；保留反例；结论仅适用于实际人群/环境；条件变化后重测。
## Decision Rules
- `proceed`：primary 达标且 guardrail 可接受。
- `conditional`：仅特定切片成立，限制扩大。
- `stop / block`：机制无支持、严重风险或设计无法归因。
- `escalate`：高风险试验、隐私/伦理或外部发布权限。
## Output Contract
输出 [Experiment / Pilot Plan and Readout](templates/experiment-pilot-plan-readout.md)：假设、机制、设计、样本、版本、指标/guardrail、阈值、控制、结果、bad cases、限制与决策。
## Handoff
- `reads_from`：Discovery、Prototype、PRD、Eval、Risk。
- `writes_to`：Experiment/Pilot evidence 与 readout。
- `supports_lifecycle`：Validation、Release、Retrospective。
- `may_trigger`：PRD、Roadmap、Evaluation、Launch、Replan。
- `reopen_when`：人群、环境、版本、机制、风险或生产表现变化。
## Completion Criteria
结果支持原决策；价值与质量/理解/成本/风险未混淆；偏差和限制披露；继续/修改/停止按预设标准决定。
## Boundaries
不把展示反馈当采用证据，不做无保护高风险开放试验，不事后挑选成功指标。
