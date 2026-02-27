#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auberon 优化版 Bot - 简化测试版
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

import requests
import json
import time

# 配置
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
        }
    },
    "premium": {
        "Deepseek": {
            "api_key": "sk-7c004758529f45c6ac42ec3e620c088d",
            "api_url": "https://api.deepseek.com/v1/chat/completions",
            "model_name": "deepseek-chat",
            "cost_level": "premium",
            "max_tokens": 2000
        }
    }
}

class SimpleOptimizedBot:
    """简化版优化 Bot"""
    
    def __init__(self):
        self.stats = {
            "total_requests": 0,
            "cheap_used": 0,
            "premium_used": 0,
            "searches": 0
        }
    
    def brave_search(self, query: str) -> list:
        """Brave 搜索"""
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": BRAVE_API_KEY
        }
        
        params = {
            "q": query,
            "count": 2,
            "country": "US",
            "search_lang": "en"
        }
        
        try:
            response = requests.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('web', {}).get('results', [])
                self.stats["searches"] += 1
                return results[:2]
            return []
        except Exception as e:
            print(f"搜索失败: {e}")
            return []
    
    def analyze_task(self, prompt: str) -> str:
        """分析任务"""
        prompt_lower = prompt.lower()
        
        # 简单任务关键词
        simple_keywords = ["搜索", "查找", "查询", "天气", "时间", "是什么", "在哪里"]
        
        # 复杂任务关键词
        complex_keywords = ["分析", "写", "创作", "代码", "编程", "解释", "为什么"]
        
        simple_score = sum(1 for kw in simple_keywords if kw in prompt_lower)
        complex_score = sum(1 for kw in complex_keywords if kw in prompt_lower)
        
        if complex_score > simple_score:
            return "premium"
        else:
            return "cheap"
    
    def call_model(self, model_config: dict, prompt: str, search_results: list = None) -> str:
        """调用模型"""
        headers = {
            "Authorization": f"Bearer {model_config['api_key']}",
            "Content-Type": "application/json"
        }
        
        # 构建提示
        user_content = prompt
        if search_results:
            results_text = "\n".join([
                f"{i+1}. {r.get('title', 'No title')}"
                for i, r in enumerate(search_results)
            ])
            user_content = f"查询: {prompt}\n\n搜索结果:\n{results_text}\n\n请回答。"
        
        # 系统消息
        if model_config['cost_level'] == 'cheap':
            system_msg = "简洁回答，50字以内。"
        else:
            system_msg = "详细回答。"
        
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
            response = requests.post(
                model_config["api_url"],
                headers=headers,
                json=data,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # 优化：便宜模型精简回复
                if model_config['cost_level'] == 'cheap' and len(content) > 100:
                    content = content[:100] + "..."
                
                return content
            else:
                return f"API错误: HTTP {response.status_code}"
        except Exception as e:
            return f"请求失败: {e}"
    
    def process_query(self, query: str) -> dict:
        """处理查询"""
        self.stats["total_requests"] += 1
        
        print(f"\n🔍 处理查询: {query}")
        
        # 分析任务
        task_type = self.analyze_task(query)
        print(f"📊 任务类型: {task_type}")
        
        # 选择模型
        if task_type == "cheap":
            model_name = "Minimax"
            model_config = MODELS["cheap"]["Minimax"]
            self.stats["cheap_used"] += 1
        else:
            model_name = "Deepseek"
            model_config = MODELS["premium"]["Deepseek"]
            self.stats["premium_used"] += 1
        
        print(f"🤖 选择模型: {model_name}")
        
        # 检查是否需要搜索
        needs_search = any(kw in query.lower() for kw in ["搜索", "查找", "查询"])
        search_results = []
        
        if needs_search:
            print("🌐 执行搜索...")
            search_results = self.brave_search(query)
            print(f"📊 找到 {len(search_results)} 个结果")
        
        # 调用模型
        response = self.call_model(model_config, query, search_results)
        
        return {
            "query": query,
            "task_type": task_type,
            "model": model_name,
            "searched": needs_search,
            "response": response,
            "stats": self.get_stats()
        }
    
    def get_stats(self) -> dict:
        """获取统计"""
        total = self.stats["total_requests"]
        if total == 0:
            return {"message": "暂无请求"}
        
        cheap_percent = self.stats["cheap_used"] / total * 100
        premium_percent = self.stats["premium_used"] / total * 100
        
        return {
            "total_requests": total,
            "cheap_usage": f"{cheap_percent:.1f}%",
            "premium_usage": f"{premium_percent:.1f}%",
            "searches": self.stats["searches"],
            "estimated_savings": f"约 {cheap_percent * 0.7:.1f}%"
        }


# 测试
if __name__ == "__main__":
    bot = SimpleOptimizedBot()
    
    test_queries = [
        "搜索今天的天气",
        "写一个Python函数计算斐波那契数列",
        "什么是人工智能",
        "分析比特币价格趋势"
    ]
    
    print("="*60)
    print("🧪 测试优化版 Bot")
    print("="*60)
    
    for query in test_queries:
        result = bot.process_query(query)
        print(f"\n📝 查询: {query}")
        print(f"💰 类型: {result['task_type']}")
        print(f"🤖 模型: {result['model']}")
        print(f"🔍 搜索: {'是' if result['searched'] else '否'}")
        print(f"💬 响应: {result['response'][:80]}...")
        print("-"*40)
    
    print("\n" + "="*60)
    print("📊 最终统计:")
    stats = bot.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n✅ 测试完成!")
    print("💡 这个简化版展示了:")
    print("  1. 智能任务分析")
    print("  2. 自动模型选择")
    print("  3. Brave搜索集成")
    print("  4. Token优化")
    print("  5. 使用统计")
