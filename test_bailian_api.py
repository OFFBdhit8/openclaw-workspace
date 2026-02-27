#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试阿里云百炼平台 API 端点
"""

import requests
import json

def test_bailian_api():
    """测试百炼平台 API"""
    api_key = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
    
    # 可能的百炼平台端点
    endpoints = [
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "https://dashscope.aliyuncs.com/api/v1/chat/completions",
        "https://bailian.aliyuncs.com/api/v1/chat/completions",
    ]
    
    # 测试 qwen3.5-plus 模型
    test_data = {
        "model": "qwen3.5-plus",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, say 'API test successful' if you can read this."}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    print("="*70)
    print("🧪 测试阿里云百炼平台 API 端点")
    print("="*70)
    
    working_endpoint = None
    
    for endpoint in endpoints:
        print(f"\n🌐 测试: {endpoint}")
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=test_data,
                timeout=15
            )
            
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"   ✅ 成功!")
                print(f"   响应: {content}")
                working_endpoint = endpoint
                
                # 显示 token 使用情况
                if "usage" in result:
                    usage = result["usage"]
                    print(f"   Token使用: {usage}")
                    
                break
            else:
                print(f"   ❌ 失败: {response.status_code}")
                error_text = response.text[:200]
                print(f"   错误: {error_text}")
                
        except Exception as e:
            print(f"   ❌ 异常: {e}")
    
    print("\n" + "="*70)
    if working_endpoint:
        print("📋 测试结果: 找到可用端点")
        print(f"   ✅ 工作端点: {working_endpoint}")
        print(f"   ✅ 模型: qwen3.5-plus")
        print(f"   ✅ API Key: 有效")
    else:
        print("📋 测试结果: 未找到可用端点")
        print("\n💡 建议:")
        print("   1. 检查 API Key 是否正确")
        print("   2. 确认是否有该模型的调用权限")
        print("   3. 检查阿里云账户状态")
    
    print("="*70)
    return working_endpoint

if __name__ == "__main__":
    test_bailian_api()
