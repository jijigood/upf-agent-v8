# UPF-Agent-Graph v8：自然语言处置方案有效性与证据约束智能编排实验方案（V2.0）

> **版本**：2026-10-08，实验设计稿 V2.0（覆盖和取代先前的“实验补强与方案有效性评测计划”中的执行规划；旧稿仍可用于研究脉络追踪）。  
> **审计基线**：[`jijigood/upf-agent-graph`](https://github.com/jijigood/upf-agent-graph)，`main` 提交 [`421d8f2450af61ebcd4938cc5a7df5841f605e53`](https://github.com/jijigood/upf-agent-graph/commit/421d8f2450af61ebcd4938cc5a7df5841f605e53)。  
> **核心目的**：建立“**证据是否正确 → 方案是否正确 → 方案是否可行 → 完成任务是否有效 → 运行开销与安全性**”的完整评测链。  
> **当前能力边界**：当前为 LangGraph 驱动的**只读取证、有限轮次、证据约束的 UPF 运维 Agent 原型**；具有 K/R/P、图查询、增量更新和只读建议门控的代码。**不意味着**真实配置下发、自动修复、跨域实网自治或 MTTR 降低已经实现。  
> **证据标签**：【代码/配置证据】可从指定仓库源码确认；【仓库脚本记录】存在验收脚本或数字引用，但本报告未独立取得/复算私有运行产物；【外部研究】论文或开源项目报告；【拟实施】新设计、实验数量和目标；【无法确认】缺原始实验证据或独立标注。

---

## 0. 执行摘要：这次新增的究竟是什么？

当前 v8 已比较充分地测试“某项机制在合成规则场景中是否能安全执行”，但还不足以证明其最终自然语言处置建议**比 P5 Agent 更正确、更完整、更可操作，更有助于真实故障调查**。

**新的主线不是堆功能，而是补一条独立可证伪的 Plan Evaluation 链：**

```text
自然语言运维任务 + 可追溯的手册/日志/拓扑
                    ↓
        B0 / P5 / v8 等公平对照
                    ↓
          原始自然语言输出（保存）
                    ↓
      PlanIR：规范化动作、依赖、证据、目标
                    ↓
      Deterministic Plan Validator
       ├─ 格式和参数 Schema
       ├─ 必要步骤/必要前置条件
       ├─ K/R/P 适用性与证据来源
       ├─ 权限/风险/错误参数/禁止动作
       └─ 计划目标与退出条件
                    ↓
      盲化专家评价 + 必要时 LLM Judge
                    ↓
     VPR、步骤覆盖、证据支持、安全性、成本
                    ↓
      （后期）Open5GS 隔离网状态验证
```

**四类主要新增实验**：

1. **E1：PlanIR + 外部符号验证器**，借鉴 TelcoAgent-Bench、TeleCom-Bench、VAL、TravelPlanner；研究自然语言处置方案到底对不对。
2. **E2：受约束图检索 + Personalized PageRank (PPR)**，借鉴 HippoRAG/ToG；研究版本/来源等约束下的有效召回与图开销，而不以“图节点更多”替代正确性。
3. **E4：Dependency-local Recompute + Early Cutoff 完整性审计**，参考 Salsa red-green；研究字段/状态/门控的等价性、安全回退与实际收益。
4. **E7：Open5GS/UERANSIM + 受控故障注入**，参考 5G Agent Benchmarking Framework 与 RCAEval；研究建议能否帮助定位真实注入目标，后期在隔离环境中验证目标状态。

另设 **E0（基线复现）、E3（状态驱动补证）、E5（门控安全与可用性）、E6（鲁棒性/迁移）、E8（外部基准）**。E1/E4 优先，E2 其次，E7 最后；E8 不能代替本领域真值。

> **禁止性结论**：格式正确 ≠ 方案正确；文本与专家相似 ≠ 可执行；规则校验通过 ≠ 网络目标达成；故障告警共现 ≠ 因果根因；PPR 相关度高 ≠ 物理关系可信；合成“零错误” ≠ 真实网络零风险。

---

## 1. 当前仓库：已有实现、证据等级、待补缺口

### 1.1 已有能力与不应重复开发的模块

| 子系统 | 当前源码 | 可确认能力 | 真实性级别 | 这次如何利用 |
|---|---|---|---|---|
| v8 编排 | [`v8/engine.py`](https://github.com/jijigood/upf-agent-graph/blob/main/src/upf_agent/v8/engine.py) | LangGraph `compile→collect→graph→evaluate→supplement→report`；checkpoint、ledger、预算、resume | 【代码/配置证据】 | 保留旧引擎和 trace；新增计时、方案输出，不重做框架 |
| Evidence Contract | `v8/models.py`、`compiler.py` | 任务模板、K/R/P/C/A Requirement、按只读工具能力编译 QueryPlan | 【代码/配置证据】 | 作为 PlanIR 的证据前提输入 |
| 证据来源 | `v8/adapters.py`、`store.py` | Binding、source SHA、locator、版本/时间窗、receipt、revision、synthetic 标记 | 【代码/配置证据】 | 直接形成 action-to-evidence 引用 |
| K/R/P | `v8/evaluator.py` | 错版、时区、缺字段、双边界不一致、冲突/未知判断 | 【代码/配置证据】 | 作为可重复的 Plan Validator 规则源 |
| 图存储 | `v8/graph.py`、`builders.py`、`source_graph.py` | Memory/Neo4j、节点适用性过滤、关系白名单、最多 2 跳等 | 【代码/配置证据】 | E2 用现有图/相同种子做检索算法对照 |
| 局部重算 | `v8/dependency.py` | NetworkX 读者索引、失效传播、早停基础、异常时 full fallback | 【代码/配置证据】 | E4 测完整读集与早停，不声称“新引入 Early Cutoff” |
| 建议门控 | `v8/actions.py` | 只读动作、影响范围、`suggest_allowed/re_evidence/human_review/blocked` | 【代码/配置证据】 | E1/E5 增加**多步骤 Plan** 而不废弃单动作 Gate |
| 合成方案消融 | `v8/scenarios.py` | `B0/B1/B2/B3/B4/Ours`、合成 oracle、freeze | 【代码/配置证据】 | 保留旧数值作为历史，修正对照口径 |
| 图小实验 | `v8/graph_experiment.py` | 四问、同一 P3 seed、FixedGraph/ContractGraph、Neo4j 内存对照 | 【代码/配置证据】 | 扩充评测集、做同成本计时、PPR/合法补证 |
| 局部规模实验 | `v8/evaluation.py` | `S/M/L/XL × {1,5,10,50} fields × 20 seeds × 50 batches` 设计 | 【代码/配置证据】 | 同时报告状态、动作、实际时延、内存及 fallback |

### 1.2 不应当作已独立复算结果的数字

[`scripts/v8_delivery_report.py`](https://github.com/jijigood/upf-agent-graph/blob/main/scripts/v8_delivery_report.py) 读取/检查的材料包括 `371 passed`、局部/全量 `16,000/16,000`、11 个 heldout × 6 方法、只读门控 0 次错误放行与 10/10 合法建议等。**这些是【仓库脚本记录】；本次审查的公开 GitHub 提交排除了原始运行 artifacts、部分原件和完整实验 CSV，所以不能直接写成独立复验成绩。**

已有图实验的报告脚本还记录 **4 个图场景中，契约式检索对必需合成控制事实的覆盖只有 2/4**：某些 P3 seed 缺少可确认版本，被拒绝后导致下游真值不可达。该限制必须保留为待解决问题，而不能因不适用接受数为零就宣布图检索全指标提升。

### 1.3 本次真正新增的工程缺口

1. 没有**稳定、独立、可核验的最终 PlanIR**；`ActionDecision` 是单个建议准入，不是专家定义的多步处置方案。
2. 没有方案层的必要步骤依赖 DAG、前置条件推进、禁止动作集合、期望检查结果与正确停止条件。
3. `compile_graph_query()` 仍较偏 task/seed，未完整以**逐条 Requirement** 编译图查询；图扩展回写 K 时 purpose 证明链不足。
4. 缺大样本图证据相关/适用性 Gold；现有四问不足以支持通用召回结论。
5. 局部重算虽有 early cutoff，但需要“读集起始遗漏、状态不变数值变化、批次/as_of 变化”系统测试。
6. B0/B2/B3/B4 部分工具开销属于**声明访问数**，B1/Ours 使用后端/ledger 回执数；未做到同口径。
7. 没有独立注入故障后的业务/设备最终状态验证；当前建议不能声称已修复故障。
8. `scripts/v8_prepare.py` 等包含同机绝对路径/共享模型环境假设，开放复现需提供最小无私有资料模式。

---

## 2. 研究问题、假设与评价层级

| RQ | 要解决的问题 | 必须能被证伪的假设（尚未证实） | 主实验 |
|---|---|---|---|
| RQ1 | v8 能否生成比 P5 更正确、完整、适用的多步骤方案？ | VPR↑、必要步骤/依赖覆盖↑、错误操作↓ | E1、E5 |
| RQ2 | 图检索能够在严格适用性过滤下保持足够的有效证据召回吗？ | Valid Evidence Recall@K↑或在同风险下得到更佳 Precision/Recall 平衡 | E2 |
| RQ3 | Typed Gap 真的减少无关取证并提高可补缺口的关闭率吗？ | 同预算下 Gap Closure↑、无效查询↓ | E3 |
| RQ4 | Dependency-local 和 Early Cutoff 在复杂变更下是否与全量完全等价且省资源？ | 状态和动作判断等价；稀疏变更净耗时降低 | E4 |
| RQ5 | Action Gate 在消除不安全建议时是否仍能保留可用建议？ | URR↓且 VAAR 不显著恶化，正确转人工率高 | E5 |
| RQ6 | 换来源、结构、语言表达、随机数后能否稳定工作？ | 方差可控、错误放行不因 OOD 激增 | E6 |
| RQ7 | 面对隔离 5GC 注入故障，方案能否正确定位/满足可观测网络目标？ | Root Cause Top-K、定位时延/已审批实验目标优于基线 | E7 |
| RQ8 | 系统在外部 AIOps/3GPP/微服务基准是否呈现合理迁移？ | 分域报告，不强求跨域数值胜出 | E8 |

**评价分四层，必须分开统计：**

| 层级 | 验证对象 | 可由当前仓库独立评估吗？ |
|---|---|---|
| L1 Schema | JSON/Pydantic 格式、命令模板、参数类型 | 新增评测后可以 |
| L2 Plan validity | 必要步骤、顺序、权限、证据、动作前置条件、安全风险 | 新增 PlanIR/Validator + 标注后可以 |
| L3 Diagnostic usefulness | 正确故障类别/目标网元、可操作建议、可解任务完成、正确拒答 | 需要经复核 Gold 和任务输出 |
| L4 Functional outcome | 注入后网络状态是否恢复/达到目标、是否引入副作用 | 仅隔离网络 + 外部执行/观测成立；当前无证据 |

---

## 3. 外部论文、开源项目及其正确复用边界

以下按“**真实论文/代码用途**”列出，防止一概当成可直接迁移的 UPF 数据集。参考链接见末尾书目，正式写作须标注论文状态、对应开源 tag/commit 和许可。

| 工作 | 已有研究贡献/数据类型 | 实际借用 | 不能做什么 | 优先级 |
|---|---|---|---|---|
| **TelcoAgent-Bench**（2026 预印本） | 蓝图样本、必要工具序列、MSC/EAP/SAS 与重复场景稳定性 | 必要步骤、无关动作惩罚、路径一致性；**Gold 顺序扩展成依赖 DAG** | 英/阿模拟对话不可直接当中文 UPF 真实故障标签 | P0 |
| **TeleCom-Bench**（2026 预印本） | Intent/RCA/**Solution Generation** 分任务，开放答案评审；仅部分数据公开 | 方案生成专家 rubric、评审一致性校准 | 不能声称掌握或复现完整 22,678 题 | P0 |
| **LLM-Modulo / VAL**（ICML 2024 观点论文 + VAL 工具） | LLM proposal 与外部形式化校验分离；PDDL 前置/效果验证 | PlanIR 验证、非法步骤诊断；只读动作先做轻量 Python 校验器 | 不因形式化“通过”宣称真实网络可执行或无风险 | P0 |
| **TravelPlanner/PlanBench** | 多条件计划和动作前置条件的任务验证 | 多有效路径、状态推进与 hard constraint | 不用旅行/积木数据计算 UPF 准确率 | P0（方法） |
| **Outlines / XGrammar** | 结构化输出和 Grammar-constrained decoding | 结构成功率消融；固定同一模型/温度 | JSON 合法 ≠ 技术语义正确；不保证“零格式失败” | P1 |
| **HippoRAG**（NeurIPS 2024） | 实体关联/PPR 图检索 | Constrained PPR / 与定跳 BFS 消融 | 不保证毫秒级、可靠物理连接或更高召回 | P1 |
| **Think-on-Graph**（ICLR 2024） | LLM 引导的关系筛选/Beam Search | 有预算时做 beam 检索可选对照 | 不能声称原作者框架专门为时态网络图设计 | P2 |
| **Salsa red-green** | 增量计算、读取追踪、revision 与 early cutoff | 用于依赖完整性假设与消融对照 | 当前代码已经有 early cutoff 基础；不能说“首次引入” | P0 |
| **OpsEval**（arXiv:2310.07637） | IT 运维知识、多选与 QA；公开部分题，含通信子集 | 域外/知识诊断能力压力测试 | **不是**带 N4 故障注入真值的工业 RCA 数据集 | P2 |
| **Telco-RAG**（arXiv:2404.15939） | 3GPP 标准文档检索框架 | 标准分块/查询改写 RAG 对照 | 不直接当生成处置方案 Gold，不导入未授权标准文本 | P2 |
| **RCAEval**（ASE 2024/WWW 2025 关联研究） | 微服务遥测 RCA，提供注入故障案例及服务/故障标签 | Top-1/Top-K 定位、注入事件时间、遥测评测方法 | 不能假定每例都有已标注真实**因果边**，也不能作 UPF 现场准确率 | P2 |
| **5G Agent Benchmarking Framework** | Open5GS + UERANSIM、K8s、Ansible 注入、Loki/Prometheus/MCP/trace | 直接参考隔离故障注入生命周期和评测 runner | 不因平台有 Kubernetes exec 就允许本项目 Agent 写配置 | P2/后期 |
| **NetConfEval / NetConfBench / NetArena** | 网络配置/意图的功能测试、正确/安全/时延分层 | 定义最终目标状态与黑盒功能测试 | NetConfBench 是 Internet-Draft，不能称已发布 RFC | P2 |

**版本与来源校正**：OpsEval 论文为 [arXiv:2310.07637](https://arxiv.org/abs/2310.07637)，公开仓库是 `NetManAIOps/OpsEval-Datasets`；Telco-RAG 为 [arXiv:2404.15939](https://arxiv.org/abs/2404.15939)，代码是 `netop-team/Telco-RAG`；ToG 代码可从 `DataArcTech/ToG` 获取；RCAEval 官方是 `phamquiluan/RCAEval`。不要继续使用此前提供的错误仓库名或 arXiv 编号。

---

## 4. E0：基线复现、冻结和公平性（所有后续实验的前置门槛）

### 4.1 目标

先解决“相同数据、模型、工具权限、预算、时间窗的公平对照”，再运行新算法。每个实验必须保存环境和产物，否则结果不能进入论文主结果。

### 4.2 必须冻结的条件

- 代码：commit SHA、`uv.lock`、`requirements/v8-graphrag.in`、是否启用新模块的 feature flags；
- 数据：手册/日志/拓扑/结构化 oracle 的 SHA、来源授权、synthetic/real 标签、时间窗、版本；
- 模型：generation/embedding/reranker 的模型 ID、权重 hash、量化、推理端点、sampling 参数、tokenizer；
- 工具：工具清单、Schema、timeout、返回格式、权限、错误处理策略；
- 资源：同卡/CPU/GPU、显存、线程、缓存 cold/warm、Neo4j 索引及容量；
- 运行：每案例 `run_id`、随机种子、尝试次数、预算、是否中断/恢复、排除条件；
- 评价：冻结 Gold 和 evaluator 版本，禁止从 heldout 答案生成提示或调阈值。

### 4.3 消融公平性必须改正

旧 `scenarios.py` 中 B0/B2/B3/B4 的工具计数为“声明的来源访问次数”，而 B1/Ours 用真实 `ledger/backend`；不允许直接作为工具节省量比较。建立统一的 `MetricCollector`：

```text
LLM requests (successful/failed)
Tool invocations (attempted/committed/reused/error)
Retriever calls (exact/BM25/dense/reranker/graph separately)
Source reads (cache hit/miss)
Tokens (input/output; if unavailable明确为NA)
Wall-time (including cold/warm and preprocessing)
Peak RAM/VRAM (optional,由监测器获得)
```

改造 B4：不要仅将 MemoryGraphStore 的节点/边列表作为 prompt，而要**执行**与 Ours 对等的 Graph Retrieval；原来的 B4 更名 `GraphContextOnly` 作为补充消融。相同 P3 seed + 不同过滤策略的检索算法比较应与“原生 Neo4j HybridCypherRetriever”分开，因为其索引底座不同。

### 4.4 E0 验收条件

- [ ] 基线 P5、当前 v8 原测试在隔离环境可复跑，并保留原日志；失败/skip 逐项列出。
- [ ] 所有实验方法都输出统一 `metrics.json` 和逐次 `traces.jsonl`。
- [ ] 原 P6 heldout 若已消费，不重标为新盲测；另建来源/结构分组不同的新 heldout。
- [ ] 提供可公开运行的 synthetic-only 小环境（无需企业原件、GPU 或真实 Neo4j 也能跑确定性测试）。
- [ ] 实际测得的计数、估算的计数、缺失计数三者不混合。

---

## 5. E1 主实验：结构化自然语言处置方案正确性

### 5.1 设计目标

**让最终中文处置方案成为独立、可机器校验、可由专家复核的研究对象。** 不再只校验 K/R/P 和单个 `ActionDecision`。

### 5.2 PlanIR 数据模型（拟新增）

建议新建 `src/upf_agent/v8/plan_ir.py`，逻辑字段如下；只是**设计 Schema 示例**，不是当前源码已有接口。

```python
class PlanStep(BaseModel):
    step_id: str
    action_type: str                     # 只读白名单 / 建议标签
    target_object: str
    interface: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)
    depends_on: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    preconditions: list[Predicate] = Field(default_factory=list)
    expected_observations: list[Predicate] = Field(default_factory=list)
    claimed_effects: list[Predicate] = Field(default_factory=list)
    effect_kind: Literal["epistemic", "network"] = "epistemic"
    permission_kind: Literal["read", "suggest", "write"] = "read"
    risk: Literal["low", "medium", "high", "unknown"] = "unknown"
    on_failure: Literal["stop", "ask_human", "re_evidence"] = "re_evidence"

class PlanIR(BaseModel):
    task_id: str
    plan_id: str
    scope_fingerprint: str
    source_type: Literal["generated", "expert_gold", "parsed_from_text"]
    diagnosis: list[DiagnosticHypothesis] = Field(default_factory=list)
    steps: list[PlanStep]
    exit_criteria: list[Predicate]
    uncertainty_notes: list[str] = Field(default_factory=list)
    source_evidence_ids: list[str] = Field(default_factory=list)
    non_executable: bool = True
```

这里 **`effect_kind` 必须区分**：

- `epistemic`：只读检查得到新知识/观测（例如检查 PFCP 状态）；不是网络配置被改变；
- `network`：对真实系统状态产生变化（当前 v8 不允许执行，只能作为未来实验计划或建议）；
- `on_failure`：证据不足/执行失败时必须停止或补证，禁止自由编造执行成功。

### 5.3 样例：N4/PFCP 只读诊断计划

```yaml
case_id: n4-001
plan_id: baseline-example
non_executable: true
steps:
  - step_id: s1
    action_type: VERIFY_TARGET_IDENTITY
    target_object: UPF-A
    permission_kind: read
    evidence_refs: [ev_device_mapping]
    expected_observations: [device_identity]
  - step_id: s2
    action_type: READ_PFCP_EVENTS
    target_object: UPF-A
    interface: N4
    depends_on: [s1]
    permission_kind: read
    expected_observations: [pfcp_event_window]
  - step_id: s3
    action_type: CHECK_N4_CONFIGURATION
    target_object: UPF-A
    interface: N4
    depends_on: [s1]
    evidence_refs: [ev_manual_pfcp_rule]
    permission_kind: read
    expected_observations: [n4_peer_config]
  - step_id: s4
    action_type: COMPARE_EVIDENCE
    target_object: UPF-A
    depends_on: [s2, s3]
    permission_kind: read
    expected_observations: [supported_or_missing_diagnosis]
exit_criteria: [report_with_evidence_or_request_more_data]
```

这只是合成示例，不是现网真实故障因果链，不包含可执行厂商命令。

### 5.4 方案评估不能单独依赖 LLM 解析

对各方法同时保存**原始自然语言文本**和可得的**原生结构化输出**：

- v8：先基于已有 ActionDecision 和 final report 产生 PlanIR，再生成自然语言；保证 PlanIR 是计算/证据驱动而非从结果反推 Gold。
- P5/B0：可由**固定、冻结、独立**的 PlanIR 转写器抽取动作/依赖，但抽取器可能有错误；必须报告转写成功率，并对样本做人工盲审；不能只评价转换成功的样本。
- 评审时人工专家始终能看原始回答，避免把转换器的语义遗漏错误地归咎于生成模型。
- Parser failure 单独记作 `parse_failed`；技术违规单独记作 `semantic_invalid`；如果系统无法产生可用方案，计入可解任务的失败分母。

### 5.5 Plan Validator（拟新增）

新建 `v8/plan_validator.py`：

```text
PlanIR
 ├─ 1) Schema / action whitelist / target scope
 ├─ 2) permissions and no-write invariant
 ├─ 3) required evidence bindings and K/R/P validity
 ├─ 4) action preconditions and dependency DAG
 ├─ 5) expected observation/effect type compatibility
 ├─ 6) prohibitions and critical command/version constraints
 └─ 7) stop/deferral rules and report traceability
       ↓
PlanValidationReport
  valid: bool
  critical_violations: []
  missing_mandatory_steps: []
  failed_preconditions: []
  unsupported_claims: []
  blocking_evidence_gaps: []
  adjudication_needed: bool
```

`VAL` 是成熟的 PDDL 规划验证工具（可在高级阶段选择导出 PDDL domain/problem/plan 测试），但第一版推荐纯 Python 确定性校验，以免仅为了几个 read-only 检查步骤引入复杂编译层。**验证正确性仅针对已建模前置条件**；遗漏的领域约束仍需要专家与测试补齐。

### 5.6 E1 对照矩阵（两条正交轴）

**轴 A：规划来源**（回答 v8 是否比原 Agent 好）：

| 方法 ID | 实际规划者 | 相同输入/预算 | 输出评价 |
|---|---|---|---|
| E1-A0 | Baseline direct LLM（仅提供等价手册上下文） | 是 | 原文 + 结构化转写 |
| E1-A1 | 当前 P5 Agent | 是 | 原文 + 结构化转写 |
| E1-A2 | v8 without graph（Contract/KRP/Gap/Gate） | 是 | PlanIR + 原文 |
| E1-A3 | v8 full（当前可用的图增强） | 是 | PlanIR + 原文 |

**轴 B：输出约束/校验**（回答 Validator 和 grammar 各自贡献，不改变规划者）：

| 方法 ID | 结构生成 | Validator | 测试目标 |
|---|---|---|---|
| E1-B0 | 普通 JSON/free-text | 无 | 解析失败、语义错误 |
| E1-B1 | Pydantic Schema 提示/校验 | 无 | 格式提升是否影响技术正确性 |
| E1-B2 | Outlines/XGrammar（若后端可用） | 无 | Grammar 强约束效果与延迟 |
| E1-B3 | 与 B2 相同生成 | Deterministic Validator | 技术/权限/前置条件违规拦截和保留率 |

**禁止**把 E1-B2 和 E1-B3 的改动同时归因于某一个新机制。格式正确率与技术有效率必须分别报。

### 5.7 E1 指标与严格口径

记 `S` 为有充分证据、**可解**的测试任务，`U` 为必要信息不可获得或越权的任务，`P_i` 为一次完整生成方案。Gold 中允许多个有效方案和依赖 DAG。

1. **Valid Plan Rate（VPR）**：`|{i∈S: P_i 通过全部硬性技术/权限/步骤约束，并满足任务目标}| / |S|`。可解任务无结果、解析失败或临界违规均进入分母并视为失败。
2. **Mandatory Step Recall（MSR）**：`匹配的必需步骤数量 / Gold 必需步骤总数`。**MSC-DAG** 另增加 `满足的必需先后关系数 / Gold 必需依赖边数`。两者并列报告，避免一个平均值掩盖遗漏。
3. **Hard Constraint Violation Rate（HCVR）**：`发生至少一项硬约束违规的生成方案数 / 全部生成或应生成方案的任务数`，另计 `critical_violations_per_plan`。
4. **Evidence-Grounded Recommendation Rate（EGRR）**：`每个关键建议均有经 version/time/object/permission/source 验证的证据支撑的方案数 / 提出至少一项关键建议的方案数`；无建议任务不并入这个分母，而另由 VPR/CDR 评价。
5. **Correct Deferral Rate（CDR）**：`U 中正确要求补证/转人工/停止且未错误给出确定处置的任务数 / |U|`。
6. **Diagnostic Top-1/Top-K**：**只有具有独立根因真值**的案例才计算；无真值仅报受支持的候选诊断比例。
7. **Plan Technical Validity Score（辅助）**：专家对技术正确、适用、完整、可操作、风险/退出机制的事先定义维度评分，不替代 VPR。

注意 `VPR` 和 `CDR` 是两个不同子集的指标，不要把正确拒答加到“成功诊断”的分子中提高表面结果。

### 5.8 E1 人工评审协议

- 至少两名具备相关网络技术知识的评审独立标注案例；争议由第三方复核/仲裁（实际人数应按招募情况如实报告）。
- 给评审者**冻结的事实材料、产品版本、可见证据、隐去方法名称的原始方案**；不要给出需要被评的方法身份。
- 先盲标 `root_cause_known?`、步骤覆盖、fatal violations 和可操作性，再看 Validator 结果；否则专家可能被机器结论引导。
- 报告类别型一致性 Cohen’s κ / Krippendorff’s α（按实际标注形式选择），连续评分报告相关/一致性并保留冲突案例；不能只说“专家高度一致”。
- LLM Judge 只用于大样本预评分；必须先在人工子集上校准错误率与偏差。

### 5.9 E1 成果图/表

- 表：P5 vs v8 的 VPR、MSR、DAG 依赖边满足率、EGRR、CDR、HCVR（附 N 和 CI）。
- 图：方案正确性 vs 资源成本散点/Pareto 图；按 N4/N3/配置/多对象/缺证分组箱线图。
- 案例：同一 N4 故障，旧 Agent/新 Agent 的方案步骤、引用证据、错误前置条件、专家判定。

---

## 6. Gold Bench：数据、标签与隔离策略（计划规模，不是现成样本）

### 6.1 数据来源分层

| 级别 | 来源 | 可以验证什么 | 不能宣称什么 |
|---|---|---|---|
| D1 | 仓库现有 synthetic fixtures / mutation | K/R/P 逻辑、门控、计划约束、依赖更新 | 真实网络根因准确率 |
| D2 | 脱敏手册 + 真实历史日志/拓扑 + 独立专家复核 | 真实知识适用性、证据支撑、部分诊断候选/操作有效性 | 无注入真值时的确证根因 |
| D3 | 独立实验者在 Open5GS/UERANSIM 注入已知故障，保存网络状态和恢复日志 | root cause、时间、定位和受控目标达成 | 运营商现网闭环自治能力 |
| D4 | OpsEval/Telco-RAG/RCAEval 外部域数据 | 跨领域迁移、知识检索、微服务 RCA | 与 D3 混成单一“UPF 准确率” |

### 6.2 推荐任务规模（**设计目标**）

**试点**：20–30 个开发样本、10 个评审样本，验证 Schema 和统计口径；不在试点上宣布性能优越。

**完整第一轮**：建议 150 个案例，来源/结构分组的 `dev=60 / validation=30 / heldout=60`；如果专家标注资源不足，先执行 60 个有质量的案例，不要用重复改写凑 150。

| 样本类型 | 目标数量 | 标签侧重点 |
|---|---:|---|
| N4/PFCP 关联/心跳/配置问题 | 30 | PFCP 运行、N4 对端、版本与处置步骤 |
| N3/GTP-U 数据面问题 | 25 | 接口、丢包/流量、定位与缺证 |
| UPF 基础状态/配置/命令知识 | 25 | 产品版本、只读检查建议、禁止编造命令 |
| 错版本/缺时区/越权/证据冲突 | 30 | CDR、EGRR、ActionGate |
| 多对象/双侧边界/路径变体 | 25 | P 配对、跨边界依赖、多个可行步骤 |
| 不可支持请求/对抗指令/图噪声 | 15 | 拒答和鲁棒性 |
| **合计** | **150** | 规模仅供实验规划 |

真正含独立根因真值的案例应另标 `causal_ground_truth_level=experimental_injection/expert_verified/unknown`，**不是所有 150 个都默认可计算 RCA accuracy**。

### 6.3 Gold 定义：多方案、依赖 DAG、不可忽略的禁止条件

建议每个 `case.yaml` 包含：

```yaml
case_id: N4-001
split: dev
source_group: isolated-fixture-family-A
structure_group: two-node-n4
source_level: D1
synthetic: true
root_cause_ground_truth_level: unknown
status: solvable                # solvable/unsolvable/needs_more_evidence
intent: n4_troubleshooting
scope:
  product: UPF
  version: "5.0"
  objects: [UPF-A, SMF-B]
  time_window: null
required_evidence:
  - id: req1
    kind: R
    fields: [event_type, observed_window]
    accepted_sources: [runtime_receipt]
  - id: req2
    kind: K
    fields: [version, troubleshooting_procedure]
    accepted_sources: [manual]
gold_plan:
  required_actions: [VERIFY_IDENTITY, READ_PFCP_STATUS, CHECK_N4_CONFIG]
  optional_actions: [READ_RELEVANT_LOG_CONTEXT]
  dependency_edges:
    - [VERIFY_IDENTITY, READ_PFCP_STATUS]
    - [VERIFY_IDENTITY, CHECK_N4_CONFIG]
  forbidden_actions: [UNAPPROVED_WRITE, CLAIM_EXECUTED_RESTART]
  permitted_equivalence_classes:
    - [READ_PFCP_STATUS, QUERY_PFCP_ASSOCIATION]
expected_behavior: diagnosed_with_evidence_or_explicit_gap
labels:
  reviewer_ids: []
  reviewed: false
```

**必须声明**：这些字段和 `accepted_sources` 是 proposed benchmark label，不对应已存在的厂商 CLI/API；真实命令必须来自已授权手册与明确版本。

### 6.4 防止数据泄漏与人为挑选

- 先按 `source_group` / `structure_group` 分组，再分配 dev/validation/heldout；同一故障注入 family 的细微词面变体不能跨 split。
- 专家 Gold 在模型推理前冻结；不能用待评价 Agent 的输出当 Gold，也不能把新系统特有 Contract 字段暴露给 baseline 作为答案提示。
- 验证集可用于调阈值和修 bug；最终 heldout **只在模型、prompt、代码与评价脚本冻结后使用**，已有 P6 消费的 heldout 不作为全新盲验。
- 外部公开 benchmark 若被用来微调、few-shot 或编写 prompt，相关题不能作为同轮独立 heldout。
- 难度维度包括：证据数量、关系跳数、版本/时间冲突、可见工具数量、缺失率和任务范围。

---

## 7. E2：GraphRAG × Evidence Contract × PPR 的有效证据检索

### 7.1 研究目的

判断“同一检索请求、同一证据源和图快照下，哪种图检索能找到更多**当前合法且有用**的证据”，不是展示更多图节点。

当前 `v8/graph.py` 是关系类型白名单 + 2-hop + node/edge 限额；PPR 可以作为新候选排序方法，ToG beam 作为成本更高的可选对照。**不要将 PPR 作为基础系统的强制组件。**

### 7.2 对照组：严格同一种子/预算

| 方法 | 文本种子 | 图扩展 | 适用性检查 | 目的 |
|---|---|---|---|---|
| G0 Hybrid P3 | 相同 | 无 | 原 P3 检查 | 稳定基线 |
| G1 Fixed-Hop | 相同 | 1/2-hop BFS | 统一最终检查 | 扩图效果 |
| G2 Contract BFS | 相同 | Relation/Scope/Time/Version 先验过滤 | K/R/P | 当前 v8 方法 |
| G3 PPR | 相同 | PPR top-K | 与 G2 **相同安全前置过滤** | 算法排序效果 |
| G4 Contract PPR | 相同 | 合格候选图上 PPR + 自定义 requirement | 与 G2 相同安全规则 | 方案候选 |
| G5 Beam-ToG-like（可选） | 相同 | 有限 beam + 相同关系约束 | 与 G2 相同安全规则 | 有更高成本的探索方法 |
| G6 Contract BFS + Re-seed | 原种子+合法替代种子 | G2 逻辑 | 与 G2 相同 | 排查错版本 seed 导致漏召回 |

**公平性**：约束前后只允许“候选扩展算法/补证策略”这一维变化；统一最大源扫描量、最大节点/边、top-K、日志和文档版本；不同检索底座（Neo4j 官方 HybridCypherRetriever）单列补充实验，不与同 P3 seed 的图方法直接比耗时。

### 7.3 Constrained PPR 机制（拟新增）

```text
Requirement
   ↓
验证 task scope、关系白名单、节点身份/时态/版本、来源标记
   ↓
生成可接受候选图 H（拒绝关系不参与 ranking）
   ↓
P3 semantic seeds → H 中的可用合法 seeds
   ↓
Personalized PageRank（damping/iter/tol 固定）
   ↓
按 PPR 排名输出 top-K 节点+可溯源路径
   ↓
K/R/P 再校验 → 必需字段覆盖/缺口补证
```

注意：如原 P3 seeds 因未知版本全部不可用，则 PPR 不会神奇地产生真值。必须报告 `seed_validity_rate`，并通过独立的 G6 `legal_reseed` 实验检验补救，而不能将“跳数变大”当成对错版问题的修复。

### 7.4 Gold 与指标

第一版建议 **80–120 个独立 Evidence-Requirement 查询**（计划值；按 K/R/P、1/2/3+ 跳、版本缺失、时效、跨对象分类），每条标注：

- 必需证据 ID 集合；允许多份等价证据；
- 支持/反对/不适用标签，产品/版本/时间/对象适用条件；
- 必需关系/路径（只有具有可靠关系标签时才评价 GraphPath Recall）；
- 查询预算、候选图大小、可能需要补充证据。

核心指标：

\[
\mathrm{ValidPrecision@K}=\frac{|R_K\cap G_{valid}|}{|R_K|},\quad
\mathrm{ValidRecall@K}=\frac{|R_K\cap G_{valid}|}{|G_{valid}|}
\]

另计 `Required Evidence Coverage`（按 requirement 是否至少得到必要字段集合，和 evidence-level recall 区分）、`Invalid Acceptance Rate`（错版/过期/越权/无凭据的节点/关系被采信比例）、`P95` 全链 retrieval latency、图扫描量与 token/工具成本。

**空分母处理**：无合法证据的案例不计入 recall 平均值，改评 `Correct No-Evidence Rate`；无返回节点时 Precision 标 N/A，而不是偷偷记 100%。

### 7.5 PPR 作为可选分支的退出条件

只有在同风险边界、同预算下，G4 相对 G2 呈现可信的有效 Recall/计划完成收益，且开销可接受，才将其设为默认候选；否则保留 BFS。不能预设 PPR 的时延、Token 或 Recall 必定更优。

---

## 8. E3：类型化补证的闭环效果

### 8.1 RQ

当 K/R/P 缺少证据，系统能否准确判断“缺什么、向哪里查、什么时候停”，从而比自由 Agent 补查更有效？

### 8.2 对照组

- T0：缺证后直接总结 / 拒答（no supplement）。
- T1：每轮重复原完整检索（naive full refresh）。
- T2：P5 LLM planner 选择工具（受相同权限预算约束）。
- T3：v8 `route_gaps` + `compile_gap_plan`（状态驱动定向补证）。
- T4：T3 + 合法重选种子/关系查询（待 E2 能力可用）。

### 8.3 场景

按 `knowledge-version-unknown`、`runtime-timezone-unknown`、`stale`、`one-side-missing`、`boundary-conflict`、`permission-denied`、`tool-unavailable`、`no-source-exists` 构建可补/不可补案例；确保存在**本来就不可补的情况**，不能让模型“查到什么都算成功”。

### 8.4 指标

- **Solvable Gap Closure Rate**：被真实有效证据关闭的可补缺口数 / Gold 指明可补缺口数。
- **False Gap Closure Rate**：无适用证据却被误判关闭的缺口 / 应维持未满足的缺口。
- **Redundant Tool Call Rate**：没有增加必需覆盖、没有完成合法确认、且被 Gold 判为非必要的工具调用 / 全部调用。不得把审计/必要负证据查询都当冗余。
- **Evidence per Call**：每次实际调用新增、经验证、被需要的字段数；另计预算消耗和 P95。
- **Correct Stop/Deferral**：工具不可用/预算不足时是否明确停止并保留未解决状态。

---

## 9. E4：局部更新、Salsa Early Cutoff 与依赖完整性

### 9.1 对比已经存在的实现，不误认“从零新增”

当前 `LocalEvaluator.update()` 已按依赖传播、读取集和语义状态变化做局部更新基础机制；新实验重点是**验证边界/性能，不是重复创建 Salsa**。

Salsa 官方 red-green 思路强调：输入 revision 更新后，判断 tracked function 的依赖是否真的变化；若重算输出可观察结果没变，就安全复用相关下游。将其用作理论参考，但不引入 Rust Salsa 运行库。

### 9.2 正确性所需的明确前提（建议写入论文的条件性命题）

对于依赖图 `D=(V,E)`，若满足：

1. **完备性**：每个 evaluator/ActionGate 的真实读取集合都包含在索引登记的边内，或有可执行的漏边发现机制；
2. **确定性**：相同快照、`evaluation_as_of`、权限、版本、策略输入下计算可复现；
3. **语义充分性**：下游实际观察的字段/版本/时窗/provenance/value 均进入变更投影；
4. **提交一致性**：新 evidence revision、状态和 gate 决定来自同一冻结 batch；
5. **异常回退**：依赖漏边、环路不收敛、源数据变化、预算不足时 fail closed；

则局部更新可以**以独立全量计算为可测试 oracle**，检查最终 `RequirementState` 与 `ActionDecision` 在可观察语义上相等。注意：这是有前提的算法正确性条件，**不是对任意动态代码和任意副作用的无条件数学定理**。

### 9.3 对照组

| 方法 | 算法特点 | 验证目标 |
|---|---|---|
| L0 Full | 每批独立全量重算 + full gate | 正确性 oracle |
| L1 Local-no-cutoff | 只沿依赖可达节点重算，输出不变时仍继续 | 区分局部索引与 early cutoff 收益 |
| L2 Local-with-cutoff | 当前语义基础 + 经加强的细粒度早停 | 评估早停贡献 |
| L3 Local-with-audit | L2 + 读集/依赖完整性审计 + 安全回退 | 可靠性/成本权衡 |

### 9.4 实验矩阵

继承现有规模脚本的 `S/M/L/XL × {1,5,10,50} × 20 seeds × 50 batches` 结构，作为可复核的**目标运行矩阵**。另加真实工作流更新场景（建议至少 30 个更新案例）：

- 字段值未变，仅 receipt/revision 变化；
- 状态码仍 `SATISFIED`，但 CPU、n4_enabled、MTU、peer_endpoint 等关键值改变；
- 仅无关字段变化；
- K 来源版本更新；
- R 时间跨过 freshness；
- P 对端映射 revision 改变；
- 证据删除 / 反证新增 / source SHA 改变；
- permission、task scope、`as_of` 改变；
- 跨 batch 复用旧 `ActionDecision`；
- 读取边**构建初始阶段**遗漏（不仅是事后手工删边）；
- 依赖环或无法收敛；
- 仅一个字段变化影响多个 ActionGate；
- dense update 使局部开销高于 full。

### 9.5 正确性指标（硬前置）

- `Semantic State Equality`: `full_states == local_states`（忽略纯展示序号，但**不忽略**重要 evidence basis、有效时间、版本、值、权限）。
- `Action Decision Equality`: full 和 local 对所有动作的 outcome、影响范围、前置证据引用相同。
- `Dependency Miss Rate`: 应失效但未被标记或误早停的读取者比例；产生一个实例即报告 blocker。
- `Safe Fallback Recall`: 漏边、环路、预算/失效触发时，是否及时 full recompute / pending / human review。
- `Stale Batch Decision Rate`: 是否出现旧 batch 的 `suggest_allowed` 被错误复用。

### 9.6 效率指标

- `Recomputed States/Actions`、`Pruned Downstream Readers`、`Fallback Rate`；
- `wall time` 的 P50/P95 + 置信区间，独立记录索引构建和缓存命中成本；
- `peak memory`、CPU time；在线阶段若调用工具/模型才统计真实工具/LLM；
- `Net Speedup = T_full / T_local`：小于 1 即局部更慢，必须诚实报告；
- `End-to-end incremental investigation latency`：针对真实 Agent 更新，不只测 Python evaluator。

### 9.7 推荐新增测试

```text
test_initial_missing_dependency_edge_fail_closed.py
test_early_cutoff_changed_value_same_state.py
test_action_predicate_direct_read.py
test_changed_as_of_and_expiry.py
test_multi_revision_batch_identity.py
test_permission_context_invalidation.py
test_dense_update_full_fallback.py
```

**学术表述**：可以说“在带有证据有效性/作用范围/动作门控的读取依赖图中，实现并实证考察提前截断与安全回退”；不要说“首次发明 Early Cutoff”。

---

## 10. E5：ActionGate 安全性与方案可用性

### 10.1 核心警惕：全部拒绝也能达到 0 unsafe

因此必须成对报告：

\[
\mathrm{URR}=\frac{\#\text{违规却被允许的候选建议}}{\#\text{本应禁止的候选建议}},\quad
\mathrm{VAAR}=\frac{\#\text{正确允许的合法候选建议}}{\#\text{本应允许的合法候选建议}}
\]

另外，给出方案级 `Unsafe Plan Rate`、`Correct Deferral Rate`、`VPR`，且将**未知/不应给出确定建议**的案例单独统计。

### 10.2 对照方法

- A0：LLM 原始建议、无 Validator（**只离线评估，不执行**）。
- A1：仅 Schema + Tool Whitelist。
- A2：加 K/R/P 和来源/版本/时间门控。
- A3：A2 + Action Impact Scope + 依赖快照一致性。
- A4：A3 + PlanIR 多步骤前置条件/依赖/禁止动作（建议方案）。

这组实验**使用相同候选集**进行纯 Gate 消融；另一组 end-to-end 实验再允许各系统产生不同候选，防止把模型生成差异错误归因于 Gate。

### 10.3 测试案例

重点加入：合法但缺少信息的检查建议、确有目标但无权限、假版本手册、错 peer/direction、旧时区、无审计来源、全是拒绝的退化系统、部分可解任务、审批状态不明、网络高风险操作请求。

### 10.4 安全统计的置信区间

若 N 个独立错误机会中观察到 0 错误，**不能宣布真实错误率 0%**；需要报告 N、分组情况和二项置信区间。对独立伯努利近似，95% 单侧上界可用 `1 - 0.05^(1/N)`（大 N 近似 `3/N`）；相关案例须按故障家族聚类。没有大量独立案例，就只能写“本测试集未观察到错误放行”。

---

## 11. E6：跨次运行稳定性与泛化

### 11.1 设计

相同场景多次采样、同义改写、信息顺序扰动、部分日志噪声、手册版本替换、拓扑多对象重排、missing fields、tool timeout。保持源语义和 Gold 不变的 perturbation 需先经专家确认。

### 11.2 指标

- `Task Pass@1` 与 `pass^k`：**同一实例连续 k 次均成功的实例比例**（τ-bench 思路），不要把 `pass^k` 简单理解为单次成功率的 k 次方；
- `Worst-case VPR`、`Critical Violation Frequency`、`Decision Flip Rate`；
- 各结构/来源组上的 Macro 平均而非只算总平均；
- `Seed/Temperature Stability`、`P95` 时间与工具成本。

### 11.3 heldout

新 source group + 新结构拓扑 + 新模板组合必须与 dev 隔离；失败不能删除重跑覆盖，修复之后只能在新的预注册评估批次上验收。

---

## 12. E7：Open5GS/UERANSIM 隔离网络验证（后期、必须和文本评估分离）

### 12.1 最省工程量的外部底座

优先参考 [`ATNoG/5g-agent-benchmarking-framework`](https://github.com/ATNoG/5g-agent-benchmarking-framework)：项目提供 Open5GS/UERANSIM + Kubernetes 测试床、Ansible 故障注入、Loki/Prometheus 日志指标、MCP 工具、trace、Token/工具计数和恢复清理。它适合当作**实验运行器和故障注入模板**，而不应该复制其所有多 Agent 架构替代本项目。

### 12.2 实验权限结构

```text
Independent Fault Harness (separate identity)
        │
        ├── apply fault in isolated lab
        ├── record injection time and ground truth
        ├── capture live logs/metrics/config and topology snapshot
        │
        ▼
UPF-Agent v8 (read-only access; no Chaos/SSH/kubectl writes)
        │
        ├── read observations / query evidence
        ├── produce diagnosis and PlanIR
        └── supply cited suggestions / abstain
        │
        ▼
Independent Evaluator
        ├── check injected root cause / location
        ├── check plan preconditions and step coverage
        └── (optional, explicitly approved) lab executor tests plan effects
        │
        ▼
Independent cleanup / restore baseline and verify recovery
```

若未来要验证处置效果，由**独立受控执行器或人工**在隔离环境按批准方案操作；v8 不会因此变成已实现自动修复。失败时必须恢复测试床，不得保留前一次故障造成的状态污染。

### 12.3 建议先测哪些故障

| 故障类 | 独立注入 | 关键观测 | 可评价目标 |
|---|---|---|---|
| UPF GTP-U 丢包 | lab 网络损伤 | N3 关联流量、丢包、日志 | N3/UPF 定位、调查步骤 |
| UPF 通信中断 | network partition | UE 业务异常、NF 状态 | 正确发现并定位断连 |
| 错误 DNN/订阅配置 | 合成/实验配置 | PDU Session 成功率、SMF/AMF 日志 | 配置问题类别与责任对象 |
| SCTP 阻断 / AMF 侧异常 | lab 层注入 | NGAP/SCTP 状态 | 区分 RAN/core 侧边界问题 |
| N6 限速 | tc/policer | 吞吐率、UPF/N6 数据面 | 区分用户面性能与核心网控制面 |
| N4/PFCP 心跳/关联异常 | 仅在掌握可复现注入器之后 | PFCP association/heartbeat + 真实事件 | N4 状态、故障对象、时间线 |

不要仅因旧厂商日志有 PFCP 关键字，就假定 Open5GS 会打印同一消息格式；`LogEvent` 适配器与故障标签需经 Open5GS 实际日志校验。

### 12.4 实验计划与指标

建议**先做 6–12 个不同注入条件，独立重复 3–5 次**；这只是建议的试点规模。若同一家族有多次重复，统计时按 fault family 聚类，不能把重试当独立故障类型。

- `Root Cause Top-1 / Top-3 Localization`（注入元信息为真值）；
- `Fault Localization Delay`（从第一份 Agent 可观察到的异常证据，到正确定位输出的时间）；
- `Read-only Investigation Cost`（真实工具调用、日志查询、模型请求、Token）；
- `Evidence Coverage and CDR`；
- `Network Functional Goal Achievement`（仅在独立执行器实验中，按预定义通过用例数/总用例数计算）；
- `Collateral Regression Tests`（处理前后其他 UE/Session/接口的功能回归）；
- `Cleanup/Restoration Integrity`（故障是否完全清除及实验基线恢复）。

**不要把 Diagnosis Latency 写成 MTTR；不要将经外部执行器完成的恢复归因于 Agent 的自动修复。**

### 12.5 关于“因果传播路径”指标

RCAEval 公开基准可提供注入故障标签、根因服务和多源遥测；但**仅有服务调用拓扑不能当因果传播图真值**。只有实验明确提供已验证的因果边集合，才使用：

\[
P_{edge}=\frac{|E_{pred}\cap E_{gold}|}{|E_{pred}|},\quad
R_{edge}=\frac{|E_{pred}\cap E_{gold}|}{|E_{gold}|}
\]

否则仅报告注入根因的 Top-K 命中、故障对象 F1，以及“推导关系的证据支撑率”，不得把相关性边叫因果边。

---

## 13. E8：外部 Benchmark 与 RAG 对照（独立报告，不参与 UPF 主结果平均）

### 13.1 OpsEval

- 使用公开的 5G Communication、Mobile Communication Network、Log Analysis / Wired Network 等已获许可题目评价领域知识；
- 对照当前生成模型、旧 Hybrid RAG、v8（能合理回答的任务类型）；
- 报告 MCQ Accuracy/QA 事实正确性；**不评价 N4 根因定位或 PlanIR 技术有效率**；
- 保留公开集合名称、版本、language split，避免将论文全文任务量当作公开可下载量。

### 13.2 Telco-RAG

- 在许可范围内，使用 3GPP 标准文本的版本/章节/交叉引用建立**独立标准检索实验**；
- 文本分块、查询改写和 rerank 策略分别消融；
- 评估章节/规范条款 Recall@K、引用定位准确率、版本适用性；
- 用户企业手册、UPF 实际产品命令和标准条款必须分来源/版本，不允许把 3GPP 通用消息字段冒充厂商具体命令。

### 13.3 RCAEval

- 先用官方标准 RCAEval 方法跑通外部数据与 baseline；
- 如需将微服务数据映射到 `EvidenceBinding`，建立独立 adapter，保留 source/type/ground truth；
- 只在数据确有根因标签的样本报告 Top-1/Top-K；
- 与 5GC 注入数据分开显示，不合成“整体 UPF 根因准确率”。

---

## 14. 全部指标字典：分母、缺失值、谁负责判定

| 指标 | 分母 | 判定方式 | 必须一起报告的伴随指标 |
|---|---|---|---|
| VPR | 可解任务总数 | Deterministic validator + expert adjudication | CDR、N、CI |
| MSR | Gold 必需步骤总数 | Action equivalence class 映射 | DAG dependency coverage |
| DAG Coverage | Gold 必需依赖边总数 | 计划拓扑序/先决条件 | MSR |
| HCVR | 应输出方案的任务数 | 类型化 hard constraints | Critical Violation 数 |
| EGRR | 提出关键建议的方案数 | evidence provenance + applicability | 无建议/正确拒答数 |
| CDR | Gold 不可解/需补证任务数 | Gold deferral label | VPR、错误确定性建议数 |
| URR | Gold 禁止候选动作数 | Gate + Oracle | VAAR，N，CI |
| VAAR | Gold 允许候选动作数 | Gate + Oracle | URR，CDR |
| Valid Evidence P@K | 返回证据项数 | Gold valid item | Valid R@K |
| Valid Evidence R@K | Gold valid evidence item 数 | Gold correspondence | No-evidence accuracy |
| Required Field Coverage | Gold 必需字段数 | fields verified under scope | Version/time violations |
| Gap Closure | Gold 可补缺口数 | 新合法 Binding + snapshot | Wrong closure rate |
| Local-State Consistency | 全部更新 batch 数 | full vs local | Action Consistency |
| Latency | 成功/失败任务分别报告 | wall-clock + stages | P50/P95，cold/warm |
| Root Cause Top-K | 有独立根因真值案例数 | 注入/核验标签 | unknown-GT 不纳入 |
| Functional GAR | 受控执行的独立功能测试数 | lab black-box assertion | 副作用、cleanup |

空分母输出 `N/A` 和计数，不用填 0 或 100%。所有样本保存 `source_level/synthetic/reviewed`，相同脚本下若混入多级数据，应分层报告；宏平均不取代各类结果。

---

## 15. 统计设计、消融公平性和停止准则

### 15.1 统计分析

- 二分类成功率：给出分子/分母、Wilson 95% CI；若两方法在相同任务上配对，考虑 McNemar 检验。
- 连续开销：给出 P50/P95、均值和任务级 paired bootstrap 置信区间；多次随机采样按 case/fault-family 聚类，避免伪独立。
- 同一场景不同方法：统一模型、seed、预算，固定输入快照和候选动作；如果方法天然具有不同工具行为，则记录真实资源消耗并在 **质量—成本 Pareto** 图比较。
- 多组实验：预先指定 E1 的 VPR/HCVR 为 primary，E2 的 Valid Recall 与 Invalid Acceptance、E4 的 equality/net cost 为 co-primary/secondary；避免事后选显著子图。
- 阶段报告失败案例、abstention、超时、源不可用、Schema 失败，不能过滤“不方便比较”的任务。

### 15.2 工程验收门槛（**拟定条件，不是已取得结果**）

**正确性硬门槛**：

1. Plan Validator 必须能检出测试集预植入的全部关键违规类型（未授权写、越权对象、错版本、关键参数不可信、伪称已执行等）；具体检出率报告基于哪些注入类别/数量。
2. Full-vs-Local 在冻结的确定性测试集中 `State + Action` 可观察语义一致；任何系统性不一致先修代码，不继续发表效率结论。
3. 图返回必须标注 source/time/version/synthetic，任何被错误接受的无来源物理关系为 blocker；**但允许返回“未知待核”的节点用于补证，不能将其当已适用证据**。
4. 网络实验仅在隔离部署成功、注入真值可核验、恢复脚本可用后开始。

**效果评价**：不预设必然提高 10%、30%；先注册正向假设和采样计划。预期结果未达到时，应给出影响因素、召回代价、负收益范围与模块修正路线。

### 15.3 实验停止/回退条件

- 出现越权写操作执行风险或敏感凭据外泄；
- 跨任务证据/缓存污染；
- Graph 或 Local 使用未经验证/错版本来源产生 `suggest_allowed`；
- 独立实验注入失败/清理失败；
- 评测器依赖待评系统的输出反向构造标准答案；
- Heldout 在调参阶段泄漏。

---

## 16. 具体代码改造清单（可拆给 Codex 的任务）

> 当前仓库未必存在以下新文件名。**本节全是【拟实施】接口，开发时以最新 `main`/正确分支为准，优先通过 adapter，避免覆盖旧 P5/P6 baseline。**

### P0：方案输出与评价底座（第一批）

| 新增/修改 | 具体实现 | 验收用例 |
|---|---|---|
| `v8/plan_ir.py` | `PlanIR/PlanStep/Predicate/PlanValidationReport`；动作类别、观察效果与网络效果分离 | 合法 N4 检查/未授权重启案例序列化 |
| `v8/plan_translator.py` | 模型输出→PlanIR，原文与解析错误不丢；所有方法同一转写约束 | 改写文本步骤数、字段一致性抽检 |
| `v8/plan_validator.py` | 工具白名单、Precondition、DAG、K/R/P、权限、版本、来源、终止条件、失败闭锁 | 错参数、缺前置、环路、命令未知、伪执行拒绝 |
| `v8/plan_metrics.py` | VPR/MSR/DAG/EGRR/CDR/HCVR/URR/VAAR，空分母 CI | 人工构造指标数值可逐项算对 |
| `v8/engine.py` | 保存原始方案、PlanIR、PlanValidationReport、stage timing | 一次 run 产物可回放；不改已有 ledger 语义 |
| `v8/scenarios.py` | baseline 工具/模型真实计数，修 B4 名称；结构化 plan 输出 | 同输入、同预算重跑 |
| `eval/v8_plan/` | Gold schema、专家复核、案例冻结、分组 split | 先试点 20–30 案例 |

**P0 Definition of Done**：至少 20–30 个试点 Gold、至少 3 类违规负例、P5/v8 均有原始文本和标准化 PlanIR；评审和统计工具能从冻结 trace 离线复算，且无不可追溯数字。

### P1：图、增量、安全性实验（第二批）

| 新增/修改 | 具体实现 | 验收用例 |
|---|---|---|
| `v8/graph_query_compiler.py` | 每条 Requirement → 允许对象/关系/字段/版本/时间/跳数/来源限制 | 不会因用户自由文本绕过 allowlist |
| `v8/graph_ranking.py` | `ConstrainedPPRRetriever`，与 BFS 相同安全过滤；记录 seed validity | 错版 seed 和合法 reseed 分组 |
| `v8/graph_experiment.py` | 80–120 需求、BFS/PPR/合法补证、统一计时与 Valid P/R | 结果支持按来源/跳数分析 |
| `v8/builders.py`、`v8/engine.py` | 图回写 K 时补可追溯目的标签/映射，绝不按任务自动编造 | graph evidence 能合法进入 K 或清楚报告 unknown |
| `v8/dependency.py` | 构建期漏边检测、早停语义审计、批次/as_of 的 gate 同步 | 与 full oracle 始终一致或安全 fallback |
| `v8/evaluation.py` | Full、Local-no-cutoff、Local-cutoff、Local-audited | 稀疏/稠密、显式负收益 |
| `v8/actions.py` | 统一 evaluation_as_of、Batch identity 与 PlanIR gate | 旧批次 `suggest_allowed` 不能跨范围生效 |

**P1 Definition of Done**：在既定测试矩阵中能复算 full/local；图对照报告同种子、同预算、多个来源标签和有效召回/错受；安全负例无错误执行授权（系统仍只读）。

### P2：外部基准与隔离网络（第三批）

| 新增/修改 | 实施原则 |
|---|---|
| `v8/external_benchmark.py` | 将 OpsEval/RCAEval/标准语料标为不同 `dataset_domain`；只读数据适配 |
| `lab/blueprints/` | 独立故障注入/清理，不由被测 Agent 执行 |
| `lab/adapters/open5gs.py` | 明确 Open5GS 日志与厂商日志规则差异，版本化解析映射 |
| `lab/metrics.py` | ground truth、故障时间、定位时间、网络功能用例 |
| `lab/run.py` | 注入—固定观测—诊断—（可选审批执行）—状态校验—清理 |

---

## 17. 推荐项目目录与产物格式

```text
upf-agent-graph/
  src/upf_agent/v8/
    plan_ir.py                # NEW
    plan_translator.py        # NEW
    plan_validator.py         # NEW
    plan_metrics.py           # NEW
    graph_query_compiler.py   # NEW
    graph_ranking.py          # NEW
    external_benchmark.py     # NEW (P2)
    ... original stable code
  config/
    v8_experiments.yaml       # NEW
  eval/v8_plan/
    schemas/{case,plan,review,metric}.schema.json
    dev/
    validation/
    heldout/                  # freshly frozen, no read by tuning pipeline
    adjudication/
  eval/v8_graph/
    gold_requirements/
    results/
  eval/v8_incremental/
    mutations/
    results/
  lab/
    blueprints/
    adapters/
    metrics.py
  experiments/v8_next/
    <experiment_id>/
      protocol.yaml
      frozen_inputs.json
      environment.json
      method_manifest.json
      raw_outputs.jsonl
      plan_ir.jsonl
      validation.jsonl
      traces.jsonl
      metrics_by_case.csv
      summary.json
      failures.jsonl
      sha256_manifest.json
```

### 17.1 建议逐任务 Trace 结构

```json
{
  "case_id": "N4-001",
  "method": "v8-full",
  "dataset_domain": "upf-fixture",
  "source_level": "D1",
  "synthetic": true,
  "reviewed": false,
  "run_id": "<opaque-id>",
  "code_commit": "<git-sha>",
  "model_id": "<frozen-model-id>",
  "source_manifest_sha256": "<sha256>",
  "output_kind": "plan",
  "raw_text_path": "raw/N4-001-v8.txt",
  "plan_ir_path": "plans/N4-001-v8.json",
  "validation_path": "validations/N4-001-v8.json",
  "metrics": {
    "valid_plan": false,
    "mandatory_step_coverage": null,
    "critical_violations": [],
    "tool_calls_attempted": null,
    "tool_calls_committed": null,
    "token_usage": null,
    "latency_ms": null
  }
}
```

`null` 表示未获取，绝不能填写猜测的 GPU、Token 或网络指标。

### 17.2 配置开关示例

```yaml
experiment_version: v8-next-1
freeze_required: true
methods:
  - p5-agent
  - v8-nograph
  - v8-full
plan:
  translator: frozen_parser
  validator: deterministic
  constrained_decoding: false
graph:
  backend: memory
  ranking: fixed_bfs      # fixed_bfs / constrained_ppr
  same_p3_seeds: true
  max_nodes: 100
  max_edges: 200
incremental:
  mode: audited_cutoff     # full / local_no_cutoff / audited_cutoff
safety:
  execute_network_write: false
stats:
  confidence: 0.95
  cluster_key: source_group
```

这是建议配置格式，**不是仓库现成可运行配置**。

---

## 18. 开发顺序与提交计划

| 迭代 | 任务 | 验证门槛 | 建议交付 |
|---|---|---|---|
| W0 | E0：基线冻结/统一计数 | 复跑原测试，公平计数器 | `e0-baseline-report.md` |
| W1 | PlanIR/PlanTranslator/PlanValidator + 20–30 试点 Gold | 合法/非法计划分类按人工 Gold 可复核 | `e1-pilot/` |
| W2 | E1 完整指标/盲评 + E5 门控同候选消融 | 分母、方法、标注差异可追溯 | `e1-e5-evaluation.md` |
| W3 | E4 Early Cutoff/完整读集负例及消融 | 独立 Full vs Local 语义一致 | `e4-local-audit.md` |
| W4 | E2 多源图 Gold + PPR/BFS | 同 seed 和成本；报告过滤召回代价 | `e2-graph-retrieval.md` |
| W5 | E3 定向补证 + E6 结构迁移 | 可补/不可补分离，blind split | `e3-e6-results.md` |
| W6+ | E8 域外基准、E7 隔离 Open5GS | 实验注入清理、真值和 trace | `e7-lab-report.md` |

时间仅为建议的周级任务拆分；是否能在每周完成取决于资料权限、标注人员和可用算力。**每个 W 段可作为独立 PR，禁止大规模改动旧 baseline 后又无法复现之前结果。**

### 18.1 第一批 Codex 开发任务（可直接复制）

> 基于 `jijigood/upf-agent-graph` 当前 `main` 工作，先创建独立评测分支，不修改现有 P5/P6 baseline 的运行逻辑。实现 `PlanIR`、`PlanValidator`、`PlanMetrics`，让 `v8.engine` 保存原始自然语言输出、结构化 PlanIR 和验证回执；为 P5/B0 设计公平且冻结的方案转换器。先在 synthetic-only fixtures 上编写可复算的 pytest，覆盖合法计划、缺必要步骤、依赖环、目标越权、错版本、证据来源无效、未经允许的写动作、误称已执行、缺证正确转人工。任何评分不得引用模型输出自行生成 Gold；每项失败保留 `case_id` 和原因。最后只提交代码、测试、合成样例与 README，并给出与旧 baseline 的回归结果。**不要**引入 Open5GS/Neo4j 新依赖，不要执行任何真实网络写操作。

---

## 19. 论文/专利中的建议结果展示与表述边界

### 19.1 结果章节建议

1. **表 1：体系与评价协议**。对照方法、任务类型、数据来源、主指标定义。
2. **图 1：E1 方案有效性**。P5/v8 的 VPR、步骤依赖覆盖、EGRR、HCVR 与 CDR；给出 CI。
3. **图 2：E2 有效证据检索**。BFS/PPR/Contract+Re-seed 的 Valid Precision/Recall、违规接受率、P95 和代价。
4. **图 3：E4 更新性能**。Full/Local-no-cutoff/Audited-cutoff 的等价性、净速度比、fallback，包含密集更新负收益。
5. **图 4：E5 安全—有效性 Pareto**。URR vs VAAR，错误拒绝/正确转人工并列。
6. **图 5：E7（仅成功搭建后）**。注入故障的 Top-1/Top-3 定位率、诊断延迟、网络目标通过数、无害性回归。
7. **案例表**。N4 错版 + 缺右侧边界实例：Raw evidence → K/R/P → Gap → PlanIR → Validator → 建议/转人工，标注每步来源。

### 19.2 论文贡献应如何写

- **已经实现基础**：只读工具型 UPF Agent、证据引用、契约模板、K/R/P、受约束图检索、局部重算、建议门控（以当前源码和补齐回归证据为准）。
- **拟新增并需实验证实的贡献**：具有多解/DAG 的方案有效性评价协议；PlanIR + 确定性验证；PPR 作为在契约过滤下的算法消融；读取依赖完备性检测与 early cutoff 安全性；真实故障注入的目标达成。
- **不得提前写的结论**：显著提高方案准确率、降低 MTTR、GraphRAG 全面提升 Recall、现网零危险、已实现自主修复、因果路径定位成功率、端到端 RAN/核心网强耦合自动闭环。

### 19.3 关于专利的注意点

PPR、VAL/PDDL 前置条件验证、Early Cutoff、grammar-constrained decoding 都是已公开的通用技术，不能把单独采用这些技术称为原创。专利的潜在重点应留在**以业务路径和证据需求限定取证、以 K/R/P 驱动补证、以字段读取依赖控制局部状态更新、以作用范围对建议门控**的技术协同。是否具备新颖性和创造性仍需专利检索，评测效果不能替代该判断。

---

## 20. 验收清单（用于研发和论文自审）

### 方案与数据

- [ ] PlanIR 区分只读观察、建议和真实网络状态改变。
- [ ] Gold 样例有 multiple-valid-plan/DAG、禁止动作、必须步骤、来源/版本/可解性标签。
- [ ] 两名以上专家盲评且分歧可追踪；评价器与被评模型隔离。
- [ ] 不可解/缺证案例的 CDR 与可解案例 VPR 分别统计。
- [ ] 所有方案原文都保留；PlanIR parser 失败不被剔除。

### 图与增量

- [ ] Graph 合法性过滤在关系排序前与后均清晰记录；未知来源不直接当可用证据。
- [ ] PPR 与 BFS 使用同样 P3 seeds、可比较预算、同一个真实/合成图快照。
- [ ] 同时报告 precision 和 recall，尤其记录错误版本种子造成的覆盖损失。
- [ ] 局部重算与全量比较包含值、时效、来源、权限、ActionGate，而不仅 state code。
- [ ] 读边起始遗漏、未收敛、跨批次时有安全 fallback 证据。

### 实验与安全

- [ ] 工具调用数均来自真实计数器；估算口径不混用。
- [ ] `results.csv` 包括失败、超时、拒答和空输出。
- [ ] 完整样本与指标公式预先冻结，`heldout` 不反复调参。
- [ ] 任何真实网络写操作都由独立授权隔离执行器负责；Agent 在当前阶段只读。
- [ ] 审稿人能从 synthetic-only fixtures 复跑确定性指标，而无需企业数据或个人密码。
- [ ] 结果文字只表达已实际复算的数字，不把脚本声明或预设目标写成实测事实。

---

## 21. 参考文献、标准与开源入口（核验后的正确链接）

### 21.1 与方案评价直接相关

1. **TelcoAgent-Bench** (2026，预印本)，论文 [arXiv:2604.06209](https://arxiv.org/abs/2604.06209)；仓库 [BrahiM-Mefgouda/TelcoAgent](https://github.com/BrahiM-Mefgouda/TelcoAgent)。MSC/EAP/SAS/稳定性与蓝图结构用于借鉴。
2. **TeleCom-Bench** (2026，预印本)，[arXiv:2605.18025](https://arxiv.org/abs/2605.18025)；仓库 [ZTE-AICloud/TeleCom-Bench](https://github.com/ZTE-AICloud/TeleCom-Bench)。公开仓库只放出部分数据。
3. **Position: LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks**，ICML 2024，[PMLR](https://proceedings.mlr.press/v235/kambhampati24a.html)。外部验证器思想；属于观点论文，不能误写为已经严格证明所有 LLM 都无法规划。
4. **VAL**，计划验证工具，[KCL-Planning/VAL](https://github.com/KCL-Planning/VAL)；前置条件、动作效果和状态推进参考。
5. **PlanBench**，[arXiv:2206.10498](https://arxiv.org/abs/2206.10498)；**TravelPlanner**，ICML 2024，[arXiv:2402.01622](https://arxiv.org/abs/2402.01622)，[代码](https://github.com/OSU-NLP-Group/TravelPlanner)。
6. **NetConfEval**，2024，[DOI](https://doi.org/10.1145/3656296)，[代码](https://github.com/RedHatResearch/conext24-NetConfEval)，[数据](https://huggingface.co/datasets/NetConfEval/NetConfEval)。
7. **NetConfBench**，2026 Internet-Draft（**非 RFC**），[草案](https://datatracker.ietf.org/doc/draft-cui-nmrg-llm-benchmark/)；**NetArena**，ICLR 2026，[论文](https://openreview.net/forum?id=BPVPOtzoOz)，[代码](https://github.com/Froot-NetSys/NetArena)。
8. **τ-bench**，[arXiv:2406.12045](https://arxiv.org/abs/2406.12045)；[代码](https://github.com/sierra-research/tau-bench)。最终状态与多次运行稳定性。

### 21.2 检索、图和增量计算

9. **Telco-RAG**，Bornea et al.，2024，[arXiv:2404.15939](https://arxiv.org/abs/2404.15939)，[代码](https://github.com/netop-team/Telco-RAG)。3GPP 标准检索方法，非故障方案 Gold。
10. **HippoRAG**，NeurIPS 2024，[arXiv:2405.14831](https://arxiv.org/abs/2405.14831)，[代码](https://github.com/OSU-NLP-Group/HippoRAG)。PPR 关联检索；较新的仓库可能同时包含 HippoRAG 2，使用时标明具体版本。
11. **Think-on-Graph**，ICLR 2024，[论文](https://proceedings.iclr.cc/paper_files/paper/2024/hash/10a6bdcabbd5a3d36b760daa295f63c1-Abstract-Conference.html)，[代码](https://github.com/DataArcTech/ToG)。LLM + beam 图探索。
12. **Salsa**，[仓库](https://github.com/salsa-rs/salsa)，[red-green 算法说明](https://github.com/salsa-rs/salsa/blob/master/book/src/reference/algorithm.md)。作为动态读依赖和 early cutoff 方法参考，不需要 Rust 运行库。
13. **Outlines**，[仓库](https://github.com/dottxt-ai/outlines)；**XGrammar**，[仓库](https://github.com/mlc-ai/xgrammar)。用于结构化解码消融，不保证网络语义正确。

### 21.3 AIOps 与 5GC 实验资源

14. **OpsEval**，Liu et al.，[arXiv:2310.07637](https://arxiv.org/abs/2310.07637)，[公开数据](https://github.com/NetManAIOps/OpsEval-Datasets)。运维知识 QA/MCQ，不是直接可用的真实 UPF 因果故障标签。
15. **RCAEval**，Pham et al.，[arXiv:2412.17015](https://arxiv.org/abs/2412.17015)，[仓库](https://github.com/phamquiluan/RCAEval)，[数据入口](https://huggingface.co/datasets/phamquiluan/RCAEval)。以根因服务/故障标签和遥测评测为主；因果边指标需逐样本确认真值。
16. **DejaVu**，[仓库](https://github.com/NetManAIOps/DejaVu)。作为 RCA 算法参考，不能误充 RCAEval 数据集。
17. **5G Agent Benchmarking Framework**，[ATNoG/5g-agent-benchmarking-framework](https://github.com/ATNoG/5g-agent-benchmarking-framework)。隔离 Open5GS/UERANSIM 测试床、故障注入、轨迹和成本统计。
18. **Open5GS**，[open5gs/open5gs](https://github.com/open5gs/open5gs)；**UERANSIM**，[aligungr/UERANSIM](https://github.com/aligungr/UERANSIM)。作为后期实验网络，不等同于当前 v8 已部署环境。

### 21.4 参考文献使用与版权安全

- 所有论文量化结果均只能按“作者报告”引用，除非保存可复算原始数据和运行环境。
- 外部仓库是否直接复制、修改或重新分发，需在实施前检查各项目实际许可证、数据使用条款和具体版本。3GPP 规范与运营商手册的获取/复用需单独核实授权。
- 当前本报告以 `upf-agent-graph` 的指定 commit 为代码快照，若未来代码已有变化，应重新审计相应文件，不能将旧缺口永久写成当前状态。

---

## 22. 最后给研发的一句话

**先做 E0 + E1（把“方案”变成真正可核验的对象），再做 E4（证明局部更新正确且有条件高效），之后做 E2/E3/E5/E6（证明证据约束与 Agent 决策的贡献），最后通过 E7 的隔离 5GC 注入实验把“文本/规则正确”推进为“任务与网络目标有可观察效果”。**

新的实验体系不以“计划看起来合理”为成果，也不预设复杂度越高越好；只有当它在同数据、同预算、同评价规则下带来明确可重复的改进，才将该改进写成论文与专利的有效效果。
