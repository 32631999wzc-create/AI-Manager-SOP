# Eval Design

## Use

当产品声明、方案选择、修复或发布判断尚未转成可执行评测时读取。

## Design from the Decision

1. 固定待支持的决策、系统边界、版本、目标用户/任务和错误成本；区分 capability、product quality、regression 与 production monitoring。
2. 将每项声明拆为可观察成功条件与失败严重度，建立 task taxonomy：主路径、关键切片、edge、拒绝/恢复和相称安全场景。
3. case 必须追溯到 requirement、真实任务、历史 bad case 或生产来源；合成数据标记生成方法与适用边界，避免测试集与开发材料污染。
4. 为每项条件选择 grader：确定性检查优先；人工 rubric 明确维度与锚点；LLM judge 需用人工标注样本校准一致性、偏差和失败边界。
5. 预先定义 trial 数、聚合方法、置信/不确定性、切片、primary threshold、guardrail、严重错误零容忍项和决策规则。
6. 记录数据、系统、模型、prompt、tool、grader 与环境版本，以及每项变化何时使证据失效。

## Completion

在看结果前计划已固定；关键声明、切片和严重失败有覆盖；grader 可解释且经过相称校准；阈值足以直接支持原决策。
