#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Coding Plan Lite 阿里云端点
"""

import requests
import json

CODING_PLAN_KEY = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"
CODING_PLAN_ENDPOINT = "https://coding.dashscope.aliyuncs.com/v1"

def test_coding_plan():
    """测试 Coding Plan Lite 端点"""
    print("🔍 测试 Coding Plan Lite 阿里云端点...")
    print(f"🌐 端点: {CODING_PLAN_ENDPOINT}")
    print(f"🔑 Key: {CODING_PLAN_KEY[:10]}...")
    
    chat_url = f"{CODING_PLAN_ENDPOINT}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {CODING_PLAN_KEY}",
        "Content-Type": "application/json"
    }
    
    # 尝试不同的模型名称
    possible_models = [
        "codingplan-lite",  # 最可能的名称
        "qwen-coder",       # 代码模型
        "qwen-plus",        # 通用模型
        "qwen-turbo",       # 快速模型
        "gpt-3.5-turbo",    # OpenAI 兼容名称
        "deepseek-coder"    # 其他可能
    ]
    
    test_data_template = {
        "model": "",
        "messages": [
            {"role": "system", "content": "You are Coding Plan Lite assistant."},
            {"role": "user", "content": "Hello, please respond with 'Coding Plan Lite is working!'"}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    working_models = []
    
    for model in possible_models:
        print(f"\n🤖 测试模型: {model}")
        
        test_data = test_data_template.copy()
        test_data["model"] = model
        
        try:
            response = requests.post(
                chat_url,
                headers=headers,
                json=test_data,
                timeout=15
            )
            
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                print(f"  ✅ 成功! 响应: {content[:50]}...")
                working_models.append({
                    "model": model,
                    "content": content
                })
            elif response.status_code == 400:
                error_data = response.json()
                error_msg = error_data.get("error", {}).get("message", response.text[:100])
                print(f"  ❌ 模型不存在: {error_msg}")
            elif response.status_code == 401:
                print("  ❌ 认证失败 (401)")
            else:
                print(f"  ⚠️  其他错误: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")
    
    return working_models

def get_available_models():
    """获取可用模型列表"""
    print("\n🔍 获取可用模型列表...")
    
    models_url = f"{CODING_PLAN_ENDPOINT}/models"
    headers = {
        "Authorization": f"Bearer {CODING_PLAN_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(models_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("data", [])
            
            print(f"✅ 找到 {len(models)} 个模型:")
            for model in models:
                model_id = model.get("id", "未知")
                print(f"  🆔 {model_id}")
            
            return models
        else:
            print(f"❌ 获取失败: HTTP {response.status_code}")
            print(f"错误: {response.text[:200]}")
            return []
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return []

def main():
    print("="*60)
    print("🧪 Coding Plan Lite 阿里云端点测试")
    print("="*60)
    
    # 测试聊天端点
    working_models = test_coding_plan()
    
    # 尝试获取模型列表
    available_models = get_available_models()
    
    print("\n" + "="*60)
    print("📋 测试结果总结:")
    
    if working_models:
        print(f"✅ 端点连接成功!")
        print(f"   可用模型: {len(working_models)} 个")
        for wm in working_models:
            print(f"   🤖 {wm['model']}: {wm['content'][:30]}...")
    else:
        print("❌ 未找到可用的模型名称")
    
    if available_models:
        print(f"\n📊 服务提供的模型: {len(available_models)} 个")
        # 显示前5个
        for i, model in enumerate(available_models[:5], 1):
            model_id = model.get("id", "未知")
            print(f"   {i}. {model_id}")
    
    print("\n💡 建议:")
    if working_models:
        print("   使用第一个成功的模型进行配置")
    else:
        print("   1. 检查文档确认正确的模型名称")
        print("   2. 确认服务权限和配额")
        print("   3. 联系阿里云技术支持")
    
    print("="*60)

if __name__ == "__main__":
    main()
