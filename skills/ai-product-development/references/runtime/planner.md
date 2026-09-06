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

## 8.2 Generate Tasks from Gaps

For each active node:

`Node Profile → inspect existing artifacts → identify gaps → generate 0..N tasks`

A node may generate zero tasks when existing verified artifacts already satisfy it.

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
