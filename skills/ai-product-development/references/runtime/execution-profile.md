# Execution Profile

## Delivery Target

Use one of:

- `PROTOTYPE` — product/UI concept and interaction; real backend or AI may be mocked.
- `DEMO` — core AI chain must actually run and prove feasibility.
- `MVP` — real users can use the product in a real workflow; persistent state, integration, reliability, evaluation, and basic monitoring normally matter.
- `ENTERPRISE` — production deployment with appropriate reliability, security, permissions, observability, governance, deployment, rollback, and cost controls.
- `UNDECIDED` — diagnose the target with the smallest necessary question set.

If `UNDECIDED`, determine only what materially affects the target, such as:

- Does the AI chain need to run for real?
- Are real users involved?
- Is persistent data required?
- Are external APIs or tools required?
- Is authentication or permission control required?
- Is production deployment expected?
- Is enterprise security, compliance, monitoring, or auditability required?

Recommend a target with a short reason and ask for confirmation when the choice materially changes scope.

## 5.2 Determine Assignment Scope

Separate project maturity from this assignment.

结构定义：[AssignmentScope](../../schemas/execution-profile.yaml)。

A project may be Enterprise while the current assignment covers only evaluation, architecture, UI, one service, or another subset.

## Profile Generation

After Qualification, calculate an execution profile for all eight lifecycle nodes.

Each node receives:

结构定义：[AssignmentScope / NodeProfile](../../schemas/execution-profile.yaml)。

## 6.1 Base Profile by Delivery Target

Use this as a starting point only:

| Node | Prototype | Demo | MVP | Enterprise |
|---|---|---|---|---|
| Qualification | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| Cognition | LIGHT | REQUIRED | REQUIRED | REQUIRED |
| Product Definition & Scope | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| Solution Design | LIGHT | REQUIRED | REQUIRED | REQUIRED |
| Implementation | REQUIRED | REQUIRED | REQUIRED | REQUIRED |
| Validation & Iteration | LIGHT | REQUIRED | REQUIRED | REQUIRED |
| Release & Operation | SKIP | LIGHT | REQUIRED | REQUIRED |
| Retrospective | LIGHT | LIGHT | LIGHT | LIGHT |

Assignment Scope may make a node `OUT_OF_SCOPE`. Existing assets may reduce work to `VERIFY`. Risk and hard dependencies may raise the minimum depth.

## 6.2 Scope Rules

Classify each node:

- `PRIMARY` — directly produces requested deliverables; normally at least `LIGHT`, usually `REQUIRED`.
- `SUPPORTING` — required for a primary node to be executed reliably; normally at least `LIGHT`.
- `OUT_OF_SCOPE` — not part of this assignment; default `SKIP` unless risk or hard dependency requires minimal work.

If a capability is required for the overall project but outside the current assignment, record it as `external_project_requirement` instead of pretending it is unnecessary.

## 6.3 Existing Asset Rules

Classify relevant assets:

- `ABSENT`
- `PRESENT_UNVERIFIED`
- `VERIFIED_REUSABLE`
- `PARTIAL`
- `OUTDATED`
- `CONFLICTING`

Apply:

- `VERIFIED_REUSABLE` → prefer `VERIFY`; do not rebuild.
- `PRESENT_UNVERIFIED` → verify before relying on it.
- `PARTIAL` → keep required depth but generate tasks only for the gap.
- `OUTDATED` → do not reduce required work.
- `CONFLICTING` → resolve the conflict before dependent work proceeds.

Existing assets reduce duplicated work; they do not automatically remove necessary validation.

## 6.4 Project Mode

Infer:

- `GREENFIELD` — no existing implementation to understand.
- `BROWNFIELD` — modify an existing system.
- `HYBRID` — reuse some existing components while creating others.

If modifying an existing repository, `Cognition` is `REQUIRED` for the affected code path.
If no repository exists, repository cognition is not applicable.

## 6.5 Feature Triggers

Activate capabilities only when the project actually needs them.

Examples:

- Existing repository modification → repository inspection and dependency tracing.
- Persistent state → data/state design.
- External API/tool → integration contract and failure handling.
- Real users → reliability, evaluation, monitoring, observation.
- Authentication/permissions → access-control design.
- Sensitive data → privacy/security requirements.
- Long-running work → task state, recovery, and possibly async execution.
- Cost sensitivity → cost measurement or caching only where repeated cost is demonstrated.
- RAG, Agent, Multi-Agent, long-term memory, cache, or async → activate only when the requirement justifies them.

## 6.6 Risk Floors

Risk may raise a node or capability above what scope preferences alone would suggest.

Examples:

- High-risk decisions → stronger evaluation, traceability, and human review as appropriate.
- Sensitive data → privacy/security controls cannot be silently skipped.
- Enterprise production → release readiness, monitoring, reliability, security, and rollback expectations must be covered, either in-scope or explicitly externalized.

Time or budget pressure should primarily reduce scope or execution breadth, not silently remove essential quality or safety floors.

## 6.7 Dependency Closure

After initial profile calculation, restore any prerequisite required by an active dependent node.

Examples:

- Implementation without a verified design → Solution Design at least `LIGHT`.
- Validation without defined acceptance criteria → Evaluation Design capability inside Solution Design at least `MINIMAL`.
- Existing repo modification → Cognition cannot be skipped.
- Production release → validation and release readiness cannot be skipped.

Repeat dependency closure until the profile no longer changes.

## Rule Precedence

按 [Kernel 的 Rule Precedence](../../SKILL.md#rule-precedence) 处理冲突。

## 6.9 Consistency Check

Reject contradictory profiles, such as:

- implementation required while all design is skipped and no reusable design exists;
- validation required but no success criteria exist;
- existing repository modification with cognition skipped;
- enterprise production release with validation or monitoring completely ignored.

Every `SKIP` must have a reason.
