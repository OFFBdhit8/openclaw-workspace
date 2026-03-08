# LEARNINGS.md

> 经验教训记录。按时间倒序排列。

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
