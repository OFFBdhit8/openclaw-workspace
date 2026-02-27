#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Discord Token 有效性
"""

import requests
import json
import base64

# 用户提供的 Token
TOKEN = "YOUR_DISCORD_BOT_TOKEN"

def decode_token_parts(token):
    """解码 Token 的各个部分"""
    print("=" * 60)
    print("🔍 分析 Token 结构")
    print("=" * 60)
    
    parts = token.split('.')
    print(f"分割为 {len(parts)} 部分:")
    for i, part in enumerate(parts):
        print(f"  第{i+1}部分: {part}")
    
    # 尝试解码第一部分（可能是 Bot ID）
    if len(parts) > 0:
        try:
            # Bot ID 通常是 Base64 编码
            decoded = base64.b64decode(parts[0] + '=' * (-len(parts[0]) % 4))
            print(f"\n🔐 第一部分解码结果: {decoded}")
        except:
            print(f"\n🔐 第一部分无法解码")
    
    return parts

def test_token(token):
    """测试 Token 有效性"""
    print("\n" + "=" * 60)
    print("🧪 测试 Token 有效性")
    print("=" * 60)
    
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    # 测试多个端点
    endpoints = [
        ("/users/@me", "获取当前用户信息"),
        ("/gateway", "获取网关信息"),
        ("/applications/@me", "获取应用信息"),
    ]
    
    results = {}
    
    for endpoint, description in endpoints:
        try:
            print(f"\n📡 测试: {description}")
            print(f"  端点: {endpoint}")
            
            response = requests.get(
                f"https://discord.com/api/v10{endpoint}",
                headers=headers,
                timeout=10
            )
            
            print(f"  状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                results[endpoint] = {"success": True, "data": data}
                
                if endpoint == "/users/@me":
                    print(f"  ✅ 认证成功！")
                    print(f"    用户名: {data.get('username', 'N/A')}")
                    print(f"    ID: {data.get('id', 'N/A')}")
                    print(f"    是否为 Bot: {data.get('bot', False)}")
                    print(f"    全局名称: {data.get('global_name', 'N/A')}")
                    print(f"    Discriminator: {data.get('discriminator', 'N/A')}")
                    
                    # 检查是否是 Bot
                    is_bot = data.get('bot', False)
                    if is_bot:
                        print(f"  🤖 这是一个 Bot 账号！")
                    else:
                        print(f"  👤 这是一个用户账号！")
                
                elif endpoint == "/applications/@me":
                    print(f"  📱 应用信息:")
                    print(f"    应用名称: {data.get('name', 'N/A')}")
                    print(f"    应用 ID: {data.get('id', 'N/A')}")
                    print(f"    描述: {data.get('description', 'N/A')}")
            
            else:
                results[endpoint] = {"success": False, "status": response.status_code}
                print(f"  ❌ 失败: {response.text[:200]}")
                
        except requests.exceptions.Timeout:
            print(f"  ⏱️  超时")
            results[endpoint] = {"success": False, "error": "timeout"}
        except Exception as e:
            print(f"  💥 异常: {e}")
            results[endpoint] = {"success": False, "error": str(e)}
    
    return results

def check_bot_status(user_id):
    """检查 Bot 状态"""
    print("\n" + "=" * 60)
    print("🤖 检查 Bot 状态")
    print("=" * 60)
    
    # 通过用户 ID 检查
    headers = {"Authorization": f"Bot {TOKEN}"}
    
    try:
        response = requests.get(
            f"https://discord.com/api/v10/users/{user_id}",
            headers=headers,
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 找到用户:")
            print(f"  用户名: {data.get('username', 'N/A')}")
            print(f"  ID: {data.get('id', 'N/A')}")
            print(f"  是否为 Bot: {data.get('bot', False)}")
        else:
            print(f"❌ 无法找到用户: {response.text[:200]}")
    except Exception as e:
        print(f"💥 异常: {e}")

def main():
    """主函数"""
    print("🚀 Discord Token 验证工具")
    print("=" * 60)
    
    # 解码 Token
    parts = decode_token_parts(TOKEN)
    
    # 测试 Token
    results = test_token(TOKEN)
    
    # 如果用普通方式失败，尝试 Bot 前缀
    if "/users/@me" in results and not results["/users/@me"]["success"]:
        print("\n" + "=" * 60)
        print("🔄 尝试使用 Bot 前缀")
        print("=" * 60)
        
        bot_token = f"Bot {TOKEN}"
        print(f"Token 格式: {bot_token[:50]}...")
        
        headers = {"Authorization": bot_token}
        try:
            response = requests.get(
                "https://discord.com/api/v10/users/@me",
                headers=headers,
                timeout=10
            )
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 使用 Bot 前缀成功！")
                print(f"  用户名: {data.get('username', 'N/A')}")
                print(f"  是否为 Bot: {data.get('bot', False)}")
            else:
                print(f"❌ 失败: {response.text[:200]}")
        except Exception as e:
            print(f"💥 异常: {e}")
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    if "/users/@me" in results and results["/users/@me"]["success"]:
        user_data = results["/users/@me"]["data"]
        is_bot = user_data.get('bot', False)
        
        if is_bot:
            print("✅ 这是一个有效的 Bot Token！")
            print("🎉 可以用于创建 Auberon 机器人")
        else:
            print("⚠️ 这是一个有效的用户 Token，但不是 Bot Token")
            print("❌ 无法用于创建机器人（Discord 禁止用户 Token 自动化）")
    else:
        print("❌ Token 无效或认证失败")
        print("💡 可能原因:")
        print("   1. Token 已过期/被撤销")
        print("   2. 这是用户 Token（Discord 已禁用）")
        print("   3. Token 格式不正确")
        
        print("\n🔧 解决方案:")
        print("   请创建真正的 Discord Bot:")
        print("   1. 访问 https://discord.com/developers/applications")
        print("   2. 创建 New Application → 添加 Bot")
        print("   3. 复制 Bot Token（以 M 开头）")

if __name__ == "__main__":
    main()
