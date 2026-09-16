# Eval Readout

## Use

当已有有效 Run Evidence，需要判断是否达到阈值、为什么失败及结论适用范围时读取。

## Procedure

1. 先确认 run 完整性和 grader 有效性；无效评测得出 `block / rerun`，不解释产品质量。
2. 对照预设 primary threshold、guardrail 和零容忍项报告，不在看到结果后改变标准。
3. 同时报分布、trial 波动、严重度和关键切片；总体平均通过不能覆盖高影响切片失败。
4. 对 bad cases 去重聚类，区分数据、能力、prompt/tool、产品交互、权限/安全和 grader 问题；根因未证实时保持 hypothesis。
5. 检查基线差异、置信区间/不确定性、反例和可推广边界，明确未覆盖的人群、语言、任务与环境。
6. 按预设规则给出 `proceed | conditional | block | more evidence`，将确认失败路由到修复、Regression、Risk 或 Replan。

## Completion

报告直接回答原决策，关键失败未被平均值掩盖，结论与证据强度相称，且每项下一步都关联具体 bad case 或不确定性。
