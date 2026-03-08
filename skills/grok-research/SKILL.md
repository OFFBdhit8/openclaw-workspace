---
name: grok-research
description: >
  通过 Grok 模型获取 X/Twitter 实时信息。Grok 拥有 X 平台的实时知识，
  适合查询：加密货币叙事/情绪、项目舆情、推特热点、KOL 观点、实时事件。
  触发词：调研、research、grok、查一下、推上怎么说、X上、twitter。
  不适用于：价格分析、链上数据、交易执行。
---

# Grok Research v2

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

## 调研模式

| 模式 | 用途 | 触发场景 |
|------|------|----------|
| `crypto` | 加密货币调研 | 币圈叙事、KOL观点、社区情绪、风险信号 |
| `tech` | 科技产品调研 | 产品反馈、竞品对比、趋势判断 |
| `sentiment` | 情绪分析 | 纯情绪评分、情绪分布、转折点 |
| `general` | 通用调研（默认） | 其他所有场景 |

## 使用方式

```bash
cd ~/.openclaw/workspace/skills/grok-research
bun run grok-research.ts <query>
bun run grok-research.ts --mode crypto "查一下 $PEPE 最近叙事"
bun run grok-research.ts --model grok-4.1-thinking --mode tech "OpenClaw 社区评价"
```

## 调用规则

1. 用户说"调研"、"research"、"grok"、"查一下"、"推上怎么说"时触发
2. 涉及加密货币/meme币 → 自动用 `--mode crypto`
3. 涉及科技产品 → 自动用 `--mode tech`
4. 只问情绪/看涨看跌 → 自动用 `--mode sentiment`
5. 其他 → `--mode general`
6. 结果有 10 分钟缓存，同样的问题不重复调 API
7. 将 Grok 返回的结果直接展示给用户，不二次加工

## 缓存

- 缓存目录：`.cache/`
- TTL：10 分钟
- 同 model + mode + query 命中缓存时不调 API
- 缓存自动过期，无需手动清理

## 成本

ikuncode Grok 按次计费 ¥0.003/次 × 分组倍率 0.1 = **¥0.0003/次**
