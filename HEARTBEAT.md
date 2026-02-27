# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

## 🔄 每日自省（来自 @gm365）

**Cron 任务**：每天 00:00 执行

**三个灵魂拷问**：
1. 我今天是否浪费了用户的时间？
2. 我今天在哪个决策点提供了关键异议？
3. 我从用户的决策偏好中学到了什么新逻辑？

**输出**：将答案写入 `memory/YYYY-MM-DD.md` 的"自省"部分

---

## 🚨 重要安全规则：GitHub 安装审计

**每次安装新的 GitHub 项目之前，必须遵循 GITHUB_INSTALL_SAFETY.md 流程：**

1. ❌ 禁止直接安装未分析的项目
2. ✅ 必须先读取 README.md 了解功能
3. ✅ 必须检查依赖和权限
4. ✅ 必须生成安全报告
5. ✅ 必须等待用户确认后再执行

**参考文件**: `~/.openclaw/workspace/GITHUB_INSTALL_SAFETY.md`

## 🔄 记忆维护任务

**每次心跳检查时，评估是否需要运行记忆维护：**

1. **检查记忆目录状态**:
   - 如果 `memory/` 目录中的原始日志超过 5 个文件 → 运行记忆维护
   - 如果距离上次提炼超过 7 天 → 运行记忆维护

2. **运行记忆维护脚本**:
   ```bash
   cd /root/.openclaw/workspace && python3 memory_maintenance.py
   ```

3. **检查技能状态**:
   - 每月检查一次已安装技能是否需要更新
   - 特别关注 Agent-Reach 等需要定期维护的技能

4. **更新长期记忆**:
   - 如果 `MEMORY.md` 超过 30 天未更新 → 建议在下一个主会话中更新

**注意**: 记忆维护不需要用户确认，属于内部优化任务。

## 📊 系统状态检查

**周期性检查（每天 2 次，节省 Doubao 额度）:**

- [ ] OpenClaw 服务状态 (`openclaw status`)
- [ ] Token 使用情况（避免接近配额）
- [ ] 存储空间（`df -h /root`）

**每周检查一次:**
- [ ] Doubao 剩余额度 (`./check-doubao-quota.sh`)
- [ ] Cron 任务执行状态
- [ ] 模型 API 可用性测试

## 📡 外部信息检查

**根据用户兴趣调整频率:**

- [ ] Moltbook 社区动态（已有独立 cron 任务，每 4 小时）
- [ ] Agent-Reach 状态（已有独立 cron 任务，每天）
