# Phase 5 Replan 稳定性规划审查与最小验证记录

日期：2026-09-16

## 审查结论

原规划的核心判断正确：Replan 必须建立在既有 baseline 之上，并同时具备 baseline 之后发生的变化事件与可识别的实质影响；运行模式应区分 `INITIAL_PLAN`、`CONTINUE`、`LOCAL_REPLAN` 与 `PROFILE_REPLAN`。本轮按此方向修复，不新增 Manager、状态机或平行 Runtime API。

以下表述需要修正：

1. Phase 3 的 `EvidenceRecord`、`DecisionRecord` 与 Registry 接入已经存在，不属于后续待建设项。
2. “从结构上不可能误入 Replan”只适用于持久化 Runtime 能校验既有状态的路径；纯提示词调用仍依赖 Skill Contract，并必须由独立 forward trace 验证，不能宣称绝对确定性。
3. 当前问题不要求新增 `execution_context` schema，也不要求修改 Plan/Runtime API。应先在 Planner 的 canonical contract 中统一 Replan 前置条件，再由 Replan reference 承接局部或 Profile 级恢复。
4. 稳定性结论以新鲜、独立的最小边界用例为准；单次 PASS 证明该样本满足合同，不等于统计意义上的“100% 稳定”或“完美运行”。

## 已实施修复

- Planner 增加 canonical `Replan Trigger Contract`，明确 baseline、post-baseline change event 与 material impact 三项判定。
- Planner 明确四种互斥运行模式；`INITIAL_PLAN` 与 `CONTINUE` 禁止加载 Replan reference，并要求 change、reopen 与 actions 为空。
- Capability 触发改为同时依据明确 gap、待做决策与证据状态；“通常需要”不能单独触发 Capability。
- Replan recovery 增加加载前置条件；初始请求、初始上下文、初始证据、当前刚生成的 Profile/Plan 不得伪装成 `INPUT_CHANGE`。
- Kernel Router 只允许 `LOCAL_REPLAN` 与 `PROFILE_REPLAN` 加载 Replan reference。
- 最小验证器固定四个边界用例，并校验输出模式、变更类型、受影响动作、reopen 与实际读取 trace。

## 最小链路结果

| 用例 | 边界 | 结果 | 实际证据 |
|---|---|---|---|
| A | 无 baseline 的首次规划 | PASS | 输出 `INITIAL_PLAN`，未触发 Replan，未读取 Replan reference |
| B | baseline 后发生有实质影响的局部输入变化 | PASS | 输出 `LOCAL_REPLAN`，仅调整受影响任务 |
| C | baseline 后出现新信息但无实质影响 | PASS | [独立 forward trace](evidence/Replan-C-v1/trace.jsonl)：`CONTINUE`、Replan 关闭、change/reopen 为空、actions 为空，未读取 Replan reference |
| D | baseline 后目标、范围或主要约束变化 | PASS（修复后） | [D-v1 失败 trace](evidence/Replan-D-v1/trace.jsonl) 仅错 `reopen_trigger`；canonical 单字段澄清后，[D-v2 独立 trace](evidence/Replan-D-v2/trace.jsonl) 输出 `PROFILE_REPLAN`、`SCOPE_CHANGE`、最小动作及 `reopen_trigger=null` |

静态最小检查已通过：结构验证 PASS；Phase 5 单元测试 2 项 PASS。未运行 Phase 1—4 或全链路回归。

## 测试基础设施定位与修复

上次中断点是测试驱动补丁应用：Windows 沙箱的 `setup refresh had errors` 导致补丁辅助进程无法创建，故补丁没有落盘，C/D 没有启动。这是宿主执行器故障，不是 Skill 行为失败；本轮使用受控执行恢复了测试。仓库内不能修复宿主沙箱，但测试驱动现已将子进程启动失败、非零退出、超时、trace 无效/不完整、结果缺失与 Skill 副本变动统一归类为 `INFRA_BLOCKED`；完整运行的业务违例归类为 `CONTRACT_FAIL`。默认超时从 600 秒调至 900 秒，原始 trace、stderr、metadata 与结果分别保存。一次故意使用不存在的 CLI 的无模型负例返回 `INFRA_BLOCKED`，包含 `PROCESS_START_FAILED`、`TRACE_INCOMPLETE` 和 `RESULT_MISSING`，没有被记为合同失败。

## 初次结论与后续闭环

D-v1 是有完整 forward evidence 的 `CONTRACT_FAIL`，而非基础设施阻断。其唯一差异是 `SCOPE_CHANGE` 携带了非空 `reopen_trigger`。用户随后明确要求修掉该单字段问题；因此在 [canonical 规则](../../../skills/ai-product-development/references/runtime/replan-recovery.md#decision-reopen-trigger) 将判定改为“本次 change type 不是 `DECISION_CHANGE` 时一律为 `null`”，其余 Replan 规则保持不变。D-v2 独立复验 PASS。A/B/C/D 四个核心边界现均有独立 forward PASS；这是边界验收，不是统计上的“100% 稳定”。后续 Capability Routing 与真实任务审阅结果另见 [真实使用就绪报告](real-use-readiness.md)。
