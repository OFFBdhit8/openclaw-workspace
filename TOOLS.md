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

### Tier 0 — 完全免费
1. **Camofox Google Search** — `camofox_navigate` + `@google_search`，¥0，Google 原生结果，质量最高的免费方案。需 Camofox 在线（端口 9377）
2. **DuckDuckGo Skill** — `duckduckgo-search`，¥0，无需 API key，国内可访问。质量弱于 Google，轻量 fallback
3. **Multi Search Engine Skill** — `multi-search-engine-2-0-1`，¥0，聚合 17 个引擎（8 国内 + 9 国际），覆盖面广但稳定性一般

### Tier 1 — 几乎免费
4. **Grok Research** — grok-research skill，ikuncode 零计费，搜 X/Twitter 实时内容的唯一选项
5. **Brave Search API** — `web_search`（默认），$5/千次，月 $5 免费额度，已配置开箱即用
6. **Tavily** — tavily skill，$8/千次，月免费 1,000 次，LLM 优化结构化摘要

### Tier 2 — 待接入（值得加）
7. **Serper** — $0.30/千次，最便宜付费方案，注册送 2500 次。比 Brave 便宜 16 倍
8. **Firecrawl** — 搜到链接后读全文，比 web_fetch 结构化更好

### 决策规则
- 普通搜索 → Camofox（免费 + 质量最高）
- Camofox 挂了 → DuckDuckGo → Brave
- 搜 X/Twitter → Grok
- 需要结构化摘要喂 LLM → Tavily
- 大批量搜索 → Brave / Serper（接入后）
- 搜到链接读全文 → web_fetch（现有）/ Firecrawl（待接入）
- 不确定 → Camofox 兜底

Add whatever helps you do your job. This is your cheat sheet.
