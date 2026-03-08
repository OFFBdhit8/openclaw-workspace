# ERRORS.md

> 错误记录。按时间倒序排列。

## [ERR-20260308-001] gateway-install

**Logged**: 2026-03-08T12:15:00+08:00
**Priority**: high
**Status**: resolved

### Summary
`openclaw gateway install --force` 覆盖了主机的 systemd 服务文件

### Error
救援机的 install 命令把主机的 openclaw-gateway.service 覆盖成了救援机配置

### Context
- 执行 `openclaw --profile rescue gateway install --force --port 19789`
- 期望创建 openclaw-gateway-rescue.service
- 实际覆盖了 openclaw-gateway.service

### Suggested Fix
手动创建独立的 systemd 服务文件，不依赖 install 命令

### Resolution
- **Resolved**: 2026-03-08T12:30:00+08:00
- **Notes**: 手动恢复主机服务文件 + 手动创建救援机服务文件

---

## [ERR-20260308-002] rescue-config

**Logged**: 2026-03-08T12:20:00+08:00
**Priority**: medium
**Status**: resolved

### Summary
救援机配置格式不对，`models.default` 字段不存在

### Error
照猜写的配置结构和主机实际结构不一致

### Context
- 写了 `models.default` 字段
- 实际应该用 `agents.defaults.model.primary`

### Suggested Fix
先 cat 主机配置看清结构再写新配置

### Resolution
- **Resolved**: 2026-03-08T12:25:00+08:00
- **Notes**: 参考主机配置重写

---
