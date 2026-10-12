# P2 手册结构化验收记录（更新至 2026-09-28）

P2 的自动化实现已在独立工程运行。四份 DOCX、论文 PDF、OCR 模型和待处理日志/DSL 均按 P0 白名单及 SHA-256 复制到 `data/raw/`；`config/corpus.yaml` 已指向该目录。当前运行不需要访问 Dify 目录。原件和 SQLite 存在于忽略版本控制的 `data/`，可复查的报告在 `evidence/p2/`。

**当前状态：M2 人工验收已完成。**两轮用户复核合计 60 条结构样本和 30 张截图通过，原有 7 条模糊/遮挡行接受继续隔离。下文保留初次待审与首轮不通过记录，最新结果见本文末尾的修正复核收口。

## 系统组成与边界

| 组件 | 作用 | 关键实现/产物 |
|---|---|---|
| DOCX 原生解析 | 按 OOXML 正文顺序保留标题、段落、列表、表、单元格、文本框、图片 | `docx_parse.py`、`data/p2/media/` |
| 命令候选 | 记录精确原始语法、占位参数及相邻前提/示例引用 | `commands.py`、SQLite `commands`；全部标记 `candidate_requires_review` |
| 版本化文档库 | SHA 校验、幂等导入、原子切换 generation、产品/版本过滤 | `corpus_db.py`、`data/p2/corpus.sqlite3` |
| 截图 OCR | 从截图候选中选 30 张，记录识别文字、置信度、坐标、图片哈希 | PP-OCRv5 server det/rec，`ocr_30.json`；全部标记 `ocr_unverified` |
| PDF 论文分支 | 使用本地 Docling standard pipeline 提取页码、文本、边界框 | `pdf_adapter.py`、`paper_docling.json`；角色固定为 `paper` |
| 辅助资料附着 | OCR 与 PDF 在当前 generation 下幂等纳入，按角色隔离 | `auxiliary.py`，`auxiliary_items`/`auxiliary_assets` |

**DOCX 抽取结果。**活动 generation 为 `c05fe621e37ebdb1c663`，见 `evidence/p2/ingest.json`：四份手册共 9,713 块、126 张表、871 表行、107 条命令候选。表格记录 8 处横向跨格、47 处纵向合并起点、89 处纵向延续，并同时保留单元格原文与合并后的有效值。OOXML 有 58 个文本框节点，其中 3 个是 `AlternateContent` 的 Fallback 重复分支；保留 Choice 后实际 55 个文本框。四份 DOCX 媒体目录共 472 个文件，正文有 474 次图片引用，另保留 1 个未被正文引用的媒体对象。图片、表格和文本框均有 OOXML 定位；Word 原件没有稳定页码，引用不填写猜测页数。

命令采用保守识别：107 条候选中 18 条保留了原文 `<...>`/`{...}` 等参数占位符，14 条连接到同节前提段落，4 条连接到示例段落。当前没有发现足以可靠配对到这些命令的相邻参数表，因此 `parameter_block_ids` 留空；不会把远处的表格猜成参数定义。所有候选仍待 P2.6 人工确认后才能用作权威命令。

**OCR 和 PDF。**30 张截图产生 1,712 条 OCR 行，逐行保留 box、score、原图哈希及上下文章节；`upf-agent ocr-search N4` 已能回查 N4 截图。PaddleOCR 3.7.0、PaddlePaddle 3.2.0 与 PP-OCRv5 server 检测/识别权重均在本机独立目录。论文 PDF 12 页经 Docling 2.130.0 离线解析出 57 个项目，其中有 2 张表，全部有页码与边界框；另保存 12 页 pypdf 文本层后备结果。论文来源哈希与 P0 清单一致，只作为 `paper` 存放，手册 `commands` 表仅含 `manual` 来源。OCR 截图文字和命令可能出现断行或误识别，未完成人工确认前不进入权威命令记录。

**离线资产。**`evidence/p2/assets-manifest.json` 列出 OCR 两模型及 Docling 布局/表格资产的逐文件 SHA-256 和树哈希；`environment-lock/ocr.freeze.txt`、`docling.freeze.txt` 固定运行环境。Docling 使用 `do_ocr=False`、`enable_remote_services=False` 和本地 `artifacts_path`；OCR 运行显式指定本地模型路径。下载只发生在准备资产阶段，解析运行使用本地路径及离线环境变量。

## 可复现命令

```bash
cd /home/huangxiaolin/upf-agent
uv run upf-agent ingest-documents
uv run upf-agent p2-review-packet
mkdir -p runs/p2
.venv-ocr/bin/python src/upf_agent/ocr_adapter.py evidence/p2/image_review_queue.json runs/p2/ocr_regenerated.json /home/huangxiaolin/models/ocr/PP-OCRv5_server_det /home/huangxiaolin/models/ocr/PP-OCRv5_server_rec
.venv-docling/bin/python src/upf_agent/pdf_adapter.py data/raw/提取自main.pdf evidence/p2/paper_docling.json /home/huangxiaolin/models/docling paper-d23b138f9a73d510
uv run upf-agent attach-p2-assets
uv run upf-agent repair-ocr
uv run upf-agent verify-p2
uv run upf-agent manual-blocks --product UPF --version 5.0 --kind table --limit 5
uv run upf-agent ocr-search N4 --limit 2
uv run upf-agent paper-search RAG --limit 2
```

重复执行 DOCX 导入返回 `reused=true`，活跃 generation、块数和命令数不变；改变解析器版本会得到新 generation。重复附着 OCR/PDF 同样返回 `reused=true`。导入事务失败不会替换旧活动 generation。来源按产品和版本过滤；论文检索使用单独命令，OCR 结果也有独立的未确认角色。

## 初次抽验与剩余工作（历史记录）

`evidence/p2/structure_review_60.json` 按命令、表行、操作步骤各抽 20 条，60/60 已通过对原始 OOXML 定位和原文的逐字机器回查；命令语法与原文块一致。[当前人工复核单](/home/huangxiaolin/upf-agent/evidence/p2/review_sheet_c05fe621e37ebdb1c663_v3.md)汇总这 60 条和 30 张截图，并链接到原图。测试包括真实来源重复导入、版本过滤、兼容分支、合并格、误识别命令排除、参数字符保留、OCR 哈希和辅助资料隔离。本轮补充诊断行排除、步骤类别、纠错前文/重复目标/越界拒绝、原文与坐标保留、隔离搜索、旧 generation、复核注释归档等回归；完整测试结果见 `runs/quality-tests.log`，Ruff 检查通过。

计划 P2.6 要求**人工核对结果**。该工作不能由机器逐字比对替代；目前结构抽验 60 条和截图清单 30 张的 `human_status` 均为 `pending`，未填写人工签字或质量结论。人工核对时应特别检查命令大小写、冒号与等号、连字符与下划线、I/l/1、O/0、IP/端口、跨格表头和截图裁切；用户只填写当前 Markdown 复核单，维护者根据实际签署同步 JSON 状态，再决定是否将 OCR 文字纳入后续检索。P3 可以先用已验证的 DOCX 原生文本推进，M2 人工验收待复核后勾选。

## 用户复核报告的纠错闭环（2026-09-28）

已对照原图核查用户报告的 122 条发现，保留不可变的 `ocr_30.json` 和用户报告。`ocr_corrections.json` 按截图/行号记录原始文本、报告建议、最终处置、原因和 SHA；`repair-ocr` 校验原始 OCR、报告、图片和 generation 后生成 `ocr_corrected.json`。116 条发现纠错，截图 16 PCI 尾部 `.00` 属于原图内容，报告建议 `.0` 为明确误报；5 条模糊/冲突发现及截图 14 的 2 条遮挡行被隔离。截图 8–10 的原图 `ne=2288` 与报告建议不同，按原图保留或隔离；不能把它默认为 `2268`。截图 14/21 明确仅覆盖可见区域，不能据截图还原完整配置。

纠错不改变原始坐标与置信度，1712 行均有原文对照。状态为 `ocr_assistant_corrected_unverified`、人工签署为 false；SQLite 保留原始/纠错/隔离角色，`ocr-search` 默认使用纠错副本且排除隔离行。纠错 OCR 与论文均不进入 P3 原生产品证据索引。源内容未变的重建通过块 ID、来源 ID 和原图 SHA 重新绑定 OCR，历史原件不改写；内容变化即拒绝绑定。不要覆盖原始 `ocr_30.json` 重新识别，新增识别结果放 `runs/p2/` 并另做复核。

原结构包中混入了终端报错、标题和输出；已用 `commands-v4` 与 `review-selection-v3` 修复。当前命令/表行/步骤各 20 条均完成助手对原件与类别、邻近上下文的核对，见 [逐条核对记录](../evidence/p2/structure_audit.md)。6 处原件疑点包含 heredoc 片段、core_pattern 尾部百分号、命令行中的中文说明、两处指标映射和 Unlock 文案。忠实抽取不代表这些原件事实正确，未擅自改写原手册。原抽样与注释归档保留；同版本重跑不覆盖复核注释。

验证结果：4 份源 SHA、9713 块、126 表、107 候选命令、60 条原件回查、30 图/1712 OCR 行、12 页/57 项论文、隔离角色与纠错血缘均通过。重复导入/附着/纠错得到一致数量与 SHA。技术修复已完成，助手核对为 60/60、30/30；人工签署仍为 0/60、0/30，M2 的人工业务验收不提前勾选。

另对**全部 144 个合并单元格**独立回查原始 OOXML：8 个横向跨格、47 个纵向起点、89 个纵向延续的 column/span/vMerge 属性与 raw/effective 文本来源一致。证据见 `evidence/p2/merged_cells_audit.json`，由 `scripts/audit_p2_structure.py` 重现；此为原件结构验证，不替代人工业务判断。

## 初次复核的填写说明（历史记录）

只填写 [当前复核单](../evidence/p2/review_sheet_c05fe621e37ebdb1c663_v3.md)，不要继续填写旧 `bf8fb923cd90036e501f` 版本，也不需要重写已有的 122 条 OCR 报告。原始手册位于 `data/raw/`，原图链接已在复核单中。复核期间不执行安装、重启或其他手册命令。

1. 命令、表行、步骤各 20 项：逐项对照原件，确认内容、章节、表头/合并关系、步骤顺序和上下文。写 `通过/不通过/无法确认；问题及精确修正文；复核人；日期`，只有通过才勾选。命令抽取忠实与命令是否可直接执行应分别说明。
2. 30 张截图：比较 [纠正后逐行文本](../evidence/p2/ocr_corrected_text.md) 与原图，在对应截图条目填写确认或纠错。特别检查截图 8 第 54 行、截图 14 第 68/69 行、截图 22 第 68/102/121/142 行；看不清可明确接受继续隔离，不能补猜。截图 16 原图 PCI 末尾是 `.00`，截图 8–10 可见网元参数为 `ne=2288`，请核对原图后确认；截图 14/21 不代表完整配置文件。
3. [结构审查](../evidence/p2/structure_audit.md) 的 6 处原件疑点：命令 01 是 heredoc 开始片段；命令 06 的 core_pattern 末尾 `%`；命令 12 含中文执行说明；表行样本 36/37 的指标解释；步骤样本 49 的 Unlock/锁定文案。若原件本身错误，请明确写“抽取一致，但原文疑似错误”，给出依据或保留无法确认。

可以在复核单末尾记录共同复核人和日期，逐项仍应保留通过/失败/不确定范围。系统不会自动把空白、助手意见或勾选以外的模糊注释转成人工通过；收到文件后再同步实际结果。P6 的 120 条正式评测标注属于后续工作，当前不用一次性完成。

P4 的现场补充资料是日志原始时区与真实拓扑 CSV/XLSX 路径；缺失时分别保持 `unknown` 和“无真实拓扑”，不妨碍代码及合成边界测试。

## v3 首轮用户复核与修正（历史记录）

用户明确提交完成复核的当前 v3 文件，已读取并绑定其 SHA-256。90 项均有结论：命令、表行、步骤各 20 条均通过；截图 26 条通过，01/07/17/20 共 4 条不通过。结果保存为 [复核接收记录](../evidence/p2/human_review_v3.json)。文件仍写“AI辅助复核（待人工签名）”，接收记录如实保留该字段，并记录用户本次明确的完成声明；没有代填人名或逐项签名。此前 0/60、0/30 是本次提交前的历史状态。

原件 6 处疑点按用户意见保留：抽取一致不表示原手册无误，heredoc 起始片段不成为完整脚本，原文疑似错误不擅自改写。7 条模糊/遮挡 OCR 行继续隔离，截图可见区域通过也不表示补全被遮挡文字。60 条样本通过不自动批准全部 107 条候选命令，也不授权在设备上执行。

已修正 4 张截图中的 20 个 OCR 片段（17 个新增目标、3 个已有纠错更新），原图核对后恢复接口索引、括号、数字、大小写、GRUB 下划线与重复等号；补充截图 20 的 6 条同一视觉行拼接。原始坐标、置信度、OCR 文本与段号保留，拼接行另附原段号和各片段坐标，不把编辑器行号计为配置文本。纠错账本共 139 个目标，133 条纠错、1 条原报告误报、5 条模糊项及另 2 条遮挡行隔离。26 张已通过图片的内容未变。

提交文件、原始 `ocr_30.json` 和旧用户报告不改写，纠错前副本保存在 `evidence/p2/archive/user_review_v3/`。更新后的 `ocr_corrected.json` 已同步 SQLite 的辅助资料；OCR 不进入 P3 原生手册索引。复核状态使用独立的 `human_review_v3.json`，不把冻结的机器结构包与助手审查记录改成人工意见。`verify-p2` 校验接收记录绑定的来源，报告已复核 60 条结构样本、30 张截图，同时分别报告通过 60/26 和待重查 4 项；技术 `pass=true` 不表示 M2 人工出口通过。

现在只需检查 [4 张截图修正复核单](../evidence/p2/review_followup_v3_4_images.md)，可逐项填写或回复“4 项修正均通过”；无需重做其余 86 项。修正由助手完成，不能自动覆盖本轮“不通过”结论，所以 M2 保持未勾选。P6 的正式真值标注与 P4 的真实时区/设备/拓扑仍是独立待办。

复现：

```bash
# 校验纠错账本及提交文件，重建辅助副本；不覆盖用户复核单
uv run upf-agent repair-ocr
# 本次 --user-confirmed 来自用户明确提交完成复核的消息
uv run python scripts/sync_p2_review.py --user-confirmed
uv run upf-agent verify-p2
```

本轮完整回归 **203 项测试通过（18.31 秒）**，Ruff 与 69 个文件格式检查通过。结果见 `evidence/p2/user_review_tests.log`；新增配置行拼接测试验证源坐标保留、文本必须由现有片段拼成、乱序/重复/越界及隔离文本不能进入拼接。

## 修正复核收口：M2 完成

已收到用户确认并读取 `review_followup_v3_4_images.md`：截图 01/17/20 明确通过，截图 07 为“通过（本轮修正确认；附 1 条残留问题请下轮处理）”，用户同时明确该残留不影响本轮签署。保留完整限定语和原始意见，在接收记录中将两轮有效结果合并为 **60/60 结构样本通过、30/30 截图通过、待重查 0 项**。不是把上一轮不通过改写成通过；首次结论仍在每条 `initial_conclusion` 和归档中。

截图 07 的 016 段 `PEDM` 经原图确认应为 `PFDM(PFD管理程序)`，已按用户给出的原文修正并同步 SQLite 辅助库。纠错账本当前为 140 个目标，其中 134 条纠错、1 条原报告误报，7 条模糊/遮挡行继续隔离。其余已通过内容、原始 OCR、提交的两份复核单、原图、P3 原生手册 generation 均未改写。用户提交文件仍保留“AI辅助复核（待人工签名）”，接收记录以用户明确完成复核的消息作为确认依据，没有代填姓名或签名。

M2 按计划的资料定位、抽样保真与分支缺口定义完成。截图通过限于可见区域和已接受的隔离处理，不表示遮挡文字被恢复；原手册 6 处疑点继续保留，也不批准全部 107 条候选命令在现场执行。P6 的业务准确率、完整性、模型比较与 P7 的隔离部署仍需分别验收。

`human_review_v3.json` 同时绑定首轮与修正复核单、纠错账本和当前文本 SHA-256；`verify-p2` 已返回 `m2_human_acceptance_pass=true`。先前状态归档于 `evidence/p2/archive/followup_v3_submitted/`。同步脚本支持 `--followup`，重复同步已接收的修正结果不会退回首轮待审状态。

```bash
uv run upf-agent repair-ocr
uv run python scripts/sync_p2_review.py --user-confirmed --followup
uv run upf-agent verify-p2
```

本轮全工程 **209 项测试通过（17.59 秒）**，Ruff、70 个文件格式检查和 81 个包的依赖检查通过。回归记录见 `evidence/p2/followup_tests.log`。复核解析测试确认限定范围的通过意见及残留说明可完整保留，并拒绝重复/缺失截图、结论与勾选冲突、模糊结论或缺来源定位。
