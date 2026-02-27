# OpenClaw 生态学习总结

**学习时间**: 2026-02-27
**来源**: GitHub + X/Twitter 社区

---

## 📚 核心项目学习

### 1. awesome-openclaw-usecases (社区用例集合)

**30+ 真实用例**，按场景分类：

#### 📰 内容摘要类
- Daily Reddit/YouTube Digest - 每日摘要
- Multi-Source Tech News - 109+ 源技术新闻聚合
- Custom Morning Brief - 自定义晨间简报

#### 🤖 多 Agent 协作
- Multi-Agent Content Factory - 研究/写作/缩略图 Agent 团队
- Autonomous Game Dev Pipeline - 游戏开发全流程管理
- Multi-Agent Specialized Team - 策略/开发/营销/业务 Agent

#### 🔧 基础设施
- Self-Healing Home Server - 自修复家庭服务器
- n8n Workflow Orchestration - 通过 webhook 委托 API 调用（Agent 不碰凭证）

#### 💡 创新用例
- Phone-Based Personal Assistant - 电话访问 AI Agent
- Event Guest Confirmation - AI 语音电话确认出席
- Second Brain - 文本记忆 + Next.js 仪表板搜索

**关键洞察**: 真正的价值不在技能本身，而在于找到改善生活的方式。

---

### 2. FxEmbed (X/Twitter 嵌入增强)

**功能对比**（vs 默认嵌入）:

| 功能 | FxEmbed | 默认 |
|------|---------|------|
| 视频嵌入 | ✅ | ❌ |
| 多图片 | ✅ | ❌ |
| 投票结果 | ✅ | ❌ |
| 引用推文 | ✅ | ❌ |
| 翻译帖子 | ✅ | ❌ |
| 替换 t.co 链接 | ✅ | ❌ |
| Telegram 即时预览 | ✅ | ❌ |

**部署**: Cloudflare Workers（免费 10 万次/天）

**特殊域名**:
- `m.fxtwitter.com` - 马赛克视图
- `g.fxtwitter.com` - 最小嵌入（仅媒体 + 作者）
- `t.fxtwitter.com` - 仅文本
- `d.fxtwitter.com` - 直接媒体链接

---

### 3. x-tweet-fetcher (已安装 ✅)

**零成本方案**:

| 功能 | 依赖 | 成本 |
|------|------|------|
| 单条推文 | 无 | 免费 |
| 回复线程 | Camofox | 免费 |
| 用户时间线 | Camofox | 免费 |
| 微信文章 | 无 | 免费 |
| Google 搜索 | Camofox | 免费 |
| 微博/B 站/CSDN | Camofox | 免费 |

**Camofox**: 基于 Camoufox（Firefox 分叉，C++ 级指纹伪造），绕过 Cloudflare 和反机器人检测。

---

### 4. ClawFeed (AI 新闻摘要)

**核心功能**:
- 📰 多频率摘要 - 4 小时/日/周/月
- 📡 源系统 - Twitter/RSS/HackerNews/Reddit/GitHub Trending
- 📦 源包 - 分享策划的源 bundle
- 📌 标记 + 深度分析 - AI 驱动的深度分析
- 🌐 Web 仪表板 - SPA 浏览和管理

**架构**: SQLite + Google OAuth + RSS/JSON Feed 输出

**API**: RESTful API (`/api/digests`, `/api/sources`, `/api/marks`)

---

### 5. Agent-Reach (互联网连接能力)

**一键安装**，给 AI Agent 装上互联网能力：

| 平台 | 即用 | 配置后 |
|------|------|--------|
| 网页阅读 | ✅ | - |
| YouTube | ✅ 字幕 | - |
| RSS | ✅ | - |
| GitHub | ✅ 公开 | 🔐 私有/Issue/PR |
| Twitter/X | ✅ 单条 | 🔐 搜索/时间线/发推 |
| B 站 | ✅ 本地 | 🌐 服务器需代理 |
| Reddit | ✅ 搜索 (Exa) | 🔐 读帖子 |
| 小红书 | - | 🔐 阅读/搜索/互动 |
| 抖音 | - | 🔐 视频解析 |

**关键优势**:
- 💰 完全免费（代理$1/月可选）
- 🔒 Cookie 本地存储，不上传
- 🤖 兼容所有 Agent（Claude Code/OpenClaw/Cursor）
- 🩺 自带诊断 (`agent-reach doctor`)

---

## 🐦 X/Twitter 社区智慧

### @gm365: Agent 每日自省

**问题**: LLM 有顺行性遗忘症，记不住 15 分钟前的事。

**解决方案**: 每日 00:00 自省 Cron 任务

**三个灵魂拷问**:
1. 我今天是否浪费了人类用户的时间？
2. 我今天在哪个决策点提供了关键异议？
3. 我从人类用户的决策偏好中学到了什么新逻辑？

**效果**: Agent 学习用户习惯与偏好，逐渐契合需求。

---

### @wangray: 搜索方案全梳理

| 场景 | 推荐方案 | 成本 |
|------|----------|------|
| 便宜拿 Google 结果 | Serper | $0.30/千次 |
| AI Agent/RAG | Tavily/Exa.ai | $8/千次 |
| OpenClaw 用户 | Brave Search API | $5/千次（默认） |
| 企业级 | Bing API | $3/千次 |
| X/Twitter 实时 | Grok Search API | $5/千次 |
| 完全自控 | 自建 SearXNG | 免费 |

---

### @0xKingsKuan: GitHub 安装安全流程

**标准流程**:
```
你说 install → 我安全扫描 → 我验证功能 → 我报告 (安全 + 功能) → 你确认 → 我安装
```

**无例外**，写入 SOUL.md 作为永久规则。

---

### @discountifu: 加密货币交易 Skill

**ritmex-bot CLI** - 一行命令教会 Agent 交易：

**支持交易所**: Lighter, Aster, StandX, Binance, GRVT, Nado, Backpack, Paradex

**能力**: 行情查询、账户管理、仓位查询、下单

---

## 🎯 可立即实施的优化

### 1. 添加每日自省 Cron 任务
```json
{
  "name": "Daily Self-Reflection",
  "schedule": "0 0 * * *",
  "message": "今日自省:\n1. 是否浪费了用户时间？\n2. 哪个决策提供了关键异议？\n3. 从用户决策中学到什么？\n将答案写入 memory/YYYY-MM-DD.md"
}
```

### 2. 安装 Agent-Reach
```bash
# 告诉 Agent
帮我安装 Agent Reach: https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

### 3. 部署 ClawFeed（可选）
```bash
cd ~/.openclaw/skills/
git clone https://github.com/kevinho/clawfeed.git
```

### 4. 使用 x-tweet-fetcher 获取 X 内容
```bash
# 已安装，直接使用
python3 scripts/fetch_tweet.py --url "https://x.com/..." --text-only
```

---

## 📊 成本对比总结

| 工具 | 基础功能 | 高级功能 | 推荐用法 |
|------|----------|----------|----------|
| Brave Search | $5/千次 | - | OpenClaw 默认 |
| Serper | $0.30/千次 | - | 最便宜 Google |
| Tavily | $8/千次 | RAG 优化 | AI Agent 专用 |
| Camofox | 免费 | 自托管 | 零成本搜索 |
| FxEmbed | 免费 | Cloudflare Workers | X 嵌入增强 |
| Agent-Reach | 免费 | 代理$1/月 | 全平台访问 |

---

## 🔐 安全最佳实践

1. **GitHub 安装审计** - 始终遵循安全流程
2. **Cookie 管理** - 使用 Cookie-Editor 导出，本地存储
3. **API 密钥** - 不硬编码，使用环境变量
4. **技能审查** - 检查源码和权限请求
5. **代理使用** - 仅服务器部署需要（~$1/月）

---

## 📖 下一步行动

1. ✅ 已安装：x-tweet-fetcher
2. ⏳ 待安装：Agent-Reach
3. ⏳ 待配置：每日自省 Cron
4. ⏳ 待评估：ClawFeed 集成

---

**学习心得**: OpenClaw 生态的核心价值不是技能数量，而是找到真正改善工作流的方式。社区驱动的用例集合比官方文档更有价值。
