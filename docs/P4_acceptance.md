# P4 日志与拓扑工具验收（2026-09-28）

P4.1–P4.7 的确定性工具已在独立工程实现并实测，不启动模型，不访问 Dify。M4 技术出口通过；日志时区、真实设备标识和真实拓扑仍待用户提供，现场关联和业务准确率尚未验收。

## 工具组成

| 组件 | 实现 | 输出与边界 |
|---|---|---|
| 流式解析 | `log_parser.py` | CRLF/UTF-8 字节偏移、行范围、多行事件；非法日期/编码/超长行和无法归属行隔离，空行单独记账 |
| 语义规则 | `upfd-rules-v1` | 发生、解除、观察分离；严重级别原样保留；脱敏值记入 masked_fields，不生成虚构身份 |
| 事件存储 | `log_tools.py` | 每 4096 事件批量写 Zstd Parquet，按原始墙钟月份分区；generation 固定源哈希、代码、契约、时区、设备与模板版本 |
| 统计和检索 | DuckDB 参数化查询 | 半开 UTC 时间窗、实体/协议/事件过滤、总数、分桶、首尾/峰值/实体代表；样本上限与完整统计分开标明 |
| 原文回查 | `LogStore.context` | 根据注册 generation/event_id 回查原始字节并复核源 SHA；前后各最多 20 行，单事件读取最多 64KiB |
| 冻结模板 | `log_templates.py` | Drain3 离线训练，纯 JSON 快照；恢复后仅 match，不训练、不自动判异常，记录 LRU 淘汰 |
| 拓扑导入 | `topology.py` | CSV/XLSX 字段映射、显式别名、源 sheet/row、半开有效期、合成标记；仅真实合并格范围继承，坏行隔离 |
| 保守关联 | `log_correlation.py` | 真实设备/对端/类型一致且时间明确才配对；重复发生、窗口不完整或超期不强配；拓扑只提供候选检查对象 |

单物理行和合并事件上限各 64KiB，存储摘录上限 8192 字符。超限字节仍在源文件中且计入 offset/length；所有行和字节有去向。FID 是执行信息，不作为设备编号。目前关联单个注册日志，不包含跨日志因果分析。

源文本带 offset 为 explicit；用户指定源时区后转换为 assumed，manifest 注明 user_provided。未知时区或 DST 模糊/不存在时间保持 unknown，绝对时间查询返回 need_input。月份分区采用源文本月份，UTC 查询仍按转换后的时间过滤。

拓扑文件限 20MiB、XLSX 展开限 100MiB、数据行限 10 万；不包含拓扑图或自由文本猜边。有效期未知的边带 partial 提示；没有真实拓扑时返回 missing_source。合成边不能用于真实故障结论。

## 真实日志回放

[回归证据](../evidence/p4/regression.json) 固定源 SHA `a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc`，工具 generation 为 `a6f18ac81a18aa2125fa`。32539 行 / 6347974 字节 / 32539 事件全部解析，连续行号和字节范围 SQL 回查违例为 0；原日志无需隔离。1 处相邻墙钟时间逆序保留。没有擅自补时区或设备 ID。

| 旧统计或问题 | 修正后消息数 | 解释 |
|---|---|---|
| PFCP 不可达 37 | 不可达发生 14；收到心跳 23 | 心跳为观察事件 |
| PFCP 恢复 12 | cleared 12 | 类型和解除状态分别保存 |
| 许可证告警 11 | raised 1；cleared 11 | 原 11 条均为解除；另 1 条发生以前未识别 |
| 脱敏 FAR 未识别 | observed 3238 | 接受脱敏字段，保留身份未知 |
| N4 名称失败 15 | observed 30 | 旧规则仅含 svc1，另 15 条 svc2 以前未识别 |
| 心跳响应未归类 | observed 7 | 新增响应观察类型 |
| 未分类 25979 | 22718 | 差值 3261 = FAR 3238 + 响应 7 + 许可证发生 1 + svc2 15 |
| GTP-U 检测/上报各 120 | 各 120，分类型保存 | 不能宣称 240 次独立故障 |

PFCP 会话释放 5715、GTP-U 重传 382、接口索引失败 111、启动 21、定时器失败 16 等消息计数保持一致。FATAL 不作为新业务故障等级。四类代表记录另通过原始字节逐字回查。

真实日志告警发生/解除消息共 278，全部缺少足够的明确设备/对端身份，配对为空并输出缺口。人为给文件一个设备 ID，也不能用统一 IP_ADDR 证明 PFCP/GTP-U 对端相同。

Drain3 同源训练出 162 个模板，无 LRU 淘汰；同源冻结推理未匹配消息为 0。这是训练集回放，不是泛化质量结论。另有合成新消息、淘汰、快照哈希和重载稳定性测试。22718 条业务规则未分类消息按模板形成待扩展清单；未分类与快照未匹配分别统计，均不自动判异常。

## 拓扑与关联验证

`data/p4/fixtures/synthetic_topology.csv`、`synthetic_merged_topology.xlsx` 使用 SYNTHETIC 名称，manifest/edge 中 synthetic=true。验证 N3 不匹配 N30、显式别名、有效期结束点排除、A2:A3 不补到 A4、缺端点行隔离、循环别名拒绝和合成提示。

关联测试覆盖真实对端与时间配对、脱敏值不配对、重复发生不折叠、未知时区不计算时长、无拓扑不编造端口。PFCP 查 N4 候选，GTP-U 查 N3/N9 候选集合，不代表已经识别实际接口或因果路径。

## 容量实测

[容量报告](../evidence/p4/capacity.json) 使用两个新进程，Linux ru_maxrss 覆盖完整入库和全量统计查询；两次 cached_generation=false。

| 数据 | 输入字节 / 行数 | 入库秒 | 查询秒（含归档校验） | 峰值 RSS | Parquet 字节 |
|---|---|---:|---:|---:|---:|
| 原日志 | 6347974 / 32539 | 1.5732 | 0.1112 | 144642048（约 138 MiB） | 1073682 |
| 合成放大 | 1079155580 / 5531630 | 215.2896 | 2.6137 | 252379136（约 241 MiB） | 182919502 |

放大数据完整重复原日志 170 次，超过 1GiB，分类计数严格为原日志的 170 倍。重复时间戳与身份是合成放大，不是新现场故障。输入增长 170 倍，峰值 RSS 约增长 1.75 倍，均低于 4GiB 目标。未对 1GiB 输入执行 Drain3 训练或模型推理，不声称这些步骤也已通过容量指标。

## 复现和使用

```bash
cd /home/huangxiaolin/upf-agent
uv run upf-agent p4 --help
uv run python scripts/validate_p4.py
uv run upf-agent p4 analyze-log a6f18ac81a18aa2125fa
uv run upf-agent p4 find-events a6f18ac81a18aa2125fa --event-type far_handover --limit 3
uv run upf-agent p4 read-context a6f18ac81a18aa2125fa log-a698d029342259b7-0 --before 0 --after 2
uv run upf-agent p4 template-inventory a6f18ac81a18aa2125fa
uv run upf-agent p4 correlate-events a6f18ac81a18aa2125fa
uv run python scripts/p4_capacity.py
uv run pytest -q
uv run ruff check src tools tests scripts
```

容量脚本重复运行会复用同 generation，并显式记录 cached_generation=true；只有 false 证明本次执行完整入库。重测新入库需新容量目录，或备份报告后清理可重建的容量索引；普通业务归档和原件无需删除。

确认源时区后 `p4 import-log data/raw/upfd_masked.log --timezone 实际时区` 生成新 generation；设备 ID 同样要有资料依据。时间查询同时提供带 offset 的 --start/--end，区间为 `[start,end)`。

真实拓扑通过 `p4 import-topology /实际路径/topology.xlsx` 导入；可选 --mapping JSON 的 header_mapping 是“原表头 → canonical 字段”，device_aliases/interface_aliases 是显式别名。没有真实资料时保留合成结果，不代替现场验收。

78 项测试通过，其中 P4 为 26 项，Ruff 通过。应用 uv.lock 固定新增 DuckDB 1.5.5、PyArrow 23.0.1、Drain3 0.9.11、openpyxl 3.1.5，未改推理/OCR/检索环境。API 参考 [DuckDB Parquet](https://duckdb.org/docs/stable/data/parquet/overview)、[Drain3 冻结推理](https://github.com/logpai/Drain3)、[openpyxl 合并格](https://openpyxl.readthedocs.io/en/3.1/api/openpyxl.worksheet.merge.html)。

下一阶段 P5 接入有限 Agent、调查状态与报告。P2 人工签署、日志时区与真实拓扑、P6 正式标注和业务评测继续保留待办。
