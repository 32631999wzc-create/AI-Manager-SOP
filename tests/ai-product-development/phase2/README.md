# Phase 2 Executable Validation

固定场景输入位于 `fixtures/scenarios/`，结构化断言位于 `fixtures/expected/`。`negative-cases.json` 只描述对正例的确定性变更及预期错误码，测试不会修改仓库 fixture。

验证包装层不是新的项目状态 schema：

- `profile` 包含 `delivery_target`、`project_mode`、canonical `AssignmentScope`、八个 canonical `NodeProfile`，以及只供交叉校验的 `validation_context`。
- `plan` 包含 canonical `Plan`，以及只供 READY 判断的 `available_inputs`、`artifacts`、`gates`、`blocked_inputs` 和只供并行写冲突判断的 `write_targets`。
- `Plan.dependencies` 的 fixture 记录使用 `{from, to, type}`；`Task.dependencies` 保留对应的来源 ID。该表示只让原有依赖规则可确定性检查，不修改 canonical YAML 文件。

运行确定性验证：

```sh
python -B -X utf8 skills/ai-product-development/scripts/validate_runtime.py combined tests/ai-product-development/phase2/fixtures/scenarios/01-greenfield-prototype.yaml
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase2*.py"
```

CLI 成功返回 0，规则不满足返回 1，文档无法读取返回 2。输出始终为 JSON，错误包含稳定的 `code`、`path` 和 `message`。验证器只读输入，不保存或修复状态。

行为回归分别启动八个独立、只读、ephemeral Codex 场景。运行单个场景时必须使用新目录：

```sh
python -B -X utf8 tests/ai-product-development/phase2/behavior/run_behavior.py --scenario B1 --output tests/ai-product-development/phase2/behavior/evidence/B1-new
```

最终验收证据和失败修复说明见 [行为报告](behavior/report.md)。回放八个最终 trace：

```sh
python -B -X utf8 tests/ai-product-development/phase2/behavior/verify_behavior.py
```

PASS 必须有实际成功读取证据，并通过确定性 Profile / Plan validator。少量依赖确认、导航、Gate、模板或 validator 接口读取可作为支持模块；必要模块漏读、未解释额外读取、eager loading、失败 turn、可写 sandbox 或无最终结构化结果均不能通过。
