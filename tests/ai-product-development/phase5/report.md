# Phase 5 End-to-End Validation Report

> 阅读提示（2026-09-17）：下文按日期保留当时的验证过程与结论；其中的“当前”只指相应运行时的 Skill 版本，不构成 2026-09-17 工作区的全链路 PASS。当前版本、历史证据与 PRD 定向证据的适用范围见 [P0 证据状态报告](../evidence-status-p0.md)。

日期：2026-09-15

## 结论

Phase 5 已完成三类初始验证，并针对 E1/E2 失败做了最小定位、定点修复和最小链路复验。已确认的 Skill 规则缺陷均已修复；当前严格证据状态仍不是三场景全部 PASS，因为两次最终复验分别受到 trace 丢行和模型服务超时影响。未把基础设施失败改写为行为 PASS。

本轮没有重跑 E3、Phase 1–4 或全链路行为测试，没有产品写入、外部操作或 GitHub 推送。

## 2026-09-16 最小链路补证

为验证不稳定项和缺失证据，新增 `run_targeted_repair.py`，没有重跑完整 E2E：

| 断点 | 证据 | Routing | 行为 | 结论 |
|---|---|---:|---:|---|
| E1 Profile / Capability / no-Replan | `evidence/E1-targeted-v1/` | PASS | FAIL | 不稳定仍存在 |
| E2 Product Definition / Profile / Replan | `evidence/E2-targeted-v1/` | PASS | PASS | 缺失证据已补齐 |

E1 已稳定输出 `PARTIAL_PROJECT`、exact `Evaluation Design`，且没有误触发 Responsible AI；但仍把无变化的 Greenfield 初始规划误判为 `INPUT_CHANGE Replan`，Capability 集合和 Discovery mode 也不稳定。因此 Skill 仍不能声明完美运行。

E2 已稳定输出 `PARTIAL_PROJECT`、exact `Evaluation Design`、`INPUT_CHANGE`、`reopen_trigger: null` 和精确的五项最小 Replan。当前先新增 `T-TAXONOMY-IMPACT`，再根据影响决定是否执行 Product Requirements；不在影响尚未形成证据时强迫调用 PRD。

## 定点修复

1. 在 `schemas/execution-profile.yaml` 将 `Evaluation Design` 的 canonical Profile 名称约束放到 `active_capabilities` 对象定义旁。
2. 在 Execution Profile 明确：只负责规划/评估且不负责后续执行时为 `PARTIAL_PROJECT`，不能因计划覆盖全项目而标成 FULL。
3. 在 Product Definition 路由明确：输入变化使 scope、success measures 或 acceptance criteria 失效时，必须触发 `Product Requirements`。
4. 在 Replan 规则明确：只有 `DECISION_CHANGE` 可携带 `reopen_trigger`；其他 change type 未命中既有决策触发条件时必须为 `null`。可执行 runtime 已有同样约束，无需改代码。
5. 在 Qualification 明确：已排除敏感、高影响、外部工具和自动行动且无相反证据时，不为重述边界调用 Responsible AI。
6. 在 Kernel 明确：SKIP 节点不为“确认 SKIP”预读 reference；只有 `Replan.required=true` 或实际调整任务时加载 Replan 规则。

## 最小复验结果

| 场景 | 证据 | Skill hash | Routing | Behavior / Objects | 结论 |
|---|---|---:|---:|---:|---|
| Greenfield | `evidence/E1-v7/` | 当前 | FAIL | PASS | 业务修复通过；一次 `execution-profile.md` 分块输出发生工具级丢行，严格 routing 证据不通过 |
| Existing change | `evidence/E2-v3/` | 当前 | PASS | 未返回 | 所有必要文件完整读取、无额外读取；模型服务 900 秒超时，未生成 JSON |
| Production risk | `evidence/E3-v2/` | 修复前 | PASS | PASS | 本轮改动未涉及其业务链，依用户要求未重跑 |

### E1 已验证行为

- `PARTIAL_PROJECT`：PASS；
- Solution Design 使用 exact `Evaluation Design`：PASS；
- Discovery、Product Requirements、AI Feasibility、Data Strategy、Human-AI、Evaluation 均对应当前真实 gap：PASS；
- Responsible AI 不再误触发：PASS；
- 无 Replan 的业务输出：PASS；
- 唯一未通过项是工具 trace 未完整回传一次成功读取的中间行，不是输出行为或对象错误。

### E2 已验证范围

- Qualification、Product Definition、Solution Design、Implementation、Validation、Release、Execution Profile、Gate、Replan 及两个 schema 均完整读取：PASS；
- 无无关文件或 Capability 读取：PASS；
- 因模型服务连续超时且最终没有 agent JSON，无法验证 Product Requirements 输出和 `reopen_trigger=null`；按停止条件不再盲重跑。

## 最小确定性验证

最终改动后只运行：

- structure validator：PASS（295 kernel lines、8 lifecycle nodes、6 runtime capabilities、235 links）；
- Phase 5 runtime tests：2 tests PASS；
- `verify_e2e.py`：E1 behavior/object 无问题但 routing trace FAIL；E2 routing PASS 但结果 JSON 缺失。

未运行 Phase 1、Phase 2、Phase 3、Phase 4 或 E3 全链路回归。若需要把 Phase 5 总状态改为 PASS，只需在模型服务稳定后分别生成一份新的 E1 完整 trace 和一份 E2 JSON 结果；不需要重跑 E3 或其他阶段。

## 2026-09-16 Replan 最小边界续验

上文记录的是当时的 E1/E2/E3 全场景状态，不代表后续 Replan 边界已验收。最新针对性记录见 [Replan 稳定性审查与最小验证](replan-stability-review.md)：A/B/C 为 `PASS`，D 为有完整 trace 的 `CONTRACT_FAIL`（`SCOPE_CHANGE` 错带非空 `reopen_trigger`）。测试驱动现区分 `PASS`、`CONTRACT_FAIL`、`INFRA_BLOCKED`；宿主沙箱 `setup refresh had errors` 不能由仓库脚本修复，不能记为 Skill 失败。Replan Contract 尚不能冻结；按优先级暂不进入 Capability Routing 四边界或 Evidence → Decision → Replan 验证，也未重跑全链路。

## 最终续验入口

上述 D 失败状态为修复前快照。后续已完成 D-v2 单次独立 PASS、Capability Routing 四边界、三项开放式工作任务及四类失败可见性检查；具体证据、仍需人审的问题和使用判断见 [Phase 5 收尾与真实使用就绪判断](real-use-readiness.md)。未把早期 E1/E2 严格全场景失败追改为 PASS，也未宣称统计意义上的绝对稳定。
