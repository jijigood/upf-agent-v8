# E7 本地隔离实验入口

状态与结果见 [e7-lab-report.md](../../docs/v8/e7-lab-report.md)；精确上游版本见 [upstream-lock.json](upstream-lock.json)。下列旧runner用于网络生命周期和日志接入；收到复核意见后的RootCause诊断原型、预检／18轮pilot／60轮扩展及离线复算，见[修订版实验复现入口](../../docs/v8/修订版实验复现入口_20261010.md)。两种runner的分母、模型费用与结论分别登记。

宿主机需要可访问的 Docker daemon、TUN 设备；无需在宿主机安装 Open5GS/MongoDB/UERANSIM。`control.py` 只能放在专用容器的 `/control` 只读挂载中运行，**不要在宿主机调用它的注入或清理函数**。Runner 使用独立 label、名称和内部网络，拒绝清理没有本轮 label 的资源；固定子网 `10.208.7.0/24` 若与已有网络重叠，创建失败即退出，不修改现有网络。

本机已构建镜像可以直接复跑：

```bash
cd /home/huangxiaolin/upf-agent-v8
.venv-v8/bin/python scripts/v8_e7_runner.py \
  --output runtime/v8-next/wp11/e7-pilot-NEW \
  --image sha256:0298b2faf2810793b7d21ee61fd9f0189c35e22e3e3565b8dcfd615f78c04a3d
.venv-v8/bin/python scripts/v8_e7_audit.py \
  --root runtime/v8-next/wp11/e7-pilot-NEW \
  --output runtime/v8-next/wp11/e7-pilot-NEW-audit.json
```

output 必须不存在；默认固定三次重复、六条件。先健康基线，再依次注入、核验、采集、Agent 接入、清理和恢复。任何清理失败停止下一轮；正常退出／捕获到的中断回收本轮容器和网络。强制杀死进程或 Docker daemon 故障需要根据该批 `private/` 中保存的所有权记录恢复清理，不能全局删除容器或网络。

重新构建的实际输入已保存：

```bash
# 只在确认构建输入 SHA／commit 与 upstream-lock.json 一致后运行。
docker build -t upf-e7-lab:open5gs-2.7.6-ueransim-3.2.7 \
  -f lab/e7/Dockerfile runtime/v8-next/wp11/environment-001
docker image inspect upf-e7-lab:open5gs-2.7.6-ueransim-3.2.7 --format '{{.Id}}'
```

运行时用实际 image ID，不能将标签变化后的镜像冒充原冻结版本。APT 安装版本另见 `environment-001/image-packages-and-version.txt`；重建出来的 ID 可能变化，应在新批次锁定并重新验收。运行镜像包含本地上游源码以便核验；目前没有制作可对外分发的容器包。

`scripts/v8_e7_agent.py` 是 CPU 只读日志接入：捕获窗口提供明确 UTC 来源，原事件年份／时区不补写；保留每个物理行和字节范围。未知行与没有新事件的情况均保留，工具失败不能算接入通过。Agent 看不到 `private/` 中的注入命令、Gold 和健康判定。

```bash
.venv-v8/bin/pytest -q tests/test_v8_e7.py
```
