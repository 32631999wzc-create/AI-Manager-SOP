# Greenfield Prototype — Expected Behavior

## Profile 与行为断言

- Delivery Target = PROTOTYPE；AssignmentScope.mode = FULL_PROJECT。
- Qualification、Product Definition & Scope、Implementation 为 REQUIRED；Cognition、Solution Design、Validation & Iteration、Retrospective 按原型基线 LIGHT。
- Release & Operation = SKIP，给出无发布需求的理由；跳过 repository cognition，不把全部产品认知误判为不适用。
- 没有可复用设计时，依赖闭包保留至少 LIGHT 的 Solution Design；mock 不可描述为真实 AI 链已验证。
- 不自动引入 Agent、RAG、Vector DB、持久化或企业基础设施。

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
