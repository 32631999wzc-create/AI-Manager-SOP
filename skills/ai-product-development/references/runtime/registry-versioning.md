# Registry and Versioning

Use one logical `Project Registry` containing Project Records, Evidence Records, Decision Records, and Artifacts. It may be implemented with files, JSON, a database, or existing project infrastructure depending on delivery level.

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

Artifact 使用 `evidence_refs` 和 `decision_refs` 指向支撑其关键结论的 EvidenceRecord 与 DecisionRecord。引用只建立可追溯关系，不复制证据、决策或详细业务规则；引用对象必须已存在于同一 Registry。

## 11.3 Evidence Record Rules

当某项观察将支撑或反驳重要产品结论时，将其登记为 [EvidenceRecord](../../schemas/evidence-record.yaml)：

- `observation` 只记录观察到的内容；`interpretation` 单独记录其含义，不把推断伪装成事实；
- `source`、`observed_at`、`context`、`owner` 说明来源、时间、适用语境和责任人；
- `supports` 与 `contradicts` 指向它影响的结论、假设或决策问题；
- `confidence` 与 `limitations` 明确证据强度和限制；
- 正式更新使用 `vN`；不得静默覆盖旧证据。

## 11.4 Decision Record Rules

重要产品选择使用 [DecisionRecord](../../schemas/decision-record.yaml)，必须能够直接回答：

- 为什么这么决定：`question`、`options`、`selected`、`rationale`；
- 依据是什么：`evidence_refs`，并保留仍影响判断的 `assumptions` 与 `dissent`；
- 什么时候重新决定：`valid_until` 与 `reopen_trigger`。

`evidence_refs` 只能引用已登记 EvidenceRecord。发生重新决策时创建新的 DecisionRecord，并用 `supersedes` 指向被替代的当前决策；不修改旧记录。`ProjectRecord.type=DECISION` 仅为已有 Registry 兼容保留，新建重要决策使用 DecisionRecord，避免维护两份详细决策真相。

## 11.5 Artifact Versioning

Create an artifact only when it must be reused, delivered, versioned, shared across tasks, used for a major decision, or used by release/validation.

Formal updates create a new version:

`vN ACTIVE → create vN+1 ACTIVE → vN SUPERSEDED`

Use simple monotonic versions (`v1`, `v2`, ...). Do not require semantic versioning.

`OUTDATED` means the artifact may no longer be valid and has no replacement yet.
`SUPERSEDED` means a newer valid version exists.

Parallel tasks must not directly overwrite the same active artifact. Produce isolated proposed changes, merge/resolve conflicts, validate, then commit one new version.

对象字段与枚举见 [ProjectRecord / Artifact / RuntimeSnapshot](../../schemas/project-state.yaml)、[EvidenceRecord](../../schemas/evidence-record.yaml) 与 [DecisionRecord](../../schemas/decision-record.yaml)。

## Local Persistence

需要在本地产品仓库保存 Registry 时，使用 [Continuous Project Runtime](../../scripts/project_runtime/README.md) 的 `register-record`、`register-evidence`、`register-decision`、`commit-artifact` 和 `checkpoint`。运行时复用本节规则及 canonical schema，不建立第二套对象定义。
