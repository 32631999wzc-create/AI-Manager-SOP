# Validator 设计边界

本文定义 AI Product Development Skill 的确定性 Validator 边界。它不改变现有合同、Schema、错误码或验证行为。

## 1. Validator 负责什么

Validator 只执行能够从当前验证输入中确定性判断的规则：

- 检查必需字段、未知字段、数据类型、列表、枚举、版本格式和 canonical object shape；
- 检查 Task、Artifact、Gate、dependency、write target 和 critical path 等引用完整性；
- 检查 Plan DAG、Task dependency 一致性、READY 前置条件和并行正式产物写入冲突；
- 检查明确写入 canonical contract 的 lifecycle / Profile 依赖闭包；
- 返回稳定、可定位的错误，不修改输入、不补默认值、不推进项目状态。

规则必须能用相同输入得到相同结果。Validator 是只读合同检查器，不是 Planner、Executor、Gate owner 或 Runtime 状态机。

## 2. Validator 不负责什么

Validator 不判断需要专业判断、证据解释或人工授权的事项，包括：

- 产品方案、PRD、路线图或 AI 设计是否优质；
- 证据来源是否真实、充分、代表性良好或仍然有效；
- 业务结论、优先级、风险接受或发布决策是否合理；
- 某个 Capability 是否是最佳方法，或复杂语义是否已充分覆盖；
- 人工审核是否应批准，以及失败后应如何 Replan。

这些事项分别由 scenario contract、独立 forward test、Evidence / Decision 记录和 human review 验证。不能为了覆盖主观判断而向 Validator 持续增加条件分支。

## 3. `validation_context` 的边界

`validation_context` 只承载 deterministic cross-check 所需、但不属于 canonical Profile object 本体的事实。例如：是否修改既有仓库、设计是否已验证、验收标准是否已定义，以及当前发布相关条件。

它必须遵守以下边界：

- 不是 Project State、RuntimeSnapshot、Registry、EvidenceRecord 或 DecisionRecord；
- 不是默认值来源，不保存历史，不驱动任务执行，也不接受 Validator 回写；
- 只加入已有 canonical rule 确实需要的最小事实；不得为方便新增规则而无限扩字段；
- 不能用布尔字段替代证据质量、业务判断或人工确认；调用方仍负责提供可信、当前且可追溯的事实；
- 不需要 deterministic cross-check 的信息应留在正式对象、证据、场景测试或人工审核中。

## 4. Contract 同步规则

每条 deterministic business rule 必须按同一条链维护：

```text
Markdown canonical contract
→ tests/ai-product-development/phase2/validation-contract.yaml
→ runtime validator implementation
→ targeted positive / negative test
```

具体要求：

1. 先在唯一 canonical Markdown 位置定义业务约束；字段结构可由 canonical schema 补充，但限制不得只存在于 Python。
2. 在 `validation-contract.yaml` 记录稳定错误码、canonical source 和可确定性检查的含义。
3. Validator 只实现该合同明确要求的判断，不放宽合同，也不增加隐藏业务规则。
4. 使用最小 targeted test 同时证明错误输入被拒绝、合法输入仍通过；修改共享规则时只运行受影响的必要回归。
5. 任一层发生语义变化时同步审查其余三层；纯重构不得改变错误码、输入合同或既有行为。

如果规则不能从验证输入中确定性判断，就不进入 Validator，改由 scenario、forward evidence 或 human review 处理。
