# 分离的 Python 环境

- 应用：Python 3.11，根目录 `uv.lock`，`uv sync --extra dev --python 3.11`。
- 推理：Python 3.10，`.venv-inference`；精确版本见 `inference.freeze.txt`，起始候选约束见 `inference.in`。此版本组合尚需生成模型与共享 GPU 实测。
- 检索：Python 3.11，`.venv-retrieval`；精确版本见 `retrieval.freeze.txt`，起始候选约束见 `retrieval.in`。两组真实 4B 权重的 CPU smoke 已通过。

环境都位于独立工程目录，不修改 `/home/huangxiaolin/AITO` 或已有 Dify 虚拟环境。两个环境的精确 freeze 已生成，`uv pip check` 均通过；后续仍须在干净进程复现生成服务。`*.in` 是本轮候选约束，不等于已经验证的生产锁。

当前主机驱动 535.183.06，CUDA 12.8 的基础 BF16 小算例已通过；vLLM 0.19.1 对基线和目标模型的独立服务 smoke 也已通过，包括目标模型 32K 上下文下的 20,029 tokens 请求。

在新目录从精确版本重建环境：

```bash
uv sync --extra dev --python 3.11
uv venv .venv-inference --python 3.10
uv pip install --python .venv-inference/bin/python -r environment-lock/inference.freeze.txt
uv venv .venv-retrieval --python 3.11
uv pip install --python .venv-retrieval/bin/python -r environment-lock/retrieval.freeze.txt
uv pip check --python .venv-inference/bin/python
uv pip check --python .venv-retrieval/bin/python
uv run python tools/verify_model_manifest.py evidence/p1/model-hashes.json
uv run python tools/check_hf_etags.py evidence/p1/model-hashes.json
```

这些命令需要事先缓存 wheels 或有可访问的依赖源；只有运行时才要求完全离线。`verify_model_manifest.py` 重新哈希文件，`check_hf_etags.py` 比较清单与本地 Hugging Face 元数据里的权重 SHA-256 etag 和 revision。目标模型用 `evidence/p1/target-model-hashes.json` 同样复验。

## P7 同机离线重建与恢复演练

`scripts/p7_snapshot.py` 为代码、配置、原始资料、P2/P3/P4/P5 产物、题库和运行记录生成 SHA256 清单；SQLite 使用 backup API，包含已经提交但尚未 checkpoint 的 WAL 数据。内部历史报告链接复制为普通文件并记入清单，指向工程外的链接拒绝打包。`uv.lock` 是依赖锁，必须保留；任务 `.lock`、虚拟环境、模型权重、合成容量数据和持续写入的 P7 服务日志不进入数据快照。

制作快照时暂停新查询、导入和调查任务，生成模型服务可继续运行。恢复先检查文件清单和哈希，只允许写入新目录；旧项目、原始资料和旧运行记录不被覆盖。

```bash
cd /home/huangxiaolin/upf-agent
# 每次选新的输出目录，不能复用已经存在的快照或恢复目录。
.venv/bin/python scripts/p7_snapshot.py create --root /home/huangxiaolin/upf-agent --output /home/huangxiaolin/upf-agent-delivery/my-snapshot
.venv/bin/python scripts/p7_snapshot.py verify --root /home/huangxiaolin/upf-agent-delivery/my-snapshot
.venv/bin/python scripts/p7_snapshot.py restore --root /home/huangxiaolin/upf-agent-delivery/my-snapshot --output /home/huangxiaolin/upf-agent-delivery/my-workspace
.venv/bin/python scripts/p7_isolation.py rebuild --workspace /home/huangxiaolin/upf-agent-delivery/my-workspace --output evidence/p7/my-offline-rebuild.json
.venv/bin/python scripts/p7_isolation.py validate --workspace /home/huangxiaolin/upf-agent-delivery/my-workspace --output evidence/p7/my-isolated-runtime.json
```

`rebuild` 需要本机已有 uv、缓存的 Python 3.11/3.10、精确依赖缓存、模型权重以及 bubblewrap；缺少缓存立即失败，不从网络补包。它在新建的 Linux mount/network namespace 中按锁重建三个环境并检查依赖，Dify/AITO 路径隐藏，外网无路由。此流程证明同机离线缓存重建，不等于已经提供可迁往另一台主机的 wheel/权重安装包。

`validate` 只向现有本地 18000 生成服务提供固定目的地的 Unix socket 桥接，保留服务驻留 GPU；应用及检索在隔离空间，宿主生成进程自身未被迁入网络隔离空间。测试包含手册原文引用、日志原始上下文、缺原件/缺检索环境拒绝处理和 Agent checkpoint。桥接日志或标准输出不是正式业务正确率证据，也不消费 P6 留出集。

运行报告中的 `checkpoint.paused_id` 可用于恢复演练：对测试 workspace 再制作快照、恢复到另一个新目录，执行下列命令。恢复的数据使用独立重建好的环境（以只读方式挂载），不是复制或依赖旧 Dify/AITO 环境。

```bash
.venv/bin/python scripts/p7_isolation.py validate --workspace /home/huangxiaolin/upf-agent-delivery/my-restored-workspace --environment-workspace /home/huangxiaolin/upf-agent-delivery/my-workspace --resume-id <paused_id> --output evidence/p7/my-recovery-runtime.json
```

当前配置、索引和日志 manifest 含绝对路径；namespace 将每个副本映射到原 `/home/huangxiaolin/upf-agent` 路径，并将原模型路径只读挂载。因此本轮是同机、同虚拟路径的恢复，不能直接将目录搬到任意路径后运行。遇到缺包查看 rebuild JSON；模型失败先检查 `curl --noproxy '*' http://127.0.0.1:18000/health`；资料或数据库损坏先验证 manifest，不能跳过来源校验。模型加载耗时单列，不与热服务请求耗时混用。

2026-10-07实跑的[汇总](../evidence/p7/summary.json)、[离线重建](../evidence/p7/offline_rebuild.json)、[依赖/CUDA检查](../evidence/p7/offline_environment_check.json)、[隔离运行](../evidence/p7/recovery_runtime.json)及[恢复一致性](../evidence/p7/recovery_consistency.json)均通过。实际数据快照为`/home/huangxiaolin/upf-agent-delivery/p7-20261007/runtime-snapshot`，包含5,914个文件、8份SQLite一致性备份；对应原副本`application-workspace-v2`和恢复副本`restored-workspace`均在同一交付目录。第一次`source-snapshot`遗漏依赖锁，已被`source-snapshot-v2`替代，不能用于重建。[试运行修正记录](../evidence/p7/pilot_fixes.json)保留原因。生成进程最终隔离、可转移安装包与M6独立质量验收仍待完成。
