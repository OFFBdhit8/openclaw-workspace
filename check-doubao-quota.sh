#!/bin/bash
# check-doubao-quota.sh - 检查 Doubao 剩余额度
# 用法：./check-doubao-quota.sh

API_KEY="51d28c39-105f-4325-b206-ca8b6056ae8a"
ENDPOINT="https://ark.cn-beijing.volces.com/api/v3"

echo "=== Doubao 额度检查 ==="
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 尝试获取用量信息
response=$(curl -s -X GET "${ENDPOINT}/usage" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json")

if echo "$response" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null; then
    echo "✅ API 调用成功"
    echo ""
    echo "$response" | python3 -m json.tool
else
    echo "⚠️ API 调用失败或返回非 JSON"
    echo "响应内容:"
    echo "$response"
    echo ""
    echo "建议:"
    echo "1. 访问 https://console.volcengine.com/ark 查看用量"
    echo "2. 检查 API Key 是否正确"
fi

echo ""
echo "=== 当前 OpenClaw 会话 Tokens ==="
openclaw status 2>/dev/null | grep -A 15 "Sessions" | head -20
