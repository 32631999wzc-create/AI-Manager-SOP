# Phase 1 验证报告

最新验证日期：2026-09-10（Asia/Shanghai）。P2 在 Kernel 增加 Executable Validation 路由后，R1–R3 已用当前 Skill 哈希重新验证。

## 结论

R1、R2、R3 均为 **PASS**。三个场景分别使用独立临时目录、ephemeral Codex 会话和 read-only 沙箱。必要模块均由成功的单文件完整读取命令证明；没有必要模块漏读、未解释额外读取或 lifecycle/runtime eager loading。模型自述不作为读取证据。

结构检查保持八个 lifecycle node、六项 runtime capability、三个顶层 Gate、八个原 YAML 对象、533 条源规则指纹与 70 个原始标题映射。Kernel 当前 244 行。迁移指纹证明内容保留，不把任意语义变更形式化为正确。

## 当前实际读取

| 场景 | 实际读取顺序 | 结论 |
|---|---|---|
| R1 Greenfield Qualification/Profile | Kernel → Qualification → Profile → Gates → Profile schema → validator launcher → CLI → loader → validators | PASS |
| R2 Existing Validation Only | Kernel → Profile → Validation & Iteration → Executor | PASS |
| R3 Local Replan | Kernel → Replan → Planner → Registry → Plan/Task/Project State schema | PASS |

R1 的四个 validator 文件来自 Kernel 新增的只读 Executable Validation 路由。它们用于入口及本地依赖确认，不属于生命周期或 Runtime 规则批量加载。首次重测因此被旧 support 表判为 WARN；逐项审阅确认必要读取完整且无 eager loading后，父判定器登记具体支持理由并从同一原始 trace 重放为 PASS。

R2 额外读取 Profile 用于确认给定 Profile 的复用与依赖闭包。R3 的三个 schema 分别核对计划版本/依赖、任务状态和产物版本。所有额外读取都有局部任务依据。

完整命令、读取路径、item id 和 dependency closure 见各自 [evidence](evidence) 目录的 `result.json`；[accepted-runs.json](accepted-runs.json) 固定五类证据哈希，[verify_evidence.py](verify_evidence.py) 核对当前 Skill 哈希、独立会话、只读参数和 trace 回放。

## 历史修复

Phase 1 初始实施时，R2 曾因机械展开无当前核验需要的 VERIFY 节点被判 WARN，R3 曾因漏读 Registry 被判 FAIL；修复 Router 后独立重测。P2 后旧哈希 evidence 已移除，只保留当前三组最终 PASS。此次新增 validator 导航没有改变八节点、六项 Runtime capability、Gate 或产品方法论语义。

## 回放

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p test_phase1.py
python -B -X utf8 tests/ai-product-development/routing/verify_evidence.py
```

Routing smoke tests 只证明三个有限任务的 progressive disclosure。完整 Profile/Plan 行为由 Phase 2 的八个独立场景验证；产品持续交付与 Golden MVP 仍不在 Phase 1/P2 证明范围内。
