#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简测试 - 找到正确的模型名称
"""

import requests
import json

CODING_PLAN_KEY = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
CODING_PLAN_ENDPOINT = "https://coding.dashscope.aliyuncs.com/v1"

# 根据阿里云 Coding Plan 文档，最可能的模型
test_models = [
    "qwen2.5-coder-7b-instruct",
    "qwen2.5-coder-14b-instruct", 
    "codeqwen1.5-7b-chat",
    "qwen-coder",
    "code-llama",
    "codellama"
]

print("🚀 立即测试 Coding Plan Lite 模型")
print("="*50)

for model in test_models[:2]:  # 只测试前两个
    print(f"\n测试模型: {model}")
    
    headers = {
        "Authorization": f"Bearer {CODING_PLAN_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "max_tokens": 10
    }
    
    try:
        response = requests.post(
            f"{CODING_PLAN_ENDPOINT}/chat/completions",
            headers=headers,
            json=data,
            timeout=5
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ 成功! 响应: {content}")
            print(f"🎯 使用这个模型: {model}")
            break
        else:
            error = response.json().get("error", {}).get("message", response.text[:100])
            print(f"错误: {error}")
            
    except Exception as e:
        print(f"异常: {e}")
