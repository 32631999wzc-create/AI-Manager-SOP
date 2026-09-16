# Observability and Metric Tree

## Use

当产品已进入真实使用，需要判断是否创造价值、质量是否稳定、成本与风险是否受控时读取。

## Metric Tree

1. 从产品声明和 DecisionRecord 反推一个 outcome，而非从现有日志出发堆 dashboard。
2. 分开六类信号：`outcome | AI/product quality | reliability | unit cost/latency | risk/guardrail | adoption/workflow`。每项必须说明它支持什么决定。
3. 定义分子、分母、事件、窗口、切片、版本、数据延迟、owner、阈值与触发动作；没有动作的指标不默认采集。
4. 连接 exposure、输入情境、输出/动作、人工纠正、最终任务结果和系统/模型/prompt/tool/data 版本，避免只看请求成功率。
5. 为 silent failure 设计代理和抽样审查，例如纠正、撤销、二次处理、放弃、申诉和下游异常；代理必须标明偏差。
6. 以最小化原则采集敏感内容，优先事件/引用而非原文，定义访问、保留、删除和审计。

## Review Cadence

严重 guardrail/event 实时处理；操作指标按风险选择日/周；趋势与产品决策按周/月。不同 cadence 不应复制互相冲突的指标定义。

## Completion

关键产品声明、风险和单位经济可观察；每项信号有版本、切片、阈值、owner 和动作；仪表板没有把 uptime 或 adoption 等同于成功。
