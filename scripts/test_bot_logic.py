#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试 Bot 的消息处理逻辑
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/scripts')

# 导入 Bot 的消息处理函数
try:
    # 创建一个简化的测试环境
    from auberon_smart_bot import SmartModelBot
    print("✅ 成功导入 SmartModelBot")
    
    # 创建实例
    bot = SmartModelBot()
    
    # 测试任务分析
    test_messages = [
        "你好，测试一下",
        "搜索今天的天气",
        "写一个简单的Python函数",
        "浏览一下moltbook论坛",
        "发一个关于AI的帖子"
    ]
    
    print("\n🔍 测试任务分析:")
    for msg in test_messages:
        analysis = bot.analyze_task(msg)
        print(f"  '{msg[:20]}...' → {analysis['category']} ({analysis['reason']})")
    
    print("\n🤖 测试模型选择:")
    for category in ["cheap", "premium", "moltbook_browse", "moltbook_post"]:
        try:
            model_name, model_config = bot.select_model(category)
            print(f"  {category} → {model_name}")
        except:
            print(f"  {category} → 选择失败")
    
    print("\n✅ Bot 核心逻辑测试完成")
    
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
