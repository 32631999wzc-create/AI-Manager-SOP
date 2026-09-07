# Phase 1 验证报告

验证日期：2026-09-07（Asia/Shanghai）。范围仅为 Modularization 与 Progressive Disclosure。

## 最终结论

R1、R2、R3 均为 **PASS**。依据是各自独立 Codex 会话的实际成功文件读取命令及完整输出，不依据模型最终自述。受测进程使用 read-only 沙箱和独立临时 Skill 副本；均正常退出，副本前后哈希不变。没有必要模块漏读、无依据的批量详细规则读取或未审阅 WARN。

结构检查保持八个 lifecycle node、六项 runtime capability、三个顶层 Gate、八个原 YAML 对象和 533 条源规则；完整映射包含 70 个原始标题。枚举及对象字段与原始基线一致。Kernel 238 行，详细规则保留 canonical location。明显详细规则重复扫描通过，并人工审阅全部八个 lifecycle 和七个 runtime 文件。迁移指纹是内容保留证据，不是任意语义变更的形式化证明。

## 原始尝试与修正

- 环境探测曾因默认 Windows 沙箱配置导致读取失败；未计入成功测试。保持 read-only，显式指定现有 elevated 沙箱后成功读取；未使用可写权限、ignore-rules 或绕过审批方式解决测试。
- 首次 R1 为 PASS，首次 R2 为 WARN，首次 R3 为 FAIL。清洗后只保留最终验收采用的三组 PASS trace；首轮问题与修复依据保留如下。
- R2 无必要漏读，但机械展开了四个 VERIFY 节点，其中 Cognition、Product Definition 两项额外读取缺乏当前核验需要。没有批量读取全部详情，按规范为 WARN。没有把该 WARN 直接转为 PASS；Kernel 明确已确认可复用资料不自动触发逐节点读取，随后独立重测。
- R3 漏读 Registry，无法用最终回答弥补。Kernel 的 Registry 路由补充正式产物状态判断；Replan 增加到 Planner、Registry 和条件性 Profile 的导航。只明确既有规则的加载依赖，没有新增业务规则。
- Kernel 另一处摘要“不得修改正式状态”宽于原文，改为引用 Executor 原始具体操作边界，避免新增限制。

以下读取顺序直接来自 command_execution 事件；模型自述中的列举顺序不作为顺序证据。每个文件均为单文件完整读取，exit_code=0、status=completed。路径相对 Skill。

## R1 — Greenfield Prototype Qualification 与 Profile：PASS

活动任务：为一个面向个人的 AI 食谱卡片概念做初始 Qualification 和 Execution Profile。交付目标已确认 PROTOTYPE；只做概念和交互，AI 和数据均可 mock。无现有仓库、无真实用户、无外部 API、无登录、无持久化、无上线、安全敏感数据或高风险决策。当前委托仅为初始资格判断和八节点 Profile，不设计界面、不生成实现任务、不执行后续节点。输出 Qualification Gate 结果和八节点的 scope_role、activation、depth、asset_status、原因与依赖检查。

必要模块：`SKILL.md`、`references/lifecycle/01-qualification.md`、`references/runtime/execution-profile.md`、`references/runtime/gates.md`、`schemas/execution-profile.yaml`。

| 实际顺序 | 文件 | trace item |
|---|---|---|
| 1 | `SKILL.md` | `item_2` |
| 2 | `templates/execution-plan.md` | `item_3` |
| 3 | `references/runtime/execution-profile.md` | `item_4` |
| 4 | `references/runtime/gates.md` | `item_5` |
| 5 | `references/lifecycle/01-qualification.md` | `item_6` |
| 6 | `schemas/execution-profile.yaml` | `item_7` |

必要模块漏读：无。

额外读取及依据：

- `templates/execution-plan.md`：Kernel 初始计划沟通格式。

Dependency closure：只制定 Profile；不存在实现或验证执行，不能把八节点 Profile 误解为加载八节点详细规则。

人工审阅：所有命令均为任务相关的逐文件读取，无目录批量扫描。支持读取有具体依据，没有不必要的全量 lifecycle/runtime 加载。

证据：[原始 trace](evidence/R1-final/trace.jsonl)、[判定明细](evidence/R1-final/result.json)、[隔离和版本元数据](evidence/R1-final/metadata.json)。

## R2 — 已有系统 Validation Only：PASS

活动任务：对已有内部 AI 文本分类 DEMO 做一次 Validation Only。Qualification 已确认 PASS，范围和目标不变；本轮只核对给定结果并给出结论，不改代码、不修复、不发布、不写正式记录。已验证可复用的系统与验收设计：规则标签仅 A/B；三个固定样例全部精确匹配期望即通过；输入1/2/3的期望分别为 A/B/A，实际分别为 A/B/A；测试覆盖只限这三个样例，不宣称泛化。已确认 Profile：Qualification VERIFY，Cognition VERIFY，Product Definition & Scope VERIFY，Solution Design VERIFY，Validation & Iteration REQUIRED，其余 SKIP；不存在敏感数据或新增依赖。请按 Skill 核验，说明通过范围和限制。

必要模块：`SKILL.md`、`references/lifecycle/06-validation-iteration.md`、`references/runtime/executor.md`。

| 实际顺序 | 文件 | trace item |
|---|---|---|
| 1 | `SKILL.md` | `item_2` |
| 2 | `references/runtime/executor.md` | `item_3` |
| 3 | `references/lifecycle/06-validation-iteration.md` | `item_4` |

必要模块漏读：无。

额外读取：无。

Dependency closure：已有验收标准且不修改仓库，不触发缺少验收标准的 Solution Design 补建或代码修改的 Cognition。局部确认这些规则允许。

人工审阅：所有命令均为任务相关的逐文件读取，无目录批量扫描。支持读取有具体依据，没有不必要的全量 lifecycle/runtime 加载。

证据：[原始 trace](evidence/R2-final/trace.jsonl)、[判定明细](evidence/R2-final/result.json)、[隔离和版本元数据](evidence/R2-final/metadata.json)。

## R3 — 目标和范围不变的 Local Replan：PASS

活动任务：对既有 AI DEMO 的计划做 Local Replan 建议，仅在回答中输出，不执行代码、不写记录或状态。Qualification 已 PASS；交付目标、范围、主要约束和验收标准均不变。已完成并验证的 T1（范围）和 T2（设计）及其正式产物 v1 仍有效。T3（工具适配）因外部 API 契约字段变更而失败，确认不能直接重试；其适配产物 v1 失效。T4（依赖 T3 适配产物的集成验证）未开始，T5（与 T3 无依赖的演示说明）已完成且有效。现需加入一项独立契约修正任务，再产生新适配产物并验证；不得重做 T1/T2/T5。请给出局部影响、PRESERVE/OUTDATE/ADD/CANCEL 建议、新任务依赖、是否需要新计划版本，以及与 Profile Replan 的区别；不用重新生成八节点 Profile。

必要模块：`SKILL.md`、`references/runtime/replan-recovery.md`、`references/runtime/planner.md`、`references/runtime/registry-versioning.md`。

| 实际顺序 | 文件 | trace item |
|---|---|---|
| 1 | `SKILL.md` | `item_2` |
| 2 | `references/runtime/replan-recovery.md` | `item_3` |
| 3 | `references/runtime/planner.md` | `item_4` |
| 4 | `references/runtime/registry-versioning.md` | `item_5` |
| 5 | `schemas/task.yaml` | `item_6` |
| 6 | `schemas/plan.yaml` | `item_7` |
| 7 | `schemas/project-state.yaml` | `item_8` |

必要模块漏读：无。

额外读取及依据：

- `schemas/plan.yaml`：核对计划版本和依赖字段。
- `schemas/project-state.yaml`：核对受影响产物状态和版本。
- `schemas/task.yaml`：核对任务状态。

Dependency closure：DAG 新增独立契约修正任务，触发新计划版本；不触发交付目标或范围变化的 Profile Replan。Registry 用于失效及版本建议，不授权提交。

人工审阅：所有命令均为任务相关的逐文件读取，无目录批量扫描。支持读取有具体依据，没有不必要的全量 lifecycle/runtime 加载。

证据：[原始 trace](evidence/R3-final/trace.jsonl)、[判定明细](evidence/R3-final/result.json)、[隔离和版本元数据](evidence/R3-final/metadata.json)。

## 检查命令与边界

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py
python -B -X utf8 tests/ai-product-development/validate_structure.py --source /path/to/original/SKILL.md
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p test_phase1.py
python -B -X utf8 tests/ai-product-development/routing/verify_evidence.py
```

另运行 skill-creator 的 quick_validate.py 检查技能元数据。原始源文件没有复制回仓库；逐条迁移表及对象指纹保持原基线。

证据索引 [accepted-runs.json](accepted-runs.json) 固定五类证据文件的哈希；回放检查当前 Skill 文件哈希、实际命令输出、独立会话/工作目录和保存判定一致性。回放不会调用模型。原始 stdout 保留 HTTPS 回退诊断；模型读取成功，传输回退没有被计作读取失败或路由失败。

这三个场景只证明本版本在本次有限任务中的路由行为，不保证所有任务或模型版本。没有创建 `.ai-product/`、没有实现 init/save/resume、状态 Runtime、Python domain models、完整行为回归或反馈整理助手。八个人工 case/expected 仍未执行；Phase 2 和 Phase 3 均未开始。
