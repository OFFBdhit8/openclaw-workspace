#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取 DeepSeek 可用模型列表
"""

import requests
import json

DEEPSEEK_API_KEY = "sk-7c004758529f45c6ac42ec3e620c088d"
DEEPSEEK_MODELS_URL = "https://api.deepseek.com/v1/models"

def get_deepseek_models():
    """获取 DeepSeek 模型列表"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 获取 DeepSeek 模型列表...")
        response = requests.get(DEEPSEEK_MODELS_URL, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get("data", [])
            
            print(f"✅ 找到 {len(models)} 个模型:")
            print("="*60)
            
            for model in models:
                model_id = model.get("id", "未知")
                created = model.get("created", 0)
                # 转换时间戳
                from datetime import datetime
                if created:
                    created_str = datetime.fromtimestamp(created).strftime("%Y-%m-%d")
                else:
                    created_str = "未知"
                
                print(f"🆔 {model_id}")
                print(f"  创建时间: {created_str}")
                print(f"  对象类型: {model.get('object', '未知')}")
                print(f"  所属组织: {model.get('owned_by', '未知')}")
                print("-"*40)
            
            return models
        else:
            print(f"❌ 获取失败: HTTP {response.status_code}")
            print(f"错误: {response.text[:200]}")
            return []
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return []

def main():
    print("🧪 获取 DeepSeek 可用模型")
    print("="*60)
    
    models = get_deepseek_models()
    
    if models:
        print("\n📊 模型统计:")
        print(f"  总模型数: {len(models)}")
        
        # 按组织统计
        org_count = {}
        for model in models:
            org = model.get("owned_by", "未知")
            org_count[org] = org_count.get(org, 0) + 1
        
        print("\n🏢 按组织分布:")
        for org, count in org_count.items():
            print(f"  {org}: {count} 个模型")
        
        # 查找可能的 V3.2 模型
        print("\n🔍 查找包含 'v3' 或 '3.2' 的模型:")
        v3_models = []
        for model in models:
            model_id = model.get("id", "").lower()
            if "v3" in model_id or "3.2" in model_id:
                v3_models.append(model)
        
        if v3_models:
            print(f"✅ 找到 {len(v3_models)} 个 V3 相关模型:")
            for model in v3_models:
                print(f"  🆔 {model.get('id')}")
        else:
            print("⚠️  未找到 V3 相关模型")
    
    print("\n" + "="*60)
    print("💡 结论:")
    print("  如果未找到 deepseek-v3.2，可能是:")
    print("  1. 模型尚未公开")
    print("  2. 需要特定权限访问")
    print("  3. 模型名称不同")
    print("  建议使用当前可用的 deepseek-chat 或 deepseek-reasoner")

if __name__ == "__main__":
    main()
