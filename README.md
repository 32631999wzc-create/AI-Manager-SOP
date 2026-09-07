# AI-Manager-SOP

本仓库维护可复用的 AI 产品开发技能，正式入口为 [AI Product Development](skills/ai-product-development/SKILL.md)。依据交付目标、范围、已有资产、依赖和风险调整产品定义、设计、实现、评估和发布的深度。

## 当前边界

Phase 1 模块化与按需读取验证已经完成，并已进行内容清洗。Skill 是 Codex 可读取的指令包；schema 保留原文结构示意，不代表已经实现项目状态存储、实例验证或自动恢复。下一阶段只完成 Executable Validation，范围见 [Phase 2 任务书](docs/decisions/002-content-cleanup-and-phase-2-plan.md)；当前尚未开始实现。

## 结构

```text
skills/ai-product-development/
├── SKILL.md                  # Kernel + Router
├── references/
│   ├── lifecycle/            # 八节点
│   └── runtime/              # 六项能力及共享 Gates，七个文件
├── schemas/                  # 五个 YAML 文件，八个原始对象
└── templates/                # execution-plan.md
tests/ai-product-development/
├── cases/                    # 八个人工行为场景
├── expected/
├── behavior-contract.md      # 行为场景共用边界
├── migration-manifest.json    # 533 条源规则和对象指纹
├── section-migration.json     # 70 个源标题完整映射
├── structure_contract.py
├── validate_structure.py
├── test_phase1.py
└── routing/                  # 三个隔离只读场景及真实 trace
docs/
├── architecture.md
└── decisions/
examples/ai-product-development/
```

先读 Kernel，再按当前任务加载 Profile 或相关节点、Runtime。生成八节点 Profile 不意味着读取八节点详情；已确认可复用的 VERIFY 资料不自动触发逐节点读取。依赖闭包确实要求补充工作时再加载相应规则。详细规则只在 canonical location 维护。

## 检查与测试

需要 Python 3.10+、PyYAML；实际 Routing Test 还需要已认证的 Codex CLI 及正常工作的只读沙箱。在仓库根目录运行：

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p test_phase1.py
```

结构验证检查 frontmatter、Kernel 章节、节点与能力、模块集合及路由、内部文件和锚点、Gate、schema 字段与枚举、迁移完整性和明显详细规则重复。负例测试验证判定器能发现缺陷。

可额外核验用户保存的原始文件：

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py --source /path/to/original/SKILL.md
```

[Routing Test 方法与证据](tests/ai-product-development/routing/README.md)说明如何独立启动 R1/R2/R3、回放实际工具输出并判定 PASS/WARN/FAIL。静态链接检查不能代替 Routing Test；模型自述不能独立支持 PASS。

八组 [cases](tests/ai-product-development/cases) / [expected](tests/ai-product-development/expected) 仍为人工行为回归骨架，统一遵循 [行为契约](tests/ai-product-development/behavior-contract.md)，本次不宣称它们已执行。完整迁移及源文疑点见 [重构记录](docs/decisions/001-modularize-ai-product-development.md)。
