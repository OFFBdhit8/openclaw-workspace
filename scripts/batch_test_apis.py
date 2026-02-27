#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量测试所有 AI 模型 API 可用性
测试模型：Deepseek、Kimi、Minimax、Qwen、豆包、腾讯混元
"""

import os
import json
import time
import requests
from datetime import datetime

# 模型配置
MODELS_CONFIG = {
    "Deepseek": {
        "api_key": "sk-7c004758529f45c6ac42ec3e620c088d",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-chat",
        "headers": lambda key: {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        "payload": lambda model, prompt: {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "stream": False
        }
    },
    "Kimi": {
        "api_key": "sk-AeUlUSlTJR30ixssrvsksEU23TCFXEBPyg3gh1mZBSMqYu0h",
        "api_url": "https://api.moonshot.cn/v1/chat/completions",
        "model": "moonshot-v1-8k",
        "headers": lambda key: {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        "payload": lambda model, prompt: {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "stream": False
        }
    },
    "Minimax": {
        "api_key": "sk-api-3hOqY3VgQvbmm4xhi1zZXTVfKNg0046epcuvKWriFuy9C8sM7_UOwC4IsYL_WOAYB8TD0CDc0nbKlOdLt9k-s6mMQNcmw8XQlY6xiAYYVp_jZ3CUPeBwNAM",
        "api_url": "https://api.minimax.chat/v1/text/chatcompletion",
        "model": "abab6.5-chat",
        "headers": lambda key: {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        "payload": lambda model, prompt: {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "stream": False
        }
    },
    "Qwen": {
        "api_key": "sk-46ecd3efbdd540af82eb4a2c763b72d6",
        "api_url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "model": "qwen-turbo",
        "headers": lambda key: {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        "payload": lambda model, prompt: {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "stream": False
        }
    },
    "腾讯混元": {
        "api_key": "sk-qv0tltkn0dztn4ghhyeBg5TnXQ58QKc0ClmAk3ogb07zNCTH",
        "api_url": "https://api.hunyuan.cloud.tencent.com/v1/chat/completions",
        "model": "hunyuan-standard",
        "headers": lambda key: {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        "payload": lambda model, prompt: {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100,
            "stream": False
        }
    }
}

TEST_PROMPT = "你好，请回复一个简短的问候，只需说'API测试成功'即可。"

def test_model(model_name, config):
    """测试单个模型 API"""
    print(f"\n{'='*50}")
    print(f"🧪 正在测试: {model_name}")
    print(f"{'='*50}")
    
    start_time = time.time()
    result = {
        "model": model_name,
        "status": "unknown",
        "response_time": 0,
        "status_code": None,
        "error": None,
        "content": None
    }
    
    try:
        api_key = config["api_key"]
        api_url = config["api_url"]
        model = config["model"]
        
        print(f"  📡 API URL: {api_url}")
        print(f"  🤖 Model: {model}")
        print(f"  🔑 API Key: {api_key[:20]}...")
        
        headers = config["headers"](api_key)
        payload = config["payload"](model, TEST_PROMPT)
        
        print(f"  📤 发送请求...")
        
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        result["response_time"] = round(time.time() - start_time, 2)
        result["status_code"] = response.status_code
        
        if response.status_code == 200:
            data = response.json()
            result["status"] = "✅ 成功"
            
            # 尝试提取返回内容
            try:
                if model_name == "Qwen":
                    content = data.get("output", {}).get("choices", [{}])[0].get("message", {}).get("content", "")
                else:
                    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                result["content"] = content[:100] if content else "无内容"
            except:
                result["content"] = "解析内容失败"
            
            print(f"  ✅ 状态: 成功")
            print(f"  ⏱️  响应时间: {result['response_time']}s")
            print(f"  💬 回复预览: {result['content'][:50]}...")
            
        else:
            result["status"] = "❌ 失败"
            result["error"] = f"HTTP {response.status_code}: {response.text[:200]}"
            print(f"  ❌ 状态: 失败")
            print(f"  📛 状态码: {response.status_code}")
            print(f"  📝 错误信息: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        result["status"] = "⏱️ 超时"
        result["error"] = "请求超时 (>30s)"
        print(f"  ⏱️ 状态: 超时")
        
    except requests.exceptions.ConnectionError:
        result["status"] = "🔌 连接错误"
        result["error"] = "无法连接到 API 服务器"
        print(f"  🔌 状态: 连接错误")
        
    except Exception as e:
        result["status"] = "💥 异常"
        result["error"] = str(e)
        print(f"  💥 状态: 异常")
        print(f"  🐛 错误: {str(e)}")
    
    return result

def generate_report(results):
    """生成测试报告"""
    print(f"\n{'='*60}")
    print("📊 API 批量测试报告")
    print(f"{'='*60}")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # 统计
    total = len(results)
    success = sum(1 for r in results if "成功" in r["status"])
    failed = total - success
    
    print(f"📈 统计概览:")
    print(f"   总计测试: {total} 个模型")
    print(f"   ✅ 成功: {success} 个")
    print(f"   ❌ 失败: {failed} 个")
    print()
    
    # 详细结果表格
    print(f"{'模型名称':<12} {'状态':<10} {'响应时间':<10} {'状态码':<8} {'备注'}")
    print("-" * 70)
    
    for r in results:
        status_icon = "✅" if "成功" in r["status"] else "❌"
        status_text = r["status"].replace("✅ ", "").replace("❌ ", "").replace("⏱️ ", "").replace("🔌 ", "").replace("💥 ", "")
        response_time = f"{r['response_time']}s" if r["response_time"] > 0 else "-"
        status_code = str(r["status_code"]) if r["status_code"] else "-"
        note = r["error"][:25] if r["error"] else (r["content"][:25] if r["content"] else "OK")
        
        print(f"{r['model']:<12} {status_icon} {status_text:<8} {response_time:<10} {status_code:<8} {note}")
    
    print()
    print(f"{'='*60}\n")
    
    # 保存详细报告到文件
    report_file = "logs/api_test_report.json"
    os.makedirs("logs", exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "summary": {
                "total": total,
                "success": success,
                "failed": failed
            },
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"📁 详细报告已保存到: {report_file}")

def main():
    """主函数：批量测试所有模型"""
    print("🚀 开始批量测试所有 AI 模型 API...")
    print(f"📝 测试提示词: '{TEST_PROMPT}'")
    print(f"⏱️  超时设置: 30秒")
    
    results = []
    
    for model_name, config in MODELS_CONFIG.items():
        result = test_model(model_name, config)
        results.append(result)
        time.sleep(1)  # 避免请求过快
    
    # 生成报告
    generate_report(results)
    
    print("\n✨ 批量测试完成！")

if __name__ == "__main__":
    main()
