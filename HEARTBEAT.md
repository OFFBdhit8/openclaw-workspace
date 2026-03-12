# HEARTBEAT.md

## 状态追踪
所有定时任务状态通过 `memory/report-state.json` 追踪，避免重复执行。
每次心跳先读取该文件，执行完毕后更新对应字段。

## 定时任务 ① 基础设施巡检（每次心跳）

每次心跳必做，快速过一遍：
- `systemctl --user status openclaw-gateway` — 主机 Gateway
- `systemctl --user status openclaw-gateway-rescue` — 救援机
- `cat /root/.openclaw-rescue/alert-gateway-down 2>/dev/null` — 告警文件
- `df -h /` — 磁盘 >85% 告警
- `free -h` — 内存状况
- 检查近期日志里是否出现新的 schema / profile / plugin conflict 噪音（unknown keys、tool conflict、tools.profile warning）
- 检查模型是否漂移（main / rescue 默认模型、thinkingDefault 是否被改坏）
- 发现问题先修，修不了再通知老板
- 全绿 → 不汇报，继续下一个任务

## 定时任务 ② 记忆代谢（每 6 小时）

读取 `report-state.json` 的 `lastMemoryReview`。
距上次 ≥ 6h（或为 null）→ 执行，否则跳过。

流程：
1. 读取自上次维护以来的 `memory/YYYY-MM-DD.md` 日志
2. 提炼写入 MEMORY.md：
   - 🏆 里程碑：重大进展、目标达成
   - 💡 教训：踩过的坑、失败方案、有效方法论
   - 📊 关键数据：指标变化、性能数据
   - 🔧 配置变更：环境/参数/工具链变化
   - 📝 决策记录：重要决策及原因
3. 清理 MEMORY.md 中过时信息（已完成的临时任务、已修复的 bug）
4. 合并重复条目，保持结构清晰
5. 更新 `lastMemoryReview`

原则：精炼不精简，保留关键细节和数据。不删原始日志。

## 定时任务 ③ 主动反思（每 4 小时）

读取 `report-state.json` 的 `lastSelfReflection`。
距上次 ≥ 4h（或为 null）→ 执行，否则跳过。

快速扫描近期对话，问自己：
1. 有没有犯错？什么错？根因是什么？
2. 有没有更好的做法？（工具选择、执行顺序、沟通方式）
3. 有没有重复出现的问题？（检查 `errorPatterns`）

教训路由：
- 工具问题 → 更新 TOOLS.md
- 流程/行为问题 → 更新 AGENTS.md
- 临时事实 → 写入 memory/YYYY-MM-DD.md
- 重复错误（≥2次同类）→ 写入 AGENTS.md 作为铁律 + 更新 errorPatterns

质量标准：
- 具体，不写"下次注意" — 写"下次用 X 代替 Y 因为 Z"
- 可执行，未来的我能直接照做
- 非显而易见，跳过常识
- 不重复已有教训

更新 `lastSelfReflection`。

## 定时任务 ④ 安全审计（每 12 小时）

读取 `report-state.json` 的 `lastSecurityAudit`。
距上次 ≥ 12h（或为 null）→ 执行，否则跳过。

**自动化部分（每晚 23:00 cron 自动跑）：**
`/root/.openclaw/workspace/scripts/nightly-security-audit.sh`
13 项检查：进程网络 / 目录变更 / Cron / SSH / 配置基线 / 磁盘 / 内存 / Gateway / 高资源进程 / 环境变量 / DLP / Skill 基线 / 黄线审计

**心跳补充检查（白天每 12h）：**
- 读取 `/tmp/openclaw/security-reports/report-YYYY-MM-DD.txt` 看昨晚巡检结果
- 有告警 → 通知老板
- 无告警 → 静默

## 定时任务 ⑤ 赚钱雷达（每 8 小时，白天）

仅白天 09:00-21:00 执行。轮换检查：
- 扫描 memory/opportunities/ 下的机会清单，有没有到期或需要跟进的
- 快速搜一下工作室相关领域的新动态（AI 工具、自动化、独立开发者赚钱）
- 涉及 X / 社区 / GitHub / 多平台调研时，先走平台 skill 和专用通道，失败后才降级，并明确标注降级来源
- 有值得关注的 → 简短通知老板
- 没有 → 静默

## 规则
- 深夜 23:00-08:00：仅执行 ① 巡检，其余全跳过，除非紧急
- 没有新情况就 HEARTBEAT_OK，不要为了说话而说话
- 发现问题先修，修不了再通知老板
- 所有定时任务执行后必须更新 report-state.json
- 汇报要具体有数据，不要笼统
