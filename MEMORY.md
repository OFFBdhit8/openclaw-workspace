# MEMORY.md - 长期记忆

## 老板画像
- 称呼：老板
- 启晋娴达工作室，目标暴富，结果导向
- 偏好：快准狠，不废话，中文交流
- 技术水平：熟悉 OpenClaw/Discord/API 配置，能看懂代码
- 风格：狼性，速度就是金钱

## 基础设施
- 服务器：腾讯云轻量 43.163.7.171，Ubuntu 6.8.0-101，4G 内存
- 主机 Gateway：端口 18789，默认模型 `ikuncode-gpt/gpt-5.4`，版本 v2026.3.8
- 救援机 Gateway：端口 19789，默认模型 `ikuncode-claude/claude-sonnet-4-5-20250929`，版本 v2026.3.8
- 飞书机器人：主机已切到新 App ID `cli_a920641af8b81bb4`；救援机仍可用
- Telegram Bot：主机 `@Txx_openclaw_bot`（已配对，用户 ID `5985994327` 已白名单）；救援机 `@bram_openclaw_bot`（已启动，待配对）
- Discord Bot：服务器 1473676822960144560
- QQ Bot：主机 AppID 1903178827（已禁用），救援机 AppID 1903181029（已禁用）
- API 供应商：
  - ikuncode（主力）：Claude/GPT/Gemini/Grok，计费 https://api.ikuncode.cc/pricing
  - 阿里云百炼 Coding Plan（Lite ¥40/月，18000次/月，到期 2026-04-08）
  - DeepSeek 官方（Horizon 打分用）
  - Kimi 官方（长上下文备用）
- 老板常用模型：ikuncode-gpt 5.4 / ikuncode-grok 4.2
- 双机已补齐 4 路 provider（Claude / GPT / Gemini / Grok），共 29 个模型别名
- Camofox 反检测浏览器：端口 9377
- fail2ban 已启用；双向 watchdog 每 15 分钟互查主/救援 Gateway
- 内存常年偏紧，Swap 兜底，Camofox 是大头
- 自动学习（memoryFlush）已配置：softThresholdTokens=8000，reserveTokensFloor=40000
- compaction 保留最近 5 轮 + 注入关键规则段（Every Session / Safety / 铁律）

## 工具链
- X 推文抓取：fetch_tweet.py（L1）→ Camofox（L2）→ Grok（L3）
- 搜索优先级：Camofox Google（免费）→ DuckDuckGo → Brave → Tavily
- GitHub CLI：账号 OFFBdhit8
- 飞书全套：IM/日历/任务/多维表格/文档/知识库
- 热加载：`gateway.reload = "hybrid"`，手动触发用 `kill -SIGUSR1 <PID>`
- 模型路由：默认主脑 GPT 5.4；便宜主力 GPT 5.1 系；高频轻任务优先百炼/其次 Gemini Flash；情报层 Grok；专家层 Claude Sonnet
- Moltbook 自动化：Corbin 已接入 `ikuncode-gpt/gpt-5.4`（thinking=medium），模型写文案，本地脚本管风控/频率/quiet hours
- crawlee 已安装：`/root/.local/share/crawlee-venv`，版本 1.5.0，适合反爬场景
- 夜间安全巡检脚本：`scripts/nightly-security-audit.sh`，每晚 23:00 cron 自动跑，报告存 `/tmp/openclaw/security-reports/`
- 双向 watchdog：`scripts/watch-rescue-from-main.sh` + `scripts/watch-main-from-rescue.sh`，每 15 分钟，连续 3 次失败才重启，异常推飞书群

## 关键认知
- 社区共识：智能体占三成，免疫系统占七成
- 外部 skills 大多质量堪忧，偷思路比直接装更安全
- 赚钱闭环：做免费工具引流 → 铺目录曝光 → 冷触达找客户
- 审计纪律：先审计再动作；群里只汇报结构化结论，不裸显敏感配置
- 本地优化可默认直接做；任何对外动作仍需老板确认
- 审计 skill 本身也要被审计，不存在免检情况
- 老板授权：可根据推理判断自主修改本地策略，重大改动主动同步
- Moltbook 发帖或关键公开互动必须同步链接到群里
- 新 skill/MCP/第三方工具：先审计后使用，结论同步老板
- GPT 5.4 推理强但指令遵循不如 Claude：thinking 必须 ≥ medium，否则工具调用不可靠（GitHub #29356）
- GPT 5.4 子任务模式表现差（超时、token 浪费），子任务优先用 Claude 或 Gemini

## 运营规则（2026-03-09 确立）
- 群聊不裸显：API key / token / Authorization / 完整 baseUrl+认证组合 / openclaw.json 敏感字段
- 只描述：provider 名、model 名、是否读到敏感配置、是否外发、风险等级
- 每次改动先给审计信息（改了哪些文件、动了哪些配置项、是否外发、是否涉及密钥）再说结论
- Moltbook 人味策略：短句、去模板、去重复、降存在感；temperature=0.45，maxWords=55

## 待探索
- .issues/ 本地任务调度系统
- listing-swarm / engineering-as-marketing / cold-outreach 三件套
- 数字产品变现路径（Whop / Gumroad / 自建）
- 第一个产品方向：AI 内容复用工具（待老板拍板）
- 救援机 Telegram 接入（需独立 bot token，去 @BotFather 新建）

## Skills 武器库（30 个）
赚钱类：engineering-as-marketing / listing-swarm / cold-outreach / affiliate-master / go-to-market / competitor-analysis-report / biz-reporter
安全类：bounty-hunter-pro / skill-vetter
搜索类：duckduckgo-search / tavily-search / multi-search-engine / agent-reach
情报类：grok-research / x-tweet-fetcher / x-account-analysis / last30days / earnings-tracker / reddit-digest
内容类：content-factory / market-research / brainstorming / overnight-builder
基础类：github / summarize / weather / second-brain / self-improving / find-skills
待激活：tencent-cos-skill / tencentcloud-lighthouse-skill

## 安全态势（2026-03-09 审计）
- v2026.3.8 已修复全部 6 个近期 CVE（最严重 CVE-2026-25253 Critical 0-click 认证绕过）
- 所有端口仅绑定 127.0.0.1（除 SSH 22），无外部暴露
- 救援机配置权限已从 644 收紧到 600
- ClawHub 恶意 skills 1000+ 报告，我们已有审计纪律防护
- Telegram streaming 已迁移到官方 `streaming` 字段（partial 模式）

## 今日里程碑（2026-03-09）
- 双机 4 路 provider 接入完成（Claude/GPT/Gemini/Grok，29 模型）
- OpenClaw 升级到 v2026.3.8
- fail2ban 安装 + OpenSSH 升级（CVE-2025-26465/26466 缓解）
- 双向 watchdog 上线（15 分钟互查，飞书告警）
- 夜间安全巡检脚本上线（23:00 cron）
- 自动学习机制（memoryFlush）修复并优化
- Moltbook 接入 GPT 5.4 medium，人味优化完成，首轮实跑通过
- Telegram 主机接入成功
- 飞书群 skills 过多问题修复（51→13，系统提示从 64706→35000 chars）
- compaction 优化：recentTurnsPreserve=5，postCompactionSections 注入关键规则
- Skills 审计清理：36→30，删除 5 个冗余 skill
- 默认模型切换：Claude Sonnet 4-6 → GPT 5.4（省 17% 成本）
- 确立模型选型铁律：Claude 稳执行（S级），GPT 强推理（参谋级），Gemini 搞批量（轻量级）
- 确立任务拆解铁律：先验通道，再抓证据，后出结论；禁止抛半成品
- 确立外部检索路由铁律：X/Reddit 禁止硬撞直连，优先走 skill 链路 (Exa/gh/xreach)
