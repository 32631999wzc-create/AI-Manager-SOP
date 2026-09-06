# RAG Evaluation Only — Expected Behavior

## Profile 与行为断言

- Delivery Target = MVP；AssignmentScope.mode = PARTIAL_PROJECT，Validation & Iteration 为 PRIMARY。
- 对系统、数据和入口做必要 Cognition；Solution Design 只补齐或核实 Evaluation Design，不重新设计 RAG。
- 现有 RAG 是输入资产，不是引入新 RAG / Vector DB / Agent 的理由；不改实现和部署。
- 验收资产验证后可 VERIFY；缺少成功标准时依赖闭包恢复 Evaluation Design 至至少 MINIMAL。
- Implementation 与 Release & Operation 默认 OUT_OF_SCOPE / SKIP；失败可报告 bad case 和根因，不越权修复产品。
- 确定性检查足够时不强制 LLM Judge；报告不满足标准时不得声称通过。

## 按需加载

- 共用入口：[Skill Kernel](../../../skills/ai-product-development/SKILL.md)。
- Runtime：execution-profile.md；规划时 planner.md；进入 Gate 时 gates.md；其他 Runtime 文件仅在相应操作发生时读取。
- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design,06-validation-iteration。
- 本场景不默认加载：05-implementation,07-release-operation,08-retrospective；后续风险或硬依赖改变时说明理由并调整。

## 完成判定

共用 [Completion Criteria](../../../skills/ai-product-development/SKILL.md#17-completion-criteria)，不复制或改写全局完成规则。计划或 Profile 本身不等同于场景交付已完成。

## 人工记录

- 实际观察：待执行。
- 结论：未执行（静态检查不代替模型行为评估）。
