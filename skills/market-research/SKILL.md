---
name: market-research
description: "痛点挖掘 + 产品机会发现。扫描 Reddit/X/HN/Web 的真实用户痛点，按频率排序，找到没人解决的问题。触发词：调研、痛点、市场、机会、什么值得做、last30"
---

# Market Research Skill — 痛点挖掘机

## 用法

老板说"调研 [话题]"或"[话题] 有什么痛点"时触发。

## 执行流程

### 1. 多源搜索（并行）

用以下工具同时搜索：

**Reddit:**
```
camofox_navigate → @reddit_search → "[话题] frustrating OR annoying OR wish OR need OR help"
```

**X/Twitter:**
```
fetch_tweet.py 抓相关推文
或 Grok skill 调研舆情
```

**Hacker News:**
```
web_fetch → https://hn.algolia.com/api/v1/search?query=[话题]&tags=ask_hn,show_hn
```

**Web:**
```
web_search → "[话题] pain point OR problem OR complaint OR feature request"
```

### 2. 痛点提取

从搜索结果中提取：
- 具体的抱怨和不满（原文引用）
- 功能请求（"我希望有..."）
- 现有方案的缺陷
- 反复出现的关键词

### 3. 排序和评分

按以下维度打分（1-10）：

| 维度 | 说明 |
|------|------|
| 频率 | 多少人提到这个问题 |
| 痛感 | 问题有多严重 |
| 付费意愿 | 有没有人说"愿意花钱解决" |
| 竞品空白 | 现有方案覆盖程度 |
| 可行性 | 我们能不能做 |

### 4. 输出格式

```markdown
# [话题] 痛点调研报告

## 🔴 高价值机会（综合评分 > 7）
### 1. [痛点名称]
- 频率: X/10 | 痛感: X/10 | 付费意愿: X/10
- 原文引用: "..."
- 现有竞品: [列表]
- 建议方案: [一句话]

## 🟡 中等机会（综合评分 4-7）
...

## 🟢 低优先级
...

## 下一步建议
1. 最值得做的 1-2 个方向
2. 验证方法（怎么确认需求真实）
3. MVP 范围（最小可行产品长什么样）
```

### 5. 保存

结果保存到 `memory/research/[话题]-[日期].md`

## 定时调研（可选）

每周一早上自动调研老板关注的领域，结果推送到飞书。
在 cron 中配置 `openclaw run` 触发。
