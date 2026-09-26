<p align="center">
  <img src="docs/assets/ai-product-copilot.png" alt="AI Product Copilot" width="100%">
</p>

<p align="center">
  <a href="https://github.com/32631999wzc-create/AI-Manager-SOP/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/32631999wzc-create/AI-Manager-SOP?display_name=tag&amp;sort=semver"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/github/license/32631999wzc-create/AI-Manager-SOP"></a>
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827?logo=openai&amp;logoColor=white">
  <img alt="Workflow: Human Reviewed" src="https://img.shields.io/badge/Workflow-Human%20Reviewed-F59E0B">
</p>

# AI Product Copilot

## 1. 是什么，给谁用

**AI Product Copilot** 是一套可安装到 Codex 的 AI 产品开发 Skill，面向需要实际推进 AI 产品工作的：

- 产品经理与 AI 产品经理；
- 创业者与独立开发者；
- 产品负责人；
- AI 应用团队；
- 参与产品定义、方案、评测、交付和发布的跨职能团队。

它可以持续推进真实产品工作，覆盖产品定义、AI 方案、执行计划、任务交付、验证、人工审核、变更重规划、发布和生产学习。

用户只需提供当前目标和已有材料。Skill 会结合以下信息自行选择工作路径：

- 交付目标与 Assignment Scope；
- 已有 PRD、代码、原型、数据和评测资产；
- 当前证据与已作决策；
- 任务依赖；
- 风险与约束。

~~~text
产品定义
→ 产品与 AI 方案
→ 执行计划
→ Task 执行
→ Validation
→ Human Review
→ Replan
→ Release
→ Production Learning
~~~

当前版本：

> **AI Product Development Skill v1 — 可在人工审核下用于真实任务。**

重要产品决策、Build Readiness、Release Readiness 和高影响操作由人工负责人确认。

## 2. 如何用

安装后，在 Codex 中调用：

~~~text
$ai-product-development
~~~

然后描述当前要完成的产品工作。

从产品想法开始：

~~~text
$ai-product-development

我要做一个 AI 客户访谈分析产品。
目前有访谈样例和 CRM API 文档，希望推进到可内部试用的 MVP。
~~~

继续已有项目：

~~~text
$ai-product-development

读取当前仓库里的 PRD、代码和评测资产，继续推进这个产品。
~~~

处理需求变化：

~~~text
$ai-product-development

这是最新的需求变更。
检查它影响了哪些现有产品决策和任务，并继续处理。
~~~

处理生产问题：

~~~text
$ai-product-development

分析这批 production bad cases，
判断需要修复什么，并完成必要的回归和重新发布准备。
~~~

Skill 会根据上下文确定生命周期节点、Capability、Task DAG、Replan 类型和执行深度。跨任务或跨会话的项目可以在产品仓库中使用 <code>.ai-product/</code> 保存显式状态，并在后续会话继续执行。

## 3. 当前支持能力

### 产品定义与规划

- 用户与机会发现；
- 市场与竞品分析；
- Business Case 与优先级；
- Roadmap 与版本规划；
- PRD 起草、修改与审阅；
- 产品范围与成功指标；
- Requirement Review；
- Task DAG、依赖、验收标准与交付物规划。

### AI 产品设计

- AI Feasibility；
- 模型与方案选择；
- Data Strategy；
- Human-AI Experience；
- Evaluation Design；
- Dataset、Metrics、Judge Strategy 与 Pass Criteria；
- Responsible AI；
- 隐私、安全、滥用和风险检查；
- Experimentation 与 Pilot。

### 产品执行与持续迭代

- 接手已有 PRD、代码、原型、数据和评测资产；
- 对已有资产执行 <code>REUSE / VERIFY / EXECUTE</code>；
- 按 Task 推进产品和工程交付；
- 每个确定 Task 完成后的人工审核；
- Build Readiness 与 Release Readiness；
- Launch 与发布准备；
- Production Learning 与 bad case 分析；
- Evidence、Decision 与 Artifact 管理；
- Requirement Change 与 Replan；
- Local Replan 与 Profile Replan；
- Regression 与重新发布；
- Retrospective；
- 跨会话持续项目状态恢复。

Skill 包含 8 个产品生命周期节点：

~~~text
Qualification
Cognition
Product Definition & Scope
Solution Design
Implementation
Validation & Iteration
Release & Operation
Retrospective
~~~

Skill 包含 16 个按需加载的专业 Capability：

~~~text
Discovery
Competitive Intelligence
Business Case
Roadmap
Product Requirements
Requirement Review
AI Feasibility
Data Strategy
Human-AI Experience
Evaluation
Responsible AI
Delivery
Experimentation
Launch
Production Learning
Retrospective
~~~

Skill 根据真实缺口、已有证据和当前目标选择：

~~~text
EXECUTE
VERIFY
REUSE
不激活
~~~

- 详细 Skill 定义：[AI Product Development Skill](skills/ai-product-development/SKILL.md)
- 使用边界：[Usage Boundary](docs/usage-boundary.md)

## 4. 部署方式和方法

### Codex 安装

在 Codex 中调用：

~~~text
$skill-installer
~~~

然后发送：

~~~text
请从 https://github.com/32631999wzc-create/AI-Manager-SOP/tree/main/skills/ai-product-development 安装这个 Skill。
~~~

安装完成后直接使用：

~~~text
$ai-product-development
~~~

### 手动安装

将：

~~~text
skills/ai-product-development/
~~~

完整复制到：

~~~text
$CODEX_HOME/skills/ai-product-development/
~~~

默认目录通常为：

~~~text
~/.codex/skills/ai-product-development/
~~~

请保留完整目录结构：

~~~text
ai-product-development/
├── SKILL.md
├── references/
├── schemas/
├── templates/
└── scripts/
~~~

Continuous Runtime 和 Validator 需要：

~~~text
Python 3.10+
PyYAML
~~~

- 项目地址：[AI-Manager-SOP](https://github.com/32631999wzc-create/AI-Manager-SOP)
- 最新版本：[Releases](https://github.com/32631999wzc-create/AI-Manager-SOP/releases)
- License：[MIT](LICENSE)
