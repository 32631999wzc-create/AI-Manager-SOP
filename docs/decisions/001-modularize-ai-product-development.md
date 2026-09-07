# AI Product Development 结构性模块化重构

## 决策与来源

按 Preserve semantics → Split by responsibility → Add routing → Remove duplication → Validate 执行。来源为用户提供的完整 SKILL.md，共 945 行，SHA-256：0db07435d169006990aeeabdecbb4b9f09210a00390a76d78ffb516e0ca18ace。

该完整源文件此前未存在于 Git 历史，仓库只有 ai-product-sop 占位文件。本次将外部源文模块化导入 ai-product-development，首次导入时保留历史占位目录（随后由远程提交 592d974 删除，本次接受该删除），不将目录占位误报为被重构的完整旧版本。源文未重复提交，指纹与逐行归属保存在 [迁移清单](../../tests/ai-product-development/migration-manifest.json)。

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

## 首次导入修改文件（3d0332f）

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

## Phase 1 补充审计

八个 lifecycle 与七个 runtime 职责文件已逐一审阅。原有效规则继续以 533 条迁移指纹及八个 YAML 对象基线核验；不改变原文条件例外、枚举和 Gate。Kernel 原摘要“不得修改正式状态”比源文更宽，改为链接 Executor 的具体操作边界，避免误禁止正常任务状态迁移。详细规则仍以原 canonical 文件为准。

重复扫描排除标题、导航链接及短组织性占位说明，检查长规则行和多行详细段落。相似但职责不同的 Profile 节点依赖与 Planner 任务依赖仍保留。重复检测不是语义证明；未添加新方法论、状态系统或执行服务。

### 全部源标题逐项映射

以下包含每个原始标题；父章节列出其子章节涉及的位置，逐条规则归属以迁移清单为准。机器可核验版本见 [section-migration.json](../../tests/ai-product-development/section-migration.json)。行号来自固定 945 行源文，不依赖用户下载路径。

| 源行 | 旧 Section / 标题 | 新 canonical location（相对 Skill） |
|---|---|---|
| 6 | AI Product Development | `SKILL.md` |
| 12 | 1. Operating Principles | `SKILL.md` |
| 27 | 2. Lifecycle | `SKILL.md` |
| 42 | 3. Runtime | `SKILL.md` |
| 55 | 4. Core Data | `SKILL.md`<br>`schemas/project-state.yaml`<br>`schemas/task.yaml` |
| 59 | Task | `schemas/task.yaml` |
| 85 | Project Record | `schemas/project-state.yaml` |
| 103 | Artifact | `schemas/project-state.yaml` |
| 123 | Runtime Snapshot (optional) | `schemas/project-state.yaml` |
| 140 | 5. Qualification | `references/lifecycle/01-qualification.md`<br>`references/runtime/execution-profile.md`<br>`references/runtime/gates.md`<br>`schemas/execution-profile.yaml` |
| 144 | 5.0 Initial Response Protocol | `references/lifecycle/01-qualification.md` |
| 156 | 5.1 Determine Delivery Target | `references/runtime/execution-profile.md` |
| 178 | 5.2 Determine Assignment Scope | `references/runtime/execution-profile.md`<br>`schemas/execution-profile.yaml` |
| 193 | 5.3 Inspect Product Context | `references/lifecycle/01-qualification.md` |
| 210 | 5.4 Classify Missing Information | `references/lifecycle/01-qualification.md` |
| 222 | 5.5 Qualification Gate | `references/runtime/gates.md` |
| 234 | 6. Execution Profile | `SKILL.md`<br>`references/runtime/execution-profile.md`<br>`schemas/execution-profile.yaml` |
| 254 | 6.1 Base Profile by Delivery Target | `references/runtime/execution-profile.md` |
| 271 | 6.2 Scope Rules | `references/runtime/execution-profile.md` |
| 281 | 6.3 Existing Asset Rules | `references/runtime/execution-profile.md` |
| 302 | 6.4 Project Mode | `references/runtime/execution-profile.md` |
| 313 | 6.5 Feature Triggers | `references/runtime/execution-profile.md` |
| 329 | 6.6 Risk Floors | `references/runtime/execution-profile.md` |
| 341 | 6.7 Dependency Closure | `references/runtime/execution-profile.md` |
| 354 | 6.8 Rule Precedence | `SKILL.md` |
| 367 | 6.9 Consistency Check | `references/runtime/execution-profile.md` |
| 380 | 7. Lifecycle Node Registry | `references/lifecycle/01-qualification.md`<br>`references/lifecycle/02-cognition.md`<br>`references/lifecycle/03-product-definition.md`<br>`references/lifecycle/04-solution-design.md`<br>`references/lifecycle/05-implementation.md`<br>`references/lifecycle/06-validation-iteration.md`<br>`references/lifecycle/07-release-operation.md`<br>`references/lifecycle/08-retrospective.md`<br>`references/runtime/executor.md`<br>`references/runtime/gates.md` |
| 382 | 7.1 Qualification | `references/lifecycle/01-qualification.md` |
| 392 | 7.2 Cognition | `references/lifecycle/02-cognition.md` |
| 406 | 7.3 Product Definition & Scope | `references/lifecycle/03-product-definition.md` |
| 416 | 7.4 Solution Design | `references/lifecycle/04-solution-design.md`<br>`references/runtime/executor.md`<br>`references/runtime/gates.md` |
| 422 | Solution Architecture capabilities | `references/lifecycle/04-solution-design.md` |
| 433 | Evaluation Design capabilities | `references/lifecycle/04-solution-design.md`<br>`references/runtime/executor.md`<br>`references/runtime/gates.md` |
| 448 | 7.5 Implementation | `references/lifecycle/05-implementation.md` |
| 456 | 7.6 Validation & Iteration | `references/lifecycle/06-validation-iteration.md` |
| 478 | 7.7 Release & Operation | `references/lifecycle/07-release-operation.md` |
| 491 | 7.8 Retrospective | `references/lifecycle/08-retrospective.md` |
| 501 | 8. Planner | `references/runtime/planner.md`<br>`schemas/plan.yaml` |
| 519 | 8.1 Plan Before Execute | `references/runtime/planner.md` |
| 532 | 8.2 Generate Tasks from Gaps | `references/runtime/planner.md` |
| 540 | 8.3 Valid Task Rule | `references/runtime/planner.md` |
| 552 | 8.4 Split a Task When | `references/runtime/planner.md` |
| 565 | 8.5 Dependencies | `references/runtime/planner.md` |
| 578 | 8.6 Parallelism | `references/runtime/planner.md` |
| 589 | 8.7 Priority | `references/runtime/planner.md` |
| 606 | 8.8 Planning Gate | `references/runtime/planner.md` |
| 626 | 9. Context | `references/runtime/context.md`<br>`schemas/context-pack.yaml` |
| 668 | 10. Executor | `references/runtime/executor.md` |
| 672 | 10.1 Worker Types | `references/runtime/executor.md` |
| 684 | 10.2 Worker Selection | `references/runtime/executor.md` |
| 692 | 10.3 Execution | `references/runtime/executor.md` |
| 704 | 10.4 Validation | `references/runtime/executor.md` |
| 708 | Structural Validation | `references/runtime/executor.md` |
| 712 | Acceptance Validation | `references/runtime/executor.md` |
| 718 | 10.5 Failure | `references/runtime/executor.md` |
| 730 | 11. Registry and Versioning | `references/runtime/registry-versioning.md` |
| 734 | 11.1 Record Write Rules | `references/runtime/registry-versioning.md` |
| 747 | 11.2 Artifact Commit Rules | `references/runtime/registry-versioning.md` |
| 768 | 12. Replan and Recovery | `references/runtime/replan-recovery.md` |
| 776 | 12.1 Change Types | `references/runtime/replan-recovery.md` |
| 788 | 12.2 Replan Actions | `references/runtime/replan-recovery.md` |
| 799 | 12.3 Local vs Profile Replan | `references/runtime/replan-recovery.md` |
| 811 | 13. Flow Gates | `references/runtime/gates.md` |
| 815 | Qualification Gate | `references/runtime/gates.md` |
| 819 | Build Readiness | `references/runtime/gates.md` |
| 823 | Release Readiness | `references/runtime/gates.md` |
| 831 | 14. Complexity Guardrails | `SKILL.md` |
| 863 | 15. User-Facing Execution Style | `SKILL.md`<br>`templates/execution-plan.md` |
| 886 | 16. End-to-End Procedure | `SKILL.md` |
| 926 | 17. Completion Criteria | `SKILL.md` |

### Canonical 归属修正

补全逐标题映射时发现首次迁移清单用相同文本匹配归属，导致 `id`、`version`、短状态枚举、主流程节点标签等被归到其他章节的同文行。按源章节与数据对象上下文修正 18 条 canonical_file；所有 source_sha256、canonical_sha256、frontmatter 与 schema 对象指纹不变，不重新生成源基线。清洗后不再保留与 Git diff 重复的过程清单；最终完整表与逐行归属一致。

Routing Test 首轮暴露 VERIFY 机械读取和 Replan 漏读 Registry，修正仅为 Kernel 与 Replan 的加载导航；最终三组独立只读 trace 均通过。完整证据与历史 WARN/FAIL 见 [Phase 1 报告](../../tests/ai-product-development/routing/report.md)。
