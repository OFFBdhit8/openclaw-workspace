#!/bin/bash
# weekly-research.sh — 每周一 09:00 自动痛点调研
export PATH="/root/.nvm/versions/node/v22.22.0/bin:/root/.bun/bin:$PATH"

openclaw run --message '
## 每周痛点调研

使用 market-research skill 的流程，调研以下领域过去 7 天的痛点：

1. AI Agent / OpenClaw 生态 — 用户在抱怨什么、缺什么
2. AI 工具变现 — 什么 AI 工具在赚钱、什么方向有空白
3. 独立开发者 / 小工作室 — 什么产品需求没被满足

每个领域给出 top 3 痛点，按"付费意愿 × 竞品空白"排序。

结果：
1. 保存到 memory/research/weekly-$(date +%Y-%m-%d).md
2. 通过飞书发给老板，简洁版（每个领域 top 1 + 建议）
3. 如果发现评分 > 8 的高价值机会，标记 🔴 重点提醒
' 2>&1 >> /root/.openclaw/workspace/memory/research/weekly.log
