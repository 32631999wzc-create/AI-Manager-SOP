---
name: ai-feasibility-prototyping
description: Test whether AI can meet a real product task and what complexity is justified when capability, data, integration, latency, cost, safety, or controllability remains uncertain. Do not treat a polished product prototype as technical feasibility evidence.
---

# AI Feasibility & Prototyping

## Purpose
用最小实验区分“AI 能否可靠完成任务”和“用户是否理解并愿意使用产品方案”。
## When to use
AI fit、能力阈值、模型/检索/工具/工作流取舍或产品交互假设尚不明确时使用。
## When NOT to use
能力边界已有新鲜证据且只需实现；纯用户问题先 Discovery；离线质量验收使用 Evaluation。
## Decision / Unknown
- `decision_to_inform`：feasible、受限可行、继续取证或暂不可行；是否进入产品定义/设计。
- `unknown_to_reduce`：能力、数据、集成、延迟、成本、安全、控制或用户理解。
- `risk_to_reduce`：一次成功即宣布可用、跳过非 AI 基线、探索代码变生产架构。
## Required Inputs
- `blocking`：真实任务、成功阈值、最大未知项、错误成本。
- `reusable`：样例、数据、API、基线、已有试验与限制。
- `optional`：用户原型、模型候选、成本/延迟预算。
## Method
按未知项选择性读取：

- 模型、数据、检索、工具、可靠性、延迟或成本未知，读取 [AI Capability Spike](references/ai-capability-spike.md)；
- 用户理解、工作流、控制或产品价值未知，读取 [Product Prototype Test](references/product-prototype-test.md)；
- 两类未知都存在时分别执行并分别下结论，不用产品原型证明技术能力。

正式交付分别使用 [Feasibility Note](templates/feasibility-note.md) 或 [Prototype Test Readout](templates/prototype-test-readout.md)；仅在校准深度时查看 [Example](examples/feasibility-note.md)。
## Evidence Rules
保存任务、版本、配置、输入、输出、trace、trial、成本/延迟与失败；事实/假设分开；包含反例和简单基线；模型/数据变化使旧证据降级。
## Decision Rules
- `proceed`：代表性任务达到预设阈值且复杂度有证据。
- `conditional`：仅在明确场景/控制/成本约束下可行。
- `stop / block`：核心阈值失败或所需数据/控制不可得。
- `escalate`：高影响残余风险、法律/隐私或预算权限问题。
## Output Contract
输出 [Feasibility Note](templates/feasibility-note.md) 和/或 [Prototype Test Readout](templates/prototype-test-readout.md)，分别声明能力结论与产品结论、证据、限制、推荐复杂度和重开条件。
## Handoff
- `reads_from`：Discovery、PRD、Data、Risk。
- `writes_to`：Feasibility Note / Prototype Readout。
- `supports_lifecycle`：Qualification、Product Definition、Solution Design。
- `may_trigger`：Evaluation、Data、Human-AI、Experimentation、Roadmap。
- `reopen_when`：任务、模型、数据、工具、阈值、成本或用户情境变化。
## Completion Criteria
最大未知项被证据降低；能力与产品体验结论未混淆；包含更简单/非 AI 基线；结论和约束能支持 PRD、设计或 stop 决策。
## Boundaries
不把供应商 benchmark 或一次 demo 当产品可行性，不把探索实现静默升级为生产方案。
