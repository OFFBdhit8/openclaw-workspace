# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## 搜索策略（按成本优先级）

每次需要搜索时，按以下顺序选择：

### 1. Camofox Google Search（免费）
- 工具：`camofox_navigate` + `@google_search` macro
- 成本：¥0
- 适用：通用搜索、日常查询
- 限制：需要 Camofox 在线（端口 9377），速度略慢于 API

### 2. Grok Research（几乎免费）
- 工具：grok-research skill
- 成本：¥0.0003/次（ikuncode 分组倍率 0.1）
- 适用：X/Twitter 实时内容、社交媒体舆情、KOL 动态
- 这是搜 X 的唯一选项

### 3. Brave Search API（有免费额度）
- 工具：`web_search`（默认 provider）
- 成本：$5/千次，每月 $5 免费额度
- 适用：Camofox 不可用时的 fallback、需要快速批量搜索
- Key 已配置，开箱即用

### 4. Tavily（有免费额度）
- 工具：tavily skill
- 成本：$8/千次，每月免费 1,000 次
- 适用：需要 LLM 优化的结构化摘要、RAG 场景
- 省着用，留给真正需要结构化输出的场景

### 决策规则
- 普通搜索 → Camofox
- 搜 X/Twitter → Grok
- Camofox 挂了 → Brave
- 需要结构化摘要喂 LLM → Tavily
- 不确定 → Camofox（免费兜底）

Add whatever helps you do your job. This is your cheat sheet.
