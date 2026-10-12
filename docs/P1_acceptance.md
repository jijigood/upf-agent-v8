# P1 实测与阶段出口记录（2026-09-25）

本记录区分“代码和环境已备好”与“真实模型已通过”。验收快照保存在 `evidence/p1/`，对应的可重跑输出在 `runs/p1/`；包括 doctor、两个模型指纹清单、下载元数据比对报告及独立服务 smoke 输出。**P1 阶段出口 M1 已通过**；这只证明本机推理底座可用，不代表 P2–P7 的知识问答或日志诊断已实现。

| 子任务 | 当前证据 | 结论 |
|---|---|---|
| P1.1 工程与契约 | 独立项目 `upf-agent`；`config/`、`src/upf_agent/contracts.py`、CLI；9 项基础测试通过 | 已完成 |
| P1.2 硬件与 BF16 | `doctor.json` 记录 2×A100 80GB、驱动 535.183.06、Torch 2.10.0 CUDA 12.8 的 BF16 算例结果 64.0；本地代理被客户端绕过；低显存时启动保护已验证 | 已完成 |
| P1.3 基线独立服务 | vLLM 0.19.1、Transformers 5.8.0；`runs/p1/baseline-smoke.json` 记录中文文本、JSON Schema、工具调用与工具结果后的回答全部通过；四步总耗时 8,906 ms | 独立 127.0.0.1:18000 服务已实测通过；验收后正常关闭 |
| P1.4 Qwen3.8-27B | 18 个分片、51.75 GiB 权重已到齐；`target-model-hashes.json` 和 `target-hf-etag-check.json` 验证全部 18 个权重 SHA-256 与官方仓库 revision `1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0` 的本地下载元数据一致；16K/32K 的中文、JSON、工具往返、独立 `reasoning` 字段均通过；32K 服务实测 20,029 tokens 输入并找回末尾校验码 | 已完成兼容验收；默认模型仍须 P6 业务集比较后决定 |
| P1.5 检索模型 | 独立 CPU worker 已离线加载 Qwen3-Embedding-4B 与 Qwen3-Reranker-4B；`runs/p1/retrieval-smoke.json`：2560 维、L2 范数 0.9999999907、重复输入一致，相关/无关原始分数 8.0223/−13.0589 | CPU float32 路径通过；GPU BF16 性能仍待资源允许时测试 |
| P1.6 可复现配置 | 应用 `uv.lock`、推理/检索 freeze、四组模型的逐文件 SHA-256 清单及 etag/revision 比对报告已保存；两个独立环境的 `uv pip check` 通过；本机独立服务与健康/生成请求已验证 | 已完成本阶段配置锁定 |

启动保护已实际验证：`serve --model baseline --gpu 0` 返回退出码 2，提示仅有 19,253 MiB 空闲，低于 69,632 MiB 的计划阈值；`serve --model target --gpu 0` 也返回退出码 2，指出分片索引未下载完成。两种失败均未启动新服务。

共享任务释放显存后，同一基线启动命令成功加载 16 个分片，vLLM 报告权重占 56.93 GiB、KV cache 可用 10.02 GiB（109,472 tokens），最大上下文配置 16,384。服务运行时一次 `nvidia-smi` 快照显示 GPU0 已用 69,281 MiB；这是采样值，不能作为精确峰值。`baseline-smoke.json` 的四次请求均返回 HTTP 200，结构化结果及工具往返均通过。验收后对本轮自启服务发出 SIGTERM，GPU0 恢复约 81,050 MiB 空闲。

目标模型 16K 完整 smoke 见 `runs/p1/target-16k-smoke.json`（总耗时 16,551 ms）；32K 完整 smoke 见 `runs/p1/target-32k-smoke.json`（18,739 ms）。独立 `reasoning` 字段由 vLLM 0.19.1 返回，初版脚本误查 `reasoning_content` 后已修正并重测通过。32K 长上下文见 `runs/p1/target-32k-context.json`：正文 20,029 tokens，8,581 ms，返回 `UPF-CTX-7319`。目标模型加载权重占 51.1 GiB，KV cache 可用 14.18 GiB、58,016 tokens。加载预热日志有 FLA 输入形状提示；上述实际请求均通过，性能优化与业务质量留待 P6。

## 复现顺序

1. 先运行 `upf-agent doctor --probe-bf16`，确认模型资产、端口和当前显存；用 `tools/verify_model_manifest.py` 与 `tools/check_hf_etags.py` 复验已有/目标模型清单。
2. 当 GPU 空闲显存足够时，启动 `upf-agent serve --model baseline --gpu 0 --max-model-len 16384`，另开终端执行 `upf-agent smoke --model baseline`；关闭本轮服务。
3. 对 `target` 先以 16,384 启动和 smoke，再关闭后以 32,768 启动和 smoke，最后运行 `.venv-inference/bin/python tools/context_smoke.py --model-path /home/huangxiaolin/models/Qwen3.8-27B --output runs/p1/target-32k-context.json`。

显存不足时不强行启动、不终止其他用户任务。独立端口为 127.0.0.1:18000/18001，不能把其他端口上已有服务的响应当作本项目验收结果。上述两个自启服务在验收后均已关闭，GPU 已释放。人工业务评测和资料索引属于后续阶段。
