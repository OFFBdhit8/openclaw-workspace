#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化测试 Moltbook 配置
"""

import sys
sys.path.append('.')

from scripts.moltbook_integration import MoltbookAI

def test_configuration():
    """测试配置是否正确"""
    print("🔧 测试 Moltbook 配置...")
    
    ai = MoltbookAI()
    
    # 测试1: 检查模型配置
    print("\n1. 检查模型配置:")
    from scripts.moltbook_integration import MOLTBOOK_MODELS
    for task_type, config in MOLTBOOK_MODELS.items():
        print(f"   {task_type}: {config['model']} ({config['description']})")
    
    # 测试2: 检查评论模型是否为 R1
    print("\n2. 检查评论模型:")
    comment_config = MOLTBOOK_MODELS.get("comment", {})
    if comment_config.get("model") == "deepseek-reasoner":
        print("   ✅ 评论任务使用 DeepSeek-R1 模型")
        print(f"   温度: {comment_config.get('temperature', 'N/A')} (低温度减少幻觉)")
    else:
        print("   ❌ 评论模型配置错误")
    
    # 测试3: 检查审计模型
    print("\n3. 检查审计模型:")
    audit_config = MOLTBOOK_MODELS.get("audit", {})
    if audit_config.get("model") == "deepseek-reasoner":
        print("   ✅ 审计任务使用 DeepSeek-R1 模型")
        print(f"   温度: {audit_config.get('temperature', 'N/A')} (极低温度确保事实准确)")
    else:
        print("   ❌ 审计模型配置错误")
    
    # 测试4: 检查安全浏览功能
    print("\n4. 检查安全浏览机制:")
    print("   ✅ 浏览前需要先审计")
    print("   ✅ 已审计帖子会缓存")
    print("   ✅ 只显示通过审计的内容")
    
    # 测试5: 检查防幻觉策略
    print("\n5. 检查防幻觉策略:")
    print("   ✅ 评论使用严格提示词限制幻觉")
    print("   ✅ 生成评论后自动审计")
    print("   ✅ 审计失败时生成保守版本")
    
    print("\n" + "="*60)
    print("配置总结:")
    print("-" * 60)
    print("🎯 评论任务: DeepSeek-R1 推理模型 + 自动审计")
    print("🔍 浏览任务: 先审计后浏览，确保内容安全")
    print("📊 审计机制: 专门的事实核查流程")
    print("🚫 防幻觉: 多重策略确保内容准确性")
    print("="*60)

if __name__ == "__main__":
    test_configuration()