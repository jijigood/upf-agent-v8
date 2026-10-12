# UPF-Agent 向 v8 证据契约智能编排架构升级规划

> 项目：`jijigood/upf-agent`  
> 目标：在当前 Dify 外迁后的本地 UPF 运维 Agent 基础上，逐步升级为“Evidence Contract → QueryPlan → 多源证据 → K/R/P → Typed Re-evidence → Dependency-local Recompute → Action Gate”的受控智能编排原型。  
> 原则：最大化复用当前 P3/P4/P5/P6 已实现能力，不推倒重来；新增模块与专利 v8、实验验证和论文表达保持一一对应。

---

## 1. 当前系统真实基线

当前 `upf-agent` 已经不是简单的 Dify 固定工作流迁移版本，而是一个具备有限自治能力的、本地部署的、只读 Tool-using Agent。

当前可确认的主要能力包括：

- 基于 LangGraph 的有限轮次 Agent 调查流程；
- 本地模型调用、工具调用、checkpoint、resume、interrupt；
- 任务预算、工具调用预算、模型调用预算；
- `Exact + BM25 + Dense Retrieval + RRF + Qwen3 Reranker` 的 Hybrid RAG；
- 手册知识的来源 SHA、chunk、locator、版本范围校验；
- 日志结构化解析、Parquet 存储、DuckDB 查询；
- PFCP / GTP-U 等事件分类及 raised / cleared / observed 状态区分；
- 日志事件与时间、实体、拓扑的保守关联；
- TopologyEdge 的 `valid_from / valid_to` 时态字段；
- VerifiedEvidence、ToolPacket、Receipt、Journal 等证据和审计对象；
- P6 开发集 / heldout / 人工复核 / freeze / 单次留出集等实验治理体系。

当前仍未完整实现的 v8 核心能力：

- 显式 Evidence Contract；
- Contract → QueryPlan Compiler；
- K / R / P 状态机；
- 双侧边界证据匹配；
- 状态驱动的 Typed Re-evidence；
- 字段级 DependencyIndex；
- Dependency-local Recompute；
- 三类逻辑证据图与 GraphRAG；
- ActionCandidate 与 ActionGate；
- 受控写操作、回采和回滚。

因此当前升级重点不是重写基础工程，而是补齐“结构化证据需求与受控编排层”。

---

# 2. 总体升级架构

```text
Current stable system
────────────────────────────────

Task
 ↓
AgentTask
 ↓
LangGraph
 ├── Hybrid RAG
 ├── Log tools
 ├── Topology tools
 └── VerifiedEvidence

                    ↓ evolve

V8 orchestration layer
────────────────────────────────

Task
 ↓
AgentTask
 ↓
EvidenceContract
 ↓
QueryPlanCompiler
 ↓
 ┌──────────────┬───────────────┬────────────────┐
 │              │               │                │
Hybrid RAG   GraphRAG       Runtime Tools     Topology Tools
 existing      NEW             existing          existing
 │              │               │                │
 └──────────────┴───────┬───────┴────────────────┘
                        ↓
                 EvidenceBinding
                        ↓
                   K / R / P
                        ↓
                    GapRouter
                        ↓
              Targeted Re-evidence
                        ↓
                 DependencyIndex
                        ↓
                 LocalRecompute
                        ↓
          Diagnostic Candidate + ActionCandidate
                        ↓
                    ActionGate
                        ↓
          Suggest / Re-evidence / Human
```

核心设计原则：

1. LLM 负责理解、规划、解释和候选生成；
2. K/R/P、版本、时效、权限、边界一致性、依赖更新和 ActionGate 由确定性代码实现；
3. 现有 Hybrid RAG、日志解析、拓扑工具、LangGraph 和 P6 评估体系全部保留；
4. GraphRAG 作为新增证据图通道，而不是替换当前 Qdrant / BM25 / Reranker；
5. 第一阶段只做只读建议，不做真实网络配置下发。

---

# 3. 推荐代码目录

```text
src/upf_agent/
│
├── 现有稳定代码
│   ├── agent_contracts.py
│   ├── agent_engine.py
│   ├── agent_tools.py
│   ├── agent_store.py
│   ├── agent_runtime.py
│   ├── agent_worker.py
│   ├── p3_search.py
│   ├── p3_answer.py
│   ├── log_parser.py
│   ├── log_tools.py
│   ├── log_correlation.py
│   └── topology.py
│
├── orchestration/
│   ├── __init__.py
│   ├── models.py
│   ├── contract.py
│   ├── contract_compiler.py
│   ├── query_plan.py
│   ├── evidence.py
│   ├── adapters.py
│   ├── state.py
│   ├── evaluator.py
│   ├── boundary.py
│   ├── gap_router.py
│   ├── dependency.py
│   ├── recompute.py
│   ├── action.py
│   ├── action_gate.py
│   ├── engine.py
│   └── store.py
│
├── graph/
│   ├── schema.py
│   ├── store.py
│   ├── memory_store.py
│   ├── neo4j_store.py
│   ├── builder.py
│   └── retrieval.py
│
└── orchestration_cli.py
```

配置与实验目录：

```text
config/
├── orchestration.yaml
└── evidence_contracts.yaml

eval/
└── orchestration/
    ├── contracts/
    ├── states/
    ├── boundaries/
    ├── recompute/
    ├── graph/
    ├── action_gate/
    └── end_to_end/

tests/
└── orchestration/
    ├── test_contract.py
    ├── test_contract_compiler.py
    ├── test_query_plan.py
    ├── test_evidence_binding.py
    ├── test_k_state.py
    ├── test_r_state.py
    ├── test_boundary_state.py
    ├── test_gap_router.py
    ├── test_dependency.py
    ├── test_local_recompute.py
    ├── test_graph_store.py
    ├── test_graph_retrieval.py
    ├── test_action_gate.py
    ├── test_orchestration_engine.py
    └── test_orchestration_resume.py
```

---

# 4. V1：Evidence Contract + QueryPlan

## 4.1 保留 AgentTask

当前 `AgentTask` 继续表示：

- 用户问题；
- product / version；
- device_ids；
- time_window；
- log_generation；
- topology_generation；
- manual_generation；
- budget。

它解决的是“允许访问什么任务范围”。

Evidence Contract 则解决“完成判断必须有哪些证据”。

---

## 4.2 新增 Evidence Contract

建议 `orchestration/contract.py`：

```python
class EvidenceClass(StrEnum):
    KNOWLEDGE = "K"
    RUNTIME = "R"
    BOUNDARY = "P"


class RequirementStatus(StrEnum):
    UNKNOWN = "unknown"
    SATISFIED = "satisfied"
    MISSING = "missing"
    NOT_APPLICABLE = "not_applicable"
    STALE = "stale"
    CONFLICT = "conflict"


class ObjectRef(StrictModel):
    domain: str
    object_type: str
    object_id: str


class EvidenceRequirement(StrictModel):
    requirement_id: str
    evidence_class: EvidenceClass
    object_ref: ObjectRef
    required_fields: list[str]

    product: str | None = None
    version: str | None = None

    interface_type: str | None = None

    time_window: TimeWindow | None = None
    freshness_seconds: int | None = None

    path_position: str | None = None

    permission: Literal["read", "suggest", "execute"] = "read"

    mandatory: bool = True


class EvidenceContract(StrictModel):
    contract_id: str
    run_id: str
    template_id: str
    requirements: list[EvidenceRequirement]
    compiler_version: str
    contract_hash: str
```

要求：

- Contract 必须是 machine-checkable；
- 不把自由文本 Prompt 当作 Contract；
- requirement 必须明确对象、字段、时间、版本、权限和证据类别。

---

# 5. Business Path 与跨域边界模型

`orchestration/models.py`：

```python
class Domain(StrEnum):
    RAN = "ran"
    TRANSPORT = "transport"
    CORE = "core"


class PathSegment(StrictModel):
    segment_id: str
    domain: Domain
    object_type: str
    object_id: str
    order: int


class PathBoundary(StrictModel):
    boundary_id: str
    left_segment_id: str
    right_segment_id: str
    interface_type: str | None = None


class BusinessPath(StrictModel):
    path_id: str
    segments: list[PathSegment]
    boundaries: list[PathBoundary]
    synthetic: bool = False
```

当前真实资料不足以支撑完整 RAN—Transport—Core 实网跨域，因此跨域实验必须显式使用：

```python
synthetic=True
```

避免把合成 fixture 表述为真实网络拓扑。

---

# 6. Contract 模板机制

不建议让 LLM 自由生成全部 Evidence Contract。

推荐流程：

```text
Question
   ↓
IntentFrame
   ↓
Contract Template
   ↓
EvidenceContract
```

例如：

```yaml
templates:

  upf_n4_fault:
    requirements:

      - id: K_N4_GUIDE
        class: K
        domain: core
        object_type: UPF
        required_fields:
          - fault_description
          - troubleshooting_procedure
          - version

      - id: R_PFCP_EVENTS
        class: R
        domain: core
        object_type: UPF
        interface: N4
        required_fields:
          - event_type
          - event_state
          - timestamp
          - peer_ip

      - id: P_N4_BOUNDARY
        class: P
        domain: core
        interface: N4
        required_fields:
          - local_endpoint
          - peer_endpoint
          - direction
          - observation_window
```

第一版至少实现：

- `upf_n4_fault`
- `upf_n3_fault`
- `manual_operation`
- `log_observation`

---

# 7. ContractCompiler

`orchestration/contract_compiler.py`：

```python
def compile_contract(
    task: AgentTask,
    intent: IntentFrame,
    path: BusinessPath | None,
    templates: ContractTemplateRegistry,
) -> EvidenceContract:
    ...
```

第一版建议使用确定性规则：

```text
PFCP / N4
→ upf_n4_fault

GTP-U / N3
→ upf_n3_fault

配置 / 命令 / 操作
→ manual_operation

日志统计 / 告警观察
→ log_observation
```

LLM-assisted compiler 可作为后续实验分支，不作为主实现的第一依赖。

---

# 8. QueryPlan

`orchestration/query_plan.py`：

```python
class QueryRoute(StrEnum):
    MANUAL_RAG = "manual_rag"
    LOG_TOOL = "log_tool"
    TOPOLOGY_TOOL = "topology_tool"
    GRAPH = "graph"


class QueryStep(StrictModel):
    query_id: str
    requirement_ids: list[str]
    route: QueryRoute
    tool_name: str | None = None
    arguments: dict[str, JsonValue]
    mandatory: bool = True
    reason: str


class QueryPlan(StrictModel):
    contract_id: str
    steps: list[QueryStep]
    compiler_version: str
```

第一版直接复用当前已有工具：

```text
K requirement
→ search_manual
→ read_manual_block

R requirement
→ analyze_log_window
→ find_log_events
→ read_log_context

P requirement
→ lookup_topology
```

例如：

```text
K_N4_GUIDE
→ search_manual(query="PFCP节点不可达", product="UPF", version="5.0")

R_PFCP_EVENTS
→ find_log_events(protocol="PFCP")

P_N4_BOUNDARY
→ lookup_topology(device_id="UPF-A", interface_type="N4")
```

---

# 9. EvidenceBinding：不重写 VerifiedEvidence

现有 `VerifiedEvidence` 继续负责：

- evidence_id；
- source_id；
- SHA；
- locator；
- excerpt；
- native_id；
- metadata；
- task scope。

新增 `EvidenceBinding` 表示：

> 某份 VerifiedEvidence 对当前 Evidence Requirement 能证明什么。

```python
class EvidenceBinding(StrictModel):
    binding_id: str
    evidence_id: str
    requirement_ids: list[str]

    evidence_class: EvidenceClass
    object_ref: ObjectRef

    fields: dict[str, JsonValue]

    observed_at: datetime | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None

    product: str | None = None
    version: str | None = None

    source_generation: str | None = None

    synthetic: bool = False
```

---

# 10. Adapter 层

`orchestration/adapters.py`：

```python
def bind_manual_evidence(
    evidence: VerifiedEvidence,
    requirement: EvidenceRequirement,
) -> EvidenceBinding:
    ...


def bind_log_evidence(
    evidence: VerifiedEvidence,
    requirement: EvidenceRequirement,
) -> EvidenceBinding:
    ...


def bind_topology_evidence(
    evidence: VerifiedEvidence,
    requirement: EvidenceRequirement,
) -> EvidenceBinding:
    ...
```

作用：

- 保持现有 P3/P4/P5 工具输出兼容；
- 将 manual / log / topology 的 metadata 统一绑定到 Requirement；
- 不直接修改现有稳定模块。

---

# 11. V2：K / R / P 状态机

## 11.1 State 模型

```python
class StateReason(StrEnum):
    FIELD_MISSING = "field_missing"
    VERSION_MISMATCH = "version_mismatch"
    VERSION_UNKNOWN = "version_unknown"

    TIME_EXPIRED = "time_expired"
    TIME_UNKNOWN = "time_unknown"

    IDENTITY_MISSING = "identity_missing"

    LEFT_MISSING = "left_missing"
    RIGHT_MISSING = "right_missing"

    BOUNDARY_CONFLICT = "boundary_conflict"


class RequirementState(StrictModel):
    requirement_id: str
    evidence_class: EvidenceClass
    status: RequirementStatus

    supporting_evidence_ids: list[str] = []
    opposing_evidence_ids: list[str] = []

    missing_fields: list[str] = []
    conflicting_fields: list[str] = []

    reasons: list[StateReason] = []

    evaluator_version: str


class SatisfactionSnapshot(StrictModel):
    contract_id: str
    states: list[RequirementState]
    evaluated_at: datetime
    snapshot_hash: str
```

---

# 12. K：Knowledge Applicability

K 主要判断：

- source 是否存在；
- object 是否匹配；
- product 是否匹配；
- version 是否适用；
- required_fields 是否齐全；
- source 是否可追溯；
- 证据是否满足 Contract 当前用途。

示例：

```text
Requirement:
UPF 5.0
requires:
  troubleshooting_procedure
  version

Retrieved manual:
version = 4.x
```

结果：

```text
K = NOT_APPLICABLE
reason = VERSION_MISMATCH
```

不能因为“检索到了相关文本”就视为满足。

---

# 13. R：Runtime Evidence

R 主要判断：

- required_fields 是否完整；
- timestamp 是否可用；
- timezone 是否明确；
- evidence 是否落在 observation window；
- freshness 是否满足；
- device identity 是否明确；
- tool receipt 是否成功；
- 多来源当前值是否冲突。

示例：

```text
timestamp_utc = null
device_id = null
```

结果：

```text
R = MISSING

missing_fields:
  - timestamp
  - device_id

reasons:
  - TIME_UNKNOWN
  - IDENTITY_MISSING
```

---

# 14. P：Boundary Evidence

`orchestration/boundary.py`：

```python
class BoundarySide(StrEnum):
    LEFT = "left"
    RIGHT = "right"


class BoundaryEvidenceTuple(StrictModel):
    boundary_id: str
    side: BoundarySide

    service_id: str | None

    local_endpoint: str | None
    peer_endpoint: str | None

    direction: str | None

    observation_start: datetime | None
    observation_end: datetime | None

    mapping_version: str | None

    evidence_ids: list[str]
```

匹配函数：

```python
def match_boundary(
    left: BoundaryEvidenceTuple | None,
    right: BoundaryEvidenceTuple | None,
) -> RequirementState:
    ...
```

满足条件：

```text
service_id compatible
AND
left.local == right.peer
AND
left.peer == right.local
AND
direction reciprocal
AND
time-window overlap
```

状态：

```text
SATISFIED
LEFT_MISSING
RIGHT_MISSING
CONFLICT
STALE
UNKNOWN
```

注意：当前 TopologyEdge 不能直接等同于 P；P 需要双侧边界证据。

---

# 15. Typed Re-evidence

`orchestration/gap_router.py`：

```python
class SupplementType(StrEnum):
    KNOWLEDGE = "knowledge"
    RUNTIME = "runtime"
    BOUNDARY_LEFT = "boundary_left"
    BOUNDARY_RIGHT = "boundary_right"
    VERSION = "version"
    TIMEZONE = "timezone"
    IDENTITY = "identity"


class SupplementTask(StrictModel):
    supplement_id: str
    requirement_id: str
    supplement_type: SupplementType

    route: QueryRoute
    tool_name: str | None
    arguments: dict[str, JsonValue]

    trigger_reasons: list[StateReason]
```

规则示例：

```text
K = VERSION_UNKNOWN
→ 补版本证据

R = TIME_UNKNOWN
→ 请求时区或时间基准

R = STALE
→ 只刷新 Runtime

P = RIGHT_MISSING
→ 只补右侧边界

P = CONFLICT
→ 双侧复核 / mapping review

permission denied
→ Human
```

这一步将当前 LLM-driven 补查升级为：

> state-gap-driven mandatory supplement。

---

# 16. LLM Planner 的新角色

当前 `agent_worker.py` 的 planner 不删除。

新结构：

```text
Mandatory Plan
  ← K/R/P GapRouter

Optional Exploratory Plan
  ← LLM
```

优先级：

```text
Evidence Contract
>
K/R/P Gap
>
LLM Plan
```

LLM 不能绕过 mandatory requirement，也不能直接将缺失证据视为满足。

---

# 17. V3：DependencyIndex

`orchestration/dependency.py`：

```python
class DependencyKey(StrictModel):
    evidence_id: str
    field_name: str


class DependencyIndex(StrictModel):
    field_readers: dict[str, list[str]]
    state_readers: dict[str, list[str]]
```

依赖关系至少包括：

```text
EvidenceField → RequirementState
RequirementState → RequirementState
RequirementState → ActionGate
EvidenceField → ActionGate
```

示例：

```text
E1(PFCP log.peer_ip)
   ↓
R_PFCP
   ↓
ACTION_CHECK_N4

E2(boundary-right.peer_endpoint)
   ↓
P_TC
   ↓
ACTION_CHECK_N4

E3(PFCP knowledge.version)
   ↓
K_CORE
   ↓
ACTION_CHECK_N4
```

---

# 18. Local Recompute

`orchestration/recompute.py`：

```text
changed evidence
       ↓
diff fields
       ↓
mark reachable readers INVALID
       ↓
queue = direct readers
       ↓
recompute node
       ↓
compare:
  state code
  validity
  judgement basis
       ↓
if changed:
  enqueue successors
else:
  preserve unaffected readers
       ↓
queue empty
```

关键要求：

不能只比较：

```text
old_state.status == new_state.status
```

还必须比较：

- judgement_basis；
- actual evidence values；
- version；
- provenance；
- validity window。

例如：

```text
CPU 30% → 90%
R status 仍为 SATISFIED
```

如果动作要求 `CPU < 80%`，ActionGate 仍必须重算。

---

# 19. Full vs Local Baseline

当前系统 scope 变化后会粗粒度清空：

```text
receipts
evidence
facts
gaps
candidates
```

因此天然可以作为：

> Full / Coarse Invalidation baseline。

实验：

```text
B0 Current Full/Coarse Recompute

vs

B1 Dependency-local Recompute
```

核心指标：

- State Consistency；
- Action Decision Consistency；
- Recomputed State Count；
- Tool Calls；
- Retrieval Count；
- LLM Requests；
- Latency；
- Dependency Recall。

正确性要求：

```text
Final State(Local) == Final State(Full)

Action Decision(Local) == Action Decision(Full)
```

效率提升是第二目标。

---

# 20. State Update Receipt

每次增量更新必须保存：

```json
{
  "update_id": "u3",
  "new_evidence": [
    "ev-boundary-right-001"
  ],
  "changed_fields": [
    "P_TC.peer_endpoint"
  ],
  "invalidated_states": [
    "P_TC"
  ],
  "recomputed_states": [
    "P_TC"
  ],
  "invalidated_actions": [
    "ACTION-2"
  ],
  "full_recompute": false
}
```

该 artifact 用于：

- 调试；
- 实验；
- 专利实施例；
- 论文可复现；
- 局部重算证明。

---

# 21. V4：Evidence Graph 与 GraphRAG

GraphRAG 不应替换当前 Hybrid RAG。

目标架构：

```text
                     QueryPlan
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 Current Hybrid RAG                Graph Route
 Exact/BM25/Dense/RRF          Neo4j relation retrieval
        │                               │
        └───────────────┬───────────────┘
                        ▼
               Evidence Candidates
                        ▼
               Applicability Gate
```

---

# 22. Evidence Graph Store 抽象

`graph/store.py`：

```python
class EvidenceGraphStore(Protocol):

    def upsert_nodes(...): ...

    def upsert_edges(...): ...

    def bounded_subgraph(
        self,
        seed_ids: list[str],
        relations: list[str],
        max_hops: int,
        valid_at: datetime | None,
        limit: int,
    ) -> EvidenceSubgraph:
        ...
```

实现：

```text
MemoryEvidenceGraphStore
Neo4jEvidenceGraphStore
```

单元测试优先使用 Memory backend，集成实验再使用 Neo4j。

---

# 23. 三类逻辑图

## Static Network Graph

来源：

- TopologyEdge；
- device；
- port；
- interface；
- domain。

核心节点：

```text
NetworkObject
Interface
ManagementDomain
Service
```

核心关系：

```text
HAS_INTERFACE
CONNECTS_TO
BELONGS_TO_DOMAIN
CARRIES
PEER_OF
```

---

## O&M Knowledge Graph

来源：

- DocumentBlock；
- CommandRecord；
- RetrievalChunk；
- fault rule；
- procedure。

文本继续留在 Qdrant。

只把高价值结构关系写入图：

```text
KnowledgeItem
FaultRule
Procedure
Command
Version
Interface
```

关系：

```text
APPLIES_TO
REQUIRES
SUPPORTS
RELATED_TO_INTERFACE
HAS_VERSION
FROM_SOURCE
```

---

## Dynamic Evidence Graph

来源：

- LogEvent；
- VerifiedEvidence；
- ToolPacket；
- Receipt；
- ConfigSnapshot。

不要把全部原始日志逐行入图。

正确链路：

```text
raw log
↓
existing parser
↓
LogEvent
↓
selected EvidenceBinding
↓
Dynamic Evidence Graph
```

---

# 24. GraphRAG 第一版节点与关系

节点类型：

```text
NetworkObject
Interface
KnowledgeItem
Observation
BoundaryEvidence
Requirement
ActionCandidate
```

关系类型：

```text
BELONGS_TO_DOMAIN
CONNECTS_TO
APPLIES_TO
OBSERVED_ON
BOUNDARY_PEER
SUPPORTS
CONTRADICTS
REQUIRES
DEPENDS_ON
AFFECTS
```

第一阶段不要建：

```text
CAUSES
```

因为当前没有足够因果证据。

---

# 25. Contract-constrained Graph Retrieval

普通 GraphRAG：

```text
question
↓
entity seed
↓
free expansion
```

本方案：

```text
EvidenceRequirement
↓
GraphQueryPlan
↓
约束：
  seed object
  path position
  relation types
  max hops
  time
  version
  permission
↓
Bounded Evidence Subgraph
```

示例：

```text
Requirement = P_N4
```

允许：

```text
UPF-A
 -- CONNECTS_TO →
 N4
 -- BOUNDARY_PEER →
 SMF-A
```

不允许：

```text
UPF-A
→ 无限制多跳扩展
→ 大量无关网元
```

---

# 26. GraphRAG 对照实验

建议方法组：

```text
B0 Current Hybrid RAG
B1 Ordinary GraphRAG
B2 Contract-constrained GraphRAG
```

主要指标：

- Evidence Precision；
- Required Evidence Coverage；
- Invalid Evidence Acceptance Rate；
- Wrong-version Acceptance Rate；
- Stale Evidence Acceptance Rate；
- Unsupported Relation Acceptance Rate；
- Source Traceability Rate。

其中：

```text
Source Traceability = 100%
Unsupported physical/runtime evidence acceptance = 0
```

可以作为硬约束目标。

---

# 27. V5：ActionCandidate 与 ActionGate

当前 `Candidate` 继续表示：

> 诊断候选解释。

新增 `ActionCandidate`：

```python
class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ActionCandidate(StrictModel):
    action_id: str
    action_type: str

    target_object: ObjectRef

    parameters: dict[str, JsonValue]

    rationale_evidence_ids: list[str]

    required_requirement_ids: list[str]

    impact_object_ids: list[str]

    risk_level: RiskLevel

    approval_required: bool = True
```

第一阶段仅允许生成建议，例如：

```text
CHECK_N4_CONFIGURATION
CHECK_INTERFACE_STATUS
VERIFY_PEER_MAPPING
RESTART_RECOMMENDATION
```

不执行真实命令。

---

# 28. ActionGate

```python
class GateDecision(StrEnum):
    SUGGEST_ALLOWED = "suggest_allowed"
    RE_EVIDENCE = "re_evidence"
    HUMAN_REVIEW = "human_review"
    BLOCKED = "blocked"
```

第一阶段明确不加入：

```text
EXECUTE_ALLOWED
```

避免提前进入真实写操作、回滚、幂等和权限事务复杂度。

ActionGate 判断至少包含：

- 所需 K/R/P 是否满足；
- required fields 是否当前有效；
- version 是否适用；
- permission 是否满足；
- impact scope 是否已重新计算；
- conflicting / stale / unknown 是否存在。

---

# 29. Action Impact Scope

例如：

```text
Action:
CHECK N4 configuration on UPF-A
```

根据：

```text
UPF-A
↔ N4
↔ SMF-A
```

计算：

```text
ImpactScope =
  UPF-A
  N4 boundary
  SMF-A
```

只重新验证该影响范围需要的：

```text
K
R
P
permission
```

而不是重算整个业务路径。

---

# 30. 新 LangGraph 结构

`orchestration/engine.py`：

```text
START
  ↓
resolve_intent
  ↓
resolve_path
  ↓
compile_contract
  ↓
compile_query_plan
  ↓
collect_initial_evidence
  ↓
bind_evidence
  ↓
evaluate_states
  ↓
┌─────────────────────────────────┐
│                                 │
│ 存在缺口                        │ 全部满足
▼                                 ▼
route_gap                    derive_candidates
  ↓                                 ↓
supplement_evidence           derive_actions
  ↓                                 ↓
bind_incremental              impact_scope
  ↓                                 ↓
local_recompute               action_gate
  │                                 ↓
  └──────→ evaluate if needed ─→ finalize
```

人工补充继续复用当前：

- `interrupt()`；
- `Command()`；
- `SqliteSaver`；
- resume 机制。

---

# 31. OrchestrationData

```python
class OrchestrationData(StrictModel):

    task: AgentTask

    intent: IntentFrame | None = None

    business_path: BusinessPath | None = None

    contract: EvidenceContract | None = None

    query_plan: QueryPlan | None = None

    evidence_ids: list[str] = []

    bindings: list[EvidenceBinding] = []

    satisfaction: SatisfactionSnapshot | None = None

    supplement_tasks: list[SupplementTask] = []

    dependency_index: DependencyIndex | None = None

    diagnostic_candidates: list[Candidate] = []

    action_candidates: list[ActionCandidate] = []

    gate_decisions: list[ActionGateResult] = []

    terminal: bool = False
```

不建议继续扩大现有 `AgentData`。

---

# 32. 运行产物

```text
runs/orchestration/<run_id>/
│
├── task.json
├── intent.json
├── path.json
├── contract.json
├── query_plan.json
│
├── evidence/
│   ├── initial.json
│   └── supplements.jsonl
│
├── states/
│   ├── initial.json
│   └── updates.jsonl
│
├── dependency.json
├── action_candidates.json
├── gate_results.json
│
├── events.jsonl
├── metrics.json
├── report.json
└── report.md
```

---

# 33. orchestration.yaml

```yaml
version: orchestration-v1

contract:
  template_file: config/evidence_contracts.yaml

supplement:
  max_rounds: 3
  max_attempts_per_requirement: 2

dependency:
  strategy: field_level

graph:
  enabled: false
  backend: memory
  max_hops: 2
  max_nodes: 100

action_gate:
  execution_enabled: false
  default_approval_required: true
```

第一阶段：

```text
graph.enabled = false
```

等 K/R/P 与 Local Recompute 稳定后再打开。

---

# 34. 开发阶段

## V1：Contract + QueryPlan + Adapter

实现：

```text
AgentTask
↓
EvidenceContract
↓
QueryPlan
↓
Current Tools
↓
EvidenceBinding
```

暂时不做：

- Neo4j；
- Action；
- Local Recompute。

完成标准：

对于：

```text
“分析 UPF-A 的 N4 PFCP 节点不可达问题”
```

能得到：

```text
K1:
  N4 / PFCP 故障知识

R1:
  PFCP 告警 / 心跳运行证据

P1:
  N4 拓扑 / 边界证据
```

并生成对应 QueryPlan。

---

## V2：K/R/P + GapRouter

完成后应输出类似：

```text
K1 = SATISFIED
  source = emergency-guide
  version = 5.0

R1 = MISSING
  missing = device_id
  reason = IDENTITY_MISSING

P1 = MISSING
  reason = RIGHT_MISSING
```

随后：

```text
R1 → request device identity
P1 → retrieve peer-side boundary evidence
```

---

## V3：Dependency + Local Recompute

示例：

```text
初始：
K1 = SATISFIED
R1 = SATISFIED
P1 = RIGHT_MISSING

新增：
right endpoint evidence
```

Full：

```text
K1 重算
R1 重算
P1 重算
Action1 重算
Action2 重算
```

Local：

```text
只重算：
P1
Action2
```

要求：

```text
FinalState(Full) == FinalState(Local)
```

---

## V4：Evidence Graph + GraphRAG

保留：

- Qdrant；
- BM25；
- Exact；
- Qwen Embedding；
- Qwen Reranker。

新增：

- Neo4j；
- Graph Store；
- Contract-constrained graph retrieval。

对照：

```text
Current Hybrid RAG
vs
Ordinary GraphRAG
vs
Contract-constrained GraphRAG
```

---

## V5：ActionCandidate + ActionGate

第一阶段只做：

```text
Suggest
Re-evidence
Human review
Blocked
```

不做真实网络执行。

---

# 35. 推荐提交顺序

建议 Codex 按如下 commit 拆分：

```text
Commit 1
feat(orchestration): add core contract models

Commit 2
feat(orchestration): add deterministic contract compiler

Commit 3
feat(orchestration): add query plan compiler

Commit 4
feat(orchestration): add evidence bindings and adapters

Commit 5
feat(orchestration): add K/R/P state evaluators

Commit 6
feat(orchestration): add boundary matching and gap router

Commit 7
feat(orchestration): add dependency index

Commit 8
feat(orchestration): add local recompute engine

Commit 9
feat(graph): add evidence graph abstraction and memory backend

Commit 10
feat(graph): add Neo4j backend and graph retrieval

Commit 11
feat(orchestration): add action candidate and action gate

Commit 12
feat(orchestration): add orchestration LangGraph and CLI
```

---

# 36. 实验体系

继续复用当前 P6 实验治理思路：

```text
dev
heldout
source-group isolation
reviewed labels
freeze configuration
single-use heldout
```

新增：

```text
eval/orchestration/business_v1/
```

---

# 37. 核心实验矩阵

| 方法 | Hybrid RAG | Agent | Contract | K/R/P | Evidence Graph | Local Recompute | Action Gate |
|---|---:|---:|---:|---:|---:|---:|---:|
| B0 | ✓ | × | × | × | × | × | × |
| B1 Current Agent | ✓ | ✓ | × | × | × | × | × |
| B2 Contract Agent | ✓ | ✓ | ✓ | ✓ | × | × | × |
| B3 Contract + Local | ✓ | ✓ | ✓ | ✓ | × | ✓ | × |
| B4 GraphRAG | ✓ | ✓ | × | × | ✓ | × | × |
| Ours | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

# 38. 单元实验

必须覆盖：

```text
版本错误
→ K != SATISFIED

版本未知
→ K = UNKNOWN / NOT_APPLICABLE，按契约规则

时区未知
→ R 不得满足绝对时间要求

字段缺失
→ R = MISSING

过期运行证据
→ R = STALE

单侧边界
→ P != SATISFIED

端点冲突
→ P = CONFLICT

方向不匹配
→ P = CONFLICT

窗口不交叠
→ P = STALE / CONFLICT

无关字段变化
→ 不触发无关状态重算

必要状态未满足
→ ActionGate 不得放行

状态码不变但真实值变化
→ 相关 ActionGate 必须重算
```

---

# 39. Local vs Full 主实验

规模建议：

| 规模 | Evidence | State | Action |
|---|---:|---:|---:|
| S | 100 | 30 | 10 |
| M | 500 | 150 | 30 |
| L | 2,000 | 600 | 100 |
| XL | 10,000 | 3,000 | 500 |

每次随机更新：

```text
1
5
10
50
```

个 Evidence fields。

指标：

```text
State Consistency
Action Consistency
Recomputed State Count
Recomputed Action Count
Tool Calls
Retrieval Calls
Model Calls
Latency
```

硬性要求：

```text
State Consistency = 100%
Action Consistency = 100%
```

效率数据按实测报告，不预设“提升 XX%”。

---

# 40. Dependency 缺边反例

故意删除：

```text
P_TC → ActionG
```

然后更新：

```text
boundary-right.peer_endpoint
```

预期：

```text
Local result != Full result
```

证明：

> DependencyIndex completeness 是局部重算正确性的必要前提。

保护机制：

```text
dependency completeness uncertain
→ expand recompute
or
→ HUMAN_REVIEW
```

---

# 41. State 编码不变但 Value 改变

例如：

```text
Old CPU = 30%
R = SATISFIED

New CPU = 90%
R = SATISFIED
```

若 Action 前置条件：

```text
CPU < 80%
```

则：

```text
ActionGate 必须重算
```

因此状态比较必须包含：

- judgement basis；
- actual evidence values；
- version；
- provenance；
- validity。

---

# 42. GraphRAG 实验

方法：

```text
B0 Current Hybrid RAG
B1 Ordinary GraphRAG
B2 Contract-constrained GraphRAG
```

指标：

```text
Evidence Precision
Required Evidence Coverage
Invalid Evidence Acceptance
Wrong-version Acceptance
Stale Evidence Acceptance
Unsupported Relation Acceptance
Source Traceability
```

不要只使用最终问答准确率。

---

# 43. ActionGate 实验

组合：

| K | R | P | Permission | Expected |
|---|---|---|---|---|
| SAT | SAT | SAT | OK | Suggest |
| NOT_APPLICABLE | SAT | SAT | OK | Re-evidence |
| SAT | STALE | SAT | OK | Re-evidence |
| SAT | SAT | CONFLICT | OK | Review |
| SAT | SAT | SAT | Denied | Human/Blocked |

核心指标：

```text
Incorrect Release Rate
```

目标：

```text
0
```

---

# 44. 现有资源复用映射

```text
Qdrant
→ Text Knowledge Store

BM25 / Exact
→ Sparse / Literal Retrieval

Qwen3-Embedding-4B
→ Dense Retrieval

Qwen3-Reranker-4B
→ Evidence Ranking

DocumentBlock / CommandRecord
→ O&M Knowledge Graph source

LogEvent / DuckDB / Parquet
→ Runtime Evidence source

TopologyEdge
→ Static Network Graph source

VerifiedEvidence
→ Provenance source

Journal / Receipt
→ Audit source

LangGraph
→ Orchestration Runtime

P6
→ Evaluation Governance
```

---

# 45. 暂时不要做的工作

当前阶段不建议：

- 重写现有 Hybrid RAG；
- 重写 log parser；
- 更换 LangGraph；
- 上复杂 Multi-Agent；
- 直接做真实配置下发；
- 全量把所有文本构造成知识图谱；
- 把 Neo4j 中存在节点就称为 GraphRAG；
- 让 LLM 决定 K/R/P 最终状态；
- 让日志相关性直接等同于根因；
- 把合成跨域数据写成真实跨域闭环。

---

# 46. 第一批建议创建的文件

第一阶段只创建：

```text
src/upf_agent/orchestration/
├── __init__.py
├── models.py
├── contract.py
├── contract_compiler.py
├── query_plan.py
├── evidence.py
├── adapters.py
├── state.py
└── evaluator.py
```

再新增：

```text
config/evidence_contracts.yaml
tests/orchestration/
```

第一阶段目标：

```text
Task
→ Contract
→ QueryPlan
→ Existing Tool
→ EvidenceBinding
→ K/R/P
```

跑通后再进入 GapRouter / Dependency / GraphRAG / ActionGate。

---

# 47. 推荐正式技术表述

第一阶段完成后可使用：

> 在现有本地 UPF 运维 Agent 的 Hybrid RAG、日志分析和拓扑查询能力基础上，新增显式 Evidence Contract 与证据状态评估层，将运维任务转换为结构化证据需求，并将检索和工具调用映射到对应需求；通过知识适用性 K、运行证据 R 和边界一致性 P 状态区分“有证据”与“证据可用于当前决策”，为后续类型化补证、局部重算和动作门控提供统一状态基础。

此阶段不能声称：

> 已实现完整时态异构 GraphRAG。

GraphRAG 要等 V4 真正接入关系图与有界图查询后再表述。

---

# 48. 与专利 v8 的代码对应关系

```text
S1 业务路径
→ models.py

S2 Evidence Contract
→ contract.py
→ contract_compiler.py

S3 多源取证
→ query_plan.py
→ adapters.py
→ current tools

S4 K/R/P
→ state.py
→ evaluator.py
→ boundary.py

S5 定向补证 + 局部更新
→ gap_router.py
→ dependency.py
→ recompute.py

S6 候选动作与影响范围校验
→ action.py
→ action_gate.py
```

最终目标：

> 专利、代码、实验、论文图采用同一条技术链，不再形成四套不同叙事。

---

# 49. 总结

当前 `upf-agent` 已经具备较成熟的基础工程能力，因此升级不应从零开始。

建议路线：

```text
现有 P3/P4/P5/P6 稳定底座
        ↓
Evidence Contract
        ↓
QueryPlan
        ↓
EvidenceBinding
        ↓
K / R / P
        ↓
Typed Re-evidence
        ↓
Dependency-local Recompute
        ↓
Evidence Graph / GraphRAG
        ↓
ActionCandidate
        ↓
ActionGate
```

优先顺序：

```text
V1 Contract + QueryPlan
V2 K/R/P + GapRouter
V3 Dependency + Local Recompute
V4 Evidence Graph + GraphRAG
V5 ActionCandidate + ActionGate
```

其中最值得优先形成实验结果的是：

> **Current Full/Coarse Invalidation vs Dependency-local Recompute**

其次是：

> **Current Hybrid RAG vs Ordinary GraphRAG vs Contract-constrained GraphRAG**

以及：

> **无 Evidence Gate vs K/R/P + ActionGate 的错误放行率比较。**

整个升级过程中应坚持：

> 保留现有稳定能力，新增模块逐层覆盖，不为追求“Agent化”“GraphRAG化”而重写已经验证过的工程资产。
