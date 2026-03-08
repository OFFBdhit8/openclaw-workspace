---
name: self-improvement
description: "记录学习、错误和修正，实现持续自我进化。触发场景：(1) 命令/操作失败 (2) 老板纠正我 (3) 发现更好的方案 (4) 外部 API/工具故障 (5) 知识过时。重大任务前先回顾 .learnings/ 目录。"
---

# Self-Improvement Skill

## 快速参考

| 场景 | 动作 |
|------|------|
| 命令/操作失败 | 记录到 `.learnings/ERRORS.md` |
| 老板纠正我 | 记录到 `.learnings/LEARNINGS.md`，category=correction |
| 缺少功能 | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| API/工具故障 | 记录到 `.learnings/ERRORS.md` |
| 知识过时 | 记录到 `.learnings/LEARNINGS.md`，category=knowledge_gap |
| 发现更好方案 | 记录到 `.learnings/LEARNINGS.md`，category=best_practice |
| 广泛适用的经验 | 提升到 AGENTS.md / SOUL.md / TOOLS.md |

## 记录格式

### Learning Entry → `.learnings/LEARNINGS.md`

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601
**Priority**: low | medium | high | critical
**Status**: pending

### Summary
一句话描述

### Details
完整上下文

### Suggested Action
具体改进措施

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file
- Tags: tag1, tag2
```

### Error Entry → `.learnings/ERRORS.md`

```markdown
## [ERR-YYYYMMDD-XXX] command_or_tool

**Logged**: ISO-8601
**Priority**: high
**Status**: pending

### Summary
什么失败了

### Error
实际错误信息

### Context
- 尝试的操作
- 输入参数
- 环境信息

### Suggested Fix
修复方案
```

### Feature Request → `.learnings/FEATURE_REQUESTS.md`

```markdown
## [FEAT-YYYYMMDD-XXX] capability

**Logged**: ISO-8601
**Priority**: medium
**Status**: pending

### Requested Capability
需要什么功能

### User Context
为什么需要

### Suggested Implementation
怎么实现
```

## 状态流转

- `pending` → 待处理
- `in_progress` → 处理中
- `resolved` → 已解决
- `promoted` → 已提升到项目记忆
- `wont_fix` → 不修

## 提升规则

经验广泛适用时，提炼成简洁规则写入：
- **SOUL.md** — 行为模式、沟通风格
- **AGENTS.md** — 工作流、自动化规则
- **TOOLS.md** — 工具使用技巧、踩坑记录
- **MEMORY.md** — 长期记忆
