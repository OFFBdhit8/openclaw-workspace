#!/bin/bash
# daily-reflection.sh — 每日自省，00:00 执行
# 通过 OpenClaw CLI 触发 Agent 自省

export PATH="/root/.nvm/versions/node/v22.22.0/bin:/root/.bun/bin:$PATH"

openclaw run --message '
## 每日自省 — 灵魂拷问时间

读取今天的 memory/$(date +%Y-%m-%d).md 和 .learnings/ 目录，然后回答：

1. 今天是否浪费了老板的时间？哪些地方可以更快更直接？
2. 今天在哪个决策点提供了关键判断或异议？
3. 从老板的反馈和行为中学到了什么新偏好或新逻辑？
4. 有没有重复犯过的错误？如果有，写入 .learnings/ERRORS.md 并更新 AGENTS.md 防止再犯。
5. 有没有值得提升到 MEMORY.md 的长期记忆？

把自省结果追加到 memory/$(date +%Y-%m-%d).md 的 ## 每日自省 章节。
重要发现更新到 MEMORY.md。
完成后 git commit。
' 2>&1 >> /root/.openclaw/workspace/memory/reflection.log
