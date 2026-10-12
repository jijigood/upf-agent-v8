# P6 开发评测、模型比较与正式验收

**当前状态（2026-10-07）：**v5l开发回归机器门槛通过，M6仍未获新的独立正式成绩。旧增量表的提交已接收或暂停，不需要用户继续填写；下面各版本按时间保留，是历史记录。现有UPF日志十份副本的SHA256相同，[独立来源审计](../evidence/p6/independent_source_audit_20261007.json)没有发现新日志。资料等待期间继续P7隔离重建与恢复技术准备，[复现说明](../environment-lock/README.md)列出命令和范围；技术部署通过不能替代M6业务验收。

120题真值已正式导入，署名按用户指定为张三，日期沿用2026-09-28；不需重做。

原开发60题的答案复核单已接收，署名豆包（AI辅助复核），日期2026-09-29。用户明确确认“目前只是 AI 辅助评分”，因此只作为问题发现依据，不计入人工验收。已保存原始提交并确认问题、预期原文、实际输出与summary/suite SHA绑定均未改动。

本轮AI辅助评分：证据支持56/60（93.3%），完整26/60（43.3%），命令正确20/20，新增关键参数0，缺资料处理3/4（75%）；34题有失败字段，语义门槛未通过。这些分数只对应修复前的60题输出，不是人工业务准确率或修复后成绩。

已补上AI评分来源隔离、指定版本配置发布门槛与被拒绝候选的报告过滤；日志回答增加所问类型的代表原文、状态和定位。原10题日志工具验证通过，计数保持全量；真实TXT版本问题返回missing_source、无配置事实或候选来源、0次模型请求。该阶段的280项测试记录保留为历史结果。

**2026-09-30 修复后开发集状态：**已修复手册章节完整性/发布异常、命令范围与示例限制、日志原文样例、过期拓扑说明及9.9版本拒答，并在新目录完成60题真实开发集：60/60状态契约符合、无执行错误；40道手册题重排Recall@20=1.0、nDCG@8=0.9922。机器逐类检查为命令原生摘录20/20、知识/排障完整章节证据20/20、日志原文10/10、过期拓扑与N30负控3/3、9.9版本拒答2/2；288项测试及Ruff通过。P0的7份data/raw原件SHA不变。检索命中和证据覆盖不等于语义完整性或人工业务准确率。[根因与修复说明](../runs/p6-v4-v5b/修复与根因复核.md)、[新开发集摘要](../runs/p6-v4-v5b/reviewed-dev/summary.json)、[机器检查](../runs/p6-v4-v5b/repair_audit.json)。

v5b运行完成时，[60题答案复核单](../runs/p6-v4-v5b/reviewed-dev/answer_review.md)评分尚空白；随后已收到填写版本，见下方接收记录。旧AI辅助评分只对应更早的v3输出，不能迁移为新答案成绩。当前仍须完成新输出人工确认、当前版本模型/工具/性能出口与冻结保留集验收；M6未通过。原AI评分见[历史修复清单](../runs/p6-v4-v3/review-intake-f7fb338d3c11/results.md)。

**2026-09-30 新复核接收与追修：**用户提交了v5b的60题复核单，已原样归档并与v5b摘要、题库、原始空白模板逐项核对。逐题填写结果为证据支持60/60、完整58/60、命令正确20/20、缺资料处理4/4、凭空增加关键参数0；不完整的两题为`troubleshooting-005/006`，均指出手册N3案例的解决方法却写“N4接口”而答案未明示矛盾。以上是**提交表内容的统计，尚非确认的人工评分**：表中60题均署名“张三”、日期2026-09-29，早于v5b答案在9月30日生成；用户曾说明“张三”可作占位名，实际复核身份/日期正在核实。[原提交与解析回执](../runs/p6-v4-v5b/review-intake-dbbe2ad9cef1/parsed_submission.json)。表尾“命令正确30（含不适用）”不作为统计，适用分母是20题。

已按原件新增N3标题/N4解决方法的来源矛盾提示，保留原文，不推断现场配置；290项测试及Ruff通过。使用新代码在v5c目录再次真实运行60题，状态契约60/60、无执行错误，[机器检查](../runs/p6-v4-v5c/repair_audit.json)通过，保留集未执行。对比v5b用户可见答案，[55题一致、5题变化](../runs/p6-v4-v5c/publication_delta.json)：两道N3题新增提示，另有3道日志题的终止说明或引用上下文变化。已生成[5题增量复核页](../runs/p6-v4-v5c/增量复核_5题.md)和[新60题完整复核单](../runs/p6-v4-v5c/reviewed-dev/answer_review.md)。只有在v5b原表确认为实际人工复核且新旧答案逐题一致时，55题原判断才可考虑沿用；5道变化题仍需确认。M6保持未通过，模型/工具/性能当前版本出口与冻结测试仍待完成。

**2026-09-30 v5c 60题填写接收：**用户已直接填写v5c[完整复核单](../runs/p6-v4-v5c/reviewed-dev/answer_review.md)，原提交已按SHA归档。60题字段齐全、运行摘要/题库哈希匹配，非评分文本与原始模板完全一致；表内结果为支持60/60、完整40/60、命令正确20/20、缺资料处理4/4、关键参数新增0。日期“9.30”只在派生解析中规范为2026-09-30，原文件不回写；“张三”作为用户曾指定的署名标签保留。用户本人是否逐题核对仍待确认，故这组数字仅为提交表统计，未作为人工验收。[接收解析](../runs/p6-v4-v5c/review-intake-bd66c5e75b34/parsed_submission.json)。

20题标“不完整”，其中N6排障2题的意见称仅有症状，但实际输出含症状、信息收集和解决方法；n4switch排障2题的原件信息收集节只有标题、无正文，属于真实源资料缺口；日志10题与拓扑6题复用“缺少有效的信息收集内容”的意见，与题意不符。用户已确认这16题是误填，并要求按题意重新核对。助手逐题核对后建议这16题改判完整，派生候选完整数为56/60；N6两题若另采纳助手建议则为58/60。两种候选值都不是用户人工评分，原表40/60不改写。[逐类核对与派生结果](../runs/p6-v4-v5c/review-intake-bd66c5e75b34/问题核对.md)。n4switch的结构解析与检索已忠实保留空白小节；旧答案未明示“原件仅有标题”，属于呈现逻辑缺陷，现已修复并等待新输出验收。没有补造信息收集步骤。保留集未执行，M6未通过。

**2026-09-30 v5d开发集实跑：**空白信息收集小节现在会在答案缺口和审计字段中明确指出，真实v5c检索结果的定点回放及新模型运行均验证了两道n4switch题；N6两题不会触发空节误报。全项目292项测试、Ruff和格式检查通过。当前代码以同一题库重新运行60道开发题，[摘要](../runs/p6-v4-v5d/reviewed-dev/summary.json)状态契约60/60、无执行错误；[机器审计](../runs/p6-v4-v5d/repair_audit.json)通过原生手册章节20/20、日志原文10/10、过期拓扑3/3、未知版本拒答2/2，7份P0原件哈希未变。自启本地2507服务已停止。[可见答案比较](../runs/p6-v4-v5d/publication_delta.json)显示与v5c有54题一致、6题变化：排障009/010新增资料缺口说明，日志003/007/009/010仅变更引用上下文或终止说明；[6题增量复核页](../runs/p6-v4-v5d/增量复核_6题.md)和[v5d完整空白复核单](../runs/p6-v4-v5d/reviewed-dev/answer_review.md)已生成。机器通过不构成人工评分，v5c原表和独立更正建议均保持原样；冻结保留集尚未运行，M6未通过。

**2026-09-30 v5d复核接收：**用户已填写v5d 60题表并明确声明复核完成。原件归档，与运行摘要/题库哈希绑定；评分以外的题目、原件、输出未改，首页仅将“待填写”说明改为“已填写”。60题评分字段齐全，日期规范为2026-09-30；署名“张三”按用户此前约定视作标签，不作实名核验。[用户声明和接收说明](../runs/p6-v4-v5d/review-intake-fde728cf47de/接收与验收.md)、[正式开发集判定](../runs/p6-v4-v5d/review-intake-fde728cf47de/adjudication.json)记录支持60/60、完整60/60、命令正确20/20、缺资料处理4/4、关键参数新增0，语义门槛通过。P6.1完成；该成绩不能迁移到目标模型、冻结保留集或生产环境。当前代码下的目标模型比较及其他P6出口仍待验，M6未通过。

**2026-09-30 当前版本模型对照：**同一题库、代码和检索索引，2507与3.8各完成60道开发题，状态契约和逐类机器审计均通过。3.8首次启动因对照脚本错用端口18000而被身份检查停止，未产生题目结果；修正为目标模型配置端口18001后完整运行并关闭服务，失败记录单独保留。两轮49题用户可见内容一致，40道手册题与6道拓扑题完全一致；11题差异为10道日志和`missing-002`。[逐题差异](../runs/p6-v4-v5d-target2/publication_delta.json)与[模型选择说明](../runs/p6-v4-v5d-target2/模型对照与选择.md)记录：手册题完整回答p95为2507的2.78秒、3.8的2.84秒；日志诊断p95为64.54秒、106.05秒。3.8答案尚无人工作业务评分，也未证明有可解释的质量收益，因此**默认继续2507**，不宣称两模型普遍优劣。P6.2当前代码对照与默认选择依据已完成；P6.3复杂跨资料Agent增益和P6.4端到端首字指标仍待验，配置未冻结，M6未通过。

**2026-10-01 当前流水线v5e：**针对明确同时要求日志与手册的任务，有限Agent现在先检索手册并发布可回溯的原文；跨资料因果结论没有可靠验证时不发布模型候选。[复杂任务取证对照](../runs/p6-v4-v5d/复杂任务取证对照.md)证实安全边界改善，但同题固定流程用3次工具调用、0次模型调用就找到两类证据，尚不能证明Agent业务增益。修改后流水线指纹为`bb857ccc332c28e3978c19c296d4a2762b10a59a7bbf960e0c1da4035b21b9df`；v5d的模型A/B属于旧指纹，不能当作严格的当前代码A/B。2507仍为保守默认，3.8未获人工评分。293项测试及Ruff通过。

当前代码的[开发集v5e摘要](../runs/p6-v4-v5e/reviewed-dev/summary.json)和[机器审计](../runs/p6-v4-v5e/repair_audit.json)显示60/60状态契约通过、无执行错误；P0原始7份资料未变化。[逐题输出比较](../runs/p6-v4-v5e/publication_delta.json)中57题与已由用户确认复核的v5d可见内容及状态完全一致，3题`log-005/007/010`有引用上下文或终止说明变化。[沿用审计](../runs/p6-v4-v5e/carryforward_review.json)逐题绑定旧评分和两版输出哈希，只沿用57题原判断；3题需在[短复核页](../runs/p6-v4-v5e/增量复核_3题.md)按[v5e完整输出](../runs/p6-v4-v5e/reviewed-dev/answer_review.md)核对。当前代码的60题人工验收暂未完成，也未运行冻结保留集。

当前配置的CLI首字基准已备有[可重试脚本](../runs/p6-v4-v5e/benchmark_cli_first_visible.py)，但首次启动时两张GPU各有约35.6GiB被共享进程占用，GPU0仅余约45.5GiB，低于2507服务的68GiB规划门槛；服务拒绝启动，[阻塞记录](../runs/p6-v4-v5e/cli-first-visible/blocked.json)为0个有效样本。该记录只是第一次尝试；显存释放后的有效实测见下。不能用旧生成组件TTFT代替端到端首字p95。

**2026-10-01 v5e增量复核接收：**用户已对三题变化输出逐题填写并声明完成增量复核。[原件与接收说明](../runs/p6-v4-v5e/review-intake-3db73a9c8b42/接收与验收.md)保留提交原文，核验当前摘要、题库、原始日志和流水线指纹。57题可见输出与v5d完全一致，原用户判断逐题沿用；三题使用本轮2026-10-01的判断。[当前开发集正式判定](../runs/p6-v4-v5e/review-intake-3db73a9c8b42/adjudication.json)为证据支持60/60、完整60/60、命令20/20、缺资料4/4、关键操作参数新增0，语义门槛通过。P6.1当前版本完成。“张三”仍是用户指定的署名标签，不构成实名核验。共享GPU占用持续，首字基准仍无有效样本；复杂Agent增益及严格当前指纹模型A/B未完成，配置和冻结保留集未执行，M6仍未通过。

基于同轮60题的[当前性能预检查](../runs/p6-v4-v5e/current_performance_precheck.json)：40道手册类题完整答案p95约2.78秒，10道日志诊断p95约58.36秒，分别低于计划的60秒与180秒预算。同轮[资源采样](../runs/p6-v4-v5e/resources.json)记录GPU0/1设备总占用峰值约69.35/38.10GiB、0.5秒采样957次；设备总量包含共享任务，不能直接归因本应用。这是开发集评测器的完整答案耗时与资源采样，既没有测CLI首字，也不是每类代表题预热后20次独立重复，不能据此完成P6.4。

[P6.2/P6.3决策草案](../runs/p6-v4-v5e/P6模型与Agent决策草案.md)保留2507默认：旧同题A/B中3.8未获人工评分且日志耗时更高；[当前开发题路由核对](../runs/p6-v4-v5e/model_branch_audit.json)显示新增跨资料Agent分支0/60命中，但严格当前指纹A/B未重跑。有限Agent已能安全并列取证，未证实优于固定流程，故不能宣称有Agent业务质量提升。[冻结配置草案](../eval/p6/development_decision.v5e.draft.json)仍为`configuration_accepted=false`，并已实测会被`freeze-config`拒绝；保留集尚未预占。

[P6当前就绪核对](../evidence/p6/readiness_v5e.json)逐项区分已通过的开发集人工/检索/完整答案预算、已有但包含共享任务的资源采样、未达成的Agent增益，以及被GPU占用阻断的CLI首字。默认模型继续2507，不因缺失的3.8当前指纹实跑而升级模型；配置不冻结，冻结保留集不运行。

用户提出“GPU利用率为0但显存已占用，能否启动”后，已用正式命令实测：GPU0空闲44,203MiB时被68GiB规划门槛拒绝，BF16基线权重分片本身约56.9GiB，单卡无法容纳权重和运行缓存。后续快照GPU0/1空闲约43,118/24,994MiB，利用率均瞬时为0，也不释放已分配显存。[可行性记录](../runs/p6-v4-v5e/gpu_start_assessment.json)还核对了端口8000的旧同名服务：它为32K/并发16/不同显存配置，16-token请求30秒未返回，不能替代P6正式16K/并发1服务。没有结束或修改共享进程，也没有消费保留集。

**2026-10-02 显存释放后实测：**正式2507 BF16、16K、并发1、GPU0服务通过精确配置预检查；[单次`ask --json`基准](../runs/p6-v4-v5e/cli-first-visible-freegpu-20261001/summary.json)对四道已复核开发题各预热一次、各测五次，20次首输出p50/p95为34.14/35.11秒，完整输出p95为35.57秒，未达到10秒首输出预算。该入口每题重新启动嵌入与重排进程，并在完整答案完成后才发布JSON。新增`manual-chat`连续提问入口沿用同一个问答函数和逐题审计路径，在会话内保持检索进程常驻；[20次独立计时](../runs/p6-v4-v5e/manual-chat-first-visible-freegpu-20261001/summary.json)首输出p50/p95为3.36/4.67秒，完整输出p95为4.67秒，达到**这四道代表手册题**的体验预算。会话首次准备约26.48秒，单独计时；JSONL首字发生在完整结果发布时，不将进度提示冒充答案。两组都是单并发、GPU0最高设备总占用69,281MiB；常驻组GPU1设备总占用峰值22,180MiB。服务和会话均由脚本关闭。保留集未消费，M6仍未通过。

**2026-10-02 当前代码v5f开发集：**[60题正式配置复跑](../runs/p6-v4-v5f/reviewed-dev/summary.json)状态契约60/60、无执行错误，检索门槛通过；[逐类机器审计](../runs/p6-v4-v5f/repair_audit.json)原生命令20/20、完整手册章节20/20、日志原文10/10、过期拓扑3/3、未知版本拒答2/2，P0原始7份文件哈希未变。与v5e人工复核答案比较，[56题完全一致、4道日志题变化](../runs/p6-v4-v5f/publication_delta.json)；[沿用审计](../runs/p6-v4-v5f/carryforward_review.json)只保留56题旧判断，`log-003/004/005/010`必须按[四题短复核页](../runs/p6-v4-v5f/增量复核_4题.md)确认。[差异机器核对](../runs/p6-v4-v5f/delta_machine_audit.json)表明四题事实、候选解释和建议不变，6处新版引用均能在原日志连续行找到；变化为引用上下文展开或收缩及三题终止说明，机器检查不能替代人工判断。[同轮性能汇总](../runs/p6-v4-v5f/current_performance_precheck.json)40道手册题完整答案p95=4.79秒、10道日志诊断p95=98.12秒，均低于60/180秒预算；这组数据与上段四道题重复基准口径不同。294项测试及Ruff通过。[当前就绪表](../evidence/p6/readiness_v5f.json)与[冻结决策草案](../eval/p6/development_decision.v5f.draft.json)保持人工验收和配置接受为未完成，程序实测拒绝冻结，保留集标记不存在；M6未通过。

**2026-10-02 v5f增量复核接收：**用户已填写四道变化日志题并明确声明完成复核。接收脚本逐字比对空白模板的非评分内容，核对本轮摘要、题库、原始日志和旧版用户评分的哈希；56题只在可见输出完全一致时沿用，4题采用本轮判断。[提交原件及接收记录](../runs/p6-v4-v5f/review-intake-fb450cc8cee8/接收与验收.md)与[正式开发集判定](../runs/p6-v4-v5f/review-intake-fb450cc8cee8/adjudication.json)显示支持60/60、完整60/60、命令20/20、缺资料4/4、凭空新增关键参数0，当前代码P6.1人工语义门槛通过。署名“张三”为用户此前允许的标签，不作实名核验。[配置决策草案](../eval/p6/development_decision.v5f.draft.json)已绑定判定但仍为`configuration_accepted=false`，需要对具体2507 BF16/16K/并发1与固定工具默认方案作真实接受决定；冻结保留集尚未执行，M6未通过。

## 本次实现

- `eval/p6/business_v4/candidates.jsonl`：120 道有来源的候选题，命令40、知识20、排障20、日志20、合成拓扑10、缺资料10；开发/保留各60。题目近义变体按章节、命令族、日志模板和合成场景分组，分组不跨集。40道命令题只有10个命令族，不能视为40种独立命令。
- `eval/p6/business_v4/reviewed_truth_user_named.md`：每题问题、候选相关块原文、原件位置、预期事实、禁止结论、人工勾选与签名。日志题补充三条代表原文及原生事件ID；候选类型/状态已纳入本轮真值复核，不把解析器标签当人工真值。
- 旧草案 `eval/p6/candidates.jsonl` 原样保留，用于复现本轮兼容/预算实测。新版替换40道知识/排障题及4道已曝光来源的保留命令题，共44题；76题沿用，有些开发题已有历史输出。新版完整120题尚未执行评测，不能把旧草案分数搬过去。新版知识与排障覆盖产品、网管、紧急故障手册；故障题要求区分历史案例与当前现场。
- `p6 cache-retrieval / compare-model`：旧草案42道开发问题（40道手册题及2道未知版本题），两模型复用逐文件哈希相同的检索证据、同一发布策略和4次模型请求预算。只检查机器契约；命令漏答、相关章节错答会明确记录。
- `p6 tool-parameters`：100次真实请求，10族各10次确定性重复，一次修复；验证真实工具参数和用户确认范围，不执行工具。这组重复不代表100个独立业务场景，也不替代 P5 的类型/null/时间/隔离代码边界测试。
- `p6 compare-agents`：五个开发集日志模板，各比较单次统计问答、固定三步工具和有限Agent。固定流程已获题目明确的事件类型，不能用此对照声称Agent必然更优。该对照不是完整手册单次RAG/复杂跨资料任务的业务增益验收；跨资料增益仍待人工真值及现场资料。
- `p6 benchmark`：16K/32K服务容量、客户端并发1/2，1200/5000字符提示预算，每个提示预算先预热1次、再测20次；记录实际服务max_num_seqs、tokens、可见首输出与总时延、0.5秒采样GPU/RSS。容量不是实际输入token数；重复输入可能命中服务默认前缀缓存。
- `p6 benchmark-rag`：一题20次重复，包含预热检索和最终经校验发布的答案。正式应用发布不是流式，生成流首输出与CLI发布耗时分别报告。不能将生成组件TTFT当作端到端首输出。
- `p6 import-review / evaluate / adjudicate / freeze-config`：人工标签导入、复核后开发集执行、人工答案评分、配置冻结和一次性保留集预占。代码/配置/模型清单/活动索引/日志清单/合成拓扑指纹变化会拒绝原冻结配置；正式执行先检查本地服务的模型路径、健康、16K/32K容量、并发、dtype和解析器与配置一致；保留集执行前创建独占标记，失败后也不能重跑同一集调参。

主性能矩阵包含基线4档和目标关闭思考4档；另保留目标low的16K两档失败对照，32K low未执行。优化标志只作用于生成组件基准，未改变普通Agent的low策略。

本机结果见 [实测报告](../evidence/p6/results.md)、[汇总JSON](../evidence/p6/summary.json)、[失败分类](../evidence/p6/failures.json)。42题不含新业务整集；源码适配修订与首版5题失败均保留归档。

正式评测只有先通过机器复核门槛才生成 `answer_review.json`；失败时只生成机器问题清单，不要求人工逐题评分。需要人工评分的运行中，所有适用判断都必须填 true/false、复核人和日期，SHA必须匹配对应summary。人工评分给出分母、支持率、命令正确率和缺资料正确率。`adjudicate` 只判语义门槛，不自动宣称整阶段M6通过；检索、工具、资源及一次冻结测试的出口另行检查。

## 简单日志查询的使用方式

事件类型明确时可直接使用现有确定性入口，例如：

```bash
uv run upf-agent p4 find-events a6f18ac81a18aa2125fa --event-type pfcp_heartbeat_request --limit 3
# 再把返回的event_id交给 p4 read-context。
```

有限Agent的价值应由条件不明确、多来源补查的已标注复杂题验证。当前五个明确类型的对照不能代替该验证，也没有把“自然语言自动改走固定流程”宣称为已经完成的优化。

## 人工复核记录与当前待办

**2026-10-06正式保留集：**配置已接受并冻结，保留60题只运行了一次。运行60/60状态契约符合、0执行错误，重排召回Recall@20=1.0、nDCG@8约0.983，资料分区和原始7份资料哈希不变。[冻结文件](../evidence/p6/frozen_v5f.json)、[一次性消费标记](../eval/p6/heldout_consumed.json)、[结果摘要](../runs/p6-v4-v5f/heldout-run/reviewed-heldout/summary.json)、[机器审计](../runs/p6-v4-v5f/heldout-run/machine_audit.json)可核对。保留集的机器检查不提供证据支持率、完整率或业务正确率；M6继续标记未通过。

[M6逐项出口核对](../runs/p6-v4-v5f/M6_gate_review.md)已把开发集评分、默认模型选择、Agent负面增益结果、本机时延、保留集机器检查和人工待办分列。新做的同缓存开发集手册对照中，2507的42道题均未发起模型请求；它验证确定性摘录路径，不能用于宣称当前代码下2507或3.8生成质量更好。3.8的额外加载已停止，2507按用户要求保持在GPU0。

**2026-10-06人工复核接收：**用户已填写并声明复核保留集60题。原表归档、字段和非评分内容核验通过；日期“10.06”仅在派生记录规范为2026-10-06。正式人工判定支持60/60、完整42/60、命令20/20、缺资料5/6、关键参数新增0；缺资料处理83.3%低于预定90%门槛，`semantic_gate_pass=false`，所以M6正式验收失败。[接收与逐题问题](../runs/p6-v4-v5f/heldout-run/review-intake-232c9043e180/接收与验收.md)、[判定JSON](../runs/p6-v4-v5f/heldout-run/review-intake-232c9043e180/adjudication.json)。知识题`knowledge-017～020`的“不完整”意见称来源版本未知，但题库和引用文件显示V1.3，正在核实；不会自行改分。本保留集已消费，不能看结果修复后再次用它验收。

[失败归因表](../runs/p6-v4-v5f/heldout-run/review-intake-232c9043e180/失败归因与修复边界.md)把原资料空白/截图限制与答案呈现、Agent路由问题分开。直接触发门槛失败的是`missing-007`：现场交换机端口问题误走手册例子。修复后须用新的独立验收集，不把本集再当未见测试集。

**2026-10-06 v5h开发继续：**在v5g修复后，进一步纠正了“掩码地址→实际UPF设备身份”仍误走手册，以及无日志时误写“当前日志事件”的问题。当前代码对旧留出60题仅作开发集重跑，[摘要](../runs/p6-v4-v5h/reviewed-dev/summary.json)显示状态契约60/60、无执行错误、手册40题重排Recall@20=1.0；[逐题差异](../runs/p6-v4-v5h/reviewed-dev/development_delta.json)显示33题语义可见内容未变、27题变化，后者在[当前增量复核单](../runs/p6-v4-v5h/reviewed-dev/增量复核_27题.md)等待人工评分。新留出60题是[未签真值草案](../eval/p6/business_v5_replacement/truth_review.md)，原件路径和定位已列全；新题未经运行，旧保留集不重跑。304项测试及Ruff通过。模型仍驻留GPU0，M6未通过。

**2026-10-06 用户复核后：**新60题真值已签收并导入[审核题库](../eval/p6/business_v5_replacement/reviewed_suite.jsonl)，旧60题真值沿用；新题仍未执行。[v5h原表归档与评分](../runs/p6-v4-v5h/review-intake-3684c65f16f7/接收与评分.md)绑定表格和摘要哈希，支持60/60、完整55/60、命令20/20、缺资料6/6。`troubleshooting-014`仍不完整，已依据邻近案例原文补上两类报错、配置文件路径和关系未明的缺口。当前[v5i开发重跑](../runs/p6-v4-v5i/reviewed-dev/summary.json)使用已审核题库，60/60状态契约符合、无执行错误、检索门槛通过；较v5h仅3题可见内容变化，待[3题短复核](../runs/p6-v4-v5i/reviewed-dev/增量复核_3题.md)。[冻结前技术核对](../runs/p6-v4-v5i/pre_freeze_audit.json)显示P0原件7/7哈希不变、手册p95=25.49秒、日志p95=50.52秒，2507模型常驻GPU0。新留出集尚未消费，M6未通过。

**2026-10-06 v5i复核及v5j：**用户填完v5i三题后，已将原表按SHA归档并合并57题沿用判断。[正式开发判定](../runs/p6-v4-v5i/review-intake-e025ae9d9ad3/adjudication.json)为支持60/60、完整55/60、命令20/20、缺资料6/6；`log-012`因未解释心跳响应为何不能证明故障/根因而不完整，原判定保留。v5j为已观测心跳响应补充与告警、独立故障次数和因果关系的边界，[当前开发重跑](../runs/p6-v4-v5j/reviewed-dev/summary.json)状态契约60/60、无执行失败，手册重排Recall@20=1.0。[逐题差异](../runs/p6-v4-v5j/reviewed-dev/development_delta.json)为57题可见内容不变，3题变化（`log-012/017/018`）；[短复核单](../runs/p6-v4-v5j/reviewed-dev/增量复核_3题.md)待人工判断。[冻结前审计](../runs/p6-v4-v5j/pre_freeze_audit.json)显示原件7/7哈希不变、手册p95=25.81秒、日志p95=42.86秒，新留出未消费。306项测试和`src`、`tests`范围Ruff通过。既定2507服务继续驻留GPU0，M6未通过。

**2026-10-06 v5j冻结后一次性新留出：**用户已完成3题复核，[开发集人工判定](../runs/p6-v4-v5j/review-intake-b1b61ff676af/adjudication.json)支持60/60、完整56/60、命令20/20、缺资料6/6，语义门槛通过。按既定配置[冻结](../evidence/p6/frozen_v5j.json)并一次性执行新留出60题；[正式摘要](../runs/p6-v4-v5j/heldout-run/reviewed-heldout/summary.json)显示56/60状态契约符合，手册重排Recall@20=1.0、来源分区及原件哈希通过，但`v5-command-007/008/015`和`v5-troubleshooting-002`未形成有效答案。[机器审计](../runs/p6-v4-v5j/heldout-run/machine_audit.json)及[失败归因](../runs/p6-v4-v5j/heldout-run/失败归因与人工复核.md)记录生成/证据校验问题，另有`v5-command-019`遗漏预期命令。**M6未通过，当前留出集不得重跑。**原先要求填写的60题实际答案复核单现已暂停，不是当前必须完成的人工任务；填写它也无法改变机器门槛失败。2507服务继续驻留GPU0。

**2026-10-07 v5k开发修复：**根据已消费留出失败题，仅修复可确认的手册发布路径，并将这些题降为开发回归样例。[修复审计](../runs/p6-v4-v5k/repair_audit.json)显示`v5-command-007/008/015/019`和`v5-troubleshooting-002`现输出来源校验后的部分答案；不是第二次正式留出结果。[当前开发60题](../runs/p6-v4-v5k/reviewed-dev/summary.json)状态契约60/60、无执行错误、重排Recall@20=1.0；59题可见答案不变，仅`log-014`终止措辞变化，其[单题复核](../runs/p6-v4-v5k/reviewed-dev/增量复核_1题.md)现已暂缓。309项测试及`src`、`tests`范围Ruff通过。当前仅一份登记原始UPF日志，日志模板已用于前两轮；需要新的独立原始日志或明确降低验收独立性要求，再建候选留出真值。M6仍未通过，2507继续驻留GPU0。

**2026-10-07 复核流程修复：**当前评测代码先以状态契约、执行错误、检索、来源分区及命令原文可见性构造机器复核门槛。失败只保存`machine_failure_triage.json`，不生成新的空白`answer_review.json`；正式留出机器失败时`adjudicate`拒绝接受逐题评分，开发集机器失败时`freeze-config`拒绝冻结。[旧结果回查](../runs/p6-v4-v5l/retrospective_machine_triage.json)对已消费v5j列出5个机器问题，对v5k开发集无机器问题，绝非新正式成绩。v5k的`log-014`单题增量复核也暂缓，待候选稳定后集中处理。以后先自动回归并合并差异，只在机器门槛通过、候选定版且确需人工判断时集中复核；旧真值不重填。独立新留出资料不足时如实标记受限验证，不宣称M6通过。

**同日当前代码开发回归：**[v5l开发集摘要](../runs/p6-v4-v5l/reviewed-dev/summary.json)记录60/60状态契约符合、无执行异常，检索和机器复核门槛通过。[与v5k逐题比较](../runs/p6-v4-v5l/development_delta.json)显示58题可见内容相同，`log-014/017`只有调查停止理由变化；事实、建议及证据缺口不变。该比较只是机器差异审计，不替代这两个变化答案的人工评分，也不制造新的人工待办。v5l没有运行新的正式留出集，M6仍未通过；2507服务继续驻留GPU。

后续开发回归可使用 `python scripts/compare_p6_visible.py --old <旧开发运行目录> --new <新开发运行目录> --output <新差异JSON>`；脚本要求同一题库和同一开发分区，并单列“只有调查终止理由变化”和实质答案变化，不自动沿用人工评分。

此前要求逐题填写[保留60题答案复核单](../runs/p6-v4-v5f/heldout-run/reviewed-heldout/answer_review.md)；现已按上文接收和判定，不再要求重复填写。`missing-007`已由用户判为缺资料处理错误；`knowledge-017～020`的版本意见尚待澄清。原保留集不重跑。评测脚本结束时曾停止自启服务，用户随后要求保留模型常驻，服务已按冻结配置重新启动。

此前v5e开发集人工复核已通过；随后v5f代码复跑、增量人工复核、CLI首字实测、配置接受与一次性保留集运行均已完成。保留集人工复核也已提交，正式门槛失败；需要先确认四题版本意见，修复问题后另建独立验收集。120题原真值和P2原件无需重做。

本次保留集复核单由[排版脚本](../runs/p6-v4-v5e/render_review.py)根据真实输出生成，用户已填写并完成接收。不要再次运行冻结保留集。

评分工具接受review_kind=ai_assisted用于统计，但human_review_complete=false，配置冻结必须拒绝该评分作为人工验收。旧模板answer_review.json保持空值；导入评分保存为本轮目录中的ai_assisted_review.json与ai_assisted_scores.json。原开发摘要和每题输出不回写评分，避免覆盖失败历史。

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

下列为原开发版本的命令示例，当前不可据此冻结；修复后改用新开发摘要和人工评分路径，且只在人工复核及其他出口完成后执行；输出路径必须是新路径，保留旧题库、旧分数和失败样本：

```bash
# 120题reviewed_suite.jsonl已正式导入，当前无需重复导入。
# 有修正时另加 --overrides eval/p6/business_v4/review_overrides.json
# 原开发集已执行，但当前源码已改变；修复完成后须在全新目录执行开发集。
# 阅读/填写当前60题answer_review.md或answer_review.json，保留summary_sha256。
uv run upf-agent p6 adjudicate --suite eval/p6/business_v4/reviewed_suite.jsonl --summary runs/p6-v4-v3/reviewed-dev/summary.json --review runs/p6-v4-v3/reviewed-dev/answer_review.json --output evidence/p6/development-adjudication.json
# 从development_decision.template.json创建决策，绑定summary SHA及adjudication路径；检查计划第4.4和11节所有适用门槛后确认。
uv run upf-agent p6 freeze-config --suite eval/p6/business_v4/reviewed_suite.jsonl --development runs/p6-v4-v3/reviewed-dev/summary.json --decision eval/p6/development_decision.json --output evidence/p6/frozen.json
uv run upf-agent p6 evaluate --suite eval/p6/business_v4/reviewed_suite.jsonl --split heldout --model baseline --frozen evidence/p6/frozen.json --output runs/p6/final-heldout
```

正式主模型升级要求冻结质量不低于基线且有解释得清的收益。只有60题的一次保留集无法同时证明两个模型的非劣比较；若要正式切换，需预先保留独立、同题同证据的基线参考或扩展一次性对照协议，禁止看过保留集后新增比较和调参。目前2507保持默认，3.8保留候选，不能据机器契约或厂商榜单宣布切换。

源日志时区和真实身份未知、真实拓扑缺失仍按缺口处理；无根因真值不报根因准确率。P7技术准备的隔离/恢复结果单独记录在 `evidence/p7/`，不计入P6业务正确率。P1–P5历史证据保留，新增评测证据见 `evidence/p6/`，详细实跑见 `runs/p6/`。
