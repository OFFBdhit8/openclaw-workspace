# MEMORY.md - 长期记忆

## 老板画像
- 称呼：老板
- 启晋娴达工作室，目标暴富，结果导向
- 偏好：快准狠，不废话，中文交流
- 技术水平：熟悉 OpenClaw/Discord/API 配置，能看懂代码
- 风格：狼性，速度就是金钱

## 基础设施
- 服务器：腾讯云轻量 43.163.7.171，Ubuntu 6.8.0-101，4G 内存
- 主机 Gateway：端口 18789，默认模型 gpt-5.4
- 救援机 Gateway：端口 19789，默认模型 claude-sonnet-4.5
- 飞书机器人：主机已切到新 App ID `cli_a920641af8b81bb4`；救援机仍可用
- Discord Bot：服务器 1473676822960144560
- API 供应商：
  - ikuncode（主力）：Claude/GPT/Grok，计费 https://api.ikuncode.cc/pricing
  - 阿里云百炼 Coding Plan（Lite ¥40/月，18000次/月，到期 2026-04-08）
  - DeepSeek 官方（Horizon 打分用）
  - Kimi 官方（长上下文备用）
- 老板常用模型：ikuncode-gpt 5.4 / ikuncode-grok 4.2
- 双机已补齐 4 路 provider（Claude / GPT / Gemini / Grok），共 29 个模型别名
- Camofox 反检测浏览器：端口 9377
- fail2ban 已启用；双向 watchdog 每 15 分钟互查主/救援 Gateway
- 内存常年偏紧，Swap 兜底，Camofox 是大头

## 工具链
- X 推文抓取：fetch_tweet.py（L1）→ Camofox（L2）→ Grok（L3）
- 搜索优先级：Camofox Google（免费）→ DuckDuckGo → Brave → Tavily
- GitHub CLI：账号 OFFBdhit8
- 飞书全套：IM/日历/任务/多维表格/文档/知识库
- 热加载：`gateway.reload = "hybrid"`，手动触发用 `kill -SIGUSR1 <PID>`
- 模型路由：默认主脑 GPT 5.4；便宜主力 GPT 5.1 系；高频轻任务优先百炼/其次 Gemini Flash；情报层 Grok；专家层 Claude Sonnet
- Moltbook 自动化：Corbin 已接入 `ikuncode-gpt/gpt-5.4`（thinking=medium），模型写文案，本地脚本管风控/频率/quiet hours

## 关键认知
- 社区共识：智能体占三成，免疫系统占七成
- 外部 skills 大多质量堪忧，偷思路比直接装更安全
- 赚钱闭环：做免费工具引流 → 铺目录曝光 → 冷触达找客户
- 审计纪律：先审计再动作；群里只汇报结构化结论，不裸显敏感配置
- 本地优化可默认直接做；任何对外动作仍需老板确认

## 待探索
- .issues/ 本地任务调度系统
- listing-swarm / engineering-as-marketing / cold-outreach 三件套
- 数字产品变现路径（Whop / Gumroad / 自建）
- 第一个产品方向：AI 内容复用工具（待老板拍板）

## Skills 武器库（35 个）
赚钱类：engineering-as-marketing / listing-swarm / cold-outreach / affiliate-master / go-to-market / competitor-analysis-report / biz-reporter
安全类：bounty-hunter-pro（漏洞赏金，非找赏金活动）
已有：market-research / content-factory / earnings-tracker / reddit-digest / grok-research / x-account-analysis / last30days / second-brain / self-improving 等
