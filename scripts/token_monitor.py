#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 使用监控系统
记录和分析模型使用情况，优化成本
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path

class TokenMonitor:
    """Token 使用监控"""
    
    def __init__(self, data_file="token_usage.json"):
        self.data_file = Path("/root/.openclaw/workspace/data") / data_file
        self.data_file.parent.mkdir(exist_ok=True)
        
        # 模型成本配置（相对成本）
        self.model_costs = {
            "deepseek-chat": 1.0,
            "moonshot-v1-8k": 1.2,
            "abab6.5-chat": 0.3,
            "hunyuan-standard": 0.4,
            "qwen-turbo": 0.5
        }
        
        # 加载现有数据
        self.data = self.load_data()
    
    def load_data(self):
        """加载数据"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 默认数据结构
        return {
            "daily_stats": {},
            "model_usage": {},
            "cost_savings": {
                "total_saved": 0,
                "cheap_usage_percent": 0,
                "estimated_savings": 0
            },
            "last_updated": None
        }
    
    def save_data(self):
        """保存数据"""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def record_usage(self, model: str, tokens_in: int, tokens_out: int, task_type: str = "general"):
        """记录使用情况"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 初始化数据结构
        if today not in self.data["daily_stats"]:
            self.data["daily_stats"][today] = {
                "total_tokens": 0,
                "total_requests": 0,
                "cheap_requests": 0,
                "premium_requests": 0,
                "search_requests": 0
            }
        
        if model not in self.data["model_usage"]:
            self.data["model_usage"][model] = {
                "total_tokens": 0,
                "total_requests": 0,
                "last_used": None
            }
        
        # 更新统计
        total_tokens = tokens_in + tokens_out
        
        # 每日统计
        daily = self.data["daily_stats"][today]
        daily["total_tokens"] += total_tokens
        daily["total_requests"] += 1
        
        # 判断任务类型
        is_cheap = self.model_costs.get(model, 1.0) < 0.6
        if is_cheap:
            daily["cheap_requests"] += 1
        else:
            daily["premium_requests"] += 1
        
        if task_type == "search":
            daily["search_requests"] += 1
        
        # 模型统计
        model_stats = self.data["model_usage"][model]
        model_stats["total_tokens"] += total_tokens
        model_stats["total_requests"] += 1
        model_stats["last_used"] = datetime.now().isoformat()
        
        # 计算节省
        self.calculate_savings()
        
        # 保存数据
        self.save_data()
        
        return {
            "date": today,
            "model": model,
            "tokens": total_tokens,
            "task_type": task_type,
            "is_cheap": is_cheap
        }
    
    def calculate_savings(self):
        """计算节省的成本"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.data["daily_stats"]:
            return
        
        daily = self.data["daily_stats"][today]
        total_requests = daily["total_requests"]
        
        if total_requests == 0:
            return
        
        # 计算便宜模型使用比例
        cheap_percent = daily["cheap_requests"] / total_requests * 100
        
        # 估算节省（假设便宜模型节省70%成本）
        estimated_savings = cheap_percent * 0.7
        
        # 更新节省数据
        self.data["cost_savings"] = {
            "total_saved": self.data["cost_savings"].get("total_saved", 0) + estimated_savings,
            "cheap_usage_percent": cheap_percent,
            "estimated_savings": estimated_savings,
            "last_calculated": datetime.now().isoformat()
        }
    
    def get_daily_report(self, date: str = None) -> dict:
        """获取每日报告"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        if date not in self.data["daily_stats"]:
            return {"error": f"没有 {date} 的数据"}
        
        daily = self.data["daily_stats"][date]
        total = daily["total_requests"]
        
        if total == 0:
            return {"message": f"{date} 没有请求记录"}
        
        cheap_percent = daily["cheap_requests"] / total * 100
        premium_percent = daily["premium_requests"] / total * 100
        
        return {
            "date": date,
            "total_requests": total,
            "total_tokens": daily["total_tokens"],
            "cheap_requests": daily["cheap_requests"],
            "premium_requests": daily["premium_requests"],
            "search_requests": daily["search_requests"],
            "cheap_usage_percent": f"{cheap_percent:.1f}%",
            "premium_usage_percent": f"{premium_percent:.1f}%",
            "estimated_savings": f"{cheap_percent * 0.7:.1f}%"
        }
    
    def get_model_ranking(self) -> list:
        """获取模型使用排名"""
        models = []
        for model, stats in self.data["model_usage"].items():
            models.append({
                "model": model,
                "requests": stats["total_requests"],
                "tokens": stats["total_tokens"],
                "last_used": stats["last_used"],
                "cost_level": "cheap" if self.model_costs.get(model, 1.0) < 0.6 else "premium"
            })
        
        # 按请求数排序
        models.sort(key=lambda x: x["requests"], reverse=True)
        return models
    
    def get_recommendations(self) -> dict:
        """获取优化建议"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.data["daily_stats"]:
            return {"message": "今天还没有数据"}
        
        daily = self.data["daily_stats"][today]
        total = daily["total_requests"]
        
        if total == 0:
            return {"message": "今天还没有请求"}
        
        cheap_percent = daily["cheap_requests"] / total * 100
        
        recommendations = []
        
        if cheap_percent < 60:
            recommendations.append({
                "type": "cost_optimization",
                "priority": "high",
                "message": f"便宜模型使用率只有 {cheap_percent:.1f}%，建议增加简单任务使用便宜模型",
                "suggestion": "优化任务分类算法，将更多简单任务路由到便宜模型"
            })
        
        if daily["search_requests"] == 0:
            recommendations.append({
                "type": "feature_usage",
                "priority": "medium",
                "message": "今天还没有使用搜索功能",
                "suggestion": "考虑在查询中增加搜索关键词以利用Brave搜索"
            })
        
        # 检查模型使用分布
        model_ranking = self.get_model_ranking()
        if len(model_ranking) > 0:
            top_model = model_ranking[0]
            if top_model["cost_level"] == "premium" and top_model["requests"] > total * 0.5:
                recommendations.append({
                    "type": "model_balance",
                    "priority": "medium",
                    "message": f"{top_model['model']} 使用过于频繁 ({top_model['requests']}/{total} 请求)",
                    "suggestion": "考虑将部分任务分流到其他模型"
                })
        
        return {
            "date": today,
            "total_requests": total,
            "cheap_usage_percent": cheap_percent,
            "recommendations": recommendations,
            "recommendation_count": len(recommendations)
        }
    
    def generate_report(self) -> str:
        """生成文本报告"""
        today = datetime.now().strftime("%Y-%m-%d")
        daily_report = self.get_daily_report(today)
        
        if "error" in daily_report:
            return f"📊 Token 使用监控\n\n今天还没有数据记录。"
        
        model_ranking = self.get_model_ranking()
        recommendations = self.get_recommendations()
        
        report_lines = [
            "📊 Token 使用监控报告",
            "=" * 40,
            f"📅 日期: {today}",
            f"📈 总请求数: {daily_report['total_requests']}",
            f"🔢 总Token数: {daily_report['total_tokens']:,}",
            f"💰 便宜模型使用率: {daily_report['cheap_usage_percent']}",
            f"💎 贵模型使用率: {daily_report['premium_usage_percent']}",
            f"🌐 搜索请求: {daily_report['search_requests']}",
            f"💵 预估节省: {daily_report['estimated_savings']}",
            "",
            "🏆 模型使用排名:"
        ]
        
        for i, model in enumerate(model_ranking[:5], 1):
            report_lines.append(f"  {i}. {model['model']} - {model['requests']} 请求 ({model['cost_level']})")
        
        if recommendations.get("recommendation_count", 0) > 0:
            report_lines.extend([
                "",
                "💡 优化建议:"
            ])
            
            for i, rec in enumerate(recommendations["recommendations"], 1):
                report_lines.append(f"  {i}. [{rec['priority'].upper()}] {rec['message']}")
        
        report_lines.extend([
            "",
            "=" * 40,
            "✅ 监控系统运行正常"
        ])
        
        return "\n".join(report_lines)


# 测试
if __name__ == "__main__":
    monitor = TokenMonitor()
    
    print("🧪 测试 Token 监控系统")
    print("="*60)
    
    # 模拟一些使用记录
    test_records = [
        ("abab6.5-chat", 100, 50, "search"),
        ("deepseek-chat", 200, 150, "analysis"),
        ("abab6.5-chat", 80, 40, "general"),
        ("moonshot-v1-8k", 300, 200, "writing"),
        ("qwen-turbo", 120, 60, "search")
    ]
    
    print("📝 记录测试数据...")
    for model, tokens_in, tokens_out, task_type in test_records:
        record = monitor.record_usage(model, tokens_in, tokens_out, task_type)
        print(f"  记录: {model} - {tokens_in+tokens_out} tokens ({task_type})")
    
    print("\n📊 生成报告...")
    report = monitor.generate_report()
    print(report)
    
    print("\n💡 优化建议:")
    recommendations = monitor.get_recommendations()
    for rec in recommendations.get("recommendations", []):
        print(f"  • {rec['message']}")
    
    print("\n✅ 测试完成!")
    print(f"数据文件: {monitor.data_file}")
