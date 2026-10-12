# P6 开发评测、模型比较与正式验收

P2 的原文与截图复核已通过。P6 需要另外确认业务问题的预期答案、相关证据、缺资料边界，以及模型实际答案是否完整。已接收旧版复核：116题通过、4题不通过；复核人仍为“AI辅助复核（待人工签名）”。旧版原件保留，实际署名待补；新题与修正题仍待复核，没有执行保留集。正式 M6 暂不通过。本轮全工程248项测试通过；检查日志见evidence/p6/review_followup/059da33fbaf3d338。

## 本轮复核接收与来源修正

本次填写的是 `eval/p6/truth_review.md` 旧版。与v3相比，76题题目与真值相同，其中72题原结论通过，另4题（command-009至012）不通过；44题已经换成新版业务问题，因此不能继承旧结论。复核信息原样保存在 `evidence/p6/review_followup/059da33fbaf3d338/submitted_truth_review.md`。

已核实并修正“相关说明”拼接：命令格式只引用p[177]，示例独立引用p[183]，不再将人工标签当成原文。全量107个命令块已逐块与原始OOXML及自身定位核对，原P2提取与用户签署不变。新P3索引为 `daa6f8e85f8a664b0a55`，1,061块；原索引与本机性能结果留作历史，不能当成新索引的业务验收。

当前题库为 `eval/p6/business_v4/candidates.jsonl`：保持v3的全部问题、分组和开发/保留划分，只更新来源ID及4题预期原文。默认P6 CLI使用v4。

- 内容复核只需查看 [本轮48题](../eval/p6/business_v4/pending_48_review.md)：44道新版题及4道修正题。
- 原件路径与章节见 [48题原件定位](../eval/p6/business_v4/pending_48_sources.md)。
- 完整120题与72题旧结论在 [v4完整复核单](../eval/p6/business_v4/truth_review.md)。72题不需要重做内容复核，但实际复核人和日期需要明确；不得把“待人工签名”导入为正式真值。
- 若填写48题独立文件，我会先合并到完整单并核对改动，再调用严格导入；不会直接把48题当作完整120题导入。

正式导入仍未执行，开发模型评测与冻结保留集仍未执行。下面旧版实测属于历史；继续验收时按v4命令执行。

## 本次实现

- `eval/p6/business_v3/candidates.jsonl`：120 道有来源的候选题，命令40、知识20、排障20、日志20、合成拓扑10、缺资料10；开发/保留各60。题目近义变体按章节、命令族、日志模板和合成场景分组，分组不跨集。40道命令题只有10个命令族，不能视为40种独立命令。
- `eval/p6/business_v3/truth_review.md`：每题问题、候选相关块原文、原件位置、预期事实、禁止结论、人工勾选与签名。日志题补充三条代表原文及原生事件ID；候选类型/状态仍需人核对，不把解析器标签当人工真值。
- 旧草案 `eval/p6/candidates.jsonl` 原样保留，用于复现本轮兼容/预算实测。新版替换40道知识/排障题及4道已曝光来源的保留命令题，共44题；76题沿用，有些开发题已有历史输出。新版完整120题尚未执行评测，不能把旧草案分数搬过去。新版知识与排障覆盖产品、网管、紧急故障手册；故障题要求区分历史案例与当前现场。
- `p6 cache-retrieval / compare-model`：旧草案42道开发问题（40道手册题及2道未知版本题），两模型复用逐文件哈希相同的检索证据、同一发布策略和4次模型请求预算。只检查机器契约；命令漏答、相关章节错答会明确记录。
- `p6 tool-parameters`：100次真实请求，10族各10次确定性重复，一次修复；验证真实工具参数和用户确认范围，不执行工具。这组重复不代表100个独立业务场景，也不替代 P5 的类型/null/时间/隔离代码边界测试。
- `p6 compare-agents`：五个开发集日志模板，各比较单次统计问答、固定三步工具和有限Agent。固定流程已获题目明确的事件类型，不能用此对照声称Agent必然更优。该对照不是完整手册单次RAG/复杂跨资料任务的业务增益验收；跨资料增益仍待人工真值及现场资料。
- `p6 benchmark`：16K/32K服务容量、客户端并发1/2，1200/5000字符提示预算，每个提示预算先预热1次、再测20次；记录实际服务max_num_seqs、tokens、可见首输出与总时延、0.5秒采样GPU/RSS。容量不是实际输入token数；重复输入可能命中服务默认前缀缓存。
- `p6 benchmark-rag`：一题20次重复，包含预热检索和最终经校验发布的答案。正式应用发布不是流式，生成流首输出与CLI发布耗时分别报告。不能将生成组件TTFT当作端到端首输出。
- `p6 import-review / evaluate / adjudicate / freeze-config`：人工标签导入、复核后开发集执行、人工答案评分、配置冻结和一次性保留集预占。代码/配置/模型清单/活动索引/日志清单/合成拓扑指纹变化会拒绝原冻结配置；正式执行先检查本地服务的模型路径、健康、16K/32K容量、并发、dtype和解析器与配置一致；保留集执行前创建独占标记，失败后也不能重跑同一集调参。

主性能矩阵包含基线4档和目标关闭思考4档；另保留目标low的16K两档失败对照，32K low未执行。优化标志只作用于生成组件基准，未改变普通Agent的low策略。

本机结果见 [实测报告](../evidence/p6/results.md)、[汇总JSON](../evidence/p6/summary.json)、[失败分类](../evidence/p6/failures.json)。42题不含新业务整集；源码适配修订与首版5题失败均保留归档。

正式评测生成 `answer_review.json`，所有适用判断都必须填 true/false、复核人和日期；SHA必须匹配对应summary。人工评分给出分母、支持率、命令正确率和缺资料正确率。`adjudicate` 只判语义门槛，不自动宣称整阶段M6通过；检索、工具、资源及一次冻结测试的出口另行检查。

## 简单日志查询的使用方式

事件类型明确时可直接使用现有确定性入口，例如：

```bash
uv run upf-agent p4 find-events a6f18ac81a18aa2125fa --event-type pfcp_heartbeat_request --limit 3
# 再把返回的event_id交给 p4 read-context。
```

有限Agent的价值应由条件不明确、多来源补查的已标注复杂题验证。当前五个明确类型的对照不能代替该验证，也没有把“自然语言自动改走固定流程”宣称为已经完成的优化。

## 现在人工需要完成什么

先完成上述48题及实际署名；完整业务真值单为 [v4](../eval/p6/business_v4/truth_review.md)。每题核对：问题可否由给定资料回答、相关块集合是否漏项/多项、命令参数与版本是否一致、日志状态是否正确、结论是否越过资料边界。拓扑五份CSV均为合成测试，不能确认真实现场连接。

逐题把复核框改为 `[x]`，结论填“通过”，复核人填实际确认人，日期填 YYYY-MM-DD。命令题建议两次独立核对关键字符串，第二次核对可另写“第二次命令核对”记录；修正意见只填写需修改的内容或“无”。如果题目或真值需改，保留修改意见，并提供按题号组织的JSON覆盖字段（question/evidence_ids/expected_extracts/forbidden_claims/expected_statuses）；程序拒绝忽略修正意见或擅自更改分组。不要仅签“AI辅助待人工签名”。不通过的题先修订并再次确认；不要为了通过率删题或挪动保留集。

导入时校验每个原生块的实际章节与原件SHA、日志事件的generation和原始字节、合成CSV的实际文件及数据行（表头第1行，数据从第2行开始）；拒绝来源跨开发/保留分组。允许同组内修正真值；跨章节/场景修订需建立新版本，再正式评测。正式检索报告分别列出精确命令、BM25、dense、RRF、reranked；Recall与Hit分开，缺失或失败不从分母剔除。机器检索门槛不代替人工相关性。

相关性确认针对整组候选块，而非只看标题。命令场景中同一章节可能包含多个工具写法，请明确题目问哪一种；无依据的题明确标缺资料。原生DOCX命令与已审OCR仍遵守各自来源级别，OCR不自动加入本次权威检索。

模型答案复核在标签完成后开展：逐题判断引用是否支持问题、事实是否完整、必要操作前提是否遗漏、版本是否串用、无依据是否正确说明。先复核开发集，失败可在开发集修复；所有配置固定后才能运行一次保留集，再复核其实际答案。

## 复现命令

```bash
cd /home/huangxiaolin/upf-agent
uv run upf-agent p6 --help
# 先启动所选本地服务；检索模型使用GPU1，生成使用GPU0。
uv run upf-agent serve --model baseline --gpu 0 --max-model-len 16384 --max-num-seqs 1
# 以下为开发草案测试，不会消费heldout。
uv run upf-agent p6 cache-retrieval --suite eval/p6/candidates.jsonl --output runs/p6/new-cache
uv run upf-agent p6 compare-model --suite eval/p6/candidates.jsonl --model baseline --cache runs/p6/new-cache --output runs/p6/new-baseline
uv run upf-agent p6 tool-parameters --model baseline --output runs/p6/new-parameters.json
uv run upf-agent p6 compare-agents --suite eval/p6/candidates.jsonl --model baseline --output runs/p6/new-agents
# benchmark的server-pid必须是该模型服务的真实PID，配置必须匹配。
uv run upf-agent p6 benchmark --model baseline --context 16384 --concurrency 1 --server-pid <PID> --output runs/p6/new-perf.json
# 目标模型生成组件优化实验：服务改为target，选定容量和并发；普通Agent策略不受此选项影响。
uv run upf-agent p6 benchmark --model target --thinking-policy off --context 16384 --concurrency 1 --server-pid <TARGET_PID> --output runs/p6/new-target-off-perf.json
```

下列流程只在人工复核完成后执行；输出路径必须是新路径，保留旧题库、旧分数和失败样本：

```bash
uv run upf-agent p6 import-review --suite eval/p6/business_v4/candidates.jsonl --review eval/p6/business_v4/truth_review.md --output eval/p6/business_v4/reviewed_suite.jsonl
# 有修正时另加 --overrides eval/p6/business_v4/review_overrides.json
uv run upf-agent p6 evaluate --suite eval/p6/business_v4/reviewed_suite.jsonl --split dev --model baseline --output runs/p6/reviewed-dev
# 人工填写 reviewed-dev/answer_review.json，保留summary_sha256。
uv run upf-agent p6 adjudicate --suite eval/p6/business_v4/reviewed_suite.jsonl --summary runs/p6/reviewed-dev/summary.json --review runs/p6/reviewed-dev/answer_review.json --output evidence/p6/development-adjudication.json
# 从development_decision.template.json创建决策，绑定summary SHA及adjudication路径；检查计划第4.4和11节所有适用门槛后确认。
uv run upf-agent p6 freeze-config --suite eval/p6/business_v4/reviewed_suite.jsonl --development runs/p6/reviewed-dev/summary.json --decision eval/p6/development_decision.json --output evidence/p6/frozen.json
uv run upf-agent p6 evaluate --suite eval/p6/business_v4/reviewed_suite.jsonl --split heldout --model baseline --frozen evidence/p6/frozen.json --output runs/p6/final-heldout
```

正式主模型升级要求冻结质量不低于基线且有解释得清的收益。只有60题的一次保留集无法同时证明两个模型的非劣比较；若要正式切换，需预先保留独立、同题同证据的基线参考或扩展一次性对照协议，禁止看过保留集后新增比较和调参。目前2507保持默认，3.8保留候选，不能据机器契约或厂商榜单宣布切换。

源日志时区和真实身份未知、真实拓扑缺失仍按缺口处理；无根因真值不报根因准确率。P7断网隔离未测试。P1–P5历史证据保留，新增评测证据见 `evidence/p6/`，详细实跑见 `runs/p6/`。
