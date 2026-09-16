---
name: ai-product-development
description: Plan and execute AI product development from prototype through production, dynamically adapting scope and engineering depth to the delivery target, existing assets, assignment scope, project characteristics, dependencies, and risk.
---

# AI Product Development

Use this skill when the user wants to define, design, build, evaluate, improve, or release an AI-enabled product, including work on an existing product or repository.

Do not force the full lifecycle when the user only owns or requests a subset. Use `Assignment Scope` to constrain execution.

## 1. Operating Principles

Always follow these rules:

1. **Plan before execution.** For every significant work package, create a concise plan before doing the work.
2. **Confirm delivery depth before designing.** Determine whether the target is Prototype, Runnable Demo, Integrated MVP, or Production / Enterprise.
3. **Inspect before replacing.** Reuse valid existing documents, code, architecture, datasets, APIs, evaluations, and decisions.
4. **Define success before build.** Establish the minimum evaluation and acceptance criteria needed for the delivery target before substantial implementation.
5. **Generate tasks from gaps, not checklists.** A capability does not automatically become a task.
6. **Use the lowest-complexity solution that meets the requirement.** Do not default to Agent, Multi-Agent, RAG, long-term memory, vector databases, knowledge graphs, async queues, caches, or enterprise infrastructure.
7. **Preserve valid work.** When requirements or artifacts change, replan only the affected work.
8. **Store fully, read selectively.** Keep important project state and formal artifacts, but provide each task only the context it needs.
9. **Do not silently convert assumptions into facts.** Assumptions remain explicit until confirmed.
10. **Do not silently overwrite formal artifacts.** Formal updates create a new version.

## 2. Lifecycle

The lifecycle has exactly eight top-level nodes. Do not create additional top-level lifecycle nodes unless the user explicitly requires a different process.

1. `Qualification`
2. `Cognition`
3. `Product Definition & Scope`
4. `Solution Design`
5. `Implementation`
6. `Validation & Iteration`
7. `Release & Operation`
8. `Retrospective`

Internal checklist items are **capabilities**, not lifecycle nodes and not automatically tasks.

## 3. Runtime

Use only these runtime capabilities:

- `Profile` — determine which lifecycle nodes are needed and at what depth.
- `Planner` — convert active lifecycle gaps into tasks and dependencies.
- `Context` — assemble minimal task-specific context.
- `Executor` — select a capable worker, execute, and validate.
- `Registry` — store confirmed project records and formal artifact references.
- `Replan` — preserve, invalidate, add, or cancel work after change or failure.

Do not introduce extra Manager, Orchestrator, Recovery, Merge, or Memory-Agent layers unless a concrete project requirement makes them necessary.

## 4. Architecture and Responsibility Boundary

Use five cooperating layers without introducing another state machine:

- `Kernel` — global principles, complexity guardrails, progressive disclosure, and routing.
- `Lifecycle` — the product state and the decisions required before that state is satisfied.
- `Runtime` — profiling, planning, context assembly, execution, registry, and replanning.
- `Professional Capabilities` — domain methods used to reduce a specific uncertainty or produce evidence for a decision.
- `Evidence / Decision / Artifact` — why a conclusion is credible, what choice was made, and what durable output resulted.

`Gate` is not a layer or capability. It decides whether work may advance using evidence supplied by lifecycle and capability work. `Registry` records which facts, decisions, and artifacts are currently valid.

Planner may select a professional capability only for an actual lifecycle gap. Treat the selection as an internal `Capability Need` with: capability, reason, supported lifecycle node, `EXECUTE | VERIFY | REUSE` mode, and the decision it must unlock. Do not persist a separate capability status machine or turn the capability catalog into tasks.

## Global Invariants

- Profile 决定所需节点和深度；Planner 从实际缺口生成任务。节点、能力与任务不可混为一谈。
- 只执行依赖和输入满足的 READY 任务；Worker 的范围、计划及正式内容操作边界见 [Executor](references/runtime/executor.md#103-execution)。
- 正式内容经验证后提交；假设与事实分开，更新创建新版本，保留有效工作。
- Qualification、Build Readiness、Release Readiness 是仅有的三个顶层 Gate；其他检查保持局部。
- 所有节点共用下方 Completion Criteria；不能以访问完清单代替完成任务。
- 执行节点时遵循对应 reference 的 Required Inputs → Required Decisions / State → Capability Routing → Outputs → Completion Criteria；专业方法遵循被选 Capability 的合同。输入不足时明确假设或阻塞，未满足节点完成条件不得标记 `SATISFIED`。

## Progressive Disclosure Router

路径相对于本 Skill 目录。核心原则与 guardrails 始终生效，详细规则在对应操作前读取。
先用当前 Kernel 和已提供材料判断任务；Qualification 仍按原文作为前置检查。
初次 Qualification 按需读取 Qualification reference，以及用于目标与范围判断的 Execution Profile。
随后遵循：Execution Profile → determine active nodes → load only relevant node references。
Profile 为全部八个节点记录状态，但不要默认读取全部 lifecycle references。
对 REQUIRED、LIGHT 或实际启用的 OPTIONAL 节点，在开始该节点工作时加载对应文件。
VERIFY 只加载当前核验任务相关节点规则；已确认的可复用资料用于满足依赖，不因 Profile 中列为 VERIFY 就逐个读取节点详情。
SKIP 不触发该节点的完整流程或任务。
不要为了确认 `SKIP` 而先读取节点 reference；例如 Greenfield 且没有既有产品、系统或仓库时，不读取 Cognition reference。
Profile 改变时重新判断相关文件；不因一次任务读取过某文件而把全部 references 常驻上下文。

### Lifecycle Routing

| Active node | Reference |
|---|---|
| Qualification | [规则](references/lifecycle/01-qualification.md) |
| Cognition | [规则](references/lifecycle/02-cognition.md) |
| Product Definition & Scope | [规则](references/lifecycle/03-product-definition.md) |
| Solution Design | [规则](references/lifecycle/04-solution-design.md) |
| Implementation | [规则](references/lifecycle/05-implementation.md) |
| Validation & Iteration | [规则](references/lifecycle/06-validation-iteration.md) |
| Release & Operation | [规则](references/lifecycle/07-release-operation.md) |
| Retrospective | [规则](references/lifecycle/08-retrospective.md) |

### Professional Capability Routing

以下 16 项是可按需调用的 `Professional Capability Domains`，不是新的顶层节点、Gate、Agent 或固定步骤。先由 lifecycle gap 和待解锁决策判断是否触发，再只读取所需 domain；同一任务可加载多个有直接依赖的 domain，但不得为“完整”而预读全部。

| 类别 | 当前问题或交付物 | Capability domain |
|---|---|---|
| Decision | 发现真实用户问题、梳理现有工作流、验证机会 | [用户与机会发现](references/capabilities/discovery/SKILL.md) |
| Decision | 研究市场、替代方案、竞品与可行动差异 | [市场与竞品情报](references/capabilities/competitive-intelligence/SKILL.md) |
| Decision | 建立商业论证、评估价值/成本/风险并排优先级 | [商业论证与优先级](references/capabilities/business-case/SKILL.md) |
| Planning & Learning | 形成 outcome-based roadmap、里程碑与发布切片 | [路线图与版本规划](references/capabilities/roadmap/SKILL.md) |
| Decision | 编写或修订可实现、可评测的 PRD | [产品需求定义](references/capabilities/product-requirements/SKILL.md) |
| Operating | 组织需求评审、解决异议并固化决策 | [需求评审与决策](references/capabilities/requirement-review/SKILL.md) |
| Decision | 判断 AI fit、模型/方案可行性并做学习型原型 | [AI 可行性与原型](references/capabilities/ai-feasibility/SKILL.md) |
| Design / Cross-cutting | 规划数据来源、许可、质量、标注、治理与反馈数据 | [数据策略与治理](references/capabilities/data-strategy/SKILL.md) |
| Design | 设计预期、控制、解释、人工介入与失败恢复 | [Human-AI 体验](references/capabilities/human-ai-experience/SKILL.md) |
| Design / Cross-cutting | 把产品要求变成 eval、数据集、grader、阈值和回归 | [评测与质量](references/capabilities/evaluation/SKILL.md) |
| Design / Cross-cutting | 识别危害、滥用、隐私、安全与合规风险并设置控制 | [责任 AI、安全与风险](references/capabilities/responsible-ai/SKILL.md) |
| Operating | 将已评审范围转成跨职能交付、backlog 与变更决策 | [跨职能交付协作](references/capabilities/delivery/SKILL.md) |
| Operating | 用原型、实验、dogfood 或 pilot 验证价值与质量 | [实验与试点](references/capabilities/experimentation/SKILL.md) |
| Operating | 规划 rollout、培训、支持、采用与发布沟通 | [发布、采用与赋能](references/capabilities/launch/SKILL.md) |
| Operating / Cross-cutting | 监测质量/价值/成本/风险并把信号转成改进闭环 | [生产观测与学习闭环](references/capabilities/production-learning/SKILL.md) |
| Planning & Learning | 复盘结果、决策、失败假设、债务与可复用资产 | [复盘与组合学习](references/capabilities/retrospective/SKILL.md) |

Lifecycle 与 capability 是多对多关系，具体选择以各 lifecycle reference 的 `Capability Routing` 为准。`Data`、`Evaluation`、`Responsible AI` 和 `Production Learning` 是 cross-cutting capabilities，不因当前节点不同而失效。

### Runtime Routing

Runtime 文件按当前执行阶段加载，不机械一次性读取全部文件。

| 当前操作 | Reference |
|---|---|
| 判断交付目标、范围、资产、深度、风险与依赖闭包，或 Profile Replan | [Execution Profile](references/runtime/execution-profile.md) |
| 从缺口规划、拆任务、排依赖、并行或优先级，检查计划 | [Planner](references/runtime/planner.md) |
| 检索项目状态、组装或裁剪任务上下文 | [Context](references/runtime/context.md) |
| 选择 Worker、执行、验证或局部重试 | [Executor](references/runtime/executor.md) |
| 判断正式产物状态、写入项目记录、提交正式产物或更新版本 | [Registry and Versioning](references/runtime/registry-versioning.md) |
| 实质变更、不可重试失败或恢复执行 | [Replan and Recovery](references/runtime/replan-recovery.md) |
| 判断 Qualification / Build / Release Gate | [Gates](references/runtime/gates.md) |

先按 [Planner 的 Replan Trigger Contract](references/runtime/planner.md#replan-trigger-contract) 区分 `INITIAL_PLAN | CONTINUE | LOCAL_REPLAN | PROFILE_REPLAN`。只有后两者或准备调整任务时读取 Replan and Recovery；`required = false` 的空 Replan 结构不触发该文件。普通输入变化不能因输出结构含有 `reopen_trigger` 字段而被解释为决策重开。

### Data and Output Routing

Use canonical project objects for work, evidence, decisions, artifacts, and optional recovery state.
数据定义保留原文 YAML 对象示意，字段留空不是默认值；枚举用原文的竖线写法表示。
这些文件不是 JSON Schema，也不声称已有对象实例自动验证器。
只在构造、读取或验证相应对象时加载：

| 对象 / 输出 | Canonical location |
|---|---|
| Task、任务状态 | [task.yaml](schemas/task.yaml) |
| ProjectRecord、Artifact、可选 RuntimeSnapshot | [project-state.yaml](schemas/project-state.yaml) |
| EvidenceRecord | [evidence-record.yaml](schemas/evidence-record.yaml) |
| DecisionRecord | [decision-record.yaml](schemas/decision-record.yaml) |
| AssignmentScope、NodeProfile（Execution Profile 的每节点定义） | [execution-profile.yaml](schemas/execution-profile.yaml) |
| Plan | [plan.yaml](schemas/plan.yaml) |
| TaskContextPack | [context-pack.yaml](schemas/context-pack.yaml) |
| 用户可见的初始 / 重大变更计划 | [execution-plan.md](templates/execution-plan.md) |

原文没有独立 ExecutionProfile 聚合对象字段，不补造 schema。
Product Context Snapshot、Product Definition & Scope、Retrospective 没有稳定字段格式；
其输出规则留在对应 lifecycle reference，不为它们新增固定模板。
详细规则只在 canonical location 维护；Kernel 仅保留全局 invariant 和路由。


### Executable Validation

构造或修改 Profile、Plan 或 canonical runtime object 后，运行只读的 [runtime validator](scripts/validate_runtime.py)。
根据当前输入使用 `profile`、`plan`、`combined` 或 `objects` 模式；验证失败时修正对应对象或计划，不让验证器自动补字段、改状态或写项目记录。
验证包装层仅提供交叉检查所需的输入上下文，不是新的持久化 schema。

### Continuous Local Runtime

当本地产品确有跨任务或跨会话连续执行需要时，使用 [project runtime](scripts/project_runtime/README.md) 将已验证的 Profile、Plan、Task、ProjectRecord、EvidenceRecord、DecisionRecord、Artifact、RuntimeSnapshot 和 TaskContextPack 保存到产品仓库的 `.ai-product/`。先按当前 Router 读取相关 canonical rules，再调用对应命令；Runtime 只保存、校验和恢复显式状态，不代替产品判断或生命周期工作。

首次建立状态使用 `init`；执行前用 `next` 构造当前 READY Task 的最小上下文；重大确认、Gate、阶段完成或长暂停时用 `checkpoint`；新会话用 `resume`；实质变更使用 `replan`；节点状态确认后用 `update-profile`；结束前用 `complete` 检查 Completion Criteria。不要把 `.ai-product/` 当作聊天记忆，也不要在没有连续性需求时机械创建它。

## Rule Precedence

Resolve conflicts in this order:

1. Hard safety / feasibility rule
2. Risk floor
3. Hard dependency
4. Explicit assignment scope
5. Feature trigger
6. Existing asset reuse
7. Delivery-target base profile
8. Preference / nice-to-have

# 14. Complexity Guardrails

Apply these throughout the project:

1. No business trigger → no new Agent.
2. No demonstrated retrieval-scale problem → no vector database by default.
3. No real relationship-reasoning need → no knowledge graph by default.
4. No cross-task continuity need → no long-term memory system by default.
5. No demonstrated repeat-cost problem → no cache infrastructure by default.
6. No long-running/concurrency need → no async queue by default.
7. No production requirement → no enterprise CI/CD, SLA, or heavy monitoring by default.
8. No approval requirement → no approval workflow engine.
9. No concrete distributed-recovery requirement → no rollback/recovery infrastructure.
10. If a field, rule, existing tool, or existing platform is enough, do not introduce a new service, manager, or Agent.

Explicitly avoid by default:

- Agent Orchestrator
- Memory Manager Agent
- Recovery Manager
- Rollback Manager
- Merge Manager
- Impact Analysis Service
- Event Bus / Event Sourcing
- Vector Memory
- Knowledge Graph
- autonomous worker-to-worker negotiation

These remain conditional capabilities, not skill infrastructure.

# 15. User-Facing Execution Style

Keep runtime machinery mostly internal. User-facing communication should stay concise and decision-oriented.

At the start of substantial work, show:

使用 [Plan Preview 模板](templates/execution-plan.md)。

During execution, surface only material findings, blockers, assumptions needing confirmation, major decisions, and changes to plan or scope.

Do not repeatedly show internal registries, IDs, state transitions, or full DAGs unless the user requests them or they materially improve understanding.

When asking a question, ask only what is currently blocking or materially changes the solution.

# 16. End-to-End Procedure

Execute this loop:

```text
User Request / Project Materials
        ↓
Qualification
        ↓
Execution Profile
        ↓
Cognition
        ↓
Product Definition & Scope
        ↓
Solution Design
   ├─ Architecture
   └─ Evaluation Design
        ↓
Build Readiness
        ↓
Planner → Task DAG
        ↓
Context → Execute → Validate → Commit
        ↓
Validation & Iteration
   ├─ PASS
   └─ FAIL → Root Cause → Minimal Fix → Replan → Execute → Re-evaluate
        ↓
Release & Operation, if required
        ↓
Retrospective
        ↓
Complete
```

Do not mechanically run every node. The Execution Profile controls actual depth and may skip nodes that are not applicable.

# 17. Completion Criteria

Do not declare completion because every predefined checklist item was visited.

Complete the assignment only when:

- requested deliverables are complete;
- all `REQUIRED` nodes in the current assignment are `SATISFIED`;
- acceptance criteria are met;
- no blocking issue remains;
- required formal artifacts are `ACTIVE`;
- any project-critical capability outside the assignment is explicitly identified rather than silently ignored.

At completion, provide a concise summary of:

- what was delivered;
- what was validated;
- remaining assumptions or risks;
- deferred/out-of-scope items;
- reusable artifacts, when relevant.
