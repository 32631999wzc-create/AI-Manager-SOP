# Context

Do not treat chat history as the memory system.

Use:

- current working context;
- active Project Records;
- Project Registry 中与当前任务相关的 ProjectRecord、EvidenceRecord、DecisionRecord 与 Artifact；
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

需要跨会话恢复本地项目时，使用 [Continuous Project Runtime](../../scripts/project_runtime/README.md) 的 `next`、`checkpoint` 和 `resume`。恢复依据 Project Registry、Plan 与 RuntimeSnapshot，不读取旧聊天作为状态源。TaskContextPack 只放当前任务显式请求、相关 Artifact 引用或相关 DecisionRecord 所需的 Evidence/Decision ID，不把完整 Registry eager load 进上下文。
