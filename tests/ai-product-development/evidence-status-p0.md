# P0 证据状态收敛与操作过程报告

日期：2026-09-17（Asia/Shanghai）。范围仅为证据版本、历史 PASS 适用性及一份跨行业 PRD 定向 trace；**没有修改 Skill 规则、验收器或原始证据，没有重跑全链路，也没有推送 GitHub**。

## 结论与版本口径

当前本地工作区的 Skill 文件清单包含 95 个文件，清单指纹为 `2393f96dd900e71c1df1e22c46ac94aee7bdae4dffe424094ec702d74a6c7666`。这是包含尚未提交的 PRD 节点修改及新增 reference/template 的**本地工作区版本**，不等同于远程仓库版本。

指纹计算口径：沿用 `routing/run_routing.py` 的 `inventory(root)`（每个 Skill 文件的 SHA-256），将所得 `相对路径 → 文件哈希` 映射按键排序，以紧凑 JSON 序列化，再取 SHA-256。原始 `metadata.json` 保存完整清单；本报告只展示其摘要，不能用摘要代替原始证据。文件变动后必须重新比较完整清单，不能沿用本报告的“当前”称谓。

| 证据组 | 采样时 Skill 清单指纹 | 本地当前适用性 | 处理 |
|---|---|---|---|
| [Routing R1–R3](routing/accepted-runs.json) | `8ad979e236d1a810c6b6dfb01127f1236dd6fa0484e38f5c818560db06c777ec`，51 文件 | 不匹配 | 保留采样版本的历史 PASS；不声称当前 Routing PASS |
| [Phase 2 B1–B8](phase2/behavior/accepted-runs.json) | `c3d51e0394dd9d8dd86e4b48dfab4ce0cd50eac5db475a994d7f896d03e9f5ec`，35 文件 | 不匹配 | 保留采样版本的历史 PASS；不声称当前行为 PASS |
| [Phase 3 G1–G4](phase3/golden/accepted-run.json) | `c3d51e0394dd9d8dd86e4b48dfab4ce0cd50eac5db475a994d7f896d03e9f5ec`，35 文件 | 不匹配 | 保留采样版本的历史 PASS；不声称当前 Golden PASS |
| [PRD-cross-industry-v2](phase5/evidence/PRD-cross-industry-v2/metadata.json) | `2393f96dd900e71c1df1e22c46ac94aee7bdae4dffe424094ec702d74a6c7666`，95 文件 | 完整清单匹配 | 采纳为**当前 PRD 路由与草稿产出的定向运行证据**；内容质量仍为 `REVIEW_REQUIRED`，不是全 Skill PASS |

Phase 5 的其他场景是各自日期与输入下的历史观察，不自动升级成当前版本结论。旧 accepted manifest 和 raw trace 均未改写；版本不匹配是证据适用范围变化，不是把既有行为 PASS 重新判成 `CONTRACT_FAIL`，也不是 `INFRA_BLOCKED`。

## 当前 PRD trace 的采纳边界

仅采纳 [PRD-cross-industry-v2](phase5/evidence/PRD-cross-industry-v2/)；v1 不采纳。v2 原始记录包含一次独立 `thread.started` 与一次 `turn.completed`，进程退出码 0，`infra_issues=[]`，`metadata.status=REVIEW_REQUIRED`。三份必要文件——主 `SKILL.md`、`product-requirements/SKILL.md`、`references/prd-drafting.md`——均有退出码 0 的完整工具读取，输出正文可与当前文件内容核对；最终交付物与 trace 中最终消息一致。没有把模型自述当作读取证据。

该 trace 能证明：在一个电商客服内测任务上，当前本地版本触发了 PRD 节点、按需加载撰写方法，并产出包含 Why、What、How、范围、需求、失败、验收及人工阻塞的中文草稿。它**不能**证明跨行业泛化、其他 15 个 Capability、当前版全部 Routing/Phase 2/Golden 或可无人复核地直接发布 PRD。额外读取了执行计划模板、Responsible AI 与 Evaluation 节点；与 AI 客服质量/风险有关，但未据此宣称最少读取或无额外上下文成本。

人工复核保留两项问题：文档把“决策、假设与阻塞”放在 Why/What/How 之外的第四个一级章节，未完全遵守无指定模板时的三级一级结构；“回复必须可核对”被列为“已证实问题”，但输入给出的是已批准约束，并非访谈观察。两者不影响“成功调用并起草”的狭义结论，却阻止将内容质量标成无条件 PASS。产品/业务 owner 仍需确认质量阈值、数据保存期限与发布 Gate。

为防止后续修改原始证据而仍沿用本记录，采纳时五个文件的 SHA-256 固定如下：

| 文件 | SHA-256 |
|---|---|
| [prompt.txt](phase5/evidence/PRD-cross-industry-v2/prompt.txt) | `8b73c3a5c04c7635ce2283922a60e1201aa9c9326bcc796ae94b7f8696f0644e` |
| [trace.jsonl](phase5/evidence/PRD-cross-industry-v2/trace.jsonl) | `97632369d1904a161bbca794b9312f27856dcd444c24a00edf146ceb5618978f` |
| [stderr.txt](phase5/evidence/PRD-cross-industry-v2/stderr.txt) | `c6689cc8d2f914e095f9ef0be8d8d9cb8f44b196557068cd38ffed945c59bb53` |
| [metadata.json](phase5/evidence/PRD-cross-industry-v2/metadata.json) | `042e6ad4c71b50450f120b6d2ddfc2412acf409a85aa1ec705c0377c975fcf27` |
| [deliverable.md](phase5/evidence/PRD-cross-industry-v2/deliverable.md) | `7d1acfc52f647cfca509087e06a83aa6d5f6d26ac729c8a900bb01d8bf923cb5` |

## 操作过程

1. 阅读仓库 README、主 Skill 和现有 Routing、Phase 2、Phase 3、Phase 5 报告及 verifier，确认现行 verifier 用完整 Skill 文件清单匹配，而不是只看文档中的 PASS 字样。
2. 用既有 `inventory` 算法只读计算当前清单，与全部已采纳 R1–R3、B1–B8、G1–G4 的 `metadata.skill_sha256` 比对；各组内部指纹一致，但均与当前清单不同。
3. 核验 PRD-v2 的完整清单、原始 trace、必需模块的实际成功读取、交付物来源及五份证据文件哈希；人工检查草稿与节点合同，按上述有限范围采纳。
4. 在原有四份报告及真实使用结论页增加版本提示，保留当时的过程与 PASS，不修改 manifest、trace、metadata 或既有判定规则。
5. 本轮只需做文档链接、证据哈希和 `git diff --check` 的定向核验；不运行模型采样、Phase 1–5 回归或完整端到端测试。

执行环境曾对默认命令及直接补丁入口返回 `setup refresh had errors`；改用获准的命令执行环境和同一 Codex `apply_patch` 入口后完成读写。该错误属于本轮工具基础设施问题，不计为 Skill 合同失败，也未触发重复模型采样。`git diff --check` 未报空白错误；Git 仅提示部分既有文件的 LF/CRLF 工作区转换。

## 后续使用边界

现有历史 trace 可用于解释架构演进和当时验收，但不能直接证明当前 95 文件版本的整体稳定性。新 Skill 规则变动时，先确定影响范围，再按需做一份新的独立 forward trace；基础设施失败单列 `INFRA_BLOCKED`，合同失败单列 `CONTRACT_FAIL`，不得改写旧哈希或把 `REVIEW_REQUIRED` 自动提升为 PASS。P0 到此为止，不以版本漂移为由批量重采样。
