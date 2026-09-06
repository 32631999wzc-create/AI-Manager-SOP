# AI-Manager-SOP

真实的AI产品经理工作流。

本仓库维护可复用的 AI 产品开发技能。正式入口为 [AI Product Development](skills/ai-product-development/SKILL.md)，覆盖原型到生产的产品定义、设计、实现、评估和发布，依据任务范围、已有资产、依赖和风险调整深度。

## 架构

- **Skill Kernel + Router**：激活范围、八个固定节点、六项 Runtime 能力、全局约束、主流程和完成标准。
- **References**：生命周期与 Runtime 详细规则各有唯一维护位置。
- **Schemas**：原文 YAML 对象定义，保留字段、枚举和约束；是结构示意，不是实例验证框架。
- **Templates**：仅抽离原文提供稳定格式的 Plan Preview；其他输出规则留在 references。

遵循 Execution Profile → active nodes → relevant references。不要默认读取全部 references；Runtime 也按实际操作的需要读取。

## 目录

```text
skills/
├── ai-product-development/
│   ├── SKILL.md
│   ├── references/
│   │   ├── lifecycle/        # 八个固定节点
│   │   └── runtime/          # 七个职责文件，不是额外 Agent
│   ├── schemas/             # 五个 YAML 文件
│   └── templates/           # execution-plan.md
└── ai-product-sop/           # 保留历史占位目录
tests/
├── ai-product-development/
│   ├── cases/
│   ├── expected/
│   ├── migration-manifest.json
│   └── validate_structure.py
└── cases/
examples/
└── ai-product-development/
docs/
├── architecture.md
└── decisions/
```

## 测试

安装 Python 3 和 PyYAML 后，在仓库根目录运行：

```sh
python tests/ai-product-development/validate_structure.py
```

检查内部文件与锚点链接、frontmatter、八节点顺序、Runtime 列表、原始 schema 对象、规则迁移指纹和八组 case/expected 配对。迁移基线只保存哈希，不重复保存整份旧 Skill。

额外核验原始文件时：

```sh
python tests/ai-product-development/validate_structure.py --source /path/to/original/SKILL.md
```

行为回归为人工检查：逐个使用 [cases](tests/ai-product-development/cases) 的输入，记录实际 Profile、references、计划和完成判定，与 [expected](tests/ai-product-development/expected) 对照。静态通过不代表模型行为用例已自动通过。

迁移映射、去重与语义疑点见 [重构记录](docs/decisions/001-modularize-ai-product-development.md)。
