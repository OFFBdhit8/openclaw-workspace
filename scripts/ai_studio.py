#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Studio - 多 Agent 协作系统
Auberon 作为总控，协调多个专业 Agent 协同工作
"""

import os
import sys
import json
import asyncio
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Callable

# 添加 x-tweet-fetcher 到路径
sys.path.insert(0, '/root/.openclaw/workspace/x-tweet-fetcher')

# ============ Agent 配置 ============

AGENTS = {
    "coordinator": {
        "name": "Auberon",
        "role": "总控/CEO",
        "model": "auto",  # 智能选择
        "description": "任务分配、结果汇总、协调沟通",
        "emoji": "👔"
    },
    "analyst": {
        "name": "Deepseek-Analyst",
        "role": "深度分析师",
        "model": "Deepseek",
        "description": "复杂分析、代码编程、策略规划、深度推理",
        "emoji": "🔬",
        "keywords": ["分析", "代码", "编程", "策略", "深度", "研究", "优化", "算法"]
    },
    "creative": {
        "name": "Kimi-Creative",
        "role": "创意总监",
        "model": "Kimi",
        "description": "写作创作、文案生成、头脑风暴、长文撰写",
        "emoji": "🎨",
        "keywords": ["写", "创作", "文案", "故事", "文章", "邮件", "帖子", "生成"]
    },
    "researcher": {
        "name": "Qwen-Researcher",
        "role": "研究员",
        "model": "Qwen",
        "description": "快速查询、资料搜索、翻译、信息检索",
        "emoji": "⚡",
        "keywords": ["搜索", "查询", "查找", "翻译", "是什么", "在哪里", "资料"]
    },
    "general": {
        "name": "Hunyuan-General",
        "role": "通用助手",
        "model": "腾讯混元",
        "description": "日常对话、通用任务、协调支持",
        "emoji": "🌐",
        "keywords": ["通用", "日常", "帮助", "协助"]
    }
}

# ============ 工具集成 ============

class Tools:
    """外部工具集成"""
    
    @staticmethod
    def fetch_tweet(url: str) -> Dict:
        """获取推文内容"""
        try:
            result = subprocess.run(
                ['python3', '/root/.openclaw/workspace/x-tweet-fetcher/scripts/fetch_tweet.py', 
                 '--url', url, '--pretty'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return json.loads(result.stdout)
            return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}}
    
    @staticmethod
    def search_wechat(keyword: str, limit: int = 10) -> List[Dict]:
        """搜索微信公众号文章"""
        try:
            result = subprocess.run(
                ['python3', '/root/.openclaw/workspace/x-tweet-fetcher/scripts/sogou_wechat.py',
                 '--keyword', keyword, '--limit', str(limit), '--json'],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 and result.stdout:
                return json.loads(result.stdout)
            return []
        except Exception as e:
            return [{"error": str(e)}]
    
    @staticmethod
    def discover_tweets(keywords: List[str], limit: int = 5) -> Dict:
        """发现推文"""
        try:
            result = subprocess.run(
                ['python3', '/root/.openclaw/workspace/x-tweet-fetcher/scripts/x_discover.py',
                 '--keywords', ','.join(keywords), '--limit', str(limit), '--json'],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0 and result.stdout:
                return json.loads(result.stdout)
            return {"error": result.stderr}
        except Exception as e:
            return {"error": str(e)}}

# ============ 多 Agent 协作系统 ============

class AIStudio:
    """AI 工作室 - 多 Agent 协作"""
    
    def __init__(self):
        self.agents = AGENTS
        self.tools = Tools()
        self.task_history = []
        
    def analyze_task(self, task: str) -> Dict:
        """
        分析任务，确定：
        1. 需要哪些 Agent
        2. 是否需要外部工具
        3. 执行顺序
        """
        task_lower = task.lower()
        
        # 检测是否需要工具
        needs_tools = {
            "fetch_tweet": any(kw in task_lower for kw in ["推文", "tweet", "x.com", "twitter"]),
            "search_wechat": any(kw in task_lower for kw in ["微信", "公众号", "文章"]),
            "discover": any(kw in task_lower for kw in ["发现", " trending", "热门"])
        }
        
        # 检测需要的 Agent
        required_agents = []
        
        for agent_id, agent in self.agents.items():
            if agent_id == "coordinator":
                continue
            
            # 检查关键词匹配
            match_score = sum(1 for kw in agent["keywords"] if kw in task_lower)
            if match_score > 0:
                required_agents.append({
                    "id": agent_id,
                    "name": agent["name"],
                    "score": match_score,
                    "role": agent["role"]
                })
        
        # 按匹配度排序
        required_agents.sort(key=lambda x: x["score"], reverse=True)
        
        # 如果只有一个简单任务，只用一个 Agent
        # 如果涉及多个方面，使用多个 Agent
        if len(required_agents) == 0:
            required_agents = [{"id": "general", "name": "Hunyuan-General", "role": "通用助手"}]
        elif len(required_agents) > 3:
            required_agents = required_agents[:3]  # 最多 3 个 Agent
        
        return {
            "primary_agent": required_agents[0] if required_agents else None,
            "supporting_agents": required_agents[1:] if len(required_agents) > 1 else [],
            "needs_tools": {k: v for k, v in needs_tools.items() if v},
            "complexity": "complex" if len(required_agents) > 1 or any(needs_tools.values()) else "simple"
        }
    
    async def execute_task(self, task: str, user_id: str = None) -> Dict:
        """
        执行任务（协作模式）
        """
        print(f"\n{'='*70}")
        print(f"🏢 AI Studio - 任务接收")
        print(f"{'='*70}")
        print(f"📝 任务: {task[:80]}...")
        print()
        
        # 1. 任务分析
        analysis = self.analyze_task(task)
        print(f"📊 任务分析:")
        print(f"   复杂度: {analysis['complexity']}")
        print(f"   主 Agent: {analysis['primary_agent']['name'] if analysis['primary_agent'] else 'N/A'}")
        if analysis['supporting_agents']:
            print(f"   协助 Agent: {', '.join(a['name'] for a in analysis['supporting_agents'])}")
        if analysis['needs_tools']:
            print(f"   需要工具: {', '.join(analysis['needs_tools'].keys())}")
        print()
        
        # 2. 执行工具（如果需要）
        tool_results = {}
        if analysis['needs_tools']:
            print(f"🔧 执行工具:")
            if 'fetch_tweet' in analysis['needs_tools']:
                # 提取 URL
                import re
                urls = re.findall(r'https?://(?:x\.com|twitter\.com)/\S+', task)
                if urls:
                    print(f"   获取推文: {urls[0]}")
                    tool_results['tweet'] = self.tools.fetch_tweet(urls[0])
            
            if 'search_wechat' in analysis['needs_tools']:
                # 提取关键词
                keyword = task.replace("搜索", "").replace("微信", "").replace("公众号", "").strip()
                print(f"   搜索微信: {keyword}")
                tool_results['wechat'] = self.tools.search_wechat(keyword)
            print()
        
        # 3. 分配 Agent 执行任务
        results = {
            "task": task,
            "analysis": analysis,
            "tool_results": tool_results,
            "agent_results": [],
            "final_output": None
        }
        
        print(f"🤖 Agent 协作:")
        
        # 主 Agent 执行
        primary = analysis['primary_agent']
        if primary:
            print(f"   {primary['name']} ({primary['role']}) 正在处理...")
            # 这里调用实际的模型 API
            # 暂时用模拟结果
            agent_result = {
                "agent": primary['name'],
                "status": "completed",
                "output": f"[{primary['name']}] 已完成任务分析..."
            }
            results['agent_results'].append(agent_result)
        
        # 协助 Agent 执行
        for agent in analysis['supporting_agents']:
            print(f"   {agent['name']} ({agent['role']}) 正在协助...")
            agent_result = {
                "agent": agent['name'],
                "status": "completed",
                "output": f"[{agent['name']}] 已提供支持..."
            }
            results['agent_results'].append(agent_result)
        
        # 4. 汇总结果
        print()
        print(f"📋 结果汇总:")
        final_output = self.summarize_results(results)
        results['final_output'] = final_output
        
        # 记录历史
        self.task_history.append({
            "time": datetime.now().isoformat(),
            "task": task[:50],
            "agents": [r['agent'] for r in results['agent_results']],
            "tools_used": list(analysis['needs_tools'].keys())
        })
        
        return results
    
    def summarize_results(self, results: Dict) -> str:
        """汇总所有 Agent 的结果"""
        output = []
        output.append("=" * 70)
        output.append("🎯 任务完成报告")
        output.append("=" * 70)
        output.append("")
        
        # 工具结果
        if results['tool_results']:
            output.append("📊 数据收集:")
            for tool, data in results['tool_results'].items():
                if 'error' not in data:
                    output.append(f"  ✅ {tool}: 成功")
                else:
                    output.append(f"  ⚠️ {tool}: {data['error']}")
            output.append("")
        
        # Agent 结果
        output.append("🤖 Agent 工作:")
        for result in results['agent_results']:
            output.append(f"  • {result['agent']}: {result['output']}")
        output.append("")
        
        output.append("💡 最终结果:")
        output.append("  [这里是整合后的最终回答]")
        output.append("")
        
        return "\n".join(output)
    
    def get_stats(self) -> Dict:
        """获取使用统计"""
        return {
            "total_tasks": len(self.task_history),
            "recent_tasks": self.task_history[-5:] if self.task_history else [],
            "agents_used": list(set(agent for task in self.task_history for agent in task['agents']))
        }


# ============ 命令行接口 ============

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Studio - 多 Agent 协作系统")
    parser.add_argument("--task", "-t", type=str, required=True, help="任务描述")
    parser.add_argument("--agent", "-a", type=str, help="指定单个 Agent")
    parser.add_argument("--tools", action="store_true", help="使用外部工具")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    
    args = parser.parse_args()
    
    studio = AIStudio()
    
    if args.stats:
        print(json.dumps(studio.get_stats(), indent=2, ensure_ascii=False))
        return
    
    # 运行任务
    result = asyncio.run(studio.execute_task(args.task))
    
    print(result['final_output'])

if __name__ == "__main__":
    main()
