# AI-Manager-SOP 使用说明书

AI-Manager-SOP 是一套可安装到 Codex 的 AI 产品开发 Skill。它根据交付目标、当前委托范围、已有资产、依赖和风险，帮助用户从需求判断持续推进到产品定义、方案、实现、验证、发布和复盘。

正式 Skill 入口：[AI Product Development](skills/ai-product-development/SKILL.md)。

## 1. 它适合解决什么问题

适合：

- 从想法开始建设 Prototype、可运行 Demo、MVP 或 Enterprise 产品；
- 接手已有产品或代码仓库，完成局部分析、设计、实现或验证；
- 只负责某个环节，例如 PRD、AI 方案、评估设计、版本验证或发布准备；
- 在本地产品仓库中保存计划和产物状态，跨任务、跨会话持续推进。

它不会默认执行完整八节点，也不会默认引入 Agent、RAG、向量数据库、长期记忆、异步队列或企业级基础设施。交付目标、依赖和风险不要求这些能力时，Skill 应选择更简单的方案。

当前成熟度：本地单用户持续交付 Beta。多人实时协作、云端状态、组织级组合管理、财务模型、法务采购和自动生产发布不属于默认范围；项目明确需要时，可作为具体任务处理。

## 2. 安装

### 推荐：让 Codex 安装

在 Codex 中调用 `$skill-installer`，并发送：

```text
请从 https://github.com/32631999wzc-create/AI-Manager-SOP/tree/main/skills/ai-product-development 安装这个 Skill。
```

安装完成后，在新任务或下一轮对话中调用 `$ai-product-development`。

### 手动安装

将仓库中的 `skills/ai-product-development/` 完整复制到：

```text
$CODEX_HOME/skills/ai-product-development/
```

未设置 `CODEX_HOME` 时，默认位置通常是：

```text
~/.codex/skills/ai-product-development/
```

必须复制整个目录，保留 `SKILL.md`、`references/`、`schemas/`、`templates/` 和 `scripts/` 的相对位置。

## 3. 五分钟开始使用

最小调用只需要说明想做什么：

```text
$ai-product-development
我想做一个帮助销售整理客户访谈的 AI 产品。请先判断合理的交付目标和范围，再给出第一阶段计划。
```

如果你已经知道目标，直接提供，Skill 不应重复提问：

```text
$ai-product-development
交付目标：MVP
目标用户：20 人以内的销售团队
核心问题：访谈记录无法快速归纳为机会和风险
现有材料：访谈样例、现有 CRM API 文档
本次范围：从产品定义做到可运行内测版本
请在当前仓库持续执行，并在关键节点保存状态。
```

建议一次提供以下信息中已经确定的部分，不需要填写完整问卷：

- 想解决的问题和目标用户；
- 期望交付物或交付目标；
- 本次负责的范围；
- 已有文档、数据、原型、代码或接口；
- 时间、成本、隐私、安全、发布等硬约束；
- 已知验收标准。

缺失信息会被分为阻塞项、非阻塞项或可显式声明的假设。Skill 只应询问会改变方案或阻塞执行的问题。

## 4. 选择使用方式

### 单次任务

适合 PRD 审阅、方案设计、评估计划、局部实现或验证。说明当前委托范围即可，Skill 不创建长期状态目录。

```text
$ai-product-development
只审阅现有 AI 搜索方案的评估设计，不修改代码、不发布。输出缺口、风险和可执行的验收标准。
```

### 持续建设一个产品

当工作会跨多个任务或会话时，明确要求在当前产品仓库持续执行。Skill 会在产品仓库创建 `.ai-product/`，保存已验证的 Profile、Plan、Registry、Snapshot 和当前任务上下文。

```text
$ai-product-development
在当前仓库启动一个持续产品项目。先检查已有材料，生成 Profile 和 Plan；验证通过后初始化本地状态，并继续执行第一个 READY Task。
```

新会话继续时：

```text
$ai-product-development
恢复当前仓库中的产品项目，检查最新 Snapshot 和阻塞项，然后继续下一个 READY Task。
```

需求变化时：

```text
$ai-product-development
目标和范围不变，但外部 API 字段已经变化。请做 Local Replan，保留仍有效的工作，只重做受影响任务。
```

`.ai-product/` 是显式项目状态，不是聊天记忆。普通用户无需直接调用 Runtime CLI；命令参考见 [Continuous Project Runtime](skills/ai-product-development/scripts/project_runtime/README.md)。

## 5. 八节点工作流

Execution Profile 会为全部八节点记录范围角色、执行深度、资产状态和状态，但只加载当前任务需要的详细规则。

| 节点 | 解决的问题 | 主要输出 | 节点完成的核心判断 |
|---|---|---|---|
| Qualification | 目标、范围和材料是否足以开始 | Context Snapshot、Profile、Gate、假设/阻塞项 | 能可靠规划，或明确阻塞 |
| Cognition | 现有产品、流程、资产和实现是什么 | Current State、Asset Inventory、必要的 System Map | 受影响范围和关键依赖已理解 |
| Product Definition & Scope | 为谁解决什么问题，AI 边界和成功是什么 | 产品定义、范围/非目标、价值假设、成功指标 | 已足以支持方案决策和验证 |
| Solution Design | 用什么产品/AI 流程可靠实现 | Solution Design、Evaluation Design、Build Readiness | 方案可构建且验收方法明确 |
| Implementation | 如何交付最小可靠增量 | 可运行或可审阅增量、Task Result、验证证据 | 当前任务验收通过且未越界 |
| Validation & Iteration | 当前版本是否达到标准 | 结论、证据、bad cases、根因和修复结果 | 证据覆盖标准，结论不过度外推 |
| Release & Operation | 如何让目标用户安全使用 | Release Readiness、版本/环境、发布验证与观察项 | 已可用，或发布被明确阻塞 |
| Retrospective | 哪些经验和资产值得复用 | 结果复盘、学习、债务、复用资产和后续行动 | 只保留有证据且会改变决策的经验 |

详细节点合同位于 [lifecycle references](skills/ai-product-development/references/lifecycle/)。每个节点统一包含 Purpose、Activation Conditions、Required Inputs、Capabilities、Procedure、Outputs、Completion Criteria、Dependencies、Load With 和 Do Not。

## 6. 执行时会发生什么

1. **Qualification**：确认交付目标、Assignment Scope、已有材料和阻塞项。
2. **Profile**：计算八节点的深度，不把节点清单机械变成任务。
3. **Planner**：从真实缺口生成 Task DAG，检查依赖、冲突和 Gate。
4. **Context + Executor**：为 READY Task 加载最小上下文，执行并验证。
5. **Registry**：只有经过确认或验证的事实、决策和正式产物才写入长期状态。
6. **Replan**：输入、产物、决策、任务或范围变化时，只调整受影响工作。
7. **Completion**：交付物、必要节点、验收标准、阻塞项和正式产物同时满足才完成。

用户通常只会看到初始/重大变更计划、重要发现、阻塞问题、关键决策和最终交付摘要，不需要阅读内部 DAG 或 Registry。

## 7. 如何写出高质量请求

明确结果和边界比指定内部流程更有效：

```text
交付目标：Runnable Demo
本次范围：产品定义、方案、实现和离线验证
已有资产：5 份访谈记录、一个空仓库
必须满足：中文输入；结果可追溯到原始反馈 ID；不调用外部服务
完成标准：样例可运行，输出 JSON 和 Markdown，测试通过
```

局部任务要明确不做什么：

```text
只验证当前版本，不修复、不发布；三个固定样例全部匹配才通过，不宣称泛化。
```

重大变更要说明哪些保持不变：

```text
目标用户、交付目标和验收标准不变；只替换数据源。保留已验证设计，评估受影响任务并局部重规划。
```

## 8. 结果与状态如何判断

顶层只有三个 Gate：

- Qualification：能否开始可靠规划；
- Build Readiness：范围、方案和验收标准是否足以开始实现；
- Release Readiness：当前结果是否达到发布目标。

最终完成还要求：请求的交付物完成、所有 REQUIRED 节点满足、验收标准通过、没有阻塞项、必需正式产物为 ACTIVE，并明确范围外但项目关键的要求。

## 9. 常见问题

**为什么没有自动跑完八个节点？**
Execution Profile 会根据当前委托、已有资产和交付目标选择深度。SKIP、VERIFY 或零任务都可能是正确结果。

**为什么 Skill 又读取了一个支持模块？**
依赖闭包可能要求核对 Profile、Gate、Planner 或 Registry。少量有理由的支持读取是允许的；无任务依赖地批量读取全部 references 才是 eager loading。

**为什么没有创建 `.ai-product/`？**
单次任务不需要持久状态。只有明确存在跨任务或跨会话连续性时才创建。

**为什么不能直接把草稿写入 Registry？**
假设、草稿和失败输出不能成为长期事实；正式产物必须先通过验证并创建版本。

**如何确认安装没有损坏？**
检查 Skill 目录结构完整，并运行本文下一节的结构验证。若只是使用 Skill，无需运行开发者 trace 测试。

## 10. 仓库维护与验证

运行环境需要 Python 3.10+ 和 PyYAML。在仓库根目录执行：

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase*.py"
python -B -X utf8 tests/ai-product-development/routing/verify_evidence.py
python -B -X utf8 tests/ai-product-development/phase2/behavior/verify_behavior.py
python -B -X utf8 tests/ai-product-development/phase3/golden/verify_golden.py
```

结构验证覆盖路由、节点合同、内部链接、Gate、schema、迁移完整性和明显规则重复。真实行为证据见 [Routing 报告](tests/ai-product-development/routing/report.md)、[Phase 2 行为报告](tests/ai-product-development/phase2/behavior/report.md)和 [Phase 3 Golden 报告](tests/ai-product-development/phase3/golden/report.md)。

仓库结构和 canonical location 见 [架构说明](docs/architecture.md)；本次完整性审查见 [工作流合同审查](docs/decisions/005-workflow-contract-review.md)。
