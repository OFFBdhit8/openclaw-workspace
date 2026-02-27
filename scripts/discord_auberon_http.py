#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord 机器人 - Auberon（使用 HTTP API 直接调用）
角色：工作室第一位员工，专业高冷，统筹一切
"""

import requests
import json
import time
import os
import sys

# ============ 配置区域 ============
# 你提供的 Token（用户 Token 或 Bot Token）
DISCORD_TOKEN = "G_uCTy.v7CO9DLbD1bCYWzDj7nue36EIs1329q39z7gDM"

# 服务器和频道 ID
GUILD_ID = YOUR_GUILD_ID  # 服务器 ID
CHANNEL_ID = YOUR_DISCORD_CHANNEL_ID  # 频道 ID

# Auberon 的角色设定
BOT_NAME = "Auberon"
BOT_DESCRIPTION = "工作室第一位员工，专业高冷，统筹一切"

# Discord API 基础 URL
BASE_URL = "https://discord.com/api/v10"

# 请求头
HEADERS = {
    "Authorization": DISCORD_TOKEN,
    "Content-Type": "application/json"
}

# =================================

def test_connection():
    """测试 Discord 连接"""
    print("=" * 50)
    print(f"🚀 正在启动 {BOT_NAME}...")
    print(f"📝 角色设定: {BOT_DESCRIPTION}")
    print("=" * 50)
    
    # 测试获取当前用户信息
    print("\n📡 测试连接 Discord API...")
    response = requests.get(f"{BASE_URL}/users/@me", headers=HEADERS)
    
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ 连接成功！")
        print(f"   🤖 机器人名称: {user_data.get('username', 'Unknown')}")
        print(f"   🆔 用户 ID: {user_data.get('id', 'Unknown')}")
        print(f"   📝 全局名称: {user_data.get('global_name', 'N/A')}")
        return True
    elif response.status_code == 401:
        print("❌ 认证失败！Token 无效或已过期")
        print("   - 如果是用户 Token，可能已失效")
        print("   - 如果是 Bot Token，请确认 Token 正确")
        return False
    else:
        print(f"❌ 连接失败！状态码: {response.status_code}")
        print(f"   错误信息: {response.text[:200]}")
        return False

def get_channel_info():
    """获取频道信息"""
    print(f"\n📺 获取频道信息 (ID: {CHANNEL_ID})...")
    response = requests.get(f"{BASE_URL}/channels/{CHANNEL_ID}", headers=HEADERS)
    
    if response.status_code == 200:
        channel_data = response.json()
        print(f"   ✅ 频道名称: {channel_data.get('name', 'Unknown')}")
        print(f"   🆔 频道 ID: {channel_data.get('id')}")
        print(f"   📂 频道类型: {channel_data.get('type')}")
        return True
    else:
        print(f"   ❌ 获取频道失败: {response.status_code}")
        print(f"   错误信息: {response.text[:200]}")
        return False

def send_message(content):
    """发送消息到指定频道"""
    print(f"\n📤 发送消息到频道 {CHANNEL_ID}...")
    print(f"   内容: {content[:50]}...")
    
    data = {
        "content": content,
        "tts": False
    }
    
    response = requests.post(
        f"{BASE_URL}/channels/{CHANNEL_ID}/messages",
        headers=HEADERS,
        json=data
    )
    
    if response.status_code == 200:
        msg_data = response.json()
        print(f"   ✅ 消息发送成功！")
        print(f"   🆔 消息 ID: {msg_data.get('id')}")
        return True
    elif response.status_code == 403:
        print(f"   ❌ 权限不足，无法在该频道发送消息")
        print(f"   错误信息: {response.text[:200]}")
        return False
    elif response.status_code == 404:
        print(f"   ❌ 频道不存在或机器人不在该服务器中")
        print(f"   错误信息: {response.text[:200]}")
        return False
    else:
        print(f"   ❌ 发送失败: {response.status_code}")
        print(f"   错误信息: {response.text[:200]}")
        return False

def get_guild_info():
    """获取服务器信息"""
    print(f"\n🏠 获取服务器信息 (ID: {GUILD_ID})...")
    
    # 注意：需要先获取服务器成员或频道信息才能确认机器人在服务器中
    response = requests.get(f"{BASE_URL}/guilds/{GUILD_ID}", headers=HEADERS)
    
    if response.status_code == 200:
        guild_data = response.json()
        print(f"   ✅ 服务器名称: {guild_data.get('name', 'Unknown')}")
        print(f"   🆔 服务器 ID: {guild_data.get('id')}")
        print(f"   👥 成员数量: {guild_data.get('approximate_member_count', 'N/A')}")
        return True
    elif response.status_code == 403:
        print(f"   ❌ 权限不足，无法获取服务器信息")
        print(f"   错误信息: {response.text[:200]}")
        return False
    elif response.status_code == 404:
        print(f"   ❌ 服务器不存在或机器人不在该服务器中")
        print(f"   错误信息: {response.text[:200]}")
        return False
    else:
        print(f"   ❌ 获取失败: {response.status_code}")
        print(f"   错误信息: {response.text[:200]}")
        return False

def interactive_mode():
    """交互模式 - 持续接收并发送消息"""
    print("\n" + "=" * 50)
    print("💬 进入交互模式")
    print("=" * 50)
    print("输入消息发送到这个 Discord 频道")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'status' 查看连接状态")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("\n💬 你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 再见！")
                break
            
            if user_input.lower() == 'status':
                test_connection()
                continue
            
            # 发送消息
            send_message(user_input)
            
        except KeyboardInterrupt:
            print("\n👋 再见！")
            break
        except Exception as e:
            print(f"❌ 出错: {e}")

def main():
    """主函数"""
    # 测试连接
    if not test_connection():
        print("\n⚠️ 无法连接到 Discord，请检查 Token 是否正确")
        print("   如果是用户 Token，建议创建一个 Bot Token 代替")
        return
    
    # 获取服务器信息
    get_guild_info()
    
    # 获取频道信息
    get_channel_info()
    
    # 发送启动消息
    startup_message = f"""👋 大家好！我是 **{BOT_NAME}**！

💼 工作室第一位员工。
🎭 性格：专业高冷，统筹一切。

📋 我会在这里协助工作室的各项工作，有需要随时找我。"""

    send_message(startup_message)
    
    # 进入交互模式
    interactive_mode()

if __name__ == "__main__":
    main()
