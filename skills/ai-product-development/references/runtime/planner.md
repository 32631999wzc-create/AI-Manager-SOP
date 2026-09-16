# Planner

The Profile determines **what needs to be done and how deeply**. The Planner determines **which concrete tasks to execute and in what order**.

Use this minimal runtime plan structure:

结构定义：[Plan](../../schemas/plan.yaml)。

The Plan is runtime state, not a new lifecycle node or management service.

## 8.1 Plan Before Execute

For every significant work package:

1. state the immediate objective;
2. identify active lifecycle gaps;
3. identify reusable assets;
4. produce a concise task plan;
5. check dependencies, blocking inputs, and parallel conflicts;
6. execute only after the plan is valid.

Show a concise Plan Preview to the user for the initial major plan and for material scope/cost/deployment changes. Do not repeatedly interrupt the user for trivial local replans.

## Replan Trigger Contract

在读取 Replan reference 或生成 Replan 动作前，先判断三个事实：

1. `baseline_exists`：当前 assignment 已有经验证且当前有效的 Execution Profile 与 Plan；初始请求、初始材料或本轮刚生成的初始 Profile/Plan 不构成“变化前 baseline”。
2. `change_event_exists`：baseline 建立后发生了新的外部输入、证据、产物修改、任务失败、决策变化、范围变化或主要约束变化。
3. `material_impact_exists`：该事件实际使既有 Task、Artifact、Decision、Assumption、Dependency、Acceptance Criteria、Assignment Scope 或 Node Profile 至少一项需要改变或失效。

三项判断产生一个轻量内部分类，不新增 Runtime capability 或持久状态机：

| 条件 | Operation Mode | Replan |
|---|---|---|
| 无 baseline | `INITIAL_PLAN` | `required = false` |
| 有 baseline，但无 baseline 后事件或无实质影响 | `CONTINUE` | `required = false` |
| 有 baseline、事件和实质影响，且交付目标、Assignment Scope、主要约束不变 | `LOCAL_REPLAN` | `required = true` |
| 有 baseline、事件和实质影响，且交付目标、Assignment Scope 或主要约束变化 | `PROFILE_REPLAN` | `required = true` |

`INITIAL_PLAN` 与 `CONTINUE` 必须输出 `change_type = null`、`reopen_trigger = null`、`actions = []`，且不加载 Replan reference。只有 `LOCAL_REPLAN` 或 `PROFILE_REPLAN` 才读取 Replan and Recovery 并选择 change type 与最小动作。`material_impact_exists` 必须由具体受影响对象或字段支持；“收到新信息”本身不是影响证据。

## 8.2 Generate Tasks from Gaps

For each active node:

`Node Profile → inspect existing artifacts → identify gaps → generate 0..N tasks`

A node may generate zero tasks when existing verified artifacts already satisfy it.

### Capability Need Selection

Before generating a task, translate only the unresolved lifecycle gap into a `Capability Need`:

```yaml
capability_need:
  capability:
  reason:
  supports_node:
  mode: EXECUTE | VERIFY | REUSE
  decision_to_unlock:
```

Select a capability only when its `When to use` matches the gap and its `When NOT to use` does not. Then check that its `decision_to_inform`, required blocking inputs, evidence requirements, output contract, and supported lifecycle can unlock the named decision.

Capability activation 必须同时具有 explicit gap、decision to unlock 和当前 evidence state。没有 gap 时不创建 Capability Need；项目通常会用到某能力不是触发理由。相关资产只有在当前 gap 的决策依赖它时才进入 `VERIFY` 或 `REUSE`。

- `EXECUTE` — the required analysis or output is absent and necessary.
- `VERIFY` — a relevant asset exists but its evidence, freshness, consistency, or applicability is unconfirmed.
- `REUSE` — a verified, current asset already satisfies this gap; do not rerun the capability.

这里的 `gap` 指当前 lifecycle 决策尚未解锁，不等于该 Capability 的分析工作一定未做。若决策仍待完成，而已验证、仍适用的资产正好提供该决策所需证据，记录 `REUSE` Capability Need 并引用该资产，不生成重复执行任务；若决策已完成且没有新的 gap，则不激活 Capability。

If no domain matches, keep the gap explicit rather than choosing the nearest label. If several match, select the smallest dependency set and order them by the decisions they unlock. Capability selection does not create a second state machine; only actual independent deliverables become Tasks.

## 8.3 Valid Task Rule

A task is valid only if it has:

- one clear goal;
- identifiable inputs;
- one primary deliverable/result;
- explicit acceptance criteria;
- known dependencies.

Do not create tasks such as “think more”, “continue analyzing”, or one task per checklist item without a real independent deliverable.

## 8.4 Split a Task When

Split when one of these is true:

- there are multiple independent outputs;
- different capabilities/workers are needed;
- part can run in parallel;
- part needs an independent retry or gate;
- a failure should not force unrelated work to rerun;
- the task is too large to complete reliably in one execution.

Stop splitting when the task has one goal, one deliverable, clear acceptance, and can be retried independently.

## 8.5 Dependencies

Use only:

- `HARD`
- `DATA`
- `DECISION`
- `GATE`

Soft dependencies may influence quality or priority but do not block `READY` status.

A task becomes `READY` only when all hard dependencies and required artifacts are valid and no blocking input or gate remains.

## 8.6 Parallelism

Parallelize only when:

- there is no hard dependency;
- there is no shared mutable state;
- tasks do not directly write the same formal artifact version;
- outputs have independent contracts and can be merged or committed independently.

Parallelism is a performance optimization, not a correctness requirement. Sequential execution must remain valid.

## 8.7 Priority

Use `P0 | P1 | P2 | P3`.

Prioritize based on:

- blocking impact;
- business impact;
- risk reduction;
- dependency-unlock value;
- deadline urgency;
- execution cost.

Dependency determines what must precede what; priority determines what to execute first among ready work.

`OPTIONAL` work stays out of the active DAG unless requested, risk-reducing, newly required by dependency, or clearly worth remaining resources.

## 8.8 Planning Gate

Before execution check:

- objective is clear;
- assignment scope is respected;
- required nodes are covered;
- hard dependencies are closed;
- the DAG has no cycle;
- blocking inputs are identified;
- acceptance criteria exist;
- parallel tasks do not conflict;
- risk floors remain satisfied.

Result: `PASS | PASS_WITH_ASSUMPTIONS | BLOCKED`.

Represent iteration with new task instances, never a cyclic DAG.
