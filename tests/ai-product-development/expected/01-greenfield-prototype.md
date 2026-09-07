# Greenfield Prototype — Expected Behavior

遵循 [共用行为契约](../behavior-contract.md)。

## Profile 与行为断言

- Delivery Target = PROTOTYPE；AssignmentScope.mode = FULL_PROJECT。
- Qualification、Product Definition & Scope、Implementation 为 REQUIRED；Cognition、Solution Design、Validation & Iteration、Retrospective 按原型基线 LIGHT。
- Release & Operation = SKIP，给出无发布需求的理由；跳过 repository cognition，不把全部产品认知误判为不适用。
- 没有可复用设计时，依赖闭包保留至少 LIGHT 的 Solution Design；mock 不可描述为真实 AI 链已验证。
- 不自动引入 Agent、RAG、Vector DB、持久化或企业基础设施。

## 按需加载

- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design,05-implementation,06-validation-iteration,08-retrospective。
- 本场景不默认加载：07-release-operation；后续风险或硬依赖改变时说明理由并调整。
