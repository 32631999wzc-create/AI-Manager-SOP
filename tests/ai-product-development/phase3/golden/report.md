# Phase 3 Golden MVP 验证报告

状态：PASS（2026-09-10）。验收采用 `evidence/G-final`，哈希固定在 `accepted-run.json`，由 `verify_golden.py` 回放。

## 最终证据

| 场景 | 独立 thread | 结果 | 关键行为 |
|---|---|---|---|
| G1 init | `01a08b7a-4fd9-78a0-9aab-5c86fadeb10f` | PASS | 读取 Kernel/Runtime，init、next、checkpoint |
| G2 resume/build | `01a08b7d-0f2d-7932-83c1-bc993cb3d6b3` | PASS | 新会话 resume，运行产品，登记 Record/Artifact，推进任务 |
| G3 local replan | `01a08b81-9727-7bc3-8d19-bf82509f9725` | PASS | 新会话 resume，INPUT_CHANGE，计划 v2，筛选报告，checkpoint |
| G4 resume/complete | `01a08b86-72f3-77b2-ae47-8250c90cc455` | PASS | 新会话 resume，验证输出，更新 Profile，complete=true |

四个场景均以实际成功的独立 `Get-Content` 和命令调用作为证据。模型最终说明不参与 PASS 的充分性判断。场景只读取当前 dependency closure，没有批量加载全部 lifecycle/runtime references。

最终产品状态：

- Plan `v2`，Snapshot sequence `4`。
- T1、T2、T4、T5 为 `COMPLETED`；被变更替代的 T3 为 `CANCELLED`。
- `design-v1`、`report-v1`、`filtered-v1` 均为 `ACTIVE`，位置存在。
- 基础输出接收 5 条、得到 4 条唯一反馈和 1 条重复；来源筛选输出仅含 2 条 support 反馈。
- REQUIRED 节点、Task、Gate、必需 Artifact 和阻塞项检查全部满足，`complete=true`。

## 失败与修复

验收前的未采用运行不提交原始 trace，只保留以下诊断：

1. G2 网络流超时，在 Kernel 读取后终止；未发生产品写入。
2. G1 暴露相对 `--input` 按 shell 目录解析的问题；修复为相对于 `--root`，增加跨进程回归。
3. G2 完成命令但漏读 Context；明确各阶段合法 dependency closure。
4. G2 提前运行验证器时，fixture 错误要求未来筛选输出；改为只验证当期存在的输出。
5. G3 的取消任务仍声明已移除依赖；清空依赖并增加启动前 plan validator 预检。
6. G2 执行产品和状态更新但未调用 `resume`；Prompt 明确新会话第一条状态命令，Runner 增加阶段前状态恢复重试。

这些问题均修复后使用全新会话和最终目录重测。`G-final` 未触发内部重试，`failed_attempts` 为空。

## 回放

```sh
python -B -X utf8 tests/ai-product-development/phase3/golden/verify_golden.py
```

回放检查当前 Skill 哈希、证据文件哈希、四个独立 thread、必要读取、必要命令、Runtime 完整性、最终状态和 Golden 产品输出。
