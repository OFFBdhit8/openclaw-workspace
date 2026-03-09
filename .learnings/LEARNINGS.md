# LEARNINGS.md

> 经验教训记录。按时间倒序排列。

## [LRN-20260308-005] knowledge_gap

**Logged**: 2026-03-08T14:35:00+08:00
**Priority**: high
**Status**: promoted

### Summary
飞书 allowlist 模式下，`groups` 控制哪些群可以交互，`groupAllowFrom` 控制哪些用户可以在群里触发机器人

### Details
两个配置缺一不可：
- `groups: { "oc_xxx": { enabled: true } }` — 允许哪些群
- `groupAllowFrom: ["ou_xxx"]` — 允许哪些用户

### Suggested Action
配 allowlist 时两个都要配

### Metadata
- Source: error
- Tags: feishu, allowlist, groups, config
- Promoted: MEMORY.md

---

## [LRN-20260308-004] best_practice

**Logged**: 2026-03-08T13:17:00+08:00
**Priority**: high
**Status**: promoted

### Summary
OpenClaw 支持热加载配置，用 SIGUSR1 不断连

### Details
- `gateway.reload = "hybrid"` 默认模式，自动监听 openclaw.json 变更
- `pkill -SIGUSR1 -f gateway` 手动触发热加载，不断连不丢会话
- 通道设置、模型、工具权限、heartbeat 都能热加载
- 端口、auth、新增通道才需要重启
- 不要用 SIGHUP，用 SIGUSR1

### Suggested Action
以后改配置直接改 json，Gateway 自动热加载。需要手动触发时用 SIGUSR1。

### Metadata
- Source: web_search
- Tags: openclaw, hot-reload, SIGUSR1, config
- Promoted: MEMORY.md

---

## [LRN-20260308-001] best_practice

**Logged**: 2026-03-08T12:00:00+08:00
**Priority**: high
**Status**: promoted

### Summary
从会话内执行 `openclaw gateway restart` 会断连挂起

### Details
Gateway 重启会断开当前 WebSocket 连接，exec 拿不到返回结果，命令看起来像卡住了。

### Suggested Action
用 `systemctl --user restart openclaw-gateway` 或让老板手动跑

### Metadata
- Source: error
- Tags: openclaw, gateway, restart
- Promoted: MEMORY.md, feedback.json

---

## [LRN-20260308-002] knowledge_gap

**Logged**: 2026-03-08T12:10:00+08:00
**Priority**: medium
**Status**: promoted

### Summary
`--profile rescue` 配置目录是 `~/.openclaw-rescue/` 不是 `~/.openclaw/profiles/rescue/`

### Details
OpenClaw profile 名为 X 时，配置目录固定为 `~/.openclaw-X/`

### Suggested Action
先确认目录结构再写配置

### Metadata
- Source: error
- Tags: openclaw, profile, path
- Promoted: MEMORY.md, feedback.json

---

## [LRN-20260308-003] best_practice

**Logged**: 2026-03-08T12:50:00+08:00
**Priority**: high
**Status**: pending

### Summary
社区共识：智能体占三成，免疫系统占七成

### Details
极道文章总结：反馈循环、自愈审计、验证层、预算控制四层免疫系统。`ls -la` 比 "task complete" 可靠一万倍。

### Suggested Action
所有自动化任务都要有验证步骤，不信 AI 的口头汇报

### Metadata
- Source: conversation
- Tags: architecture, self-healing, community

---

## [LRN-20260309-006] correction

**Logged**: 2026-03-09T21:18:00+08:00
**Priority**: high
**Status**: pending

### Summary
老板指出：外部检索任务不该先硬撞直连网页；任务拆解不能把“通道可用性验证”漏掉。

### Details
这次在做系统/社区/X/Reddit 自检时，先用直连访问 X/Reddit，遇到 403 后才补查 skill 和替代链路，导致结果半成品、节奏拖沓。根因不是工具缺失，而是任务拆解顺序错了：应该先验证通道，再选搜索链路，再汇总结论。

### Suggested Action
- 外部平台检索任务默认拆成三步：通道体检 → 证据抓取 → 结论汇总
- X/Reddit/受限站点先查 `TOOLS.md` 和 `agent-reach doctor`
- 复杂任务先给出“验证路径”，不要边试边汇报半成品
- 模型选型要按任务类型：主会话稳定执行优先 Claude；长上下文/成本优先再考虑 GPT/Gemini

### Metadata
- Source: user_feedback
- Related Files: TOOLS.md, memory/2026-03-09.md
- Tags: correction, task-decomposition, search-routing, model-selection
