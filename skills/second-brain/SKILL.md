---
name: second-brain
description: "第二大脑 — 随手存、随时搜。触发词：记住这个、存一下、之前说过什么、找一下"
---

# Second Brain Skill

## 核心理念
老板随手丢信息进来，我负责分类存储。需要时搜索召回。

## 存储规则

### 收到信息时自动分类：

| 类型 | 存储位置 |
|------|---------|
| 灵感/想法 | `memory/ideas/[日期]-[关键词].md` |
| 链接/文章 | `memory/bookmarks/[日期]-[标题].md` |
| 联系人/人脉 | `memory/contacts/[名字].md` |
| 项目笔记 | `memory/projects/[项目名]/` |
| 技术方案 | `memory/tech/[主题].md` |
| 商业机会 | `memory/opportunities/[日期]-[描述].md` |
| 其他 | `memory/inbox/[日期]-[摘要].md` |

### 存储格式
```markdown
# [标题]
- **日期**: YYYY-MM-DD
- **来源**: [老板说的 / 链接 / 调研]
- **标签**: tag1, tag2
- **状态**: inbox / processing / done

## 内容
[原始内容或摘要]

## 我的理解
[一句话总结为什么重要]
```

## 搜索规则

老板说"之前说过 XXX"或"找一下 XXX"时：
1. 先搜 memory/ 目录（grep + 文件名匹配）
2. 再搜 .learnings/ 目录
3. 最后搜 MEMORY.md

## 定期整理

每周 heartbeat 中：
- inbox/ 里超过 7 天的归档或删除
- 重复内容合并
- 高价值内容提升到 MEMORY.md
