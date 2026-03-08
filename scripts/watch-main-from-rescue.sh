#!/bin/bash
set -euo pipefail
TARGET_PORT=18789
TARGET_SERVICE="openclaw-gateway.service"
LOG_FILE="/root/.openclaw-rescue/watchdog.log"
FAIL_COUNT_FILE="/root/.openclaw-rescue/watchdog-fails"
ALERT_FILE="/root/.openclaw-rescue/alert-gateway-down"
STATUS_FILE="/root/.openclaw/workspace/memory/watchdog-status.json"
DASHBOARD_SCRIPT="/root/.openclaw/workspace/scripts/render-watchdog-dashboard.sh"
DASHBOARD_FILE="/root/.openclaw/workspace/memory/watchdog-dashboard.md"
MAX_FAILS=3
CHECK_URL="http://127.0.0.1:${TARGET_PORT}/health"

ts(){ date '+%Y-%m-%d %H:%M:%S'; }
iso(){ date -Iseconds; }
mkdir -p "$(dirname "$STATUS_FILE")"
[ -f "$FAIL_COUNT_FILE" ] || echo 0 > "$FAIL_COUNT_FILE"
FAILS=$(cat "$FAIL_COUNT_FILE" 2>/dev/null || echo 0)
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 "$CHECK_URL" 2>/dev/null || true)

write_status(){
python3 - <<PY
import json
p = "$STATUS_FILE"
try:
    data = json.load(open(p))
except Exception:
    data = {}
data['updatedAt'] = '$(iso)'
data['main'] = {
  'lastHttpCode': '${HTTP_CODE:-ERR}',
  'failCount': ${FAILS},
  'threshold': ${MAX_FAILS},
  'status': '$1',
  'lastAction': '$2'
}
with open(p, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
PY
[ -x "$DASHBOARD_SCRIPT" ] && "$DASHBOARD_SCRIPT" >/dev/null 2>&1 || true
}

notify_feishu(){
  local title="$1"
  local extra="$2"
  local dashboard
  dashboard=$(cat "$DASHBOARD_FILE" 2>/dev/null || echo 'dashboard unavailable')
  /root/.nvm/versions/node/v22.22.0/bin/openclaw --profile rescue run --message "使用 message 工具发送一条飞书群消息到群 oc_1dac3242c001625735760f54c579b7ec（channel=feishu）。消息内容如下，原样发送，不要补充：${title}
${extra}

${dashboard}" >> /root/.openclaw-rescue/watchdog-notify.log 2>&1 || true
}

if [ "$HTTP_CODE" = "200" ]; then
  if [ "$FAILS" -gt 0 ]; then
    echo "$(ts) [RECOVERED] main recovered after ${FAILS} fails" >> "$LOG_FILE"
    echo 0 > "$FAIL_COUNT_FILE"
    FAILS=0
    write_status healthy recovered
    rm -f "$ALERT_FILE"
    notify_feishu "[Watchdog] 主机 Gateway 已恢复" "目标=main 端口=18789 原先连续失败，当前已恢复。时间=$(ts)"
    exit 0
  fi
  echo 0 > "$FAIL_COUNT_FILE"
  FAILS=0
  write_status healthy none
  rm -f "$ALERT_FILE"
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
    notify_feishu "[Watchdog] 主机 Gateway 自动恢复成功" "目标=main 端口=18789 原因=连续${MAX_FAILS}次健康检查失败，已自动重启并恢复。时间=$(ts)"
    exit 0
  fi
  echo "$(ts) [CRITICAL] main still down after restart HTTP=${HTTP_AFTER:-ERR}" >> "$LOG_FILE"
  echo "$(ts) main gateway still unhealthy after auto-restart" > "$ALERT_FILE"
  HTTP_CODE="$HTTP_AFTER"
  write_status critical restart-failed
  notify_feishu "[Watchdog] 主机 Gateway 故障未自动恢复" "目标=main 端口=18789 状态=连续${MAX_FAILS}次健康检查失败且重启后仍异常 HTTP=${HTTP_AFTER:-ERR}。时间=$(ts)"
  if [ -x /root/.openclaw-rescue/scripts/smart-repair.sh ]; then
    /root/.openclaw-rescue/scripts/smart-repair.sh >> /root/.openclaw-rescue/smart-repair.log 2>&1 &
  fi
fi
