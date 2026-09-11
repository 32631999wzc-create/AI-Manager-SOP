# Release & Operation

## Purpose

make the result safely usable at the requested delivery level.

## Activation Conditions

由 [Execution Profile](../runtime/execution-profile.md) 决定本节点是否激活及执行深度；不因存在本文件而自动创建任务。

## Required Inputs

- 已验证的候选版本或正式 Artifact；
- 交付目标、发布范围、目标用户/环境和必要授权；
- Release Readiness 条件，以及适用的监控、成本、回滚和运营要求。

## Capabilities

release readiness, deployment, monitoring, cost/performance validation, pilot/observation, rollback readiness, scale decision.

## Procedure

1. 明确发布单元、目标环境、受众、渠道和负责人。
2. 按交付目标检查功能、质量、安全、权限、成本、监控和回滚要求。
3. 记录 Release Readiness；只执行已获授权的部署、发布或外部写入。
4. 发布后执行必要的部署验证或 smoke check。
5. 在适用时观察使用、可靠性、质量和成本，并决定继续、暂停或回滚。

Activate only what the delivery target needs.

- Prototype: usually `SKIP`.
- Demo: often `LIGHT`.
- MVP: normally `REQUIRED` at practical pilot depth.
- Enterprise: `REQUIRED` with production-appropriate controls.

## Outputs

Release Readiness 结果；已发布版本、环境和受众，或明确阻塞原因；发布验证与监控证据；适用的回滚条件、剩余风险和后续观察项。

## Completion Criteria

- 目标用户能在约定环境使用目标版本，或发布被明确阻塞；
- Release Readiness 与必要发布验证有证据；
- 监控、成本、权限和回滚达到交付目标所需深度；
- 版本、结果、剩余风险和责任边界已记录。节点完成后仍须满足 [全局 Completion Criteria](../../SKILL.md#17-completion-criteria)。

## Dependencies

生产发布依赖见 [Dependency Closure](../runtime/execution-profile.md)；执行 [Release Readiness](../runtime/gates.md#release-readiness)。

## Load With

仅在相应操作发生时加载上面链接的 Runtime 文件；数据对象定义按 [Kernel Router](../../SKILL.md#progressive-disclosure-router) 读取。

## Do Not

遵守 [Kernel 的 Operating Principles 和 Complexity Guardrails](../../SKILL.md)，不要将能力清单机械转换为任务。不要在未授权时发布，不要跳过必要 readiness，也不要给 Demo 强加 Enterprise 运营体系。
