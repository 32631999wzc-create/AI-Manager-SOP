# Existing Reusable Assets — Expected Behavior

遵循 [共用行为契约](../behavior-contract.md)。

## Profile 与行为断言

- Delivery Target = MVP；AssignmentScope.mode = PARTIAL_PROJECT。
- 相关 Cognition 保留；VERIFIED_REUSABLE 优先 VERIFY，已满足节点可生成零任务。
- PARTIAL 只对缺口建任务，不整套重建；PRESENT_UNVERIFIED 先验证。
- OUTDATED 不能降低必需工作；CONFLICTING 在依赖工作前解决，不能当 VERIFIED_REUSABLE。
- PRIMARY 为实现与验证；范围外发布默认 SKIP；supporting 最小化，SKIP 都有理由。
- 复用不省略验收；不新增 Agent、RAG、Vector DB；读最新 ACTIVE 资产，旧版只在有理由时加载。

## 按需加载

- 本场景在检索已有资产时加载 context.md。
- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design,05-implementation,06-validation-iteration。
- 本场景不默认加载：07-release-operation,08-retrospective；后续风险或硬依赖改变时说明理由并调整。
