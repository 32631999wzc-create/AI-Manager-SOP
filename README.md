<p align="center">
  <img src="docs/assets/ai-product-copilot.png" alt="AI Product Copilot" width="100%">
</p>

<p align="center">
  <a href="https://github.com/32631999wzc-create/AI-Manager-SOP/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/32631999wzc-create/AI-Manager-SOP?display_name=tag&amp;sort=semver"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/32631999wzc-create/AI-Manager-SOP"></a>
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827?logo=openai&amp;logoColor=white">
  <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&amp;logoColor=white">
  <img alt="Workflow: Human Reviewed" src="https://img.shields.io/badge/Workflow-Human%20Reviewed-F59E0B">
</p>

AI Product Copilot 是一套可安装到 Codex 的 AI 产品开发 Skill。它根据交付目标、委托范围、已有资产、依赖、证据和风险，为真实产品任务生成执行路径，并持续推进产品定义、方案设计、实现、验证、发布和生产学习。

当前版本：**AI Product Development Skill v1 — 可在人工审核下用于真实任务。**

- Skill 入口：[AI Product Development](skills/ai-product-development/SKILL.md)
- 使用边界：[Usage Boundary](docs/usage-boundary.md)
- 架构说明：[Architecture](docs/architecture.md)
- 最新版本：[Releases](https://github.com/32631999wzc-create/AI-Manager-SOP/releases)

## 核心能力

AI Product Copilot 可以处理以下工作：

- 从模糊想法建立产品定义、范围、成功指标和可执行计划；
- 接手已有 PRD、代码、原型、数据或评测资产，先核验有效性，再复用有效内容；
- 自动起草和修订跨行业 PRD，维持问题、需求、验收和收益之间的可追溯关系；
- 评估 AI 可行性、数据条件、Human-AI 交互、评测方案和 Responsible AI 风险；
- 将产品缺口转换为带依赖、验收标准、交付物和 Gate 的 Task DAG；
- 在每个已确定的任务节点完成后展示结果，等待人工审核；
- 根据审核意见、最新文件和新证据调整后续计划；
- 在需求、范围、外部接口或生产证据变化时，只重算受影响范围；
- 为持续项目保存 Profile、Plan、Registry、Snapshot 和人工审核状态；
- 将生产 bad case 连接到证据、决策、最小修复、回归验证和重新发布。

系统根据任务目标选择所需能力和工程深度。简单任务会形成短链路；高风险、生产级或跨团队任务会增加相应的证据、验证和 Gate。

## 安装

### 使用 Codex 安装

在 Codex 中调用 `$skill-installer`，并发送：

```text
请从 https://github.com/32631999wzc-create/AI-Manager-SOP/tree/main/skills/ai-product-development 安装这个 Skill。
```

安装完成后，在新任务中调用 `$ai-product-development`。

### 手动安装

将 `skills/ai-product-development/` 完整复制到：

```text
$CODEX_HOME/skills/ai-product-development/
```

默认目录通常为：

```text
~/.codex/skills/ai-product-development/
```

请保留 `SKILL.md`、`references/`、`schemas/`、`templates/` 和 `scripts/` 的相对位置。

## 快速开始

### 从一个产品想法开始

```text
$ai-product-development
我想做一个帮助销售整理客户访谈的 AI 产品。
请判断合理的交付目标和范围，列出关键未知项，并生成第一阶段计划。
```

### 直接提供明确目标

```text
$ai-product-development
交付目标：MVP
目标用户：20 人以内的销售团队
核心问题：访谈记录难以快速归纳为机会和风险
现有材料：访谈样例、CRM API 文档
本次范围：从产品定义做到可运行内测版本
请在当前仓库持续执行，并在每个关键文档和任务节点完成后等待人工审核。
```

### 修改已有产品

```text
$ai-product-development
读取当前仓库的 PRD、代码和评测资产。
识别本次需求影响的范围，复用仍有效的内容，输出修改方案和最小必要验证。
```

### 处理生产问题

```text
$ai-product-development
根据这批生产 bad cases 判断受影响的产品决策和任务。
保存证据，执行最小 Replan，并给出修复、回归和重新发布条件。
```

提供以下信息可以减少确认轮次：

- 用户、场景和待解决问题；
- 目标交付物或交付深度；
- 本次委托范围；
- 已有文档、数据、原型、代码、接口和评测；
- 时间、成本、隐私、安全和发布约束；
- 已知验收标准与决策人。

系统会把缺失信息分类为阻塞项、可补充证据和显式假设，并优先询问会改变方案或阻塞执行的问题。

## 工作方式

### 单次任务

单次任务适合 PRD 起草或审阅、竞品分析、AI 方案、评测计划、需求评审和局部验证。系统根据当前请求完成交付，并将关键假设和证据边界写入结果。

```text
$ai-product-development
审阅现有 AI 搜索方案的评测设计。
输出证据缺口、主要风险和可执行验收标准，保持代码与发布状态不变。
```

### 持续产品项目

跨任务或跨会话的产品建设会在产品仓库中使用 `.ai-product/` 保存状态：

```text
$ai-product-development
在当前仓库启动持续产品项目。
检查已有材料，生成 Execution Profile 和 Plan；人工审核通过后初始化状态并执行第一个 READY Task。
```

后续会话可以直接恢复：

```text
$ai-product-development
恢复当前仓库中的产品项目，读取最新 Snapshot、人工审核记录和阻塞项，继续下一个 READY Task。
```

`.ai-product/` 保存显式项目状态。Runtime 使用文件指纹、审核回执和验证结果维护跨会话连续性。命令参考见 [Continuous Project Runtime](skills/ai-product-development/scripts/project_runtime/README.md)。

## 八节点生命周期

Execution Profile 始终记录八个生命周期节点，并为每个节点计算 `SKIP / VERIFY / LIGHT / STANDARD / DEEP` 深度。Planner 根据真实缺口生成任务，因此一次任务可以只执行其中一部分节点。

| 节点 | 主要判断 | 典型输出 |
|---|---|---|
| Qualification | 目标、范围、证据和约束是否足以规划 | Context Snapshot、Execution Profile、Gate、阻塞项 |
| Cognition | 现有产品、流程、资产和依赖如何工作 | Current State、Asset Inventory、System Map |
| Product Definition & Scope | 为谁解决什么问题，价值和边界如何定义 | 产品定义、范围、成功指标、PRD |
| Solution Design | 产品与 AI 工作流如何达到目标 | Solution Design、Evaluation Design、Build Readiness |
| Implementation | 如何交付最小可靠增量 | 可运行或可审阅增量、Task Result、验证证据 |
| Validation & Iteration | 当前结果是否达到验收标准 | Eval Readout、bad cases、根因、回归结果 |
| Release & Operation | 如何安全地交付给目标用户 | Release Readiness、发布计划、观测与回滚条件 |
| Retrospective | 哪些经验和资产可以进入下一轮 | 复盘、学习、技术债、复用资产、后续行动 |

详细合同位于 [Lifecycle References](skills/ai-product-development/references/lifecycle/)。

## 16 个专业能力域

Planner 使用“明确缺口 + 待解锁决策 + 当前证据状态”选择能力，并决定执行方式：

- `EXECUTE`：当前缺口缺少可用证据；
- `VERIFY`：已有资产需要核验；
- `REUSE`：已有证据仍然有效；
- 无缺口：保持未激活。

| 产品与市场 | AI 与体验 | 交付与学习 |
|---|---|---|
| Discovery | AI Feasibility | Delivery |
| Competitive Intelligence | Data Strategy | Launch |
| Business Case | Human-AI Experience | Production Learning |
| Roadmap | Evaluation | Retrospective |
| Product Requirements | Responsible AI |  |
| Requirement Review | Experimentation |  |

专业方法、模板和示例位于 [Capability References](skills/ai-product-development/references/capabilities/)，并在任务需要时按需加载。

## 决策、证据与人工审核

系统为重要产品结论维护三个问题：

1. 为什么作出这个决定？
2. 使用了哪些证据？
3. 什么变化会触发重新判断？

每个已确定的 Task 完成并验证后，系统会：

1. 展示交付物、验证结果、证据和未决项；
2. 暂停当前执行；
3. 等待人工批准、驳回或修改建议；
4. 重新读取人工可能修改过的文件；
5. 以最新内容更新任务路径和后续交付。

PRD、产品范围、关键方案、Build Readiness、Release Readiness 和高风险决策均进入人工审核。证据达到合同要求后可提交审核；关键输入缺失、高影响风险未关闭或验收条件不可执行时，任务保持阻塞。

顶层 Gate 包含：

- **Qualification**：当前信息是否足以形成可靠计划；
- **Build Readiness**：范围、方案、依赖和验收是否足以进入实现；
- **Release Readiness**：结果、风险、运营条件和回滚准备是否支持发布。

## 变更与 Replan

已有 baseline 后，系统会评估新事件的影响：

- 信息更新且未产生实质影响：继续当前计划；
- 局部任务、依赖或资产变化：执行 Local Replan；
- 目标、范围或主要约束变化：执行 Profile Replan；
- 新产品项目：建立 Initial Plan。

Replan 先识别仍有效的证据、决策和产物，再生成受影响节点与任务的调整计划，并将结果提交人工审核。生产证据可以重新打开已有决策，并触发对应的修复与回归链路。

## 项目结构

```text
skills/ai-product-development/
├── SKILL.md                 # Kernel 与 Router
├── references/
│   ├── lifecycle/           # 八节点合同
│   ├── capabilities/        # 16 个专业能力域
│   └── runtime/             # Profile、Planner、Gate、Executor、Registry
├── schemas/                 # Profile、Plan、Task、Evidence、Decision 等对象
├── templates/               # 可复用交付模板
└── scripts/                 # 只读验证器与持续项目 Runtime
```

架构、canonical location 和依赖关系见 [架构说明](docs/architecture.md)。能力触发、重叠治理和退役规则见 [Capability 资产治理](docs/capability-governance.md)。

## 成熟度与使用边界

v1 已覆盖本地单用户的持续产品交付，并通过结构、Routing、Phase 2 行为、Phase 3 continuous runtime 和代表性真实任务验证。当前执行模式以人工审核为 Gate，重要决策由指定 owner 放行。

以下场景需要项目团队提供额外 owner、系统或流程：

- 多人实时协作与云端状态同步；
- 组织级项目组合和财务审批；
- 法务、采购与正式合规签署；
- 生产环境凭证、发布权限和事故指挥；
- 高影响领域的专业责任判断。

完整边界与 LIGHT/实验性能力见 [Usage Boundary](docs/usage-boundary.md)。

## 仓库验证

维护环境需要 Python 3.10+ 和 PyYAML。在仓库根目录运行：

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase*.py"
python -B -X utf8 tests/ai-product-development/routing/verify_evidence.py
python -B -X utf8 tests/ai-product-development/phase2/behavior/verify_behavior.py
python -B -X utf8 tests/ai-product-development/phase3/golden/verify_golden.py
```

这些检查覆盖目录结构、路由、对象合同、Gate、schema、validator、行为证据和持续状态。采用的 v1 证据清单见 [Release v1 Manifest](docs/release-v1-manifest.yaml)，发布判断见 [Final Readiness Review](docs/final-readiness-review-v1.md)。

## License

[MIT](LICENSE)
