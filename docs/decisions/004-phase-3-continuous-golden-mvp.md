# Phase 3 Continuous Delivery Golden MVP

状态：完成（2026-09-10）。本阶段建立在已完成的 Phase 1 模块化和 Phase 2 可执行验证之上。

## 目标

证明用户把 Skill 配置到本地后，可以从一个经过确认的产品目标开始，在同一产品仓库中持续执行、保存、恢复、局部重规划并完成一个 Runnable Demo。Phase 3 不改变八个 lifecycle node、六项 Runtime capability、三个顶层 Gate 或已有状态枚举。

## 实现范围

- 用 `.ai-product/` 文件目录实现 Registry、Context 与 Replan 的最小持久状态。
- 提供 `init`、`validate`、`status`、`next`、`task`、`register-record`、`commit-artifact`、`checkpoint/save`、`resume`、`update-profile`、`complete` 和 `replan` 命令。
- 所有对象继续由 Phase 2 validator 校验；Runtime 不修改验证输入，也不自动补全业务判断。
- 使用 Feedback Organizer 作为 Golden MVP，提供 CSV/JSON 导入、去重、主题/情绪/紧急度整理、来源筛选、证据引用及 JSON/Markdown 输出。
- 使用确定性分类器保证离线回归；真实模型 Provider 属于后续可选产品增强。

## 状态设计

Plan 是 Task 的唯一持久来源，Registry 是 Record 和 Artifact 的唯一持久来源，避免另建 `tasks.yaml` 或在 Plan 中复制 Artifact。Snapshot 只保存 plan version、task states、ACTIVE 引用和 unresolved items。聊天记录不是恢复来源。

初始化先在临时目录写完全部文件，再整体改名；后续单文件更新使用同目录临时文件与原子替换。Runtime 验证 ACTIVE Artifact 的目标文件存在，并在 resume 时核对 Snapshot 与当前 Plan、Registry 一致。

## 验收

1. 同一初始化输入可以安全重试，不同输入不能覆盖已有项目。
2. `next` 只选择合法 READY Task，并生成通过 canonical schema 验证的最小 Context Pack。
3. 新进程可以从 Snapshot 恢复同一计划和下一任务，不读取旧聊天历史。
4. COMPLETED 和 Artifact commit 必须有显式验证 PASS；Artifact 版本连续且旧版本 SUPERSEDED。
5. Local Replan 使用 `PRESERVE / OUTDATE / ADD / CANCEL`；每个任务变化有对应 action，DAG 变化才增加 Plan 版本。
6. Golden MVP 可离线运行，输出可追溯到反馈 ID。
7. P1、P2、P3 自动化验证全部通过；Skill 哈希变化后重新生成 P1/P2 独立 Codex trace。
8. P3 独立行为验收必须记录初始化、保存、全新会话恢复、变更与完成的实际文件和工具 trace；模型自述不能单独支持 PASS。

## 非目标

多人并发、数据库、事件溯源、向量记忆、云端状态、真实模型供应商集成、生产部署、权限系统和自动发布不属于本阶段。P3 完成时的目标是本地单用户持续交付 Beta，不声称达到 Production / Enterprise。

## 完成结果

13 项 Phase 3 自动化测试和四个全新 Codex 会话全部通过。最终状态为 Plan v2、四个 Snapshot、三个 ACTIVE Artifact，Completion Criteria 返回 true。实际 trace、失败修复和回放方式见 [Golden 报告](../../tests/ai-product-development/phase3/golden/report.md)。
