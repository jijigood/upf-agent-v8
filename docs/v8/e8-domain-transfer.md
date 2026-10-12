# E8：OpsEval 中文5G知识单选小样本迁移

日期：2026-10-10；状态：小样本读取、adapter、真实zero-shot与独立复算完成。

来源：[OpsEval官方仓库](https://github.com/NetManAIOps/OpsEval-Datasets)，commit `13e04f574c2a1c6f30005af346ef4a56402d3f2e`。下载 `data/zh/test/5G Communication.json`（SHA256 `2cb443d162a6d006ee9ae6d62da5c4a01aae67bf995c82864ea9c3030da7f96c`）、对应dev、英文同域数据以及README/LICENSE，完整版本元数据位于[源快照](../../runtime/v8-next/wp12/e8-source-001/)。

中文公开测试源有363条记录；仅选择明确qtype=0且答案为合法单选选项的记录，按ID SHA256排序取前24条。选题规则、24个问题、官方标签、驱动、模型部署在推理前冻结。英文源本轮只下载核对，没有运行英文实验，也不声明全部363题结果。

使用 Qwen3-30B-A3B-Instruct-2507，同一固定本地部署，温度0、答案JSON约束、32个输出token、4 worker。模型仅见题目及选项，无solution/官方答案，无检索、UPF工具或网络操作。方法采用README中的naive zero-shot方法族；未找到发布的评价runner，不能视为官方全量排行榜复现。

| 指标 | 实际结果 |
|---|---:|
| 真实回答 | 24 |
| 与官方选项一致 | 15 |
| exact option accuracy | 62.5% |
| 运行失败 | 0 |
| 由公开dev确定多数选项C的对照 | 8/24（33.33%） |
| 按题目选项数的均匀随机期望 | 29.51% |

[运行批次](../../runtime/v8-next/wp12/e8-opseval-pilot-002/)保留逐题request、HTTP原始response、usage、finish_reason和结果；[独立复算](../../runtime/v8-next/review-remediation-20261010/e8-audit-002.json)重新核对选题、源SHA、问题／标签一致性及响应中的原始选项，新增模型调用0。

初批 `e8-opseval-pilot-001` 的24次请求误走环境代理，均502；这属于运输请求失败，没有可核验的成功推理或token用量。原件保留，Client禁用环境代理后用002另批重跑，不覆盖失败记录。

该小样本仅用于adapter和领域知识检查，不能与UPF VPR相加、不能证明图方法迁移收益或总体领先，模型训练重叠未知。真实领域问答数据不标synthetic；本轮UPF正式heldout消费为0。LICENSE文件MIT与README frontmatter Apache-2.0声明不一致，原文分别保存；作为本地私有真实附件处理，不加入公开合成分发候选包。
