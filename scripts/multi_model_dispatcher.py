import os
import argparse
import requests
import json

# =============================================
# 多模型 API 调用管理器（支持自由切换模型）
# 所有 API Key 通过环境变量传入，安全且灵活
# =============================================

# ---------------------
# 模型配置
# ---------------------

MODELS_CONFIG = {
    "腾讯混元": {
        "api_key_env": "HUNYUAN_API_KEY",
        "api_base": "https://hunyuan.tencentcloudapi.com",  # 请根据腾讯云官方文档替换为实际接入点
        "model_name": "hunyuan-standard",  # 示例，请按实际文档填写
        "api_type": "http_json",  # 模拟 HTTP JSON 请求，实际可能需签名
        "prompt_field": "messages",
        "example_payload": {
            "messages": [{"role": "user", "content": "{prompt}"}],
            "stream": False
        }
    },
    "Kimi": {
        "api_key_env": "KIMI_API_KEY",
        "api_base": "https://api.moonshot.cn/v1/chat/completions",  # 官方示例，请确认
        "model_name": "moonshot-v1-8k",
        "api_type": "http_json",
        "prompt_field": "messages",
        "example_payload": {
            "model": "moonshot-v1-8k",
            "messages": [{"role": "user", "content": "{prompt}"}],
            "stream": False
        }
    },
    "Deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "api_base": "https://api.deepseek.com/v1/chat/completions",  # 请根据实际文档调整
        "model_name": "deepseek-chat",
        "api_type": "http_json",
        "prompt_field": "messages",
        "example_payload": {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": "{prompt}"}],
            "stream": False
        }
    },
    "Qwen": {
        "api_key_env": "QWEN_API_KEY",
        "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        "model_name": "qwen-turbo",
        "api_type": "http_json",
        "prompt_field": "messages",
        "example_payload": {
            "model": "qwen-turbo",
            "messages": [{"role": "user", "content": "{prompt}"}],
            "stream": False
        }
    },
    "minimax": {
        "api_key_env": "MINIMAX_API_KEY",
        "api_base": "https://api.minimax.chat/v1/text/chatcompletion",  # 请根据实际文档调整
        "model_name": "abab6.5-chat",  # 示例模型
        "api_type": "http_json",
        "prompt_field": "messages",
        "example_payload": {
            "model": "abab6.5-chat",
            "messages": [{"role": "user", "content": "{prompt}"}],
            "stream": False
        }
    },
}

# ---------------------
# 工具函数：获取环境变量中的 API Key
# ---------------------
def get_api_key(model_name):
    env_var = MODELS_CONFIG.get(model_name, {}).get("api_key_env")
    if not env_var:
        raise ValueError(f"未找到模型 '{model_name}' 的 API Key 环境变量配置")
    api_key = os.getenv(env_var)
    if not api_key:
        raise ValueError(f"请设置环境变量 {env_var}，值为 {model_name} 的 API Key")
    return api_key

# ---------------------
# 工具函数：调用模型 API
# ---------------------
def call_model_api(model_name, prompt):
    config = MODELS_CONFIG.get(model_name)
    if not config:
        raise ValueError(f"未支持的模型：{model_name}。支持的模型有：{list(MODELS_CONFIG.keys())}")

    api_key = get_api_key(model_name)
    api_base = config["api_base"]
    api_type = config.get("api_type", "http_json")
    example_payload = config.get("example_payload", {})
    prompt_field = config.get("prompt_field", "messages")

    print(f"[信息] 正在调用模型：{model_name}")
    print(f"[信息] API Base: {api_base}")
    print(f"[信息] 使用 API Key 环境变量: {config['api_key_env']}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"  # 部分模型可能要求 API Key 在 Header 或 Body 中，请按实际调整
    }

    # 构造 payload（将 {prompt} 动态替换为用户输入）
    payload = example_payload.copy()
    if isinstance(payload, dict) and prompt_field in payload:
        if isinstance(payload[prompt_field], list):
            for msg in payload[prompt_field]:
                if msg.get("content", "").startswith('{prompt}'):
                    msg["content"] = msg["content"].format(prompt=prompt)
        elif isinstance(payload[prompt_field], str):
            payload[prompt_field] = payload[prompt_field].format(prompt=prompt)
    else:
        # 简单回退：直接构造 messages
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }

    try:
        response = requests.post(api_base, headers=headers, data=json.dumps(payload), timeout=15)
        if response.status_code == 200:
            result = response.json()
            print(f"[✅ {model_name}] API 调用成功！\n返回：{json.dumps(result, ensure_ascii=False, indent=2)}")
            return result
        else:
            print(f"[❌ {model_name}] API 调用失败，状态码：{response.status_code}，返回内容：{response.text}")
            return None
    except Exception as e:
        print(f"[❌ {model_name}] API 请求异常：{str(e)}")
        return None

# ---------------------
# 主函数
# ---------------------
def main():
    parser = argparse.ArgumentParser(description="多模型 AI API 切换调用脚本")
    parser.add_argument("--model", type=str, required=True, help="要调用的模型名称，如：腾讯混元、Kimi、Deepseek、Qwen、minimax、豆包")
    parser.add_argument("--prompt", type=str, required=True, help="要发送给模型的提问或指令")
    args = parser.parse_args()

    model_name = args.model
    prompt = args.prompt

    if model_name not in MODELS_CONFIG:
        supported = list(MODELS_CONFIG.keys())
        print(f"[错误] 不支持的模型：{model_name}\n支持的模型有：{supported}")
        return

    call_model_api(model_name, prompt)

if __name__ == "__main__":
    main()

# =====================================
# 使用方法
# =====================================
#
# 1. 设置你的各个模型 API Key 为环境变量，例如：
#    export HUNYUAN_API_KEY='sk-qv0tltkn0dztn4ghhyeBg5TnXQ58QKc0ClmAk3ogb07zNCTH'
#    export KIMI_API_KEY='sk-AeUlUSlTJR30ixssrvsksEU23TCFXEBPyg3gh1mZBSMqYu0h'
#    export DEEPSEEK_API_KEY='sk-7c004758529f45c6ac42ec3e620c088d'
#    export QWEN_API_KEY='sk-46ecd3efbdd540af82eb4a2c763b72d6'
#    export MINIMAX_API_KEY='sk-api-3hOqY3VgQvbmm4xhi1zZXTVfKNg0046epcuvKWriFuy9C8sM7_UOwC4IsYL_WOAYB8TD0CDc0nbKlOdLt9k-s6mMQNcmw8XQlY6xiAYYVp_jZ3CUPeBwNAM'
#    export DOUBAO_API_KEY='51d28c39-105f-4325-b206-ca8b6056ae8a'
#
# 2. 运行脚本，指定模型和问题，例如：
#    python scripts/multi_model_dispatcher.py --model 腾讯混元 --prompt "你好，请介绍一下自己"
#    python scripts/multi_model_dispatcher.py --model kimi --prompt "今天天气如何？"
#    python scripts/multi_model_dispatcher.py --model Qwen --prompt "帮我写个 Python 函数"
#
# =====================================

# 注意：
# - 部分模型（如腾讯混元、Qwen）可能使用腾讯云/阿里云官方 API，需要按其官方文档进行签名或使用 SDK
# - 本脚本为通用 HTTP 方式，部分模型可能需要调整 API Base、headers、签名、请求体结构
# - 你可以根据实际返回结果进一步解析和优化
