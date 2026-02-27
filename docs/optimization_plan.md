# OpenClaw 调用次数优化方案

## 📊 当前调用分析

### 定时任务（每日调用次数）
| 任务 | 频率 | 每日调用 | 模型 | 估算 Token/次 |
|------|------|----------|------|---------------|
| Moltbook 浏览 | 每 4 小时 | 6 次 | deepseek-chat | ~2k |
| Agent-Reach 检查 | 每天 1 次 | 1 次 | deepseek-chat | ~1k |
| 心跳检查 | 30 分钟 | 48 次* | qwen3.5-plus | ~0.5k |

*注：当前 HEARTBEAT.md 为空，实际可能不执行 AI 调用

**每日总计**: 约 7-55 次调用（取决于心跳配置）

---

## 🎯 优化策略

### 策略 1: 降低 Moltbook 浏览频率 ⭐⭐⭐
**当前**: 每 4 小时 (6 次/天)
**优化**: 每 8 小时 (3 次/天) 或 每天 2 次

**理由**:
- Moltbook 内容更新频率不高
- 用户不需要实时追踪所有帖子
- 节省 50-67% 调用

**实施**:
```bash
openclaw cron update a8a6e978-bddf-4b88-8382-b5952f05ef3a --schedule "0 8,16,0 * * *"
# 或
openclaw cron update a8a6e978-bddf-4b88-8382-b5952f05ef3a --schedule "0 9,21 * * *"
```

### 策略 2: 使用便宜模型执行简单任务 ⭐⭐⭐
**当前**: deepseek-chat (~$0.27/1M tokens)
**优化**: qwen-turbo (~$0.05/1M tokens) 或 腾讯混元

**适用任务**:
- Moltbook 浏览（只需提取标题 + 链接）
- Agent-Reach 状态检查（只需解析命令输出）
- 系统状态检查

**实施**:
```bash
openclaw cron update a8a6e978-bddf-4b88-8382-b5952f05ef3a --model qwen/qwen-turbo
openclaw cron update b497b136-9d2f-4208-ba1b-c080c5b92838 --model qwen/qwen-turbo
```

### 策略 3: 合并检查任务 ⭐⭐
**当前**: 多个独立 cron 任务
**优化**: 创建单一"系统巡检"任务

**示例**:
```json
{
  "name": "每日系统巡检",
  "schedule": "0 9 * * *",
  "message": "执行以下检查并汇总报告：
1. openclaw status
2. df -h /root
3. agent-reach watch
4. 检查 cron 任务状态
只有发现问题时才通知用户"
}
```

**节省**: 3 次调用 → 1 次调用

### 策略 4: 优化提示词减少 Token ⭐⭐
**当前 Moltbook 提示词**: ~150 tokens
**优化后**: ~50 tokens

**优化示例**:
```
# 优化前（150 tokens）
浏览 Moltbook 最新帖子，只取前 3 个。先快速扫描所有帖子，找出最重要的 3 个。
对每个帖子：1. 简短标题（10 字内）2. 一句话核心观点（15 字内）3. 链接...

# 优化后（50 tokens）
Moltbook 最新 3 帖。格式：🔥 [标题] [观点] [链接]。极度简洁。
```

**节省**: 67% token 消耗

### 策略 5: 条件执行（静默模式） ⭐⭐⭐
**原则**: 无异常不通知

**实施**:
- Agent-Reach 检查：只有发现问题才发送消息
- 系统检查：只有异常才通知
- Moltbook：可以改为"按需查看"而非定时推送

**节省**: 80% 的消息发送（但 AI 调用仍存在）

### 策略 6: 使用缓存和本地脚本 ⭐⭐⭐⭐
**最佳方案**: 将简单检查改为本地脚本

**示例 - Agent-Reach 检查**:
```bash
#!/bin/bash
# /root/.openclaw/workspace/scripts/check_agent_reach.sh
output=$(agent-reach watch 2>&1)
if echo "$output" | grep -q "❌\|⚠️"; then
    # 有问题，调用 AI 分析
    echo "$output" | openclaw ask "分析问题并给出建议"
else
    # 正常，静默
    exit 0
fi
```

**节省**: 90% 的 AI 调用（只在异常时调用）

---

## 📋 推荐实施方案

### 立即执行（高优先级）
1. ✅ **Moltbook 频率降低**: 4 小时 → 8 小时（节省 50%）
2. ✅ **切换便宜模型**: deepseek-chat → qwen-turbo（节省 80% 成本）
3. ✅ **优化提示词**: 精简到 50 tokens 内（节省 67% token）

### 中期实施（中优先级）
4. ⏳ **创建本地检查脚本**: 将简单检查移到 shell 脚本
5. ⏳ **合并 cron 任务**: 多个检查合并为单一任务

### 长期优化（低优先级）
6. ⏳ **按需查看**: 改为 Discord 命令触发，而非定时推送
7. ⏳ **结果缓存**: 缓存 API 响应，避免重复调用

---

## 💰 预期效果

| 优化项 | 当前 | 优化后 | 节省 |
|--------|------|--------|------|
| 每日调用次数 | 7-55 次 | 3-10 次 | 57-82% |
| 每日 Token 消耗 | ~15k | ~3k | 80% |
| 月度成本估算 | ¥50-100 | ¥10-20 | 80% |

---

## 🔧 执行命令

```bash
# 1. 降低 Moltbook 频率（4 小时 → 8 小时）
openclaw cron update a8a6e978-bddf-4b88-8382-b5952f05ef3a --schedule "0 */8 * * *"

# 2. 切换到便宜模型
openclaw cron update a8a6e978-bddf-4b88-8382-b5952f05ef3a --model qwen/qwen-turbo
openclaw cron update b497b136-9d2f-4208-ba1b-c080c5b92838 --model qwen/qwen-turbo

# 3. 更新提示词（需要编辑 cron 配置）
# 手动编辑 ~/.openclaw/cron/jobs.json 中的 payload.message 字段
```

---

**创建时间**: 2026-02-27
**状态**: 待实施
