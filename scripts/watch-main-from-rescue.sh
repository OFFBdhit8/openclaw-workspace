#!/bin/bash
set -euo pipefail
TARGET_NAME="main"
TARGET_PORT=18789
TARGET_SERVICE="openclaw-gateway.service"
LOG_FILE="/root/.openclaw-rescue/watchdog.log"
FAIL_COUNT_FILE="/root/.openclaw-rescue/watchdog-fails"
ALERT_FILE="/root/.openclaw-rescue/alert-gateway-down"
STATUS_FILE="/root/.openclaw/workspace/memory/watchdog-status.json"
MAX_FAILS=3
CHECK_URL="http://127.0.0.1:${TARGET_PORT}/health"

ts(){ date '+%Y-%m-%d %H:%M:%S'; }
iso(){ date -Iseconds; }
mkdir -p "$(dirname "$STATUS_FILE")"
[ -f "$FAIL_COUNT_FILE" ] || echo 0 > "$FAIL_COUNT_FILE"
FAILS=$(cat "$FAIL_COUNT_FILE" 2>/dev/null || echo 0)
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 "$CHECK_URL" 2>/dev/null || true)

write_status(){
cat > "$STATUS_FILE" <<JSON
{
  "updatedAt": "$(iso)",
  "main": {
    "lastHttpCode": "${HTTP_CODE:-ERR}",
    "failCount": ${FAILS},
    "threshold": ${MAX_FAILS},
    "status": "$1",
    "lastAction": "$2"
  }
}
JSON
}

notify_feishu(){
  local text="$1"
  /root/.nvm/versions/node/v22.22.0/bin/openclaw --profile rescue run --message "使用 message 工具发送一条飞书群告警到群 oc_1dac3242c001625735760f54c579b7ec（channel=feishu）。消息内容如下，原样发送，不要补充：$text" >> /root/.openclaw-rescue/watchdog-notify.log 2>&1 || true
}

if [ "$HTTP_CODE" = "200" ]; then
  if [ "$FAILS" -gt 0 ]; then echo "$(ts) [RECOVERED] main recovered after ${FAILS} fails" >> "$LOG_FILE"; fi
  echo 0 > "$FAIL_COUNT_FILE"
  rm -f "$ALERT_FILE"
  FAILS=0
  write_status healthy none
  exit 0
fi

FAILS=$((FAILS+1))
echo "$FAILS" > "$FAIL_COUNT_FILE"
echo "$(ts) [FAIL #${FAILS}] main HTTP=${HTTP_CODE:-ERR}" >> "$LOG_FILE"
write_status degraded none

if [ "$FAILS" -ge "$MAX_FAILS" ]; then
  echo "$(ts) [ACTION] restarting $TARGET_SERVICE" >> "$LOG_FILE"
  write_status restarting restart-service
  systemctl --user restart "$TARGET_SERVICE" >> "$LOG_FILE" 2>&1 || true
  sleep 30
  HTTP_AFTER=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 "$CHECK_URL" 2>/dev/null || true)
  if [ "$HTTP_AFTER" = "200" ]; then
    echo "$(ts) [FIXED] main restarted successfully" >> "$LOG_FILE"
    echo 0 > "$FAIL_COUNT_FILE"
    rm -f "$ALERT_FILE"
    FAILS=0
    HTTP_CODE="$HTTP_AFTER"
    write_status healthy restart-fixed
    notify_feishu "[Watchdog] 主机 Gateway 自动恢复成功。目标=main 端口=18789 原因=连续${MAX_FAILS}次健康检查失败，已自动重启并恢复。时间=$(ts)"
    exit 0
  fi
  echo "$(ts) [CRITICAL] main still down after restart HTTP=${HTTP_AFTER:-ERR}" >> "$LOG_FILE"
  echo "$(ts) main gateway still unhealthy after auto-restart" > "$ALERT_FILE"
  HTTP_CODE="$HTTP_AFTER"
  write_status critical restart-failed
  notify_feishu "[Watchdog] 主机 Gateway 故障未自动恢复。目标=main 端口=18789 状态=连续${MAX_FAILS}次健康检查失败且重启后仍异常 HTTP=${HTTP_AFTER:-ERR}。时间=$(ts)"
  if [ -x /root/.openclaw-rescue/scripts/smart-repair.sh ]; then
    /root/.openclaw-rescue/scripts/smart-repair.sh >> /root/.openclaw-rescue/smart-repair.log 2>&1 &
  fi
fi
