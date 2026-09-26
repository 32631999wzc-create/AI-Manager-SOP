# P1 触发边界、成本与产出评估：操作过程报告

日期：2026-09-17（Asia/Shanghai）。范围是上一轮二次审查的两个 P1 阶段：相邻 Capability 触发边界；三类真实任务的读取成本与资深 PM 产出 Rubric。未修改 Skill 业务规则，未运行 Phase 1–5 全链路回归，未推送 GitHub。

## 结论

四组相邻边界各测两侧，另测“无 gap”：九份独立、只读、ephemeral trace 的最终判读均符合预期；Planner 单任务与无 gap 均未激活 Professional Capability。三份已有开放式任务的成本与产出基线已记录，[轻量 Rubric](real-work-rubric.md)已建立。样本只证明这些边界，不证明 16 个 Capability 在所有行业中零误触发；既有真实任务的范围扩张和 Gate 偏乐观问题仍需 PM owner 审阅。

本轮当前本地 Skill 清单指纹为 `2393f96dd900e71c1df1e22c46ac94aee7bdae4dffe424094ec702d74a6c7666`（95 文件）。九份 metadata 的完整 `skill_sha256` 均与本地清单匹配；这是本地未提交版本，不等同于 GitHub 版本。原始 trace 不因重判读而改写。

## 1. 相邻触发边界

测试器为 [run_adjacent_routing.py](run_adjacent_routing.py)。每例只允许读取主 Skill 与 Planner，输出一项 Capability Need 或 `null`，不执行专业方法，不写产品状态。原始结果和透明重判结果均在对应证据目录。

| 边界 | 样例 → 实际主 Capability | 最终判读 | 证据 |
|---|---|---|---|
| PRD / 需求评审 | 已选机会、缺 PRD → Product Requirements | PASS（同 trace 重判） | [PRD trace](evidence/P1-adj-prd-v1/trace.jsonl)、[重判](evidence/P1-adj-prd-v1/regraded-result.json) |
| PRD / 需求评审 | 已批准 PRD、实质分歧 → Requirement Review | PASS（同 trace 重判） | [Review trace](evidence/P1-adj-review-v1/trace.jsonl)、[重判](evidence/P1-adj-review-v1/regraded-result.json) |
| Evaluation / Experimentation | 离线事实性与发布阈值 → Evaluation | PASS | [Eval trace](evidence/P1-adj-evaluation-v1/trace.jsonl) |
| Evaluation / Experimentation | 离线 eval 已过、真实采用/耗时未知 → Experimentation | PASS | [Experiment trace](evidence/P1-adj-experimentation-v1/trace.jsonl) |
| Roadmap / Planner | 跨三个版本的 outcome 切片 → Roadmap | PASS | [Roadmap trace](evidence/P1-adj-roadmap-v1/trace.jsonl) |
| Roadmap / Planner | 单个已定义 READY Task → 不激活专业 Capability | PASS（同 trace 重判） | [Planner trace](evidence/P1-adj-planner-v1/trace.jsonl)、[重判](evidence/P1-adj-planner-v1/regraded-result.json) |
| Production Learning / Retrospective | 线上七天新 bad-case，事件未结束 → Production Learning | PASS | [Production trace](evidence/P1-adj-production-v1/trace.jsonl) |
| Production Learning / Retrospective | Pilot 已结束，需对照原目标提炼学习 → Retrospective | PASS | [Retrospective trace](evidence/P1-adj-retrospective-v1/trace.jsonl) |
| 无 gap | 已批准计划，仅汇报状态 → 不激活 | PASS | [No-gap trace](evidence/P1-adj-no-gap-v1/trace.jsonl) |

PRD、Review 的原 `CONTRACT_FAIL` 来自测试器不接受正常英文能力别名，以及对成功的合并分段读取识别不足；两份完整原始输出已证明实际读到主 Skill 和 Planner。Planner 的原失败是测试器强制将已有 READY Task 等同于“尚未解锁生命周期 gap”，而本题真正要验的是“不误用 Roadmap”。修订后在原目录增加 `regraded-result.json`，保留原 `result.json`；没有再运行模型。无 gap 样例曾出现模型流断开并自动重试，最终进程成功、trace 完整、`infra_issues=[]`，未将短暂重试误判成 Skill 失败。

本轮边界测试本身也揭示成本问题：PRD、Evaluation、Experimentation 三份分段读取样例各消耗约 22–25 万 input tokens；后续改为两次完整原文读取后，单例约 4.9 万 input tokens。Review 样例虽同样使用分段命令，但执行者合并读取，约 5.1 万 input tokens。以上是 trace 的会话 input token 计数，不是单纯 Skill token，不能直接折算费用。后续只在相关路由规则改变或真实误路由出现时运行这组定向样例，不把九例做成每次文案修改的默认回归。

## 2. 三类真实任务的成本基线

复用 2026-09-16 的开放式真实任务 trace，**没有重跑**。它们采样时的 Skill 指纹均为 `9144d13affb4ee83c1337492ed471e92ba484e02d1f573c8dd91cda18f045395`（93 文件），故下表是历史基线，不是当前 95 文件版本的性能或质量 PASS。文件数按成功命令中可辨认的唯一文件路径计；“命令输出字符”包含辅助命令内容，不能视为纯 Skill 字数。input token 包含缓存与其他会话上下文。

| 任务 | 唯一读取 | 其中 Skill 文件 | 成功命令输出字符 | input / cached / output tokens | wall time |
|---|---:|---:|---:|---|---|
| [Greenfield](evidence/Real-greenfield-v1/trace.jsonl) | 12 | 12 | 46,298 | 116,625 / 93,952 / 3,583 | 未记录 |
| [已有产品变更](evidence/Real-existing-v1/trace.jsonl) | 15 | 12 | 54,093 | 89,722 / 63,488 / 3,030 | 未记录 |
| [生产问题](evidence/Real-production-v1/trace.jsonl) | 9 | 9 | 37,084 | 58,318 / 41,216 / 1,699 | 未记录 |

Greenfield 读取 4 个 Capability 入口及 2 份方法 reference，覆盖 AI 可行性、评测、人工控制与数据问题；没有逐个加载所有 Capability。已有产品变更读取 3 个产品文件与 12 个 Skill 文件，其中 PRD、AI Feasibility、Evaluation、Human-AI 四个 Capability 入口需要在真实使用中重点审查必要性：交付物最终判断当前确定性规则已足够，不能据一次读取断言四者全是误触发，但它暴露了上下文开销与范围扩张风险。生产问题读取 Production Learning、Evaluation、Responsible AI 三个相关入口，未展开无关 Discovery 或 Roadmap。

另有当前版本的 [PRD 定向 trace](evidence/PRD-cross-industry-v2/trace.jsonl)：6 个 Skill/支持文件，成功命令输出 22,986 字符，input/cached/output 为 73,132 / 55,296 / 2,887 tokens。除 PRD 节点及撰写方法外，还读取执行计划模板、Responsible AI 和 Evaluation 入口；是否都能改善这份 PRD 的决策质量，单一样本不足以判定。其内容仍为 `REVIEW_REQUIRED`，详见 [P0 状态报告](../evidence-status-p0.md)。

旧 runner 在完成执行后才写 `started_utc`，未记录真实 wall time；没有从文件创建时间补造耗时。本轮仅在 [run_real_work.py](run_real_work.py) 为**未来**运行记录真实开始时刻和单调时钟 `run_duration_seconds`，没有重写历史 metadata。

## 3. 产出 Rubric 与人工复核

按 [Rubric](real-work-rubric.md) 的“证据真实性 / 范围与上下文成本 / 决策可执行性 / 人工确认与恢复”四项各 0–2 分，阅读输入、trace 和交付物后记录：

| 交付物 | 四项分数 | 结论与必须保留的问题 |
|---|---|---|
| [Greenfield](evidence/Real-greenfield-v1/deliverable.md) | 2 / 2 / 2 / 2 = 8 | 可由资深 PM 接手；未提供的六份记录和指标基线明确标缺，未虚构效果。 |
| [已有产品变更](evidence/Real-existing-v1/deliverable.md) | 2 / 1 / 2 / 1 = 6 | 有条件可接手；多主题和证据 URL 被扩大为方案内容，需 PM 收窄或另行批准。 |
| [生产问题](evidence/Real-production-v1/deliverable.md) | 2 / 2 / 1 / 2 = 7 | 有条件可接手；新证据→旧决策重开→局部 Replan 正确，但修复方案/验收集未定时将 Build Readiness 写为 `PASS_WITH_ASSUMPTIONS` 偏乐观，须由 Gate owner 保持/改为 `BLOCKED` 直至证据就绪。 |

评分不把代表性 dry-run 升格为当前版本质量 PASS。产出质量的两个真实缺陷比格式差异更重要：未经授权的范围扩张与 Gate 过早放行。二者已在 [真实使用就绪报告](real-use-readiness.md)列为人工使用边界。

## 4. 修改、核验与停止条件

1. 先查阅上一轮 P1 清单、README、主 Skill、四组相邻 Capability 合同和 Planner canonical 规则；未把“P1”误认作仓库中的任务优先级字段。
2. 新增最小定向 runner，逐组独立生成 read-only/ephemeral prompt、trace、stderr、metadata、原判结果；完整 Skill 清单一致才采纳。先看原始输出再修测试器，只对三份判定器误判作透明重判。
3. 复用三类已有真实任务做成本与 Rubric 基线；只给未来 runner 加耗时记录。主 Skill 仍为 295 行、17,857 字节，本轮没有在入口堆补丁，也没有删减规则。
4. 九份 trace 均有一条 `turn.completed`，最终状态如上；定向核验了 Skill 版本、文件链接、runner 语法和差异空白。没有执行新的端到端产品任务或全量回归。

因未发现新的完整 forward evidence 证明 Skill 路由合同错误，本轮不修改任何 Skill 规则，也就没有“修改前后质量改善”的声称。已建立成本和质量基线；将来若针对已有产品范围扩张或生产 Gate 做窄修，须用同类输入比较前后读取与 Rubric，不能以降低 token 为由牺牲安全边界。P1 到此停止，不进入 P2 治理阶段。
