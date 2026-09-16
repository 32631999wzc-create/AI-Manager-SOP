# Release & Operation

## Purpose

make the result safely usable at the requested delivery level.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

- 已验证的候选版本或正式 Artifact；
- 交付目标、发布范围、目标用户/环境和必要授权；
- Release Readiness 条件，以及适用的监控、成本、回滚和运营要求。

## Required Decisions / State

- 发布单元、目标环境、受众、渠道、版本和责任人明确；
- Release Readiness 已基于功能、质量、风险、权限、成本、监控和回滚证据判定；
- 部署、发布或外部写入已获得所需授权；
- rollout 的继续、暂停、缩小或回滚条件明确；
- 发布后的采用、可靠性、质量、成本和风险信号有去向。

## Capability Routing

受控 pilot 调用[实验与试点](../capabilities/experimentation/SKILL.md)；需要规划、执行或恢复面向用户的 rollout、采用和赋能时调用[发布、采用与赋能](../capabilities/launch/SKILL.md)，若 Release Readiness 已阻塞且当前只补质量或风险证据则不调用；生产质量、成本、反馈和事件闭环调用[生产观测与学习闭环](../capabilities/production-learning/SKILL.md)；高影响、受监管或滥用风险调用[责任 AI、安全与风险](../capabilities/responsible-ai/SKILL.md)。

## Outputs

Release Readiness 结果；已发布版本、环境和受众，或明确阻塞原因；发布验证与监控证据；适用的回滚条件、剩余风险和后续观察项。

## Completion Criteria

- 目标用户能在约定环境使用目标版本，或发布被明确阻塞；
- Release Readiness 与必要发布验证有证据；
- 监控、成本、权限和回滚达到交付目标所需深度；
- 版本、结果、剩余风险和责任边界已记录。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

生产发布依赖见 [Dependency Closure](../runtime/execution-profile.md)；执行 [Release Readiness](../runtime/gates.md#release-readiness)，正式版本状态遵循 [Registry](../runtime/registry-versioning.md)。

## Boundaries

Prototype 通常 `SKIP`，Demo 通常 `LIGHT`，MVP 和 Enterprise 按实际风险提升深度。不要在 Lifecycle 中复制 rollout 或运营方法，不在未授权时发布，不跳过必要 readiness，也不给 Demo 强加 Enterprise 体系。
