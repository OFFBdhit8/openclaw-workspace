# 本地模型部署方案

**服务器配置**: 腾讯云 VPS · 2 核 CPU · 4GB 内存 · 60GB 系统盘

---

## 📊 资源分析

| 项目 | 数值 |
|------|------|
| 总内存 | 3.6GB |
| 已用内存 | 1.9GB |
| **可用内存** | **~1.7GB** |
| CPU | 2 核 (无 GPU) |
| 系统盘 | 60GB (剩余 23GB) |

---

## 🎯 推荐模型（按优先级）

### 方案 A：Ollama + Qwen2.5-3B（推荐）

| 项目 | 详情 |
|------|------|
| **模型** | `qwen2.5:3b` (GGUF Q4_K_M 量化) |
| **内存占用** | ~2GB |
| **推理速度** | ~5-10 tokens/s (CPU) |
| **适用场景** | 心跳检查、简单对话、文本分类 |
| **优点** | 中文优秀、安装简单、社区支持好 |
| **缺点** | 需要 swap 支持 |

**安装命令**:
```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull qwen2.5:3b

# 测试
ollama run qwen2.5:3b "你好"
```

---

### 方案 B：Ollama + Phi-3-mini

| 项目 | 详情 |
|------|------|
| **模型** | `phi3:mini` (3.8B, Q4 量化) |
| **内存占用** | ~2.5GB |
| **推理速度** | ~3-8 tokens/s (CPU) |
| **适用场景** | 英文任务、逻辑推理 |
| **优点** | 微软出品、推理能力强 |
| **缺点** | 中文稍弱、内存占用高 |

---

### 方案 C：llama.cpp + TinyLlama（最轻量）

| 项目 | 详情 |
|------|------|
| **模型** | TinyLlama-1.1B-Chat (GGUF Q4_K_M) |
| **内存占用** | ~1GB |
| **推理速度** | ~15-30 tokens/s (CPU) |
| **适用场景** | 极简单任务、快速响应 |
| **优点** | 最轻量、速度最快 |
| **缺点** | 能力有限、中文一般 |

**安装命令**:
```bash
# 安装 llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# 下载模型
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf

# 运行
./main -m tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -p "你好" -n 128
```

---

### 方案 D：Ollama + Gemma-2-2b（平衡方案）

| 项目 | 详情 |
|------|------|
| **模型** | `gemma2:2b` |
| **内存占用** | ~1.5GB |
| **推理速度** | ~10-20 tokens/s (CPU) |
| **适用场景** | 通用任务、平衡性能 |
| **优点** | Google 出品、内存友好 |
| **缺点** | 中文不如 Qwen |

---

## 🔧 系统优化建议

### 1. 增加 Swap 空间（必须）

```bash
# 创建 4GB swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 永久生效
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 2. 优化 Ollama 配置

```bash
# 创建 systemd 服务配置
sudo mkdir -p /etc/systemd/system/ollama.service.d/
sudo tee /etc/systemd/system/ollama.service.d/override.conf << EOF
[Service]
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_CONTEXT_LENGTH=2048"
EOF

sudo systemctl daemon-reload
sudo systemctl restart ollama
```

---

## 📋 OpenClaw 配置

### 添加本地模型到配置

```json
{
  "providers": {
    "local": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "models": [
        {
          "id": "qwen2.5:3b",
          "name": "Qwen2.5 3B (Local)"
        }
      ]
    }
  }
}
```

### 心跳任务使用本地模型

修改 cron 任务或心跳配置，指定使用 `local/qwen2.5:3b`。

---

## 🎯 最终推荐

**针对你的配置，推荐方案 A（Ollama + Qwen2.5-3B）**:

1. **中文优秀** - 适合心跳检查的中文任务
2. **安装简单** - Ollama 一键安装
3. **社区活跃** - 问题容易解决
4. **OpenClaw 兼容** - 支持 OpenAI 兼容 API

**前提条件**: 必须先配置 4GB swap 空间

---

## ⚠️ 注意事项

1. **CPU 推理较慢** - 简单任务 5-10 秒，复杂任务可能 30 秒+
2. **内存紧张** - 必须配置 swap，否则可能 OOM
3. **并发限制** - 建议设置 `OLLAMA_NUM_PARALLEL=1`
4. **网络依赖** - 首次拉取模型需要下载 ~2GB

---

## 📞 下一步

1. 确认是否安装 Ollama
2. 配置 swap 空间
3. 拉取推荐模型
4. 测试本地模型
5. 配置 OpenClaw 使用本地模型

需要我帮你执行安装吗？
