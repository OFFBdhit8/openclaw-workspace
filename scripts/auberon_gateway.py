#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auberon - 工作室第一位员工（WebSocket Gateway 版）
支持在线状态显示
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

import asyncio
import websockets
import json
import time
import signal
import requests
from datetime import datetime

# ============ 配置区域 ============
BOT_TOKEN = "Bot YOUR_DISCORD_BOT_TOKEN"
GUILD_ID = YOUR_GUILD_ID
CHANNEL_ID = YOUR_DISCORD_CHANNEL_ID
BOT_NAME = "Auberon"
BOT_STATUS = "统筹一切"

API_BASE = "https://discord.com/api/v10"
GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"
HEADERS = {
    "Authorization": BOT_TOKEN,
    "Content-Type": "application/json"
}

# =================================

PERSONALITY = {
    "name": "Auberon",
    "title": "工作室第一位员工",
    "temperament": "专业高冷，统筹一切",
    "responses": {
        "greeting": ["收到。", "嗯。", "说。"],
        "acknowledgment": ["明白。", "收到。", "了解。"],
        "task_response": ["我来处理。", "统筹安排中。", "交给我。"],
        "error": ["不清楚。", "无法处理。", "需要更多信息。"]
    }
}

class AuberonGatewayBot:
    """支持 WebSocket Gateway 的 Auberon 机器人"""
    
    def __init__(self):
        self.ws = None
        self.running = False
        self.session_id = None
        self.heartbeat_interval = None
        self.sequence_number = None
        self.bot_user = None
        
    async def start(self):
        """启动机器人"""
        print("=" * 60)
        print(f"🚀 启动 {BOT_NAME}（WebSocket Gateway 版）")
        print(f"🎭 性格: {PERSONALITY['temperament']}")
        print(f"💼 身份: {PERSONALITY['title']}")
        print(f"🌐 连接: {GATEWAY_URL}")
        print("=" * 60)
        
        self.running = True
        
        # 设置信号处理
        for sig in (signal.SIGTERM, signal.SIGINT):
            asyncio.get_event_loop().add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))
        
        while self.running:
            try:
                await self.connect_gateway()
            except Exception as e:
                print(f"💥 连接异常: {e}")
                print("🔄 5秒后重连...")
                await asyncio.sleep(5)
    
    async def connect_gateway(self):
        """连接 Discord Gateway"""
        print(f"\n📡 正在连接 Gateway...")
        
        async with websockets.connect(GATEWAY_URL) as websocket:
            self.ws = websocket
            print("✅ WebSocket 连接已建立")
            
            while self.running:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=60)
                    await self.handle_message(json.loads(message))
                except asyncio.TimeoutError:
                    continue
                except websockets.exceptions.ConnectionClosed:
                    print("⚠️ WebSocket 连接已关闭")
                    break
                except Exception as e:
                    print(f"⚠️ 消息处理异常: {e}")
    
    async def handle_message(self, data):
        """处理 Gateway 消息"""
        op = data.get("op")
        event_type = data.get("t")
        
        # 调试：打印所有收到的事件（除了心跳和某些频繁事件）
        if event_type and event_type not in ["PRESENCE_UPDATE", "TYPING_START", "GUILD_CREATE"]:
            print(f"📨 [{datetime.now().strftime('%H:%M:%S')}] 收到事件: {event_type}")
        
        if "s" in data and data["s"] is not None:
            self.sequence_number = data["s"]
        
        # 处理 Hello
        if op == 10:
            self.heartbeat_interval = data["d"]["heartbeat_interval"] / 1000
            print(f"💓 心跳间隔: {self.heartbeat_interval}秒")
            
            # 开始心跳
            asyncio.create_task(self.heartbeat_loop())
            
            # 发送 Identify
            await self.send_identify()
        
        # 处理心跳确认
        elif op == 11:
            print("💓 心跳确认收到")
        
        # 处理事件
        elif event_type == "READY":
            self.session_id = data["d"]["session_id"]
            self.bot_user = data["d"]["user"]
            print(f"✅ Gateway 认证成功！")
            print(f"   🤖 用户名: {self.bot_user['username']}")
            print(f"   🆔 ID: {self.bot_user['id']}")
            print(f"   🟢 状态: 在线")
            
            # 发送启动消息
            await self.send_startup_message()
            
            # 更新状态为在线
            await self.update_presence()
        
        elif event_type == "MESSAGE_CREATE":
            await self.handle_message_create(data["d"])
    
    async def heartbeat_loop(self):
        """心跳循环"""
        while self.running and self.ws:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                await self.ws.send(json.dumps({"op": 1, "d": self.sequence_number}))
                print("💓 心跳发送")
            except Exception as e:
                print(f"⚠️ 心跳异常: {e}")
                break
    
    async def send_identify(self):
        """发送 Identify 消息"""
        identify = {
            "op": 2,
            "d": {
                "token": BOT_TOKEN.replace("Bot ", ""),
                "intents": 33281,  # Guilds + Guild Messages + Message Content Intent
                "properties": {
                    "os": "linux",
                    "browser": "AuberonBot",
                    "device": "AuberonBot"
                },
                "presence": {
                    "status": "online",
                    "activities": [{
                        "name": BOT_STATUS,
                        "type": 0
                    }]
                }
            }
        }
        await self.ws.send(json.dumps(identify))
        print("🔐 Identify 已发送")
    
    async def update_presence(self):
        """更新在线状态"""
        presence = {
            "op": 3,
            "d": {
                "since": None,
                "activities": [{
                    "name": BOT_STATUS,
                    "type": 0
                }],
                "status": "online",
                "afk": False
            }
        }
        await self.ws.send(json.dumps(presence))
        print("🟢 在线状态已更新")
    
    async def send_startup_message(self):
        """发送启动消息"""
        import requests
        import asyncio
        
        headers = HEADERS.copy()
        headers["Authorization"] = BOT_TOKEN
        
        startup_message = f"""
👋 **大家好，我是 {BOT_NAME}**

💼 **身份**: {PERSONALITY['title']}
🎭 **性格**: {PERSONALITY['temperament']}
⚡ **状态**: 🟢 在线，统筹一切

📋 **我能做什么**:
• 统筹安排工作
• 协调沟通
• 任务管理与跟进
• 信息整理与汇报

💬 **使用方式**:
• 直接 @{self.bot_user['username']} 与我对话
• 或直接发送消息

随时待命。
        """
        
        data = {"content": startup_message.strip(), "tts": False}
        
        def _send():
            try:
                response = requests.post(
                    f"{API_BASE}/channels/{CHANNEL_ID}/messages",
                    headers=headers,
                    json=data,
                    timeout=10
                )
                return response.status_code == 200
            except Exception as e:
                print(f"⚠️ 发送启动消息异常: {e}")
                return False
        
        loop = asyncio.get_event_loop()
        success = await loop.run_in_executor(None, _send)
        if success:
            print("✅ 启动消息已发送")
        else:
            print("⚠️ 启动消息发送失败")
    
    async def handle_message_create(self, message):
        """处理收到的消息"""
        # 忽略机器人自己的消息
        if message.get("author", {}).get("id") == self.bot_user.get("id"):
            return
        
        # 忽略系统消息
        if message.get("type") != 0:
            return
        
        author = message.get("author", {})
        content = message.get("content", "").strip()
        channel_id = message.get("channel_id")
        
        # 记录所有消息（用于调试）
        is_target_channel = str(channel_id) == str(CHANNEL_ID)
        print(f"\n📨 [{datetime.now().strftime('%H:%M:%S')}] 收到消息:")
        print(f"   👤 {author.get('username')}")
        print(f"   📝 内容: {content[:80]}...")
        print(f"   📺 频道ID: {channel_id} {'✅' if is_target_channel else '❌ 非目标频道'}")
        print(f"   🎯 目标频道ID: {CHANNEL_ID}")
        
        # 只处理指定频道的消息
        if not is_target_channel:
            print(f"   ⚠️ 忽略非目标频道的消息")
            return
        
        # 检查是否提及机器人
        bot_mentioned = False
        if self.bot_user and f"<@{self.bot_user.get('id')}>" in content:
            bot_mentioned = True
            content = content.replace(f"<@{self.bot_user.get('id')}>", "").strip()
            print(f"   🔔 检测到 @ 提及")
        
        # 检查是否包含机器人名字
        if not bot_mentioned and BOT_NAME.lower() in content.lower():
            bot_mentioned = True
            print(f"   🔔 检测到机器人名称提及")
        
        # 如果是提及或包含机器人名字，则回复
        if bot_mentioned:
            response = self.generate_response(content)
            print(f"   🤖 生成回复: {response}")
            success = await self.send_message(response)
            if success:
                print(f"   ✅ 回复已发送")
            else:
                print(f"   ❌ 回复发送失败")
        else:
            print(f"   ⚠️ 未检测到提及，忽略消息")
    
    def generate_response(self, content):
        """生成回复"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["你好", "hi", "hello", "hey"]):
            return f"你好，我是 {BOT_NAME}。"
        
        elif any(word in content_lower for word in ["状态", "status", "怎样", "如何"]):
            return "一切正常，统筹中。"
        
        elif any(word in content_lower for word in ["任务", "工作", "安排", "计划"]):
            return "收到，我来处理。"
        
        elif any(word in content_lower for word in ["谢谢", "感谢", "thanks"]):
            return "职责所在。"
        
        else:
            # 直接回复，去掉前缀
            return "收到。"
    
    async def send_message(self, content):
        """发送消息（使用 executor 避免阻塞）"""
        import requests
        import asyncio
        
        headers = HEADERS.copy()
        headers["Authorization"] = BOT_TOKEN
        
        data = {"content": content, "tts": False}
        
        def _send():
            try:
                response = requests.post(
                    f"{API_BASE}/channels/{CHANNEL_ID}/messages",
                    headers=headers,
                    json=data,
                    timeout=10
                )
                if response.status_code == 200:
                    print(f"   📤 消息发送成功 (ID: {response.json().get('id', 'unknown')})")
                    return True
                else:
                    print(f"   ❌ 消息发送失败: {response.status_code} - {response.text[:100]}")
                    return False
            except requests.exceptions.Timeout:
                print(f"   ⏱️  消息发送超时")
                return False
            except Exception as e:
                print(f"   💥 消息发送异常: {e}")
                return False
        
        # 使用 run_in_executor 避免阻塞事件循环
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _send)
    
    async def stop(self):
        """停止机器人"""
        print("\n📡 正在停止...")
        self.running = False
        if self.ws:
            await self.ws.close()
        print(f"👋 {BOT_NAME} 已停止")

# 主函数
def main():
    bot = AuberonGatewayBot()
    
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        print("\n👋 收到停止信号")
    except Exception as e:
        print(f"💥 严重错误: {e}")

if __name__ == "__main__":
    main()
