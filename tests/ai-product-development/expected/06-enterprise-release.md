# Enterprise Release — Expected Behavior

遵循 [共用行为契约](../behavior-contract.md)。

## Profile 与行为断言

- Delivery Target = ENTERPRISE；AssignmentScope.mode = FULL_PROJECT。
- Qualification 至 Release & Operation 按企业基线 REQUIRED，Retrospective LIGHT；已有资产先验证，再以 VERIFY 减少重复工作。
- 风险与依赖闭包不能跳过验证、发布就绪、权限、安全、监控、可靠性和回滚要求。
- 生产发布前读取 Release Readiness；没有证据不得把验收或产物状态写成已通过或 ACTIVE。
- 阻塞输入或失败 Gate 阻止受影响执行；不能用时间紧或偏好掩盖不足。
- 不因 ENTERPRISE 自动添加无业务触发的 Agent、RAG 或 Vector DB。

## 按需加载

- 生命周期候选（随执行阶段按需加载，VERIFY 只核实相关规则）：01-qualification,02-cognition,03-product-definition,04-solution-design,05-implementation,06-validation-iteration,07-release-operation,08-retrospective。
