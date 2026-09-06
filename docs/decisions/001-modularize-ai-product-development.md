# AI Product Development 结构性模块化重构

## 决策与来源

按 Preserve semantics → Split by responsibility → Add routing → Remove duplication → Validate 执行。来源为用户提供的完整 SKILL.md，共 945 行，SHA-256：0db07435d169006990aeeabdecbb4b9f09210a00390a76d78ffb516e0ca18ace。

该完整源文件此前未存在于 Git 历史，仓库只有 ai-product-sop 占位文件。本次将外部源文模块化导入 ai-product-development，保留历史占位目录，不将目录占位误报为被重构的完整旧版本。源文未重复提交，指纹与逐行归属保存在 [迁移清单](../../tests/ai-product-development/migration-manifest.json)。

## 原 section → canonical location

路径均相对 skills/ai-product-development。

| 原 section | 新位置 |
|---|---|
| Frontmatter / Activation | SKILL.md，原文保留 |
| 1 Operating Principles | SKILL.md |
| 2 Lifecycle | SKILL.md，八节点及顺序不变 |
| 3 Runtime | SKILL.md，六能力不变 |
| 4 Core Data / Task | schemas/task.yaml |
| 4 Project Record / Artifact / Runtime Snapshot | schemas/project-state.yaml |
| 5 Qualification 前置规则、5.0、5.3、5.4 | references/lifecycle/01-qualification.md |
| 5.1 Delivery Target、5.2 Assignment Scope 规则 | references/runtime/execution-profile.md |
| 5.2 AssignmentScope 字段 | schemas/execution-profile.yaml |
| 5.5 Qualification Gate | references/runtime/gates.md |
| 6 NodeProfile 字段 | schemas/execution-profile.yaml |
| 6.1–6.7、6.9 | references/runtime/execution-profile.md |
| 6.8 Rule Precedence | SKILL.md |
| 7.1 Qualification | references/lifecycle/01-qualification.md，与 section 5 合并 |
| 7.2 Cognition | references/lifecycle/02-cognition.md |
| 7.3 Product Definition & Scope | references/lifecycle/03-product-definition.md |
| 7.4 Solution Design 能力组 | references/lifecycle/04-solution-design.md |
| 7.4 Build Readiness | references/runtime/gates.md |
| 7.4 确定性评估足够时不强制 LLM Judge | references/runtime/executor.md，Solution Design 引用 |
| 7.5 Implementation | references/lifecycle/05-implementation.md |
| 7.6 Validation & Iteration | references/lifecycle/06-validation-iteration.md |
| 7.7 Release & Operation | references/lifecycle/07-release-operation.md |
| 7.8 Retrospective | references/lifecycle/08-retrospective.md |
| 8 Plan 字段 | schemas/plan.yaml |
| 8.1–8.8 Planner | references/runtime/planner.md |
| 9 TaskContextPack 字段 | schemas/context-pack.yaml |
| 9 Context 规则 | references/runtime/context.md |
| 10 Executor | references/runtime/executor.md |
| 11 Registry and Versioning | references/runtime/registry-versioning.md |
| 12 Replan and Recovery | references/runtime/replan-recovery.md |
| 13 Flow Gates | references/runtime/gates.md |
| 14 Complexity Guardrails | SKILL.md |
| 15 Execution Style | SKILL.md；Plan Preview 格式移到 templates/execution-plan.md |
| 16 End-to-End Procedure | SKILL.md |
| 17 Completion Criteria | SKILL.md；其他文件链接引用 |

## 去重与边界

- Qualification 的 section 5 详细过程与 7.1 职责汇总合入同一文件，不再保留一套完整 Registry 副本。
- Gate 的 section 5.5、7.4、13 集中到 gates.md；节点只链接 Gate。
- Solution Design 与 Executor 的确定性评估规则在 Executor 保留一条 canonical 规则。
- Profile 依赖闭包定义节点深度前置条件；Planner 依赖定义任务就绪、DAG 和排程。二者职责不同，不错误删除其中之一。
- Completion Criteria 在 Kernel 完整保存；节点和 expected 文件引用。Qualification 自身的节点完成条件保留。
- 数据字段、枚举与相关数据约束从正文搬到 YAML。原文是结构示意，不转成 JSON Schema，不补字段或默认值。
- Lifecycle 的统一标题只组织原文；原文没有固定步骤、输入或输出格式的地方明确不新增规定。
- 只有 Plan Preview 有稳定格式，因此不创建 product-context-snapshot.md、product-definition-scope.md、retrospective.md 空模板；规则仍在对应节点。
- 不新增生命周期节点、Agent、Manager、Service、AOCI、RAG、向量库或知识图谱能力。

## 尚未解决的源文语义问题（本次不修正）

1. 6.7 将 Evaluation Design 能力设为至少 MINIMAL，但只有 NodeProfile 的 depth 明确定义 MINIMAL，没有能力级深度对象；保留表述，不添加 schema。
2. 8.8 使用 Planning Gate 标题，而 13 只允许三个顶层 Gate。保留前者为规划局部检查，未新增第四个顶层 Gate；后续可单独确认是否改名。
3. 2 与 3 中“固定节点 / 仅有 Runtime”保留原文条件例外；本次未触发例外，也未扩展模型。
4. 原文 Execution Profile 只提供 NodeProfile，没有聚合对象字段；不虚构 ExecutionProfile 数据结构。

## 验证方法与边界

- 迁移清单逐一记录 533 条源文非空、非标题/分隔符行的指纹与 canonical 文件；一条等价去重有显式映射。这是内容保留证据，不是语义等价的形式化证明。
- 原 YAML 对象解析后与迁移基线比较，检查字段、枚举、空值和嵌套结构未变。
- 静态检查内部链接及锚点、Kernel frontmatter、八节点顺序、六 Runtime 能力和八组 case/expected。
- 行为回归只有清晰用例与预期；未接入模型自动执行框架，不把静态通过称为八个行为用例通过。
- 人工核对主流程、路由、guardrails、去重位置与用例预期。正式验证结果见本次交付说明。

## 本次修改文件

共 45 个文件；旧占位目录未修改。

- AGENTS.md
- README.md
- docs/architecture.md
- docs/decisions/001-modularize-ai-product-development.md
- examples/ai-product-development/.gitkeep
- skills/ai-product-development/SKILL.md
- skills/ai-product-development/references/lifecycle/01-qualification.md
- skills/ai-product-development/references/lifecycle/02-cognition.md
- skills/ai-product-development/references/lifecycle/03-product-definition.md
- skills/ai-product-development/references/lifecycle/04-solution-design.md
- skills/ai-product-development/references/lifecycle/05-implementation.md
- skills/ai-product-development/references/lifecycle/06-validation-iteration.md
- skills/ai-product-development/references/lifecycle/07-release-operation.md
- skills/ai-product-development/references/lifecycle/08-retrospective.md
- skills/ai-product-development/references/runtime/context.md
- skills/ai-product-development/references/runtime/execution-profile.md
- skills/ai-product-development/references/runtime/executor.md
- skills/ai-product-development/references/runtime/gates.md
- skills/ai-product-development/references/runtime/planner.md
- skills/ai-product-development/references/runtime/registry-versioning.md
- skills/ai-product-development/references/runtime/replan-recovery.md
- skills/ai-product-development/schemas/context-pack.yaml
- skills/ai-product-development/schemas/execution-profile.yaml
- skills/ai-product-development/schemas/plan.yaml
- skills/ai-product-development/schemas/project-state.yaml
- skills/ai-product-development/schemas/task.yaml
- skills/ai-product-development/templates/execution-plan.md
- tests/ai-product-development/cases/01-greenfield-prototype.md
- tests/ai-product-development/cases/02-existing-repository-modification.md
- tests/ai-product-development/cases/03-partial-assignment.md
- tests/ai-product-development/cases/04-rag-evaluation-only.md
- tests/ai-product-development/cases/05-agent-not-required.md
- tests/ai-product-development/cases/06-enterprise-release.md
- tests/ai-product-development/cases/07-requirement-change-replan.md
- tests/ai-product-development/cases/08-existing-reusable-assets.md
- tests/ai-product-development/expected/01-greenfield-prototype.md
- tests/ai-product-development/expected/02-existing-repository-modification.md
- tests/ai-product-development/expected/03-partial-assignment.md
- tests/ai-product-development/expected/04-rag-evaluation-only.md
- tests/ai-product-development/expected/05-agent-not-required.md
- tests/ai-product-development/expected/06-enterprise-release.md
- tests/ai-product-development/expected/07-requirement-change-replan.md
- tests/ai-product-development/expected/08-existing-reusable-assets.md
- tests/ai-product-development/migration-manifest.json
- tests/ai-product-development/validate_structure.py
