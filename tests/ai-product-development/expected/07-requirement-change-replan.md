# Requirement Change / Replan — Expected Behavior

遵循 [共用行为契约](../behavior-contract.md)。

## Profile 与行为断言

- 基础场景保持 Delivery Target = MVP 和 Assignment Scope；使用 LOCAL REPLAN，不默认项目级回滚。
- 保留无关有效工作；对受影响项使用 PRESERVE / OUTDATE / ADD / CANCEL，不新增事件类型或恢复服务。
- 按依赖影响读取相关节点；范围未变不机械加载或重跑全部八节点。
- DAG 结构实质变化才创建新 Plan 版本；普通状态改变不新增版本；迭代用新任务实例，不构造循环 DAG。
- 需要输入时一个 HUMAN_CONFIRM 任务仅阻塞相关任务；区分局部可重试与不可重试失败。
- 变体使用 PROFILE REPLAN，重算风险与依赖闭包，继续复用有效资产。
- 正式更新保留版本规则；OUTDATED 与 SUPERSEDED 含义不同。

## 按需加载

- 本场景在变更时加载 replan-recovery.md，正式更新时加载 registry-versioning.md。
- 生命周期依当前 Profile 的受影响节点确定；基础变更不要求全部重读，变体按新 Profile 调整。
