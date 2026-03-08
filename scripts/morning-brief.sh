#!/bin/bash
# morning-brief.sh — 每日早报，08:00 推送到飞书
export PATH="/root/.nvm/versions/node/v22.22.0/bin:/root/.bun/bin:$PATH"

openclaw run --message '
## 每日早报 — 推送到飞书

执行以下步骤，然后把结果通过飞书发给老板：

### 1. AI/科技新闻（3-5条）
用 web_search 搜索过去 24 小时的 AI 和科技重要新闻。
筛选标准：和赚钱相关的、行业变动、新工具发布、融资消息。
每条：标题 + 一句话摘要 + 链接

### 2. 今日待办
读取 memory/ 目录最近的日志，提取未完成的任务。
读取 .learnings/FEATURE_REQUESTS.md 中 status=pending 的项目。

### 3. 我能帮你做的事
基于当前目标和待办，主动建议 2-3 件我今天可以自主完成的任务。

### 4. 市场机会（如果有）
如果最近调研中发现了值得关注的机会，简要提醒。

### 格式要求
- 简洁，不废话
- 用飞书消息发送，不要太长
- 重要的加 🔴，一般的加 🟡
' 2>&1 >> /root/.openclaw/workspace/memory/morning-brief.log
