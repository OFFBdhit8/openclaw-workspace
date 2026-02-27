#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coding Plan Lite 配置和验证
"""

import requests
import json
import time
from pathlib import Path

CODING_PLAN_KEY = "sk-sp-14f905b909ee42e29a7fddf95250ad1b"

class CodingPlanLiteConfig:
    """Coding Plan Lite 配置管理器"""
    
    def __init__(self):
        self.key = CODING_PLAN_KEY
        self.possible_endpoints = [
            # OpenAI 兼容端点
            "https://api.openai.com/v1",
            "https://api.deepseek.com/v1",
            "https://api.moonshot.cn/v1",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "https://api.hunyuan.cloud.tencent.com/v1",
            # 可能的自定义端点
            "https://api.codingplan.com/v1",
            "https://codingplan-api.com/v1",
            "https://api.codingplan.ai/v1"
        ]
        
        self.test_results = {}
    
    def test_endpoint(self, base_url: str) -> dict:
        """测试 API 端点"""
        chat_url = f"{base_url}/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json"
        }
        
        test_data = {
            "model": "gpt-3.5-turbo",  # 通用模型名称
            "messages": [
                {"role": "system", "content": "You are Coding Plan Lite assistant."},
                {"role": "user", "content": "Say 'Coding Plan Lite is working' if you receive this."}
            ],
            "max_tokens": 30
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                chat_url,
                headers=headers,
                json=test_data,
                timeout=15
            )
            elapsed = time.time() - start_time
            
            result = {
                "status_code": response.status_code,
                "response_time": round(elapsed, 2),
                "success": False,
                "error": None,
                "content": None
            }
            
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                result["success"] = True
                result["content"] = content
            else:
                result["error"] = response.text[:200]
            
            return result
            
        except Exception as e:
            return {
                "status_code": 0,
                "response_time": 0,
                "success": False,
                "error": str(e),
                "content": None
            }
    
    def discover_endpoint(self):
        """发现可用的端点"""
        print("🔍 发现 Coding Plan Lite 端点...")
        
        working_endpoints = []
        
        for endpoint in self.possible_endpoints:
            print(f"\n🌐 测试: {endpoint}")
            result = self.test_endpoint(endpoint)
            
            self.test_results[endpoint] = result
            
            if result["success"]:
                print(f"  ✅ 成功! ({result['response_time']}秒)")
                print(f"     响应: {result['content']}")
                working_endpoints.append({
                    "endpoint": endpoint,
                    "response_time": result["response_time"],
                    "content": result["content"]
                })
            else:
                print(f"  ❌ 失败: HTTP {result['status_code']}")
                if result["error"]:
                    print(f"     错误: {result['error'][:100]}")
        
        return working_endpoints
    
    def create_config_file(self, endpoint: str):
        """创建配置文件"""
        config_dir = Path("/root/.openclaw/config")
        config_dir.mkdir(exist_ok=True)
        
        config = {
            "codingplan": {
                "api_key": self.key,
                "endpoint": endpoint,
                "model": "codingplan-lite",
                "max_tokens": 4096,
                "temperature": 0.7,
                "timeout": 30
            }
        }
        
        config_file = config_dir / "codingplan.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"📁 配置文件已创建: {config_file}")
        return config_file
    
    def update_models_json(self, endpoint: str):
        """更新 models.json"""
        models_file = Path("/root/.openclaw/agents/main/agent/models.json")
        
        if not models_file.exists():
            print(f"❌ models.json 不存在: {models_file}")
            return False
        
        try:
            with open(models_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 更新 codingplan 配置
            if "codingplan" in data["providers"]:
                data["providers"]["codingplan"]["baseUrl"] = endpoint
                data["providers"]["codingplan"]["apiKey"] = self.key
            else:
                # 添加 codingplan 配置
                data["providers"]["codingplan"] = {
                    "baseUrl": endpoint,
                    "apiKey": self.key,
                    "api": "openai-completions",
                    "models": [
                        {
                            "id": "codingplan-lite",
                            "name": "Coding Plan Lite",
                            "reasoning": False,
                            "input": ["text"],
                            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
                            "contextWindow": 200000,
                            "maxTokens": 8192,
                            "api": "openai-completions"
                        }
                    ]
                }
            
            with open(models_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ models.json 已更新")
            return True
            
        except Exception as e:
            print(f"❌ 更新 models.json 失败: {e}")
            return False
    
    def generate_report(self, working_endpoints: list):
        """生成报告"""
        report = [
            "="*60,
            "📋 Coding Plan Lite 配置报告",
            "="*60,
            f"🔑 API Key: {self.key[:10]}...",
            f"📊 测试端点数: {len(self.possible_endpoints)}",
            f"✅ 可用端点数: {len(working_endpoints)}",
            ""
        ]
        
        if working_endpoints:
            report.append("🎉 找到可用端点:")
            for i, ep in enumerate(working_endpoints, 1):
                report.append(f"  {i}. {ep['endpoint']}")
                report.append(f"     响应时间: {ep['response_time']}秒")
                report.append(f"     测试响应: {ep['content'][:50]}...")
                report.append("")
            
            # 推荐最佳端点
            best = min(working_endpoints, key=lambda x: x["response_time"])
            report.append(f"🏆 推荐端点: {best['endpoint']} ({best['response_time']}秒)")
        else:
            report.append("⚠️  未找到可用端点")
            report.append("")
            report.append("💡 建议:")
            report.append("  1. 确认 API Key 是否正确")
            report.append("  2. 获取正确的 API 端点 URL")
            report.append("  3. 检查网络连接")
            report.append("  4. 确认服务是否可用")
        
        report.append("="*60)
        return "\n".join(report)


def main():
    print("🚀 Coding Plan Lite 配置工具")
    print("="*60)
    
    config = CodingPlanLiteConfig()
    
    # 发现端点
    working_endpoints = config.discover_endpoint()
    
    # 生成报告
    report = config.generate_report(working_endpoints)
    print("\n" + report)
    
    # 如果有可用端点，创建配置
    if working_endpoints:
        # 选择最佳端点
        best_endpoint = min(working_endpoints, key=lambda x: x["response_time"])["endpoint"]
        
        print(f"\n🔧 使用最佳端点创建配置: {best_endpoint}")
        
        # 创建配置文件
        config_file = config.create_config_file(best_endpoint)
        
        # 更新 models.json
        if config.update_models_json(best_endpoint):
            print("\n✅ 配置完成!")
            print(f"   配置文件: {config_file}")
            print(f"   模型ID: codingplan/codingplan-lite")
            print(f"   稍后使用命令: openclaw models use codingplan/codingplan-lite")
        else:
            print("\n⚠️  配置部分完成，需要手动更新 models.json")
    else:
        print("\n❌ 未找到可用端点，无法创建配置")
        print("💡 请提供正确的 API 端点 URL")


if __name__ == "__main__":
    main()
