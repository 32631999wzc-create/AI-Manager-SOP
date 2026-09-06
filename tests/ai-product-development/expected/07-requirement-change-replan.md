# Requirement Change / Replan — Expected Behavior

## Profile 与行为断言

- 基础场景保持 Delivery Target = MVP 和 Assignment Scope；使用 LOCAL REPLAN，不默认项目级回滚。
- 保留无关有效工作；对受影响项使用 PRESERVE / OUTDATE / ADD / CANCEL，不新增事件类型或恢复服务。
- 按依赖影响读取相关节点；范围未变不机械加载或重跑全部八节点。
- DAG 结构实质变化才创建新 Plan 版本；普通状态改变不新增版本；迭代用新任务实例，不构造循环 DAG。
- 需要输入时一个 HUMAN_CONFIRM 任务仅阻塞相关任务；区分局部可重试与不可重试失败。
- 变体使用 PROFILE REPLAN，重算风险与依赖闭包，继续复用有效资产。
- 正式更新保留版本规则；OUTDATED 与 SUPERSEDED 含义不同。

## 按需加载

- 共用入口：[Skill Kernel](../../../skills/ai-product-development/SKILL.md)。
- Runtime：execution-profile.md；规划时 planner.md；进入 Gate 时 gates.md；变更时 replan-recovery.md；正式更新时 registry-versioning.md；其他 Runtime 文件仅在相应操作发生时读取。
- 生命周期依当前 Profile 的受影响节点确定；基础变更不要求全部重读，变体按新 Profile 调整。

## 完成判定

共用 [Completion Criteria](../../../skills/ai-product-development/SKILL.md#17-completion-criteria)，不复制或改写全局完成规则。计划或 Profile 本身不等同于场景交付已完成。

## 人工记录

- 实际观察：待执行。
- 结论：未执行（静态检查不代替模型行为评估）。
