# P3 本地检索、引用问答与开发对照记录

2026-09-28 更新；2026-09-26 在 `/home/huangxiaolin/upf-agent` 完成。P3.1–P3.2 已完成检索链，P3.3 已增加本地引用问答，P3.4 已实现五配置对照并跑完 12 条开发探针。开发探针未经人工标注，不是正式业务质量验收。P2 已完成助手原件核对与 OCR 纠错，60 条结构样本与 30 张截图仍待人工业务签署；本索引只纳入四份手册的原生 DOCX 文本，不把未确认 OCR 或论文内容当产品证据。

## 构成和运行

`build-index` 从活动 P2 generation 读取手册块，以章节为父级生成段落、表格行组、命令和代码块。命令块附带关联说明；表格块保留单元格与原文定位。每块保存来源哈希、产品/版本、块 ID、OOXML locator 和章节路径。Qwen3-Embedding-4B 生成归一化的 2,560 维向量并写入本地 Qdrant；技术词词典与 jieba/BM25s 形成中文稀疏索引；107 条命令候选形成字面命令索引。索引先在临时 generation 构建，全部成功后切换活动指针；配置、模型、词典、源 generation 变化会要求重建。

`search-index` 对三路候选使用同一产品/版本规则：明确产品必须匹配；明确版本允许相同版本及来源版本未知的手册块，拒绝其他已知版本。命中先以 RRF（k=60）按块 ID 合并，保留精确命令进入最多 32 条重排候选；Qwen3-Reranker-4B 打分后取最多 8 条证据，再添加同章节相邻块。全部上下文上限 5,000 tokens，相邻块单条上限 240 tokens。返回每路排名、原始分数、重排分数、块文本和原文位置；版本未知会明确标注需人工核对适用性。索引中的一处疑似敏感 token 已遮盖，原始 DOCX 定位仍保留在 P2。

## 可复现命令

```bash
cd /home/huangxiaolin/upf-agent
uv sync --extra dev --python 3.11
uv run upf-agent build-index --device cuda:1
uv run upf-agent verify-index
uv run upf-agent search-index '如何执行 show cp-node 查询 SMF 节点信息？' --product UPF --version 5.0 --device cuda:1 --output evidence/p3/show_cp_node.json
uv run upf-agent search-index 'N4 PFCP 链路故障如何排查？' --product UPF --version 5.0 --device cuda:1 --output evidence/p3/n4_pfcp.json
uv run pytest -q
uv run ruff check src tools tests
```

`--device cpu` 可在没有空闲 GPU 时运行，但加载和检索会慢。Qdrant 是本地进程内存储，同一索引目录只允许一个写进程；未来并发服务应切换到本机 Qdrant server。

## 本机实测

活动索引 generation 为 `c61e9796eead2610cfd4`，对应 P2 `c05fe621e37ebdb1c663`。共有 1,061 块：段落 797、表格 153、命令 109、代码 4；最长 600 tokens。BM25 词表 4,442 项；命令索引 107 条、71 个不同别名；Qdrant 1,061 点，维度 2,560。重复构建返回 `reused: true`，未增加索引项。`verify-index` 重新检查活动源哈希、配置指纹、块文件 SHA、尺寸及三路受限查询，结果通过。

以下三个检索样例的排序与 token 数来自 2026-09-26 历史 generation，保留为当日 smoke；本轮新 generation 的逐题证据见新增问答回归。

`show cp-node` 查询的精确/BM25/向量路分别返回 3/20/20 条，融合后 32 条、重排 32 条、输出 8 条证据，含命令本身、调试台入口和“查询对端 SMF 信息”的原文定位；上下文为 727 tokens。N4/PFCP 故障查询的 BM25/向量路各返回 20 条，融合 36 条、重排 32 条、输出 8 条，命中链路异常、检查方式和相关故障案例；上下文为 749 tokens。这些是检索链功能验证，不构成回答正确率统计。

`5GC网管 V1.3 如何查询告警？` 查询的 BM25/向量路各返回 20 条，融合及重排 30 条、输出 8 条，均来自 `5GC网管`、`V1.3`，包含实时告警和历史告警的操作路径；上下文为 1,668 tokens。原生索引的产品/版本分布为网管 V1.3 406 块、UPF 5.0 335 块、UPF 版本未知 320 块。

原始运行产物位于 [`evidence/p3`](../evidence/p3/)：`index_build.json`、`index_reuse.json`、`validation.json` 和各查询的完整排序、来源与定位。

## 当前边界

来源标为 `unknown` 的版本会参与有版本约束的查询，必须在后续答案中带出适用性不确定性。命令索引使用 P2 命令候选，尚待 P2.6 人工核对。当前仅根据块 ID 去除三路重复命中，不合并同一手册不同位置的相似表述；最终证据中可能出现两个相近命令例子。以下记录 P3.3–P3.4 的实现；正式检索质量仍需按 P0 协议完成人工标注。

## P3.3：有来源的本地问答

默认生成模型沿用已通过 P1 的 Qwen3-30B-A3B-Instruct-2507，检索仍为 Qwen3-Embedding-4B + Qwen3-Reranker-4B。生成服务占 GPU 0，检索 worker 在 GPU 1 按需加载。运行时只访问本地模型、原始资料副本、SQLite/Qdrant 与 loopback 推理接口。

`ask` 接受终端问题、UTF-8 TXT 或 stdin；输出 `completed / partial / missing_source / failed`，每条陈述附带引用。代码校验引用 ID、源文件 SHA、归档块文件 SHA 和连续原文。程序把原文按行切成带编号的引用片段（过长行再切分），模型只选择片段编号，代码回填原始文本与真实来源；不让模型重新拼写引用或生成来源哈希。未知编号直接拒绝。命令反引号中的内容必须出现在引用原文。来源不一致的回答不发布，引用失败最多重试一次，再失败返回 `failed`。随后单独调用本地模型检查陈述与证据的支持关系，移除不支持的陈述；这仍是自动检查，不能替代人工语义验收。

指定版本但来源版本未知时，不宣称版本适用，返回 `partial` 和明确缺口。空检索无需生成模型直接返回 `missing_source`；非空但不相关的检索由生成/支持检查拒答。主块及实际扩展的邻块可引用，邻块截断文本必须是归档文本的前缀。引用只使用本次上下文中的内容。

```bash
cd /home/huangxiaolin/upf-agent
# 终端一；需要 GPU 0 有足够空闲显存
uv run upf-agent serve --model baseline --gpu 0

# 终端二
uv run upf-agent ask '如何执行 show cp-node 查询 SMF 信息？' --product UPF --device cuda:1
uv run upf-agent ask --file runs/p3-question.txt --product 5GC网管 --version V1.3 --json
printf '%s\n' '网管历史告警在哪里查询？' | uv run upf-agent ask --product 5GC网管
uv run upf-agent source chunk-2ba8e9f369f045ad715ff45d --generation 4b57484621bf3e547723
```

每次 `ask` 保存 `runs/p3/<run_id>/answer.json`、`answer.md`、`retrieval.json`。JSON 中 `audit` 保存片段选择、展开后的草稿与支持检查布尔结果，草稿不是获准发布的回答，正式回答只看顶层 `claims`。退出码：完成 0、部分回答/缺资料 2、模型/输入/引用运行失败 1（参数用法错误由 CLI 返回 2）。`source` 按回答记录的历史 generation 回查，不会悄悄引用新索引。测试生成服务完成后关闭，使用时需按上面的命令启动。

真实模型检查产物：`evidence/p3/answer_smoke.json` 和 `answer_*.json/md`，覆盖精确命令、网管告警、N4/PFCP 和无关问题；TXT 完整 CLI 查询为 `evidence/p3/cli_answer.json`。这些是功能样例，不能作为语义正确率的分母。

## P3.4：同语料控制变量对照

`ablate-retrieval` 在相同 1,061 块、相同产品/版本过滤、每路 top20、融合最多 32 候选下比较：BGE dense → Qwen dense → Qwen+BM25 → 再加入精确命令 → 再加入 Qwen reranker。BGE 单独存放在 `data/p3/ablation/` 的 `bge_m3_1024` collection，完全不改活动 Qwen 索引。BGE 使用本地 SentenceTransformers CLS pooling 和归一化，不加 query instruction；该用法与 [BGE-M3 官方说明](https://huggingface.co/BAAI/bge-m3)一致。只比较 BGE 的 dense 分支，不宣称复现 Dify 的旧知识库或 BGE 的 sparse/ColBERT 全能力。

```bash
uv run upf-agent ablate-retrieval --device cuda:1
```

默认数据为 `eval/p3_dev_probes.jsonl`，12 条由源章节派生的开发探针；目标集合使用章节匹配，尚未经人工确认完整相关性。P0 的 120 个槽位保持原状，未消费保留测试集。程序拒绝 `split=heldout`，未全数人工确认时指标写到 `unreviewed_target_probe_metrics`。结果 `evidence/p3/ablation.json` 包含数据集 SHA、BGE 实际文件 SHA、Qwen 模型指纹、逐题候选及分数、模型加载与批量推理计时。

| 配置 | 目标集合覆盖@20（代理） | 至少一个目标命中@20 | 目标排序 nDCG@8（代理） |
|---|---:|---:|---:|
| BGE dense | 0.917 | 1.000 | 0.837 |
| Qwen dense | 0.938 | 1.000 | 0.925 |
| + BM25 | 0.944 | 1.000 | 0.954 |
| + 精确命令 | 0.944 | 1.000 | 0.944 |
| + reranker | 0.953 | 1.000 | 0.863 |

这组小样本中，重排提高了目标集合覆盖，但降低了目标排序代理分数；不能声称每加一层就更好。章节派生目标可能遗漏其他相关块，探针措辞也有选择偏差，当前保留配置用于开发，不据此完成模型定版。程序提供的 Recall@20 与 Hit@20 分别计算，多相关块情况下不混用；正式结论须由人工确认 `relevance` 的完整相关块和等级后，在开发集运行并分析错误。最终业务质量验收仍属 P6。

本轮不会把 P2 未确认命令或 OCR 标成已审核。M3 的“可运行”与 P2/P6 的人工质量验收分别记录。

自动化测试结果见 `runs/quality-tests.log`，涵盖非法引用、命令改写、未知片段编号、空证据、版本未知、支持检查否定、邻块截断、源文件篡改、排序指标区分等；Ruff 检查通过。四类真实生成 smoke 均符合预期状态：命令与 N4/PFCP 为 `partial`（未知版本），网管告警为 `completed`，无关问题为 `missing_source`。

## 2026-09-28：质量修复和端到端开发回归

剔除两条 `cp:`/`ls:` 终端诊断后，重建到 P2 `c05fe621e37ebdb1c663` / P3 `c61e9796eead2610cfd4`。107 候选命令、1061 块、2560 维均通过活动源/索引验证，重复构建不增加点。旧索引保留，历史引用仍按旧 generation 解析；12 条开发探针通过不变的原始 block IDs 重绑到新索引，旧数据/对照保存在 `evidence/p3/archive/`。上表为新索引的重新实测结果，仍不作为人工 Recall 或模型胜负结论。

新增 `eval/p3_answer_regression.jsonl`：12 题手册问答、2 题非相关/无现场数据、1 题不存在产品范围、1 题未知版本，共 16 条冻结开发回归。正向题复用同语料、同配置、同 top20/32/8 和上下文预算的对照排名；负向题调用完整生产检索。每题保存检索、回答、来源、耗时、固定关键字检查、状态/拒答与引用原文校验，报告包含数据、对照、代码和模型配置指纹。未经人工标注的语义事实仍为 pending，不能把关键字检查通过率叫作业务准确率；120 个 P0 槽位未动，未使用 heldout。

首轮 15/16 通过机器契约：无线信道题曾拼出无证据命令，被引用校验拦住，状态为 failed，未发布错误回答。首轮完整报告归档于 `evidence/p3/archive/c61e9796eead2610cfd4/answer-v1/`。由此增加 `p3-answer-v2-evidence-gate`：先用结构化证据相关性判断验证至少一个实质问题有原文支持，不能仅因同属 UPF 或数字相近就生成；假 quote ID、正向无支持 ID、负向仍带支持 ID/不解释缺口均失败关闭。无实质证据直接 missing_source，相关内容仅版本未知则继续回答并保留适用性缺口。引用校验和生成后支持检查继续保留。门控是自动判断，仍可能误拒或漏拒，正式语义质量留给 P6。

```bash
uv run upf-agent serve --model baseline --gpu 0
# 另一个终端
uv run upf-agent ablate-retrieval --device cuda:1
uv run upf-agent evaluate-p3 --device cuda:1
```

最终逐题结果见 [开发问答回归](../evidence/p3/quality_regression.md)；初次失败与开发修复后的重跑分别记录，不能包装成一次独立保留测试验收。

第二轮相关性模型仍将 N4 切换错判为无线切换，报告保留于 `answer-v2/`，再次为 15/16，引用校验仍阻止错误发布。因此最终增加 `p3-answer-v3-source-term-gate`：从问题提取显式英文技术标识（命令/带连字符或数字的标识/缩写），回查**完整的当前产品/版本原生手册**；标识没有原文依据则在调用生成模型前返回 missing_source。该规则按 ASCII 标识边界匹配，不把 N40 当 N4，正确处理 5GC / V1.3；普通英文疑问词和纯数字不当作技术名词。`absent_feature_guard.json` 验证 Wi-Fi 请求即使输入 N4 切换的检索结果也不调用模型。

此策略保守，名称仅以中文或未登记别名出现的题可能被拒绝；缺口会提示补充资料或核对名称，不自动猜别名。后续 P6 可在人工依据下维护受控别名字典和评价误拒率。语义相关性门控、引用校验、生成后支持检查继续运行。最终第三轮对同一冻结开发集完整重跑，源语料、模型与检索参数保持不变；不是新的 heldout 验收。

## 最终发布策略与验证结果

最终使用 `p3-answer-v4-source-extracts`。第三轮真实模型结果达到 16/16 机器契约，但逐条助手复查发现 6 类归纳疑点；已保留该轮回答和 `semantic_review.md`，没有把字符串校验包装为语义正确。默认正式 `claims.text` 只发布选中的引用原文，模型归纳留在 `audit`，因此动作顺序、引号、参数与事实范围不再由模型改写。回答为证据片段，仍可能不完整或选择不够相关，示例地址不代表现场地址。出现 heredoc 起始行却未引用结束符时强制 partial 并解释缺口。

验证为 **52 项测试通过，Ruff 通过**；第三轮 16 题真实模型输出已归档于 `answer-v3/`，再通过 `scripts/replay_p3_publication.py` 对同一输出应用确定性的原文发布规则，16/16 机器契约与原文发布一致性通过，未将重放记为 16 次新模型推理。当前生产代码另通过真实 TXT CLI 查询，记录见 `cli_quality_answer.json`。所有源/索引校验、幂等导入、历史来源回查仍通过。

P3 的技术实现与开发回归已收口；M2 人工业务签署、原件疑点处理与 P6 的独立语义/完整性/现场适用性评测仍待完成。默认业务模型仍未通过 P6 定版，不能宣称 100% 业务准确率。
