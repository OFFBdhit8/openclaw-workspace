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

### 决策规则
- 普通搜索 → Camofox（免费 + Google 质量）
- Camofox 挂了 → DuckDuckGo → Brave
- 搜 X/Twitter → Grok
- 需要结构化摘要喂 LLM → Tavily
- 大批量搜索 → Brave（吃免费额度）
- 搜到链接读全文 → web_fetch
- 不确定 → Camofox 兜底

### 不用的方案（评估过，不需要）
- Serper — 虽然便宜（$0.30/千次），但 Camofox 免费搜 Google 已覆盖
- Firecrawl — web_fetch 够用
- SearXNG 自建 — 维护成本高，Camofox 已解决零成本问题
- Gemini grounding — $35/千次，太贵

Add whatever helps you do your job. This is your cheat sheet.
