#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速找到 Coding Plan Lite 的正确模型名称
"""

import requests
import json

CODING_PLAN_KEY = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
CODING_PLAN_ENDPOINT = "https://coding.dashscope.aliyuncs.com/v1"

print("🔍 寻找 Coding Plan Lite 正确模型名称")
print("="*60)

# 根据阿里云文档，Coding Plan 可能有特定的模型名称
# 尝试常见的阿里云模型命名模式
possible_models = [
    # Coding Plan 专用模型
    "codingplan-lite",
    "codingplan-pro",
    "codingplan",
    "code-plan",
    "code-plan-lite",
    
    # 阿里云通用模型
    "qwen2.5-coder-7b-instruct",
    "qwen2.5-coder-14b-instruct", 
    "qwen2.5-coder-32b-instruct",
    "qwen2.5-coder-7b",
    "qwen2.5-coder-14b",
    "qwen2.5-coder-32b",
    
    # 其他可能
    "codeqwen1.5-7b-chat",
    "codeqwen1.5-7b",
    "code-llama",
    "codellama",
    
    # 简单测试
    "test",
    "default"
]

chat_url = f"{CODING_PLAN_ENDPOINT}/chat/completions"
headers = {
    "Authorization": f"Bearer {CODING_PLAN_KEY}",
    "Content-Type": "application/json"
}

test_data = {
    "model": "",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say 'hello' if you can read this."}
    ],
    "max_tokens": 10,
    "temperature": 0.1
}

working_models = []

for model in possible_models:
    print(f"🤖 测试: {model:30}", end="")
    
    test_data["model"] = model
    
    try:
        response = requests.post(chat_url, headers=headers, json=test_data, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f" ✅ 成功! -> {content[:20]}")
            working_models.append(model)
        elif response.status_code == 400:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "")
            if "not supported" in error_msg or "not exist" in error_msg:
                print(" ❌ 不支持")
            else:
                print(f" ⚠️  其他400: {error_msg[:30]}")
        else:
            print(f" ❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f" ❌ 异常: {e}")

print("\n" + "="*60)
print("📋 测试结果:")

if working_models:
    print(f"✅ 找到 {len(working_models)} 个可用模型:")
    for i, model in enumerate(working_models, 1):
        print(f"   {i}. {model}")
    
    # 测试第一个可用模型的完整能力
    print(f"\n🧪 详细测试模型: {working_models[0]}")
    
    test_data["model"] = working_models[0]
    test_data["messages"] = [
        {"role": "system", "content": "You are Coding Plan Lite assistant."},
        {"role": "user", "content": "Write a Python function to calculate fibonacci sequence."}
    ]
    test_data["max_tokens"] = 200
    
    try:
        response = requests.post(chat_url, headers=headers, json=test_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"📝 代码生成测试:")
            print(content[:150] + "..." if len(content) > 150 else content)
            
            # 显示 token 使用
            usage = data.get("usage", {})
            print(f"📊 Token使用: 输入{usage.get('prompt_tokens', 0)} / 输出{usage.get('completion_tokens', 0)}")
    except Exception as e:
        print(f"❌ 详细测试失败: {e}")
        
else:
    print("❌ 未找到可用模型")
    print("\n💡 建议:")
    print("  1. 查看阿里云文档确认模型名称")
    print("  2. 联系阿里云技术支持")
    print("  3. 检查服务权限和配额")

print("="*60)
