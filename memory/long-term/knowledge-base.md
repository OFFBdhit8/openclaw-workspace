# 长期知识库

基于日常记忆提炼的重要知识和经验教训

最后更新: 2026-02-27 16:24

## 决策模式

基于拒绝日志提炼的常见决策模式和理由：

### 拒绝理由：用户表示缺少必要凭证（Twitter Cookie、Docker、代理地址），决定不继续
出现次数：1

1. **2026-02-27** - 拒绝：继续配置 Twitter、小红书、Reddit、抖音...
   上下文：用户优先级为 B（记忆系统优化）和 C（自动监控），而非继续配置外部平台...

### 拒绝理由：单一文件难以维护、检索和提炼；结构化系统支持自动化
出现次数：1

1. **2026-02-27** - 拒绝：保持原有的单一文件日志方式...
   上下文：基于 Moltbook 社区讨论的 "The Sourdough Starter" 理念...

### 拒绝理由：Docker 需要 root 权限和用户确认；LinkedIn/Boss直聘需要复杂登录流程
出现次数：1

1. **2026-02-27** - 拒绝：安装 Docker、linkedin-scraper-mcp、mcp-bosszp...
   上下文：Agent-Reach 配置过程中的技术选型...

### 拒绝理由：AI 错误推断 Moltbook 链接为 `/posts/{id}` 复数格式，实际应为 `/post/{id}`，导致用户报告 404 错误，质疑 AI 在“骗人”
出现次数：1

1. **2026-02-27** - 拒绝：允许 AI 基于常见模式推断链接格式...
   上下文：Moltbook 浏览 cron 任务输出的链接全部为 404，用户提供了正确链接格式验证...


---

## 最近更新

# 2026-02-25 摘要

源文件: 2026-02-25.md

## 关键要点

- 上午工作（UTC 08:48-09:01）: - **awesome-openclaw-usecases**: 学习了30+个真实使用案例
- 上午工作（UTC 08:48-09:01）: - `scripts/token_optimizer.py` - Token优化配置
- 待办事项: - [✅] 获取并配置Brave API Key
- 当前状态总结 (UTC 12:59): 1. **Brave API 配置完成** ✅
- 当前状态总结 (UTC 12:59): - 配置文件: `/root/.openclaw/config/brave.json`
- 当前状态总结 (UTC 12:59): - 功能: 检查服务、进程、配置、文件状态
- 当前状态总结 (UTC 12:59): │   └── brave.json                # Brave 配置
- 当前状态总结 (UTC 12:59): │   └── brave_api_config.md       # 配置指南
- Coding Plan Lite 配置尝试 (UTC 14:01): ## Coding Plan Lite 配置尝试 (UTC 14:01)
- Coding Plan Lite 配置尝试 (UTC 14:01): **当前状态: 无法配置 Coding Plan Lite，需要正确的 API 端点 URL 或有效的 Key。**
- Coding Plan Lite 成功配置 (UTC 14:06): ## Coding Plan Lite 成功配置 (UTC 14:06)
- Coding Plan Lite 成功配置 (UTC 14:06): - 包含: API Key、端点、模型配置、文档链接
- Coding Plan Lite 成功配置 (UTC 14:06): | **状态** | ✅ 已配置完成，等待使用 |
- 或使用其他模型: **Coding Plan Lite 配置完成，可以随时使用！**
- 下午工作（UTC 12:36-12:44）: 1. **配置文件**: `/root/.openclaw/config/brave.json`

## 原始大小
字符数: 9307

---

# 2026-02-27 摘要

源文件: 2026-02-27.md

## 关键要点

- Moltbook 链接 404 严重幻觉问题: **教训**：AI 会“想当然”地套用常见模式，即使这个模式是错的
- 已完成的工作: - 配置位置: /root/.openclaw/agents/main/agent/models.json
- 当前技能状态: - ⚠️ 需要配置: Twitter搜索、全网搜索、小红书、抖音
- 待办事项: - [x] 检查 WORKFLOW_AUTO.md 是否需要创建 → 已创建
- 待办事项: - [x] 验证所有技能是否正常工作 → 部分完成
- 待办事项: - [x] 配置 Agent-Reach 的缺失功能 → 完成（核心功能就绪）
- 待办事项: - [x] 检查系统服务状态 → 正常
- Agent-Reach 配置进展（2026-02-27 14:30 UTC）: ## Agent-Reach 配置进展（2026-02-27 14:30 UTC）
- Agent-Reach 配置进展（2026-02-27 14:30 UTC）: - ✅ 配置 Exa MCP（全网语义搜索）→ 已可用
- 方案B实施：Moltbook Reader 技能创建（16:00-16:15 UTC）: ├── config.example.json # 配置模板
- 方案B实施：Moltbook Reader 技能创建（16:00-16:15 UTC）: **状态:** 方案B（Moltbook Reader技能）已创建并测试通过。技能直接调用API，避免AI幻觉，预计token消耗降低96%。等待用户决定是否创建新的cron任务进行对比测试。

## 原始大小
字符数: 4020

---

