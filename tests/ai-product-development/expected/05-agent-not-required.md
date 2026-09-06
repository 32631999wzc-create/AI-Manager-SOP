# Agent Not Required — Expected Behavior

## Profile 与行为断言

- Delivery Target = DEMO；AssignmentScope.mode = FULL_PROJECT，无发布需求的 Release & Operation 说明理由后 SKIP。
- 按 DEMO 基线激活 Qualification、Cognition、Product Definition & Scope、Solution Design、Implementation、Validation & Iteration；Retrospective LIGHT。
- Greenfield 不做 repository cognition；真实 LLM 提取链必须运行，不能只以 mock 证明 DEMO 完成。
- 使用固定流程、LLM 调用和确定性校验；不默认 Agent、Multi-Agent、RAG、Vector DB、长期记忆或队列。
- 结构校验通过不等于验收通过，仍检查提取结果验收标准。

## 按需加载

- 共用入口：[Skill Kernel](../../../skills/ai-product-development/SKILL.md)。
- Runtime：execution-profile.md；规划时 planner.md；进入 Gate 时 gates.md；其他 Runtime 文件仅在相应操作发生时读取。
- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design,05-implementation,06-validation-iteration,08-retrospective。
- 本场景不默认加载：07-release-operation；后续风险或硬依赖改变时说明理由并调整。

## 完成判定

共用 [Completion Criteria](../../../skills/ai-product-development/SKILL.md#17-completion-criteria)，不复制或改写全局完成规则。计划或 Profile 本身不等同于场景交付已完成。

## 人工记录

- 实际观察：待执行。
- 结论：未执行（静态检查不代替模型行为评估）。
