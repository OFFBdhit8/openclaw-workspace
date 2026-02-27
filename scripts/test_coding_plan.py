#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Coding Plan Lite API Key
"""

import requests
import json

CODING_PLAN_API_KEY = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
# 假设 Coding Plan 使用 OpenAI 兼容的 API
TEST_URL = "https://api.openai.com/v1/chat/completions"

def test_coding_plan_key():
    """测试 Coding Plan Lite API Key"""
    print("🔍 测试 Coding Plan Lite API Key...")
    
    headers = {
        "Authorization": f"Bearer {CODING_PLAN_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # 尝试不同的可能端点
    endpoints = [
        "https://api.openai.com/v1/chat/completions",
        "https://api.deepseek.com/v1/chat/completions",
        "https://api.moonshot.cn/v1/chat/completions",
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    ]
    
    test_data = {
        "model": "gpt-3.5-turbo",  # 通用模型名称
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, please say 'API test successful' if you can read this."}
        ],
        "max_tokens": 50
    }
    
    for endpoint in endpoints:
        print(f"\n🌐 测试端点: {endpoint}")
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=test_data,
                timeout=10
            )
            
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"  ✅ 成功! 响应: {content}")
                return endpoint
            elif response.status_code == 401:
                print("  ❌ 认证失败 (401)")
            elif response.status_code == 404:
                print("  ❌ 端点不存在 (404)")
            else:
                print(f"  ⚠️  其他错误: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")
    
    return None

def check_key_format():
    """检查 Key 格式"""
    print("\n🔑 分析 API Key 格式...")
    key = CODING_PLAN_API_KEY
    
    print(f"  Key 长度: {len(key)} 字符")
    print(f"  Key 前缀: {key[:10]}...")
    
    # 常见 API Key 前缀模式
    patterns = {
        "sk-sp-": "可能是特殊服务或自定义部署",
        "sk-": "标准 OpenAI 格式",
        "sk-api-": "Minimax 格式",
        "sk-7c0": "DeepSeek 格式",
        "sk-AeUl": "Kimi 格式",
        "sk-46ecd": "Qwen 格式",
        "sk-qv0tlt": "腾讯混元格式"
    }
    
    for prefix, description in patterns.items():
        if key.startswith(prefix):
            print(f"  📍 匹配模式: {prefix} → {description}")
            return prefix
    
    print("  ⚠️  未识别到常见前缀模式")
    return None

def main():
    print("="*60)
    print("🧪 Coding Plan Lite API Key 测试")
    print("="*60)
    
    # 检查 Key 格式
    prefix = check_key_format()
    
    # 测试 API 连接
    working_endpoint = test_coding_plan_key()
    
    print("\n" + "="*60)
    print("📋 测试结果总结:")
    
    if working_endpoint:
        print(f"✅ API Key 有效!")
        print(f"   工作端点: {working_endpoint}")
        print(f"   Key 前缀: {prefix or '未知'}")
        
        # 根据前缀猜测服务商
        if prefix == "sk-sp-":
            print("   🎯 猜测: Coding Plan Lite (特殊服务)")
            print("   💡 建议: 需要确认具体 API 端点")
        elif prefix == "sk-7c0":
            print("   🎯 猜测: DeepSeek")
        elif prefix == "sk-AeUl":
            print("   🎯 猜测: Kimi (Moonshot)")
        else:
            print("   🎯 猜测: OpenAI 兼容服务")
            
    else:
        print("❌ 未找到可用的 API 端点")
        print("💡 建议:")
        print("   1. 确认 API Key 是否正确")
        print("   2. 确认服务是否可用")
        print("   3. 获取正确的 API 端点 URL")
    
    print("="*60)

if __name__ == "__main__":
    main()
