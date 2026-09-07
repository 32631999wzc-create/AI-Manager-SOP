# Agent Not Required — Expected Behavior

遵循 [共用行为契约](../behavior-contract.md)。

## Profile 与行为断言

- Delivery Target = DEMO；AssignmentScope.mode = FULL_PROJECT，无发布需求的 Release & Operation 说明理由后 SKIP。
- 按 DEMO 基线激活 Qualification、Cognition、Product Definition & Scope、Solution Design、Implementation、Validation & Iteration；Retrospective LIGHT。
- Greenfield 不做 repository cognition；真实 LLM 提取链必须运行，不能只以 mock 证明 DEMO 完成。
- 使用固定流程、LLM 调用和确定性校验；不默认 Agent、Multi-Agent、RAG、Vector DB、长期记忆或队列。
- 结构校验通过不等于验收通过，仍检查提取结果验收标准。

## 按需加载

- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design,05-implementation,06-validation-iteration,08-retrospective。
- 本场景不默认加载：07-release-operation；后续风险或硬依赖改变时说明理由并调整。
