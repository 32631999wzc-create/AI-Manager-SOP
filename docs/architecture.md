# 架构说明

正式入口为 [Skill Kernel](../skills/ai-product-development/SKILL.md)。

Kernel 常驻核心规则与路由；[Lifecycle references](../skills/ai-product-development/references/lifecycle) 保留八节点细节，[Runtime references](../skills/ai-product-development/references/runtime) 按职责维护执行规则。Profile 决定节点和深度，Planner 从实际缺口生成任务。一个职责文件不代表一个 Agent 或 Service。

读取顺序由任务决定：先 Kernel，再执行 Profile 所需规则，在进入节点或操作时读取相关 reference。Schema 只在构造或核对对象时读取，Template 只在输出对应格式时读取。

结构集中在 [schemas](../skills/ai-product-development/schemas)。原文只定义 NodeProfile，没有独立 ExecutionProfile 聚合字段；不新增聚合对象。原文 YAML 枚举写法保持不变。

稳定输出仅有 [Plan Preview](../skills/ai-product-development/templates/execution-plan.md)。Product Context Snapshot、Product Definition & Scope 和 Retrospective 没有字段级格式，其规则保留在节点 reference，不发明模板字段。

原有占位目录保留，正式入口以 README 为准。迁移、验证与语义问题见 [重构记录](decisions/001-modularize-ai-product-development.md)。
