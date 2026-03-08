---
name: earnings-tracker
description: "AI/科技财报追踪 — 自动抓取分析重要公司财报。触发词：财报、earnings、季报、业绩"
---

# Earnings Tracker Skill

## 关注列表
- AI 巨头：NVIDIA, Microsoft, Google, Meta, Amazon, Apple
- AI 独角兽：OpenAI, Anthropic, xAI
- 工具链：Cloudflare, Vercel, Supabase
- 中概：阿里、腾讯、字节、百度

## 触发方式

### 手动
老板说"XX 财报怎么样"时触发

### 自动（每日早报中）
morning-brief 检查过去 24h 是否有关注列表的财报发布

## 分析框架

| 维度 | 关注点 |
|------|--------|
| 营收 | 同比增长、是否超预期 |
| AI 业务 | AI 相关收入占比、增速 |
| 指引 | 下季度预期、管理层态度 |
| 信号 | 裁员/招人、新产品、战略转向 |
| 对我们的影响 | 有没有新机会、有没有风险 |

## 输出
- 一句话结论（利好/利空/中性）
- 关键数据表格
- 对我们的启示
- 保存到 `memory/research/earnings-[公司]-[日期].md`
