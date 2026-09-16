---
name: human-ai-experience
description: Design user expectations, control, explanation, feedback, human oversight, and failure recovery when people interact with AI output or actions. Do not use merely to style a conventional deterministic interface.
---
# Human-AI Experience
## Purpose
让用户理解 AI 的能力与限制，并能发现、纠正、撤销或升级关键错误。
## When to use
用户接触 AI 输出、建议或动作，信任、控制、解释、反馈或人工协作影响结果时使用。
## When NOT to use
纯确定性界面无 AI 不确定性；问题实质是视觉风格；没有用户接触面的后台能力 spike。
## Decision / Unknown
- `decision_to_inform`：责任边界、告知、控制、确认、解释、恢复和人工介入。
- `unknown_to_reduce`：用户心智模型、错误发现、过度依赖、可逆性和反馈去向。
- `risk_to_reduce`：拟人化承诺、虚假置信、自动化偏差和免责声明替代设计。
## Required Inputs
- `blocking`：用户任务、AI 能力/限制、错误后果与动作可逆性。
- `reusable`：Discovery、PRD、Feasibility、风险和 bad cases。
- `optional`：可用性研究、无障碍和文化规范。
## Method
按当前决策选择性读取：

- 需要划分 AI、用户、审核者与运营责任，设计自动化级别、确认和解释时，读取 [Responsibility and Control](references/responsibility-and-control.md)；
- 需要设计错误发现、纠正、撤销、降级、人工升级与反馈闭环时，读取 [Failure Recovery and Feedback](references/failure-recovery-and-feedback.md)；
- 正式交付使用 [Human-AI Interaction Contract](templates/human-ai-interaction-contract.md)；仅在校准具体程度时查看 [Example](examples/human-ai-interaction-contract.md)。
## Evidence Rules
用任务观察、可用性证据、失败案例和行为日志；区分用户陈述与行为；保留过度信任/低信任反例；模型或交互变化后重新验证。
## Decision Rules
- `proceed`：关键状态可理解，错误可发现和恢复。
- `conditional`：限制自动化或增加确认/人工审核。
- `stop / block`：高影响动作不可控、不可撤销或边界不可沟通。
- `escalate`：无障碍、重大伤害或专业判断需对应 owner。
## Output Contract
输出 [Human-AI Interaction Contract](templates/human-ai-interaction-contract.md)：责任、能力/限制、关键状态、控制/确认、解释、失败恢复、反馈、人工升级、无障碍和测试场景。
## Handoff
- `reads_from`：Discovery、PRD、Feasibility、Risk。
- `writes_to`：Human-AI Contract。
- `supports_lifecycle`：Solution Design、Validation、Release。
- `may_trigger`：Evaluation、Experimentation、Risk、PRD。
- `reopen_when`：能力、错误模式、用户、自动化级别或生产行为变化。
## Completion Criteria
用户知道能做什么、何时不信任；关键错误可发现/纠正/撤销/升级；反馈有真实去向；高影响控制有验证证据。
## Boundaries
不以免责声明替代安全，不默认自动化越强越好，不展示未经校准的置信分数。
