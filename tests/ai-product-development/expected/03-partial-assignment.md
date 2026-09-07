# Partial Assignment — Expected Behavior

遵循 [共用行为契约](../behavior-contract.md)。

## Profile 与行为断言

- Delivery Target = ENTERPRISE；AssignmentScope.mode = PARTIAL_PROJECT，项目成熟度不等于本次全生命周期交付。
- Solution Design 为 PRIMARY；Qualification、相关 Product Definition & Scope 和必要 Cognition 支持，已验证资产可 VERIFY。
- Implementation、实际运行的 Validation & Iteration、Release & Operation 默认 OUT_OF_SCOPE / SKIP；硬依赖或风险要求时才增加最小支持工作。
- Evaluation Design 在 Solution Design 内，不伪造实现或测试通过。
- 项目级安全、监控、发布、回滚等必要能力明确 external_project_requirement，不能宣称无需这些能力。
- 不新增 Agent、RAG、Vector DB 或顶层节点。

## 按需加载

- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design。
- 本场景不默认加载：05-implementation,06-validation-iteration,07-release-operation,08-retrospective；后续风险或硬依赖改变时说明理由并调整。
