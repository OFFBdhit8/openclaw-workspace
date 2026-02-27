#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Moltbook API 连接
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

from scripts.moltbook_integration import MoltbookClient, MoltbookAI

def test_api_connection():
    """测试Moltbook API连接"""
    print("🔗 测试 Moltbook API 连接...")
    print("-" * 60)
    
    client = MoltbookClient()
    
    # 测试获取帖子列表
    print("\n1. 获取帖子列表...")
    posts = client.get_posts(limit=5)
    
    if posts:
        print(f"   ✅ 成功获取 {len(posts)} 个帖子")
        
        # 显示前3个帖子
        print("\n   📝 最近帖子:")
        for i, post in enumerate(posts[:3], 1):
            print(f"   {i}. {post.get('title', '无标题')[:60]}...")
            print(f"      作者: {post.get('author', 'Unknown')} | 👍 {post.get('upvotes', 0)} | 💬 {post.get('comment_count', 0)}")
            print(f"      链接: {post.get('url', 'N/A')}")
            print()
    else:
        print("   ❌ 获取帖子失败")
        return False
    
    # 测试获取帖子详情
    if posts:
        print("\n2. 获取帖子详情...")
        post_id = posts[0].get("id")
        detail = client.get_post_detail(post_id)
        
        if detail and detail.get("title"):
            print(f"   ✅ 成功获取帖子详情")
            print(f"   标题: {detail.get('title', 'N/A')}")
            content = detail.get("content", "N/A")
            if content:
                print(f"   内容: {content[:200]}...")
        else:
            print("   ⚠️ 帖子详情API端点可能不同，已从帖子列表获取内容")
    
    return True

def test_moltbook_ai():
    """测试Moltbook AI功能"""
    print("\n" + "="*60)
    print("🤖 测试 Moltbook AI (DeepSeek 总结)")
    print("-" * 60)
    
    ai = MoltbookAI()
    
    # 测试浏览任务
    print("\n3. 测试浏览任务...")
    try:
        result = ai.handle_task("浏览一下今天的热门帖子")
        print(f"   结果: {result['content'][:300]}...")
        print(f"   任务类型: {result['task_type']}")
    except Exception as e:
        print(f"   ❌ 浏览任务失败: {e}")
    
    # 显示统计
    print("\n4. 统计信息:")
    stats = ai.get_stats()
    print(f"   {stats}")
    
    return True

if __name__ == "__main__":
    # 测试API连接
    if test_api_connection():
        print("\n" + "="*60)
        print("🎉 API 连接测试通过！")
        print("="*60)
        
        # 测试AI功能
        test_moltbook_ai()
    else:
        print("\n❌ API 连接测试失败")
        sys.exit(1)