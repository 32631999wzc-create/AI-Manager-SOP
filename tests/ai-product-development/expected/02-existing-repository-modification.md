# Existing Repository Modification — Expected Behavior

## Profile 与行为断言

- Delivery Target = DEMO；AssignmentScope.mode = PARTIAL_PROJECT，PRIMARY 为 Implementation 和 Validation & Iteration。
- 受影响代码路径的 Cognition = REQUIRED，编辑前完成仓库检查；不能因修改小就跳过。
- 现有设计和验收资产先验证，有效后使用 VERIFY；任务只覆盖超时处理缺口。
- Product Definition & Scope 等 supporting 工作只确认相关边界，不重做完整 PRD；Release & Operation 等范围外工作默认 SKIP 并说明理由。
- 不省略修复、局部验证和回归；不引入新 Agent、RAG 或 Vector DB。

## 按需加载

- 共用入口：[Skill Kernel](../../../skills/ai-product-development/SKILL.md)。
- Runtime：execution-profile.md；规划时 planner.md；进入 Gate 时 gates.md；其他 Runtime 文件仅在相应操作发生时读取。
- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design,05-implementation,06-validation-iteration。
- 本场景不默认加载：07-release-operation,08-retrospective；后续风险或硬依赖改变时说明理由并调整。

## 完成判定

共用 [Completion Criteria](../../../skills/ai-product-development/SKILL.md#17-completion-criteria)，不复制或改写全局完成规则。计划或 Profile 本身不等同于场景交付已完成。

## 人工记录

- 实际观察：待执行。
- 结论：未执行（静态检查不代替模型行为评估）。
