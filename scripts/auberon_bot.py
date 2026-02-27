#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auberon - 工作室第一位员工
性格：专业高冷，统筹一切
"""

import requests
import json
import time
import threading
from datetime import datetime

# ============ 配置区域 ============
# Bot Token（注意：需要加上 "Bot " 前缀）
BOT_TOKEN = "Bot YOUR_DISCORD_BOT_TOKEN"

# 服务器和频道配置
GUILD_ID = YOUR_GUILD_ID  # 服务器 ID
CHANNEL_ID = YOUR_DISCORD_CHANNEL_ID  # 频道 ID

# Bot 设定
BOT_NAME = "Auberon"
BOT_AVATAR = None  # 可选：头像 URL
BOT_STATUS = "统筹一切"  # 状态

# Discord API 配置
API_BASE = "https://discord.com/api/v10"
HEADERS = {
    "Authorization": BOT_TOKEN,
    "Content-Type": "application/json",
    "User-Agent": f"DiscordBot (https://github.com/discord, 1.0.0)"
}

# 轮询间隔（秒）
POLL_INTERVAL = 2

# =================================

# Auberon 的性格设定
PERSONALITY = {
    "name": "Auberon",
    "title": "工作室第一位员工",
    "temperament": "专业高冷，统筹一切",
    "responses": {
        "greeting": [
            "收到。",
            "嗯。",
            "说。"
        ],
        "acknowledgment": [
            "明白。",
            "收到。",
            "了解。"
        ],
        "task_response": [
            "我来处理。",
            "统筹安排中。",
            "交给我。"
        ],
        "error": [
            "不清楚。",
            "无法处理。",
            "需要更多信息。"
        ]
    }
}

class AuberonBot:
    """Auberon 机器人核心类"""
    
    def __init__(self):
        self.running = False
        self.last_message_id = None
        self.bot_user = None
        
    def start(self):
        """启动机器人"""
        print("=" * 60)
        print(f"🚀 启动 {BOT_NAME}")
        print(f"🎭 性格: {PERSONALITY['temperament']}")
        print(f"💼 身份: {PERSONALITY['title']}")
        print("=" * 60)
        
        # 验证连接
        if not self.verify_connection():
            print("❌ 连接验证失败")
            return False
        
        # 设置状态
        self.set_presence()
        
        # 发送启动消息
        self.send_startup_message()
        
        # 启动消息轮询
        self.running = True
        self.poll_thread = threading.Thread(target=self.message_poll_loop)
        self.poll_thread.daemon = True
        self.poll_thread.start()
        
        print(f"\n✅ {BOT_NAME} 已启动")
        print(f"📡 开始监听消息...")
        print(f"💬 输入 'stop' 停止机器人")
        
        # 主循环
        try:
            while self.running:
                cmd = input().strip().lower()
                if cmd in ['stop', 'exit', 'quit']:
                    self.running = False
                    print("👋 正在停止...")
        except KeyboardInterrupt:
            self.running = False
            print("\n👋 收到停止信号")
        
        return True
    
    def verify_connection(self):
        """验证 Discord 连接"""
        print("\n📡 验证连接...")
        
        try:
            response = requests.get(f"{API_BASE}/users/@me", headers=HEADERS, timeout=10)
            
            if response.status_code == 200:
                self.bot_user = response.json()
                print(f"✅ 连接成功！")
                print(f"   🤖 用户名: {self.bot_user.get('username')}")
                print(f"   🆔 ID: {self.bot_user.get('id')}")
                return True
            else:
                print(f"❌ 连接失败: {response.status_code}")
                print(f"   错误: {response.text[:200]}")
                return False
                
        except Exception as e:
            print(f"💥 连接异常: {e}")
            return False
    
    def set_presence(self):
        """设置机器人状态"""
        try:
            # Discord Gateway 需要 WebSocket，这里用简单的状态更新
            print(f"\n📊 状态: {BOT_STATUS}")
        except Exception as e:
            print(f"⚠️ 设置状态失败: {e}")
    
    def send_startup_message(self):
        """发送启动消息"""
        startup_message = f"""
👋 **大家好，我是 {BOT_NAME}**

💼 **身份**: {PERSONALITY['title']}
🎭 **性格**: {PERSONALITY['temperament']}
⚡ **状态**: 已上线，统筹一切

📋 **我能做什么**:
• 统筹安排工作
• 协调沟通
• 任务管理与跟进
• 信息整理与汇报

💬 **使用方式**:
• 直接 @{self.bot_user.get('username')} 与我对话
• 或直接发送消息

随时待命。
        """
        
        success = self.send_message(startup_message)
        if success:
            print("✅ 启动消息已发送")
        else:
            print("⚠️ 启动消息发送失败")
    
    def send_message(self, content):
        """发送消息到指定频道"""
        try:
            data = {
                "content": content.strip(),
                "tts": False
            }
            
            response = requests.post(
                f"{API_BASE}/channels/{CHANNEL_ID}/messages",
                headers=HEADERS,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                return True
            else:
                print(f"⚠️ 发送消息失败: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"⚠️ 发送消息异常: {e}")
            return False
    
    def get_messages(self, limit=10):
        """获取频道消息"""
        try:
            url = f"{API_BASE}/channels/{CHANNEL_ID}/messages"
            params = {"limit": limit}
            
            if self.last_message_id:
                params["after"] = self.last_message_id
            
            response = requests.get(url, headers=HEADERS, params=params, timeout=10)
            
            if response.status_code == 200:
                messages = response.json()
                if messages:
                    self.last_message_id = messages[0]["id"]
                return messages
            else:
                print(f"⚠️ 获取消息失败: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"⚠️ 获取消息异常: {e}")
            return []
    
    def process_message(self, message):
        """处理收到的消息"""
        # 忽略机器人自己的消息
        if message.get("author", {}).get("id") == self.bot_user.get("id"):
            return
        
        # 忽略系统消息
        if message.get("type") != 0:
            return
        
        author = message.get("author", {})
        content = message.get("content", "").strip()
        
        print(f"\n💬 收到消息:")
        print(f"   👤 {author.get('username')}: {content[:50]}...")
        
        # 检查是否提及机器人
        bot_mentioned = False
        if f"<@{self.bot_user.get('id')}>" in content:
            bot_mentioned = True
            content = content.replace(f"<@{self.bot_user.get('id')}>", "").strip()
        
        # 检查是否是直接消息（没有提及但内容包含机器人名字）
        if not bot_mentioned and BOT_NAME.lower() in content.lower():
            bot_mentioned = True
        
        # 如果是提及或包含机器人名字，则回复
        if bot_mentioned:
            response = self.generate_response(content)
            self.send_message(response)
            print(f"   🤖 已回复: {response[:30]}...")
    
    def generate_response(self, content):
        """根据内容生成回复"""
        content_lower = content.lower()
        
        # 问候
        if any(word in content_lower for word in ["你好", "hi", "hello", "hey"]):
            import random
            return f"{random.choice(PERSONALITY['responses']['greeting'])} {BOT_NAME}，{PERSONALITY['title']}。"
        
        # 状态查询
        elif any(word in content_lower for word in ["状态", "status", "怎样", "如何"]):
            return f"一切正常。统筹中。"
        
        # 任务安排
        elif any(word in content_lower for word in ["任务", "工作", "安排", "计划"]):
            import random
            return f"{random.choice(PERSONALITY['responses']['task_response'])}"
        
        # 感谢
        elif any(word in content_lower for word in ["谢谢", "感谢", "thanks"]):
            return "职责所在。"
        
        # 默认回复
        else:
            import random
            return f"{random.choice(PERSONALITY['responses']['acknowledgment'])} {content[:50]}... 我会处理。"
    
    def message_poll_loop(self):
        """消息轮询循环"""
        print(f"\n📡 开始轮询消息 (间隔: {POLL_INTERVAL}s)...")
        
        while self.running:
            try:
                messages = self.get_messages(limit=5)
                
                # 逆序处理，从最旧到最新
                for message in reversed(messages):
                    self.process_message(message)
                
                time.sleep(POLL_INTERVAL)
                
            except Exception as e:
                print(f"⚠️ 轮询异常: {e}")
                time.sleep(POLL_INTERVAL * 2)
    
    def stop(self):
        """停止机器人"""
        self.running = False
        if hasattr(self, 'poll_thread'):
            self.poll_thread.join(timeout=5)
        print(f"\n👋 {BOT_NAME} 已停止")

# 主函数
def main():
    """主函数"""
    bot = AuberonBot()
    
    try:
        bot.start()
    except Exception as e:
        print(f"💥 严重错误: {e}")
    finally:
        bot.stop()

if __name__ == "__main__":
    main()
