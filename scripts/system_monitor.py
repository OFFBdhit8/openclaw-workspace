#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统状态监控脚本
"""

import subprocess
import json
import os
from datetime import datetime

def check_service_status():
    """检查服务状态"""
    print("🔧 检查服务状态...")
    
    services = ["auberon-smart.service", "auberon.service"]
    
    for service in services:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", service],
                capture_output=True,
                text=True
            )
            status = result.stdout.strip()
            print(f"  {service}: {status}")
        except:
            print(f"  {service}: 检查失败")

def check_processes():
    """检查进程"""
    print("\n🔄 检查相关进程...")
    
    try:
        # 检查 auberon 相关进程
        result = subprocess.run(
            "ps aux | grep -E '(auberon|python.*bot)' | grep -v grep",
            shell=True,
            capture_output=True,
            text=True
        )
        
        lines = result.stdout.strip().split('\n')
        print(f"  找到 {len(lines)} 个相关进程:")
        for line in lines[:3]:  # 只显示前3个
            if line:
                parts = line.split()
                pid = parts[1]
                cmd = ' '.join(parts[10:])[:50]
                print(f"    PID {pid}: {cmd}...")
    except:
        print("  进程检查失败")

def check_brave_config():
    """检查 Brave 配置"""
    print("\n🌐 检查 Brave API 配置...")
    
    config_path = "/root/.openclaw/config/brave.json"
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            key = config.get("api_key", "")
            masked_key = key[:10] + "..." if len(key) > 10 else key
            print(f"  ✅ 配置文件存在")
            print(f"  🔑 API Key: {masked_key}")
        except:
            print("  ❌ 配置文件读取失败")
    else:
        print("  ❌ 配置文件不存在")
    
    # 检查环境变量
    brave_key = os.getenv("BRAVE_API_KEY")
    if brave_key:
        masked = brave_key[:10] + "..." if len(brave_key) > 10 else brave_key
        print(f"  ✅ 环境变量: {masked}")
    else:
        print("  ❌ 环境变量未设置")

def check_api_keys():
    """检查 API Key 状态"""
    print("\n🔑 检查 API Key 状态...")
    
    keys_file = "/root/.openclaw/workspace/secrets/api_keys.md"
    
    if os.path.exists(keys_file):
        try:
            with open(keys_file, 'r') as f:
                content = f.read()
            
            # 统计 Key 数量
            deepseek_count = content.count("sk-7c0")
            kimi_count = content.count("sk-AeUl")
            minimax_count = content.count("sk-api-")
            qwen_count = content.count("sk-46ecd")
            hunyuan_count = content.count("sk-qv0tlt")
            brave_count = content.count("BSAo80XKa0")
            
            print(f"  ✅ API Key 文件存在")
            print(f"  📊 统计:")
            print(f"    Deepseek: {deepseek_count}")
            print(f"    Kimi: {kimi_count}")
            print(f"    Minimax: {minimax_count}")
            print(f"    Qwen: {qwen_count}")
            print(f"    腾讯混元: {hunyuan_count}")
            print(f"    Brave: {brave_count}")
        except:
            print("  ❌ 文件读取失败")
    else:
        print("  ❌ API Key 文件不存在")

def check_scripts():
    """检查脚本文件"""
    print("\n📁 检查脚本文件...")
    
    scripts_dir = "/root/.openclaw/workspace/scripts"
    
    if os.path.exists(scripts_dir):
        files = os.listdir(scripts_dir)
        bot_files = [f for f in files if 'auberon' in f.lower() or 'bot' in f.lower()]
        other_files = [f for f in files if f not in bot_files]
        
        print(f"  ✅ 脚本目录存在 ({len(files)} 个文件)")
        print(f"  🤖 Bot相关文件: {len(bot_files)} 个")
        for f in sorted(bot_files)[:5]:
            print(f"    - {f}")
        
        if len(bot_files) > 5:
            print(f"    ... 还有 {len(bot_files)-5} 个")
        
        print(f"  📝 其他重要文件:")
        important = [f for f in other_files if any(x in f.lower() for x in ['optimiz', 'test', 'moltbook', 'token'])]
        for f in sorted(important)[:5]:
            print(f"    - {f}")
    else:
        print("  ❌ 脚本目录不存在")

def get_system_info():
    """获取系统信息"""
    print("\n💻 系统信息...")
    
    try:
        # 内存使用
        result = subprocess.run(
            "free -h | grep Mem",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            mem_info = result.stdout.strip().split()
            print(f"  内存: {mem_info[2]}/{mem_info[1]} 使用")
        
        # 磁盘使用
        result = subprocess.run(
            "df -h / | tail -1",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stdout:
            disk_info = result.stdout.strip().split()
            print(f"  磁盘: {disk_info[2]}/{disk_info[1]} 使用 ({disk_info[4]})")
        
        # 时间
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  当前时间: {now}")
        
    except:
        print("  系统信息获取失败")

def main():
    print("="*70)
    print("🖥️  Auberon 系统状态监控")
    print("="*70)
    
    check_service_status()
    check_processes()
    check_brave_config()
    check_api_keys()
    check_scripts()
    get_system_info()
    
    print("\n" + "="*70)
    print("📋 总结:")
    print("  1. 检查服务是否运行")
    print("  2. 验证配置是否正确")
    print("  3. 确认关键文件存在")
    print("  4. 监控系统资源")
    print("="*70)
    print("✅ 监控完成!")

if __name__ == "__main__":
    main()
