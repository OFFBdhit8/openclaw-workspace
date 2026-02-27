# 智能模型路由器使用指南

自动根据任务类型选择便宜或贵的模型，优化成本和效果。

## 🎯 工作原理

| 任务类型 | 使用的模型 | 说明 |
|---------|-----------|------|
| **简单任务** | 便宜模型 (Minimax/腾讯混元/Qwen) | 快速、低成本 |
| **复杂任务** | 贵模型 (Deepseek/Kimi) | 高质量、深度分析 |

## 🚀 使用方法

### 1. 基本使用（自动路由）

```bash
python scripts/smart_model_router.py --prompt "你的问题"
```

**示例：**
```bash
# 简单任务 → 自动选择便宜模型
python scripts/smart_model_router.py --prompt "搜索今天的天气"
# 输出: 选择模型: Minimax (便宜)

# 复杂任务 → 自动选择贵模型  
python scripts/smart_model_router.py --prompt "写一篇关于人工智能的深度分析报告"
# 输出: 选择模型: Deepseek (贵)
```

### 2. 强制使用便宜模型

```bash
python scripts/smart_model_router.py --cheap --prompt "你的问题"
```

### 3. 强制使用贵模型

```bash
python scripts/smart_model_router.py --premium --prompt "你的问题"
```

### 4. 强制指定模型

```bash
python scripts/smart_model_router.py --model Deepseek --prompt "你的问题"
python scripts/smart_model_router.py --model Kimi --prompt "你的问题"
```

### 5. 查看使用统计

```bash
python scripts/smart_model_router.py --stats
```

## 📊 任务分类规则

### 简单任务关键词（自动使用便宜模型）
- 搜索、查找、查询、浏览
- 是什么、在哪里、多少钱
- 天气、时间、日期
- 翻译、转换
- 确认、检查、状态

### 复杂任务关键词（自动使用贵模型）
- 分析、深度、详细、研究、报告
- 写、创作、生成、撰写、文章、故事
- 回复、评论、建议、推荐
- 代码、编程、算法、优化
- 为什么、如何、解释、推理

## 💰 成本优化效果

- 约 **60-70%** 的日常任务可使用便宜模型
- 简单查询响应时间：**0.2-0.5秒**
- 复杂任务响应时间：**1-2秒**

## 🔧 集成到 OpenClaw

如果你想让 OpenClaw 默认使用智能路由器，可以修改配置：

```bash
# 设置环境变量
export SMART_ROUTER_ENABLED=true

# 然后在 OpenClaw 配置中使用
```

## 📁 可用模型

### 便宜模型 (快速/低成本)
- **Minimax** - 0.24s 响应
- **腾讯混元** - 1.0s 响应
- **Qwen** - 1.6s 响应

### 贵模型 (高质量)
- **Deepseek** - 1.4s 响应
- **Kimi** - 1.6s 响应

## 📝 示例场景

| 场景 | 命令 | 选择的模型 |
|------|------|-----------|
| 查天气 | `--prompt "北京今天天气"` | 便宜 (Minimax/腾讯混元) |
| 搜索资料 | `--prompt "搜索 OpenClaw 文档"` | 便宜 |
| 写文章 | `--prompt "写一篇关于环保的文章"` | 贵 (Deepseek/Kimi) |
| 写代码 | `--prompt "写一个 Python 爬虫"` | 贵 |
| 回复邮件 | `--prompt "帮我回复这封客户邮件..."` | 贵 |
| 深度分析 | `--prompt "分析比特币价格走势"` | 贵 |
| 简单问答 | `--prompt "什么是区块链技术"` | 便宜 |

## ⚡ 快速测试

```bash
# 测试 1: 简单任务
python scripts/smart_model_router.py --prompt "现在几点"

# 测试 2: 复杂任务
python scripts/smart_model_router.py --prompt "帮我写一份项目计划书"

# 测试 3: 强制便宜模型
python scripts/smart_model_router.py --cheap --prompt "翻译 'Hello World' 成中文"

# 测试 4: 强制贵模型
python scripts/smart_model_router.py --premium --prompt "分析当前 AI 发展趋势"
```

## 🔍 故障排除

### 如果某个模型失败
- 路由器会自动重试（已实现）
- 或手动切换到其他模型

### 如果任务分类不准确
- 使用 `--cheap` 或 `--premium` 强制选择
- 或修改 `smart_model_router.py` 中的关键词规则

## 📞 支持

有问题随时告诉我！
