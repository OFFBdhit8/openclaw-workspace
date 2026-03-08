#!/usr/bin/env bun
/**
 * grok-research v2 — 通过 ikuncode 调用 Grok，获取 X/Twitter 实时信息
 *
 * 优化：
 * - 多模式 system prompt（crypto/tech/sentiment/general）
 * - 结果缓存（同 query 10 分钟内不重复调 API）
 * - 更好的输出结构
 *
 * Usage:
 *   bun run grok-research.ts <query>
 *   bun run grok-research.ts --mode crypto <query>
 *   bun run grok-research.ts --model grok-4.1-thinking --mode tech <query>
 *
 * Modes: crypto | tech | sentiment | general (default)
 * Env: GROK_API_KEY (required)
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "fs";
import { join } from "path";
import { createHash } from "crypto";

const BASE_URL = "https://api.ikuncode.cc/v1";
const DEFAULT_MODEL = "grok-4.20-beta";
const CACHE_DIR = join(import.meta.dir, ".cache");
const CACHE_TTL_MS = 10 * 60 * 1000; // 10 minutes

// ==================== System Prompts ====================

const SYSTEM_PROMPTS: Record<string, string> = {
  crypto: `你是加密货币调研分析师，专精 meme 币和 DeFi 领域。基于 X/Twitter 实时数据分析。

输出格式（严格遵守）：

## 核心叙事
一句话总结当前最主要的叙事方向。

## KOL 观点
**看多派：**
- @xxx: "观点摘要"
- @xxx: "观点摘要"

**看空派：**
- @xxx: "观点摘要"

## 社区情绪
🟢看涨 / 🔴看跌 / 🟡中性（选一个），附一句话解释。

## 风险信号
- 列出潜在风险（如：团队匿名、合约未审计、巨鲸抛售等）

## 关键信息源
列出 3-5 个最相关的推文或账号，附简要说明。

注意：只输出有实际证据支撑的信息，不确定的标注"未证实"。`,

  tech: `你是科技产品调研分析师。基于 X/Twitter 实时数据分析产品、技术趋势。

输出格式：

## 产品概述
一段话说清楚是什么、解决什么问题。

## 社区反馈
**正面：** 列出好评要点
**负面：** 列出差评和吐槽
**功能请求：** 用户最想要什么

## 竞品对比
列出主要竞品和差异化。

## 趋势判断
上升期 / 平台期 / 下降期，附依据。

## 关键信息源
列出 3-5 个最相关的推文或账号。`,

  sentiment: `你是社交媒体情绪分析师。只做情绪分析，不做深度调研。

输出格式：

## 情绪评分
-10（极度恐慌）到 +10（极度贪婪），给出数字和一句话解释。

## 情绪分布
🟢 看多: X%
🔴 看空: X%
🟡 中性: X%

## 情绪转折点
最近 24-48h 有无明显情绪变化？什么事件触发的？

## 高影响力声音
列出 3 个最有影响力的观点（附账号和粉丝量级）。`,

  general: `你是 X/Twitter 实时信息调研助手。根据用户的问题，从 X 平台获取最新、最相关的信息。

输出要求：
1. 直接回答问题，不废话
2. 引用具体的推文、账号作为信息源
3. 区分事实和观点
4. 不确定的信息标注"未证实"
5. 如果信息不足，明确说明而不是编造`
};

// ==================== Cache ====================

function getCacheKey(model: string, mode: string, query: string): string {
  return createHash("md5").update(`${model}:${mode}:${query}`).digest("hex");
}

function getCache(key: string): string | null {
  if (!existsSync(CACHE_DIR)) return null;
  const file = join(CACHE_DIR, `${key}.json`);
  if (!existsSync(file)) return null;
  try {
    const data = JSON.parse(readFileSync(file, "utf-8"));
    if (Date.now() - data.ts < CACHE_TTL_MS) {
      console.error("📦 Cache hit (< 10min)");
      return data.result;
    }
  } catch {}
  return null;
}

function setCache(key: string, result: string): void {
  if (!existsSync(CACHE_DIR)) mkdirSync(CACHE_DIR, { recursive: true });
  writeFileSync(
    join(CACHE_DIR, `${key}.json`),
    JSON.stringify({ ts: Date.now(), result })
  );
}

// ==================== API ====================

function getApiKey(): string {
  const key = process.env.GROK_API_KEY;
  if (!key) throw new Error("GROK_API_KEY env var not set");
  return key;
}

async function callGrok(model: string, mode: string, query: string): Promise<string> {
  const systemPrompt = SYSTEM_PROMPTS[mode] || SYSTEM_PROMPTS.general;

  const res = await fetch(`${BASE_URL}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getApiKey()}`,
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: query },
      ],
      stream: false,
      temperature: 0.3,
      max_tokens: 8192,
    }),
  });

  if (!res.ok) {
    throw new Error(`Grok API ${res.status}: ${(await res.text()).slice(0, 500)}`);
  }

  const rawText = await res.text();

  // Handle SSE streaming
  if (rawText.startsWith("data: ")) {
    let content = "";
    for (const line of rawText.split("\n")) {
      if (!line.startsWith("data: ") || line.trim() === "data: [DONE]") continue;
      try {
        const delta = JSON.parse(line.slice(6)).choices?.[0]?.delta?.content;
        if (delta) content += delta;
      } catch {}
    }
    content = content.replace(/<thinking>[\s\S]*?<\/thinking>/g, "").trim();
    if (!content) throw new Error("Grok returned empty response");
    return content;
  }

  // Regular JSON
  const data = JSON.parse(rawText);
  const content = data.choices?.[0]?.message?.content;
  if (!content) throw new Error("Grok returned empty response");
  return content;
}

// ==================== CLI ====================

const args = process.argv.slice(2);

let model = DEFAULT_MODEL;
let mode = "general";

// Parse --model
const mi = args.indexOf("--model");
if (mi >= 0 && mi + 1 < args.length) {
  model = args[mi + 1];
  args.splice(mi, 2);
}

// Parse --mode
const moi = args.indexOf("--mode");
if (moi >= 0 && moi + 1 < args.length) {
  mode = args[moi + 1];
  args.splice(moi, 2);
}

// Validate mode
if (!SYSTEM_PROMPTS[mode]) {
  console.error(`❌ Unknown mode: ${mode}`);
  console.error(`Available: ${Object.keys(SYSTEM_PROMPTS).join(", ")}`);
  process.exit(1);
}

const query = args.join(" ").trim();
if (!query) {
  console.error("Usage: bun run grok-research.ts [--model <id>] [--mode <mode>] <query>");
  console.error("Modes: crypto | tech | sentiment | general (default)");
  process.exit(1);
}

// Check cache first
const cacheKey = getCacheKey(model, mode, query);
const cached = getCache(cacheKey);
if (cached) {
  console.log(cached);
  process.exit(0);
}

console.error(`🔍 ${model} [${mode}] ...`);
try {
  const result = await callGrok(model, mode, query);
  setCache(cacheKey, result);
  console.log(result);
} catch (err: any) {
  console.error(`❌ ${err.message}`);
  process.exit(1);
}
