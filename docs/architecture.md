# 架构说明

正式入口为 [Skill Kernel](../skills/ai-product-development/SKILL.md)。Phase 1 只重组现有规则并验证按需读取，不实现 Skill Runtime 服务。

## Progressive disclosure

技能发现时使用 name / description；技能启用后读取 Kernel；具体操作开始前才读取相关 reference。Profile 为八节点记录状态，不要求预读八节点详情。VERIFY 对应当前确有需要的核验；已有确认可复用材料可以满足依赖，不能据此机械扫描所有 VERIFY 节点。

依赖闭包由原 [Execution Profile](../skills/ai-product-development/references/runtime/execution-profile.md#67-dependency-closure) 决定。例如缺少验收标准的验证需要补充 Evaluation Design；已有可复用标准的只读核验不因此重建方案。支持性导航、局部规则检查和合法依赖读取不视为失败。

## 职责与 canonical rule

[Lifecycle references](../skills/ai-product-development/references/lifecycle) 保存八节点详情；[Runtime references](../skills/ai-product-development/references/runtime) 保存 Profile、Planner、Context、Executor、Registry、Replan 六项能力及三个共用顶层 Gate。一个文件不代表一个 Agent。Planner 的任务依赖和 Profile 的节点依赖职责不同。

详细规则只在 canonical location 维护，其他文件使用摘要或链接。例如 Replan 判断产物失效和版本时读取 Registry，包括只提出建议的任务；链接不授予写入权限。优先级、复杂度 guardrails 和共用完成标准保留在 Kernel。

[schemas](../skills/ai-product-development/schemas) 的五个 YAML 文件包含八个原始对象，是结构示意，不是实例验证器。原文只有 NodeProfile，没有 ExecutionProfile 聚合字段；本次不补字段、默认值或状态存储。

稳定输出仅有 [Plan Preview](../skills/ai-product-development/templates/execution-plan.md)。其他输出没有字段级固定格式，其规则保留在对应节点。

## 验证边界

结构验证检查链接、路由、Gate、源规则迁移、枚举和明显详细规则重复；不能证明模型行为。70 个源标题映射和 533 条逐行迁移指纹提供迁移证据，仍需审阅摘要和去重是否改变语义。

三个 [Routing Test](../tests/ai-product-development/routing/README.md) 分别在新临时目录、新 ephemeral Codex 进程中运行。受测进程始终使用 read-only；父进程准备 Skill 副本并记录 trace。成功命令与完整文件输出才是读取证据，最终自述仅作辅助。额外读取和 dependency closure 按场景审阅，不规定绝对最少文件数。

这三个有限路由 smoke tests 不证明完整产品交付能力；八个人工行为场景、Phase 2 数据模型/实例验证和 Phase 3 Golden MVP 均未执行。本次接受远程已删除旧占位目录的状态。迁移与未解决语义疑点见 [重构记录](decisions/001-modularize-ai-product-development.md)，下一阶段边界见 [Phase 2 任务书](decisions/002-content-cleanup-and-phase-2-plan.md)。
