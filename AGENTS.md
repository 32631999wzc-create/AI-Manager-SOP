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
- 正式 SOP 技能放在 `skills/ai-product-development/`，参考资料放在其 `references/` 目录。旧占位目录已在远程删除，不恢复。
- 架构说明放在 `docs/architecture.md`，决策记录放在 `docs/decisions/`。
- 当前技能的回归用例放在 `tests/ai-product-development/cases/`，预期行为放在对应 `expected/`；使用示例放在 `examples/ai-product-development/`。
- 修改前阅读相关文件，保留已有内容；未确定的流程应明确标注为待补充。

## Skill 模块化维护

1. 修改 Skill 前先读对应的 SKILL.md。
2. 根据任务和 Kernel Router 读取相关 reference，不默认读取全部 reference。
3. 修改规则先定位 canonical location，在该处维护，再检查路由。
4. 不在多个文件复制详细规则；共用约束使用链接。
5. 修改后运行 `python -B -X utf8 tests/ai-product-development/validate_structure.py` 和 `python -B -X utf8 -m unittest discover -s tests/ai-product-development -p test_phase1.py`；行为用例未实际运行时明确说明。
6. 保持目录、相对路径和内部锚点有效。
7. 本次迁移保持原文语义；语义疑点记录到 docs/decisions，不在拆分中擅自修正。

## Phase 1 Routing 验证

- 改动 Router 或模块加载依赖后，按 `tests/ai-product-development/routing/README.md` 独立运行三个只读 ephemeral 场景，保留原始工具 trace。
- PASS 必须有实际成功读取证据；不得用模型自述或静态链接测试代替。审阅必要模块漏读、额外读取、依赖闭包和 eager loading；不以绝对最少文件数限制支持读取。
- WARN 逐项审阅，FAIL 修复并使用新目录重测；不扩大受测进程为可写权限，不覆盖失败记录。
- 详细规则保持一个 canonical location，摘要不得比原文新增业务约束。保持 533 条迁移指纹、70 个源标题映射与文档一致；不要为了通过检查而重建迁移基线。
- Phase 1 不创建 `.ai-product/`、不实现 init/save/resume，不进入 Phase 2 或 Phase 3。
