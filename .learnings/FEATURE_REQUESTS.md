# FEATURE_REQUESTS.md

> 功能需求记录。按时间倒序排列。

## [FEAT-20260308-001] local-task-queue

**Logged**: 2026-03-08T12:55:00+08:00
**Priority**: medium
**Status**: pending

### Requested Capability
`.issues/` 本地任务调度系统，类似 YuLin807 的异步任务管理

### User Context
老板想要丢任务后自动排期执行，不用盯着

### Suggested Implementation
- `.issues/` 目录存任务文件（markdown）
- cron 或 heartbeat 定期扫描
- 按优先级分配给 sub-agent 执行
- 执行结果写回任务文件

---

## [FEAT-20260308-002] auto-patrol

**Logged**: 2026-03-08T12:56:00+08:00
**Priority**: high
**Status**: in_progress

### Requested Capability
救援机主动巡查 + 自愈能力

### User Context
不想等主机挂了才手动通知救援机

### Suggested Implementation
- ✅ watchdog 脚本（已完成）
- ✅ cron 每 5 分钟检测（已完成）
- 待做：飞书通知告警
- 待做：feedback 循环（修复后记录方案）

---
