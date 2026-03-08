#!/bin/bash
# OpenClaw 每晚安全巡检脚本 v1.0
# 基于慢雾安全实践指南 v2.7
# 启晋娴达工作室

set -euo pipefail
OC="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
REPORT_DIR="/tmp/openclaw/security-reports"
DATE=$(date +%Y-%m-%d)
REPORT="$REPORT_DIR/report-$DATE.txt"
SUMMARY=""
ALERTS=0

mkdir -p "$REPORT_DIR"
echo "🛡️ OpenClaw 安全巡检 $DATE $(date +%H:%M)" > "$REPORT"
echo "========================================" >> "$REPORT"

add_result() {
  local num=$1 name=$2 status=$3 detail=$4
  if [ "$status" = "WARN" ] || [ "$status" = "ALERT" ]; then
    SUMMARY="${SUMMARY}\n${num}. ${name}: ⚠️ ${detail}"
    ALERTS=$((ALERTS + 1))
  else
    SUMMARY="${SUMMARY}\n${num}. ${name}: ✅ ${detail}"
  fi
  echo -e "\n[$num] $name: $status\n$detail" >> "$REPORT"
}

# 1. 进程与网络审计
echo "--- [1] 进程与网络 ---" >> "$REPORT"
LISTEN=$(ss -tlnp 2>/dev/null | tail -n +2)
LISTEN_COUNT=$(echo "$LISTEN" | grep -c . || true)
OUTBOUND=$(ss -tnp state established 2>/dev/null | grep -v "127.0.0.1" | tail -n +2)
OUT_COUNT=$(echo "$OUTBOUND" | grep -c . || true)
echo "$LISTEN" >> "$REPORT"
add_result 1 "进程网络" "OK" "${LISTEN_COUNT} 个监听端口, ${OUT_COUNT} 个出站连接"

# 2. 敏感目录变更（24h）
echo "--- [2] 目录变更 ---" >> "$REPORT"
CHANGED=$(find "$OC/" /etc/ ~/.ssh/ -maxdepth 2 -mmin -1440 -type f 2>/dev/null | head -30)
CHANGE_COUNT=$(echo "$CHANGED" | grep -c . || true)
echo "$CHANGED" >> "$REPORT"
if [ "$CHANGE_COUNT" -gt 20 ]; then
  add_result 2 "目录变更" "WARN" "${CHANGE_COUNT} 个文件变更（偏多）"
else
  add_result 2 "目录变更" "OK" "${CHANGE_COUNT} 个文件变更"
fi

# 3. 系统定时任务
echo "--- [3] 系统 Cron ---" >> "$REPORT"
SYS_CRON=$(crontab -l 2>/dev/null || echo "(empty)")
echo "$SYS_CRON" >> "$REPORT"
# 白名单：已知安全的 cron 任务关键词
CRON_WHITELIST="stargate|feishu-plugin|gateway-watchdog|daily-reflection|morning-brief|weekly-research|openclaw"
CRON_SUSPICIOUS=$(echo "$SYS_CRON" | grep -iE "curl|wget|bash|sh|python|nc " | grep -ivE "$CRON_WHITELIST" || true)
if [ -n "$CRON_SUSPICIOUS" ]; then
  add_result 3 "系统Cron" "WARN" "发现可疑任务: $CRON_SUSPICIOUS"
else
  CRON_COUNT=$(echo "$SYS_CRON" | grep -c "^[^#]" || true)
  add_result 3 "系统Cron" "OK" "${CRON_COUNT} 个任务（均在白名单内）"
fi

# 4. SSH 安全
echo "--- [4] SSH 安全 ---" >> "$REPORT"
SSH_FAIL=$(journalctl -u sshd --since "24h ago" --no-pager 2>/dev/null | grep -c "Failed password" || true)
LAST_LOGIN=$(last -5 2>/dev/null || echo "N/A")
echo "$LAST_LOGIN" >> "$REPORT"
if [ "$SSH_FAIL" -gt 50 ]; then
  add_result 4 "SSH安全" "WARN" "${SSH_FAIL} 次失败尝试（疑似爆破）"
else
  add_result 4 "SSH安全" "OK" "${SSH_FAIL} 次失败尝试"
fi

# 5. 配置文件完整性
echo "--- [5] 配置基线 ---" >> "$REPORT"
if [ -f "$OC/.config-baseline.sha256" ]; then
  HASH_CHECK=$(sha256sum -c "$OC/.config-baseline.sha256" 2>&1)
  echo "$HASH_CHECK" >> "$REPORT"
  if echo "$HASH_CHECK" | grep -q "FAILED"; then
    add_result 5 "配置基线" "ALERT" "哈希校验失败！配置文件可能被篡改"
  else
    add_result 5 "配置基线" "OK" "哈希校验通过"
  fi
  # 权限检查
  OC_PERM=$(stat -c %a "$OC/openclaw.json" 2>/dev/null)
  PAIRED_PERM=$(stat -c %a "$OC/devices/paired.json" 2>/dev/null)
  if [ "$OC_PERM" != "600" ] || [ "$PAIRED_PERM" != "600" ]; then
    add_result 5 "配置基线" "WARN" "权限异常: openclaw.json=$OC_PERM paired.json=$PAIRED_PERM"
  fi
else
  add_result 5 "配置基线" "WARN" "未找到哈希基线文件"
fi

# 6. 磁盘使用
echo "--- [6] 磁盘 ---" >> "$REPORT"
DISK_PCT=$(df / | tail -1 | awk '{print $5}' | tr -d '%')
BIG_FILES=$(find /tmp /root -size +100M -type f 2>/dev/null | head -10)
BIG_COUNT=$(echo "$BIG_FILES" | grep -c . || true)
echo "使用率: ${DISK_PCT}%" >> "$REPORT"
echo "$BIG_FILES" >> "$REPORT"
if [ "$DISK_PCT" -gt 85 ]; then
  add_result 6 "磁盘容量" "WARN" "根分区 ${DISK_PCT}%（>85%）, ${BIG_COUNT} 个大文件"
else
  add_result 6 "磁盘容量" "OK" "根分区 ${DISK_PCT}%, ${BIG_COUNT} 个大文件(>100MB)"
fi

# 7. 内存状况
echo "--- [7] 内存 ---" >> "$REPORT"
MEM_INFO=$(free -h | grep Mem)
MEM_TOTAL=$(echo "$MEM_INFO" | awk '{print $2}')
MEM_USED=$(echo "$MEM_INFO" | awk '{print $3}')
MEM_PCT=$(free | grep Mem | awk '{printf "%.0f", $3/$2*100}')
SWAP_USED=$(free -h | grep Swap | awk '{print $3}')
echo "$MEM_INFO" >> "$REPORT"
if [ "$MEM_PCT" -gt 85 ]; then
  add_result 7 "内存" "WARN" "使用 ${MEM_PCT}% (${MEM_USED}/${MEM_TOTAL}), Swap ${SWAP_USED}"
else
  add_result 7 "内存" "OK" "使用 ${MEM_PCT}% (${MEM_USED}/${MEM_TOTAL}), Swap ${SWAP_USED}"
fi

# 8. Gateway 状态
echo "--- [8] Gateway ---" >> "$REPORT"
GW_STATUS=$(systemctl --user is-active openclaw-gateway 2>/dev/null || echo "unknown")
GW_RESCUE=$(systemctl --user is-active openclaw-gateway-rescue 2>/dev/null || echo "unknown")
if [ "$GW_STATUS" = "active" ]; then
  add_result 8 "Gateway" "OK" "主机=$GW_STATUS, 救援机=$GW_RESCUE"
else
  add_result 8 "Gateway" "ALERT" "主机=$GW_STATUS, 救援机=$GW_RESCUE"
fi

# 9. 高资源进程
echo "--- [9] 高资源进程 ---" >> "$REPORT"
TOP_PROCS=$(ps aux --sort=-%mem | head -6)
echo "$TOP_PROCS" >> "$REPORT"
add_result 9 "高资源进程" "OK" "Top 5 已记录"

# 10. 环境变量凭证检查
echo "--- [10] 环境变量 ---" >> "$REPORT"
GW_PID=$(pgrep -f "openclaw.*gateway" | head -1 || true)
if [ -n "$GW_PID" ] && [ -f "/proc/$GW_PID/environ" ]; then
  ENV_KEYS=$(tr '\0' '\n' < /proc/$GW_PID/environ 2>/dev/null | grep -iE "KEY|TOKEN|SECRET|PASSWORD" | sed 's/=.*/=***/' || true)
  ENV_COUNT=$(echo "$ENV_KEYS" | grep -c . || true)
  echo "$ENV_KEYS" >> "$REPORT"
  add_result 10 "环境变量" "OK" "${ENV_COUNT} 个凭证变量（值已脱敏）"
else
  add_result 10 "环境变量" "WARN" "无法读取 Gateway 进程环境"
fi

# 11. 明文凭证泄露扫描 (DLP)
echo "--- [11] DLP 扫描 ---" >> "$REPORT"
DLP_HITS=$(grep -rlE "(0x[a-fA-F0-9]{64}|[a-fA-F0-9]{64})" "$OC/workspace/memory/" 2>/dev/null | head -5 || true)
MNEMONIC_HITS=$(grep -rlE "\b(abandon|ability|able|about|above)\b.*\b(word|wolf|woman|wonder)\b" "$OC/workspace/memory/" 2>/dev/null | head -5 || true)
if [ -n "$DLP_HITS" ] || [ -n "$MNEMONIC_HITS" ]; then
  add_result 11 "DLP扫描" "ALERT" "发现疑似明文私钥或助记词！"
else
  add_result 11 "DLP扫描" "OK" "memory/ 未发现明文私钥或助记词"
fi

# 12. Skill 完整性
echo "--- [12] Skill 基线 ---" >> "$REPORT"
SKILL_COUNT=$(ls -d "$OC/workspace/skills/"*/ 2>/dev/null | wc -l || echo 0)
add_result 12 "Skill基线" "OK" "${SKILL_COUNT} 个 Skills 已安装"

# 13. 黄线操作交叉验证
echo "--- [13] 黄线审计 ---" >> "$REPORT"
SUDO_COUNT=$(grep -c "sudo" /var/log/auth.log 2>/dev/null || echo 0)
TODAY_MEM="$OC/workspace/memory/$(date +%Y-%m-%d).md"
MEM_SUDO=$(grep -c "sudo" "$TODAY_MEM" 2>/dev/null || echo 0)
add_result 13 "黄线审计" "OK" "auth.log sudo: ${SUDO_COUNT}, memory 记录: ${MEM_SUDO}"

# === 输出汇总 ===
echo "" >> "$REPORT"
echo "========================================" >> "$REPORT"
echo "巡检完成: $(date)" >> "$REPORT"
echo "告警数: $ALERTS" >> "$REPORT"

echo ""
echo "🛡️ OpenClaw 每日安全巡检简报 ($DATE)"
echo ""
echo -e "$SUMMARY"
echo ""
if [ "$ALERTS" -gt 0 ]; then
  echo "⚠️ 发现 $ALERTS 个告警，详见: $REPORT"
else
  echo "✅ 全部通过，详见: $REPORT"
fi
