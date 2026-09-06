# Registry and Versioning

Use one logical `Project Registry` containing Records and Artifacts. It may be implemented with files, JSON, a database, or existing project infrastructure depending on delivery level.

## 11.1 Record Write Rules

May commit as long-term records:

- user-confirmed facts;
- confirmed decisions;
- verified constraints;
- validated conclusions that materially affect later work.

Do not promote temporary model reasoning, drafts, guesses, or failed outputs.

Assumptions remain `ASSUMPTION` until confirmed or rejected.

## 11.2 Artifact Commit Rules

Formal artifact flow:

`Task Result → Validation PASS → Commit → Artifact`

Create an artifact only when it must be reused, delivered, versioned, shared across tasks, used for a major decision, or used by release/validation.

Formal updates create a new version:

`vN ACTIVE → create vN+1 ACTIVE → vN SUPERSEDED`

Use simple monotonic versions (`v1`, `v2`, ...). Do not require semantic versioning.

`OUTDATED` means the artifact may no longer be valid and has no replacement yet.
`SUPERSEDED` means a newer valid version exists.

Parallel tasks must not directly overwrite the same active artifact. Produce isolated proposed changes, merge/resolve conflicts, validate, then commit one new version.

对象字段与枚举见 [ProjectRecord / Artifact / RuntimeSnapshot](../../schemas/project-state.yaml)。
