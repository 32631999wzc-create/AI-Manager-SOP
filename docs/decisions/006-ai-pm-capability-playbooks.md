# AI PM Professional Capability 架构

状态：Phase 1 Architecture Alignment 与 Phase 2 Capability Contract 已实施（2026-09-15）；Evidence / Decision 对象仍属于后续 Phase 3。

后续状态注记（2026-09-17）：上句是本决策写作时的历史状态，不是当前进度。Phase 3 的 EvidenceRecord、DecisionRecord、Registry 引用与 Replan reopen trigger 已在后续工作中实施；当前架构见[架构说明](../architecture.md)。下文“后续阶段”保留原决策语境，不追改。

## 问题

八节点生命周期已经能决定何时做什么，但节点正文中的 `Capabilities` 多数仍是能力名，无法稳定指导竞品分析、PRD、需求评审、用户发现、AI 可行性、数据、评测、发布采用和生产反馈等真实工作。仅把节点合同填成非空，不能证明 Skill 具备 AI PM 的操作能力。

## 调研证据

本次优先使用产品团队、研究机构和标准组织的一手资料，而不是把单一公司的流程照抄为固定瀑布：

- OpenAI 的 Core Models PM 职责把用户目标转成模型/系统/研究要求，并建立 `usage + feedback → dataset → eval → experiment → training priority → launch decision` 的闭环，同时平衡质量、价值、延迟、安全、可靠性和成本：<https://openai.com/careers/product-manager-core-models-san-francisco/>。
- OpenAI 的 Youth PM 职责覆盖用户需求、端到端概念到发布迭代、指标/研究驱动路线图及跨设计、研究、政策、法务、财务和运营协作：<https://openai.com/careers/product-manager-youth-san-francisco/>。
- Google PAIR 将 AI 产品设计拆为用户需求与成功、数据与评估、mental models、解释与信任、反馈与控制、错误与优雅失败：<https://pair.withgoogle.com/guidebook-v2/chapters>。
- Microsoft HAX 提供从早期规划到失败场景的跨职能 Human-AI 工具，并强调初次交互、正常交互、出错和随时间变化：<https://www.microsoft.com/en-us/haxtoolkit/>。
- Anthropic 的真实 agent 构建经验强调从最简单方案开始，以清晰 eval 判断增加 workflow/agent 复杂度是否产生可测价值：<https://www.anthropic.com/engineering/building-effective-agents>。
- Anthropic 的 agent eval 实践把 task、trial、grader、transcript 区分开，主张产品团队用 eval-driven development 把要求变得具体，并与生产监控、A/B test、用户研究共同形成质量证据：<https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents>。
- NIST AI RMF 将 GOVERN、MAP、MEASURE、MANAGE 作为贯穿 AI 生命周期的持续风险工作，而非上线前一次性检查：<https://www.nist.gov/itl/ai-risk-management-framework>。

综合这些证据，真实 AI PM 工作不是“传统 PRD + 选模型”，而是两条相互连接的闭环：

1. `真实工作流/机会 → 产品要求 → 方案/数据 → eval → 实验/发布 → 使用与反馈 → 下一轮要求`；
2. `情境/受影响者 → 风险 → 测量 → 控制 → 监控/事件 → 重评`。

## 决策

保留八个 lifecycle、六项 runtime capability 和三个 Gate，不增加顶层阶段。将 `references/capabilities/` 中 16 项统一定义为按需加载的 `Professional Capability Domains`：

1. 用户与机会发现；2. 市场与竞品情报；3. 商业论证与优先级；4. 路线图与版本规划；
5. 产品需求定义；6. 需求评审与决策；7. AI 可行性与原型；8. 数据策略与治理；
9. Human-AI 体验；10. 评测与质量；11. 责任 AI、安全与风险；12. 跨职能交付协作；
13. 实验与试点；14. 发布、采用与赋能；15. 生产观测与学习闭环；16. 复盘与组合学习。

Phase 1 完成职责对齐：Kernel 管路由，Lifecycle 管状态和所需决策，Runtime 管执行，Capability 管专业方法，Gate 管推进判断。

Phase 2 将 16 个 Domain 迁移为独立 `SKILL.md`，统一采用 Purpose、When to use、When NOT to use、Decision / Unknown、Required Inputs、Method、Evidence Rules、Decision Rules、Output Contract、Handoff、Completion Criteria、Boundaries 合同。Planner 通过 lifecycle gap、待解锁决策和 `EXECUTE | VERIFY | REUSE` 模式选择 Capability。

五个高复杂 Domain 已按需拆分：Business Case / Prioritization、Outcome Roadmap / Release Slicing、AI Capability Spike / Product Prototype Test、Eval Design / Eval Run / Eval Readout / Regression、Retrospective / Portfolio Learning。子方法仍由父 Domain 路由，不成为 Lifecycle 或独立状态机。

## 边界

- Capability 由 lifecycle gap 和待解锁决策触发，不是固定 checklist，也不会自动生成 16 个任务或第二套状态机。
- 市场、商业化、法务、组织或组合管理只在当前产品决策确实需要时启用；Skill 不成为企业管理百科。
- 详细专业方法只在 capability canonical file 维护，lifecycle 只规定必需状态、决策、路由与完成条件。
- 外部资料用于提炼决策原则，不复制受版权保护的长文本；法律适用性由有资质责任人确认。

## 后续阶段

下一步是 Phase 3 Evidence & Decision Layer：定义 EvidenceRecord、DecisionRecord，接入 Registry，并支持 reopen trigger。本次按用户要求未运行测试，也未提前进入 Phase 3。
