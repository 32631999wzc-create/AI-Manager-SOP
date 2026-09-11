# Phase 3 Golden MVP 验证报告

状态：PASS（2026-09-11）。验收采用 `evidence/G-final`，哈希固定在 `accepted-run.json`，由 `verify_golden.py` 回放。

## 最终证据

| 场景 | 独立 thread | 结果 | 关键行为 |
|---|---|---|---|
| G1-init | `01a08ff7-246e-71d2-9909-578c00476640` | PASS | 初始化：必要读取与命令均完整 |
| G2-resume-build | `01a08ff9-c195-7bb0-978d-3d00d66e39f7` | PASS | 恢复与构建：必要读取与命令均完整 |
| G3-local-replan | `01a08ffe-2a5f-70a3-8fe1-e9d124933801` | PASS | 局部重规划：必要读取与命令均完整 |
| G4-resume-complete | `01a09002-2559-7dc0-acb0-bfea62e875e7` | PASS | 恢复与完成：必要读取与命令均完整 |

四个场景均以实际成功的独立文件读取和命令调用作为证据。模型最终说明不参与 PASS 的充分性判断。每个场景只读取当前 dependency closure，没有批量加载全部 lifecycle/runtime references。

最终产品状态：

- Plan `v2`，Snapshot sequence `4`；
- T1、T2、T4、T5 为 `COMPLETED`，被变更替代的 T3 为 `CANCELLED`；
- `design-v1`、`report-v1`、`filtered-v1` 均为 `ACTIVE` 且位置存在；
- 基础输出接收 5 条、得到 4 条唯一反馈和 1 条重复，来源筛选输出仅含 2 条 support 反馈；
- REQUIRED 节点、Task、Gate、必需 Artifact 和阻塞项全部满足，`complete=true`。

## 本轮未采用运行

使用较低推理配置的 `G-review-v1` 中，G1 与 G2 通过，但 G3 三次都在完成必要读取、`resume` 和 `replan` 后提前停止，未完成筛选执行、Task 更新、Artifact 提交和 checkpoint。没有放宽验收或修改业务规则；新目录 `G-review-v2` 重新建立完整四会话状态链并一次通过，`failed_attempts` 为空。未采用目录不进入 accepted manifest。

## 回放

```sh
python -B -X utf8 tests/ai-product-development/phase3/golden/verify_golden.py
```

回放检查当前 Skill 哈希、证据文件哈希、四个独立 thread、必要读取、必要命令、Runtime 完整性、最终状态和 Golden 产品输出。
