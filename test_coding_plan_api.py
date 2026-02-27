#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Coding Plan Lite API 连接性
使用实际的配置端点
"""

import requests
import json
import sys

def test_coding_plan_api():
    """测试 Coding Plan Lite API"""
    print("🔍 测试 Coding Plan Lite API 连接性...")
    
    # 从 models.json 中提取的配置
    api_key = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
    base_url = "https://coding.dashscope.aliyuncs.com/v1"
    
    # 尝试聊天补全端点
    chat_endpoint = f"{base_url}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 尝试不同的模型
    models_to_test = [
        "qwen2.5-coder-7b-instruct",
        "qwen2.5-coder-14b-instruct",
        "codeqwen1.5-7b-chat"
    ]
    
    test_data = {
        "model": "qwen2.5-coder-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, please say 'API test successful' if you can read this."}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    for model in models_to_test:
        print(f"\n🧪 测试模型: {model}")
        test_data["model"] = model
        
        try:
            response = requests.post(
                chat_endpoint,
                headers=headers,
                json=test_data,
                timeout=15
            )
            
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"  ✅ 成功! 响应: {content}")
                
                # 检查响应结构
                print(f"  响应结构: {list(result.keys())}")
                if 'usage' in result:
                    usage = result['usage']
                    print(f"  📊 Token 使用: {usage}")
                    
                return True, model
                
            else:
                print(f"  ❌ 错误: {response.status_code}")
                print(f"  响应: {response.text[:200]}")
                
        except Exception as e:
            print(f"  ❌ 请求异常: {e}")
    
    # 也尝试 /completions 端点（如果 /chat/completions 不行）
    print("\n🔄 尝试 /completions 端点...")
    completions_endpoint = f"{base_url}/completions"
    
    alt_test_data = {
        "model": "qwen2.5-coder-7b-instruct",
        "prompt": "Hello, please say 'API test successful' if you can read this.",
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            completions_endpoint,
            headers=headers,
            json=alt_test_data,
            timeout=15
        )
        
        print(f"  状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ /completions 端点成功!")
            print(f"  响应: {result}")
            return True, "via /completions"
        else:
            print(f"  ❌ /completions 失败: {response.status_code}")
            print(f"  响应: {response.text[:200]}")
    except Exception as e:
        print(f"  ❌ /completions 请求异常: {e}")
    
    return False, None

def check_api_endpoint():
    """检查 API 端点基本信息"""
    print("\n🔗 检查 API 端点连接性...")
    
    base_url = "https://coding.dashscope.aliyuncs.com/v1"
    
    # 简单检查端点是否可达
    try:
        response = requests.get(base_url, timeout=10)
        print(f"  GET {base_url} → 状态码: {response.status_code}")
        print(f"  响应头: {dict(response.headers)}")
    except Exception as e:
        print(f"  ❌ 端点不可达: {e}")
    
    # 检查 /models 端点（如果支持）
    models_endpoint = f"{base_url}/models"
    print(f"\n📋 尝试获取模型列表: {models_endpoint}")
    
    api_key = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(models_endpoint, headers=headers, timeout=10)
        print(f"  状态码: {response.status_code}")
        if response.status_code == 200:
            models = response.json()
            print(f"  ✅ 获取到模型列表!")
            print(f"  模型数量: {len(models.get('data', []))}")
            for model in models.get('data', [])[:3]:
                print(f"    - {model.get('id', 'N/A')}")
        else:
            print(f"  响应: {response.text[:200]}")
    except Exception as e:
        print(f"  ❌ 获取模型列表失败: {e}")

def main():
    print("="*70)
    print("🧪 Coding Plan Lite API 连接性测试")
    print("="*70)
    
    # 检查 API 端点
    check_api_endpoint()
    
    # 测试 API 功能
    print("\n" + "="*70)
    print("🚀 测试 API 功能...")
    success, model = test_coding_plan_api()
    
    print("\n" + "="*70)
    print("📋 测试结果总结:")
    
    if success:
        print(f"✅ Coding Plan Lite API 连接成功!")
        print(f"   工作模型: {model}")
        print(f"   API 端点: https://coding.dashscope.aliyuncs.com/v1")
        print("\n💡 建议:")
        print("   - API 密钥有效，可以正常使用")
        print("   - 模型配置在 models.json 中正确")
    else:
        print("❌ Coding Plan Lite API 连接失败")
        print("\n💡 可能的原因:")
        print("   1. API 密钥已过期或无效")
        print("   2. API 端点不正确")
        print("   3. 服务暂时不可用")
        print("   4. 网络连接问题")
        print("\n🔧 下一步:")
        print("   1. 检查 API 密钥是否正确")
        print("   2. 验证 API 端点 URL")
        print("   3. 联系服务提供商确认服务状态")
    
    print("="*70)

if __name__ == "__main__":
    main()