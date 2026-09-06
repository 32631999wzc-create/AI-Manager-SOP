# Partial Assignment — Expected Behavior

## Profile 与行为断言

- Delivery Target = ENTERPRISE；AssignmentScope.mode = PARTIAL_PROJECT，项目成熟度不等于本次全生命周期交付。
- Solution Design 为 PRIMARY；Qualification、相关 Product Definition & Scope 和必要 Cognition 支持，已验证资产可 VERIFY。
- Implementation、实际运行的 Validation & Iteration、Release & Operation 默认 OUT_OF_SCOPE / SKIP；硬依赖或风险要求时才增加最小支持工作。
- Evaluation Design 在 Solution Design 内，不伪造实现或测试通过。
- 项目级安全、监控、发布、回滚等必要能力明确 external_project_requirement，不能宣称无需这些能力。
- 不新增 Agent、RAG、Vector DB 或顶层节点。

## 按需加载

- 共用入口：[Skill Kernel](../../../skills/ai-product-development/SKILL.md)。
- Runtime：execution-profile.md；规划时 planner.md；进入 Gate 时 gates.md；其他 Runtime 文件仅在相应操作发生时读取。
- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design。
- 本场景不默认加载：05-implementation,06-validation-iteration,07-release-operation,08-retrospective；后续风险或硬依赖改变时说明理由并调整。

## 完成判定

共用 [Completion Criteria](../../../skills/ai-product-development/SKILL.md#17-completion-criteria)，不复制或改写全局完成规则。计划或 Profile 本身不等同于场景交付已完成。

## 人工记录

- 实际观察：待执行。
- 结论：未执行（静态检查不代替模型行为评估）。
