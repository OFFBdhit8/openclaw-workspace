#!/usr/bin/env python3
"""
Moltbook Reader - 高效浏览Moltbook的技能
直接调用API，避免AI幻觉，大幅降低token消耗
"""

import json
import sys
import requests
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from pathlib import Path

class MoltbookReader:
    """Moltbook API阅读器"""
    
    def __init__(self, api_key: str = None, base_url: str = None):
        """
        初始化阅读器
        
        Args:
            api_key: Moltbook API密钥
            base_url: API基础URL
        """
        self.api_key = api_key or "moltbook_sk_MDQ7Y7CU2cPX_yyxf6MM9ZZpXSAXZnYr"
        self.base_url = base_url or "https://moltbook.com/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "MoltbookReader/1.0"
        })
        
    def fetch_posts(self, limit: int = 3) -> List[Dict]:
        """
        获取Moltbook帖子
        
        Args:
            limit: 获取的帖子数量
            
        Returns:
            帖子列表，每个帖子包含id, title, content等字段
        """
        try:
            url = f"{self.base_url}/posts"
            params = {"limit": limit}
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data.get("success"):
                return data.get("posts", [])
            else:
                print(f"API返回失败: {data.get('error', 'Unknown error')}", file=sys.stderr)
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"API请求失败: {e}", file=sys.stderr)
            return []
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}", file=sys.stderr)
            return []
    
    def construct_link(self, post_id: str) -> str:
        """
        构建正确的帖子链接
        
        Args:
            post_id: 帖子ID
            
        Returns:
            格式正确的链接: https://moltbook.com/post/{id}
        """
        return f"https://moltbook.com/post/{post_id}"
    
    def extract_summary(self, content: str, max_chars: int = 100) -> str:
        """
        从内容中提取摘要（简化版）
        
        Args:
            content: 原始内容
            max_chars: 摘要最大字符数
            
        Returns:
            提取的摘要
        """
        if not content:
            return ""
        
        # 简单方法：取前N个字符，在句子边界截断
        if len(content) <= max_chars:
            return content
        
        # 尝试在句子边界截断
        truncated = content[:max_chars]
        last_period = truncated.rfind('.')
        last_newline = truncated.rfind('\n')
        
        if last_period > max_chars * 0.5:  # 如果在后半部分找到句号
            return truncated[:last_period + 1]
        elif last_newline > max_chars * 0.5:  # 如果在后半部分找到换行
            return truncated[:last_newline]
        else:
            return truncated + "..."
    
    def format_l1(self, posts: List[Dict]) -> str:
        """
        格式化L1输出（标题+链接）
        
        Args:
            posts: 帖子列表
            
        Returns:
            格式化后的字符串
        """
        if not posts:
            return "🔍 未找到Moltbook帖子"
        
        output = ["🔥 Moltbook 最新帖子"]
        
        for i, post in enumerate(posts, 1):
            title = post.get("title", "无标题").strip()
            post_id = post.get("id", "")
            link = self.construct_link(post_id)
            
            # 限制标题长度
            if len(title) > 30:
                title = title[:27] + "..."
            
            output.append(f"{i}. {title} {link}")
        
        return "\n".join(output)
    
    def format_l2(self, posts: List[Dict]) -> str:
        """
        格式化L2输出（标题+核心观点+链接）
        
        Args:
            posts: 帖子列表
            
        Returns:
            格式化后的字符串
        """
        if not posts:
            return "🔍 未找到Moltbook帖子"
        
        output = ["🔥 Moltbook 今日重点"]
        
        for i, post in enumerate(posts, 1):
            title = post.get("title", "无标题").strip()
            content = post.get("content", "")
            post_id = post.get("id", "")
            link = self.construct_link(post_id)
            
            # 提取摘要
            summary = self.extract_summary(content, max_chars=80)
            
            # 限制标题长度
            if len(title) > 20:
                title = title[:17] + "..."
            
            # 限制摘要长度
            if len(summary) > 60:
                summary = summary[:57] + "..."
            
            output.append(f"• {title} - {summary} {link}")
        
        return "\n".join(output)
    
    def format_raw(self, posts: List[Dict]) -> str:
        """
        格式化原始数据输出（用于调试）
        
        Args:
            posts: 帖子列表
            
        Returns:
            格式化后的JSON字符串
        """
        simplified = []
        for post in posts:
            simplified.append({
                "id": post.get("id"),
                "title": post.get("title"),
                "content_preview": post.get("content", "")[:200] + "..." if len(post.get("content", "")) > 200 else post.get("content", ""),
                "author": post.get("author", {}).get("name") if post.get("author") else None,
                "upvotes": post.get("upvotes"),
                "created_at": post.get("created_at"),
                "link": self.construct_link(post.get("id", ""))
            })
        
        return json.dumps(simplified, indent=2, ensure_ascii=False)
    
    def save_cache(self, posts: List[Dict], cache_dir: str = "cache") -> str:
        """
        保存帖子到缓存文件
        
        Args:
            posts: 帖子列表
            cache_dir: 缓存目录
            
        Returns:
            缓存文件路径
        """
        cache_path = Path(cache_dir)
        cache_path.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cache_file = cache_path / f"moltbook_{timestamp}.json"
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": timestamp,
                "posts": posts
            }, f, indent=2, ensure_ascii=False)
        
        return str(cache_file)
    
    def load_latest_cache(self, cache_dir: str = "cache") -> Optional[List[Dict]]:
        """
        加载最新的缓存文件
        
        Args:
            cache_dir: 缓存目录
            
        Returns:
            缓存的帖子列表或None
        """
        cache_path = Path(cache_dir)
        if not cache_path.exists():
            return None
        
        cache_files = list(cache_path.glob("moltbook_*.json"))
        if not cache_files:
            return None
        
        latest_file = max(cache_files, key=lambda x: x.stat().st_mtime)
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("posts", [])
        except:
            return None


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Moltbook Reader - 高效浏览Moltbook")
    parser.add_argument("--mode", choices=["l1", "l2", "raw"], default="l2",
                       help="输出模式: l1=标题+链接, l2=标题+观点+链接, raw=原始数据")
    parser.add_argument("--limit", type=int, default=3,
                       help="获取的帖子数量")
    parser.add_argument("--api-key", type=str,
                       default="moltbook_sk_MDQ7Y7CU2cPX_yyxf6MM9ZZpXSAXZnYr",
                       help="Moltbook API密钥")
    parser.add_argument("--cache", action="store_true",
                       help="启用缓存")
    parser.add_argument("--cache-dir", type=str, default="cache",
                       help="缓存目录")
    
    args = parser.parse_args()
    
    # 创建阅读器
    reader = MoltbookReader(api_key=args.api_key)
    
    # 获取帖子
    if args.cache:
        posts = reader.load_latest_cache(args.cache_dir)
        if not posts:
            posts = reader.fetch_posts(limit=args.limit)
            if posts:
                reader.save_cache(posts, args.cache_dir)
    else:
        posts = reader.fetch_posts(limit=args.limit)
    
    if not posts:
        print("❌ 无法获取Moltbook帖子")
        sys.exit(1)
    
    # 根据模式格式化输出
    if args.mode == "l1":
        output = reader.format_l1(posts)
    elif args.mode == "l2":
        output = reader.format_l2(posts)
    else:  # raw
        output = reader.format_raw(posts)
    
    print(output)


if __name__ == "__main__":
    main()