# Phase 1 验证报告

最新验证日期：2026-09-11（Asia/Shanghai）。P3 在 Kernel 增加 Continuous Local Runtime 路由后，R1–R3 已用当前 Skill 哈希重新执行。

## 结论

R1、R2、R3 均为 **PASS**。三个场景分别使用独立临时目录、ephemeral Codex 会话和 read-only 沙箱。必要模块均由成功的实际文件读取证明；没有必要模块漏读、未解释额外读取或 lifecycle/runtime eager loading。模型自述不作为读取证据。

结构检查保持八个 lifecycle node、六项 runtime capability、三个顶层 Gate、原 canonical runtime objects 与迁移基线。Kernel 当前 250 行。

## 当前实际读取

| 场景 | 实际读取顺序 | 结论 |
|---|---|---|
| R1 Greenfield Qualification/Profile | Kernel → Profile schema → Qualification → Profile → Gates | PASS |
| R2 Existing Validation Only | Kernel → Executor → Validation & Iteration → Profile | PASS |
| R3 Local Replan | Kernel → Profile → Replan → Planner → Registry | PASS |

R2 的 Profile 用于确认已给 Profile 的复用和依赖闭包；R3 的 Profile 用于确认目标与范围未变，因此不触发 Profile Replan。这些支持读取有局部任务依据，没有展开无关 lifecycle/runtime 目录。

Kernel 超过部分工具调用的动态单次输出阈值后，运行器改为两个确定性行块读取。grader 逐块与当前文件内容比较，只在 `First 120` 与 `Skip 120` 连续覆盖全部行时登记一次 Kernel 完整读取；文件名导航不算内容加载。此前 R2 的漏读、输出截断与导航 WARN 均未进入 accepted manifest。

完整命令、读取路径、item id 和 dependency closure 见 [evidence](evidence) 中被 [accepted-runs.json](accepted-runs.json) 固定的目录。[verify_evidence.py](verify_evidence.py) 核对五类证据哈希、当前 Skill 哈希、独立会话、只读参数和原始 trace 回放。

## 回放

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase1*.py"
python -B -X utf8 tests/ai-product-development/routing/verify_evidence.py
```

Routing smoke tests 只证明三个有限任务的 progressive disclosure。Profile/Plan 行为由 Phase 2 的八个独立场景验证；跨会话连续执行与 Golden MVP 由 Phase 3 验收单独证明。
