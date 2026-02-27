#!/usr/bin/env python3
"""
记忆维护脚本 - 基于 "The Sourdough Starter" 理念
定期喂养（记录）、结构化、修剪记忆系统
"""

import os
import re
import json
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
RAW_DIR = MEMORY_DIR / "raw"
DIGEST_DIR = MEMORY_DIR / "digest"
LONG_TERM_DIR = MEMORY_DIR / "long-term"
REJECTED_DIR = MEMORY_DIR / "rejected"

def ensure_dirs():
    """确保所有目录存在"""
    for dir_path in [MEMORY_DIR, RAW_DIR, DIGEST_DIR, LONG_TERM_DIR, REJECTED_DIR]:
        dir_path.mkdir(exist_ok=True)

def get_recent_files(days=7):
    """获取最近几天的记忆文件"""
    recent = []
    for file_path in MEMORY_DIR.glob("*.md"):
        if file_path.name == "MEMORY.md":
            continue
        # 尝试从文件名解析日期
        match = re.match(r"(\d{4})-(\d{2})-(\d{2})\.md", file_path.name)
        if match:
            year, month, day = map(int, match.groups())
            file_date = datetime(year, month, day)
            if datetime.now() - file_date <= timedelta(days=days):
                recent.append((file_date, file_path))
    return sorted(recent, key=lambda x: x[0])

def get_recent_rejected_files(days=7):
    """获取最近几天的拒绝日志文件"""
    recent = []
    for file_path in REJECTED_DIR.glob("*.md"):
        # 尝试从文件名解析日期
        match = re.match(r"(\d{4})-(\d{2})-(\d{2})-rejected\.md", file_path.name)
        if match:
            year, month, day = map(int, match.groups())
            file_date = datetime(year, month, day)
            if datetime.now() - file_date <= timedelta(days=days):
                recent.append((file_date, file_path))
    return sorted(recent, key=lambda x: x[0])

def extract_key_points(content):
    """从记忆内容中提取关键点"""
    key_points = []
    
    # 寻找重要部分
    lines = content.split('\n')
    current_section = ""
    
    for line in lines:
        # 标题行（## 或 #）
        if line.startswith('## '):
            current_section = line[3:].strip()
        elif line.startswith('# '):
            current_section = line[2:].strip()
        
        # 标记为重要或已完成的项目
        if line.strip().startswith('- [x]') or line.strip().startswith('✅'):
            key_points.append(f"{current_section}: {line.strip()}")
        # 包含"重要"、"关键"、"学习"等关键词
        elif any(keyword in line.lower() for keyword in ['重要', '关键', '学习', '教训', '决定', '配置']):
            if len(line.strip()) > 20:  # 避免太短的噪音
                key_points.append(f"{current_section}: {line.strip()}")
    
    return key_points

def create_daily_digest(date, file_path):
    """创建每日摘要"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        key_points = extract_key_points(content)
        
        if not key_points:
            return None
        
        digest_file = DIGEST_DIR / f"{date.strftime('%Y-%m-%d')}-digest.md"
        with open(digest_file, 'w', encoding='utf-8') as f:
            f.write(f"# {date.strftime('%Y-%m-%d')} 摘要\n\n")
            f.write(f"源文件: {file_path.name}\n\n")
            f.write("## 关键要点\n\n")
            for point in key_points:
                f.write(f"- {point}\n")
            f.write(f"\n## 原始大小\n字符数: {len(content)}\n")
        
        print(f"创建摘要: {digest_file.name}")
        return digest_file
    except Exception as e:
        print(f"处理 {file_path.name} 时出错: {e}")
        return None

def analyze_rejected_decisions(rejected_files):
    """分析拒绝日志，提取决策模式"""
    decisions = []
    
    for date, file_path in rejected_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析拒绝日志结构
            lines = content.split('\n')
            current_decision = {}
            in_decision = False
            
            for line in lines:
                line = line.strip()
                if line.startswith('**决策时间**:'):
                    if current_decision:
                        decisions.append(current_decision)
                    current_decision = {'date': date.strftime('%Y-%m-%d'), 'file': file_path.name}
                    in_decision = True
                elif line.startswith('**最终选择**:'):
                    current_decision['final_choice'] = line.split(':', 1)[1].strip()
                elif line.startswith('**被拒绝选项**:'):
                    current_decision['rejected_option'] = line.split(':', 1)[1].strip()
                elif line.startswith('**拒绝理由**:'):
                    current_decision['reason'] = line.split(':', 1)[1].strip()
                elif line.startswith('**上下文**:'):
                    current_decision['context'] = line.split(':', 1)[1].strip()
            
            if current_decision:
                decisions.append(current_decision)
                
        except Exception as e:
            print(f"分析拒绝日志 {file_path.name} 时出错: {e}")
    
    return decisions

def update_long_term_memory(digest_files, decisions=None):
    """更新长期记忆"""
    if not digest_files and not decisions:
        return
    
    long_term_file = LONG_TERM_DIR / "knowledge-base.md"
    
    # 读取现有知识库
    existing_content = ""
    if long_term_file.exists():
        with open(long_term_file, 'r', encoding='utf-8') as f:
            existing_content = f.read()
    
    # 合并新摘要
    new_knowledge = []
    for digest_file in digest_files[-5:]:  # 最近5个摘要
        try:
            with open(digest_file, 'r', encoding='utf-8') as f:
                new_knowledge.append(f.read())
        except:
            pass
    
    with open(long_term_file, 'w', encoding='utf-8') as f:
        f.write("# 长期知识库\n\n")
        f.write("基于日常记忆提炼的重要知识和经验教训\n\n")
        f.write("最后更新: " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n\n")
        
        # 如果有决策模式，添加到最前面
        if decisions:
            f.write("## 决策模式\n\n")
            f.write("基于拒绝日志提炼的常见决策模式和理由：\n\n")
            
            # 按拒绝理由分组
            reason_groups = {}
            for decision in decisions:
                reason = decision.get('reason', '未说明理由')
                if reason not in reason_groups:
                    reason_groups[reason] = []
                reason_groups[reason].append(decision)
            
            for reason, group_decisions in reason_groups.items():
                f.write(f"### 拒绝理由：{reason}\n")
                f.write(f"出现次数：{len(group_decisions)}\n\n")
                for i, decision in enumerate(group_decisions[:3], 1):  # 最多显示3个例子
                    f.write(f"{i}. **{decision.get('date', '未知日期')}** - ")
                    f.write(f"拒绝：{decision.get('rejected_option', '未知选项')[:50]}...\n")
                    if decision.get('context'):
                        f.write(f"   上下文：{decision.get('context')[:100]}...\n")
                f.write("\n")
            f.write("\n---\n\n")
        
        if new_knowledge:
            f.write("## 最近更新\n\n")
            for knowledge in new_knowledge:
                f.write(knowledge)
                f.write("\n---\n\n")
        
        if existing_content and "## 历史知识" not in existing_content:
            f.write("## 历史知识\n\n")
            # 只保留历史部分中最重要的内容
            lines = existing_content.split('\n')
            important_lines = [line for line in lines if any(
                keyword in line.lower() for keyword in ['配置', 'api', '密钥', '重要', '不要', '必须']
            )]
            if important_lines:
                f.write("\n".join(important_lines[:50]))  # 限制长度
    
    print(f"更新长期记忆: {long_term_file}")

def archive_old_files():
    """归档旧文件到raw目录"""
    for file_path in MEMORY_DIR.glob("*.md"):
        if file_path.name == "MEMORY.md":
            continue
        
        # 超过30天的文件归档到raw
        match = re.match(r"(\d{4})-(\d{2})-(\d{2})\.md", file_path.name)
        if match:
            year, month, day = map(int, match.groups())
            file_date = datetime(year, month, day)
            
            if datetime.now() - file_date > timedelta(days=30):
                raw_file = RAW_DIR / file_path.name
                if not raw_file.exists():
                    file_path.rename(raw_file)
                    print(f"归档旧文件: {file_path.name} -> raw/")

def main():
    """主函数"""
    print("开始记忆维护...")
    ensure_dirs()
    
    # 1. 处理最近7天的记忆文件
    recent_files = get_recent_files(days=7)
    digest_files = []
    
    for date, file_path in recent_files:
        digest = create_daily_digest(date, file_path)
        if digest:
            digest_files.append(digest)
    
    # 2. 处理拒绝日志
    recent_rejected = get_recent_rejected_files(days=7)
    decisions = []
    if recent_rejected:
        decisions = analyze_rejected_decisions(recent_rejected)
        print(f"分析 {len(decisions)} 个拒绝决策")
    
    # 3. 更新长期记忆（包含决策模式）
    if digest_files or decisions:
        update_long_term_memory(digest_files, decisions)
    
    # 4. 归档旧文件
    archive_old_files()
    
    # 5. 创建索引文件
    index_file = MEMORY_DIR / "INDEX.md"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write("# 记忆系统索引\n\n")
        f.write("## 目录结构\n")
        f.write("- raw/ - 原始日志（30天以上）\n")
        f.write("- digest/ - 每日摘要\n")
        f.write("- long-term/ - 长期知识库\n")
        f.write("- rejected/ - 拒绝日志\n\n")
        
        f.write("## 最近记忆文件\n")
        for date, file_path in recent_files[-10:]:
            f.write(f"- {date.strftime('%Y-%m-%d')}: {file_path.name}\n")
        
        if recent_rejected:
            f.write("\n## 最近拒绝日志\n")
            for date, file_path in recent_rejected[-5:]:
                f.write(f"- {date.strftime('%Y-%m-%d')}: {file_path.name}\n")
    
    print("记忆维护完成")
    return len(digest_files) + len(decisions)

if __name__ == "__main__":
    count = main()
    print(f"处理了 {count} 个摘要")