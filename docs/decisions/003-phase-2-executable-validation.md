# Phase 2 Executable Validation 完成记录

状态：完成（2026-09-10）。本记录落实 [Phase 2 任务书](002-content-cleanup-and-phase-2-plan.md)，不进入 Phase 3。

## 最终实现

- 使用 Python `dataclasses` 和现有 PyYAML 表达八个 canonical runtime object，不引入新的持久化对象。
- `validate_runtime.py` 提供 `objects`、`profile`、`plan`、`combined` 四种只读模式；成功、规则失败、文档错误分别返回 0、1、2，并输出稳定 JSON 错误。
- Profile validator 检查八节点、枚举、SKIP 理由、Cognition/Design/Evaluation dependency closure、生产发布、监控与 Release Readiness。
- Plan validator 检查版本、目标、Task、依赖引用与类型、DAG、READY 输入/产物/Gate、验收标准、critical path 与显式 `write_targets` 并行冲突。
- 固定 wrapper 只提供交叉验证上下文：`validation_context`、`available_inputs`、`artifacts`、`gates`、`blocked_inputs`、`write_targets`。这些字段不是项目状态 schema，也不写回文件。

## 语义处理

可执行验证只编码已有 canonical 规则。Evaluation Design 可由规则名称或 Solution Design reference 中五个必需组成项表示；`baseline when useful` 不被错误设为硬要求。中文“评估设计”和“监控”与英文 canonical 词义等价，避免因仓库默认中文而产生格式假阴性。

固定 fixture 是一个合法示例，不代表所有 supporting node 只有唯一 level。行为回归只对人工契约明确强制的节点和边界做集合断言；Delivery Target、AssignmentScope、关键 validation context、主节点、风险底线和范围外节点仍严格检查。

## 验证覆盖

- 8 个 canonical object 正例。
- 8 个 Profile / Plan 组合正例。
- 20 个定向负例，覆盖字段、枚举、版本、节点集合、依赖闭包、Gate、DAG、READY 和并行写冲突。
- 16 项 Python 回归，包括畸形嵌套输入、非字符串集合项、最低深度、双语能力名和 trace 分类。
- B1–B8 八个独立只读 Codex 行为 trace 全部 PASS；详细证据见 [行为报告](../../tests/ai-product-development/phase2/behavior/report.md)。

## 保留边界

P2 只证明结构化 Profile / Plan 可以确定性验证，并在八个固定场景中观察到选择性读取。它不保存项目状态，不创建 `.ai-product/`，不实现 init/save/resume，不自动执行产品任务，也不证明长周期连续交付。真实产品的状态恢复和 Golden MVP 仍属于后续 Phase 3 或重新规划的阶段。
