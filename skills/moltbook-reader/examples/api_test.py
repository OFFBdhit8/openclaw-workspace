#!/usr/bin/env python3
"""
Moltbook API测试脚本
验证API连接、数据格式、链接构造等功能
"""

import sys
import json
from pathlib import Path

# 添加父目录到路径以便导入
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from moltbook_reader import MoltbookReader

def test_api_connection():
    """测试API连接"""
    print("🔍 测试Moltbook API连接...")
    
    reader = MoltbookReader()
    posts = reader.fetch_posts(limit=1)
    
    if not posts:
        print("❌ API连接失败")
        return False
    
    print(f"✅ API连接成功，获取到{len(posts)}个帖子")
    print(f"   第一个帖子标题: {posts[0].get('title', '无标题')[:50]}...")
    return True

def test_link_format():
    """测试链接格式"""
    print("\n🔗 测试链接格式...")
    
    reader = MoltbookReader()
    posts = reader.fetch_posts(limit=1)
    
    if not posts:
        print("❌ 无法获取帖子测试链接")
        return False
    
    post = posts[0]
    post_id = post.get("id")
    link = reader.construct_link(post_id)
    
    print(f"✅ 帖子ID: {post_id}")
    print(f"   生成的链接: {link}")
    print(f"   验证格式: {'✅ 正确' if link == f'https://moltbook.com/post/{post_id}' else '❌ 错误'}")
    
    # 检查是否包含/posts/（错误的复数格式）
    if "/posts/" in link:
        print("   ⚠️  警告：链接包含/posts/（复数格式），应为/post/（单数格式）")
        return False
    
    return True

def test_summary_extraction():
    """测试摘要提取"""
    print("\n📝 测试摘要提取...")
    
    reader = MoltbookReader()
    posts = reader.fetch_posts(limit=1)
    
    if not posts:
        print("❌ 无法获取帖子测试摘要")
        return False
    
    post = posts[0]
    content = post.get("content", "")
    summary = reader.extract_summary(content, max_chars=100)
    
    print(f"✅ 原始内容长度: {len(content)} 字符")
    print(f"   提取摘要长度: {len(summary)} 字符")
    print(f"   摘要预览: {summary[:80]}...")
    
    return True

def test_output_formats():
    """测试输出格式"""
    print("\n📋 测试输出格式...")
    
    reader = MoltbookReader()
    posts = reader.fetch_posts(limit=2)
    
    if len(posts) < 2:
        print("❌ 需要至少2个帖子测试格式")
        return False
    
    print("--- L1格式输出 ---")
    l1_output = reader.format_l1(posts)
    print(l1_output)
    
    print("\n--- L2格式输出 ---")
    l2_output = reader.format_l2(posts)
    print(l2_output)
    
    print("\n--- 原始数据输出 ---")
    raw_output = reader.format_raw(posts)
    print(json.dumps(json.loads(raw_output), indent=2, ensure_ascii=False))
    
    return True

def test_cache_functionality():
    """测试缓存功能"""
    print("\n💾 测试缓存功能...")
    
    reader = MoltbookReader()
    
    # 清除旧缓存
    cache_dir = Path("test_cache")
    if cache_dir.exists():
        import shutil
        shutil.rmtree(cache_dir)
    
    # 获取并缓存帖子
    posts = reader.fetch_posts(limit=1)
    if not posts:
        print("❌ 无法获取帖子测试缓存")
        return False
    
    cache_file = reader.save_cache(posts, "test_cache")
    print(f"✅ 缓存保存到: {cache_file}")
    
    # 加载缓存
    cached_posts = reader.load_latest_cache("test_cache")
    if cached_posts and len(cached_posts) > 0:
        print(f"✅ 缓存加载成功，{len(cached_posts)}个帖子")
        print(f"   缓存帖子标题: {cached_posts[0].get('title', '无标题')[:50]}...")
    else:
        print("❌ 缓存加载失败")
        return False
    
    # 清理测试缓存
    if cache_dir.exists():
        shutil.rmtree(cache_dir)
    
    return True

def main():
    """主测试函数"""
    print("🧪 Moltbook Reader 功能测试")
    print("=" * 50)
    
    tests = [
        ("API连接", test_api_connection),
        ("链接格式", test_link_format),
        ("摘要提取", test_summary_extraction),
        ("输出格式", test_output_formats),
        ("缓存功能", test_cache_functionality)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success, ""))
        except Exception as e:
            results.append((test_name, False, str(e)))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    all_passed = True
    for test_name, success, error in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name}: {status}")
        if error:
            print(f"    错误: {error}")
        if not success:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！技能可以正常使用。")
        print("\n下一步:")
        print("1. 运行: python moltbook_reader.py --mode l2 --limit 3")
        print("2. 创建cron任务（参考examples/cron_example.json）")
        print("3. 集成到OpenClaw技能系统")
    else:
        print("⚠️  部分测试失败，请检查API密钥和网络连接")
        print("\n常见问题:")
        print("1. 检查API密钥是否正确")
        print("2. 检查网络连接")
        print("3. 检查Moltbook API状态")
        print("4. 查看详细错误信息")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())