# E6：重复采样与语义保持扰动实验

完成时间：2026-10-10T00:20:32.889957+08:00。最终 `e6-full-002` 完成 540/540 次，全部结果进入只读复算；独立参考与扰动语言语义尚未审定，正式验收保持待完成。

## 输入与执行

20 个 N3/N4 开发案例（01–12、17–24），三方法 × 五次独立执行，共 300 次。四类扰动是措辞、记录顺序、拓扑顺序、无关噪声，每案例每方法各一次，共 240 次。80 份扰动证明核对对象、版本、时间、权限、方向与观察事实；修改物理文件后重新绑定 source hash 与 registry。参考在全部模型输出之前冻结，reviewed=false。第二阶段 20 个双侧映射修订参考用于开发输入，不能替代用户确认和第二位评审。

所有原生 P5 规划请求和共同方案头请求明确设置 temperature=0.2；五次 seed=1101–1105，扰动使用 1101。实际 HTTP 请求、原始响应、用量和失败均保存。模型是本地 Qwen3-30B-A3B-Instruct-2507，BF16、16K；E6 三方法统一使用本轮独立服务 18002、最多 8 并发和 decode CUDA graph。模型 generation defaults 的 top_k=20、top_p=0.8 保存在 service-context.json，temperature 由请求覆盖。此服务的批处理与历史 18000 不同，不做跨服务延迟比较。

执行代码为预先冻结的 `e2-e5-code-freeze-002`；本批源 SHA 为 `04854cb77bde58eb8dea5290c1e607adbac6c2cdcaba4d0c501061b7ea6c13bc`，最终工作树另保存最新 E3 修订。每次独立任务相同 8 工具／8 模型／3 轮／180 秒预算；全部候选仅输出只读建议，不执行网络动作。

## 完整分母结果

| 方法 | 重复参考匹配／100 | 扰动参考匹配／80 | pass@1 开发估计 | 五次均成功案例／20 | 最差轮次匹配率 | 参考 Decision Flip／80 | Validator Flip／80 |
|---|---:|---:|---:|---:|---:|---:|---:|
| P5+CommonPlanHead | 100 | 80 | 100.00% | 20 | 100.00% | 0 | 0 |
| v8-no-graph+CommonPlanHead | 100 | 80 | 100.00% | 20 | 100.00% | 0 | 0 |
| v8-full+CommonPlanHead | 100 | 80 | 100.00% | 20 | 100.00% | 0 | 0 |

只读审计核验 880 个输入和 1037 次实际模型请求；失败记录 0 条。没有丢弃失败、只挑成功续跑或替换原文。正式 VPR=null，已批准参考分母=0。pass@1 是该受控开发分布上的单次匹配率，不是专家确认的成功率。

| 方法 | 实际工具调用 | 实际模型调用 |
|---|---:|---:|
| P5+CommonPlanHead | 967 | 677 |
| v8-no-graph+CommonPlanHead | 1080 | 180 |
| v8-full+CommonPlanHead | 1260 | 180 |

## 变化诊断与适用范围

任务 ID、context fingerprint 和 source hash 随独立执行或来源重绑定变化，原文 hash 不同不能证明模型进行了有效随机探索。审计另对动作／参数／依赖结构，以及 v8 实际字段事实和状态做去除这些记账标识后的诊断。结构诊断忽略自然语言，不能代替完整图语义或语言审核，也不证明服务 seed 可复现。

- P5+CommonPlanHead：20 案例中 0 个出现多种归一化动作结构。
- v8-no-graph+CommonPlanHead：20 案例中 0 个出现多种归一化动作结构。
  实际 v8 重复证据／状态变化案例 0/20，扰动字段变化 0/80、状态变化 0/80。
- v8-full+CommonPlanHead：20 案例中 0 个出现多种归一化动作结构。
  实际 v8 重复证据／状态变化案例 0/20，扰动字段变化 0/80、状态变化 0/80。

共享方案头采用固定有限 schema／模板流程，成功说明当前受控流水线稳定；不能据此宣称自由规划、图检索或生产故障诊断优势。20 个案例与模板存在血缘相关，扰动未人工审定，新 heldout 未消费。若人审发现语义漂移，保留当前批次并以新参考版本重新复算或另批执行。

## 历史批次与复现

`e6-full-001` 在原单并发服务只完成 27 次，另 2 次中断，已单独保存中止指纹；不混入最终分母。原生预检与独立服务预检各 3 次独立留档。最终 540 次在同一冻结代码、同一专用服务一次性运行。服务生命周期和启动参数独立记录，实验结束后仅停止本轮专用服务，原 18000 服务保留。

```bash
.venv-v8/bin/python scripts/v8_e6_full.py \
  --output runtime/v8-next/phase3/e6-new-id --workers 8 \
  --endpoint http://127.0.0.1:18002/v1
.venv-v8/bin/python scripts/v8_phase3_matrix_review.py --experiment E6 \
  --root runtime/v8-next/phase3/e6-full-002 \
  --output runtime/v8-next/phase3/e6-new-audit.json
```

运行前需按归档 service-context.json 启动同等独立服务；以上复跑命令不会自动启动服务。只读复算无需模型服务。输出均使用新 ID。

[机器汇总](../../runtime/v8-next/phase3/e6-full-002/summary.json)；[只读审计](../../runtime/v8-next/phase3/e6-full-audit-001.json)；[完整调用成本](../../runtime/v8-next/phase3/e6-full-costs-001.json)；[人工审查指导](第三阶段人工审查清单与操作指南_20261009.md)。
