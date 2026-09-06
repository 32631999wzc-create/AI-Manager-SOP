# Repository Instructions

This repository contains reusable AI product development skills.

Before substantial work:

1. Read README.md.
2. Identify the relevant skill under /skills.
3. Read that skill's SKILL.md.
4. Read referenced documents under /docs only when required.
5. Do not modify unrelated files.
6. Run the relevant validation/tests after changing a skill.

# 仓库协作规则

- 本仓库用于维护 AI 产品经理工作流。
- 文档默认使用中文，文件和目录名称保持清晰、一致。
- 正式 SOP 技能放在 `skills/ai-product-development/`，参考资料放在其 `references/` 目录；`skills/ai-product-sop/` 为历史占位目录。
- 架构说明放在 `docs/architecture.md`，决策记录放在 `docs/decisions/`。
- 当前技能的回归用例放在 `tests/ai-product-development/cases/`，预期行为放在对应 `expected/`；使用示例放在 `examples/ai-product-development/`。
- 修改前阅读相关文件，保留已有内容；未确定的流程应明确标注为待补充。

## Skill 模块化维护

1. 修改 Skill 前先读对应的 SKILL.md。
2. 根据任务和 Kernel Router 读取相关 reference，不默认读取全部 reference。
3. 修改规则先定位 canonical location，在该处维护，再检查路由。
4. 不在多个文件复制详细规则；共用约束使用链接。
5. 修改后运行结构验证并检查对应 regression cases；行为用例未实际运行时明确说明。
6. 保持目录、相对路径和内部锚点有效。
7. 本次迁移保持原文语义；语义疑点记录到 docs/decisions，不在拆分中擅自修正。
