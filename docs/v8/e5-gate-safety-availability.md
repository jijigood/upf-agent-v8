# E5 安全与可用性：实际分层门控完整开发控制

2026-10-09。120 候选／720 判定已完成并只读复算；标签未独立审定，VPR 为 null、分母 0。

## 完整同候选控制

允许／禁止／未知各 40；7 个任务规格、N4/N3/手册 3 模板，均来自一条 example fixture 血缘。不是 120 个独立事故。候选含身份、接口、适用 K 的配置检查、双侧 P、依赖与有限未知出口。20 种禁止注入覆盖 schema、K/R/P 源／版本／适用性、scope／peer／字段权限、DAG／前置条件／完成声明；10 种未知覆盖 R 字段缺失/null、K 缺失、P 映射缺失。所有标签和物理来源在评价前保存。

每个候选分别实际运行 A0–A4，共 600 个 Gate 调用；每层独立进入实际组件，不由一次完整诊断投影得出。另有 120 次全拒绝对照。A0 原始候选，A1 IR／动作 schema，A2 KRP／来源及适用性，A3 权限／context，A4 DAG／前置条件／未知出口。通用转写是共同准备步骤；A0 不启用 Gate。

## 结果

| 组 | 违规建议错误允许/40 | 合法保留/40 | 正确转人工/40 |
|---|---:|---:|---:|
| A0 | 40 | 40 | 0 |
| A1 | 32 | 40 | 0 |
| A2 | 16 | 40 | 0 |
| A3 | 8 | 40 | 0 |
| A4 | 0 | 40 | 40 |
| reject-all | 0 | 0 | 0 |

A4 错误拒绝 0/40，违规错误允许 0/40。作为样本描述，0/40 的双侧 Wilson95 上界为 8.76%；这些相关开发样本不满足独立总体抽样，不能用此区间承诺现网风险。全拒绝的合法保留和正确转人工均为 0，明确不通过可用性。

## 验证与权限

- [完整结果](../../runtime/v8-next/phase3/e5-full-002/summary.json)、[逐候选判定](../../runtime/v8-next/phase3/e5-full-002/decisions.json)、[只读复算](../../runtime/v8-next/phase3/e5-full-audit-001.json)：核验 1,080 输入、600 实际门控、2,742 来源引用检查。
- `max_stage` 默认 4，已有完整 Validator 行为与旧冻结模块一致；旧正式流程仍采用默认完整路径。部分层永不发布方案，所有 `execute_authorized=false`，未执行候选、未写网络。
- 53 个旧 E5 控制及新增完整来源/出口/组件进入/历史兼容回归通过；最终全部回归 893 项通过。
- A0–A4 原始耗时单列保存；此小开发矩阵没有为微秒级差异做重复、交替、冷热性能实验，不能宣称线上延迟因果效果。独立审定后才能关联方案 VPR/CDR 与自然语言盲评。

## 复跑入口

```bash
cd /home/huangxiaolin/upf-agent-v8
.venv-v8/bin/python scripts/v8_e5_full.py --output runtime/v8-next/phase3/e5-new-id
.venv-v8/bin/python scripts/v8_phase3_matrix_review.py --experiment E5 --root runtime/v8-next/phase3/e5-full-002 --output runtime/v8-next/phase3/e5-new-audit.json
```

每次使用新 ID；[总计划](../../plan.md)保留工程完成与正式人工质量审定两个状态。
