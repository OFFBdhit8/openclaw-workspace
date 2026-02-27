#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 coding.dashscope.aliyuncs.com 端点
"""

import requests
import json

def test_coding_endpoint():
    """测试 coding.dashscope 端点"""
    api_key = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
    base_url = "https://coding.dashscope.aliyuncs.com/v1"
    
    # 测试多个可能的路径
    paths = [
        "/chat/completions",
        "/completions",
        "/models",
        "/services/aigc/text-generation/generation",
        "/api/v1/chat/completions",
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("="*70)
    print(f"🧪 测试端点: {base_url}")
    print("="*70)
    
    # 先测试基础连接
    print("\n🔗 测试基础连接...")
    try:
        response = requests.get(base_url, timeout=10)
        print(f"   GET {base_url} → {response.status_code}")
        if response.status_code == 200:
            print(f"   响应: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
    
    # 测试各个路径
    print("\n📡 测试 API 路径...")
    for path in paths:
        endpoint = f"{base_url}{path}"
        print(f"\n🌐 {endpoint}")
        
        # 尝试 POST 请求（聊天补全）
        if "chat" in path or "generation" in path:
            if "generation" in path:
                # 旧版格式
                test_data = {
                    "model": "qwen2.5-coder-7b-instruct",
                    "input": {
                        "messages": [
                            {"role": "user", "content": "Hello"}
                        ]
                    },
                    "parameters": {
                        "max_tokens": 10
                    }
                }
            else:
                # OpenAI 兼容格式
                test_data = {
                    "model": "qwen2.5-coder-7b-instruct",
                    "messages": [
                        {"role": "system", "content": "You are helpful."},
                        {"role": "user", "content": "Hello, say 'test ok'"}
                    ],
                    "max_tokens": 10
                }
            
            try:
                response = requests.post(endpoint, headers=headers, json=test_data, timeout=10)
                print(f"   POST → {response.status_code}")
                if response.status_code == 200:
                    print(f"   ✅ 成功!")
                    print(f"   响应: {response.text[:200]}")
                else:
                    print(f"   响应: {response.text[:150]}")
            except Exception as e:
                print(f"   ❌ 错误: {e}")
        else:
            # GET 请求（如 /models）
            try:
                response = requests.get(endpoint, headers=headers, timeout=10)
                print(f"   GET → {response.status_code}")
                if response.status_code == 200:
                    print(f"   响应: {response.text[:200]}")
                else:
                    print(f"   响应: {response.text[:150]}")
            except Exception as e:
                print(f"   ❌ 错误: {e}")
    
    print("\n" + "="*70)
    print("📋 测试完成")
    print("="*70)

if __name__ == "__main__":
    test_coding_endpoint()
