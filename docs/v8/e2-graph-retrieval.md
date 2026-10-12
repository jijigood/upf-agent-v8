# E2 图证据检索：完整开发矩阵与复算

2026-10-09。工程矩阵完成；独立查询 Gold 尚未审定，以下质量只针对预先保存的开发参考。

## 规模与实际调用

- 96 查询：K48/R24/P24。真实现有 P3 索引 1,061 chunks，使用实际 embedding／BM25／exact／reranker，96 次检索缓存后供五组共享；原始请求结果在 `e2-full-002/seed-cache`。
- `e2-full-003`：G0 P3、G1 fixed-hop 末端过滤、G2 Contract BFS、G3 PPR、G4 BFS+legal reseed，共 480 次实际检索。top-K 5/10/20 是同一 top-20 排名的三个截面，共 1,440 条观测，不冒称 1,440 次调用。
- 2 跳／100 节点／200 邻接；同一图、原始 P3 cache、主种子及 fallback 池。首次 full 发现高扇出扫描不到 R/P；共享图按公开类别把 native evidence 边排在文档高扇出边前，五组一同使用。G4 在主种子交接失效时使用真实缓存内的合法节点，不使用参考答案种子。
- 混合补充 pilot：K12/R6/P6，24×5=120 次；PPR alpha 0.70/0.95 另 48 次，0.85 固定为主组。该混合子集是开发修订后登记的补充验证，不是先前独立审定的 Gold pilot。
- K 绑定回写审计单列。额外五个真实手册 Ledger 探针：BFS/PPR/reseed 单文段各关闭目标 K；篡改源拒绝 19 个候选；19 个不同 instruction 的共同写入保留 conflict。它们不表示完整任务已满足，不将不同文段拼成未经审查的一条事实。

## 开发参考结果

| 方法 | Recall@5 | Recall@10 | Recall@20 | 错受数@20 |
|---|---:|---:|---:|---:|
| G0-P3 | 34.68% | 41.75% | 42.11% | 0 |
| G1-fixed-hop | 82.05% | 89.12% | 89.47% | 0 |
| G2-contract-BFS | 73.10% | 87.72% | 89.47% | 0 |
| G3-PPR | 73.10% | 87.37% | 89.47% | 0 |
| G4-legal-reseed | 81.59% | 97.24% | 100.00% | 0 |

宏召回分母为有开发相关证据的 57 查询；无相关证据、单侧 P 和权限拒绝另列。K 开发参考以相同原生章节为等价集合，R/P 取任务规格对应的来源记录。未独立判定自然语言相关性。PPR 没有胜过 BFS，保持 BFS 默认。

## 来源、成本与限制

- 主结果 [summary](../../runtime/v8-next/phase3/e2-full-003/summary.json)；[1,440 条观测](../../runtime/v8-next/phase3/e2-full-003/observations.json)；[只读复核](../../runtime/v8-next/phase3/e2-full-audit-001.json)。核验 485 输入、2,413 条路径及来源、1,560 条 K 回写绑定。
- K 的适用映射是 `reviewed=false` 的明确开发规则，知识主体来自真实文件；图中对象关联与 R/P 是合成开发结构。UPF 5.0 K 主要来自一份手册，R/P 同一 fixture 血缘；96 查询不是 96 个独立故障。
- R/P 只评检索线索和必需字段覆盖，未实现 graph R/P 写回，不以返回一侧 P 声称双侧映射已满足。
- `total_retrieval_seconds` 为实际 P3 缓存准备耗时＋当前方法扫描／排序／快照序列化，P3 在本实验实际只执行一次/查询。索引构建、worker 启动、共享图最初物化未计入此值；图物化未测量，不能写成 0。K 二次来源回写审计独立记录，主检索预算不含这项辅助审计。top-5/10 没有单独测延迟。
- 现有 Full 对同一对象多个 instruction 值给出 conflict；候选合法／相关与单值 Contract 可组合性需要分别处理，禁止直接去重或合并成“已满足”。
- 早期 `e2-full-001` 来源在 data 外被保护拒绝；`e2-full-002` 保留高扇出/无 fallback 的负结果及旧写回计数问题；`e2-full-003` 修正 tuple 计数并保存实际回写列表。补充探针 001/002 的 API 使用／多值冲突失败也保留，003 五类终态通过。

## 复跑入口

```bash
cd /home/huangxiaolin/upf-agent-v8
.venv-v8/bin/python scripts/v8_e2_full.py --output runtime/v8-next/phase3/e2-new-id --seed-cache runtime/v8-next/phase3/e2-full-002/seed-cache
.venv-v8/bin/python scripts/v8_phase3_matrix_review.py --experiment E2 --root runtime/v8-next/phase3/e2-full-003 --output runtime/v8-next/phase3/e2-new-audit.json
```

使用新 ID。去掉 `--seed-cache` 会实际加载检索模型并执行全部 P3 检索；复算不调用模型。见[总计划](../../plan.md)。

补充矩阵只读审计：[168 次检索与 5 个 Ledger 探针复算](../../runtime/v8-next/phase3/e2-mixed-pilot-and-sensitivity-audit-003.json)。逐条核对原评分、实际物理来源、SQLite 中的原子 receipt／绑定／保存状态及 Full/Local，新增模型调用 0。审计脚本 001/002 的字段名误用已留失败日志，003 修正后通过；没有改动实验原件。

```bash
.venv-v8/bin/python scripts/v8_e2_supplement_review.py \
  --batch runtime/v8-next/phase3/e2-full-003 \
  --root runtime/v8-next/phase3/e2-mixed-pilot-and-sensitivity-003 \
  --output runtime/v8-next/phase3/e2-supplement-new-audit.json
```
