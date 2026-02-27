#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试 Coding Plan Lite 端点
"""

import requests
import json

CODING_PLAN_KEY = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
CODING_PLAN_ENDPOINT = "https://coding.dashscope.aliyuncs.com/v1"

print("🔍 快速测试 Coding Plan Lite...")
print(f"🌐 端点: {CODING_PLAN_ENDPOINT}")

# 直接测试最可能的配置
chat_url = f"{CODING_PLAN_ENDPOINT}/chat/completions"
headers = {
    "Authorization": f"Bearer {CODING_PLAN_KEY}",
    "Content-Type": "application/json"
}

# 根据阿里云文档，Coding Plan 可能使用 qwen 模型
test_data = {
    "model": "qwen-plus",  # 阿里云通用模型
    "messages": [
        {"role": "system", "content": "You are a coding assistant."},
        {"role": "user", "content": "Hello, test connection."}
    ],
    "max_tokens": 30
}

try:
    print("📤 发送测试请求...")
    response = requests.post(chat_url, headers=headers, json=test_data, timeout=10)
    
    print(f"📥 响应状态: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        print(f"✅ 连接成功!")
        print(f"🤖 模型响应: {content}")
        
        # 显示使用情况
        usage = data.get("usage", {})
        print(f"📊 Token使用:")
        print(f"   输入: {usage.get('prompt_tokens', 0)}")
        print(f"   输出: {usage.get('completion_tokens', 0)}")
        print(f"   总计: {usage.get('total_tokens', 0)}")
        
    elif response.status_code == 400:
        error_data = response.json()
        error_msg = error_data.get("error", {}).get("message", response.text[:200])
        print(f"❌ 请求错误: {error_msg}")
        
        # 尝试其他可能的模型
        print("\n🔄 尝试其他模型...")
        other_models = ["qwen-turbo", "qwen-max", "qwen-coder", "deepseek-coder"]
        
        for model in other_models:
            test_data["model"] = model
            try:
                resp = requests.post(chat_url, headers=headers, json=test_data, timeout=5)
                if resp.status_code == 200:
                    print(f"✅ 找到可用模型: {model}")
                    break
                else:
                    print(f"❌ {model}: HTTP {resp.status_code}")
            except:
                print(f"❌ {model}: 请求失败")
                
    elif response.status_code == 401:
        print("❌ 认证失败 - API Key 无效")
    elif response.status_code == 404:
        print("❌ 端点不存在")
    else:
        print(f"❌ 其他错误: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("❌ 请求超时")
except Exception as e:
    print(f"❌ 请求异常: {e}")
