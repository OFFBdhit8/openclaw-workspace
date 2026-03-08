# HEARTBEAT.md

## 每次心跳检查（轮换执行，不要每次全做）

### 基础设施巡检
- 检查主机 Gateway 状态：`systemctl --user status openclaw-gateway`
- 检查救援机状态：`systemctl --user status openclaw-gateway-rescue`
- 检查告警文件：`cat /root/.openclaw-rescue/alert-gateway-down 2>/dev/null`
- 如果有告警，立即通知老板并尝试修复
- 检查磁盘空间：`df -h /`（>85% 告警）
- 检查内存：`free -h`

### 记忆维护
- 读取最近的 memory/YYYY-MM-DD.md
- 有值得长期保留的内容就更新 MEMORY.md
- 清理过期的临时文件

### 日历/待办
- 如果飞书日历已授权，检查未来 24h 的日程
- 检查待办事项进度

## 规则
- 深夜 23:00-08:00 除非紧急否则 HEARTBEAT_OK
- 没有新情况就 HEARTBEAT_OK，不要为了说话而说话
- 发现问题先修，修不了再通知老板
