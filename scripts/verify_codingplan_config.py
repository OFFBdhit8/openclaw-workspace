#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 Coding Plan Lite 配置
"""

import json
from pathlib import Path

def check_configuration():
    """检查配置"""
    print("🔍 验证 Coding Plan Lite 配置")
    print("="*60)
    
    checks_passed = 0
    total_checks = 4
    
    # 检查 1: models.json 配置
    print("\n1. 检查 models.json 配置...")
    models_file = Path("/root/.openclaw/agents/main/agent/models.json")
    
    if models_file.exists():
        try:
            with open(models_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "codingplan" in data.get("providers", {}):
                codingplan = data["providers"]["codingplan"]
                endpoint = codingplan.get("baseUrl", "")
                api_key = codingplan.get("apiKey", "")
                models = codingplan.get("models", [])
                
                print(f"   ✅ codingplan 配置存在")
                print(f"      端点: {endpoint}")
                print(f"      Key: {api_key[:10]}...")
                print(f"      模型数: {len(models)}")
                
                checks_passed += 1
            else:
                print("   ❌ codingplan 配置不存在")
        except Exception as e:
            print(f"   ❌ 读取失败: {e}")
    else:
        print("   ❌ models.json 不存在")
    
    # 检查 2: 配置文件
    print("\n2. 检查配置文件...")
    config_file = Path("/root/.openclaw/config/codingplan.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if "codingplan" in config:
                print(f"   ✅ 配置文件存在")
                print(f"      默认模型: {config['codingplan'].get('default_model', '未知')}")
                print(f"      模型列表: {', '.join(config['codingplan'].get('available_models', []))}")
                
                checks_passed += 1
            else:
                print("   ❌ 配置格式错误")
        except Exception as e:
            print(f"   ❌ 读取失败: {e}")
    else:
        print("   ❌ 配置文件不存在")
    
    # 检查 3: API Key 记录
    print("\n3. 检查 API Key 记录...")
    api_keys_file = Path("/root/.openclaw/workspace/secrets/api_keys.md")
    
    if api_keys_file.exists():
        try:
            with open(api_keys_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "coding.dashscope.aliyuncs.com" in content:
                print("   ✅ API Key 记录已更新")
                checks_passed += 1
            else:
                print("   ❌ API Key 记录未更新")
        except Exception as e:
            print(f"   ❌ 读取失败: {e}")
    else:
        print("   ❌ API Key 文件不存在")
    
    # 检查 4: 记忆文件
    print("\n4. 检查记忆文件...")
    memory_file = Path("/root/.openclaw/workspace/memory/2026-02-25.md")
    
    if memory_file.exists():
        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "Coding Plan Lite 成功配置" in content:
                print("   ✅ 记忆文件已更新")
                checks_passed += 1
            else:
                print("   ❌ 记忆文件未更新")
        except Exception as e:
            print(f"   ❌ 读取失败: {e}")
    else:
        print("   ❌ 记忆文件不存在")
    
    # 总结
    print("\n" + "="*60)
    print("📊 配置验证结果:")
    print(f"   通过检查: {checks_passed}/{total_checks}")
    
    if checks_passed == total_checks:
        print("   🎉 所有配置检查通过!")
    elif checks_passed >= 3:
        print("   ✅ 主要配置完成")
    else:
        print("   ⚠️  配置不完整")
    
    print("\n🔧 使用命令:")
    print("   查看模型: openclaw models list | grep codingplan")
    print("   切换模型: openclaw models use codingplan/qwen-plus")
    print("   测试连接: 稍后实际使用测试")
    print("="*60)

if __name__ == "__main__":
    check_configuration()
