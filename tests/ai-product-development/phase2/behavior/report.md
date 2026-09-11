# Phase 2 行为验证报告

验证日期：2026-09-11（Asia/Shanghai）。生命周期节点合同和 Kernel 变化后，B1–B8 均使用当前 Skill 哈希重新执行。

## 结论

B1–B8 均为 **PASS**。每个场景使用新的临时 Skill 副本、独立 ephemeral Codex 会话和 read-only 沙箱。PASS 依据实际文件读取、原始工具输出和确定性 Profile/Plan validator；模型自述不作为读取证据。八个场景均无必要模块漏读、无未解释额外读取、无 lifecycle/runtime eager loading，临时 Skill 前后哈希不变。

[accepted-runs.json](accepted-runs.json) 固定 prompt、trace、stderr、metadata 和 result 五类文件哈希。[verify_behavior.py](verify_behavior.py) 核对当前 Skill 哈希、八个独立会话、只读参数和 prompt，并从原始 trace 重新运行 routing 与业务 grader。

## 最终 trace

| 场景 | 完整读取数 | 合法支持读取 | 结果 |
|---|---:|---|---|
| B1 Greenfield Prototype | 8 | gates.md | PASS |
| B2 Existing Repository Modification | 11 | gates.md、cli.py、loader.py、validators.py | PASS |
| B3 Partial Assignment | 10 | gates.md、cli.py、validators.py | PASS |
| B4 RAG Evaluation Only | 10 | gates.md、cli.py、validators.py | PASS |
| B5 Agent Not Required | 9 | gates.md、cli.py | PASS |
| B6 Enterprise Release | 9 | cli.py | PASS |
| B7 Requirement Change Replan | 13 | 01-qualification.md、gates.md、cli.py、loader.py、validators.py | PASS |
| B8 Existing Reusable Assets | 10 | gates.md、cli.py | PASS |

合法 dependency closure 不计为 routing failure。每个场景的完整读取顺序、命令、额外读取理由和 normalized result 位于相应 `result.json`。

B2 首次运行已完成路由，但生成的 Profile 没有使用 validator 要求的精确 `Evaluation Design` capability，且期间发生多次网络超时，因此行为判定 FAIL。未修改或放宽规则；B2 使用新目录重新独立执行后通过，只有通过版本进入 accepted manifest。

## 回放

```sh
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase2*.py"
python -B -X utf8 tests/ai-product-development/phase2/behavior/verify_behavior.py
```

回放不调用模型，也不能代替未来 Skill、场景、prompt 或 grader 变化后的真实重跑。
