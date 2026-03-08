#!/bin/bash
set -euo pipefail
TARGET_PORT=19789
TARGET_SERVICE="openclaw-gateway-rescue.service"
LOG_FILE="/root/.openclaw/watchdog-rescue.log"
FAIL_COUNT_FILE="/root/.openclaw/watchdog-rescue-fails"
ALERT_FILE="/root/.openclaw/alert-rescue-down"
MAX_FAILS=2
CHECK_URL="http://127.0.0.1:${TARGET_PORT}/health"

ts(){ date '+%Y-%m-%d %H:%M:%S'; }
[ -f "$FAIL_COUNT_FILE" ] || echo 0 > "$FAIL_COUNT_FILE"
FAILS=$(cat "$FAIL_COUNT_FILE" 2>/dev/null || echo 0)
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 "$CHECK_URL" 2>/dev/null || true)

if [ "$HTTP_CODE" = "200" ]; then
  if [ "$FAILS" -gt 0 ]; then echo "$(ts) [RECOVERED] rescue recovered after ${FAILS} fails" >> "$LOG_FILE"; fi
  echo 0 > "$FAIL_COUNT_FILE"
  rm -f "$ALERT_FILE"
  exit 0
fi

FAILS=$((FAILS+1))
echo "$FAILS" > "$FAIL_COUNT_FILE"
echo "$(ts) [FAIL #${FAILS}] rescue HTTP=${HTTP_CODE:-ERR}" >> "$LOG_FILE"

if [ "$FAILS" -ge "$MAX_FAILS" ]; then
  echo "$(ts) [ACTION] restarting $TARGET_SERVICE" >> "$LOG_FILE"
  systemctl --user restart "$TARGET_SERVICE" >> "$LOG_FILE" 2>&1 || true
  sleep 30
  HTTP_AFTER=$(curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 --max-time 10 "$CHECK_URL" 2>/dev/null || true)
  if [ "$HTTP_AFTER" = "200" ]; then
    echo "$(ts) [FIXED] rescue restarted successfully" >> "$LOG_FILE"
    echo 0 > "$FAIL_COUNT_FILE"
    rm -f "$ALERT_FILE"
    exit 0
  fi
  echo "$(ts) [CRITICAL] rescue still down after restart HTTP=${HTTP_AFTER:-ERR}" >> "$LOG_FILE"
  echo "$(ts) rescue gateway still unhealthy after auto-restart" > "$ALERT_FILE"
fi
