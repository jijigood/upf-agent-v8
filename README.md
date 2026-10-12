# UPF Agent 独立迁移工程

本工程已完成 Dify 迁移计划的 P0（资料基线）、P1（本地模型底座）、P2 文档处理与抽样复核、P3 本地检索问答及开发对照、P4 确定性日志与拓扑工具、P5 有限 Agent 与终端闭环。P2 两轮复核已完成：60 条结构样本及 30 张截图均通过，M2 人工验收已收口。[主计划](/home/huangxiaolin/dify/plan.md)记录完整 P0–P7；现在可通过终端、TXT、stdin 或 JSONL 完成问答、日志调查、暂停恢复、会话和证据报告。P6 正式质量评价与 P7 离线部署验收仍待完成。

**当前人工待办（2026-10-07）：无需继续填写旧增量答案表。** v5h 的 27 题及后续三题提交已经接收；历史段落中的“待填”不是当前任务。当前开发回归机器门槛通过，M6 尚缺新独立资料的正式验收；同时推进 P7 的环境隔离、备份恢复技术准备，最终交付验收仍受 M6 约束。现有 UPF 日志的十个副本只有一个不同 SHA256，[数据独立性核查](evidence/p6/independent_source_audit_20261007.json)已记录。

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

P0 的 120 个槽位现已成为用户指定署名的复核真值集；当前仍没有新答案的人工业务准确率结论。P1 证明本地模型底座可用，P2 证明资料能解析和定位，P3 可执行来源可查的手册问答，P4 可独立统计日志和输出证据缺口，P5 可在预算内调查并恢复任务。单次 `ask` 在查询期间加载检索模型并于结束后释放；连续提问可用 `manual-chat`，检索模型在会话期间常驻，退出后释放 GPU。

## 手册问答和 P2 人工复核

先在一个终端执行 `uv run upf-agent serve --model baseline --gpu 0`，另一个终端执行：

```bash
uv run upf-agent ask '如何执行 show cp-node 查询 SMF 信息？' --product UPF
uv run upf-agent ask --file runs/p3-question.txt --product 5GC网管 --version V1.3
uv run upf-agent manual-chat --product UPF
uv run upf-agent ablate-retrieval --device cuda:1
```

问答及检索轨迹保存在 `runs/p3/<run_id>/`；部分回答或缺证据退出码为 2，失败为 1。逐题对照在 `evidence/p3/ablation.json`，属于未人工确认的开发探针，不能当作业务准确率。详细约束见 [P3 验收记录](docs/P3_retrieval_acceptance.md)。

`manual-chat` 启动后可连续输入多道手册题，输入 `/exit` 退出；脚本调用可加 `--jsonl`，每行一个问题、每行一条 JSON 结果。它沿用 `ask` 的来源校验及 `runs/p3/<run_id>/` 审计文件。首次会话需要加载嵌入与重排模型，2026-10-02 本机实测约 26.5 秒；之后保持生成服务和会话常驻，20 次代表题首输出 p95 为 4.67 秒。单次 `ask --json` 每次重新加载检索模型，同题首输出 p95 为 35.11 秒。两次实测的完整记录分别在 [常驻会话](runs/p6-v4-v5e/manual-chat-first-visible-freegpu-20261001/summary.json)和[单次命令](runs/p6-v4-v5e/cli-first-visible-freegpu-20261001/summary.json)；这只验证四道开发代表题的单并发体验，不代表所有问题或生产负载。

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

## P6 当前状态（2026-09-30）

120题真值已正式导入，署名按用户指定为张三，日期沿用2026-09-28；不需重做。

原开发60题的答案复核单已接收，署名豆包（AI辅助复核），日期2026-09-29。用户明确确认“目前只是 AI 辅助评分”，因此只作为问题发现依据，不计入人工验收。已保存原始提交并确认问题、预期原文、实际输出与summary/suite SHA绑定均未改动。

本轮AI辅助评分：证据支持56/60（93.3%），完整26/60（43.3%），命令正确20/20，新增关键参数0，缺资料处理3/4（75%）；34题有失败字段，语义门槛未通过。这些分数只对应修复前的60题输出，不是人工业务准确率或修复后成绩。

已补上AI评分来源隔离、指定版本配置发布门槛与被拒绝候选的报告过滤；日志回答增加所问类型的代表原文、状态和定位。手册知识/历史故障改为附引用的原生小章节，命令限定范围并说明示例适用性，过期拓扑明确展示排除原因。P0原始7份资料SHA不变。

修复后的新开发60题已在独立目录实跑：60/60状态契约符合，40道手册题重排Recall@20=1.0，全部逐类机器检查通过；288项测试和Ruff通过。这些不等于人工业务评分。[根因与修复说明](runs/p6-v4-v5b/修复与根因复核.md)、[新60题答案复核单](runs/p6-v4-v5b/reviewed-dev/answer_review.md)。请对新输出逐题复核；旧AI辅助评分不能代签。未冻结、未执行保留集，M6仍未通过，P7另行实施。[旧评分及问题清单](runs/p6-v4-v3/review-intake-f7fb338d3c11/results.md)。

**最新追修：**v5b的60题提交表已归档。表内逐题填写为证据支持60/60、完整58/60、命令正确20/20、缺资料处理4/4；两道不完整题指出手册N3案例解决方法误写“N4接口”，现已保留原文并加矛盾提示。v5c新代码再跑60题无执行错误、机器检查通过，290项测试及Ruff通过。两轮用户可见答案55题一致、5题变化；[5题增量复核页](runs/p6-v4-v5c/增量复核_5题.md)及[完整新复核单](runs/p6-v4-v5c/reviewed-dev/answer_review.md)已生成。旧提交的署名“张三”和9月29日日期早于9月30日答案生成，实际复核身份/日期待确认；提交表分数尚不能计入人工验收。保留集未执行，M6仍未通过。[完整接收与当前状态](docs/P6_evaluation.md)。

v5c完整60题填写版本已原样归档并通过题库/摘要哈希及非评分内容比对。表内为支持60/60、完整40/60、命令20/20、缺资料4/4；用户已澄清日志10题和拓扑6题“不完整”为误填，按题意重核均有相应原始证据，N6两题意见也与答案不符。[18题更正建议](runs/p6-v4-v5c/review-intake-bd66c5e75b34/recheck_proposal.json)不回写原表、不冒充人工评分。n4switch两题的手册信息收集节只有标题，已修复答案未明示资料缺口的问题。当前代码以v5d再跑开发60题，机器审计各项通过，292项测试及Ruff通过；对比v5c有[6题可见变化](runs/p6-v4-v5d/增量复核_6题.md)，[v5d完整空白复核单](runs/p6-v4-v5d/reviewed-dev/answer_review.md)已生成。填写表是否为本人逐题核对仍待确认，保留集未执行，M6仍未通过。[完整接收与当前状态](docs/P6_evaluation.md)。

用户随后填写了v5d 60题复核单并声明复核完成。[原件与接收记录](runs/p6-v4-v5d/review-intake-fde728cf47de/接收与验收.md)已绑定本轮摘要/题库，正式开发集评分为证据支持60/60、完整60/60、命令20/20、缺资料4/4，语义门槛通过；“张三”为此前约定的署名标签，不作实名核验。P6.1已完成，目标模型当前代码对照、Agent增益、配置性能和冻结保留集仍待验，M6未通过。[评分判定](runs/p6-v4-v5d/review-intake-fde728cf47de/adjudication.json)。

同一当前代码和开发题库的[2507/3.8模型对照](runs/p6-v4-v5d-target2/模型对照与选择.md)已完成：两者机器状态均60/60，49题可见答案一致；3.8的10道日志题及1道缺资料题输出不同，未获人工语义评分，日志诊断p95为106.05秒（2507为64.54秒）。目前继续以2507为默认模型，3.8保留实验配置。P6.3复杂跨资料Agent增益、P6.4端到端首字指标、P6.5冻结保留集仍待完成，M6未通过。

**2026-10-01更新：**跨资料Agent已补齐手册取证并约束无证据因果候选；[对照](runs/p6-v4-v5d/复杂任务取证对照.md)尚未显示它优于固定工具流程。修改后v5e开发集真实重跑60题，状态与逐类机器审计全部通过；相对已确认复核的v5d，57题可见内容完全一致，[3题增量复核页](runs/p6-v4-v5e/增量复核_3题.md)已生成，旧评分的[逐题沿用审计](runs/p6-v4-v5e/carryforward_review.json)已保存。原2507/3.8对照属于修改前指纹，不能宣称当前版本严格A/B。CLI首字基准本次因共享GPU显存占用被启动门槛阻止，0个有效样本；[阻塞记录](runs/p6-v4-v5e/cli-first-visible/blocked.json)及[评测状态](docs/P6_evaluation.md)可查。默认仍为2507，配置与保留集未冻结/运行，M6未通过。

**2026-10-01复核收口：**用户已完成上述三题增量复核。[提交原件及接收记录](runs/p6-v4-v5e/review-intake-3db73a9c8b42/接收与验收.md)已归档，与57题旧版判断合并后，[当前开发集正式判定](runs/p6-v4-v5e/review-intake-3db73a9c8b42/adjudication.json)为证据支持60/60、完整60/60、命令20/20、缺资料4/4，P6.1当前版本通过。[同轮性能预检查](runs/p6-v4-v5e/current_performance_precheck.json)为手册类完整答案p95约2.78秒、日志诊断p95约58.36秒，并保留设备峰值资源采样；CLI首字仍未测得。还需处理Agent增益、当前代码模型比较、配置冻结和一次性保留集；M6未通过。

继续P6时已形成[模型与Agent决策草案](runs/p6-v4-v5e/P6模型与Agent决策草案.md)及[逐项就绪核对](evidence/p6/readiness_v5e.json)：保留已获人工评分的2507默认；Agent跨资料取证安全边界可用，但未证明优于固定流程。当前CLI首字仍因共享GPU占用无法测量。[冻结配置草案](eval/p6/development_decision.v5e.draft.json)维持未接受状态，程序验证拒绝冻结，保留集未消费。

GPU利用率瞬时为0仍不能使用已被其他进程分配的显存。[启动可行性实测](runs/p6-v4-v5e/gpu_start_assessment.json)显示基线权重约56.9GiB，而GPU0空闲约42–43GiB，正式单卡服务被68GiB规划门槛拒绝；端口8000已有同名但配置不同的服务，16-token试探30秒无结果，不能替代P6性能验收。

**2026-10-02进度：**显存释放后已按正式配置启动2507服务；原单次CLI首输出p95为35.11秒，新增常驻`manual-chat`同四道代表题20次首输出p95为4.67秒，首次会话准备26.48秒另计。当前代码[v5f开发60题](runs/p6-v4-v5f/reviewed-dev/summary.json)状态与[机器审计](runs/p6-v4-v5f/repair_audit.json)全部通过，手册类完整答案p95为4.79秒、日志诊断p95为98.12秒。与v5e已人工复核答案相比56题相同，4道日志题`log-003/004/005/010`的引用上下文或终止说明有变化；[四题短复核页](runs/p6-v4-v5f/增量复核_4题.md)待人工填写。[当前就绪表](evidence/p6/readiness_v5f.json)仍把当前开发集语义验收、配置接受及一次性保留集记为未完成，M6未通过。

用户随后完成四题增量复核。[原件接收](runs/p6-v4-v5f/review-intake-fb450cc8cee8/接收与验收.md)与[当前开发集判定](runs/p6-v4-v5f/review-intake-fb450cc8cee8/adjudication.json)显示支持60/60、完整60/60、命令20/20、缺资料4/4、关键参数凭空新增0。P6.1当前代码人工语义门槛通过；配置接受和一次性冻结保留集仍待完成，M6未通过。

**2026-10-06 冻结保留集：**用户同意按既定2507 BF16/GPU0/16K/并发1配置启动后，已保存[接受决策](eval/p6/development_decision.v5f.accepted.json)和[冻结配置](evidence/p6/frozen_v5f.json)。保留60题仅执行一次，60/60状态契约符合，无执行错误；检索门槛、资料来源分区及7份P0原件哈希检查通过。[运行摘要](runs/p6-v4-v5f/heldout-run/reviewed-heldout/summary.json)、[机器审计与需重点复核题](runs/p6-v4-v5f/heldout-run/machine_audit.json)和[60题人工复核单](runs/p6-v4-v5f/heldout-run/reviewed-heldout/answer_review.md)已保存。机器审计提示`command-027`、`knowledge-017/018`、`troubleshooting-013/015`、`missing-007`需重点判断；这不是人工判错。保留集人工答案评分未完成，M6仍未通过；不能看过保留集后调参重跑。首次评测的自启服务已按旧脚本结束；根据用户随后要求，已重新启动同一模型并保持常驻。

[M6正式出口逐项核对](runs/p6-v4-v5f/M6_gate_review.md)记录机器门槛、性能限制和人工评分待办。当前手册发布路径的同证据开发集对照虽有42/42机器契约通过，但2507模型请求数为0，不具备判别模型优劣的能力；额外3.8加载已停止，2507继续常驻GPU0。

用户已完成保留集60题人工复核。[原件接收](runs/p6-v4-v5f/heldout-run/review-intake-232c9043e180/接收与验收.md)及[正式判定](runs/p6-v4-v5f/heldout-run/review-intake-232c9043e180/adjudication.json)为支持60/60、完整42/60、命令20/20、缺资料5/6、关键参数新增0。缺资料正确率83.3%低于90%门槛，**M6正式验收未通过**。本次保留集不得修复后重跑；下一版修复需新独立验收集。四道V1.3知识题的“不完整”意见与来源版本标记不一致，正在向用户核实，原评分不改写。

[失败归因与修复边界](runs/p6-v4-v5f/heldout-run/review-intake-232c9043e180/失败归因与修复边界.md)区分了原资料空栏/截图与Agent答案呈现、现场请求路由问题；检索命中和证据支持不能代替完整答案。

**2026-10-06 v5g继续：**已修复现场拓扑及脱敏身份缺口路由、日志根因边界、手册空栏/图示及历史案例说明。[修复记录](runs/p6-v4-v5g/修复与新验收准备.md)和[开发回归](runs/p6-v4-v5g/development_replay/summary.json)已保存。新 60 题来源组与旧 120 题无交叉，仍是待人工核对真值的[候选集](eval/p6/business_v5_replacement/candidate_suite.jsonl)；[逐题复核单](eval/p6/business_v5_replacement/truth_review.md)附原件路径、定位和摘录。原正式保留集不重跑；新题未经审核和运行，M6仍未通过。302项测试与Ruff通过。基线2507服务继续驻留GPU0。

当前代码对旧留出60题的开发集重跑已完成：状态契约60/60，无执行错误，40道手册题重排Recall@20=1.0。[逐题差异](runs/p6-v4-v5g/reviewed-dev/development_delta.json)显示33题语义可见内容不变、27题有变化；[27题增量复核单](runs/p6-v4-v5g/reviewed-dev/增量复核_27题.md)待人工判断。这个旧集已是开发资料，不能作为新一轮正式留出成绩。

随后修复“掩码地址还原真实UPF身份”及无日志时的措辞，当前有效开发运行改为[v5h摘要](runs/p6-v4-v5h/reviewed-dev/summary.json)：60/60状态契约符合，无执行错误，重排Recall@20=1.0；33题可见语义不变、27题待[增量复核](runs/p6-v4-v5h/reviewed-dev/增量复核_27题.md)。v5g差异页仅保留作历史记录。304项测试与Ruff通过，M6仍待人工验收。

**最新复核与v5j：**用户已签新60题真值及v5i的3道变化答案。[v5i接收与评分](runs/p6-v4-v5i/review-intake-e025ae9d9ad3/adjudication.json)显示开发集证据支持60/60、答案完整55/60、命令20/20、缺资料6/6；`troubleshooting-014`转为完整，`log-012`被判不完整。v5j已针对`log-012`补充心跳响应为何不能证明独立故障或根因的证据边界，并以[已签真值题库](eval/p6/business_v5_replacement/reviewed_suite.jsonl)重跑开发60题：状态契约60/60、无执行错误、检索门槛通过。57题可见内容不变，[3题增量复核](runs/p6-v4-v5j/reviewed-dev/增量复核_3题.md)待人工判断。[冻结前审计](runs/p6-v4-v5j/pre_freeze_audit.json)核对7份原件SHA、流水线与题库指纹；306项测试和`src`、`tests`范围Ruff通过。新留出集尚未运行，M6仍未通过。

**2026-10-06 v5j正式留出结果：**用户已完成v5j三题增量复核，[开发集人工评分](runs/p6-v4-v5j/review-intake-b1b61ff676af/adjudication.json)为支持60/60、完整56/60、命令20/20、缺资料6/6，语义门槛通过。沿用已获授权的2507 BF16/GPU0/16K/并发1配置，保存[接受决策](eval/p6/development_decision.v5j.accepted.json)并[冻结](evidence/p6/frozen_v5j.json)后，仅运行一次新留出60题。该次[摘要](runs/p6-v4-v5j/heldout-run/reviewed-heldout/summary.json)显示状态契约仅56/60；检索和来源分区通过，但4题未发布有效答案，故**M6未通过**。具体原因和[全部60题人工复核入口](runs/p6-v4-v5j/heldout-run/失败归因与人工复核.md)已保存；同一留出集不能修复后重跑，旧v5f失败记录也不覆盖。模型继续驻留GPU。

**2026-10-07 v5k开发修复：**[修复与回归记录](runs/p6-v4-v5k/修复与回归记录.md)说明命令原文及历史案例改走来源校验后的原生摘录。已消费留出集的5道问题题仅作开发回归，现均可发布有来源的部分答案；原正式失败结果不变。当前开发60题重跑状态契约60/60，无执行错误，手册重排Recall@20=1.0；59题可见内容不变，[log-014单题复核](runs/p6-v4-v5k/reviewed-dev/增量复核_1题.md)待填。309项测试及`src`、`tests`范围Ruff通过。M6仍需[新留出60题实际答案复核](runs/p6-v4-v5j/heldout-run/reviewed-heldout/answer_review.md)与新的独立验收资料；模型继续驻留GPU。

**2026-10-07 复核流程更正：**上段两份“待填”复核表已暂停，不是当前人工待办。已消费v5j留出集的机器门槛失败，逐题评分不能改变该次验收；[历史机器回查](runs/p6-v4-v5l/retrospective_machine_triage.json)列出5处自动定位的问题。评测代码现先执行状态、检索、来源分区及命令原文检查；失败只产生机器故障清单，不再生成新的空白答案复核表，正式留出失败的人工评分提交会被拒绝。先完成自动回归和候选定版，再集中安排真正需要的一次人工验收。M6仍未通过；该次流程修正时P7尚未开始，后续技术实跑见下方记录。2507模型保持驻留GPU。

[v5l当前代码开发回归](runs/p6-v4-v5l/reviewed-dev/summary.json)已完成：60/60状态契约符合，无执行错误，检索与机器复核门槛通过；[可见答案差异](runs/p6-v4-v5l/development_delta.json)只有两道日志题的调查终止理由变化，暂不单独要求人工复核。这是开发回归，未对已消费留出集重测，不能据此宣布M6通过。

**2026-10-07 P7技术准备实跑：**[汇总记录](evidence/p7/summary.json)显示三个全新环境在网络namespace内离线重建，81/60/180个包通过依赖检查，新推理环境的vLLM 0.19.1、PyTorch 2.10.0+cu128导入及CUDA可用性通过。屏蔽Dify/AITO路径与外网后，应用/检索完成两道手册取证、32,539条真实日志及原文上下文验证，缺原件/缺环境均明确拒绝。[恢复一致性](evidence/p7/recovery_consistency.json)确认暂停任务从另一目录的备份恢复后继续执行，17条事实、证据ID及手册引用保持一致，终端`source`校验通过。317项测试、Ruff通过，7份原始资料SHA不变，v5l流水线指纹不变。

本轮是**同机、同虚拟绝对路径的技术验证**：应用/检索隔离，生成仍桥接宿主常驻服务；没有用新推理环境启动第二个模型进程，也未交付跨主机wheel/权重/解析资源包，因此M7尚未完成。M6仍需独立新资料正式验收，当前没有新的人工答案表待填。数据快照、恢复目录位于`/home/huangxiaolin/upf-agent-delivery/p7-20261007/`，使用`runtime-snapshot`的[manifest](/home/huangxiaolin/upf-agent-delivery/p7-20261007/runtime-snapshot/manifest.json)；`source-snapshot`是已被替代的初次试运行，不用于交付。详细命令见[环境与恢复说明](environment-lock/README.md)。2507生成服务健康检查200，继续驻留GPU0。
