#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auberon 完整优化版 - 集成监控和优化
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

import asyncio
import websockets
import json
import time
import requests
from datetime import datetime

# 导入监控系统
try:
    from token_monitor import TokenMonitor
    MONITOR_ENABLED = True
    monitor = TokenMonitor()
except:
    MONITOR_ENABLED = False
    print("⚠️ Token 监控系统未启用")

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

class FullyOptimizedAuberonBot:
    """完全优化版 Auberon Bot"""
    
    def __init__(self):
        self.ws = None
        self.running = False
        self.stats = {
            "start_time": datetime.now().isoformat(),
            "total_messages": 0,
            "successful_responses": 0,
            "failed_responses": 0
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
                return results[:count]
            return []
        except Exception as e:
            print(f"⚠️ Brave 搜索失败: {e}")
            return []
    
    def analyze_and_select(self, prompt: str) -> tuple:
        """分析和选择模型"""
        prompt_lower = prompt.lower()
        
        # 简单任务关键词
        simple_keywords = ["搜索", "查找", "查询", "天气", "时间", "是什么", "在哪里", "多少钱", "简单", "快速"]
        
        # 复杂任务关键词
        complex_keywords = ["分析", "写", "创作", "代码", "编程", "解释", "为什么", "如何", "详细", "报告"]
        
        simple_score = sum(1 for kw in simple_keywords if kw in prompt_lower)
        complex_score = sum(1 for kw in complex_keywords if kw in prompt_lower)
        
        # 根据长度调整
        if len(prompt) < 30:
            simple_score += 1
        elif len(prompt) > 150:
            complex_score += 1
        
        # 决定模型类别
        if complex_score > simple_score:
            category = "premium"
            reason = f"复杂任务（{complex_score}分）"
        else:
            category = "cheap"
            reason = f"简单任务（{simple_score}分）"
        
        # 选择具体模型
        import random
        models = MODELS[category]
        model_name = random.choice(list(models.keys()))
        
        return category, model_name, models[model_name], reason
    
    def call_model_with_monitoring(self, model_config: dict, prompt: str, search_results: list = None) -> dict:
        """调用模型并监控"""
        headers = {
            "Authorization": f"Bearer {model_config['api_key']}",
            "Content-Type": "application/json"
        }
        
        # 构建提示
        user_content = prompt
        task_type = "general"
        
        if search_results:
            results_text = "\n".join([
                f"{i+1}. {r.get('title', '无标题')}"
                for i, r in enumerate(search_results[:2])
            ])
            user_content = f"查询: {prompt}\n\n搜索结果:\n{results_text}\n\n请基于以上信息回答。"
            task_type = "search"
        
        # 系统消息优化
        if model_config['cost_level'] == 'cheap':
            system_msg = "简洁回答，重点突出。"
        else:
            system_msg = "详细回答，提供有价值的信息。"
        
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
            start_time = time.time()
            response = requests.post(
                model_config["api_url"],
                headers=headers,
                json=data,
                timeout=30
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                usage = result.get("usage", {})
                tokens_in = usage.get("prompt_tokens", 0)
                tokens_out = usage.get("completion_tokens", 0)
                
                # Token 优化
                if model_config['cost_level'] == 'cheap' and len(content) > 120:
                    content = content[:120] + "..."
                
                # 记录使用情况
                if MONITOR_ENABLED:
                    monitor.record_usage(
                        model_config["model_name"],
                        tokens_in,
                        tokens_out,
                        task_type
                    )
                
                return {
                    "success": True,
                    "content": content,
                    "time": round(elapsed, 2),
                    "tokens_in": tokens_in,
                    "tokens_out": tokens_out,
                    "total_tokens": tokens_in + tokens_out
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "response_text": response.text[:200]
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def handle_message(self, user_msg: str) -> str:
        """处理用户消息"""
        self.stats["total_messages"] += 1
        
        print(f"\n💬 收到消息: {user_msg[:50]}...")
        
        # 分析和选择模型
        category, model_name, model_config, reason = self.analyze_and_select(user_msg)
        print(f"🎯 分析: {reason}")
        print(f"💰 类别: {category}")
        print(f"🤖 模型: {model_name}")
        
        # 检查是否需要搜索
        needs_search = any(kw in user_msg.lower() for kw in ["搜索", "查找", "查询", "search"])
        search_results = []
        
        if needs_search:
            print("🌐 执行 Brave 搜索...")
            search_results = self.brave_search(user_msg)
            print(f"📊 找到 {len(search_results)} 个结果")
        
        # 调用模型
        result = self.call_model_with_monitoring(model_config, user_msg, search_results)
        
        if result["success"]:
            self.stats["successful_responses"] += 1
            
            response = result["content"]
            
            # 添加性能信息（仅限复杂任务）
            if category == "premium":
                response += f"\n\n⏱️ {result['time']}秒 | 📊 {result['total_tokens']} tokens"
            
            return response
        else:
            self.stats["failed_responses"] += 1
            print(f"⚠️ 失败: {result.get('error')}")
            
            # 尝试备用模型
            print("🔄 尝试备用模型...")
            backup_category = "cheap" if category == "premium" else "premium"
            models = MODELS[backup_category]
            backup_name = list(models.keys())[0]
            backup_config = models[backup_name]
            
            backup_result = self.call_model_with_monitoring(backup_config, user_msg, search_results)
            
            if backup_result["success"]:
                return backup_result["content"]
            else:
                return "抱歉，暂时无法处理您的请求。请稍后再试。"
    
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
        
        # 检查是否 @ 了 Bot
        bot_mentioned = f"<@1474073369979654348>" in content or "@Auberon" in content
        if not bot_mentioned:
            return
        
        # 提取消息内容
        user_msg = content.replace(f"<@1474073369979654348>", "").replace("@Auberon", "").strip()
        
        if not user_msg:
            user_msg = "你好"
        
        # 处理消息
        response = await self.handle_message(user_msg)
        
        # 发送回复
        await self.send_message(response)
    
    async def send_message(self, content: str):
        """发送消息"""
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
            print("✅ 回复已发送")
        else:
            print("❌ 回复发送失败")
    
    async def connect_gateway(self):
        """连接 Discord Gateway"""
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
                        "browser": "AuberonFull",
                        "device": "AuberonFull"
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
        print("🚀 Auberon 完全优化版")
        print("💡 功能: 智能模型切换 + Brave搜索 + Token监控 + 成本优化")
        print("💰 目标: 最大化成本效益，智能路由任务")
        print("📊 监控: 实时记录使用情况，提供优化建议")
        print("="*70)
        
        if MONITOR_ENABLED:
            print("✅ Token 监控系统已启用")
        else:
            print("⚠️ Token 监控系统未启用")
        
        self.running = True
        
        while self.running:
            try:
                await self.connect_gateway()
            except Exception as e:
                print(f"💥 连接失败: {e}")
                print("🔄 10秒后重连...")
                await asyncio.sleep(10)
    
    def get_status_report(self) -> str:
        """获取状态报告"""
        total = self.stats["total_messages"]
        success = self.stats["successful_responses"]
        failed = self.stats["failed_responses"]
        
        if total == 0:
            success_rate = 0
        else:
            success_rate = success / total * 100
        
        report = [
            "📊 Auberon Bot 状态报告",
            "="*40,
            f"🕒 启动时间: {self.stats['start_time']}",
            f"📨 总消息数: {total}",
            f"✅ 成功回复: {success}",
            f"❌ 失败回复: {failed}",
            f"📈 成功率: {success_rate:.1f}%",
            ""
        ]
        
        if MONITOR_ENABLED:
            try:
                monitor_report = monitor.generate_report()
                report.append(monitor_report)
            except:
                report.append("⚠️ 无法获取监控报告")
        
        return "\n".join(report)


# 测试函数
def test_optimization_logic():
    """测试优化逻辑"""
    bot = FullyOptimizedAuberonBot()
    
    test_cases = [
        "搜索今天的天气",
        "写一个Python函数",
        "什么是人工智能",
        "分析市场趋势",
        "简单查询测试"
    ]
    
    print("🧪 测试优化逻辑:")
    for query in test_cases:
        category, model_name, _, reason = bot.analyze_and_select(query)
        print(f"  '{query[:20]}...' → {category} → {model_name} ({reason})")


if __name__ == "__main__":
    # 测试逻辑
    test_optimization_logic()
    
    print("\n" + "="*70)
    print("要启动完全优化版 Bot，请运行:")
    print("python3 -c \"")
    print("from fully_optimized_bot import FullyOptimizedAuberonBot")
    print("import asyncio")
    print("asyncio.run(FullyOptimizedAuberonBot().start())")
    print("\"")
    print("="*70)
