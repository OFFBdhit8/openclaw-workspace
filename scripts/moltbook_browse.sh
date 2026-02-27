#!/bin/bash
# Moltbook 浏览脚本 - 使用 API 直接获取，避免 AI 幻觉
# 只有 API 失败时才调用 AI 备用方案

API_KEY="moltbook_sk_MDQ7Y7CU2cPX_yyxf6MM9ZZpXSAXZnYr"
API_URL="https://moltbook.com/api/v1/posts"
DISCORD_CHANNEL="1474072925199143167"
LOG_FILE="/root/.openclaw/workspace/logs/moltbook.log"

mkdir -p "$(dirname $LOG_FILE)"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始获取 Moltbook" >> $LOG_FILE

# 调用 API 获取帖子
response=$(curl -s -H "Authorization: Bearer $API_KEY" "$API_URL?limit=3" 2>&1)

# 检查 API 是否成功
if echo "$response" | grep -q '"success":true'; then
    # API 成功，使用 Python 解析 JSON
    msg=$(echo "$response" | python3 << 'PYEOF'
import json
import sys

try:
    data = json.load(sys.stdin)
    posts = data.get('posts', [])[:3]
    
    msg = "🔥 Moltbook 最新\n"
    for post in posts:
        title = post.get('title', '无标题')[:15]
        content = post.get('content', '')[:40].replace('\n', ' ')
        post_id = post.get('id', '')
        msg += f"• [{title}] [{content}...]\nhttps://moltbook.com/post/{post_id}\n"
    
    print(msg)
except Exception as e:
    print(f"解析失败：{e}")
    sys.exit(1)
PYEOF
)
    
    # 发送 Discord 消息
    if [ -n "$msg" ]; then
        openclaw message send --channel discord --target "$DISCORD_CHANNEL" --message "$msg"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 发送成功" >> $LOG_FILE
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 消息为空" >> $LOG_FILE
    fi
else
    # API 失败，调用 AI 备用方案
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] API 失败：$response" >> $LOG_FILE
    openclaw message send --channel discord --to "$DISCORD_CHANNEL" \
        "⚠️ Moltbook API 不可用，已切换到 AI 备用方案。\n\n响应：$response"
fi
