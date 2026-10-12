# UPF Agent 独立迁移工程

本工程已完成 Dify 迁移计划的 P0（资料基线）、P1（本地模型底座）、P2 文档处理与抽样复核、P3 本地检索问答及开发对照、P4 确定性日志与拓扑工具、P5 有限 Agent 与终端闭环。P2 两轮复核已完成：60 条结构样本及 30 张截图均通过，M2 人工验收已收口。[主计划](/home/huangxiaolin/dify/plan.md)记录完整 P0–P7；现在可通过终端、TXT、stdin 或 JSONL 完成问答、日志调查、暂停恢复、会话和证据报告。P6 正式质量评价与 P7 离线部署验收仍待完成。

## 已可执行

```bash
cd /home/huangxiaolin/upf-agent
uv sync --extra dev --python 3.11
uv run upf-agent p0-audit
uv run upf-agent ingest-documents
uv run upf-agent p2-review-packet
uv run upf-agent attach-p2-assets
uv run upf-agent repair-ocr
uv run upf-agent build-index --device cuda:1
uv run upf-agent verify-index
uv run upf-agent search-index '如何执行 show cp-node 查询 SMF 节点信息？' --product UPF --version 5.0 --device cuda:1 --output evidence/p3/show_cp_node.json
uv run upf-agent doctor --output runs/p1/doctor.json --probe-bf16
uv run pytest -q
uv run ruff check src tools tests scripts
```

P0 输入白名单为 `config/corpus.yaml`；可重跑结果在 `data/p0/`，关键快照保存在 `evidence/p0/`，包括文件哈希、手册结构与命令词覆盖、工作流节点与提示词、旧日志代码及其旧分类统计。评测协议在 `eval/protocol.md`；`eval/slots.jsonl` 为 120 个尚待人工标注的名额。

P2 将白名单资料按原哈希复制到 `data/raw/`，运行时不再读取 Dify 目录。四份 DOCX 导入为本地 SQLite generation；OCR 和论文 PDF 作为不同质量及角色的辅助资料附着。命令、截图和论文各自保留来源定位。详见 [P2 验收记录](/home/huangxiaolin/upf-agent/docs/P2_acceptance.md)。

P3.1–P3.2 将原生手册块建立为本地 Qdrant 向量、中文技术 BM25 和精确命令三个索引，统一产品/版本过滤，再经 RRF、Qwen reranker 和章节邻块扩展形成有来源位置的证据。当前索引只使用原生 DOCX 文本，`search-index` 输出检索证据，`ask` 进一步生成经引用校验的回答。详见 [P3 检索验收记录](/home/huangxiaolin/upf-agent/docs/P3_retrieval_acceptance.md)。

`doctor` 是只读快照，GPU 显存可能随后变化。2026-09-25 初次检查时两张 A100 被其他任务占用，后来显存释放，已抓住窗口通过 30B 基线服务 smoke。`serve` 对每卡要求起步至少 68 GiB 空闲，未满足时返回退出码 2，保持其他进程不变。

## 复现 P1 生成模型 smoke

先确认 `doctor` 显示资产完整、显存充足。`.venv-inference` 已安装 Python 3.10、vLLM 0.19.1、Transformers 5.8.0 和 Torch 2.10.0，精确版本见 `environment-lock/inference.freeze.txt`。在一个终端启动独立服务：

```bash
uv run upf-agent serve --model baseline --gpu 0 --max-model-len 16384
```

在另一个终端执行：

```bash
uv run upf-agent smoke --model baseline --output runs/p1/baseline-smoke.json
```

这组测试依次验证中文文本、JSON Schema 输出、工具调用及返回后的最终回答。服务只绑定 127.0.0.1:18000，客户端禁用环境代理。基线通过后对目标模型重复 `--model target`；目标服务端口 18001，先 16K 再测试 32K。两者使用独立进程，不修改已有 8000 端口模型服务。

CPU 检索模型 smoke 命令：

```bash
uv run upf-agent retrieval-smoke --device cpu --output runs/p1/retrieval-smoke.json
```

该命令通过独立 Python 子进程加载本地 embedding 和 reranker，检查向量维度、L2 范数、重复结果稳定性，以及相关/无关片段排序和 yes/no 概率范围。四组模型已生成逐文件 SHA-256 清单与 Hugging Face etag/revision 比对报告，验收快照保存在 `evidence/p1/`，可重跑输出在 `runs/p1/`。目标模型分别在 16K 和 32K 服务配置下通过完整 smoke，另在 32K 下用 20,029 tokens 的输入准确找回末尾校验码。详见 [P1 验收记录](/home/huangxiaolin/upf-agent/docs/P1_acceptance.md)。

## 当前验收状态

| 项目 | 状态 |
|---|---|
| P0 资产/工作流/旧规则审计 | 完成；可重跑和回查文件哈希 |
| P0 评测协议与 120 个标注名额 | 完成协议与槽位；人工 gold 仍待后续标注 |
| P1.1 工程、契约、CLI | 已实现 |
| P1.2 硬件探针、BF16小算例、启动保护 | 已实测通过；共享 GPU 空闲时完成模型验收 |
| P1.3 基线模型独立服务与完整 smoke | 已在独立端口通过中文、JSON Schema 和完整工具往返；验收后已释放 GPU |
| P1.4 Qwen3.8-27B | 18 个权重分片已校验；16K/32K 中文、JSON、工具往返和思考解析通过；20,029 tokens 长上下文通过 |
| P1.5 检索模型 | CPU 独立 worker 已加载两组 4B 权重并通过向量维度、范数、稳定性和正负样本排序 smoke；GPU BF16 性能待测 |
| P1.6 环境锁 | 应用 `uv.lock`、推理与检索 freeze、四组模型逐文件 SHA-256 与下载 etag/revision 比对均已保存，独立服务实测通过 |
| P2.1–P2.5 | DOCX、命令与表格、30 张 OCR、12 页 Docling PDF、版本化导入及隔离均已实测；自动化测试通过 |
| P2.6 | 60 条结构样本和 30 张截图通过两轮用户复核，M2 已收口；6 处原手册/命令片段疑点和 7 条隔离行保留 |
| P3.1–P3.2 | 1,061 块三路索引、2,560 维 Qdrant、RRF 和本地 reranker 已实测；来源和排序可检查，索引校验通过 |
| P3.3 | TXT/stdin、原文标识与相关性门控、来源校验、原文片段发布；模型归纳仅在审计中，16 题回归见下文 |
| P3.4 | 五种检索配置、12 条开发探针已运行；正式质量比较仍待人工相关性标注 |
| P4.1–P4.7 | 流式解析、语义规则、Parquet/DuckDB、冻结模板、CSV/XLSX 拓扑、保守关联、超过 1GiB 容量实测通过；真实时区/设备/拓扑待补 |
| P5.1–P5.6 | 有限调查、严格工具参数、3 轮/8 调用预算、SQLite 恢复、任务隔离、TXT/stdin/JSONL/会话及报告均通过验证；全工程 197 项测试通过 |

P0 的 120 个槽位仍待 P6 前人工标注，目前没有业务准确率结论。P1 证明本地模型底座可用，P2 证明资料能解析和定位，P3 可执行来源可查的手册问答，P4 可独立统计日志和输出证据缺口，P5 可在预算内调查并恢复任务。检索模型只在查询期间加载，查询结束后释放 GPU。

## 手册问答和 P2 人工复核

先在一个终端执行 `uv run upf-agent serve --model baseline --gpu 0`，另一个终端执行：

```bash
uv run upf-agent ask '如何执行 show cp-node 查询 SMF 信息？' --product UPF
uv run upf-agent ask --file runs/p3-question.txt --product 5GC网管 --version V1.3
uv run upf-agent ablate-retrieval --device cuda:1
```

问答及检索轨迹保存在 `runs/p3/<run_id>/`；部分回答或缺证据退出码为 2，失败为 1。逐题对照在 `evidence/p3/ablation.json`，属于未人工确认的开发探针，不能当作业务准确率。详细约束见 [P3 验收记录](docs/P3_retrieval_acceptance.md)。

P2 当前材料是 [60 条结构核对](evidence/p2/structure_audit.md)、[纠错后的 OCR 逐行文本](evidence/p2/ocr_corrected_text.md) 和 [已提交的人工复核单](evidence/p2/review_sheet_c05fe621e37ebdb1c663_v3.md)。90 项已通过复核，原 4 项不通过及本轮通过结果均可回查，详见 [已提交的修正复核单](evidence/p2/review_followup_v3_4_images.md)。用户提交的报告和原始 `ocr_30.json` 保留不变；OCR 仍是辅助资料，7 条模糊/遮挡行继续隔离，未进入 P3 权威索引。原抽样包与历史索引可回查。全部 144 个合并单元格也通过原始 OOXML 属性及继承文本核对。

## 2026-09-28 质量收口

当前 P2 generation 为 `c05fe621e37ebdb1c663`（107 条命令候选），P3 为 `c61e9796eead2610cfd4`（1,061 块）。排除了 `cp:`、`ls:` 错误输出，步骤抽样排除目录、图注和配置输出。30 张截图的 122 条报告发现已逐图处理：116 条纠错、1 条明确误报、5 条冲突/模糊项隔离，另隔离 2 条遮挡行。

```bash
uv run python scripts/audit_p2_structure.py
# 启动 baseline 服务后运行；先完成当前 generation 的检索对照
uv run upf-agent ablate-retrieval --device cuda:1
uv run upf-agent evaluate-p3 --device cuda:1
```

`evaluate-p3` 冻结 16 条开发题，检查回答状态、关键字、引用原文和拒答；逐题检索与回答保存于 [问答回归报告](evidence/p3/quality_regression.md)。存在失败时退出码为 2。前两轮记录分别保留于 `evidence/p3/archive/c61e9796eead2610cfd4/answer-v1/` 和 `answer-v2/`，开发修复和重跑不算独立测试集验收。P0 的 120 个人工标注名额与 P6 正式语义验收仍待完成。

最终验证：52 项测试与 Ruff 通过，16 题真实模型开发回归经过原文发布重放后全部满足机器契约；生产代码另通过真实 TXT CLI 问答。详见 [语义复查与发布边界](evidence/p3/semantic_review.md)。默认答案为选中的原文片段，归纳仅保留在 audit；未把重放计算为新推理或正式业务准确率。P2 原件抽样签署现已完成，完整操作步骤及现场适用性仍待 P6 业务评测。

## P4 日志和拓扑工具

```bash
uv run upf-agent p4 analyze-log a6f18ac81a18aa2125fa
uv run upf-agent p4 find-events a6f18ac81a18aa2125fa --event-type far_handover --limit 3
uv run upf-agent p4 read-context a6f18ac81a18aa2125fa log-a698d029342259b7-0
uv run upf-agent p4 template-inventory a6f18ac81a18aa2125fa
uv run upf-agent p4 correlate-events a6f18ac81a18aa2125fa
```

无需模型服务。真实日志 32539 行/6347974 字节全部可回查，心跳/发生/解除和脱敏 FAR 已分离；计数是消息数。未知时区不接受绝对时间窗，没有真实标识不配对告警。合成拓扑明确带 synthetic 标记，不能代替现场拓扑。

1,079,155,580 字节、5,531,630 行合成容量实测峰值 RSS 约 241 MiB，入库约 215 秒，全量查询约 2.6 秒。78 项测试通过，Ruff 通过。详见 [P4 验收](docs/P4_acceptance.md) 与 [回归](evidence/p4/regression.json)、[容量](evidence/p4/capacity.json)。现在的人工待办见 [P2 验收中的填写说明](docs/P2_acceptance.md)。

## P5 有限调查、恢复和批处理

模型服务按上文启动。手册继续使用原文发布策略；日志事实由确定性工具生成，模型提出补查计划。每任务最多 3 轮、8 次工具尝试、180 秒活跃执行，缺资料时保存检查点并返回；恢复继续原预算。

```bash
uv run upf-agent investigate --file examples/p5_manual.txt --product 5GC网管 --version V1.3
uv run upf-agent diagnose '统计日志消息数量' --log-generation a6f18ac81a18aa2125fa --deterministic
uv run upf-agent diagnose --question-file examples/p5_diagnosis.txt --log-generation a6f18ac81a18aa2125fa --pause-after execute
uv run upf-agent resume RUN_ID
uv run upf-agent chat --session demo
uv run upf-agent batch --input examples/p5_batch.jsonl --output runs/my-p5-batch
```

`--deterministic` 的日志统计无需模型。批处理样例故意包含一条损坏 JSON，预期退出码为 1，后续任务仍执行。其他命令完整完成退出 0，部分结果/缺资料/待输入退出 2，执行失败退出 1。每任务输出位于 `runs/p5/<run_id>/`，包括报告、状态、manifest、事件轨迹与耗时/用量指标；恢复前版保存在 `history/`。

真实 TXT 手册问答已完成；真实日志调查通过暂停、新进程恢复和继续补查，3 轮 7 调用结束，时区/设备身份/真实拓扑缺口明确保留。全工程 197 项测试、Ruff、依赖检查通过。100 个固定参数请求检验代码契约，不是模型参数正确率或业务准确率。详见 [P5 验收与操作说明](docs/P5_acceptance.md)、[实测证据](evidence/p5/regression.json)。P2 人工签署已完成，正式业务质量与部署验收留在 P6/P7。

## P2 用户复核回执（首轮历史记录）

90 项复核已接收：60 条结构样本及 26 张截图通过，4 张截图已按原图纠错待确认。现在仅需查看 [4 张截图修正复核单](evidence/p2/review_followup_v3_4_images.md)，不必重做其余 86 项。原始文件保留，7 条隔离行不补猜，M2 暂不勾选。本轮全工程 203 项测试、Ruff、69 个文件格式检查通过；详见 [接收记录](evidence/p2/human_review_v3.json) 与 [P2 验收更新](docs/P2_acceptance.md)。

## P2 修正复核完成

用户已确认截图 01/07/17/20 的本轮修正通过，两轮合计 60 条结构样本、30 张截图全部通过，M2 已收口。截图 07 指出的残留 `PEDM` → `PFDM` 已按原图修正并同步本地辅助库，用户明确该项不影响本轮签署。原复核单及本轮提交文件保留不变，7 条模糊/遮挡行继续隔离，OCR 不自动进入 P3 权威索引。当前结果见 [复核接收记录](evidence/p2/human_review_v3.json)、[P2 验收](docs/P2_acceptance.md)。后续待办为 P6 正式质量评测与 P7 部署验收，以及 P4 的真实现场资料。

## P6 开发评测与待人工验收

已增加业务候选题、两模型同证据开发对照、真实参数测试、三种日志调查路线、完整RAG计时、16K/32K并发矩阵，以及人工标签导入、答案评分、配置冻结和保留集一次性执行检查。默认继续使用 Qwen3-30B-A3B-Instruct-2507；Qwen3.8-27B 的短JSON节点关闭思考，普通输出仍low。当前开发结果存在漏答、错章节与误拒，M6尚未通过。自动实测已归档；全工程243项测试、Ruff、90文件格式及依赖检查通过。生成组件主矩阵为基线4档与目标关闭思考4档，另保留2档low失败；目标关闭思考的组件成绩不代表普通Agent业务质量。

操作与边界见 [P6评测说明](docs/P6_evaluation.md)，本机结果见 [P6实测报告](evidence/p6/results.md)。现在人工填写 [业务真值复核单v3](eval/p6/business_v3/truth_review.md)；这是另一项业务真值确认，已签署的P2原文/OCR复核保留。新版候选120题覆盖四份手册、日志与合成拓扑，开发/保留各60；旧120题和本轮42题成绩留作开发历史，不代表新版整集成绩。真值复核后先执行并评分开发集，修复至门槛满足再冻结、一次执行保留集。

## P6 旧版复核接收与来源修正（2026-09-29）

已接收旧版 `eval/p6/truth_review.md`：116题通过、4题不通过。四题共用的命令块来源拼接已修正，新索引 `daa6f8e85f8a664b0a55` 保留1,061块；107个命令块已逐块与原始OOXML及定位核对。248项测试通过；原件及旧索引、实测保持不变。P6默认候选题库更新为v4，正式人工署名与评测尚未完成。

旧版与新版一致的72题通过结论已保留，实际署名待明确；其余只需复核 [48题](eval/p6/business_v4/pending_48_review.md)（44道新版题、4道修正题），原件位置见 [来源索引](eval/p6/business_v4/pending_48_sources.md)。完整版在 [v4复核单](eval/p6/business_v4/truth_review.md)。用户原文件未覆盖，未替填写正式署名、未运行保留集。

## P6 v4补充复核已接收

本轮48题已全部勾选通过，与原72题合并后，120题内容结论均通过；内容待复核为0。复核人仍是“AI辅助复核（待人工签名）”，请提供实际姓名与实际复核日期，助手统一补入新署名副本，无需再逐题修改。正式真值尚未导入、模型评测未执行、保留集未消费，M6仍未通过。详见 [接收回执](evidence/p6/review_followup/v4_48_5a8e673eab81836e/接收与待办.md)。

## P6真值已正式导入

按用户明确指定填写复核人“张三”，日期沿用提交中的2026-09-28。120题真值已严格导入 [reviewed_suite.jsonl](eval/p6/business_v4/reviewed_suite.jsonl)，原提交保留，署名来源可追溯。下一步执行开发60题并独立复核模型实际答案；保留集不在此时执行，M6尚未通过。
