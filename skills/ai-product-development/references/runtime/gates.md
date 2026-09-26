# Flow Gates

Use only three top-level gates.

Gate 是放行判断，不是 Skill 自我批准。每次判断先确定 assignment 中对此决策负责的人工 owner；AI 可整理证据、建议结论，不能代替 owner 接受残余风险。涉及技术可行性、评测、隐私/安全或运营的硬风险时，分别取得相应责任人的证据或明确意见；关键 owner 不明时，受影响的放行保持 `BLOCKED`，向用户请求指定责任人，不推定默许。Task 交审与 Gate 放行是不同判断：文档获批不自动证明 Build/Release Ready，Gate 通过也不免除该 Task 交审。

默认放行责任边界：Qualification 由委托方指定的产品/业务 owner 确认目标与范围；Build Readiness 由产品 owner 确认需求基线、技术 owner 确认可实现性、评测 owner 确认验收设计；Release Readiness 由被授权的发布/运营 owner 决定发布，并取得受影响的产品、技术、评测及隐私/安全等风险 owner 的必要确认。一个人可兼任多角色，但不能用 AI 的判断代替其签认；组织已有明确审批制度时遵循该制度。缺席的关键角色或相互冲突的意见不能靠多数票、沉默或默认值放行。

### Evidence and Risk Decision Rule

证据是否充足取决于**当前要放行的决定、目标人群/环境、交付深度和潜在损害**，不是材料数量。对每项阻塞性主张检查：来源与版本/时间可追溯；覆盖当前场景及关键失败/人群切片；方法和结果可复核；指标、验收阈值与观察结果可比较；冲突、负例与不确定性可见；责任人及必要的控制、监测、降级/回滚已明确。引用旧版或不适用场景的结论、未经核验的自述、仅有平均值而遗漏关键切片，不能充作当前 Gate 证据。数值阈值由项目责任人、现行标准或明确的验收合同在判断前确定；Skill 不编造跨行业通用及格线。

先按严重性、暴露范围/发生可能性、可检测性和可逆性分层；涉及人身/重大财产、权利或敏感数据、不可逆外部行动、法规/合同硬约束的风险，即使发生率未知或很低，也按硬风险审查。按场景选择可测指标，例如关键错误/漏判率、敏感信息泄露、质量切片差异、可用性、延迟/成本、人工接管和恢复时间；明确分母、样本覆盖及不确定性。高影响决定缺少适用阈值或关键切片结果时不得用总体平均、口头保证或 `PASS_WITH_ASSUMPTIONS` 放行。

缺证据时先区分三种处置：

- **自行补充/核验**：所需材料或检查在当前授权与范围内可取得，且不会先跨过受阻 Gate；只做针对性取证、复测或查证，再重新判断。
- **`PASS_WITH_ASSUMPTIONS`**：仅限不影响安全/合规硬边界和当前阶段核心决定的非阻塞未知；逐项写明假设、owner、验证期限/触发器与失败后动作。它不能把未验证的修复方案、评测集或发布风险伪装为已满足。
- **`BLOCKED` / 人工确认**：核心目标、范围、方案、验收阈值、数据权利、关键风险控制或责任人缺失；关键证据无法在授权范围内取得、与阈值冲突或结果未达标；或剩余风险需责任人接受。只阻断依赖该判断的工作，记录最小补证动作和重新判定条件，不把整个项目无关工作一并冻结。

Gate 结论至少记录：决定与适用范围、owner/必要责任人、引用的 Evidence/Artifact 版本、预定阈值与实测结果（或明确不适用理由）、关键未知和反证、风险/控制、结论、补证动作及重新打开条件。没有正式 EvidenceRecord ID 时引用可定位的原始材料，不编造编号。批准后的新证据或人工修改若影响这些依据，按 Replan 合同重新判断受影响 Gate。

## Qualification Gate

Qualification result is one of:

- `PASS`
- `PASS_WITH_ASSUMPTIONS`
- `BLOCKED`

Do not proceed past blocking unknowns. Non-blocking unknowns may proceed as explicit assumptions.

Can reliable planning begin?

足够证据是：目标/交付深度、Assignment Scope、可用材料、主要约束与风险已被可靠识别，能形成不依赖臆造事实的计划；非关键未知可以列为有 owner 的假设。会改变目标、权限或风险地板的缺口阻塞相应规划。

## Build Readiness

**Build Readiness:** before substantial implementation, verify that scope, solution, and evaluation criteria are sufficiently clear for the target delivery level.

Result: `PASS | PASS_WITH_ASSUMPTIONS | BLOCKED`.

Are scope, solution, and success criteria sufficiently clear for the requested delivery depth?

足够证据是：经交审的范围/需求基线仍适用；当前实现切片的产品与技术路径、数据/接口/失败处理及责任边界明确；评测对象、样本/关键切片、验收指标与阈值可用于判断构建结果；硬风险已有控制与责任人。Prototype 可在标明 mock 和可逆边界后使用较轻证据；面向真实用户或生产的实现不能仅凭未验证假设放行。生产故障中若修复方案或验收集仍未知，保持 `BLOCKED`，先做最小诊断/设计/评测准备，再重判；不以“稍后补齐”给 `PASS_WITH_ASSUMPTIONS`。

## Release Readiness

Does the current result satisfy the requested delivery target and acceptance criteria?

足够证据是：候选版本在目标环境/人群及关键切片上通过预定验收，已知 bad cases 与安全、隐私、权限、可靠性、成本等适用风险得到验证或控制；监测、人工接管/回滚、发布范围和 owner 已明确，必要发布授权已获得。失败、关键切片未测、硬风险无控制或回滚不可用时 `BLOCKED`；缩小受众/能力须先形成新的明确发布范围与阈值，再独立判断，不能把缩小范围当作原范围 PASS。

Other checks remain local acceptance criteria rather than new gate objects.
