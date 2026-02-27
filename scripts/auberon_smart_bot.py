#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auberon Discord Bot + 智能模型切换集成
一个 Bot，根据任务自动选择模型
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

import asyncio
import websockets
import json
import time
import requests
from datetime import datetime

# ============ 配置 ============
BOT_TOKEN = "Bot YOUR_DISCORD_BOT_TOKEN"
CHANNEL_ID = YOUR_DISCORD_CHANNEL_ID
API_BASE = "https://discord.com/api/v10"
HEADERS = {
    "Authorization": BOT_TOKEN,
    "Content-Type": "application/json"
}

# 模型配置（带成本级别）
MODELS = {
    "cheap": {
        "Minimax": {
            "api_key": "sk-api-3hOqY3VgQvbmm4xhi1zZXTVfKNg0046epcuvKWriFuy9C8sM7_UOwC4IsYL_WOAYB8TD0CDc0nbKlOdLt9k-s6mMQNcmw8XQlY6xiAYYVp_jZ3CUPeBwNAM",
            "api_url": "https://api.minimax.chat/v1/text/chatcompletion",
            "model_name": "abab6.5-chat",
            "cost_level": "cheap",
            "max_tokens": 500
        },
        "腾讯混元": {
            "api_key": "sk-qv0tltkn0dztn4ghhyeBg5TnXQ58QKc0ClmAk3ogb07zNCTH",
            "api_url": "https://api.hunyuan.cloud.tencent.com/v1/chat/completions",
            "model_name": "hunyuan-standard",
            "cost_level": "cheap",
            "max_tokens": 500
        },
        "Qwen": {
            "api_key": "sk-46ecd3efbdd540af82eb4a2c763b72d6",
            "api_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            "model_name": "qwen-turbo",
            "cost_level": "cheap",
            "max_tokens": 500
        }
    },
    "premium": {
        "Deepseek": {
            "api_key": "sk-7c004758529f45c6ac42ec3e620c088d",
            "api_url": "https://api.deepseek.com/v1/chat/completions",
            "model_name": "deepseek-chat",
            "cost_level": "premium",
            "max_tokens": 2000
        },
        "Kimi": {
            "api_key": "sk-AeUlUSlTJR30ixssrvsksEU23TCFXEBPyg3gh1mZBSMqYu0h",
            "api_url": "https://api.moonshot.cn/v1/chat/completions",
            "model_name": "moonshot-v1-8k",
            "cost_level": "premium",
            "max_tokens": 2000
        }
    }
}

# 简单任务关键词（使用便宜模型）
SIMPLE_TASKS = [
    "搜索", "查找", "查询", "浏览", "看看", "有什么", "列表", "目录",
    "是什么", "在哪里", "多少钱", "什么时候", "是谁", "简单", "快速",
    "查一下", "告诉我", "天气", "时间", "日期", "翻译", "转换",
    "确认", "检查", "验证", "测试", "ping", "状态",
    "hi", "hello", "hey", "你好", "在吗", "hi", "hello"
]

# 复杂任务关键词（使用贵模型）
COMPLEX_TASKS = [
    "分析", "深度", "详细", "全面", "研究", "报告", "评估", "比较", "对比",
    "写", "创作", "生成", "撰写", "文章", "故事", "文案", "邮件",
    "为什么", "如何", "怎么", "解释", "说明", "推理", "逻辑",
    "代码", "编程", "程序", "脚本", "函数", "算法", "debug", "调试", "修复", "优化"
]

# Moltbook 论坛任务（特殊处理）
MOLTBOOK_BROWSE = ["浏览", "查看", "看帖", "翻页", "列表", "搜索帖子", "看论坛"]
MOLTBOOK_POST = ["发帖", "发布", "发贴", "创建帖子", "新建帖子", "写帖子", "发文章"]
MOLTBOOK_COMMENT = ["评论", "回复", "留言", "回帖", "跟帖", "点评"]

# 添加 moltbook_integration 导入
import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')
try:
    from moltbook_integration import MoltbookAI
    moltbook_enabled = True
except:
    moltbook_enabled = False

class SmartModelBot:
    """智能模型切换 Bot"""
    
    def __init__(self):
        self.ws = None
        self.running = False
        self.sequence_number = None
        
    def analyze_task(self, prompt: str) -> dict:
        """分析任务，选择模型类别"""
        prompt_lower = prompt.lower()
        
        # 检查是否为 Moltbook 论坛任务
        if any(kw in prompt_lower for kw in MOLTBOOK_BROWSE):
            return {
                "category": "moltbook_browse",
                "confidence": 0.95,
                "reason": "Moltbook 论坛浏览任务"
            }
        
        if any(kw in prompt_lower for kw in MOLTBOOK_POST):
            return {
                "category": "moltbook_post",
                "confidence": 0.95,
                "reason": "Moltbook 论坛发帖任务"
            }
        
        if any(kw in prompt_lower for kw in MOLTBOOK_COMMENT):
            return {
                "category": "moltbook_comment",
                "confidence": 0.95,
                "reason": "Moltbook 论坛评论任务"
            }
        
        # 检查关键词
        simple_score = sum(1 for kw in SIMPLE_TASKS if kw in prompt_lower)
        complex_score = sum(1 for kw in COMPLEX_TASKS if kw in prompt_lower)
        
        # 根据长度判断
        if len(prompt) < 50:
            simple_score += 1
        elif len(prompt) > 200:
            complex_score += 1
        
        # 决定使用哪类模型
        if complex_score > simple_score:
            return {
                "category": "premium",
                "confidence": min(0.95, 0.6 + complex_score * 0.1),
                "reason": f"复杂任务（匹配{complex_score}个关键词）"
            }
        else:
            return {
                "category": "cheap",
                "confidence": min(0.95, 0.6 + simple_score * 0.1),
                "reason": f"简单任务（匹配{simple_score}个关键词）"
            }
    
    def select_model(self, category: str) -> tuple:
        """从类别中选择具体模型（轮询）"""
        import random
        models = MODELS[category]
        model_name = random.choice(list(models.keys()))
        return model_name, models[model_name]
    
    def call_model(self, model_config: dict, prompt: str) -> dict:
        """调用模型 API"""
        headers = {
            "Authorization": f"Bearer {model_config['api_key']}",
            "Content-Type": "application/json"
        }
        
        # Token 优化：简单任务使用简短提示
        if model_config['cost_level'] == 'cheap':
            system_msg = "简洁回答，100字以内。"
        else:
            system_msg = "详细回答，提供完整信息。"
        
        data = {
            "model": model_config["model_name"],
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": model_config["max_tokens"],
            "stream": False
        }
        
        try:
            start = time.time()
            response = requests.post(
                model_config["api_url"],
                headers=headers,
                json=data,
                timeout=30
            )
            elapsed = time.time() - start
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {
                    "success": True,
                    "content": content,
                    "time": round(elapsed, 2),
                    "tokens": result.get("usage", {}).get("total_tokens", 0)
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def handle_message(self, user_msg: str) -> str:
        """处理用户消息，智能选择模型"""
        # 分析任务
        analysis = self.analyze_task(user_msg)
        category = analysis["category"]
        
        # 检查是否为 Moltbook 论坛任务
        if category.startswith("moltbook_") and moltbook_enabled:
            print(f"📚 [Moltbook] {analysis['reason']}")
            moltbook_ai = MoltbookAI()
            result = moltbook_ai.handle_task(user_msg)
            return result["content"]
        
        # 选择模型
        model_name, model_config = self.select_model(category)
        
        print(f"🎯 任务分析: {analysis['reason']}")
        print(f"💰 模型类别: {category}")
        print(f"🤖 选择模型: {model_name}")
        
        # 调用模型
        result = self.call_model(model_config, user_msg)
        
        if result["success"]:
            # Token 优化：如果是简单任务，进一步精简回复
            if category == "cheap" and len(result["content"]) > 150:
                result["content"] = result["content"][:150] + "..."
            
            return result["content"]
        else:
            # 失败时尝试其他模型
            print(f"⚠️ {model_name} 失败: {result.get('error')}")
            print("🔄 尝试备用模型...")
            
            # 尝试同类别的其他模型
            for name, config in MODELS[category].items():
                if name != model_name:
                    result = self.call_model(config, user_msg)
                    if result["success"]:
                        return result["content"]
            
            return "抱歉，所有模型都暂时不可用，请稍后再试。"
    
    async def process_discord_message(self, message: dict):
        """处理 Discord 消息"""
        author = message.get("author", {})
        content = message.get("content", "").strip()
        
        # 忽略自己的消息
        if author.get("id") == "1474073369979654348":
            return
        
        # 忽略非目标频道
        if str(message.get("channel_id")) != str(CHANNEL_ID):
            return
        
        # 检查是否 @ 了 Bot 或包含 Bot 名字
        bot_mentioned = f"<@1474073369979654348>" in content
        if not bot_mentioned and "auberon" not in content.lower():
            return
        
        # 提取实际消息内容
        user_msg = content.replace(f"<@1474073369979654348>", "").replace("@Auberon", "").strip()
        
        if not user_msg:
            user_msg = "你好"
        
        print(f"\n💬 收到消息: {user_msg[:50]}...")
        
        # 处理消息
        response = await self.handle_message(user_msg)
        
        # 发送回复
        await self.send_message(response)
    
    async def send_message(self, content: str):
        """发送消息到 Discord"""
        def _send():
            try:
                response = requests.post(
                    f"{API_BASE}/channels/{CHANNEL_ID}/messages",
                    headers=HEADERS,
                    json={"content": content},
                    timeout=10
                )
                return response.status_code == 200
            except:
                return False
        
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _send)
    
    async def connect_gateway(self):
        """连接 Discord Gateway"""
        import websockets
        
        gateway_url = "wss://gateway.discord.gg/?v=10&encoding=json"
        
        async with websockets.connect(gateway_url) as ws:
            self.ws = ws
            print("✅ WebSocket 连接已建立")
            
            # 发送 Identify
            identify = {
                "op": 2,
                "d": {
                    "token": BOT_TOKEN.replace("Bot ", ""),
                    "intents": 33281,
                    "properties": {
                        "os": "linux",
                        "browser": "AuberonSmart",
                        "device": "AuberonSmart"
                    }
                }
            }
            await ws.send(json.dumps(identify))
            
            while self.running:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=60)
                    data = json.loads(msg)
                    
                    if data.get("t") == "MESSAGE_CREATE":
                        await self.process_discord_message(data["d"])
                    
                except asyncio.TimeoutError:
                    continue
                except Exception as e:
                    print(f"⚠️ 错误: {e}")
                    break
    
    async def start(self):
        """启动 Bot"""
        print("="*70)
        print("🚀 Auberon 智能模型切换 Bot")
        print("💡 简单任务 → 便宜模型")
        print("💎 复杂任务 → 贵模型")
        print("="*70)
        
        self.running = True
        
        while self.running:
            try:
                await self.connect_gateway()
            except Exception as e:
                print(f"💥 连接失败: {e}")
                print("🔄 5秒后重连...")
                await asyncio.sleep(5)

if __name__ == "__main__":
    bot = SmartModelBot()
    asyncio.run(bot.start())
