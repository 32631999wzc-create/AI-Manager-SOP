# Feedback Organizer Golden MVP

这是 Phase 3 的固定产品样例，用来证明 Skill 能把一个产品从计划持续推进到可运行、可验证的交付物。它导入 CSV/JSON 反馈，去重，整理主题、情绪、紧急程度和证据引用，并输出 JSON 与 Markdown。

运行：

```sh
python -B -X utf8 feedback_organizer.py sample-feedback.csv --json-output output.json --markdown-output report.md
```

可用 `--source support` 只整理指定来源。

分类器保持确定性，使仓库验收不依赖网络或密钥。真实模型 Provider、多人协作、云端存储和生产部署不属于本 Golden MVP。
