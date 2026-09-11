# Phase 3 验证

本目录验证本地项目状态、跨进程恢复、局部重规划和 Feedback Organizer Golden MVP。测试使用临时产品仓库，不在本仓库根目录创建 `.ai-product/`。

```sh
python -B -X utf8 -m unittest discover -s tests/ai-product-development -p "test_phase3*.py"
```

行为验收还需要独立 Codex 会话产生真实文件读取和工具 trace；静态单元测试不能替代该证据。
## Golden trace

四个场景在同一个临时产品工作区、四个全新 ephemeral Codex 进程中顺序执行：初始化，恢复并构建，需求变化后局部重规划，再次恢复并完成。每个场景保留实际读取、命令输出和 thread id。

```sh
python -B -X utf8 tests/ai-product-development/phase3/golden/run_golden.py --output tests/ai-product-development/phase3/golden/evidence/G-final
python -B -X utf8 tests/ai-product-development/phase3/golden/verify_golden.py
```

Runner 不复用聊天历史，不允许修改 Skill，不使用外部服务。最终证据包含 `.ai-product/`、产品输出和 Completion Criteria 结果。
