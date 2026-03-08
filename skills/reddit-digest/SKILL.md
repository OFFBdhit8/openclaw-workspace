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

### 自动（融入心跳/早报）
每日早报中包含 Reddit 精华

## 抓取方法

### 方法 1（首选）：PullPush API
Reddit 官方 API 封了服务器 IP，用 PullPush 第三方 API 替代。

```bash
# 获取某 subreddit 过去 24h 热帖（按分数排序，取 10 条）
curl -s "https://api.pullpush.io/reddit/search/submission/?subreddit=SaaS&sort=score&size=10&after=$(date -d '1 day ago' +%s)"
```

参数说明：
- `subreddit` — 子版块名（不带 r/）
- `sort` — 排序：score（热度）/ created_utc（时间）
- `size` — 返回条数（最大 100）
- `after` — Unix 时间戳，只返回此时间之后的帖子
- `q` — 搜索关键词（可选）

返回 JSON，关键字段：
- `title` — 标题
- `selftext` — 正文
- `score` — 投票分数
- `num_comments` — 评论数
- `permalink` — 帖子链接（拼接 https://reddit.com）
- `author` — 作者
- `created_utc` — 发帖时间

### 方法 2（备用）：Google 搜索
```
camofox_navigate → @google_search → "site:reddit.com r/SaaS [关键词]"
```
只能看摘要，无法进入帖子详情。

### ⚠️ 不可用的方法
- Reddit 官方 JSON API（.json 后缀）→ 403
- Reddit RSS（.rss）→ 403
- Camofox 直接访问 reddit.com → blocked by network security
- web_fetch reddit.com → 403

## 输出格式

```markdown
## Reddit 精华 — YYYY-MM-DD

### r/SaaS
1. **标题** (XX↑, XX评论) — 一句话摘要
2. ...

### r/SideProject
1. ...
```

## 多 subreddit 批量抓取

逐个调用 PullPush API，每个间隔 1 秒避免限流：
```bash
for sub in SaaS SideProject Entrepreneur; do
  curl -s "https://api.pullpush.io/reddit/search/submission/?subreddit=$sub&sort=score&size=5&after=$(date -d '1 day ago' +%s)"
  sleep 1
done
```
