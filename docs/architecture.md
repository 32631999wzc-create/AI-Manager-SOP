# 架构说明

正式入口为 [Skill Kernel](../skills/ai-product-development/SKILL.md)。Phase 1 重组规则并验证按需读取，Phase 2 将对象与 Profile/Plan 规则变为只读确定性验证，Phase 3 在其上提供本地文件化 continuous runtime。

## Progressive disclosure

技能发现时使用 name / description；技能启用后读取 Kernel；具体操作开始前才读取相关 reference。Profile 为八节点记录状态，不要求预读八节点详情。VERIFY 对应当前确有需要的核验；已有确认可复用材料可以满足依赖，不能据此机械扫描所有 VERIFY 节点。

依赖闭包由原 [Execution Profile](../skills/ai-product-development/references/runtime/execution-profile.md#67-dependency-closure) 决定。例如缺少验收标准的验证需要补充 Evaluation Design；已有可复用标准的只读核验不因此重建方案。支持性导航、局部规则检查和合法依赖读取不视为失败。

## 五层职责与 canonical rule

仓库采用五层结构：`Kernel → Lifecycle → Runtime → Professional Capabilities → Evidence / Decision / Artifact`。

- [Skill Kernel](../skills/ai-product-development/SKILL.md#4-architecture-and-responsibility-boundary) 保存全局原则、复杂度约束、Progressive Disclosure 与 Router；
- [Lifecycle references](../skills/ai-product-development/references/lifecycle) 保存八个产品状态及其必需决策，不保存专业方法；
- [Runtime references](../skills/ai-product-development/references/runtime) 保存 Profile、Planner、Context、Executor、Registry、Replan 六项执行能力；
- [Professional Capability domains](../skills/ai-product-development/references/capabilities) 保存资深 AI PM 完成特定分析或决策的方法；
- Evidence、Decision 与 Artifact 保存“依据、选择、结果”；EvidenceRecord、DecisionRecord 与 Artifact 引用已接入同一 Registry。

Gate 只使用证据决定是否推进，不执行专业分析。Registry 只记录当前有效的事实、决策和产物，不替代 Capability 或 Gate。一个文件不代表一个 Agent。Planner 的任务依赖和 Profile 的节点依赖职责不同，也不新增 Capability 状态机。

[Professional Capability domains](../skills/ai-product-development/references/capabilities) 按 Decision、Design、Operating、Planning & Learning 四类组织。它们使用 gap 和待解锁决策触发，而不是固定阶段顺序；新增 domain 不改变八节点、六项 Runtime capability 或三个 Gate。Data、Evaluation、Responsible AI 与 Production Learning 可跨 Lifecycle 调用。

专业深度继续使用三级 progressive disclosure：Kernel 只路由到被选 Capability 的 `SKILL.md`；Capability 入口再按当前未知项选择 `references/` 中的方法；`templates/` 仅在生成对应正式交付物时读取，`examples/` 仅在需要校准输出粒度时读取。不得因选中一个 Capability 而默认加载其全部支持资源。

详细规则只在 canonical location 维护，其他文件使用摘要或链接。例如 Replan 判断产物失效和版本时读取 Registry，包括只提出建议的任务；链接不授予写入权限。优先级、复杂度 guardrails 和共用完成标准保留在 Kernel。

八个 lifecycle 模块只保留 Purpose、Activation Conditions、Required Inputs、Required Decisions / State、Capability Routing、Outputs、Completion Criteria、Dependencies、Boundaries。专业方法只在 capability canonical file 中维护；统一的是状态合同，不是固定任务清单。

[schemas](../skills/ai-product-development/schemas) 保存 canonical 结构示意，包括 Phase 3 新增的 EvidenceRecord 与 DecisionRecord。只读 [runtime validator](../skills/ai-product-development/scripts/validate_runtime.py) 将这些字段、枚举及 Profile / Plan 的交叉规则变成确定性检查；验证包装层只承载检查上下文，不新增 ExecutionProfile canonical schema、默认值或状态存储。

稳定输出仅有 [Plan Preview](../skills/ai-product-development/templates/execution-plan.md)。其他输出没有字段级固定格式，其规则保留在对应节点。

## Local continuous runtime

当产品确有跨任务或跨会话连续性需要时，[Continuous Project Runtime](../skills/ai-product-development/scripts/project_runtime/README.md) 在产品仓库创建 `.ai-product/`。Plan 是 Task 的唯一持久来源，Registry 是 ProjectRecord、EvidenceRecord、DecisionRecord 与 Artifact 的唯一持久来源；运行时在验证时组装 Phase 2 wrapper，避免复制 canonical 状态。Snapshot 只保存引用和状态，Context Pack 按当前 READY Task 重建。

这仍对应 Profile、Planner、Context、Executor、Registry、Replan 六项能力。文件存储和 CLI 不是新生命周期节点或 Manager。初始化目录整体提交，后续单文件使用临时文件与原子替换；恢复还会检查 Plan 版本、Task 状态、ACTIVE Registry 引用和正式产物文件。

固定 [Feedback Organizer Golden MVP](../examples/ai-product-development/golden-feedback-organizer/README.md) 用离线确定性行为证明可运行、可验收和证据可追溯。真实模型 Provider、多人并发、数据库、云端状态和生产部署保留为项目触发后的扩展，不是 Skill 默认基础设施。

## 验证边界

结构验证检查链接、路由、Gate、源规则迁移、枚举和明显详细规则重复；不能证明模型行为。70 个源标题映射和 533 条逐行迁移指纹提供迁移证据，仍需审阅摘要和去重是否改变语义。

三个 [Routing Test](../tests/ai-product-development/routing/README.md) 分别在新临时目录、新 ephemeral Codex 进程中运行。受测进程始终使用 read-only；父进程准备 Skill 副本并记录 trace。成功命令与完整文件输出才是读取证据，最终自述仅作辅助。额外读取和 dependency closure 按场景审阅，不规定绝对最少文件数。

三个有限路由 smoke tests 不证明完整产品交付能力。Phase 2 已用八组固定 fixture、正负例和隔离 Codex trace 验证 Profile、Plan、边界及按需读取；证据由哈希 manifest 固定并可从原始 trace 回放。Phase 3 continuous runtime 与 Golden MVP 已按 [Phase 3 决策记录](decisions/004-phase-3-continuous-golden-mvp.md)完成；四会话证据见 [Golden 报告](../tests/ai-product-development/phase3/golden/report.md)。本次接受远程已删除旧占位目录的状态。迁移与未解决语义疑点见 [重构记录](decisions/001-modularize-ai-product-development.md)，任务边界见 [Phase 2 任务书](decisions/002-content-cleanup-and-phase-2-plan.md)，完成结果见 [Phase 2 完成记录](decisions/003-phase-2-executable-validation.md)。
