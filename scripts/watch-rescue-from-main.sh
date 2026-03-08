#!/bin/bash
set -euo pipefail
TARGET_NAME="rescue"
TARGET_PORT=19789
TARGET_SERVICE="openclaw-gateway-rescue.service"
LOG_FILE="/root/.openclaw/watchdog-rescue.log"
FAIL_COUNT_FILE="/root/.openclaw/watchdog-rescue-fails"
ALERT_FILE="/root/.openclaw/alert-rescue-down"
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
python3 - <<PY
import json, os
p = "$STATUS_FILE"
try:
    data = json.load(open(p))
except Exception:
    data = {}
data['updatedAt'] = '$(iso)'
data['rescue'] = {
  'lastHttpCode': '${HTTP_CODE:-ERR}',
  'failCount': ${FAILS},
  'threshold': ${MAX_FAILS},
  'status': '$1',
  'lastAction': '$2'
}
with open(p, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
PY
}

if [ "$HTTP_CODE" = "200" ]; then
  if [ "$FAILS" -gt 0 ]; then echo "$(ts) [RECOVERED] rescue recovered after ${FAILS} fails" >> "$LOG_FILE"; fi
  echo 0 > "$FAIL_COUNT_FILE"
  rm -f "$ALERT_FILE"
  FAILS=0
  write_status healthy none
  exit 0
fi

FAILS=$((FAILS+1))
echo "$FAILS" > "$FAIL_COUNT_FILE"
echo "$(ts) [FAIL #${FAILS}] rescue HTTP=${HTTP_CODE:-ERR}" >> "$LOG_FILE"
write_status degraded none

if [ "$FAILS" -ge "$MAX_FAILS" ]; then
  echo "$(ts) [ACTION] restarting $TARGET_SERVICE" >> "$LOG_FILE"
  write_status restarting restart-service
  systemctl --user restart "$TARGET_SERVICE" >> "$LOG_FILE" 2>&1 || true
  sleep 30
  HTTP_AFTER=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 "$CHECK_URL" 2>/dev/null || true)
  if [ "$HTTP_AFTER" = "200" ]; then
    echo "$(ts) [FIXED] rescue restarted successfully" >> "$LOG_FILE"
    echo 0 > "$FAIL_COUNT_FILE"
    rm -f "$ALERT_FILE"
    FAILS=0
    HTTP_CODE="$HTTP_AFTER"
    write_status healthy restart-fixed
    exit 0
  fi
  echo "$(ts) [CRITICAL] rescue still down after restart HTTP=${HTTP_AFTER:-ERR}" >> "$LOG_FILE"
  echo "$(ts) rescue gateway still unhealthy after auto-restart" > "$ALERT_FILE"
  HTTP_CODE="$HTTP_AFTER"
  write_status critical restart-failed
fi
