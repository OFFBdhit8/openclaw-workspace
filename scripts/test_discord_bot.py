#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Discord Bot 响应
"""

import requests
import json

# Discord API 配置
BOT_TOKEN = "Bot YOUR_DISCORD_BOT_TOKEN"
CHANNEL_ID = "YOUR_DISCORD_CHANNEL_ID"
API_BASE = "https://discord.com/api/v10"

HEADERS = {
    "Authorization": BOT_TOKEN,
    "Content-Type": "application/json"
}

def test_bot_connection():
    """测试 Bot 连接状态"""
    print("🔌 测试 Discord Bot 连接...")
    
    # 获取 Bot 信息
    try:
        response = requests.get(
            f"{API_BASE}/users/@me",
            headers=HEADERS,
            timeout=10
        )
        
        if response.status_code == 200:
            bot_info = response.json()
            print(f"✅ Bot 连接成功!")
            print(f"🤖 Bot 名称: {bot_info.get('username')}#{bot_info.get('discriminator')}")
            print(f"🆔 Bot ID: {bot_info.get('id')}")
            return True
        else:
            print(f"❌ Bot 连接失败: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        return False

def send_test_message():
    """发送测试消息到 Discord"""
    print("\n💬 发送测试消息到 Discord...")
    
    test_messages = [
        "@Auberon 你好，测试一下",
        "@Auberon 搜索今天的天气",
        "@Auberon 写一个简单的Python函数"
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. 发送: {message}")
        
        data = {
            "content": message,
            "tts": False
        }
        
        try:
            response = requests.post(
                f"{API_BASE}/channels/{CHANNEL_ID}/messages",
                headers=HEADERS,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"   ✅ 消息发送成功")
                msg_data = response.json()
                print(f"   消息ID: {msg_data.get('id')}")
            else:
                print(f"   ❌ 发送失败: HTTP {response.status_code}")
                print(f"   响应: {response.text[:100]}")
                
        except Exception as e:
            print(f"   ❌ 发送异常: {e}")

def check_bot_status():
    """检查 Bot 状态"""
    print("\n📊 检查 Bot 状态...")
    
    # 检查服务状态
    import subprocess
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "auberon-smart.service"],
            capture_output=True,
            text=True
        )
        print(f"🔧 服务状态: {result.stdout.strip()}")
    except:
        print("🔧 服务状态: 未知")
    
    # 检查进程
    try:
        result = subprocess.run(
            ["ps", "aux", "|", "grep", "auberon_smart_bot.py", "|", "grep", "-v", "grep"],
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            lines = result.stdout.strip().split('\n')
            print(f"🔄 进程运行中: {len(lines)} 个进程")
        else:
            print("🔄 进程状态: 未找到")
    except:
        print("🔄 进程状态: 检查失败")

def main():
    print("="*60)
    print("Discord Bot 测试工具")
    print("="*60)
    
    # 测试连接
    if not test_bot_connection():
        print("\n⚠️  Bot 连接失败，请检查 Token 和网络")
        return
    
    # 检查状态
    check_bot_status()
    
    # 发送测试消息
    send_test_message()
    
    print("\n" + "="*60)
    print("✅ 测试完成!")
    print("请到 Discord 频道查看 Bot 是否回复")
    print("频道ID: YOUR_DISCORD_CHANNEL_ID")

if __name__ == "__main__":
    main()
