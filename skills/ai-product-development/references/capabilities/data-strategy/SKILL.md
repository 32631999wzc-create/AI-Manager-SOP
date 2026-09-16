---
name: data-strategy-governance
description: Define data purpose, provenance, rights, quality, labeling, access, lifecycle, and drift controls when AI product decisions depend on training, retrieval, evaluation, personalization, or feedback data. Do not collect data without a named decision or product use.
---
# Data Strategy & Governance
## Purpose
确保每类数据有合法用途、可信质量、明确 owner 和可持续生命周期，并把数据限制反馈到产品承诺。
## When to use
训练、检索、上下文、eval、个性化或反馈依赖数据，且权利、质量、代表性、漂移或保留影响决策时使用。
## When NOT to use
任务不依赖数据决策；仅需读取已验证数据；没有明确用途的数据盘点。
## Decision / Unknown
- `decision_to_inform`：可否使用、用于什么、如何采集/标注/治理、是否阻塞范围或发布。
- `unknown_to_reduce`：来源、权利、质量、覆盖、泄漏、偏差、lineage、refresh 和 owner。
- `risk_to_reduce`：无同意训练、测试泄漏、未知来源、过度收集和反馈误作真值。
## Required Inputs
- `blocking`：data-to-decision 用途、候选来源、权限/隐私边界。
- `reusable`：数据字典、许可、质量报告、版本、lineage、eval 设计。
- `optional`：标注资源、专家、漂移和历史事件。
## Method
建立用途图；盘点 provenance/owner/许可/敏感度；按目标任务检查质量、代表性、泄漏和偏差；设计标注 rubric 与抽检；定义最小权限、保留/删除、版本/lineage/refresh/drift；缺口反馈 PRD、eval、路线图或非 AI 方案。
## Evidence Rules
每个数据结论引用来源、许可、版本、样本范围和检查结果；事实/假设分开；保留缺失切片和反证；权利或分布变化触发重新验证。
## Decision Rules
- `proceed`：用途、权利、质量、owner 和控制足够。
- `conditional`：限制场景/人群并设置采集或监控条件。
- `stop / block`：关键来源、权利、质量或泄漏不可接受。
- `escalate`：隐私、版权、地域、敏感数据或风险接受需专业 owner。
## Output Contract
输出 Data Strategy：用途图、inventory、provenance/rights、质量/代表性、采集/标注、访问/保留/删除、version/lineage、refresh/drift、缺口、owner、release blocker。
## Handoff
- `reads_from`：PRD、AI flow、Eval Design、Risk。
- `writes_to`：Data Strategy 与数据证据。
- `supports_lifecycle`：Cognition、Solution Design、Validation、Release。
- `may_trigger`：PRD、Evaluation、Risk、Replan。
- `reopen_when`：来源、许可、分布、用途、模型、政策或质量变化。
## Completion Criteria
关键数据用途、权利、质量和 owner 清楚；泄漏/偏差已处理；生命周期可执行；缺口已转成范围、任务或阻塞。
## Boundaries
不默认行为等于训练同意，不以数据量替代用途/质量，不登记未知来源为正式可用数据。
