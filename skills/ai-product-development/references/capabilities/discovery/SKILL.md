---
name: user-opportunity-discovery
description: Discover and validate an AI product user's real workflow, problem, and opportunity when the decision is still based on assumptions or insufficient behavioral evidence. Do not use when the problem is already supported by current evidence and the task only concerns delivery or validation.
---

# User & Opportunity Discovery

## Purpose

降低对目标用户、真实工作流、问题强度和机会价值的不确定性，为是否继续、面向谁、解决什么及是否值得进入产品定义提供证据。

## When to use

- 目标用户、问题、现有替代流程或 desired outcome 尚未被可靠证明；
- 团队只有功能想法、利益相关者意见或零散反馈，需要验证真实行为；
- pilot、生产反馈或 bad case 暗示旧的问题定义可能需要重新打开。

## When NOT to use

- 当前问题已由新鲜、可追溯且覆盖目标情境的证据支持，本次只负责实现、发布或按既定标准验证；
- 需要回答的是市场格局、商业回报、AI 技术可行性或方案质量，应分别调用对应 Capability；
- 无法接触任何真实证据且决策又不可逆、高影响；此时应标记阻塞，不用假设替代发现。

## Decision / Unknown

- `decision_to_inform`：是否继续探索或投入；优先服务哪个用户/场景；问题和 desired outcome 如何定义；是否需要重新打开现有产品决策。
- `unknown_to_reduce`：谁在什么情境下执行什么工作；当前触发、步骤、判断、交接、例外和结果；问题的频率、严重度、现有替代方案与未满足程度。
- `risk_to_reduce`：把意见当行为、便利样本偏差、遗漏受影响者、错误因果归因、把 AI 或原型预设为答案。

## Required Inputs

### Blocking

- 当前要影响的决策及其决策人；
- 候选用户、工作情境或受影响群体的最小边界；
- 可用证据渠道，或无法获取证据的明确限制。

### Reusable

- 既有访谈、观察、研究报告、工单、支持记录、日志、pilot/生产反馈；
- 当前 Product Definition、Decision、版本与历史假设。

### Optional

- 领域专家、流程图、业务指标、竞品或替代方案使用记录；
- 可用于招募和切片的用户特征。

## Method

按当前未知项选择性读取：

- 需要设计样本、证据组合、访谈或情境观察时，读取 [Research Design](references/research-design.md)；
- 需要还原工作流、综合多来源证据并形成机会判断时，读取 [Workflow Synthesis](references/workflow-synthesis.md)；
- 需要正式交付时使用 [Discovery Brief Template](templates/discovery-brief.md)；仅在校准输出粒度时查看 [Example](examples/discovery-brief.md)。

不要为了完整性同时加载所有资源；已有研究只需核验时，读取与缺口直接相关的一个 reference。

## Evidence Rules

- `acceptable sources`：直接观察、可追溯访谈记录、任务/产品日志、工单、支持记录、已有研究和 pilot/生产证据；利益相关者意见只能作为待验证输入。
- `fact vs assumption`：观察到的行为、用户解释和团队推断分栏记录；未经证实的解释保持 assumption。
- `traceability`：每个重要结论引用访谈/观察 ID、日志查询、工单、报告或生产事件，并关联时间、用户切片和产品版本。
- `counter evidence`：主动保留不符合主叙事的样本、无问题用户、替代解释和失败招募，不以多数意见抹掉高影响反例。
- `confidence`：置信度同时考虑来源直接性、方法互证、样本覆盖、一致性和决策风险；不只按样本数量判断。
- `freshness`：工作流、产品版本、用户结构或外部约束变化后，旧证据必须降级或重新验证。

## Decision Rules

- `proceed`：目标用户和情境明确，问题由行为/结果证据支持，严重度足以改变当前决策，且关键反证不会推翻机会判断。
- `conditional`：方向有支持但切片、频率、影响或机制仍不确定；限制范围，并把下一项证据设为后续决策条件。
- `stop / block`：问题主要来自功能偏好或内部意见；证据与假设冲突且无法消解；高影响决策缺少必要受影响者证据。
- `escalate`：发现重大安全、隐私、合规、歧视或组织权限问题，转交相应 owner，并按需触发 Responsible AI Capability。

## Output Contract

输出 [Discovery Brief](templates/discovery-brief.md)。正式结论必须能追溯到 Evidence；尚未确认的内容保持 assumption。

## Handoff

- `reads_from`：Qualification、当前 Product Definition、已有 Evidence/Decision、pilot 或生产信号。
- `writes_to`：Discovery Brief；Phase 3 对象接入后写入或引用 EvidenceRecord，并为 DecisionRecord 提供依据。
- `supports_lifecycle`：Qualification、Product Definition & Scope；生产信号触发时也支持 Retrospective 与 Replan。
- `may_trigger`：Market & Competitive Intelligence、Business Case & Prioritization、AI Feasibility & Prototyping、Product Requirements、Responsible AI / Safety / Security。
- `reopen_when`：目标用户或工作流变化；新版本、pilot、生产行为或 bad case 与原问题假设冲突；关键证据过期；原 decision 的 reopen trigger 命中。

## Completion Criteria

- 当前决策已得到 `proceed | conditional | stop/block | escalate` 之一，且依据与限制明确；
- 问题来自可追溯行为或结果证据，不是功能偏好汇总；
- 谁受益、谁承担成本、问题发生在哪里以及当前如何解决均已说明；
- 反证、样本偏差、置信度和 freshness 已处理；
- 证据足够支持当前决策，或缺口已被标记为明确阻塞/后续条件；
- 输出已交给所支持的 Lifecycle 或触发的下游 Capability。

## Boundaries

不要伪造访谈、用户原话、日志或市场规模；不要把少量便利样本外推为全体用户；不要用漂亮原型代替问题证据；不要把 Discovery 变成竞品分析、商业论证或详细方案设计；不要因调用本 Capability 自动创建新的 Lifecycle、Gate、Agent 或状态机。
