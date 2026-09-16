# Product Prototype Test

## Use

回答用户是否理解 AI 的角色、能否完成真实任务、能否发现和恢复错误，以及预期价值机制是否成立。不得用 mock 表现证明模型能力。

## Procedure

1. 明确待验证产品假设、目标用户、真实任务、可观察行为和停止条件。
2. 选择能回答问题的最低保真度：概念、纸面/可点击、Wizard-of-Oz 或连接真实能力的 prototype；逐项标注 `mocked | human-operated | real AI | deterministic`。
3. 设计任务而非功能导览，观察首次理解、输入准备、等待、输出判断、编辑/拒绝、错误恢复、交接和最终 outcome。
4. 主持人避免引导；将行为、用户解释、研究者推断和系统能力证据分开记录。
5. 纳入不确定、错误、拒绝、超时和权限边界场景；高影响流程验证确认、撤销和人工升级。
6. 按预设标准判断 `proceed | conditional | redesign | stop`，并把暴露的能力未知转回 Capability Spike 或 Evaluation。

## Completion

产品/体验未知被证据降低，mock 与真实能力边界透明，价值与可用性结论未混入技术可行性，下一版产品假设及重测条件明确。
