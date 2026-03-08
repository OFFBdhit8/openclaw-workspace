---
name: overnight-builder
description: "过夜自主建 MVP — 睡前丢需求，醒来看成品。触发词：帮我做个、建一个、MVP、过夜做"
---

# Overnight Mini App Builder Skill

## 核心流程

### 1. 需求确认（睡前 5 分钟）
老板描述想要什么，我确认：
- 做什么（一句话）
- 给谁用
- 核心功能（最多 3 个）
- 技术偏好（有的话）

### 2. Pre-Build 验证
用 idea-reality MCP 检查：
- GitHub/npm 有没有现成的
- 有竞品的话，差异化在哪
- 如果已有完美方案，直接推荐，不重复造轮子

### 3. 自主执行（过夜）
通过 `openclaw run` 或 sub-agent 执行：
- 选技术栈（偏好：轻量、部署简单）
- 写代码
- 本地测试
- 写 README
- git commit

### 4. 验证（醒来后）
- 不信"完成了"，用 `ls -la` 验证文件存在
- 跑测试确认能用
- 飞书通知老板：做了什么、在哪、怎么跑

## 技术栈偏好
- 前端：HTML + Tailwind + Alpine.js（轻量）
- 后端：Node.js / Python FastAPI
- 部署：腾讯云轻量 / Vercel / Cloudflare Pages
- 数据库：SQLite（简单场景）/ Supabase（需要云端）

## 安全规则
- 不自动部署到生产环境
- 不自动购买域名/服务
- 代码写在 `/root/.openclaw/workspace/projects/[项目名]/`
- 完成后通知老板审查

## 项目目录结构
```
projects/
  [项目名]/
    README.md
    src/
    package.json (or requirements.txt)
    .env.example
```
