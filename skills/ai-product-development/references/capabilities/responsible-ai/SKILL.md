---
name: responsible-ai-safety-security
description: Assess and control AI harms, misuse, privacy, security, and compliance risks when a product affects people, sensitive data, external content, or tool actions. Do not build enterprise governance machinery for a low-risk prototype without a concrete trigger.
---
# Responsible AI / Safety / Security
## Purpose
识别受影响者、危害与滥用路径，为风险设置可测试控制、owner、发布条件和重评触发器。
## When to use
敏感数据、高影响决策、外部内容/工具、滥用可能或政策/法律约束存在时使用；其他场景做相称筛查。
## When NOT to use
无具体风险触发时不建设重治理体系；法律结论须由专业责任人给出。
## Decision / Unknown
- `decision_to_inform`：`accept | mitigate | transfer | avoid | block`。
- `unknown_to_reduce`：受影响者、危害、暴露、可逆性、控制有效性和残余风险。
- `risk_to_reduce`：原则清单替代分析、供应商责任转移、过滤器替代权限/流程。
## Required Inputs
- `blocking`：用例、用户/受影响者、环境、权限/数据流和风险 owner。
- `reusable`：PRD、threat model、policy、eval、事件和既有控制。
- `optional`：法律/隐私/安全/领域专家意见。
## Method
按风险缺口选择性读取：

- 需要识别受影响者、intended use/misuse、危害与分级时，读取 [Risk and Harm Assessment](references/risk-and-harm-assessment.md)；
- 涉及敏感数据、外部内容、工具动作、权限或攻击面时，读取 [Data, Tool and Security Controls](references/data-tool-security-controls.md)；
- 需要把风险转成可测试控制、发布条件、监控和事件路径时，读取 [Control Assurance and Release](references/control-assurance-release.md)。

正式交付使用 [AI Risk Record](templates/ai-risk-record.md)；仅在校准记录粒度时查看 [Example](examples/ai-risk-record.md)。法律、隐私、安全及专业领域结论由相应 owner 确认。
## Evidence Rules
风险声明引用场景、受影响者和证据；事实/假设与残余风险分开；记录反证、控制测试和时效；模型/数据/权限/法规变化触发重评。
## Decision Rules
- `proceed`：控制经验证且残余风险由有权限者接受。
- `conditional`：限制人群/用例/权限/流量并持续监控。
- `stop / block`：重大不可逆风险无有效控制或 owner。
- `escalate`：法律、隐私、安全、领域或风险接受权限不足。
## Output Contract
输出 [AI Risk Record](templates/ai-risk-record.md)：情境、受影响者、危害/滥用、分级、控制/测试、残余风险、owner、咨询/审批、发布条件、监控、事件与重评触发器。
## Handoff
- `reads_from`：Discovery、PRD、Data、Human-AI、Eval、生产事件。
- `writes_to`：Risk Record 与 Gate evidence。
- `supports_lifecycle`：所有 Lifecycle，重点 Qualification、Solution、Validation、Release。
- `may_trigger`：Data、Human-AI、Evaluation、Replan、incident response。
- `reopen_when`：模型、数据、权限、用例、人群、控制、事件或法规变化。
## Completion Criteria
关键风险有可测试控制和 owner；残余风险已接受或阻塞；发布/监控/暂停/补救可执行；重评条件明确。
## Boundaries
不替组织接受重大风险，不自行给法律结论，不以免责声明或内容过滤替代系统控制。
