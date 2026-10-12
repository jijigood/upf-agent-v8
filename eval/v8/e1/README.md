# E1 文件案例与正式评测入口

更新：2026-10-11。当前实际材料为 **24 个旧 dev＋12 个 validation 候选＋24 个 heldout 候选，共60份**；独立新 Gold 0、实际双评记录 0。新案例缺36份独立参考，全部60份当前 hash 的真实双评批准均未收到。`dataset.json` 的状态为 draft，正式 E1 未启动；heldout 尚未发送给模型。

## 已有材料与边界

| 目录 | 实际内容 | 使用限制 |
| --- | --- | --- |
| `development/` | 24 个既有开发案例的原始任务和可见数据副本 | 已参与开发，不能改名为 validation／heldout |
| `validation/` | E1-CAL-N001–012，实际请求过滤、回复过滤、ogstun 管理关闭观测 | 同来源／结构连接为一个组件；重复采集不能按独立来源计算，待审 |
| `heldout/` | E1-HO-N001–024：网关地址缺失、回复黑洞路由、回复策略禁止各6份，以及低MTU正常边界控制6份 | 四个来源／结构组件；只采集并冻结输入，未调用模型 |
| `gold/development/` | 24 个既有未审开发参考 | 从旧结果复制，未转成独立专家 Gold |
| `gold/provenance/` | 实际来源／注入真值和原始 hash | 组织者材料，不能输入模型；注入真值不等于处置方案 Gold |
| `reviews/` | 空接收数组、空白双评登记表 | 表格不代表实际评审；需两名真实独立评审的原件 |
| `schemas/` | 任务、案例、Gold、GoldReview、OutputReview Schema | 与当前 Pydantic 实现对应 |

原3份 validation 保留。本轮另有34次真实采集尝试，其中33次符合各自预登记的内核状态与探针效果；1次“低MTU会导致大探针失败”的假设未成立，原始记录保留，未注册为故障案例。随后先登记正常边界控制协议，再重新采集6份低MTU但双探针正常的材料。新注册9份 validation 和24份 heldout；第一批27份完整采集复制到第二批时逐文件验 hash，不重复计作新试验。

使用同一 Open5GS 2.7.6／UERANSIM 3.2.7 镜像与核心 loopback 布局，heldout 更新了用户面网段和隔离桥地址，不能声称新拓扑泛化。全部60份形成6个来源／结构组件，大小为24、12及四组6，仍有同平台相关性。原始日志、接口、路由、探针和抓包在各候选 `visible/data/raw/snapshot.json`；注入控制命令及真值在模型不可见的 provenance 和采集包 `private/` 中。恢复回执来自采集工具清理及重新建立 UE 会话，不是 Agent 修复或 MTTR。

归一化 002 仅投影实际原文日志片段、接口 JSON 和探针返回码／输出。001 版本保留；`synthetic=false` 表示来源是真实受控运行，`corroborated=false` 表示投影尚未获得专家核验，不能据此宣称生产故障或已批准 Gold。

## 加入新案例与审核

1. 按 `schemas/case-manifest.schema.json` 在对应 split 下建立 `case.json`，登记到 `dataset.json.cases`。任务、原始和归一化观测放在 `visible/`；观测必须位于 `visible/data/`，任务与观测的 synthetic、对象、版本、时间和权限保持一致。
2. 按真实来源／结构登记 `source_group`、`structure_family`。同来源或同结构连接的案例整体放在一个 split；同一物理输入及历史 E7／开发来源不可重命名进入正式 split。加载器不调用固定 SPECS 生成测试数据。
3. 从注入真值、正常观测、适用版本手册和实际技术事实独立制定 Gold，记录必须步骤、依赖、可接受替代分支、禁用动作和停止条件；保存在 `gold/`，填写 `reference_file`。不要从当前 Contract 自动生成并批准答案。
4. 两名真实独立评审分别提交匹配 Gold canonical SHA 的 GoldReview，并把实际原件放在 `reviews/` 下。`review_source` 必须指向物理文件；身份和 hash 都核验。分歧需要保留处理过程、修订参考，并重新按新 hash 双评。设置 `reviewed=true` 或填两个名字不能绕过审核。
5. 60 例门槛为 **24 dev／12 validation／24 heldout**；完整 150 例为 **60／30／60**。当前已达到最小输入规模，36份新案例独立 Gold 和60份当前 hash 双评批准仍缺。`reviews/empty-gold-review-organizer-only-002.csv` 为120行空白表；表格不能当作实际评审。评审专业能力与真实独立性仍需组织者核实，代码不能证明这一人工事实。

正式入口支持规定归一化格式的实验、手册日志、benchmark 或新合成文件案例；尚未导入外部 benchmark，也不含自动转换任意厂商原始日志的适配器。

## 运行顺序

在仓库根目录执行。初始化已完成，不要对现有目录重复 init。以下冻结／运行命令须等待真实资料齐备；当前 audit 会报告 `data_ready=false`。

```bash
.venv-v8/bin/python scripts/v8_e1_formal.py audit \
  --dataset eval/v8/e1 --scale 60 \
  --output runtime/v8-next/e1-independent-20261010/readiness-next

.venv-v8/bin/python scripts/v8_e1_formal.py freeze \
  --dataset eval/v8/e1 --stage validation --scale 60 \
  --deployment /absolute/path/to/actual-deployment.json \
  --output runtime/v8-next/e1-validation-freeze-new

.venv-v8/bin/python scripts/v8_e1_formal.py run \
  --frozen-input runtime/v8-next/e1-validation-freeze-new \
  --output runtime/v8-next/e1-validation-run-new

.venv-v8/bin/python scripts/v8_e1_formal.py finalize \
  --frozen-input runtime/v8-next/e1-validation-freeze-new \
  --run-result runtime/v8-next/e1-validation-run-new \
  --output-reviews /absolute/path/to/actual-output-reviews.json \
  --review-root /absolute/path/to/actual-review-receipts \
  --output runtime/v8-next/e1-validation-final-new

.venv-v8/bin/python scripts/v8_e1_formal.py freeze \
  --dataset eval/v8/e1 --stage heldout --scale 60 \
  --validation-result runtime/v8-next/e1-validation-final-new \
  --deployment /absolute/path/to/actual-deployment.json \
  --output runtime/v8-next/e1-heldout-freeze-new
```

实际 deployment 回执须包含与 `config/models.yaml` 一致的 `served_name`、`endpoint`、真实 `server_command` 和完整 `model_files` 相对路径→SHA 映射（权重、tokenizer、配置）。冻结时核验物理权重并 GET 实际模型身份。本机已生成[实际部署回执](../../../runtime/v8-next/e1-experiments-20261011/actual-deployment-001.json)，核验23份权重／tokenizer／配置文件及实际进程身份。GET `/models` 的易变创建时间／permission ID 不作为模型身份；模型名称、路径、能力和权限仍严格比对。

validation 先执行再完成原文双人语义复核；仅运行完成不能开启 heldout。若校准中改了代码、prompt、输入、Gold 或模型，旧 validation 结果不能用于新版本，须另版冻结并复测。heldout 的 run／finalize 用同样命令顺序和全新输出目录。项目级按物理输入 hash 记录消费，重新命名冻结目录也不能重复使用同一 heldout。

四方法固定为 DirectLLM、P5、v8-no-graph、v8-full；共同 8／8／3／180 预算，只读 MemoryGraph／CPU 检索，按预登记顺序运行。保留原文、trace、binding、Validator、成本及逐样本 CSV，失败留在既定分母。主比较 P5→v8-full；次比较另外两方法→v8-full；按来源／结构组件做配对 bootstrap，零收益和负收益正常保留。

配对成本覆盖全部冻结案例（含失败和不可解案例），分别登记工具／模型尝试、输入／输出 Token 和耗时。异常时无法测得的成本标为 unknown 并保留既定分母，成本不全时不给平均差值；已测成本汇总不能解释为全部成本。共享模型服务下的耗时仅作描述，不据此自动作成本优势声明。

run 的参考匹配只能形成机器参考统计，`formal_vpr=null`。`finalize` 必须收到每份已解析原文的真实双评；分歧需第三位仲裁原件。最终 VPR 同时要求参考／约束通过与语义有效。输出 `empty-output-review-organizer-only.csv` 含方法身份，是组织者登记表；盲评材料需由组织者独立准备，不能把该表直接称作盲评包。

当前方法仍使用已有 IR 与共同 workflow head。结果适用范围限于该实现，不直接证明无模板自由规划优势或真实网络修复／MTTR。

## 无 Gold 的工程校准

`scripts/v8_e1_calibration.py` 提供单独的 validation 工程入口。它只加载12份 validation 正常观测，在首次生成前冻结可见输入、代码及真实模型回执；不载入私有注入真值，不给新案例伪造参考。本轮已完成12例×四方法＝48份实际输出，72次模型调用；原文、trace、binding、Validator及实际成本保存于 `runtime/v8-next/e1-experiments-20261011/validation-engineering-002/`。参考匹配和 VPR 关闭，真实语义评审0；该入口不能转换为正式 E1 成绩，也不会消费 heldout。

正式推进仍按上面的 audit→validation freeze/run/finalize→heldout 顺序执行，先完成独立 Gold 和真实双评。专家编制材料在 `runtime/v8-next/e1-experiments-20261011/expert-reference-materials-001/`；新增资料和未通过试验均已保留。

当前核验：[输入来源复核](../../../runtime/v8-next/e1-experiments-20261011/source-audit-001/summary.json)、[就绪核验](../../../runtime/v8-next/e1-experiments-20261011/readiness-001/summary.json)、[正式冻结拒绝回执](../../../runtime/v8-next/e1-experiments-20261011/formal-gate-001.json)、[60份案例索引](../../../runtime/v8-next/e1-experiments-20261011/source-audit-001/case-inventory.csv)。上轮27份材料验收与477文件冻结保留在 `runtime/v8-next/e1-independent-20261010/`，代表当时版本。
