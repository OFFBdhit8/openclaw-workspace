#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能模型路由器 - 根据任务类型自动选择模型
便宜模型：简单任务（搜索、浏览、快速查询）
贵模型：复杂任务（深度分析、回复、发帖、创意）
"""

import os
import re
import time
import requests
import json
from typing import Dict, List, Tuple

# ============ 模型配置 ============

# 便宜/快速模型（用于简单任务）
CHEAP_MODELS = {
    "Minimax": {
        "api_key": "sk-api-3hOqY3VgQvbmm4xhi1zZXTVfKNg0046epcuvKWriFuy9C8sM7_UOwC4IsYL_WOAYB8TD0CDc0nbKlOdLt9k-s6mMQNcmw8XQlY6xiAYYVp_jZ3CUPeBwNAM",
        "api_url": "https://api.minimax.chat/v1/text/chatcompletion",
        "model": "abab6.5-chat",
        "cost_level": "cheap",
        "speed": "fast",
        "max_tokens": 500
    },
    "腾讯混元": {
        "api_key": "sk-qv0tltkn0dztn4ghhyeBg5TnXQ58QKc0ClmAk3ogb07zNCTH",
        "api_url": "https://api.hunyuan.cloud.tencent.com/v1/chat/completions",
        "model": "hunyuan-standard",
        "cost_level": "cheap",
        "speed": "fast",
        "max_tokens": 500
    },
    "Qwen": {
        "api_key": "sk-46ecd3efbdd540af82eb4a2c763b72d6",
        "api_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "model": "qwen-turbo",
        "cost_level": "cheap",
        "speed": "fast",
        "max_tokens": 500
    }
}

# 贵/高质量模型（用于复杂任务）
PREMIUM_MODELS = {
    "Deepseek": {
        "api_key": "sk-7c004758529f45c6ac42ec3e620c088d",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "cost_level": "premium",
        "speed": "normal",
        "max_tokens": 2000
    },
    "Kimi": {
        "api_key": "sk-AeUlUSlTJR30ixssrvsksEU23TCFXEBPyg3gh1mZBSMqYu0h",
        "api_url": "https://api.moonshot.cn/v1/chat/completions",
        "model": "moonshot-v1-8k",
        "cost_level": "premium",
        "speed": "normal",
        "max_tokens": 2000
    }
}

# ============ 任务类型检测 ============

# 简单任务关键词（用便宜模型）
SIMPLE_TASKS = [
    # 搜索和浏览
    r"搜索",
    r"查找",
    r"查询",
    r"浏览",
    r"看看",
    r"有什么",
    r"列表",
    r"目录",
    # 快速问答
    r"是什么",
    r"在哪里",
    r"多少钱",
    r"什么时候",
    r"是谁",
    r"简单",
    r"快速",
    r"查一下",
    r"告诉我",
    r"(?:天气|时间|日期)",
    r"翻译",
    r"转换",
    # 简短确认
    r"确认",
    r"检查",
    r"验证",
    r"测试",
    r"ping",
    r"状态",
]

# 复杂任务关键词（用贵模型）
COMPLEX_TASKS = [
    # 深度分析
    r"分析",
    r"深度",
    r"详细",
    r"全面",
    r"研究",
    r"报告",
    r"评估",
    r"比较",
    r"对比",
    r"优劣势",
    r"策略",
    r"方案",
    r"规划",
    # 创意写作
    r"写",
    r"创作",
    r"生成",
    r"撰写",
    r"文章",
    r"故事",
    r"文案",
    r"邮件",
    r"信件",
    r"帖子",
    r"发布",
    r"发帖",
    # 回复和评论
    r"回复",
    r"评论",
    r"回答",
    r"解答",
    r"建议",
    r"推荐",
    r"评价",
    r"反馈",
    # 编程和技术
    r"代码",
    r"编程",
    r"程序",
    r"脚本",
    r"函数",
    r"算法",
    r"debug",
    r"调试",
    r"修复",
    r"优化",
    r"重构",
    # 复杂推理
    r"为什么",
    r"如何",
    r"怎么",
    r"解释",
    r"说明",
    r"推理",
    r"逻辑",
    r"思考",
    r"讨论",
    r"辩论",
]

# 简单任务最大长度（超过此长度可能是复杂任务）
SIMPLE_MAX_LENGTH = 100

class ModelRouter:
    """智能模型路由器"""
    
    def __init__(self):
        self.all_models = {**CHEAP_MODELS, **PREMIUM_MODELS}
        self.current_model = None
        self.task_history = []
    
    def analyze_task(self, prompt: str) -> Tuple[str, float, str]:
        """
        分析任务类型，返回 (模型类别, 置信度, 原因)
        """
        prompt_lower = prompt.lower()
        
        # 检查复杂任务关键词
        complex_score = 0
        complex_matches = []
        for pattern in COMPLEX_TASKS:
            if re.search(pattern, prompt_lower):
                complex_score += 1
                complex_matches.append(pattern)
        
        # 检查简单任务关键词
        simple_score = 0
        simple_matches = []
        for pattern in SIMPLE_TASKS:
            if re.search(pattern, prompt_lower):
                simple_score += 1
                simple_matches.append(pattern)
        
        # 根据长度判断
        length_factor = "neutral"
        if len(prompt) > SIMPLE_MAX_LENGTH * 2:
            length_factor = "long"
            complex_score += 1
        elif len(prompt) < SIMPLE_MAX_LENGTH:
            length_factor = "short"
            simple_score += 1
        
        # 判断任务类型
        if complex_score > simple_score:
            confidence = min(0.9, 0.5 + (complex_score - simple_score) * 0.1)
            reason = f"复杂任务关键词({len(complex_matches)}个): {', '.join(complex_matches[:3])}"
            if length_factor == "long":
                reason += ", 内容较长"
            return "premium", confidence, reason
        elif simple_score > complex_score:
            confidence = min(0.9, 0.5 + (simple_score - complex_score) * 0.1)
            reason = f"简单任务关键词({len(simple_matches)}个): {', '.join(simple_matches[:3])}"
            if length_factor == "short":
                reason += ", 内容简短"
            return "cheap", confidence, reason
        else:
            # 无法确定，默认用便宜模型
            return "cheap", 0.5, "无法明确判断，默认使用便宜模型"
    
    def select_model(self, task_type: str) -> Tuple[str, Dict]:
        """
        根据任务类型选择具体模型
        """
        if task_type == "premium":
            # 轮流使用 premium 模型（负载均衡）
            import random
            model_name = random.choice(list(PREMIUM_MODELS.keys()))
            return model_name, PREMIUM_MODELS[model_name]
        else:
            # 轮流使用 cheap 模型
            import random
            model_name = random.choice(list(CHEAP_MODELS.keys()))
            return model_name, CHEAP_MODELS[model_name]
    
    def call_model(self, model_name: str, model_config: Dict, prompt: str) -> Dict:
        """
        调用指定模型
        """
        headers = {
            "Authorization": f"Bearer {model_config['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model_config["model"],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": model_config.get("max_tokens", 500),
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
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {
                    "success": True,
                    "model": model_name,
                    "content": content,
                    "response_time": round(response_time, 2),
                    "tokens_used": result.get("usage", {}).get("total_tokens", 0)
                }
            else:
                return {
                    "success": False,
                    "model": model_name,
                    "error": f"HTTP {response.status_code}: {response.text[:100]}",
                    "response_time": round(response_time, 2)
                }
        except Exception as e:
            return {
                "success": False,
                "model": model_name,
                "error": str(e),
                "response_time": 0
            }
    
    def route_and_call(self, prompt: str, force_model: str = None) -> Dict:
        """
        智能路由并调用模型
        """
        import time
        
        # 如果强制指定模型
        if force_model:
            if force_model in self.all_models:
                model_config = self.all_models[force_model]
                result = self.call_model(force_model, model_config, prompt)
                result["routing"] = {
                    "forced": True,
                    "model": force_model
                }
                return result
            else:
                return {
                    "success": False,
                    "error": f"未知模型: {force_model}"
                }
        
        # 分析任务类型
        task_type, confidence, reason = self.analyze_task(prompt)
        
        # 选择模型
        model_name, model_config = self.select_model(task_type)
        
        # 调用模型
        result = self.call_model(model_name, model_config, prompt)
        
        # 添加路由信息
        result["routing"] = {
            "task_type": task_type,
            "confidence": confidence,
            "reason": reason,
            "selected_model": model_name,
            "forced": False
        }
        
        # 记录历史
        self.task_history.append({
            "prompt": prompt[:50],
            "task_type": task_type,
            "model": model_name,
            "success": result["success"]
        })
        
        return result
    
    def get_stats(self) -> Dict:
        """获取使用统计"""
        if not self.task_history:
            return {"message": "暂无使用记录"}
        
        total = len(self.task_history)
        cheap_count = sum(1 for t in self.task_history if t["task_type"] == "cheap")
        premium_count = sum(1 for t in self.task_history if t["task_type"] == "premium")
        success_count = sum(1 for t in self.task_history if t["success"])
        
        return {
            "total_tasks": total,
            "cheap_tasks": cheap_count,
            "premium_tasks": premium_count,
            "success_rate": f"{success_count/total*100:.1f}%",
            "cost_saving": f"约 {cheap_count/total*100:.1f}% 的任务使用便宜模型"
        }


# ============ 命令行接口 ============

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="智能模型路由器")
    parser.add_argument("--prompt", "-p", type=str, required=True, help="输入提示词")
    parser.add_argument("--model", "-m", type=str, help="强制使用指定模型 (Deepseek/Kimi/Minimax/Qwen/腾讯混元)")
    parser.add_argument("--cheap", action="store_true", help="强制使用便宜模型")
    parser.add_argument("--premium", action="store_true", help="强制使用贵模型")
    parser.add_argument("--stats", action="store_true", help="显示使用统计")
    
    args = parser.parse_args()
    
    router = ModelRouter()
    
    if args.stats:
        stats = router.get_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        return
    
    # 确定强制模型
    force_model = args.model
    if args.cheap:
        # 随机选择一个便宜模型
        import random
        force_model = random.choice(list(CHEAP_MODELS.keys()))
    elif args.premium:
        import random
        force_model = random.choice(list(PREMIUM_MODELS.keys()))
    
    print("=" * 70)
    print("🤖 智能模型路由器")
    print("=" * 70)
    print(f"📝 任务: {args.prompt[:60]}...")
    print()
    
    # 路由并调用
    result = router.route_and_call(args.prompt, force_model)
    
    # 显示路由决策
    routing = result.get("routing", {})
    if routing.get("forced"):
        print(f"⚡ 强制使用模型: {routing['model']}")
    else:
        print(f"🎯 任务分析: {routing.get('reason', 'N/A')}")
        print(f"📊 置信度: {routing.get('confidence', 0):.0%}")
        print(f"💰 模型类别: {'便宜' if routing.get('task_type') == 'cheap' else '贵'}")
        print(f"🤖 选择模型: {routing.get('selected_model', 'N/A')}")
    
    print()
    
    # 显示结果
    if result["success"]:
        print(f"✅ 调用成功 ({result.get('response_time', 0)}s)")
        print()
        print("💬 回复内容:")
        print("-" * 70)
        print(result["content"])
        print("-" * 70)
        if result.get("tokens_used"):
            print(f"📝 Token 使用量: {result['tokens_used']}")
    else:
        print(f"❌ 调用失败")
        print(f"错误: {result.get('error', 'Unknown error')}")
    
    print()

if __name__ == "__main__":
    main()
