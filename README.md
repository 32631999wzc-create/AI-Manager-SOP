# AI-Manager-SOP

本仓库维护可复用的 AI 产品开发技能，正式入口为 [AI Product Development](skills/ai-product-development/SKILL.md)。依据交付目标、范围、已有资产、依赖和风险调整产品定义、设计、实现、评估和发布的深度。

## 当前边界

Phase 1 模块化与按需读取、Phase 2 Executable Validation 已完成。Phase 3 已把既有八个 canonical runtime object 落为本地单用户持续交付 Runtime：`.ai-product/` 保存已验证状态，支持初始化、下一任务、检查点、跨进程恢复、Registry 写入和局部重规划。Feedback Organizer 是固定 Golden MVP；范围与验收见 [Phase 3 决策记录](docs/decisions/004-phase-3-continuous-golden-mvp.md)。

## 结构

```text
skills/ai-product-development/
├── SKILL.md                  # Kernel + Router
├── references/
│   ├── lifecycle/            # 八节点
│   └── runtime/              # 六项能力及共享 Gates，七个文件
├── schemas/                  # 五个 YAML 文件，八个原始对象
├── templates/                # execution-plan.md
└── scripts/                  # 只读 validator 与本地 continuous runtime
tests/ai-product-development/
├── cases/                    # 八个人工行为场景
├── expected/
├── behavior-contract.md      # 行为场景共用边界
├── phase2/                   # 验证契约、固定 fixtures 与行为证据
├── phase3/                   # 持续状态与 Golden MVP 验证
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
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase2*.py"
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase3*.py"
python -B -X utf8 tests/ai-product-development/routing/verify_evidence.py
python -B -X utf8 tests/ai-product-development/phase2/behavior/verify_behavior.py
```

结构验证检查 frontmatter、Kernel 章节、节点与能力、模块集合及路由、内部文件和锚点、Gate、schema 字段与枚举、迁移完整性和明显详细规则重复。负例测试验证判定器能发现缺陷。

可额外核验用户保存的原始文件：

```sh
python -B -X utf8 tests/ai-product-development/validate_structure.py --source /path/to/original/SKILL.md
```

[Routing Test 方法与证据](tests/ai-product-development/routing/README.md)说明如何独立启动 R1/R2/R3、回放实际工具输出并判定 PASS/WARN/FAIL。静态链接检查不能代替 Routing Test；模型自述不能独立支持 PASS。

八组 [cases](tests/ai-product-development/cases) / [expected](tests/ai-product-development/expected) 已对应到 [Phase 2 固定 fixtures](tests/ai-product-development/phase2/README.md)，并统一遵循 [行为契约](tests/ai-product-development/behavior-contract.md)。确定性回归与八个隔离 Codex trace 均已通过；Phase 3 的本地状态命令见 [Continuous Project Runtime](skills/ai-product-development/scripts/project_runtime/README.md)，固定产品见 [Feedback Organizer](examples/ai-product-development/golden-feedback-organizer/README.md)，四会话证据见 [Phase 3 Golden 报告](tests/ai-product-development/phase3/golden/report.md)。[行为报告](tests/ai-product-development/phase2/behavior/report.md)记录实际读取与修复，[P2 完成记录](docs/decisions/003-phase-2-executable-validation.md)记录实现边界。模型自述不替代实际读取证据。完整迁移及源文疑点见 [重构记录](docs/decisions/001-modularize-ai-product-development.md)。
