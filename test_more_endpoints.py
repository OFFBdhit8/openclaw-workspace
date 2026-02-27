#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试更多阿里云百炼平台端点
"""

import requests
import json

def test_more_endpoints():
    """测试更多可能的端点"""
    api_key = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
    
    # 更多可能的端点
    endpoints = [
        # 标准兼容模式
        ("https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen3.5-plus"),
        # 尝试其他模型名称格式
        ("https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen-plus"),
        ("https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen-turbo"),
        ("https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "qwen-max"),
        # 尝试旧版API路径
        ("https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation", "qwen3.5-plus"),
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("="*70)
    print("🧪 测试不同端点和模型组合")
    print("="*70)
    
    for endpoint, model in endpoints:
        print(f"\n🌐 端点: {endpoint}")
        print(f"   模型: {model}")
        
        if "text-generation/generation" in endpoint:
            # 旧版API格式
            test_data = {
                "model": model,
                "input": {
                    "messages": [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Hello, say 'API test successful' if you can read this."}
                    ]
                },
                "parameters": {
                    "max_tokens": 50,
                    "temperature": 0.7
                }
            }
        else:
            # OpenAI兼容格式
            test_data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello, say 'API test successful' if you can read this."}
                ],
                "max_tokens": 50,
                "temperature": 0.7
            }
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=test_data,
                timeout=10
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ 成功!")
                print(f"   响应: {result}")
                return endpoint, model
            elif response.status_code == 401:
                print(f"   ❌ 401 - API Key 无效")
            elif response.status_code == 400:
                error = response.json().get("error", {}).get("message", "")
                print(f"   ⚠️ 400 - {error}")
            else:
                print(f"   ❌ {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ 异常: {e}")
    
    print("\n" + "="*70)
    print("💡 结论: API Key 可能不是标准 dashscope key")
    print("   建议: 从阿里云百炼控制台获取正确的 API 调用示例")
    print("="*70)
    return None, None

if __name__ == "__main__":
    test_more_endpoints()
