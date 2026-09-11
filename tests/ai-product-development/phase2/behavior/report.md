# Phase 2 行为验证报告

验证日期：2026-09-11（Asia/Shanghai）。P3 修改 Kernel 后，B1–B8 已使用当前 Skill 哈希重新执行；范围仍为 Executable Validation。

## 结论

B1–B8 均为 **PASS**。每个场景使用新的临时 Skill 副本、独立 `codex exec --ephemeral --ignore-user-config` 会话和 read-only 沙箱。PASS 依据成功的实际文件读取、原始工具输出及确定性 Profile/Plan validator；模型自述不作为读取证据。八个场景均无必要模块漏读、无未解释额外读取、无 lifecycle/runtime eager loading，临时 Skill 前后哈希不变。

[accepted-runs.json](accepted-runs.json) 固定 prompt、trace、stderr、metadata 和 result 五类文件哈希。[verify_behavior.py](verify_behavior.py) 会核对当前 Skill 哈希、八个独立 thread/workspace、只读参数、prompt 漂移，并从原始 trace 重新运行 routing 与业务 grader。

## 最终 trace

| 场景 | 读取数 | 主要读取闭包 | 结果 |
|---|---:|---|---|
| B1 Greenfield Prototype | 10 | Kernel、Qualification、Profile、Planner、Gates、三项 schema、validator | PASS |
| B2 Existing Repository Modification | 11 | Kernel、Qualification、Profile、Planner、Gates、三项 schema、validator dependencies | PASS |
| B3 Partial Assignment | 9 | Kernel、Qualification、Profile、Planner、Gates、三项 schema、validator CLI | PASS |
| B4 RAG Evaluation Only | 10 | Kernel、Qualification、Profile、Planner、Gates、四项 schema、Validation | PASS |
| B5 Agent Not Required | 9 | Kernel、Qualification、Profile、Planner、Gates、三项 schema、validator CLI | PASS |
| B6 Enterprise Release | 10 | Kernel、Qualification、Profile、Planner、Gates、三项 schema、validator | PASS |
| B7 Requirement Change / Local Replan | 11 | Kernel、Qualification、Profile、Planner、Replan、Registry、Gates、三项 schema、validator CLI | PASS |
| B8 Existing Reusable Assets | 10 | Kernel、Qualification、Profile、Planner、Context、Gates、三项 schema、validator CLI | PASS |

每个场景的完整读取顺序、item id、命令、额外读取理由和 normalized result 位于 accepted evidence 目录的 `result.json`。合法 dependency closure 没有被计作 routing failure。

Kernel 使用两个确定性行块读取，grader 只有在两块与当前文件逐行一致并连续覆盖全部内容时才承认 Kernel 已读。其他模块仍要求单文件完整输出。此次重跑中，低推理模型多次出现必要规则漏用或最终 JSON 截断；这些运行保留为失败原因记录但不进入 accepted manifest。复杂行为场景改用 `gpt-6-astra` medium 后重新独立执行，B4 的现有当前哈希运行已通过，无需重复。

## 回放

```sh
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase2*.py"
python -B -X utf8 tests/ai-product-development/phase2/behavior/verify_behavior.py
```

回放不调用模型，也不能替代未来 Skill、场景、prompt 或判定逻辑变更后的真实重跑。
