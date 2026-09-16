# Workflow Synthesis

## Use

当已有访谈、观察、日志或工单，需要还原真实工作流并形成问题与机会判断时读取。

## Procedure

1. 以真实任务为单位重建 `trigger → steps → decisions → handoffs → failures → outcome`，标注角色、工具、等待、返工和例外。
2. 将材料拆成 `observation | participant explanation | team interpretation | assumption`，只合并语义一致且情境相同的证据。
3. 按用户、任务、频率、严重度和现有替代方案切片；同时建立反证清单，包括没有该问题的人、成功绕过问题的流程和替代因果。
4. 将问题表述为受约束情境中的受阻 outcome，而不是缺少某功能；分别估计频率、结果影响、时间/认知成本与风险。
5. 形成机会假设：目标切片、desired outcome、可能机制、可观察变化和关键假设。此处只做 AI fit 初判，保留更简单或非 AI 方案。
6. 使用预先声明的决策规则得出结论，并写明置信度、适用边界、最强反证与下一项最有信息价值的学习动作。

## Completion

每个重要结论都有 Evidence ID，观察与解释未混淆，机会范围足以支持 Product Definition 或明确停止，且旧决策的 reopen trigger 已在需要时提出。
