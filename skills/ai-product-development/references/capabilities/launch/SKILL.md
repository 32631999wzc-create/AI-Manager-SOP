---
name: launch-adoption-enablement
description: Plan staged rollout, user enablement, support, and adoption decisions for an AI product release. Do not create a full adoption program for a one-off internal demo.
---
# Launch / Adoption / Enablement
## Purpose
让目标用户安全获得价值，并用分阶段证据决定 proceed、hold、narrow 或 rollback。
## When to use
MVP/生产发布或 AI 行为改变工作流、权限、信任或支持负担时使用。
## When NOT to use
一次性内部 demo；Release Readiness 未具备且当前只需补质量证据；无真实受众。
## Decision / Unknown
- `decision_to_inform`：rollout 人群/阶段、扩容、hold、rollback 与赋能方式。
- `unknown_to_reduce`：发现、激活、首次价值、持续使用、信任、支持与迁移。
- `risk_to_reduce`：上线即成功、隐藏限制、无监控/支持/回滚扩大流量。
## Required Inputs
- `blocking`：Release Readiness、版本、人群、阈值、support/rollback owner。
- `reusable`：价值主张、pilot/eval、known issues、运营渠道。
- `optional`：培训、销售/成功团队、迁移和地区窗口。
## Method
定义发布 outcome/人群；选择 staged rollout；设置进入/退出/freeze；准备能力边界、核验、纠错、反馈和角色化赋能；对齐权限/配置/迁移/支持/沟通；发布时核验版本/telemetry/rollback；按证据决策。
## Evidence Rules
采用指标有定义/分母/切片；连接版本、质量、成本、支持与风险；反馈不等于 outcome；保留未采用和负面信号；版本/人群变化重新评估。
## Decision Rules
- `proceed`：阶段阈值满足且支持/回滚可用。
- `conditional`：限制人群、流量或功能继续观察。
- `stop / block`：readiness、telemetry、支持或 rollback 缺失。
- `escalate`：重大风险、承诺、地区/合规或资源权限。
## Output Contract
输出 Launch and Adoption Plan/Readout：目标、人群、版本、阶段、阈值、赋能、支持/沟通、监控、owner、回滚和阶段决策。
## Handoff
- `reads_from`：PRD、Roadmap slice、Eval、Pilot、Risk、Release Readiness。
- `writes_to`：Launch Plan/Readout 与 adoption evidence。
- `supports_lifecycle`：Release & Operation。
- `may_trigger`：Production Learning、Experimentation、PRD、Replan。
- `reopen_when`：采用、质量、支持、风险、版本或人群与预期不符。
## Completion Criteria
目标用户知道何时/如何/为何使用；阶段与质量/风险证据绑定；支持/回滚可执行；采用问题有定位和 owner。
## Boundaries
不把公告代替采用，不隐藏限制，不在必要运营能力缺失时扩大高风险流量。
