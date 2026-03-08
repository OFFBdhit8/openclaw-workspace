#!/bin/bash
set -euo pipefail
STATUS_FILE="/root/.openclaw/workspace/memory/watchdog-status.json"
OUT_FILE="/root/.openclaw/workspace/memory/watchdog-dashboard.md"

if [ ! -f "$STATUS_FILE" ]; then
  cat > "$OUT_FILE" <<'EOF'
# Watchdog Dashboard

状态文件不存在。
EOF
  exit 0
fi

python3 - <<'PY'
import json
from pathlib import Path
status_path = Path('/root/.openclaw/workspace/memory/watchdog-status.json')
out_path = Path('/root/.openclaw/workspace/memory/watchdog-dashboard.md')
data = json.loads(status_path.read_text())
updated = data.get('updatedAt', '-')
main = data.get('main', {})
rescue = data.get('rescue', {})

def emoji(s):
    return {
        'healthy': '🟢',
        'degraded': '🟡',
        'restarting': '🟠',
        'critical': '🔴'
    }.get(s, '⚪')

def row(name, item):
    return f'''- **{name}** {emoji(item.get('status'))}
  - status: `{item.get('status','-')}`
  - http: `{item.get('lastHttpCode','-')}`
  - failCount: `{item.get('failCount','-')}/{item.get('threshold','-')}`
  - lastAction: `{item.get('lastAction','-')}`'''

text = f'''# Watchdog Dashboard

- updatedAt: `{updated}`

{row('Main', main)}

{row('Rescue', rescue)}
'''
out_path.write_text(text)
print(out_path)
PY
