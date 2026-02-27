# 多模型 API 调用示例

本文件提供各个模型的直接调用示例，帮助你快速测试和使用这些 API。

---

## 🛠️ 快速使用方法

### 方法1：使用多模型切换脚本（推荐）

```bash
# 先设置环境变量
export DEEPSEEK_API_KEY='sk-7c004758529f45c6ac42ec3e620c088d'
export KIMI_API_KEY='sk-AeUlUSlTJR30ixssrvsksEU23TCFXEBPyg3gh1mZBSMqYu0h'
export MINIMAX_API_KEY='sk-api-3hOqY3VgQvbmm4xhi1zZXTVfKNg0046epcuvKWriFuy9C8sM7_UOwC4IsYL_WOAYB8TD0CDc0nbKlOdLt9k-s6mMQNcmw8XQlY6xiAYYVp_jZ3CUPeBwNAM'
export QWEN_API_KEY='sk-sp-14f905b909ee42e29a7fddf95250ad1b'
export DOUBAO_API_KEY='51d28c39-105f-4325-b206-ca8b6056ae8a'
export HUNYUAN_API_KEY='sk-qv0tltkn0dztn4ghhyeBg5TnXQ58QKc0ClmAk3ogb07zNCTH'

# 然后运行
python scripts/multi_model_dispatcher.py --model Deepseek --prompt "你好"
python scripts/multi_model_dispatcher.py --model Kimi --prompt "你好"
python scripts/multi_model_dispatcher.py --model Qwen --prompt "你好"
```

---

## 📜 各模型直接调用示例

### 1. Deepseek

```python
import requests
import os

api_key = os.getenv('DEEPSEEK_API_KEY', 'sk-7c004758529f45c6ac42ec3e620c088d')
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'deepseek-chat',
    'messages': [{'role': 'user', 'content': '你好，请介绍一下自己'}],
    'stream': False
}
response = requests.post('https://api.deepseek.com/v1/chat/completions', headers=headers, json=data)
print(response.json())
```

### 2. Kimi (Moonshot)

```python
import requests
import os

api_key = os.getenv('KIMI_API_KEY', 'sk-AeUlUSlTJR30ixssrvsksEU23TCFXEBPyg3gh1mZBSMqYu0h')
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'moonshot-v1-8k',
    'messages': [{'role': 'user', 'content': '你好，请介绍一下自己'}],
    'stream': False
}
response = requests.post('https://api.moonshot.cn/v1/chat/completions', headers=headers, json=data)
print(response.json())
```

### 3. Minimax

```python
import requests
import os

api_key = os.getenv('MINIMAX_API_KEY', 'sk-api-3hOqY3VgQvbmm4xhi1zZXTVfKNg0046epcuvKWriFuy9C8sM7_UOwC4IsYL_WOAYB8TD0CDc0nbKlOdLt9k-s6mMQNcmw8XQlY6xiAYYVp_jZ3CUPeBwNAM')
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'abab6.5-chat',
    'messages': [{'role': 'user', 'content': '你好，请介绍一下自己'}],
    'stream': False
}
response = requests.post('https://api.minimax.chat/v1/text/chatcompletion', headers=headers, json=data)
print(response.json())
```

### 4. Qwen (通义千问)

```python
import requests
import os

api_key = os.getenv('QWEN_API_KEY', 'sk-sp-14f905b909ee42e29a7fddf95250ad1b')
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'qwen-turbo',
    'messages': [{'role': 'user', 'content': '你好，请介绍一下自己'}],
    'stream': False
}
response = requests.post('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', headers=headers, json=data)
print(response.json())
```

### 5. 豆包 (ByteDance)

```python
import requests
import os

api_key = os.getenv('DOUBAO_API_KEY', '51d28c39-105f-4325-b206-ca8b6056ae8a')
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'doubao-pro-4k',
    'messages': [{'role': 'user', 'content': '你好，请介绍一下自己'}],
    'stream': False
}
response = requests.post('https://ark.cn-beijing.volces.com/api/v3/chat/completions', headers=headers, json=data)
print(response.json())
```

### 6. 腾讯混元

```python
import requests
import os

api_key = os.getenv('HUNYUAN_API_KEY', 'sk-qv0tltkn0dztn4ghhyeBg5TnXQ58QKc0ClmAk3ogb07zNCTH')
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
data = {
    'model': 'hunyuan-standard',
    'messages': [{'role': 'user', 'content': '你好，请介绍一下自己'}],
    'stream': False
}
response = requests.post('https://api.hunyuan.cloud.tencent.com/v1/chat/completions', headers=headers, json=data)
print(response.json())
```

---

## 📚 更多资源

- Deepseek API 文档: https://platform.deepseek.com/api-docs
- Kimi API 文档: https://platform.moonshot.cn/docs/api-reference
- Minimax API 文档: https://platform.minimaxi.com/document
- Qwen API 文档: https://help.aliyun.com/zh/dashscope/
- 豆包 API 文档: https://www.volcengine.com/docs/82379
- 腾讯混元 API 文档: https://cloud.tencent.com/document/product/1759
