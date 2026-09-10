# Phase 2 行为验证报告

验证日期：2026-09-10（Asia/Shanghai）。范围为 Executable Validation；未执行产品构建、持久化或 Golden MVP。

## 结论

B1–B8 均为 **PASS**。每个场景使用新的临时 Skill 副本、独立 `codex exec --ephemeral --ignore-user-config` 会话和 read-only 沙箱。PASS 依据成功的单文件读取命令、原始工具输出及确定性 Profile / Plan validator；模型自述不作为读取证据。八个场景均无必要模块漏读、无未解释额外读取、无 lifecycle/runtime eager loading，临时 Skill 前后哈希不变。

[accepted-runs.json](accepted-runs.json) 固定 prompt、trace、stderr、metadata 和 result 五类文件哈希。[verify_behavior.py](verify_behavior.py) 会核对当前 Skill 哈希、八个独立 thread/workspace、只读参数、prompt 漂移，并从原始 trace 重新运行 routing 与业务 grader。

## 最终 trace

| 场景 | 读取数 | 实际读取顺序 | 结果 |
|---|---:|---|---|
| B1 Greenfield Prototype | 9 | Kernel → Profile → Qualification → Planner → Profile/Plan/Task schema → Gates → validator CLI | PASS |
| B2 Existing Repository Modification | 10 | Kernel → Qualification → Profile → Planner → Gates → 三个 schema → validator CLI/implementation | PASS |
| B3 Partial Assignment | 9 | Kernel → Profile → Qualification → Planner → 三个 schema → Gates → validator CLI | PASS |
| B4 RAG Evaluation Only | 10 | Kernel → Profile → Qualification → Planner → 三个 schema → Gates → Solution Design → Validation | PASS |
| B5 Agent Not Required | 8 | Kernel → Profile → Qualification → Profile schema → Planner → Task/Plan schema → Gates | PASS |
| B6 Enterprise Release | 9 | Kernel → Profile → Profile schema → Planner → Plan/Task schema → Gates → Qualification → validator CLI | PASS |
| B7 Requirement Change / Local Replan | 11 | Kernel → Profile → Profile schema → Qualification → Planner → Plan/Task schema → Replan → Gates → Registry → validator CLI | PASS |
| B8 Existing Reusable Assets | 10 | Kernel → Planner → 三个 schema → Profile → Qualification → Context → Gates → validator CLI | PASS |

每个场景的完整路径、item id、命令、额外读取理由和 normalized result 位于对应 [evidence](evidence) 目录的 `result.json`。支持读取包括局部 Gate 解释、validator 接口核对、受影响 lifecycle 规则和计划格式确认；均为少量、有场景依据的读取。B7 的 Qualification 用于确认目标与范围未变。合法 dependency closure 没有被计作 routing failure。

## 初始失败与修复

失败 trace 不作为验收证据，清洗后不提交；原因和修复保留如下：

- 多次 Codex 响应超时或额度耗尽，导致没有最终 JSON。这些运行保持 FAIL，额度恢复后使用新目录重测。
- 草稿使用只读 validator 返回 1，或错误地把 `-` 当文件路径返回 2。判定器现将明确的本地只读 validator 调用记录为辅助检查及退出码；它们不提供读取证据，其他失败命令仍导致 FAIL。
- Evaluation Design 最初只接受英文字面标签。原 canonical 规则同时定义五个组成项，仓库文档又以中文为主；validator 现接受英文字面标签、中文“评估设计”或五个必需组成项全集。监控计划同样识别 `monitor` 与“监控”。
- B3 把“设计评估标准”误解为“执行实际验证”；固定输入明确实际验证不在范围。B7 最初把 local replan 与 Enterprise 目标变体放入同一 envelope；自动场景现只测目标和范围不变的基础变更。
- 部分 supporting node 的 LIGHT/REQUIRED 和 B8 的 BROWNFIELD/HYBRID 都是原规则允许的裁量。fixture 保留一个 canonical 示例，行为断言只锁定人工契约强制的主节点、范围外节点和风险底线。
- B8 首次漏读 Context 且错误否认现有仓库修改。场景明确需要在现有仓库中先构造复用资产上下文，随后独立重测通过。

## 回放

```sh
python -B -X utf8 tests/ai-product-development/phase2/behavior/verify_behavior.py
```

回放不调用模型。它不能替代未来模型版本上的重新运行；Router、Skill 内容、场景或判定逻辑发生实质变化时，需用新目录重跑并重新审阅。
