# Context

Do not treat chat history as the memory system.

Use:

- current working context;
- active Project Records;
- Artifact Registry;
- task-specific retrieval.

For each task, build a minimal context pack:

结构定义：[TaskContextPack](../../schemas/context-pack.yaml)。

Default to the latest `ACTIVE` record or artifact version.

Do not automatically load `SUPERSEDED`, `OUTDATED`, `ARCHIVED`, or `REJECTED` content except for debugging, history comparison, or retrospective work.

If context is too large:

1. remove low-relevance history;
2. use artifact summaries rather than full contents;
3. retrieve only relevant sections;
4. if still too large, split the task.

Do not require a vector database unless project scale or retrieval quality demonstrates a need for one.

## Local Persistence

需要跨会话恢复本地项目时，使用 [Continuous Project Runtime](../../scripts/project_runtime/README.md) 的 `next`、`checkpoint` 和 `resume`。恢复依据 Project Records、Artifact Registry、Plan 与 RuntimeSnapshot，不读取旧聊天作为状态源。
