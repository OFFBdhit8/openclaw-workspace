#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成优化模块 - 结合 Brave Search 和 Token 优化
"""

import requests
import json
import time
from typing import Dict, List, Optional

class OptimizedAssistant:
    """优化助手 - 集成搜索和Token优化"""
    
    def __init__(self):
        self.brave_api_key = "BSAo80XKa0ke0SNirZxhOZQ6urU--Ew"
        self.brave_endpoint = "https://api.search.brave.com/res/v1/web/search"
        
        # Token 优化配置
        self.token_stats = {
            "total_requests": 0,
            "cheap_model_used": 0,
            "premium_model_used": 0,
            "search_requests": 0,
            "tokens_saved": 0
        }
        
        # 模型成本映射
        self.model_costs = {
            "deepseek-chat": 1.0,
            "moonshot-v1-8k": 1.2,
            "abab6.5-chat": 0.3,
            "hunyuan-standard": 0.4,
            "qwen-turbo": 0.5
        }
    
    def brave_search(self, query: str, count: int = 5) -> List[Dict]:
        """使用 Brave Search 搜索"""
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.brave_api_key
        }
        
        params = {
            "q": query,
            "count": count,
            "country": "US",
            "search_lang": "en"
        }
        
        try:
            response = requests.get(
                self.brave_endpoint,
                headers=headers,
                params=params,
                timeout=15
            )
            
            self.token_stats["search_requests"] += 1
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('web', {}).get('results', [])
                
                # 格式化结果
                formatted_results = []
                for result in results:
                    formatted_results.append({
                        "title": result.get('title', ''),
                        "url": result.get('url', ''),
                        "description": result.get('description', ''),
                        "age": result.get('age', '')
                    })
                
                return formatted_results
            else:
                print(f"⚠️ Brave 搜索失败: HTTP {response.status_code}")
                return []
                
        except Exception as e:
            print(f"⚠️ Brave 搜索异常: {e}")
            return []
    
    def optimize_response(self, content: str, task_type: str = "general") -> str:
        """优化回复内容以减少 Token"""
        
        # 根据任务类型应用不同优化策略
        if task_type == "search_result":
            # 搜索结果：简洁总结
            if len(content) > 300:
                content = content[:300] + "..."
        
        elif task_type == "simple_query":
            # 简单查询：非常简洁
            if len(content) > 150:
                content = content[:150] + "..."
        
        elif task_type == "complex_analysis":
            # 复杂分析：保持完整但结构化
            # 添加结构化标记
            if "###" not in content and "##" not in content:
                lines = content.split('\n')
                if len(lines) > 5:
                    content = "## 分析结果\n\n" + content
        
        # 移除多余的空行和空格
        content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())
        
        return content
    
    def select_model(self, prompt: str, has_search_results: bool = False) -> Dict:
        """智能选择模型"""
        prompt_lower = prompt.lower()
        
        # 简单任务关键词
        simple_keywords = ["搜索", "查找", "查询", "是什么", "在哪里", "多少钱", "天气", "时间"]
        
        # 复杂任务关键词
        complex_keywords = ["分析", "深度", "详细", "写", "创作", "代码", "编程", "解释", "为什么"]
        
        simple_score = sum(1 for kw in simple_keywords if kw in prompt_lower)
        complex_score = sum(1 for kw in complex_keywords if kw in prompt_lower)
        
        # 如果有搜索结果，倾向于使用便宜模型总结
        if has_search_results:
            simple_score += 2
        
        # 根据分数选择模型类别
        if complex_score > simple_score:
            model_category = "premium"
            model_name = "moonshot-v1-8k"  # Kimi
            cost = self.model_costs[model_name]
        else:
            model_category = "cheap"
            # 轮询便宜模型
            cheap_models = ["abab6.5-chat", "hunyuan-standard", "qwen-turbo"]
            model_name = cheap_models[self.token_stats["total_requests"] % len(cheap_models)]
            cost = self.model_costs[model_name]
        
        # 更新统计
        self.token_stats["total_requests"] += 1
        if model_category == "cheap":
            self.token_stats["cheap_model_used"] += 1
            # 估算节省的Token（假设premium模型成本是cheap的2-3倍）
            self.token_stats["tokens_saved"] += int(cost * 1000 * 2.5)
        else:
            self.token_stats["premium_model_used"] += 1
        
        return {
            "category": model_category,
            "model": model_name,
            "cost_level": cost,
            "reason": f"复杂分: {complex_score}, 简单分: {simple_score}"
        }
    
    def process_query(self, user_query: str) -> Dict:
        """处理用户查询 - 集成搜索和优化"""
        print(f"\n🔍 处理查询: {user_query[:50]}...")
        
        # 步骤1: 判断是否需要搜索
        needs_search = any(kw in user_query.lower() for kw in 
                          ["搜索", "查找", "查询", "search", "find", "look up"])
        
        search_results = []
        if needs_search:
            print("🌐 执行 Brave 搜索...")
            search_results = self.brave_search(user_query, count=3)
            print(f"📊 找到 {len(search_results)} 个结果")
        
        # 步骤2: 选择模型
        model_info = self.select_model(user_query, has_search_results=bool(search_results))
        print(f"🤖 选择模型: {model_info['model']} ({model_info['category']})")
        
        # 步骤3: 构建提示词
        prompt = user_query
        if search_results:
            results_text = "\n".join([
                f"{i+1}. {r['title']}\n   链接: {r['url']}\n   摘要: {r['description'][:100]}..."
                for i, r in enumerate(search_results)
            ])
            prompt = f"用户查询: {user_query}\n\n搜索到的信息:\n{results_text}\n\n请基于以上信息回答。"
        
        # 步骤4: 确定任务类型
        if needs_search:
            task_type = "search_result"
        elif len(user_query) < 30:
            task_type = "simple_query"
        else:
            task_type = "general"
        
        # 这里应该调用实际的模型API
        # 为了演示，返回模拟响应
        response = f"基于查询 '{user_query}' 的分析结果。"
        
        if search_results:
            response += f"\n\n参考了 {len(search_results)} 个搜索结果。"
        
        # 步骤5: 优化响应
        optimized_response = self.optimize_response(response, task_type)
        
        return {
            "query": user_query,
            "search_performed": needs_search,
            "search_results_count": len(search_results),
            "model_selected": model_info,
            "response": optimized_response,
            "response_length": len(optimized_response),
            "stats": self.get_stats()
        }
    
    def get_stats(self) -> Dict:
        """获取优化统计"""
        total = self.token_stats["total_requests"]
        if total == 0:
            return {"message": "暂无请求记录"}
        
        cheap_percent = self.token_stats["cheap_model_used"] / total * 100
        premium_percent = self.token_stats["premium_model_used"] / total * 100
        
        return {
            "total_requests": total,
            "cheap_model_usage": f"{cheap_percent:.1f}%",
            "premium_model_usage": f"{premium_percent:.1f}%",
            "search_requests": self.token_stats["search_requests"],
            "estimated_tokens_saved": self.token_stats["tokens_saved"],
            "estimated_cost_savings": f"约 {cheap_percent * 0.7:.1f}%"  # 假设便宜模型节省70%成本
        }


# 测试
if __name__ == "__main__":
    assistant = OptimizedAssistant()
    
    # 测试搜索查询
    print("="*60)
    print("测试 1: 搜索查询")
    result = assistant.process_query("搜索 OpenClaw AI 的最新信息")
    print(f"响应: {result['response'][:100]}...")
    print(f"统计: {json.dumps(result['stats'], indent=2, ensure_ascii=False)}")
    
    print("\n" + "="*60)
    print("测试 2: 简单查询")
    result = assistant.process_query("今天的天气怎么样？")
    print(f"响应: {result['response'][:100]}...")
    
    print("\n" + "="*60)
    print("测试 3: 复杂分析")
    result = assistant.process_query("分析人工智能的未来发展趋势")
    print(f"响应: {result['response'][:100]}...")
    
    print("\n" + "="*60)
    print("最终统计:")
    stats = assistant.get_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
