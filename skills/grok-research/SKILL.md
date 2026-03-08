---
name: grok-research
description: >
  通过 Grok 模型获取 X/Twitter 实时信息。Grok 拥有 X 平台的实时知识，
  适合查询：加密货币叙事/情绪、项目舆情、推特热点、KOL 观点、实时事件。
  触发词：调研、research、grok、查一下、推上怎么说、X上、twitter。
  不适用于：价格分析、链上数据、交易执行。
---

# Grok Research

通过 ikuncode 调用 Grok 模型，获取 X/Twitter 实时信息。

## 配置

- API Base: `https://api.ikuncode.cc/v1`
- API Key 环境变量: `GROK_API_KEY`
- 默认模型: `grok-4.20-beta`

## 可用模型

| 模型 | 特点 |
|------|------|
| grok-4.20-beta | 默认，最新 |
| grok-4.1-thinking | 深度思考 |
| grok-4-expert | 专家级 |
| grok-4-fast-expert | 快速专家 |
| grok-4.1-fast | 快速 |
| grok-3-fast | 旧版快速 |

## 使用方式

```bash
cd ~/.openclaw/workspace/skills/grok-research
bun run grok-research.ts <query>
bun run grok-research.ts --model grok-4.1-thinking <query>
```

## 调用规则

1. 将用户原始消息作为 query 直接转发，不要添加额外 prompt
2. stdout 是 Grok 的回复，直接转发给用户
3. Discord 发送时不要用 markdown 表格，用列表代替
