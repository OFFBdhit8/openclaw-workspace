# ERRORS.md

> 错误记录。按时间倒序排列。

## [ERR-20260308-005] feishu-group-config

**Logged**: 2026-03-08T14:22:00+08:00
**Priority**: high
**Status**: resolved

### Summary
飞书 `groupAllowFrom` 放了群 ID（oc_xxx），但该字段是过滤发送者的（应放 ou_xxx）

### Error
`groupAllowFrom contains chat_id entries. Please move chat_ids to "groups" config instead`

### Context
群消息被拒绝：`rejected: no bot mention in group`

### Suggested Fix
群 ID 放在 `channels.feishu.groups` 里，`groupAllowFrom` 只放用户 open_id

### Resolution
- **Resolved**: 2026-03-08T14:22:00+08:00
- **Notes**: 改用 `groups: { "oc_xxx": { enabled: true, requireMention: false } }`

---

## [ERR-20260308-006] sigusr1-self-kill

**Logged**: 2026-03-08T14:23:00+08:00
**Priority**: medium
**Status**: resolved

### Summary
`pkill -SIGUSR1 -f "openclaw-gateway"` 会把自身进程也杀掉

### Error
`Command aborted by signal SIGUSR1`

### Context
pkill 匹配到了当前 exec 子进程

### Suggested Fix
用 `kill -SIGUSR1 <具体PID>` 而不是 pkill

### Resolution
- **Resolved**: 2026-03-08T14:23:00+08:00

---

## [ERR-20260308-004] rescue-node-path

**Logged**: 2026-03-08T13:22:00+08:00
**Priority**: medium
**Status**: resolved

### Summary
救援机 systemd 服务 PATH 缺少 nvm 实际路径，导致 `openclaw status` 报 `node: not found`

### Error
PATH 里用了 `/root/.nvm/current/bin`（符号链接可能不存在），实际路径是 `/root/.nvm/versions/node/v22.22.0/bin`

### Context
手动创建 systemd 服务文件时照抄了不完整的 PATH

### Suggested Fix
systemd 服务文件的 PATH 必须包含 `/root/.nvm/versions/node/v22.22.0/bin`

### Resolution
- **Resolved**: 2026-03-08T13:22:00+08:00

---

## [ERR-20260308-003] gateway-reload-config

**Logged**: 2026-03-08T13:18:00+08:00
**Priority**: medium
**Status**: resolved

### Summary
`gateway.reload` 配置格式错误，应该是对象不是字符串

### Error
`Invalid input: expected object, received string`

### Context
- 写了 `"reload": "hybrid"`
- 实际应该是 `"reload": {"mode": "hybrid"}`

### Suggested Fix
OpenClaw 配置里复杂字段都是对象格式，不要用字符串简写

### Resolution
- **Resolved**: 2026-03-08T13:19:00+08:00

---

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
