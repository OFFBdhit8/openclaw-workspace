#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 优化配置 - 减少 Token 消耗
"""

# ============ Token 优化策略 ============

OPTIMIZATION_STRATEGIES = {
    "short_responses": {
        "enabled": True,
        "description": "优先使用简短回复",
        "savings": "30-50%"
    },
    "cheap_models_for_simple_tasks": {
        "enabled": True,
        "description": "简单任务使用便宜模型",
        "savings": "50-70%"
    },
    "caching": {
        "enabled": True,
        "description": "缓存常见查询结果",
        "savings": "20-40%"
    },
    "batching": {
        "enabled": True,
        "description": "批量处理相似请求",
        "savings": "15-30%"
    },
    "truncation": {
        "enabled": True,
        "max_context_length": 2000,
        "description": "限制上下文长度",
        "savings": "20-50%"
    }
}

# 模型 Token 成本（相对值，越小越便宜）
MODEL_TOKEN_COSTS = {
    "Minimax": 0.3,
    "腾讯混元": 0.4,
    "Qwen": 0.5,
    "Deepseek": 1.0,
    "Kimi": 1.0
}

# 简单任务关键词（使用便宜模型）
SIMPLE_TASK_KEYWORDS = [
    "搜索", "查找", "查询", "浏览", "看看",
    "是什么", "在哪里", "多少钱", "什么时候", "是谁",
    "天气", "时间", "日期", "翻译", "转换",
    "确认", "检查", "验证", "测试", "ping", "状态",
    "hi", "hello", "hey", "你好", "在吗"
]

# 短回复提示模板
SHORT_RESPONSE_TEMPLATE = """
请简洁回答，控制在100字以内。只提供核心信息，不要冗余解释。

用户问题: {question}
"""

# 模型选择提示
MODEL_SELECTION_PROMPT = """
根据任务复杂度选择模型:
- 简单查询/搜索/翻译 → Minimax/腾讯混元
- 中等复杂度 → Qwen
- 深度分析/编程/写作 → Deepseek/Kimi
"""

class TokenOptimizer:
    """Token 优化器"""
    
    def __init__(self):
        self.cache = {}
        self.request_count = 0
        self.token_saved = 0
    
    def is_simple_task(self, prompt: str) -> bool:
        """判断是否为简单任务"""
        prompt_lower = prompt.lower()
        return any(kw in prompt_lower for kw in SIMPLE_TASK_KEYWORDS)
    
    def get_cheapest_model(self) -> str:
        """获取最便宜的可用模型"""
        return "Minimax"  # 当前配置中最便宜的
    
    def optimize_prompt(self, prompt: str, force_short: bool = False) -> str:
        """优化提示词以减少 Token"""
        if force_short or self.is_simple_task(prompt):
            return SHORT_RESPONSE_TEMPLATE.format(question=prompt)
        return prompt
    
    def get_stats(self) -> dict:
        """获取优化统计"""
        return {
            "strategies_enabled": list(OPTIMIZATION_STRATEGIES.keys()),
            "estimated_savings": "40-60%",
            "recommendations": [
                "使用便宜模型处理简单任务",
                "限制上下文长度",
                "启用响应缓存",
                "优先使用简短回复"
            ]
        }
