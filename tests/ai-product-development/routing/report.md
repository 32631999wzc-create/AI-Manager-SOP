# Phase 1 Routing 验证报告

最新验证日期：2026-09-11（Asia/Shanghai）。本次生命周期节点合同和 Kernel 变化后，R1–R3 均以当前 Skill 哈希重新执行。

## 结论

R1、R2、R3 均为 **PASS**。三个场景使用独立临时目录、ephemeral Codex 会话和 read-only 沙箱。必要模块均由成功的实际文件读取证明；没有必要模块漏读、未解释额外读取或 lifecycle/runtime eager loading。模型自述不作为读取证据。

结构检查保持八个 lifecycle node、六项 runtime capability、三个顶层 Gate、原 canonical runtime objects 与迁移基线。Kernel 当前 251 行。

## 当前实际读取

| 场景 | 实际读取顺序 | 结论 |
|---|---|---|
| R1 Greenfield Prototype Qualification 与 Profile | SKILL.md → 01-qualification.md → execution-profile.md → schema:execution-profile.yaml → gates.md | PASS |
| R2 已有系统 Validation Only | SKILL.md → 06-validation-iteration.md → executor.md → execution-profile.md | PASS |
| R3 目标和范围不变的 Local Replan | SKILL.md → execution-profile.md → replan-recovery.md → planner.md → registry-versioning.md | PASS |

R2 额外读取 Profile，用于确认已给 Profile 的复用和依赖闭包；R3 额外读取 Profile，用于确认目标与范围未变，因此不触发 Profile Replan。两项都有当前任务依据。R1 无未解释额外读取。三者都没有展开无关 lifecycle/runtime 目录。

Kernel 使用两个确定性行块读取。grader 逐块与当前文件比较，只有连续覆盖全文时才登记一次完整读取；文件名导航不算内容加载。完整命令、读取路径、item id 和 dependency closure 位于 [accepted evidence](evidence)，其哈希由 [accepted-runs.json](accepted-runs.json) 固定。

## 回放

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase1*.py"
python -B -X utf8 tests/ai-product-development/routing/verify_evidence.py
```

Routing smoke tests 只证明三个有限任务的 progressive disclosure。Profile/Plan 行为由 Phase 2 八场景验证，跨会话连续执行由 Phase 3 Golden MVP 验证。
