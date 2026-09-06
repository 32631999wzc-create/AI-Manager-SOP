# Replan and Recovery

Do not use project-wide rollback as the default recovery model.

When a material change or non-retryable failure occurs:

`Change → Replan → Preserve valid work → Invalidate affected work → Add/Cancel tasks → Continue`

## 12.1 Change Types

Use only:

- `INPUT_CHANGE`
- `ARTIFACT_CHANGE`
- `TASK_FAILURE`
- `DECISION_CHANGE`
- `SCOPE_CHANGE`

This is a logical event structure, not a requirement for an event bus.

## 12.2 Replan Actions

Replan may only apply these basic actions:

- `PRESERVE`
- `OUTDATE`
- `ADD`
- `CANCEL`

Preserve unaffected work by default.

## 12.3 Local vs Profile Replan

Use `LOCAL REPLAN` for task failure, artifact changes, debugging fixes, and local requirement changes.

Use `PROFILE REPLAN` when delivery target, assignment scope, or a major project constraint changes. Recalculate affected node profiles, but continue to reuse valid existing records and artifacts.

Create a new plan version only when the task DAG structure materially changes. Normal state changes such as `RUNNING → COMPLETED` do not require a new plan version.

If user input is required, create one clear `HUMAN_CONFIRM` task, block only the affected tasks, and resume when answered.
