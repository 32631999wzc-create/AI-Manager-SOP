# Phase 5 收尾与真实使用就绪判断

日期：2026-09-16。所有模型运行均为隔离、只读、ephemeral；三项开放任务使用代表性材料，不是线上客户项目或生产操作。原始 prompt、trace、stderr、metadata 和交付物保存在各证据目录。以下 PASS 只对应列出的边界，不表示“100% 稳定”。

## 1. Replan 四边界

[Replan 续验记录](replan-stability-review.md)保留 D-v1 单字段失败及修复过程。A `INITIAL_PLAN`、B `LOCAL_REPLAN`、C `CONTINUE`、D-v2 `PROFILE_REPLAN` 均获得独立 forward PASS。D-v2 同时满足 `SCOPE_CHANGE`、受影响范围最小和 `reopen_trigger=null`。Replan 核心合同在这四个边界上冻结，不再为微小表述差异做采样。

## 2. Capability Routing 四边界

| 边界 | 证据 | 结论 |
|---|---|---|
| gap + 无证据 → `EXECUTE` | [E trace](evidence/Capability-E-v1/trace.jsonl) | PASS |
| gap + 未验证资产 → `VERIFY` | [V trace](evidence/Capability-V-v1/trace.jsonl)、[透明重判读](evidence/Capability-V-v1/regraded-result.json) | PASS；原判定器把合理的“需求评审”误限为“产品需求定义”，原失败文件保留 |
| gap + 已验证证据 → `REUSE` | [R-v1 失败](evidence/Capability-R-v1/trace.jsonl)、[R-v2 trace](evidence/Capability-R-v2/trace.jsonl) | PASS；Planner 已澄清“待解锁决策”与“需要重做分析”不同 |
| 无 gap → 不激活 | [N trace](evidence/Capability-N-v1/trace.jsonl) | PASS |

这证明代表性路由机制能作四种区分；不等于 16 个专业 Capability 的方法质量都被逐项验证。E/V 产生于 REUSE 澄清前的 Skill 快照，R-v2/N 使用澄清后的快照；未为了统一 hash 重复已不受该窄修改影响的样本。

## 3. 三项开放式 PM 工作任务

| 任务与交付物 | 关键工作有无遗漏 | 无意义工作 | 资深 PM 可接手性 |
|---|---|---|---|
| [Greenfield](evidence/Real-greenfield-v1/deliverable.md) | 用户取证、产品定义、AI fit、人工核对、数据权利、评测与 Gate 均覆盖；六份记录未实际提供被明确标为缺证据 | 未默认引入 Agent/RAG/集成；八周计划在请求范围内 | **可接手**；指标数值均注明待 owner 确认 |
| [Existing product](evidence/Real-existing-v1/deliverable.md) | 实际读取 [README/代码/样例 trace](evidence/Real-existing-v1/trace.jsonl)，识别来源筛选与来源感知判定之差，并列实施依赖/回归 | 有范围扩张：多主题、证据 URL 不是本次来源规则需求的必要前提 | **有条件可接手**；先由 PM 删去或另行批准这些扩展 |
| [Production issue](evidence/Real-production-v1/deliverable.md) | 97% 新证据命中 D-P1 重开条件，人工降级、Release BLOCK、诊断、回归与最小 Replan 均覆盖；根因保持未知 | 未重做常规 Discovery/竞品/路线图 | **有条件可接手**；修复方案和验收集未定时把 Build Readiness 写成 `PASS_WITH_ASSUMPTIONS` 偏乐观，应由 Gate owner 改为/保持 `BLOCKED` 直至方案和数据就绪 |

审阅结论：没有发现三项任务都漏掉同一关键生命周期环节；但真实使用仍需要人审范围与 Gate。不能把这些代表性 dry-run 当成真实用户价值、模型质量或生产安全的实证。

## 4. 失败可见且可恢复

| 情况 | 最小证据 | 结果 |
|---|---|---|
| 缺关键发布输入 | `test_missing_monitoring_evidence_blocks_release_without_state_change` | Release Readiness `BLOCKED`，无 READY 任务，计划不变 |
| 模型超时 | [1 秒超时负例](evidence/Timeout-smoke-v1/result.json) | `INFRA_BLOCKED`，含 `MODEL_TIMEOUT`，未伪装成功 |
| 输出违约 | [D-v1 结果](evidence/Replan-D-v1/result.json) | `CONTRACT_FAIL`，完整 trace 与错误字段保留 |
| 任务失败 | `test_task_failure_replans_only_affected_work_and_rejects_bad_change` | 非法 Replan 被拒且旧状态不变；合法 `TASK_FAILURE` 仅 OUTDATE 失败任务、ADD 替代任务，保留无关任务 |

Runtime 的状态完整性仅由这些最小样本支持，不等于已证明所有进程崩溃点都具备事务级恢复。

本轮直接相关的静态/单元检查：Skill 结构验证 PASS（295 行 Kernel、8 Lifecycle、6 Runtime、259 链接），`skill-creator` 入口检查 PASS，Phase 5 Runtime 4 项单元测试 PASS。未运行 Phase 1–4 或全场景回归。

同步前复核发现：旧 Routing 与 Phase 2 的 accepted-trace 清单仍绑定旧 Skill hash；其只读 verifier 对当前版本均报“Accepted trace is for another Skill version”。这些保留为历史证据，**不得当作当前版本的验收 PASS**。本轮未伪改 hash，也未为推送而批量重采样；这是进入真实使用时应知晓的验证债务。

2026-09-17 P0 补注：Phase 3 Golden 的 G1–G4 也绑定旧 Skill 文件清单；本页其他 PASS 均只对各自运行时的场景与版本成立。当前版本与 PRD 定向证据的适用范围见 [P0 证据状态报告](../evidence-status-p0.md)。

## 5. 进入真实使用的边界

[Usage Boundary](../../../docs/usage-boundary.md)已明确适用任务、人工确认、证据质量以及 LIGHT/实验性范围。建议停止 Phase 5 式的细粒度采样，在有 PM owner 审阅、真实证据与明确授权的项目中使用；遇到新的可复现失败再做局部修复。当前不应宣称无人值守生产可用或完美运行。
