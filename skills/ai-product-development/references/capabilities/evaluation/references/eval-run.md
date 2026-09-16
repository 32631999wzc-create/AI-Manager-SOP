# Eval Run

## Use

当 Evaluation Plan 已存在，需要执行并保存可复现证据时读取。

## Procedure

1. 冻结 dataset/case、系统/模型/prompt/tool/grader 版本、环境、随机参数和运行时间；记录无法冻结的外部依赖。
2. 在运行前检查 case 完整性、敏感数据授权、holdout 隔离、grader 可用性和资源预算。
3. 按预设顺序与 trial 数执行；保存每例输入引用、输出、trace、grader 原始结果、人工覆盖、延迟、成本和异常。
4. 不因中途结果更换 case、grader、阈值或排除失败。必要偏离单独记录原因、影响并创建新 run，而非覆盖原 run。
5. 将基础设施失败、无效输入、系统拒绝和产品质量失败分开；保留失败输出供 readout 与 root cause 使用。

## Run Evidence Contract

至少包含 run ID、计划版本、被测版本、环境、case 集版本、grader 版本、trial、开始/结束时间、完整性状态、原始结果位置和偏离说明。

## Completion

运行可复现、计划偏离透明、输出与 trace 完整，且没有用选择性重跑或静默排除改变结论。
