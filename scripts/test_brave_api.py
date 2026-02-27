#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Brave Search API
"""

import requests
import json
import os

BRAVE_API_KEY = "BSAo80XKa0ke0SNirZxhOZQ6urU--Ew"
BRAVE_ENDPOINT = "https://api.search.brave.com/res/v1/web/search"

def test_brave_api():
    """测试 Brave API 连接"""
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": BRAVE_API_KEY
    }
    
    params = {
        "q": "OpenClaw AI",
        "count": 3,
        "country": "US",
        "search_lang": "en"
    }
    
    try:
        print("🔍 测试 Brave Search API...")
        response = requests.get(BRAVE_ENDPOINT, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API 连接成功!")
            print(f"📊 搜索结果数: {len(data.get('web', {}).get('results', []))}")
            
            # 显示前2个结果
            results = data.get('web', {}).get('results', [])[:2]
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result.get('title', 'No title')}")
                print(f"   📍 {result.get('url', 'No URL')}")
                print(f"   📝 {result.get('description', 'No description')[:100]}...")
            
            return True
        else:
            print(f"❌ API 连接失败: HTTP {response.status_code}")
            print(f"响应: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_brave_api()
    if success:
        print("\n🎉 Brave Search API 配置成功!")
    else:
        print("\n⚠️  Brave Search API 配置失败，请检查 API Key")
