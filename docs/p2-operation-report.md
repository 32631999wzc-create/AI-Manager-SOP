# P2 工具与能力资产治理：操作过程报告

日期：2026-09-17（Asia/Shanghai）。执行范围来自上一轮二次审查的 P2：具体外部工具才建立适配器失败合同；建立周期性 Capability 盘点与保留/收缩/合并/退役依据；清理未采纳 trace；纠正文档状态漂移。没有改动运行时 Skill 规则、16 个 Capability 合同或 Replan 核心，也没有运行模型验证或推送 GitHub。

## 结果

- 新增[能力与工具资产治理](capability-governance.md)：规定按主要版本及季度复核的证据字段、判断标签、低使用率/误触发/重叠的判定边界、具体外部工具接入门槛和 trace 留存原则；从 [README](../README.md) 的维护章节可到达。
- 为 [006 架构决策](decisions/006-ai-pm-capability-playbooks.md)增加后续状态注记：原“Phase 3 尚未实施”是当时历史快照；正文与当时决策不重写。
- 未发现具体 MCP 或业务系统适配器。当前本地 project runtime CLI 与隔离测试 runner 不等于外部业务适配器，因此**未虚构工具参数、权限或重试实现**。将来实际接入时，必须在该具体适配器旁定义参数/权限/超时/错误/部分成功/恢复合同；此项当前为“不适用”，不是已经验证任何外部系统可靠。
- 38 个未采纳、未引用的本地 trace 目录通过 Windows `SendToRecycleBin` 接口移出工作区；10 个已被 P0/P1 报告引用的目录保持不变。旧目录中即使某个 `result.json` 写着 PASS，只要未被 accepted manifest 或报告采纳，也不升级为当前证据。

## 操作过程

1. 阅读仓库 README、正式 Skill、P1 收口报告、架构与历史决策；搜索脚本目录和文档，确认没有需要新增失败合同的具体 MCP/外部业务适配器。
2. 对未跟踪 evidence 逐目录统计文件数、字节、结果状态，并检查 accepted manifest 与非 evidence 文档引用。清理前共 48 个未跟踪 evidence 目录，约 3,938,550 字节；其中 9 个 P1 定向边界和 1 个 PRD-v2 为已采纳/已引用，合计 10 个。
3. 只将下列 38 个目录列入清理白名单，共 3,424,607 字节。执行前逐项确认其解析后的绝对路径位于对应仓库 evidence 根目录内、是普通目录而非链接、仅有五个预期文件、无跟踪文件；白名单数量与总字节数必须匹配，任一不符即停止。
4. 使用 Windows 回收站选项逐目录移出，没有运行 `git clean`、广域递归删除或覆盖命令。随后复查 38 个原路径均不存在，未跟踪 evidence 只剩上述 10 个已采纳目录。
5. 写入治理规则与 16 项初始盘点基线；对未在少量样本出现的能力标“证据不足”，没有凭目录数量自动删减。为历史 ADR 加注记并从 README 链接治理文档。

清理白名单（均位于 `tests/ai-product-development/` 下）：

| 证据根目录 | 精确目录名 | 数量 |
|---|---|---:|
| `phase2/behavior/evidence/` | `B1-capabilities-v1..v5`；`B2-capabilities-v1..v7`；`B3-capabilities-v1,v4,v5`；`B4-capabilities-v1,v4,v5`；`B5-capabilities-v2`；`B6-capabilities-v2`；`B7-capabilities-v2` | 21 |
| `phase5/evidence/` | `E1-v1..v6`；`E2-v1,v2`；`E3-v1`；`PRD-cross-industry-v1` | 10 |
| `routing/evidence/` | `R1-capabilities-v1,v2`；`R2-capabilities-v1..v3`；`R3-capabilities-v1,v2` | 7 |

这些是本地未跟踪的旧采样，不是已提交的历史文件；主要为 FAIL/WARN，也包含未被采纳的 PASS。Windows 回收站通常可恢复这些目录，恢复期限受本机回收站设置影响；本轮只验证原路径已清空、保留目录仍在，未独立检查回收站 UI 中每个条目。若需找回，按上表目录名在回收站恢复。

## 核验与边界

清理后：未跟踪 evidence 为 10 个目录，恰好是 9 个 P1 样例与 PRD-v2；README/治理文档/ADR 的本地链接与差异空白做定向检查。主 Skill 未改，旧 accepted manifest 与 raw trace 未改；无需因 P2 文档治理重新采样 P1 或运行 Phase 1–5 全链路。

本轮没有足够真实使用数据判定哪项能力“低使用率”、哪两项应合并或退役。下一次盘点须使用真实任务机会、误触发 trace、上下文成本与产出 Rubric 作依据。未接入具体外部工具前，P2 的工具失败合同门槛已定义，但实际适配器可靠性仍未被验证。
