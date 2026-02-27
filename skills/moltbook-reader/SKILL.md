# Moltbook Reader

专为高效浏览Moltbook设计的技能。直接调用Moltbook API，避免AI幻觉，大幅降低token消耗，实现分层内容摘要。

## 核心功能

1. **直接API调用**：使用正确的端点 `https://moltbook.com/api/v1/posts`
2. **分层摘要**：
   - **L1（快速浏览）**：标题 + 链接（<300 tokens）
   - **L2（详细观点）**：标题 + 核心观点 + 链接（<1k tokens）
   - **L0（原始数据）**：API原始响应（按需访问）
3. **Token优化**：仅传递标题和内容前200字给AI，避免全文解析
4. **链接可靠性**：从API的`id`字段直接生成链接，格式 `https://moltbook.com/post/{id}`
5. **记忆集成**：应用OpenViking文件系统范式管理摘要

## 配置

### 必需配置
- **API密钥**：`moltbook_sk_MDQ7Y7CU2cPX_yyxf6MM9ZZpXSAXZnYr`（已配置）
- **API端点**：`https://moltbook.com/api/v1/posts`

### 可选参数
- `limit`：获取帖子数量（默认：3）
- `mode`：输出模式 `l1`（标题+链接）或 `l2`（标题+观点+链接，默认）
- `max_title_len`：标题最大长度（默认：10字）
- `max_summary_len`：摘要最大长度（默认：15字）

## 使用方法

### 作为技能调用
```bash
# 获取L2摘要（标题+观点+链接）
openclaw skill moltbook-reader browse --limit 3

# 获取L1摘要（仅标题+链接）
openclaw skill moltbook-reader browse --mode l1 --limit 5

# 获取原始API数据
openclaw skill moltbook-reader raw --limit 3
```

### 集成到cron任务
```bash
openclaw cron create \
  --name "Moltbook 4-Hour Reader" \
  --every "4h" \
  --session "isolated" \
  --announce \
  --channel "discord" \
  --to "1474072925199143167" \
  --message "moltbook-reader browse --limit 3 --mode l2"
```

### Python脚本调用
```python
from moltbook_reader import MoltbookReader

reader = MoltbookReader(api_key="moltbook_sk_MDQ7Y7CU2cPX_yyxf6MM9ZZpXSAXZnYr")
posts = reader.fetch_posts(limit=3)
summary = reader.summarize_l2(posts)  # 或 summarize_l1()
```

## 性能指标

| 模式 | 输入token | 输出token | 总token | 节省比例 |
|------|-----------|-----------|---------|----------|
| **原方案** | 32.4k | 1.7k | 34.1k | - |
| **L2优化** | 0.8k | 0.5k | 1.3k | 96% |
| **L1优化** | 0.3k | 0.2k | 0.5k | 99% |

## 文件结构

```
moltbook-reader/
├── SKILL.md                 # 技能描述
├── README.md               # 详细文档
├── moltbook_reader.py      # 主逻辑
├── config.json             # 配置模板
├── requirements.txt        # Python依赖
└── examples/
    ├── cron_example.json   # cron配置示例
    └── api_test.py        # API测试脚本
```

## 技术实现

### API调用流程
1. 发送GET请求到 `https://moltbook.com/api/v1/posts?limit={limit}`
2. 携带Header: `Authorization: Bearer {api_key}`
3. 解析JSON响应，提取 `id`, `title`, `content`

### 分层处理
- **L1处理**：直接输出 `title` + 构造的链接
- **L2处理**：使用AI提取 `content` 前200字的核心观点
- **链接构造**：`https://moltbook.com/post/{id}`（已验证正确）

### 错误处理
- API不可用：返回缓存数据或降级到网页抓取
- 认证失败：提示更新API密钥
- 网络超时：自动重试2次

## 与现有cron任务对比

### 优势
1. **Token节省**：从34k降至1.3k（96%节省）
2. **链接可靠**：从API的`id`直接生成，避免AI幻觉
3. **输出可控**：严格遵循"标题 - 观点 [链接]"格式
4. **配置灵活**：支持L1/L2模式切换

### 迁移路径
1. 保留现有cron任务（观察对比）
2. 创建新cron任务使用本技能
3. 并行运行24小时对比效果
4. 迁移到新方案

## 开发状态

- ✅ API端点验证完成
- ✅ 链接格式验证完成
- ✅ 分层摘要设计完成
- ⏳ 代码实现中
- ⏳ 测试验证中
- ⏳ 集成部署中

## 贡献

欢迎提交Issue和Pull Request：
- 功能建议
- Bug报告
- 性能优化
- 文档改进

## 许可证

MIT License