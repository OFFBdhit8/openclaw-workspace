# API 密钥管理（请妥善保管，勿泄露）

---

## 更新记录
- **最新更新时间：** 2026-02-25

---

### Deepseek
- **Key:** `sk-7c004758529f45c6ac42ec3e620c088d`
- **模型示例:** deepseek-chat, deepseek-coder
- **API端点:** `https://api.deepseek.com/v1/chat/completions`

### Kimi (Moonshot)
- **Key:** `sk-AeUlUSlTJR30ixssrvsksEU23TCFXEBPyg3gh1mZBSMqYu0h`
- **模型示例:** moonshot-v1-8k, moonshot-v1-32k, moonshot-v1-128k
- **API端点:** `https://api.moonshot.cn/v1/chat/completions`

### Minimax
- **Key 1:** `sk-api-3hOqY3VgQvbmm4xhi1zZXTVfKNg0046epcuvKWriFuy9C8sM7_UOwC4IsYL_WOAYB8TD0CDc0nbKlOdLt9k-s6mMQNcmw8XQlY6xiAYYVp_jZ3CUPeBwNAM`
- **Key 2:** `sk-api-KjHBXjbteMsG0tnfVGmpjDnWNvbp9rjzhSvh8ALzK9D8NhJ9wZQ4eVO95KNfrNeMgz3ncxckJWdjXtE40CVmXaFEeC3IW_TdBn8ZnaNRvpb0ZPml6Zu48QQ`
- **模型示例:** abab6.5-chat, abab6-chat
- **API端点:** `https://api.minimax.chat/v1/text/chatcompletion`

### Qwen (通义千问)
- **Key 1:** `sk-46ecd3efbdd540af82eb4a2c763b72d6` ✅ (当前使用)

### Coding Plan Lite (阿里云 Model Studio)
- **Key:** `sk-sp-14f905b909ee42e29a7fddf95250ad1b` ✅ (已配置)
- **API端点:** `https://coding.dashscope.aliyuncs.com/v1`
- **可用模型:** qwen-plus, qwen-turbo, qwen-max
- **默认模型:** qwen-plus
- **文档:** https://help.aliyun.com/zh/model-studio/coding-plan
- **状态:** ✅ 已配置完成，等待使用
- **配置时间:** 2026-02-25 14:06 UTC
- **模型示例:** qwen-turbo, qwen-plus, qwen-max
- **API端点 (国内/华北2):** `https://dashscope.aliyuncs.com/compatible-mode/v1`
- **API端点 (新加坡):** `https://dashscope-intl.aliyuncs.com/compatible-mode/v1`
- **API端点 (美国):** `https://dashscope-us.aliyuncs.com/compatible-mode/v1`

### 豆包 (ByteDance) - ❌ 已移除
- **状态:** 不可用 (404 错误)
- **Key:** `51d28c39-105f-4325-b206-ca8b6056ae8a` (保留但不使用)
- **原因:** 模型/端点配置问题，暂时移除

### 腾讯混元
- **Key:** `sk-qv0tltkn0dztn4ghhyeBg5TnXQ58QKc0ClmAk3ogb07zNCTH`
- **模型示例:** hunyuan-standard, hunyuan-pro
- **API端点:** `https://hunyuan.tencentcloudapi.com`（需腾讯云签名）或使用 `https://api.hunyuan.cloud.tencent.com/v1/chat/completions`

### Moltbook 论坛 API
- **API Key:** `moltbook_sk_MDQ7Y7CU2cPX_yyxf6MM9ZZpXSAXZnYr`
- **用途:** 论坛浏览、发帖、评论
- **使用策略:**
  - 浏览: 使用 deepseek-chat (便宜量大)
  - 发帖/评论: 使用 Kimi/Deepseek premium (高质量)

---

## 🔐 安全提示

1. **永远不要将这些 Key 提交到 Git 仓库**
2. **不要在代码中硬编码这些 Key**
3. **建议通过环境变量或密钥管理服务使用**
4. **定期轮换 API Key**

---

## 📞 调用示例

见同目录 `api_call_examples.md` 或运行 `python scripts/multi_model_dispatcher.py`
