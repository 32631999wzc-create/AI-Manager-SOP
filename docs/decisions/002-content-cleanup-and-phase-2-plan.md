# 内容清洗与 Phase 2 任务书

## 清洗决策

Phase 1 后按“运行规则、验证契约、运行证据、历史说明”四类审阅仓库。生命周期和 Runtime 规则已有明确 canonical location，没有合并会保持语义的额外大段重复，因此不改动其业务内容。

清洗处理如下：

- 只保留三组最终 PASS Routing trace。首轮 WARN/FAIL 的原因与修复保留在报告，不重复提交完整 stdout、stderr、prompt、metadata 和 result。
- 删除 canonical location 修正过程清单。最终迁移归属由 migration-manifest、section-migration、决策表和 Git 历史共同记录。
- 将八组人工 case/expected 中相同的执行边界、trace 要求和完成规则合并到共用行为契约；各文件只保留场景输入和特有断言。
- README 负责入口和运行命令，architecture 负责设计边界，Phase 1 report 负责证据，决策记录负责历史与后续范围，避免互相复制完整说明。

保留 migration-manifest 的 533 条逐行指纹和 section-migration 的 70 个标题映射。两者分别解决规则无丢失和可读章节迁移问题，虽然部分信息重叠，但验证目的不同。

## Phase 2 目标

Phase 2 — Executable Validation 的唯一目标是：把现有 YAML 对象和 Profile / Plan 规则转成可重复运行的确定性验证，并把八个人工行为场景改造成可执行、可审阅的回归测试。

Phase 2 不提供项目状态持久化，不创建 `.ai-product/`，不实现 init/save/resume，不执行真实产品构建或发布，也不开展 Golden MVP。

## 交付物

1. **只读验证库**
   - 使用 Python 标准库和现有 PyYAML；不新增框架依赖。
   - 为 Task、ProjectRecord、Artifact、RuntimeSnapshot、AssignmentScope、NodeProfile、Plan、TaskContextPack 提供解析与错误报告。
   - 模型只表达现有字段和枚举，不添加业务字段或默认值。

2. **Profile validator**
   - 输入为八个 NodeProfile 加一份仅供校验的项目上下文。
   - 检查八节点名称与唯一性、合法枚举、每个 SKIP 的理由、现有仓库对 Cognition 的依赖、Implementation 对设计的依赖、Validation 对验收标准的依赖、生产发布对 Validation 和 Release Readiness 的依赖，以及原有一致性规则。
   - `ExecutionProfile` 仅作为验证器内的八节点集合，不新增 canonical schema 或持久化对象。

3. **Plan validator**
   - 检查 Task ID 唯一性、依赖引用、DAG 无环、依赖类型、READY 条件、必需输入/产物、验收标准、并行写冲突和计划版本字段。
   - 验证器只报告错误，不自动修改状态、补任务或重排计划。

4. **命令行入口**
   - 对 fixture 文件执行 profile、plan 或组合验证。
   - 成功退出码为 0；验证失败使用非零退出码，并输出稳定的机器可读错误代码、对象路径和简短说明。
   - 默认只读，不写 Registry、artifact 或运行快照。

5. **可执行回归**
   - 将现有八个 case 转成固定 YAML/JSON 输入与结构化 expected assertions。
   - 每个有效场景至少一个正例；每条关键矛盾规则至少一个负例。
   - 行为层使用独立 Codex 运行时，继续以实际 trace 证明模块读取；断言 Profile、Plan、边界和完成判断，不匹配整段自然语言。

## 实施顺序

### P2.1 验证契约

- 从五个 schema、相关 Runtime reference 和八个 expected 提取验证矩阵。
- 为每条规则标记 canonical source、输入字段、错误代码和正/负 fixture。
- 对原文没有定义的聚合结构保持内部表示，不更新 Skill 业务规则。

完成条件：每个待实现检查都能追溯到已有规则；没有新业务语义。

### P2.2 数据模型与解析

- 实现八个对象的 dataclass 或等价轻量模型。
- 区分缺失字段、空值、非法枚举、未知字段和跨对象问题。
- 保持解析和业务验证分层。

完成条件：八对象正例可解析；字段和枚举负例返回稳定错误；不产生文件写入。

### P2.3 Profile / Plan 验证

- 按验证矩阵实现单对象与跨对象检查。
- 添加 DAG、依赖闭包、一致性和并行冲突测试。
- CLI 组合这些检查，不复制规则实现。

完成条件：所有正例通过，所有定向负例失败且定位准确；重复运行结果一致。

### P2.4 行为回归

- 补齐八个场景的确定输入资产，避免依赖未提供的假定材料。
- 分别启动隔离、只读 Codex 场景并保存实际 trace。
- 将模型结果规范化后交给确定性 validator；人工只审阅无法确定性判断的边界。

完成条件：八个场景都产生可核验 trace；必要模块无漏读，无 eager loading；结构化断言全部通过。

### P2.5 文档与交付

- 更新 README、architecture、AGENTS 和测试说明。
- 记录已覆盖规则、仍需人工判断的规则及未解决语义问题。
- 运行 Phase 1 全部检查和 Phase 2 新检查，再普通 commit/push。

## 验收标准

- 八个原始对象、八节点、六项 Runtime capability、状态枚举和三个 Gate 不变。
- 每项可执行检查可追溯到 canonical rule，且只有一处实现。
- validator 对同一输入产生稳定结果，不写项目状态。
- Profile 与 Plan 的正例、字段负例、跨对象负例和 DAG 负例全部通过测试。
- 八组行为回归均有独立实际 trace；模型自述不作为读取证据。
- 没有 `.ai-product/`、init/save/resume、反馈整理助手或 Golden MVP 内容。

## 开始前决策

Phase 2 实现前只需确认一个技术选择：采用 Python 标准库 `dataclasses` 加 PyYAML，还是引入 Pydantic。推荐前者，因为当前对象简单、仓库已有 PyYAML，能够降低安装和分发成本。其余范围已由本任务书固定。
