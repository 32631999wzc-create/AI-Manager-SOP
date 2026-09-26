# Requirement Change / Replan

## 输入场景

已有代码仓库和当前生效的 Profile / Plan baseline 的 MVP 开发中，用户更改输出字段。新字段的验收标准尚未定义。本次委托仍包括受影响字段的实现与回归验证；交付目标、范围、主要约束不变，有仍有效的记录、产物和已完成任务。

固定测试输入：AssignmentScope.mode = PARTIAL_PROJECT。本次自动化场景只处理目标与范围不变的基础变更，且只生成 Profile / Plan、不实际执行。
