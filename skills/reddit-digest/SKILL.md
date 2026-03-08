---
name: reddit-digest
description: "Reddit 每日精华 — 追踪关注的 subreddit 热帖。触发词：Reddit、红迪、r/、社区动态"
---

# Reddit Digest Skill

## 关注的 Subreddit
- r/SideProject — 独立开发者项目
- r/SaaS — SaaS 产品讨论
- r/Entrepreneur — 创业
- r/OpenClaw — OpenClaw 社区
- r/LocalLLaMA — 本地 AI 模型
- r/MachineLearning — ML 前沿
- r/webdev — Web 开发趋势

## 执行方式

### 手动
老板说"Reddit 有什么新的"时触发

### 自动（融入 morning-brief）
每日早报中包含 Reddit 精华

## 抓取方法
用 Camofox：
```
camofox_navigate → @reddit_search → "subreddit:[名称] sort:top t:day"
```

或用 web_fetch 抓 Reddit JSON API：
```
https://www.reddit.com/r/[subreddit]/top.json?t=day&limit=5
```

## 筛选标准
- 点赞 > 50
- 评论 > 10
- 和赚钱/AI/开发相关

## 输出格式
每个 subreddit 选 top 2-3：
- 标题 + 一句话摘要 + 链接
- 如果有商业机会标记 🔴
- 保存到 `memory/research/reddit-[日期].md`
