# Phase 1 Routing Test

验证 Kernel + Router 能引导选择性读取。三个场景不继承对话，输入包含当前窄任务所需原始材料。[scenarios.json](scenarios.json) 的 required/support/closure 只由父判定器使用，模型只接收 task，不接收必要模块答案表。

## 运行

依赖 Python 3.10+、已认证的 Codex CLI 和正常工作的 Windows 只读沙箱。本次最终证据使用 codex-cli 0.153.4。每次必须使用新输出目录，不覆盖历史记录：

```sh
python -B -X utf8 tests/ai-product-development/routing/run_routing.py --scenario R1 --output tests/ai-product-development/routing/evidence/R1-new
python -B -X utf8 tests/ai-product-development/routing/run_routing.py --scenario R2 --output tests/ai-product-development/routing/evidence/R2-new
python -B -X utf8 tests/ai-product-development/routing/run_routing.py --scenario R3 --output tests/ai-product-development/routing/evidence/R3-new
```

每次复制 Skill 到新临时目录，使用 `codex exec --json --ephemeral --ignore-user-config -s read-only`，显式设置 `windows.sandbox="elevated"`。不使用 resume、可写沙箱、ignore-rules 或绕过审批参数。父进程保存输入、stdout/stderr、CLI 版本、启动参数、Skill 哈希与退出状态。前后哈希是补充检查，不能替代 read-only 权限限制。测试结束后清理临时副本。模型配置使用 CLI 默认值，不推断 trace 未提供的模型标识。

## 判定依据

| 场景 | 活动任务 | 必要模块（相对 Skill） |
|---|---|---|
| R1 | 初始 Qualification、Gate 与八节点 Profile | Kernel、Qualification、execution-profile、gates、execution-profile.yaml |
| R2 | 已有系统给定结果的 Validation Only | Kernel、Validation & Iteration、executor |
| R3 | 不变范围下的局部 DAG 与产物版本建议 | Kernel、replan-recovery、planner、registry-versioning |

必要性来自 Kernel 当前操作路由：R1 构造 Profile 和判断 Gate；R2 执行验收核对；R3 调整依赖并判断正式产物失效与替代版本。schema、沟通模板及局部依赖确认可作为支持读取。

- **PASS**：成功工具输出证明必要模块完整读取；没有无依赖 eager loading；额外读取有任务、导航或局部规则依据。
- **WARN**：必要模块完整，少量额外读取理由未充分证明，或 trace 分类有限制；必须逐项审阅，不能忽略后宣布完成。
- **FAIL**：必要模块漏读；只有模型自述；无任务依赖地读取全部或近乎全部 lifecycle/runtime；或明显绕过 Router 批量读取详细规则。
- 合法 dependency closure 对应模块计入合理加载范围，不以最少文件数评判。
- 自动检查的“近乎全部”为一个类别全部或仅少一个模块，且存在未解释读取；人工仍须审查明显目录批量扫描，不能把阈值当免责线。

## 实际 trace

每个 evidence 子目录保存：

- `prompt.txt`：实际输入。
- `trace.jsonl`：原始事件，包含真实 command_execution、完整输出、退出码和顺序。
- `stderr.txt`：环境诊断。
- `metadata.json`：隔离参数、CLI 版本、文件哈希和退出结果。
- `result.json`：必要模块、实际文件与顺序、漏读、额外读取、依赖闭包和判定。

仅完成且退出码为 0 的单文件 `Get-Content -LiteralPath`，并且输出包含完整文件内容，才计作必要读取；支持相对/绝对 Windows 路径。失败或截断输出、目录列表均不计为完整读取；其他读法要求审阅，不能静默计 PASS。批量完整输出即使不是已支持的单文件命令，仍用于检测 eager loading。模型自述不提供读取证据。

runner 为此最小测试限定完整单文件读取，不要求 Skill 在实际任务中总是读完整文件。通用局部读取/多工具 trace 解析器不在本次范围；未知命令产生 WARN，必要内容无法确认产生 FAIL。运行时不覆盖输出目录；提交时只保留验收采用的 trace，失败原因和修复写入报告。

实际顺序、必要性、依赖闭包及判定见 [验证报告](report.md)。回放已保存的最终证据：

```sh
python -B -X utf8 tests/ai-product-development/routing/verify_evidence.py
```

回放检查当前 Skill 与原始证据哈希、三个独立 read-only 会话和判定结果，不产生新的模型执行。Routing Test 不替代八个人工产品行为场景或 Golden MVP。
