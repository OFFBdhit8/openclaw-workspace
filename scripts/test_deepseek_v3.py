#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 DeepSeek V3.2 API
"""

import requests
import json

DEEPSEEK_API_KEY = "sk-7c004758529f45c6ac42ec3e620c088d"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

def test_deepseek_model(model_name: str):
    """测试 DeepSeek 模型"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": "你好，请简单介绍一下你自己。"}
        ],
        "max_tokens": 100,
        "stream": False
    }
    
    try:
        print(f"🔍 测试模型: {model_name}")
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 模型 {model_name} 可用!")
            print(f"   响应: {result.get('choices', [{}])[0].get('message', {}).get('content', '')[:50]}...")
            return True
        else:
            print(f"❌ 模型 {model_name} 不可用: HTTP {response.status_code}")
            print(f"   错误: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def main():
    print("🧪 测试 DeepSeek 模型可用性")
    print("="*60)
    
    # 测试已知可用的模型
    test_deepseek_model("deepseek-chat")
    
    print()
    
    # 测试可能的 V3.2 模型名称
    possible_v3_2_models = [
        "deepseek-v3.2",
        "deepseek-v3.2-chat",
        "deepseek-v3.2-2026",
        "deepseek-v3.2-latest",
        "deepseek-v3",
        "deepseek-v3-chat"
    ]
    
    print("🔍 尝试可能的 V3.2 模型名称:")
    available_models = []
    
    for model in possible_v3_2_models:
        if test_deepseek_model(model):
            available_models.append(model)
        print()
    
    if available_models:
        print("🎉 可用的 V3.2 模型:")
        for model in available_models:
            print(f"  ✅ {model}")
    else:
        print("⚠️  未找到可用的 V3.2 模型")
        print("💡 建议:")
        print("  1. 检查 DeepSeek 官方文档")
        print("  2. 确认模型名称是否正确")
        print("  3. 联系 DeepSeek 支持")

if __name__ == "__main__":
    main()
