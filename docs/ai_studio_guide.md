# AI Studio - 多 Agent 协作系统

Auberon 作为总控，协调多个专业 Agent + 外部工具协同工作。

## 🏢 系统架构

```
你 (用户)
  ↓
[Auberon - 总控/CEO] 👔
  ↓ 任务分析 → 分配
  ├─ [Deepseek-Analyst] 🔬 (深度分析、代码)
  ├─ [Kimi-Creative] 🎨 (写作、创意)
  ├─ [Qwen-Researcher] ⚡ (搜索、查询)
  └─ [Hunyuan-General] 🌐 (通用、协调)
        ↓
  [外部工具]
  ├─ x-tweet-fetcher (推文获取)
  ├─ sogou-wechat (微信搜索)
  └─ x-discover (推文发现)
        ↓
  [结果汇总] → 给你
```

## 🤖 Agent 分工

| Agent | 角色 | 专长 | 使用场景 |
|-------|------|------|---------|
| **Deepseek-Analyst** | 深度分析师 | 复杂分析、代码编程、策略规划 | "写一段代码"、"分析数据" |
| **Kimi-Creative** | 创意总监 | 写作创作、文案生成、头脑风暴 | "写一篇文章"、"创作故事" |
| **Qwen-Researcher** | 研究员 | 快速查询、资料搜索、翻译 | "搜索资料"、"翻译" |
| **Hunyuan-General** | 通用助手 | 日常对话、通用任务 | "帮我决定"、"一般问题" |
| **Auberon** | 总控 | 任务分配、结果汇总 | 自动选择或协调多个 Agent |

## 🛠️ 外部工具集成

### 已安装工具

**x-tweet-fetcher** - X/Twitter 数据获取
```bash
# 获取推文
python x-tweet-fetcher/scripts/fetch_tweet.py --url "https://x.com/..." --json

# 搜索微信文章
python x-tweet-fetcher/scripts/sogou_wechat.py --keyword "AI" --json

# 发现推文
python x-tweet-fetcher/scripts/x_discover.py --keywords "AI,LLM" --json
```

## 🚀 使用方式

### 1. 简单任务（自动路由）

```bash
python scripts/ai_studio.py --task "分析这个推文 https://x.com/..."
```

**流程：**
1. Auberon 分析任务
2. 调用 x-tweet-fetcher 获取推文
3. 分配给 Deepseek-Analyst 分析
4. 返回分析结果

### 2. 复杂任务（多 Agent 协作）

```bash
python scripts/ai_studio.py --task "搜索最新的 AI 发展趋势，然后写一份报告"
```

**流程：**
1. Auberon 分解任务
2. Qwen-Researcher 搜索资料
3. x-tweet-fetcher 获取相关推文
4. Deepseek-Analyst 分析趋势
5. Kimi-Creative 撰写报告
6. Auberon 汇总结果

### 3. 直接指定 Agent

```bash
# 只用创意 Agent 写作
python scripts/ai_studio.py --task "写一个故事" --agent creative

# 只用分析 Agent 编程
python scripts/ai_studio.py --task "写一个 Python 爬虫" --agent analyst
```

### 4. Discord 集成

在 Discord 中直接 @Auberon：

```
@Auberon 分析这个推文 https://x.com/elonmusk/status/...
→ [自动获取推文] → [Deepseek 分析] → [回复分析结果]

@Auberon 搜索微信关于 AI 的文章
→ [调用 sogou_wechat] → [Qwen 总结] → [回复文章列表]

@Auberon 发现 Twitter 上关于 bitcoin 的热门讨论
→ [调用 x_discover] → [Qwen 整理] → [回复讨论摘要]
```

## 📋 任务类型示例

| 你说 | 系统处理 | 使用的 Agent + 工具 |
|------|---------|-------------------|
| "分析这个推文" | 获取推文 + 深度分析 | x-tweet-fetcher + Deepseek |
| "搜索 AI 资料并写报告" | 搜索 + 分析 + 写作 | Qwen + x-discover + Kimi |
| "翻译这段代码" | 代码理解 + 翻译 | Deepseek + 代码工具 |
| "帮我回复这封邮件" | 理解内容 + 撰写回复 | Kimi |
| "今天有什么新闻" | 搜索 + 汇总 | Qwen + 搜索工具 |
| "创意营销方案" | 头脑风暴 + 方案撰写 | Kimi |

## 🔧 配置

### 环境变量
```bash
# AI Studio 配置
export AI_STUDIO_MODE=auto  # auto, single, collaborative
export DEFAULT_AGENT=coordinator

# x-tweet-fetcher 路径
export X_TWEET_FETCHER_PATH=/root/.openclaw/workspace/x-tweet-fetcher
```

### Discord Bot 集成
在 `auberon_gateway.py` 中集成 AI Studio：
```python
from ai_studio import AIStudio

studio = AIStudio()
result = await studio.execute_task(message_content)
```

## 📊 任务统计

```bash
python scripts/ai_studio.py --stats
```

## 🎯 未来扩展

- [ ] 更多外部工具集成
- [ ] Agent 间对话机制
- [ ] 任务流水线自动化
- [ ] 学习用户偏好
- [ ] 成本追踪和优化

## 📞 支持

有问题随时问 Auberon！
