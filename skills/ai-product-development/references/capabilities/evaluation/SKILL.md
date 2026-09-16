---
name: evaluation-quality
description: Design, run, interpret, or regress-test AI product evaluations when product claims, model choices, failures, or release decisions require reproducible quality evidence. Do not create generative eval infrastructure for deterministic behavior already covered by ordinary tests.
---
# Evaluation & Quality
## Purpose
把产品声明转成可复现的评测证据，并将失败稳定转入根因、修复与回归。
## When to use
需要定义 eval、执行 trial、解释结果、选择方案、验证修复或支持发布判断时使用。
## When NOT to use
普通确定性测试已充分回答；没有待支持的产品决策；只是监控生产 uptime。
## Decision / Unknown
- `decision_to_inform`：能否构建、哪个方案更好、是否达标、是否回归、能否推进。
- `unknown_to_reduce`：case 覆盖、grader 有效性、随机性、切片差异、根因和泛化边界。
- `risk_to_reduce`：通用 benchmark 代替产品验收、数据污染、事后降阈值、未校准 judge。
## Required Inputs
- `blocking`：产品声明/决策、acceptance criteria、版本与评测边界。
- `reusable`：代表数据、bad cases、基线、grader、历史报告。
- `optional`：专家、生产切片、成本/延迟预算。
## Method
按 gap 只加载：

- 需要把产品声明转成 case、grader、阈值与切片时，读取 [Eval Design](references/eval-design.md)；
- 需要锁定版本并执行可复现 trial 时，读取 [Eval Run](references/eval-run.md)；
- 需要解释结果、bad cases 与决策含义时，读取 [Eval Readout](references/eval-readout.md)；
- 需要把确认失败变成持续保护时，读取 [Regression](references/regression.md)。

正式交付使用 [Evaluation Plan](templates/evaluation-plan.md) 或 [Evaluation Readout](templates/evaluation-readout.md)；仅在校准报告深度时查看 [Example](examples/evaluation-readout.md)。Lifecycle 决定何时评测和如何处理 FAIL，本 Domain 只负责评测方法。
## Evidence Rules
记录 dataset/case、系统/模型/prompt/tool/grader 版本、trial、trace、阈值和时间；case 追溯到 requirement/生产来源；保留反例、切片和不确定性；防止 holdout 污染。
## Decision Rules
- `proceed`：预设阈值与 guardrail 在关键切片满足。
- `conditional`：仅有限场景达标，明确范围和控制。
- `stop / block`：grader 无效、覆盖不足、严重错误或结果不可复现。
- `escalate`：高影响结论需专家/风险 owner，或重大发布取舍需 Gate owner。
## Output Contract
输出 [Evaluation Plan](templates/evaluation-plan.md)、Run Evidence、[Evaluation Readout](templates/evaluation-readout.md) 或 Regression Result；必须说明决策、版本、方法、阈值、切片、bad case、置信/限制和下一步。
## Handoff
- `reads_from`：PRD、Feasibility、Data、Human-AI、Risk、生产 bad cases。
- `writes_to`：评测计划/证据/报告/回归集。
- `supports_lifecycle`：Solution Design、Validation、Release。
- `may_trigger`：Root Cause、Replan、Experimentation、Risk、Launch。
- `reopen_when`：requirement、数据、grader、模型、prompt/tool、风险或生产分布变化。
## Completion Criteria
选定子模式完成；评测支持原决策；关键声明/失败/风险有覆盖；grader 经校准；随机性和切片未被平均；结果可复现且结论有限定。
## Boundaries
不把 benchmark 当产品验收，不看结果后改阈值，不让未经校准 LLM judge 单独决定高风险结论。
