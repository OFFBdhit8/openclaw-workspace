import os
import requests
import json

# =====================
# 腾讯混元 API 测试脚本
# 使用环境变量读取 API Key
# =====================

# --- 配置项 ---
API_KEY_ENV_VAR = "HUNYUAN_API_KEY"             # 环境变量名
API_BASE_URL = "https://hunyuan.tencentcloudapi.com"  # 混元 API 接入点（示例，请根据实际文档调整）

# 如果是腾讯云官方 API，通常使用类似下面的 endpoint 和请求方式，请根据实际 SDK 或文档调整
# 以下为模拟请求，真实调用请参考：https://cloud.tencent.com/document/product/1759

# --- 准备请求 ---
def test_hunyuan_api():
    api_key = os.getenv(API_KEY_ENV_VAR)
    if not api_key:
        print(f"[错误] 请设置环境变量 {API_KEY_ENV_VAR}，值为你的腾讯混元 API Key")
        return

    print(f"[信息] 正在测试腾讯混元 API，使用环境变量中的 API Key")

    # 注意：以下为示例请求，腾讯混元实际 API 可能使用腾讯云 API 3.0，需要签名、region、endpoint 等
    # 请根据腾讯云官方文档进行调整，下面只是一个模拟的“文本生成”请求结构
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",  # 有些平台使用 Bearer，有些用 API Key 在 body 或 header 中传递，请按文档来
        # 实际使用中可能需要 X-TC-Action, X-TC-Version, X-TC-Region 等头部
    }

    payload = {
        "messages": [
            {"role": "user", "content": "你好，请介绍一下你自己"}
        ],
        "stream": False
    }

    try:
        # 注意：这里只是示例 URL，请根据腾讯混元真实的 API 文档填写正确的接入点和路径
        # 例如：可能是 https://hunyuan.api.tencentcloudapi.com 或通过 SDK 调用
        response = requests.post(
            API_BASE_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            print(f"[腾讯混元] API 调用成功！返回内容：\n{json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"[腾讯混元] API 调用失败，状态码：{response.status_code}，返回：{response.text}")
    except Exception as e:
        print(f"[腾讯混元] API 请求异常：{str(e)}")


if __name__ == "__main__":
    test_hunyuan_api()

# =====================
# 使用方法：
# 1. 将你的腾讯混元 API Key 设置为环境变量 HUNYUAN_API_KEY
#    - 例如在终端执行：export HUNYUAN_API_KEY='sk-qv0tltkn0dztn4ghhyeBg5TnXQ58QKc0ClmAk3ogb07zNCTH'
# 2. 运行此脚本：python test_hunyuan.py
# 3. 查看返回结果，判断是否调用成功
# =====================

# 注意：腾讯混元实际 API 可能需要使用腾讯云 API 3.0 签名机制，请以官方文档为准
# 本脚本仅为通用 HTTP 请求示例，可能需要根据实际接口调整 URL / Headers / Body
