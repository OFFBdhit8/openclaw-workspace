#!/bin/bash
# Agent-Reach 健康检查脚本
# 只有发现问题时才调用 AI，节省 90% 调用次数

LOG_FILE="/root/.openclaw/workspace/logs/agent_reach_check.log"
mkdir -p "$(dirname $LOG_FILE)"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始检查 Agent-Reach" >> $LOG_FILE

# 执行检查
output=$(agent-reach watch 2>&1)
exit_code=$?

echo "$output" >> $LOG_FILE

# 检查是否有问题
if echo "$output" | grep -qE "|⚠|ERROR|FAIL"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 发现问题，调用 AI 分析" >> $LOG_FILE
    
    # 调用 AI 分析
    analysis=$(echo "$output" | openclaw ask "分析以下 Agent-Reach 检查结果，指出问题并给出修复建议。简洁回答。" 2>&1)
    
    # 发送 Discord 通知
    openclaw message send --channel discord --to "1474072925199143167" "⚠️ Agent-Reach 检查异常\n\n$analysis"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 已发送通知" >> $LOG_FILE
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检查正常，静默" >> $LOG_FILE
fi

exit $exit_code
