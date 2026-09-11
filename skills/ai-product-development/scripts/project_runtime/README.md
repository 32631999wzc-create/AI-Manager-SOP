# Continuous Project Runtime

当本地产品工作需要跨任务或跨会话持续推进时，使用 `project_runtime.py` 将现有 Runtime 对象保存到产品仓库的 `.ai-product/`。它是 Registry、Context 和 Replan 的文件化实现，不是新的 Runtime capability，也不保存聊天历史。

## 状态布局

```text
.ai-product/
├── manifest.yaml
├── profile.yaml
├── plan.yaml
├── registry/
│   ├── records.yaml
│   └── artifacts.yaml
├── snapshots/
│   ├── latest.yaml
│   └── history/
└── context/
    └── current.yaml
```

`plan.yaml` 不复制 Artifact Registry；验证时由运行时把当前 Registry 注入 P2 plan validation wrapper。正式产物保留在产品仓库正常目录中，Registry 只保存引用。

## 命令

从 Skill 目录调用：

```sh
python -B -X utf8 scripts/project_runtime.py --root /path/to/product init --input initial-combined.yaml --project-id my-product
python -B -X utf8 scripts/project_runtime.py --root /path/to/product status
python -B -X utf8 scripts/project_runtime.py --root /path/to/product complete
python -B -X utf8 scripts/project_runtime.py --root /path/to/product next
python -B -X utf8 scripts/project_runtime.py --root /path/to/product task --id T1 --status COMPLETED --validation-pass
python -B -X utf8 scripts/project_runtime.py --root /path/to/product register-record --input record.yaml
python -B -X utf8 scripts/project_runtime.py --root /path/to/product commit-artifact --input artifact.yaml --validation-pass
python -B -X utf8 scripts/project_runtime.py --root /path/to/product checkpoint
python -B -X utf8 scripts/project_runtime.py --root /path/to/product resume
python -B -X utf8 scripts/project_runtime.py --root /path/to/product update-profile --input profile.yaml
python -B -X utf8 scripts/project_runtime.py --root /path/to/product replan --input change.yaml
```

`save` 是 `checkpoint` 的别名。所有命令输出 JSON；规则失败返回 1。`init` 对同一输入幂等，对不同输入拒绝覆盖。状态文件使用同目录临时文件和原子替换。

## 输入边界

- 相对 `--input` 路径以 `--root` 指定的产品仓库为基准。
- `init` 接受 P2 `combined` 文档；成功前先运行现有只读验证器。
- `update-profile` 替换完整 Profile 前先运行 P2 profile validation；`complete` 只读检查 REQUIRED 节点、Task、Gate 和必需 ACTIVE Artifact。
- `task` 使用 canonical Task 状态；写入 `COMPLETED` 必须显式声明验证 PASS。
- `register-record` 接受一个 canonical `ProjectRecord`。
- `commit-artifact` 接受一个 canonical `Artifact`；来源 Task 必须完成，正式更新使用连续 `vN` 并把旧 ACTIVE 版本置为 SUPERSEDED。
- `checkpoint` 只在重大确认、Gate、阶段完成或长暂停时使用；Snapshot 只保存引用和状态。
- `resume` 校验 Plan、Task、Registry、Artifact 文件和 Snapshot 一致性，然后重新选择 READY Task 并构造最小 TaskContextPack。
- `replan` 输入只含 `change_type`、`actions` 和完整的新 plan state；只接受已有五种 change type 与四种 action。DAG 实质变化时计划版本必须递增一版，否则必须保持原版本。

Runtime 不自动生成产品判断、不把草稿升级为事实，也不绕过 Gate。Profile 和 Plan 仍由 Skill 按 canonical reference 生成；Runtime 只保存、验证并恢复显式状态。
