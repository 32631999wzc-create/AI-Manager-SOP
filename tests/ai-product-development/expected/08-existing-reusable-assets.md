# Existing Reusable Assets — Expected Behavior

## Profile 与行为断言

- Delivery Target = MVP；AssignmentScope.mode = PARTIAL_PROJECT。
- 相关 Cognition 保留；VERIFIED_REUSABLE 优先 VERIFY，已满足节点可生成零任务。
- PARTIAL 只对缺口建任务，不整套重建；PRESENT_UNVERIFIED 先验证。
- OUTDATED 不能降低必需工作；CONFLICTING 在依赖工作前解决，不能当 VERIFIED_REUSABLE。
- PRIMARY 为实现与验证；范围外发布默认 SKIP；supporting 最小化，SKIP 都有理由。
- 复用不省略验收；不新增 Agent、RAG、Vector DB；读最新 ACTIVE 资产，旧版只在有理由时加载。

## 按需加载

- 共用入口：[Skill Kernel](../../../skills/ai-product-development/SKILL.md)。
- Runtime：execution-profile.md；规划时 planner.md；进入 Gate 时 gates.md；检索时 context.md；其他 Runtime 文件仅在相应操作发生时读取。
- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design,05-implementation,06-validation-iteration。
- 本场景不默认加载：07-release-operation,08-retrospective；后续风险或硬依赖改变时说明理由并调整。

## 完成判定

共用 [Completion Criteria](../../../skills/ai-product-development/SKILL.md#17-completion-criteria)，不复制或改写全局完成规则。计划或 Profile 本身不等同于场景交付已完成。

## 人工记录

- 实际观察：待执行。
- 结论：未执行（静态检查不代替模型行为评估）。
