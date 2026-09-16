# Experiment Design

## Use

当需要验证产品机制、行为改变或 outcome，而不只是模型离线质量时读取。

## Procedure

1. 写可证伪假设：`if intervention → observable change → because mechanism`，并说明失败会改变哪个产品决策。
2. 区分 outcome、leading behavior、AI/product quality、人工负担、成本和风险；选择一个 primary metric，设置相称 guardrails。
3. 固定 metric 定义、分母、事件、窗口、目标切片、最小有意义变化、成功/失败/继续取证阈值和停止条件。
4. 选择最低成本且能区分替代解释的设计：任务观察、prototype test、before/after、switchback、分阶段 rollout、对照实验或受控 pilot。因果要求越高，越需要可比对照与随机化。
5. 样本按真实任务和使用情境选择；记录资格、招募渠道、基线差异、暴露程度和流失，避免只保留活跃成功者。
6. 预先列出混杂因素、新奇效应、学习效应、季节性、支持强度和并发产品变化；无法控制时限制结论为关联。
7. 在看结果前固定分析和决策规则；探索性发现单独标记，不事后改为主要成功指标。

## Completion

设计能回答原决策，指标不混淆价值与质量/风险，归因边界透明，样本和窗口足以观察目标机制，且停止与扩大规则预先确定。
