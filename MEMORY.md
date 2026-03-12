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
- 救援机 Gateway：端口 19789，默认模型 `ikuncode-claude/claude-sonnet-4-5-20250929`，版本 v2026.3.8；Discord 已恢复在线（Bot `@Bram`）
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
- rescue Discord 已收敛到手机端 + 轻社交风格：`streaming=partial`、`chunkMode=newline`、`textChunkLimit=950`、`maxLinesPerMessage=8`、`messages.ackReaction=🥰`、`removeAckAfterReply=true`、`messages.statusReactions={thinking:🤔, tool:🛠️, web:🌐, done:✨, error:⚠️}`、`typingMode=thinking`、`typingIntervalSeconds=4`；频道 prompt 强调第一句直接接话/回答、1-2 行短段落、超 8 行拆第二条、允许轻微嘴甜与互动，但禁止油腻、客服腔和工具过程直播。
- 2026-03-11 08:00-09:20 排查 rescue HTTP 500（agent/embedded request format error）：发现救援机默认模型漂移到 `ikuncode-claude/claude-sonnet-4-6` + `thinkingDefault=high`，先回滚到 `claude-sonnet-4-5` + `thinkingDefault=medium`，再切到 `ikuncode-gpt/gpt-5.4` + medium 做对照；本轮重启与自检后未再复现 500，rescue 当前保持 `GPT 5.4 + medium`。
- 2026-03-11 09:20 清理主机 OpenClaw 配置：`/root/.openclaw/openclaw.json` 中移除了重复显式加载的 `feishu-openclaw-plugin`（只保留 canonical `feishu`）以及无效 `tools.allow` 项 `apply_patch` / `image` / `gateway` / `feishu_*`；重启后 `feishu_chat` tool conflict 消失。剩余 `tools.profile=coding` 的 `apply_patch/image` unknown entries 属于内建 profile 与当前环境的兼容性噪音，不必为日志洁癖继续改主脑策略。
- 2026-03-11 下午 Discord 路由收口：主机 Auberon 与救援 Bram 都回到 `requireMention=true`；`replyToMode` 从 `all` 收到 `first`，避免每个分段都强制原生引用；主机保留更活跃的人味配置，救援保持更克制的应急风格。
- 2026-03-11 下午为排查 Discord `@everyone/@身份组` 不触发，已对 `openclaw/extensions/wecom/node_modules/openclaw/dist/*.js` 与 `plugin-sdk/*.js` 的 live bundle 打过两轮补丁：一轮把 `mentionedEveryone/mentionedRoles` 视为有效 mention，二轮给“只有 mention、无正文”的消息补 `messageText` 兜底，避免掉进 `empty content`。补丁已生效并完成双机重启，但老板实测 `@everyone` 仍不回，说明病灶更可能在更前面的 Discord 入站事件/预处理链，需要下一轮直接抓 raw trace，而不是继续盲修。
- 2026-03-11 为降低 Discord 体感噪音：主机 `tools.profile` 已从 `coding` 改为 `full`；main/rescue 的 `messages.statusReactions.enabled=false`、`removeAckAfterReply=false`、`ackReactionScope=group-mentions`，用轻量 ack 保留一点人味，同时减少 `DiscordReactionListener/RemoveListener` 慢日志。

## 工具链
- X 推文抓取：fetch_tweet.py（L1）→ Camofox（L2）→ Grok（L3）
- 搜索优先级：Camofox Google（免费）→ DuckDuckGo → ask-search（本地 SearxNG 兜底）→ Brave → Tavily
- GitHub CLI：账号 OFFBdhit8
- 飞书全套：IM/日历/任务/多维表格/文档/知识库
- 热加载：`gateway.reload = "hybrid"`，手动触发用 `kill -SIGUSR1 <PID>`
- 模型路由：默认主脑 GPT 5.4；日常编码主力优先百炼 qwen3-coder-next；内容整理/表达包装优先百炼 kimi-k2.5；高频轻任务优先百炼/其次 Gemini Flash；情报层 Grok；专家层 Claude Sonnet
- 五人议会绑定（2026-03-10 定稿）：Auberon→GPT 5.4；Bram→qwen3-coder-next；Corbin→百炼 kimi-k2.5；Doran→Claude Sonnet 4.5；Eamon→Grok 4.1 Fast
- Moltbook 自动化：Corbin 已接入 `ikuncode-gpt/gpt-5.4`（thinking=medium），模型写文案，本地脚本管风控/频率/quiet hours
- crawlee 已安装：`/root/.local/share/crawlee-venv`，版本 1.5.0，适合反爬场景
- 夜间安全巡检脚本：`scripts/nightly-security-audit.sh`，每晚 23:00 cron 自动跑，报告存 `/tmp/openclaw/security-reports/`
- 双向 watchdog：`scripts/watch-rescue-from-main.sh` + `scripts/watch-main-from-rescue.sh`，每 15 分钟，连续 3 次失败才重启，异常推飞书群
- ask-search 本地兜底搜索已上线：SearxNG 容器绑定 `127.0.0.1:18080`，健康检查 / 回滚 / MCP 入口已补齐

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
- rescue CLI 的 `openclaw --profile rescue status` / `gateway probe` 仍偏向探测本地默认 `18789`；救援机实况优先用 `systemctl --user status openclaw-gateway-rescue`、`ss -ltnp | grep 19789` 和日志判断，不把 CLI 的 token mismatch 当作服务故障
- Discord “输入中”不在 `channels.discord.*` 配；应改 `agents.defaults.typingMode` / `typingIntervalSeconds`，不要再写不存在的 `channels.discord.typingIndicator`
- Discord 手机端体验优化优先打在 channel schema + 频道级 prompt：`channels.discord.streaming=partial`、`textChunkLimit`、`maxLinesPerMessage`、`guilds.<id>.channels."*".systemPrompt`；不要把 `systemPrompt` 挂在 guild 根层
- rescue Discord 当前稳定方案：`messages.ackReaction=👀`、`removeAckAfterReply=true`、`messages.statusReactions.enabled=true`、`typingMode=thinking`、`typingIntervalSeconds=4`；这套比只调文案更像“活 bot”
- `agents.defaults.suppressPreToolText` 在当前 OpenClaw v2026.3.8 schema 不受支持；想减少 Discord 废话，优先靠频道 `systemPrompt` 和输出风格约束，不要硬写无效字段
- 2026-03-11 定稿模型路由：默认主脑/综合判断用 `GPT 5.4`；真代码修改默认 `GPT 5.1`，复杂改动升 `GPT 5.4`；内容包装用百炼 `kimi-k2.5`；heartbeat/摘要/分类/巡检用 `Gemini Flash Lite/Flash`；X/社区用 `Grok`；`Claude Sonnet` 只做高风险复核。Qwen 自家模型移出主路由。
- 2026-03-11 定稿“子任务智能切换铁律 v1”：先按任务类型分流；代码默认 `GPT 5.1`，多文件/重构/高不确定任务升 `GPT 5.4`；内容走 `Kimi`；轻活走 `Gemini`；情报走 `Grok`；改 `openclaw.json`、认证/权限/路由、cron/守护逻辑、稳定性或安全边界相关任务时，必须触发 `Claude Sonnet` 二审。子任务回报统一只交：结论 / 改了什么 / 验证结果 / 风险或未完成项 / 是否建议二审。
- 2026-03-11 定稿 skill-first 铁律：命中 X、GitHub、多平台调研等任务时，必须先走对应 skill / 专用通道；`doctor` 或“已安装”不等于真的可用，必须先做 auth / 实测，失败后才允许降级到通用搜索，并明确标注“降级结果”。
- 2026-03-12 主机 Feishu 运行面已从 bundled `feishu` 切换到官方 `@larksuite/openclaw-lark`（plugin id `feishu-openclaw-plugin`）：旧 `feishu` 已禁用，新插件已安装启用并随主 gateway 重启后恢复运行；实测日志确认完整官方工具集（chat / im / calendar / task / doc / oauth 等）均已注册，Feishu channel 已以 websocket 模式启动并解析出 bot open_id。当前唯一残留是 `openclaw doctor` 的 plugin id mismatch 噪音，根因是 **npm 包名 `@larksuite/openclaw-lark` 与 plugin id `feishu-openclaw-plugin` 不一致**，更像上游打包/元数据瑕疵，不是本地主配置脏项。
- 2026-03-12 主机安全收口新定稿：`adp-openclaw` 保留安装但默认禁用；`wecom` 已加本地文件发送白名单（默认仅允许 workspace/tmp/openclaw 相关目录，可通过 `WECOM_LOCAL_FILE_ALLOWLIST` 扩展）；`plugins.installs` 已补 pinned spec / integrity / shasum / resolved metadata。

## 运营规则（2026-03-09 确立）
- 群聊不裸显：API key / token / Authorization / 完整 baseUrl+认证组合 / openclaw.json 敏感字段
- 只描述：provider 名、model 名、是否读到敏感配置、是否外发、风险等级
- 每次改动先给审计信息（改了哪些文件、动了哪些配置项、是否外发、是否涉及密钥）再说结论
- Moltbook 人味策略：短句、去模板、去重复、降存在感；temperature=0.45，maxWords=55

## 待探索
- .issues/ 本地任务调度系统
- Agent Flow Console：本地 MVP 已重新落盘到 `projects/agent-flow-console/`，用 Node 内置 http + JSON 文件存储；当前可通过 `HOST=0.0.0.0 PORT=4318 node server.js` 启动，已验证 `/api/health` 与 `/api/dashboard` 可用，日志在 `/tmp/agent-flow-console.log`。定位仍是 OpenClaw 任务控制台（任务 / run / 产物 / 重跑），先在当前 workspace 内验证，再决定是否独立成软件
- 2026-03-11 下午已把 Agent Flow Console 接上 A 版执行桥：后端直接调用 `openclaw agent --session-id ... --message ... --json`（rescue 用 `--profile rescue`），每个 task 固定自己的 executor session；main / rescue 两条链路都已烟测通过，run 状态能走 `queued → running → completed/failed`，并回写 events / artifacts / usage / provider / model。
- 2026-03-11 老板明确调整职责：救援机**不承担日常任务**，暂时只负责“救援主机、修复故障、兜底恢复”。后续调度、控制台 auto 路由、任务分流都要把 rescue 视为应急执行面，而不是常规产能面。
- 关键教训：`openclaw agent --json` 在 main 与 rescue 输出结构不完全一致，rescue 还会混入 plugin 注册日志；控制台侧必须做“截取 JSON 正文 + payloads 兜底判成功”，不能假设 stdout 是干净统一 JSON。
- Agent Flow Console 第二阶段已补上“结果正文单独展示 + 一键重跑”能力；`/api/runs/:id` 需返回关联 task，`/api/runs/:id/rerun` 可基于原 task 直接再跑一次，重跑 run 的 `trigger` 记为 `rerun`。
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

## GPT 5.4 优化方案（2026-03-09/10 完成）

### 核心问题（已识别）
- 跳过前置步骤（因为最终状态看起来明显）
- 部分完成后就结束（遗漏批次中的项目）
- 空结果立即放弃（不尝试后备策略）
- 缺少验证循环（不检查输出正确性）
- 工具调用可靠性差（不开 thinking mode 准确率下降）
- 自适应推理导致行为不一致（快速路径 vs 深度推理路径）

### 已执行的优化（三轮）

**第一轮（2026-03-09 21:50）：系统提示 + 配置参数**
- 添加工具调用优先级规则（消除指令冲突）
- 添加上下文收集规则（早停条件）
- 添加深度控制规则（避免传递扩展）
- 添加工具调用预算（简单 2 次 / 中等 5 次 / 复杂不限）
- 配置 `verbosity=low`（减少 30% output tokens）
- 新增模型别名：gpt-5.4-minimal / gpt-5.4-high

**第二轮（2026-03-09 22:14）：OpenAI 官方 7 项最佳实践**
基于 OpenAI 官方 46k tokens 的 GPT-5.4 Prompt Guidance，注入 7 项核心规则：

1. **工具持久性**：不跳过前置步骤，持续调用直到完成且验证通过
2. **完整性契约**：保持检查清单，空结果时尝试后备策略
3. **验证循环**：检查正确性、可靠性、格式、安全性
4. **并行工具调用**：独立步骤并行，有依赖时串行
5. **输出契约**：准确返回请求内容，简洁但不省略证据
6. **默认跟进策略**：可逆低风险直接做，不可逆先确认
7. **自主性与坚持性**：端到端完成，不停在分析或部分修复

**第三轮（2026-03-09 22:21）：社区实战经验（10+ 来源）**
基于 bswen.com / nxcode.io / apiyi.com / GitHub OpenClaw 社区实践，新增 4 项防护：

1. **危险操作防护**：检测 DROP TABLE / rm -rf 等危险模式，暂停确认
2. **API 方法验证**：防止技术幻觉（编造方法名/参数），Schema 验证
3. **Context 管理策略**：避免 272K 成本陷阱（超过后整个会话翻倍计费）
4. **Chain-of-Thought 强制显示推理**：复杂计算必须显示 Step 1-5 推理过程

**关键文件：**
- `.gpt54-optimization-rules.md`（7249 bytes，OpenAI 官方参考）
- `AGENTS.md`（工具调用策略章节，已扩展至 150+ 行新增内容）

### 预期效果（OpenAI 官方数据）
- 复杂任务完成率：+30-50%
- 工具调用失败率：-60%
- 部分完成问题：消失
- 总成本：可能更低（减少重试）

### 关键洞察（OpenAI 官方）
- **规则 > reasoning_effort**：先添加规则，再考虑提升 reasoning_effort
- **reasoning_effort 不是万能药**：是"最后一英里的旋钮"，不是主要优化手段
- **推荐默认值**：medium（当前配置）✅
- **GPT 5.4 设计目标**：生产级助手和 agent，强多步推理，长上下文可靠性能
- **仍需明确提示的场景**：会话早期工具路由、依赖感知工作流、不可逆操作

### 使用建议
| 场景 | 推荐模型 | 理由 |
|---|---|---|
| 心跳检查、简单查询 | GPT 5.4 Minimal | 最便宜，速度快 |
| 日常对话、工具调用 | GPT 5.4（默认） | 平衡性能和成本 |
| 复杂任务、代码重构 | GPT 5.4 High | 推理能力强 |
| 关键任务（飞书、GitHub） | Claude Sonnet 4.5 | 工具调用最稳定 |

### 调研来源
- OpenAI 官方：GPT-5.4 Prompt Guidance（46k tokens）/ Reasoning Best Practices / Latest Model Guide
- GitHub OpenClaw：Issue #36817 / PR #36590
- Portkey.ai：Claude vs GPT-5 性能对比
- Composio.dev：实战测试（电商 app 构建）
- Reddit 社区：Prompt Optimizer 实测反馈

### 待研究
- phase 参数支持（避免 preambles 被当作最终答案）
- Preambles 启用（工具调用前解释，提升准确性）
- Tool Search 支持（预期减少 47% tokens）
- 长期记忆方案（memory-lancedb-pro / total-recall）
- 实际 token 消耗数据收集与验证

## Token 优化配置（2026-03-09 22:35 完成）

### Heartbeat Model 优化
- **配置**：`agents.defaults.heartbeat.model = "ikuncode-gpt/gpt-5.1-codex-mini"`
- **成本**：$9/月 → $0.42/月（节省 95%）
- **关键教训**：配置位置是 `heartbeat.model`，不是 `model.heartbeat`（第一次配错了）

### Context 自动清理
- **配置**：`contextPruning = { mode: "cache-ttl", ttl: "6h", keepLastAssistants: 3 }`
- **效果**：自动清理 6 小时前的历史，避免 272K token 陷阱
- **272K 陷阱**：GPT 5.4 超过 272K tokens 后，整个会话按双倍计费（$2.50→$5.00）

### 配置错误教训（2026-03-09 22:30-22:35）
**第一轮配置（错误）：**
1. ❌ `model.heartbeat`（位置错误，应该是 `heartbeat.model`）
2. ❌ `cacheRetention: "long"`（字段不存在）
3. ❌ `contextTokens: 250000`（字段不存在，应该用 `contextPruning`）

**第二轮修正（正确）：**
1. ✅ `heartbeat.model`（正确位置）
2. ✅ `contextPruning`（正确字段）
3. ✅ 删除所有无效配置

**验证方法：**
- 联网查阅官方文档（GitHub PR #33363 / docs.openclaw.ai）
- 社区最佳实践（digitalknk/openclaw-runbook）
- 不盲目信任第三方指南

### 预期成本节省
- **当前**：$20-35/月
- **优化后**：$10-15/月
- **节省**：50-60%

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
- **GPT 5.4 深度优化完成**（系统提示 + 配置参数，预期成本降至 Claude 的 20-30%）
- **Token 优化配置完成**（Heartbeat Model + Context Pruning，预期节省 50-60%）
- 确立模型选型铁律：Claude 稳执行（S级），GPT 强推理（参谋级），Gemini 搞批量（轻量级）
- 确立任务拆解铁律：先验通道，再抓证据，后出结论；禁止抛半成品
- 确立外部检索路由铁律：X/Reddit 禁止硬撞直连，优先走 skill 链路 (Exa/gh/xreach)
- **确立配置验证铁律**：配置前查官方文档，配置后联网验证，不盲目信任第三方指南
