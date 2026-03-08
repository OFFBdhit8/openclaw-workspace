# MEMORY.md - 长期记忆

## 老板画像
- 称呼：老板
- 工作室，目标暴富，结果导向
- 偏好：快准狠，不废话，中文交流
- 技术水平：熟悉 OpenClaw/Discord/API 配置，能看懂代码

## 基础设施
- 服务器：腾讯云轻量 43.163.7.171，Ubuntu 6.8.0-71
- 主机 Gateway：端口 18789，模型 claude-opus-4-6
- 救援机 Gateway：端口 19789，模型 gpt-5.4
- 飞书机器人 x2：主机 + 救援机（cli_a920618557789bcd）
- Discord Bot：服务器 1473676822960144560
- API 供应商：ikuncode（Claude/GPT/Grok），计费标准见 https://api.ikuncode.cc/pricing
- Camofox 反检测浏览器：端口 9377

## 工具链
- X 推文抓取：fetch_tweet.py（L1）→ Camofox（L2）→ Grok（L3）
- Brave Search / Tavily 双搜索引擎
- GitHub CLI：账号 OFFBdhit8
- 飞书全套：IM/日历/任务/多维表格/文档/知识库

## 经验教训
- 从会话内执行 `openclaw gateway restart` 会断连挂起，让老板手动跑或用 systemctl
- `--profile rescue` 配置目录是 `~/.openclaw-rescue/` 不是 `~/.openclaw/profiles/rescue/`
- 飞书 groupPolicy=open 有安全风险，用 allowlist
- 社区共识：智能体占三成，免疫系统占七成
- 热加载：`gateway.reload = "hybrid"`，改 json 自动生效；手动触发用 `pkill -SIGUSR1 -f gateway`，不断连
- 不要用 SIGHUP，用 SIGUSR1
- 飞书群 ID（oc_xxx）放 `channels.feishu.groups`，不是 `groupAllowFrom`（那个是过滤发送者 ou_xxx 的）
- `pkill -SIGUSR1` 会误杀自身进程，用 `kill -SIGUSR1 <PID>`

## 待探索
- .issues/ 本地任务调度系统
- 赚钱路子
