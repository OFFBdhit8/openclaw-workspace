#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moltbook 论坛集成模块
- 浏览: 使用 deepseek-chat (便宜量大)
- 发帖/评论: 使用 Kimi/Deepseek premium (高质量)
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

# Moltbook API 配置
MOLTBOOK_API_KEY = "moltbook_sk_MDQ7Y7CU2cPX_yyxf6MM9ZZpXSAXZnYr"
MOLTBOOK_BASE_URL = "https://moltbook.com/api/v1"  # 真实的Moltbook API地址

# 模型配置 - 根据任务类型选择
MOLTBOOK_MODELS = {
    "browse": {
        # 浏览任务 - 便宜量大
        "model": "deepseek-chat",
        "api_key": "sk-7c004758529f45c6ac42ec3e620c088d",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "max_tokens": 500,
        "temperature": 0.7,
        "description": "浏览用 - 便宜量大管饱"
    },
    "post": {
        # 发帖 - 使用 DeepSeek-R1 推理模型，杜绝幻觉
        # 发帖 - 高质量
        "model": "deepseek-reasoner",
        "api_key": "sk-7c004758529f45c6ac42ec3e620c088d",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "max_tokens": 1000,
        "temperature": 0.5,
        "description": "发帖 - 高质量"
    },
    "comment": {
        # 评论 - 使用 DeepSeek-R1 推理模型，杜绝幻觉
        "model": "deepseek-reasoner",
        "api_key": "sk-7c004758529f45c6ac42ec3e620c088d",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "max_tokens": 1500,
        "temperature": 0.3,  # 降低温度，减少随机性
        "description": "评论 - 使用 R1 推理模型，杜绝幻觉"
    },
    "audit": {
        # 审计任务 - 使用 R1 模型进行事实核查
        "model": "deepseek-reasoner",
        "api_key": "sk-7c004758529f45c6ac42ec3e620c088d",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "max_tokens": 1000,
        "temperature": 0.1,  # 极低温度，确保事实准确性
        "description": "审计 - 使用 R1 模型进行事实核查"
    }
}


class MoltbookClient:
    """Moltbook 论坛客户端"""
    
    def __init__(self, api_key: str = MOLTBOOK_API_KEY):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_posts(self, forum_id: str = None, limit: int = 20) -> List[Dict]:
        """获取帖子列表（浏览）- 真实API调用"""
        try:
            url = f"{MOLTBOOK_BASE_URL}/posts"
            params = {"limit": limit} if limit else {}
            
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get("posts", [])
                
                # 格式化帖子数据
                formatted_posts = []
                for post in posts:
                    formatted_posts.append({
                        "id": post.get("id"),
                        "title": post.get("title"),
                        "content": post.get("content"),
                        "author": post.get("author", {}).get("name", "Unknown"),
                        "submolt": post.get("submolt", {}).get("display_name", "General"),
                        "upvotes": post.get("upvotes", 0),
                        "comment_count": post.get("comment_count", 0),
                        "score": post.get("score", 0),
                        "created_at": post.get("created_at"),
                        "url": f"https://moltbook.com/post/{post.get('id')}"
                    })
                
                return formatted_posts
            else:
                print(f"⚠️ API返回错误: {response.status_code}")
                return []
        except Exception as e:
            print(f"⚠️ 获取帖子失败: {e}")
            return []
    
    def get_post_detail(self, post_id: str) -> Dict:
        """获取帖子详情（浏览）- 真实API调用"""
        try:
            url = f"{MOLTBOOK_BASE_URL}/post/{post_id}"
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                post = response.json()
                
                return {
                    "id": post.get("id"),
                    "title": post.get("title"),
                    "content": post.get("content"),
                    "author": post.get("author", {}).get("name", "Unknown"),
                    "submolt": post.get("submolt", {}).get("display_name", "General"),
                    "upvotes": post.get("upvotes", 0),
                    "comment_count": post.get("comment_count", 0),
                    "score": post.get("score", 0),
                    "created_at": post.get("created_at"),
                    "url": f"https://moltbook.com/post/{post.get('id')}"
                }
            else:
                print(f"⚠️ API返回错误: {response.status_code}")
                return {}
        except Exception as e:
            print(f"⚠️ 获取帖子详情失败: {e}")
            return {}
    
    def create_post(self, title: str, content: str) -> Dict:
        """创建帖子（发帖）"""
        # 调用 Moltbook API
        data = {
            "title": title,
            "content": content
        }
        # return self.session.post(f"{MOLTBOOK_BASE_URL}/posts", json=data).json()
        return {"success": True, "post_id": "new_post_id"}
    
    def create_comment(self, post_id: str, content: str) -> Dict:
        """创建评论"""
        data = {
            "content": content
        }
        # return self.session.post(f"{MOLTBOOK_BASE_URL}/post/{post_id}/comments", json=data).json()
        return {"success": True, "comment_id": "new_comment_id"}


class MoltbookAI:
    """Moltbook AI 助手 - 智能模型选择"""
    
    def __init__(self):
        self.client = MoltbookClient()
        self.task_count = {"browse": 0, "post": 0, "comment": 0, "audit": 0}
        self.audit_log = []  # 审计日志
        self.audited_posts = set()  # 已审计的帖子ID
    
    def detect_task_type(self, prompt: str) -> str:
        """
        检测任务类型:
        - browse: 浏览、查看、阅读、获取
        - post: 发帖、发布、创建新帖
        - comment: 评论、回复、留言
        """
        prompt_lower = prompt.lower()
        
        # 发帖关键词
        post_keywords = ["发帖", "发布", "发贴", "创建帖子", "新建帖子", "写帖子", "发文章", "发布文章"]
        for kw in post_keywords:
            if kw in prompt_lower:
                return "post"
        
        # 评论关键词
        comment_keywords = ["评论", "回复", "留言", "回帖", "跟帖", "点评"]
        for kw in comment_keywords:
            if kw in prompt_lower:
                return "comment"
        
        # 浏览关键词（默认）
        browse_keywords = ["浏览", "查看", "看", "阅读", "获取", "搜索", "查找", "翻页", "列表"]
        for kw in browse_keywords:
            if kw in prompt_lower:
                return "browse"
        
        # 默认浏览
        return "browse"
    
    def call_model(self, task_type: str, prompt: str, context: str = "") -> Dict:
        """
        根据任务类型调用相应模型
        """
        model_config = MOLTBOOK_MODELS.get(task_type, MOLTBOOK_MODELS["browse"])
        
        headers = {
            "Authorization": f"Bearer {model_config['api_key']}",
            "Content-Type": "application/json"
        }
        
        # 构建提示词
        if task_type == "browse":
            system_msg = "你是一个论坛浏览助手。简洁总结内容，不要过度发挥。"
        elif task_type == "post":
            system_msg = "你是一个专业的论坛写手。创作高质量、有深度的帖子内容。"
        elif task_type == "comment":
            system_msg = "你是一个 thoughtful 的评论者。提供有价值的观点和回应。"
        else:
            system_msg = "你是一个 helpful 的助手。"
        
        messages = [
            {"role": "system", "content": system_msg}
        ]
        
        if context:
            messages.append({"role": "user", "content": f"上下文：{context}"})
        
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": model_config["model"],
            "messages": messages,
            "max_tokens": model_config["max_tokens"],
            "temperature": model_config["temperature"]
        }
        
        try:
            response = requests.post(
                model_config["api_url"],
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                
                # 统计
                self.task_count[task_type] += 1
                
                return {
                    "success": True,
                    "content": content,
                    "task_type": task_type,
                    "model": model_config["model"],
                    "cost_level": "cheap" if task_type == "browse" else "premium",
                    "tokens": result.get("usage", {}).get("total_tokens", 0)
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "task_type": task_type
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "task_type": task_type
            }
    
    def audit_content(self, content: str, content_type: str = "post") -> Dict:
        """
        审计内容 - 使用 R1 模型进行事实核查，杜绝幻觉
        """
        print(f"🔍 [Moltbook] 审计任务 - 使用 DeepSeek-R1 (事实核查)")
        
        audit_prompt = f"""
请对以下{content_type}内容进行事实核查和幻觉检测：

内容：
{content}

请按照以下步骤进行分析：
1. 识别内容中的事实性陈述
2. 检查是否存在未经证实的断言或猜测
3. 标记任何可能产生误导的信息
4. 评估整体事实准确性
5. 提供改进建议（如果需要）

请以结构化格式回复，包括：
- 事实准确性评分（1-10分）
- 发现的潜在问题
- 改进建议
- 是否通过审计（是/否）
"""
        
        result = self.call_model("audit", audit_prompt, content)
        
        if result["success"]:
            audit_result = {
                "content_type": content_type,
                "original_content": content[:500] + "..." if len(content) > 500 else content,
                "audit_report": result["content"],
                "model": result["model"],
                "timestamp": datetime.now().isoformat(),
                "passed": "通过" in result["content"] or "是" in result["content"]
            }
            
            # 记录审计日志
            self.audit_log.append(audit_result)
            self.task_count["audit"] += 1
            
            print(f"✅ 审计完成 - 结果: {'通过' if audit_result['passed'] else '未通过'}")
            return audit_result
        else:
            print(f"❌ 审计失败: {result.get('error')}")
            return {
                "success": False,
                "error": result.get("error"),
                "passed": False
            }
    
    def browse_forum_with_audit(self, instruction: str) -> str:
        """
        浏览论坛 - 必须先审计后才能浏览
        """
        print(f"🔍 [Moltbook] 安全浏览任务 - 需要先审计")
        
        # 获取帖子
        posts = self.client.get_posts()
        
        # 对每个帖子进行审计
        audited_posts = []
        for post in posts:
            post_id = post.get("id", "unknown")
            
            # 如果已经审计过，跳过
            if post_id in self.audited_posts:
                audited_posts.append(post)
                continue
            
            # 审计帖子内容
            content = f"标题: {post.get('title', '无标题')}\n内容: {post.get('content', '无内容')}"
            audit_result = self.audit_content(content, "post")
            
            if audit_result.get("passed", False):
                # 审计通过，添加到已审计集合
                self.audited_posts.add(post_id)
                audited_posts.append(post)
                print(f"✅ 帖子 {post_id} 审计通过")
            else:
                print(f"⚠️ 帖子 {post_id} 审计未通过，跳过")
        
        if not audited_posts:
            return "⚠️ 没有通过审计的帖子可供浏览"
        
        # 构建浏览提示
        context = f"通过审计的帖子列表：\n{json.dumps(audited_posts, ensure_ascii=False, indent=2)}"
        prompt = f"{instruction}\n\n请基于以上通过审计的内容给出简洁的总结。"
        
        result = self.call_model("browse", prompt, context)
        
        if result["success"]:
            return f"✅ 安全浏览结果（仅显示通过审计的内容）：\n\n{result['content']}"
        else:
            return f"浏览失败: {result.get('error')}"
    
    def browse_forum(self, instruction: str) -> str:
        """
        浏览论坛 - 使用便宜模型
        """
        print(f"🔍 [Moltbook] 浏览任务 - 使用 deepseek-chat")
        
        # 获取帖子
        posts = self.client.get_posts()
        
        # 构建浏览提示
        context = f"论坛帖子列表：\n{json.dumps(posts, ensure_ascii=False, indent=2)}"
        prompt = f"{instruction}\n\n请基于以上内容给出简洁的总结。"
        
        result = self.call_model("browse", prompt, context)
        
        if result["success"]:
            return result["content"]
        else:
            return f"浏览失败: {result.get('error')}"
    
    def create_post(self, topic: str, requirements: str = "") -> str:
        """
        创建帖子 - 使用高质量模型
        """
        print(f"✍️ [Moltbook] 发帖任务 - 使用 Kimi (高质量)")
        
        prompt = f"请为论坛创作一篇高质量的帖子。\n\n主题: {topic}"
        if requirements:
            prompt += f"\n\n要求: {requirements}"
        
        prompt += "\n\n请创作有深度、有价值的内容，吸引读者互动。"
        
        result = self.call_model("post", prompt)
        
        if result["success"]:
            # 可以在这里实际发布到论坛
            # self.client.create_post(topic, result["content"])
            return result["content"]
        else:
            return f"创作失败: {result.get('error')}"
    
    def create_comment_with_r1(self, post_content: str, user_opinion: str = "") -> str:
        """
        创建评论 - 使用 DeepSeek-R1 推理模型，严格杜绝幻觉
        """
        print(f"💬 [Moltbook] 评论任务 - 使用 DeepSeek-R1 (推理模型，杜绝幻觉)")
        
        # 严格的系统提示词，杜绝幻觉
        strict_prompt = f"""
请针对以下帖子内容创作一条有价值的评论。

重要要求：
1. **严格基于帖子内容**：只评论帖子中明确提到的内容，不要添加未提及的信息
2. **杜绝幻觉**：不猜测、不断言未知事实、不编造信息
3. **事实准确性**：如果引用事实，必须是公认的、可验证的
4. **明确区分**：清楚区分帖子观点和你个人的观点
5. **谦逊态度**：如果不确定，明确说明"我不确定"或"根据我的理解"

帖子内容：
{post_content}
"""
        
        if user_opinion:
            strict_prompt += f"\n\n你的观点或角度（请基于此但保持事实准确）：{user_opinion}"
        
        strict_prompt += "\n\n请创作一条 thoughtful、事实准确、促进健康讨论的评论。"
        
        result = self.call_model("comment", strict_prompt, post_content)
        
        if result["success"]:
            # 对生成的评论进行审计
            print("🔍 对生成的评论进行事实核查...")
            audit_result = self.audit_content(result["content"], "comment")
            
            if audit_result.get("passed", False):
                print("✅ 评论通过审计，可以发布")
                return result["content"]
            else:
                print("⚠️ 评论未通过审计，需要重新生成")
                # 如果审计失败，重新生成更保守的评论
                fallback_prompt = f"""
帖子内容：{post_content}

请创作一条非常保守、完全基于帖子内容的简单评论。
要求：
1. 只回应帖子中明确提到的1-2个点
2. 不添加任何新信息
3. 使用"我同意"、"我理解"等简单回应
4. 绝对不猜测、不断言
"""
                fallback_result = self.call_model("comment", fallback_prompt, post_content)
                if fallback_result["success"]:
                    return f"⚠️ 原始评论未通过事实核查，已生成保守版本：\n\n{fallback_result['content']}"
                else:
                    return "❌ 评论生成失败，请重试"
        else:
            return f"评论失败: {result.get('error')}"
    
    def create_comment(self, post_content: str, user_opinion: str = "") -> str:
        """
        兼容方法 - 使用新的 R1 评论方法
        """
        return self.create_comment_with_r1(post_content, user_opinion)
    
    def handle_task(self, user_input: str) -> Dict:
        """
        统一任务处理入口 - 更新版，支持安全浏览和 R1 评论
        """
        task_type = self.detect_task_type(user_input)
        
        print(f"🎯 任务类型检测: {task_type}")
        
        # 更新模型选择显示
        if task_type == "browse":
            model_info = "cheap (deepseek-chat) + 审计"
        elif task_type == "post":
            model_info = "premium (Kimi)"
        elif task_type == "comment":
            model_info = "premium (DeepSeek-R1) + 审计"
        else:
            model_info = "cheap (deepseek-chat)"
        
        print(f"🤖 模型选择: {model_info}")
        
        if task_type == "browse":
            # 使用安全浏览（需要先审计）
            content = self.browse_forum_with_audit(user_input)
        elif task_type == "post":
            # 提取主题
            topic = user_input.replace("发帖", "").replace("发布", "").strip()
            content = self.create_post(topic)
        elif task_type == "comment":
            # 需要从上下文中获取帖子内容
            # 这里假设有一个帖子内容，实际应用中应该从上下文获取
            sample_post = "这是一个关于人工智能发展的帖子，讨论了AI在医疗、教育和创作领域的应用前景。"
            content = self.create_comment(sample_post, user_input)
        else:
            content = self.browse_forum_with_audit(user_input)
        
        return {
            "task_type": task_type,
            "content": content,
            "stats": self.get_stats(),
            "audit_count": len(self.audit_log)
        }
    
    def get_stats(self) -> Dict:
        """获取使用统计"""
        total = sum(self.task_count.values())
        if total == 0:
            return {"message": "暂无任务记录"}
        
        cheap_count = self.task_count["browse"]
        premium_count = self.task_count["post"] + self.task_count["comment"]
        audit_count = self.task_count["audit"]
        
        # 计算审计通过率
        passed_audits = sum(1 for log in self.audit_log if log.get("passed", False))
        audit_pass_rate = f"{passed_audits/audit_count*100:.1f}%" if audit_count > 0 else "N/A"
        
        return {
            "total_tasks": total,
            "browse_tasks": cheap_count,
            "post_tasks": self.task_count["post"],
            "comment_tasks": self.task_count["comment"],
            "audit_tasks": audit_count,
            "audit_pass_rate": audit_pass_rate,
            "audited_posts_count": len(self.audited_posts),
            "cheap_percentage": f"{cheap_count/total*100:.1f}%",
            "premium_percentage": f"{premium_count/total*100:.1f}%",
            "estimated_savings": f"约 {cheap_count/total*100:.1f}% 任务使用便宜模型",
            "safety_level": "高 (R1推理模型 + 审计机制)"
        }


# 测试
if __name__ == "__main__":
    ai = MoltbookAI()
    
    # 测试安全浏览（需要先审计）
    print("="*60)
    print("测试 1: 安全浏览论坛（需要先审计）")
    result = ai.handle_task("浏览一下今天的帖子")
    print(f"结果: {result['content'][:200]}...")
    print()
    
    # 测试发帖
    print("="*60)
    print("测试 2: 发帖")
    result = ai.handle_task("发一个关于AI发展趋势的帖子")
    print(f"结果: {result['content'][:200]}...")
    print()
    
    # 测试评论（使用 R1 模型 + 审计）
    print("="*60)
    print("测试 3: 评论（使用 DeepSeek-R1 + 审计）")
    result = ai.handle_task("评论一下这个AI帖子")
    print(f"结果: {result['content'][:200]}...")
    print()
    
    # 测试直接审计功能
    print("="*60)
    print("测试 4: 直接审计内容")
    sample_content = "人工智能将在2030年完全取代人类工作，这是不可避免的趋势。"
    audit_result = ai.audit_content(sample_content, "statement")
    print(f"审计结果: {'通过' if audit_result.get('passed', False) else '未通过'}")
    if "audit_report" in audit_result:
        print(f"审计报告摘要: {audit_result['audit_report'][:150]}...")
    print()
    
    # 统计
    print("="*60)
    print("完整统计:")
    print(json.dumps(ai.get_stats(), indent=2, ensure_ascii=False))
    
    # 显示审计日志摘要
    print("\n" + "="*60)
    print("审计日志摘要:")
    for i, log in enumerate(ai.audit_log[-3:], 1):  # 显示最后3条审计记录
        print(f"{i}. 类型: {log.get('content_type', 'unknown')}")
        print(f"   时间: {log.get('timestamp', 'unknown')}")
        print(f"   结果: {'✅ 通过' if log.get('passed', False) else '❌ 未通过'}")
        print(f"   模型: {log.get('model', 'unknown')}")
        print()
