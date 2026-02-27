# Brave API 配置指南

## 获取 Brave API Key

### 步骤 1: 注册 Brave Search API
1. 访问: https://brave.com/search/api/
2. 注册账户
3. 获取 API Key

### 步骤 2: 配置 OpenClaw

#### 方法 A: 环境变量
```bash
export BRAVE_API_KEY="your_api_key_here"
```

#### 方法 B: 配置文件
创建 `/root/.openclaw/config/brave.json`:
```json
{
  "api_key": "your_api_key_here",
  "endpoint": "https://api.search.brave.com/res/v1/web/search",
  "country": "US",
  "search_lang": "en"
}
```

#### 方法 C: 在代码中使用
```python
import os
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY", "your_api_key_here")
```

## 推荐的 ClawHub 技能

### 1. Token 优化类
- **token-saver** (v3.0.0) - Token 节省器
- **token-manager** (v1.2.0) - Token 管理器
- **openclaw-token-optimizer** (v1.4.3) - OpenClaw Token 优化器

### 2. Brave 搜索类
- **brave-search** (v1.0.1) - Brave 搜索技能
- **brave-api-search** (v2.1.1) - Brave API 搜索
- **brave-api-setup** (v0.1.2) - Brave API 设置

### 3. Discord 优化类
- **discord-chat** (v1.0.0) - Discord 聊天优化
- **discord-hub** (v1.1.0) - Discord 中心

## 当前系统状态

### ✅ 运行正常
- **Auberon Smart Bot:** 运行中 (PID: 848)
- **Python:** 3.11.6
- **Requests:** 2.32.3
- **内存使用:** 22.8 MB

### 📁 脚本文件
```
auberon_smart_bot.py      # 主Bot程序
moltbook_integration.py   # Moltbook集成
token_optimizer.py        # Token优化
ai_studio.py              # AI协作系统
```

### 🔧 建议优化

#### 立即执行:
1. **获取 Brave API Key** - 用于网页搜索
2. **安装 token-saver 技能** - 进一步优化Token使用
3. **配置环境变量** - 统一管理API密钥

#### 长期优化:
1. **监控 Token 使用** - 添加使用统计
2. **添加缓存机制** - 减少重复API调用
3. **优化模型选择算法** - 更精准的任务分类

## 安装命令示例

```bash
# 安装 Token 优化技能
clawhub install token-saver --dir /root/.openclaw/workspace/skills

# 安装 Brave 搜索技能
clawhub install brave-search --dir /root/.openclaw/workspace/skills

# 更新所有技能
clawhub update --dir /root/.openclaw/workspace/skills
```

## 注意事项
1. **速率限制:** ClawHub 有API调用限制
2. **API密钥安全:** 不要硬编码在代码中
3. **定期更新:** 保持技能最新版本
4. **测试:** 安装后测试功能是否正常
