#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auberon 智能 Bot 修复版 + 优化集成 - 第一部分
"""

import sys
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

# Brave API 配置
BRAVE_API_KEY = "BSAo80XKa0ke0SNirZxhOZQ6urU--Ew"

# 模型配置
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

# 任务关键词（修复版）
SIMPLE_TASKS = [
    "搜索", "查找", "查询", "浏览", "看看", "有什么", "列表", "目录",
    "是什么", "在哪里", "多少钱", "什么时候", "是谁", "简单", "快速",
    "查一下", "告诉我", "天气", "时间", "日期", "翻译", "转换",
    "确认", "检查", "验证", "测试", "ping", "状态",
    "hi", "hello", "hey", "你好", "在吗", "hi", "hello"
]

COMPLEX_TASKS = [
    "分析", "深度", "详细", "全面", "研究", "报告", "评估", "比较", "对比",
    "写", "创作", "生成", "撰写", "文章", "故事", "文案", "邮件",
    "为什么", "如何", "怎么", "解释", "说明", "推理", "逻辑",
    "代码", "编程", "程序", "脚本", "函数", "算法", "debug", "调试", "修复", "优化"
]

# Moltbook 论坛任务（修复关键词）
MOLTBOOK_BROWSE = ["浏览论坛", "看论坛", "刷论坛", "查看帖子", "看帖", "翻页", "列表", "搜索帖子"]
MOLTBOOK_POST = ["发帖", "发布帖子", "发帖子", "创建帖子", "新建帖子", "写帖子", "发文章", "发布文章", "写文章"]
MOLTBOOK_COMMENT = ["评论", "回复", "留言", "回帖", "跟帖", "点评", "发表评论"]

class OptimizedAuberonBot:
    """优化版 Auberon Bot"""
    
    def __init__(self):
        self.ws = None
        self.running = False
        self.sequence_number = None
        self.stats = {
            "total_messages": 0,
            "cheap_model_used": 0,
            "premium_model_used": 0,
            "search_performed": 0,
            "moltbook_tasks": 0
        }
        
    def brave_search(self, query: str, count: int = 3) -> list:
        """Brave 搜索"""
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": BRAVE_API_KEY
        }
        
        params = {
            "q": query,
            "count": count,
            "country": "US",
            "search_lang": "en"
        }
        
        try:
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('web', {}).get('results', [])
                self.stats["search_performed"] += 1
                return results[:count]
            return []
        except:
            return []
    
    def analyze_task(self, prompt: str) -> dict:
        """分析任务（修复版）"""
        prompt_lower = prompt.lower()
        
        # 检查是否为 Moltbook 论坛任务（更精确的匹配）
        for kw in MOLTBOOK_BROWSE:
            if kw in prompt_lower:
                return {
                    "category": "moltbook_browse",
                    "confidence": 0.95,
                    "reason": "Moltbook 论坛浏览任务"
                }
        
        for kw in MOLTBOOK_POST:
            if kw in prompt_lower:
                return {
                    "category": "moltbook_post",
                    "confidence": 0.95,
                    "reason": "Moltbook 论坛发帖任务"
                }
        
        for kw in MOLTBOOK_COMMENT:
            if kw in prompt_lower:
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
        """选择模型"""
        import random
        
        if category in ["cheap", "premium"]:
            models = MODELS[category]
            model_name = random.choice(list(models.keys()))
            return model_name, models[model_name]
        elif category == "moltbook_browse":
            # 浏览用 deepseek
            return "Deepseek", MODELS["premium"]["Deepseek"]
        elif category in ["moltbook_post", "moltbook_comment"]:
            # 发帖/评论用 Kimi
            return "Kimi", MODELS["premium"]["Kimi"]
        else:
            # 默认用便宜模型
            return "Minimax", MODELS["cheap"]["Minimax"]
    
    def call_model(self, model_config: dict, prompt: str, search_results: list = None) -> dict:
        """调用模型 API（集成搜索）"""
        headers = {
            "Authorization": f"Bearer {model_config['api_key']}",
            "Content-Type": "application/json"
        }
        
        # 构建系统消息
        if model_config['cost_level'] == 'cheap':
            system_msg = "简洁回答，100字以内。"
        else:
            system_msg = "详细回答，提供完整信息。"
        
        # 如果有搜索结果，添加到提示中
        user_content = prompt
        if search_results:
            results_text = "\n".join([
                f"{i+1}. {r.get('title', 'No title')}\n   链接: {r.get('url', 'No URL')}\n   摘要: {r.get('description', 'No description')[:100]}..."
                for i, r in enumerate(search_results)
            ])
            user_content = f"用户查询: {prompt}\n\n搜索到的信息:\n{results_text}\n\n请基于以上信息回答。"
        
        data = {
            "model": model_config["model_name"],
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_content}
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
                
                # Token 优化：如果是便宜模型，精简回复
                if model_config['cost_level'] == 'cheap' and len(content) > 150:
                    content = content[:150] + "..."
                
                return {
                    "success": True,
                    "content": content,
                    "time": round(elapsed, 2),
                    "tokens": result.get("usage", {}).get("total_tokens", 0)
                }
            else:
                return {"success": False, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}    async def handle_message(self, user_msg: str) -> str:
        """处理用户消息"""
        self.stats["total_messages"] += 1
        
        # 分析任务
        analysis = self.analyze_task(user_msg)
        category = analysis["category"]
        
        print(f"\n🎯 收到消息: {user_msg[:50]}...")
        print(f"📊 任务分析: {analysis['reason']}")
        print(f"💰 模型类别: {category}")
        
        # 检查是否需要搜索
        needs_search = any(kw in user_msg.lower() for kw in ["搜索", "查找", "查询", "search", "find"])
        search_results = []
        
        if needs_search:
            print("🌐 执行 Brave 搜索...")
            search_results = self.brave_search(user_msg, count=3)
            print(f"📊 找到 {len(search_results)} 个搜索结果")
        
        # 选择模型
        model_name, model_config = self.select_model(category)
        print(f"🤖 选择模型: {model_name}")
        
        # 更新统计
        if category == "cheap" or category.startswith("moltbook"):
            self.stats["cheap_model_used"] += 1
        else:
            self.stats["premium_model_used"] += 1
        
        if category.startswith("moltbook"):
            self.stats["moltbook_tasks"] += 1
        
        # 调用模型
        result = self.call_model(model_config, user_msg, search_results)
        
        if result["success"]:
            response = result["content"]
            
            # 添加统计信息（仅限复杂任务）
            if category == "premium":
                response += f"\n\n⏱️ 响应时间: {result['time']}秒 | 📊 Token使用: {result['tokens']}"
            
            return response
        else:
            print(f"⚠️ 模型调用失败: {result.get('error')}")
            return "抱歉，暂时无法处理您的请求，请稍后再试。"
    
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
        success = await loop.run_in_executor(None, _send)
        
        if success:
            print("✅ 回复已发送到 Discord")
        else:
            print("❌ 回复发送失败")
    
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
                    "intents": 33281,  # Guilds + Guild Messages
                    "properties": {
                        "os": "linux",
                        "browser": "AuberonOptimized",
                        "device": "AuberonOptimized"
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
                    print(f"⚠️ WebSocket 错误: {e}")
                    break
    
    async def start(self):
        """启动 Bot"""
        print("="*70)
        print("🚀 Auberon 优化版 Bot")
        print("💡 集成: Brave搜索 + 智能模型切换 + Token优化")
        print("💰 策略: 简单任务→便宜模型 | 复杂任务→贵模型")
        print("🌐 搜索: 自动使用 Brave Search API")
        print("="*70)
        
        self.running = True
        
        while self.running:
            try:
                await self.connect_gateway()
            except Exception as e:
                print(f"💥 连接失败: {e}")
                print("🔄 5秒后重连...")
                await asyncio.sleep(5)
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        total = self.stats["total_messages"]
        if total == 0:
            return {"message": "暂无消息处理"}
        
        cheap_percent = self.stats["cheap_model_used"] / total * 100
        premium_percent = self.stats["premium_model_used"] / total * 100
        
        return {
            "total_messages": total,
            "cheap_model_usage": f"{cheap_percent:.1f}%",
            "premium_model_usage": f"{premium_percent:.1f}%",
            "search_performed": self.stats["search_performed"],
            "moltbook_tasks": self.stats["moltbook_tasks"],
            "estimated_cost_savings": f"约 {cheap_percent * 0.7:.1f}%"
        }


# 测试函数
def test_bot_logic():
    """测试 Bot 逻辑"""
    bot = OptimizedAuberonBot()
    
    test_cases = [
        "你好，测试一下",
        "搜索今天的天气",
        "写一个简单的Python函数",
        "浏览一下moltbook论坛",
        "发一个关于AI的帖子",
        "评论这个帖子"
    ]
    
    print("🔍 测试 Bot 逻辑:")
    for msg in test_cases:
        analysis = bot.analyze_task(msg)
        model_name, _ = bot.select_model(analysis["category"])
        print(f"  '{msg[:20]}...' → {analysis['category']} → {model_name}")


if __name__ == "__main__":
    # 测试逻辑
    test_bot_logic()
    
    print("\n" + "="*70)
    print("要启动 Bot，请运行:")
    print("python3 -c \"from auberon_optimized_v1 import OptimizedAuberonBot; import asyncio; asyncio.run(OptimizedAuberonBot().start())\"")
    print("="*70)