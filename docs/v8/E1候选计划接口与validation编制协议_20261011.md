# E1 候选计划接口与 validation 编制协议

日期：2026-10-11。范围：推进12份现有 validation 的来源、知识和参考编制准备，以及既有开发案例上的共同计划接口试跑。本轮不增加题量，不运行正式 validation 或 heldout，不把自动草稿登记为批准 Gold。

## validation 编制入口

[编制包](../../runtime/v8-next/e1-planning-progress-20261011-001/validation-authoring-002/)含12份正常输入副本、12份组织者参考编制草稿、对应私有注入／独立内核读取／前后探针回执，以及24行空白专家登记表。原始输入 hash 与原采集逐一匹配；请求过滤、回复过滤、接口关闭各4份的观测效果通过独立读回。初次导出遇到旧采集回执使用 `ogstun`、新回执使用 `links` 的格式差异，部分001包保留为失败前序，002按两种真实格式读取后完成，不补造缺失资料。

原始 UPF 日志有8个空窗口，RAN 日志12个窗口均为空；这些是实际采集结果，不能填成诊断日志，也不能从空窗口推断正常。12份 RAN 绑定都带有 `core_interface_inventory`，评审需核对其作为共享核心侧背景的用途，避免当成独立 RAN 接口观测。当前 UPF／RAN 可能共处实验核心侧命名空间，数据归属需要结合实际拓扑确认，不能凭字段重复就直接判为伪造。

专家按如下顺序工作：

1. 先看 `normal-inputs/<case_id>/` 的任务和正常资料，记录可推断事实、未知信息与只读调查方案；不参考模型答案。
2. 再对照 `organizer-only/<case_id>/` 的注入真值及独立读回，核对失败机制与正常观测的对应关系。注入真值仅证明实验条件，不直接批准调查或处置步骤。
3. 独立查证版本知识，审核草稿中每项检查是否必要、是否受权限允许、依赖关系、合理替代、停止条件及禁止操作。草稿的 `required`、依赖、可解性及自然语言参考保持空值，由实际专家填写。
4. 分别记录来源投影／对象归属确认、知识适用性判定和 Gold 判定；三者不互相替代。两名实际评审填独立记录，保存实际原件和专业能力说明；分歧保留、仲裁后按修订参考新 hash 重新审核。
5. 先定完整自然语言参考，再映射 `CaseGold`。若必要步骤超出现有动作表，记录表达缺口；不能删减 Gold 让系统通过。自动草稿不是 `CaseGold`，现有 `reference_file=null`、`corroborated=false` 和真实审核0的状态不变。

[导出程序](../../scripts/v8_e1_validation_packet.py)直接访问 `validation/`，不使用会加载整个60例内容的数据入口，因此没有读取 heldout 的输入或私有真值。所有正常材料与组织者材料分目录保存；编制包不会作为模型检索目录。

## 已固定的知识来源与待审事项

Open5GS `v2.7.6` 的 tag 指向 commit `d9d3abdd480be96fac3bc8a997e83446648763ca`。本轮保存[UPF配置原文](https://github.com/open5gs/open5gs/blob/d9d3abdd480be96fac3bc8a997e83446648763ca/configs/open5gs/upf.yaml.in)、[官方 quickstart](https://github.com/open5gs/open5gs/blob/d9d3abdd480be96fac3bc8a997e83446648763ca/docs/_docs/guide/01-quickstart.md)、构建文档和 LICENSE，每份有 commit、URL、SHA 与适用性待审标记。[本地来源索引](../../runtime/v8-next/e1-planning-progress-20261011-001/knowledge-sources/index.json)。

另已核实 UERANSIM `v3.2.7` 的固定 commit `1d1e154f869260b5e98f6905827b1bd9b8663afc`，保存 README、[官方 UE 配置示例](https://github.com/aligungr/UERANSIM/blob/1d1e154f869260b5e98f6905827b1bd9b8663afc/config/open5gs-ue.yaml)及 LICENSE。[补充来源索引](../../runtime/v8-next/e1-planning-progress-20261011-001/knowledge-supplement-002/index.json)。配置示例可供审核 TUN 与初始 PDU 会话的字段含义，不代表本实验实际配置或会话成功真值；适用性仍待专家确认。

这些资料可供核对用户面会话网段、网关、隧道接口及接入主机的规则；本地目标为核心侧网关的探针，不能直接套用“访问外网需要 NAT”的说明去认定缺 NAT。手册中的写命令也不能作为本任务执行权限。OUTPUT方向规则判断仍须结合 Linux 数据路径与本实验读回，由专家确认。本轮没有生成可信 K 绑定或把这些资料自动设为专家批准。

## 共同候选接口

[候选计划头](../../src/upf_agent/v8/bounded_plan_generator.py)通过 `run_method` 的可选 `plan_generator` 接入。原正式入口和既有开发入口仍使用默认共同方案头，历史固定流程、IR、动作表、Translator、完整 Validator 和参考匹配规则保留。

候选接口保留有限动作、对象与字段权限、产品版本及时间、已采信引用、配置检查 K、双侧映射 P、只读效果、身份依赖和8步上限。Schema 不再给出固定步骤槽位：模型选择动作子集、数量、顺序和额外依赖，仍须满足对象身份锚点；未选择的依赖、循环或重复ID由独立 Validator 检查。Schema 不编码 Gold 的必要步骤覆盖，生成后也不修复原文。

当前 validation 的实际材料和权限仍只允许 `CHECK_IDENTITY`、`READ_LOG`、`REQUEST_EVIDENCE`、`HUMAN_REVIEW`。48份保存输入上的 Schema 检查确认1–8步可选择，未确认 R 仍不可引用。因此此接口的开发成功只说明解除固定流程后的运行可行，不能证明完整领域诊断或规划收益。

候选第一版出现一个实际长空白、3072 token截断失败；另一个方法完成成功输出。为修复解码格式，中止该版本剩余任务，保留原文、实际请求、账本与[中止回执](../../runtime/v8-next/e1-planning-progress-20261011-001/development-preflight-001/abort-receipt.json)。第一版尚有一次未完成请求的响应／token用量未知，不能当作0成本，也不能并入完整新版本分母。

候选第二版将同一 JSON Schema 用实际 xgrammar 编译为紧凑 EBNF，通过本机 vLLM 的 `structured_outputs.grammar` 发出；转换时禁止任意空白并指定逗号／冒号分隔符。保存实际请求里的完整语法和输入 Schema SHA，模型文字不放入 Schema，没有后处理补写。既有请求方式仍为默认 JSON Schema；新的语法参数与 Schema 参数互斥，传输测试核对实际HTTP请求、trace及调用账本一致。服务未重启、模型未切换。[本机解码器版本与源码回执](../../runtime/v8-next/e1-planning-progress-20261011-001/compact-decoder-receipt.json)，相关[官方接口说明](https://docs.vllm.ai/en/v0.31.0/features/structured_outputs/)。

## 开发试跑与领域接口缺口

推理前选定旧 dev `pilot-01`（完整N4）、`pilot-05`（知识目的未知）、`pilot-13`（手册操作），每例四方法，共12份。固定实际模型部署、代码、原始输入、共同预算8工具／8模型／3轮／180秒及预登记轮换顺序；模型输入不含 Gold。12/12完成并解析，11/12通过完整 Validator 与未审开发参考，P5手册案例重复ID失败保留；20次模型／52次工具，输入103,604、输出15,889 token。正式 VPR 保持 null。结果及逐份 trace 在[第二版开发批次](../../runtime/v8-next/e1-planning-progress-20261011-001/development-preflight-002/)，成本和局限见[推进验收](E1证据编制与候选计划接口推进验收_20261011.md)；不能用3个开发案例估计总体领先。

在正式 validation 前需由领域参考明确以下接口缺口，后续实现另版登记，不在当前试跑中冒充已有工具：

| 候选只读检查能力 | 应明确的参数、作用域与证据 | 现有缺口 |
| --- | --- | --- |
| Linux隧道接口检查 | 注册的接口名、管理状态、地址／MTU及所属命名空间；产品版本与数据时窗 | `CHECK_INTERFACE` 当前限定N3/N4/N6/N9，不能把ogstun改名为N3来替代检查 |
| 防火墙规则／计数读取 | 明确INPUT或OUTPUT链、接口、协议／方向、地址范围；只读规则来源与返回码 | 没有该动作和普通材料对应字段；私有注入规则不能直接作为模型已知证据 |
| 会话与探针对照 | UE身份／授权对象、源／目的、大小、方向、时间及返回码 | UPF/RAN对象范围不自动等于UE权限，UE探针不应冒充RAN局部状态 |
| 抓包与路径一致性核验 | 两侧实际可用的抓包、时间对齐、截断范围、端点映射和版本 | 单个核心侧抓包不证明独立双侧一致性，不能仅靠动作文字宣称完整核验 |

上述检查是参考编制的待审要求，不是自动批准的必要步骤列表。确认正常证据与任务目标后，才确定完整诊断、合理补证、人工复核及正常边界的独立分层和分母；全部预定失败和不支持案例仍保留。

## 后续门槛

当前已完成自动来源读回、资料导出、12份逐例工作说明、候选 Schema 和12份真实开发试跑／原文复算；领域知识适用性、独立参考、真实双评／仲裁及正式原文语义评价仍待完成。后续在 dev／validation 完成动作表达与权限修订、独立参考和审核，另版冻结并执行正式 validation，通过原文审核后才进入单次 heldout。固定流程工程指标、候选计划实验和外部基准分别报告。
