# E4 四模式正确性审计（2026-10-09）

当前代码的小矩阵、边界与独立控制均通过；全量 64,000 方法批次尚待完成。第二阶段人工参考批准和原文双评继续独立进行，本次没有模型请求、实际网络写入或 heldout 消费。

## 方法与安全边界

| 方法 | 受影响读者传播 | 语义不变截断 | 逐次实际读集成员核验 |
|---|---|---|---|
| L0 Full | 契约独立完整遍历，不构造 DependencyIndex | 无 | 不使用被测索引 |
| L1 Local-no-cutoff | 所有受影响读者继续重算 | 关闭 | 关闭 |
| L2 Local-cutoff | 直接读者重算，输出不变可复用下游 | 开启 | 关闭 |
| L3 Local-audited-cutoff | 同 L2，实际读边不符时 Full fallback | 开启 | 开启 |

所有 Local 均保留初始独立 Full 实际读集认证、每批索引完整性保护、环／权限／上下文／预算保护。L1/L2 只关闭逐次实际读集成员核验，不关闭读集采集；因此本次审计消融衡量成员核验增量，并非去掉全部追踪成本。默认 LocalEvaluator 保持 L3；L1/L2 是实验对照，不保证检出未来规则新增分支漏边。

比较使用 complete_results，涵盖状态／动作语义、证据来源／revision basis、batch、as_of、权限和 context；仅排除 computed_batch_id。旧 semantic_results 不作为主验收。Full 和 Local 允许共用底层规则；18 个手工预期安全控制补充同源比较，仍不属于专家 Gold。

## 已执行结果

| 实验 | 协议 | 方法批次／场景 | 结果 |
|---|---|---:|---|
| e4-small-002 | S/M × 1/5/10 字段 × 3 seeds × 10 batches × 4 | 720 | 720 一致；每方法 180 |
| e4-audit-002 | 原 30 类边界 × 3 Local | 90 | 90 完整认证一致 |
| e4-audit-002 独立控制 | 合法、值敏感拒绝、预算停止、相同输入恢复、漏边、环 × 3 | 18 | 18 通过 |
| e4-stress-002 | S/M/L/XL × 10%/50%/100%／根节点高扇出 × 3 seeds × 3 batches × 4 | 576 | 576 一致 |
| e4-stable-fanout-001 | S/M/L/XL × 3 seeds × 3 batches × 4 | 144 | 144 一致；独立错误版本／C 缺失预期均符合 |

最终源 SHA：`2e7e0b4b82614d18b1acbb3b276d0431d24fc0effbee8de048d5b930c1d8f225`。四个开发规模属于人工构造的工作负载，计数不是独立真实事故数。

稳定输出对照把 R:0 的版本设为 4.0，需求仍为 5.0；修改其值／revision 不改变“不可适用”的状态输出。C 读者因此可以安全复用：S/M/L/XL 的 L1 分别重算 11/31/101/501 个状态，L2/L3 均只重算 1 个；XL Full 重算 3,500 个。每个对照仍与独立 Full 完整比较，保存输入快照和逐批回执，避免仅凭开关名字认定消融有效。

## 修复与失败留档

1. 预算中断已推进 snapshot，但 pending 读者或仅中断动作不能因后续相同输入而永久滞留。修后无界恢复执行 Full 并重新认证；再次带预算重试保持人工出口，直到完成恢复。
2. Local 原先逐动作调用公共 gate，每次重新计算整个任务／契约的上下文。XL 50 字段 cProfile 显示 resolve_context 共 49 次、累计 1.10 秒；修后只在公开 update 入口验证一次，再执行与 Full 相同的内部规则。公开 gate 的独立上下文检查仍在；完整性／权限／basis 检查保留。
3. 旧 e4-small-001 720 批、e4-stress-001 的 440 条已完成 CSV 行全部保留。后者因 XL 严重负收益主动中断（exit 130），不是通过批次：440 条已保存行无差异，但不能当作完整 576 批通过。中断记录、修前代码快照和 profiler 均留档。

558 项全量回归通过（36.64 秒），含新 E4 19 项；最终涉及文件 Ruff 通过。新分支漏读、构建期漏边、环、时间过期、权限改变、完整认证和中断恢复均有回归。

## 证据与复跑

- [小矩阵](../../runtime/v8-next/phase3/e4-small-002/summary.json)、[90 边界与 18 控制](../../runtime/v8-next/phase3/e4-audit-002/summary.json)。
- [稠密／高扇出](../../runtime/v8-next/phase3/e4-stress-002/summary.json)、[稳定输出对照](../../runtime/v8-next/phase3/e4-stable-fanout-001/summary.json)。
- [旧慢批次中断](../../runtime/v8-next/phase3/e4-stress-001/interruption.json)、[热点修前](../../runtime/v8-next/phase3/e4-hotspot-001/before.txt)、[修后](../../runtime/v8-next/phase3/e4-hotspot-001/after.txt)。
- [全量回归](../../runtime/v8-next/phase3/regression-002.json)、[JUnit](../../runtime/v8-next/phase3/regression-002.xml)。

```bash
# 所有 output 均须使用新 ID；目录存在时拒绝覆盖。
.venv-v8/bin/python scripts/v8_next_local_matrix.py --output runtime/v8-next/phase3/e4-small-NEW
.venv-v8/bin/python scripts/v8_e4_audit.py --output runtime/v8-next/phase3/e4-audit-NEW
.venv-v8/bin/python scripts/v8_next_local_matrix.py --profile stress --correctness runtime/v8-next/phase3/e4-small-NEW/summary.json --output runtime/v8-next/phase3/e4-stress-NEW
.venv-v8/bin/python scripts/v8_e4_cutoff_control.py --output runtime/v8-next/phase3/e4-stable-fanout-NEW
```

扩量入口拒绝缺少 720 批正确性证据、失败证据或源码 hash 不同的证据。已启动全量任务以冻结副本运行，未来修改当前工作树不会改动该任务代码。不同 source 版本的实验不能混成同一统计组。
