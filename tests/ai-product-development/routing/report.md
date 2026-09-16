# Phase 1 Routing 验证报告

最新验证日期：2026-09-14（Asia/Shanghai）。新增 16 个 capability playbook、Kernel 路由及 lifecycle `Load With` 后，R1–R3 均以当前 Skill 哈希重新执行。

## 结论

R1、R2、R3 均为 **PASS**。三个场景使用独立临时目录、ephemeral Codex 会话和 read-only 沙箱。必要模块均由成功的实际文件读取证明；没有必要模块漏读、未解释额外读取或 lifecycle/runtime eager loading。模型自述不作为读取证据。

结构检查保持八个 lifecycle node、六项 runtime capability、三个顶层 Gate、原 canonical runtime objects 与迁移基线。新增 capability 是按需加载子能力，不改变这些顶层对象。

## 当前实际读取

| 场景 | 实际读取顺序 | 结论 |
|---|---|---|
| R1 Greenfield Prototype Qualification 与 Profile | SKILL.md → 01-qualification.md → execution-profile.md → schema:execution-profile.yaml → gates.md | PASS |
| R2 已有系统 Validation Only + 离线评测设计审查 | SKILL.md → execution-profile.md → executor.md → 06-validation-iteration.md → 10-evaluation-and-quality.md → execution-plan.md | PASS |
| R3 目标和范围不变的 Local Replan | SKILL.md → execution-profile.md → replan-recovery.md → planner.md → registry-versioning.md | PASS |

R2 按新增路由读取评测 playbook；额外读取 Profile 用于确认已给 Profile 的复用和依赖闭包，Plan Preview 模板用于本轮计划沟通。R3 额外读取 Profile，用于确认目标与范围未变，因此不触发 Profile Replan。三者都没有展开无关 lifecycle/runtime/capability 目录。

Kernel 使用最多 60 行的确定性行块读取。runner 按当前行数给出全部分段命令；grader 逐块与当前文件比较，只有连续覆盖全文时才登记一次完整读取，缺段仍为 FAIL。首次 R1 因 120 行块的工具输出缺失部分内容失败；R2/R3 曾因受测 Agent 误判最后分段而漏读，修复 runner 后使用全新目录重测。R2 另一次运行把新 eval playbook 作为未登记的合理读取产生 WARN，随后把场景明确为评测设计审查并纳入 required。只有最终三次 PASS 进入 accepted manifest。

## 回放

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase1*.py"
python -B -X utf8 tests/ai-product-development/routing/verify_evidence.py
```

Routing smoke tests 只证明三个有限任务的 progressive disclosure。Profile/Plan 行为由 Phase 2 八场景验证，跨会话连续执行由 Phase 3 Golden MVP 验证。
