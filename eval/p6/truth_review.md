# P6 业务真值复核单

120 题候选，开发/保留各 60；全部为助手草案，不是已审核业务真值。
原文抽取通过不能代替题目的相关性、完整性和现场适用性。
逐题勾选并写复核人/日期；必要时修改问题、证据集合与预期事实。近义问法归同一来源组，禁止跨组泄漏。
日志原文补充定位见 [source_references.json](source_references.json)。
保留集在配置冻结前不执行推理；下面仅显示资料与拟定真值，便于人工复核。

## command-001 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：在‘检查upf 业务网络地址配置 / 检查所有接口地址’中，show 命令的原文写法是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-5c4b984cb9fb9b794139, command-family:show
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1055], word/document.xml/body/p[1056], word/document.xml/body/p[1057], word/document.xml/body/p[1058], word/document.xml/body/p[1059], word/document.xml/body/p[1060], word/document.xml/body/p[1061] · `chunk-611060638cb88f44e6bbdfc9`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
检查所有接口地址
方法1、使用脚本查询
# upfmgr ip qry
方法2、使用curll命令查询
# curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: `kubectl get ingress -A |grep "HOSTS\|nma"| awk '{for(i=1;i<=NF;i++){if($i=="HOSTS") {getline;print $i;}}}'`" -X POST -d '{QRY UpfIntfAddrConfig;}' 127.0.0.1
方法3、使用telnet登录UPFD POD 37100端口查询
# upfmgr ctrl
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1062] · `chunk-b586b6d6c78e913d75bfa0b2`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1063] · `chunk-e2c3df09d389081631789e9d`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
其中方法3的查询截图如下：
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```

## command-002 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：请引用‘检查upf 业务网络地址配置 / 检查所有接口地址’中的命令 show config，保留占位符和参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-5c4b984cb9fb9b794139, command-family:show
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1055], word/document.xml/body/p[1056], word/document.xml/body/p[1057], word/document.xml/body/p[1058], word/document.xml/body/p[1059], word/document.xml/body/p[1060], word/document.xml/body/p[1061] · `chunk-611060638cb88f44e6bbdfc9`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
检查所有接口地址
方法1、使用脚本查询
# upfmgr ip qry
方法2、使用curll命令查询
# curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: `kubectl get ingress -A |grep "HOSTS\|nma"| awk '{for(i=1;i<=NF;i++){if($i=="HOSTS") {getline;print $i;}}}'`" -X POST -d '{QRY UpfIntfAddrConfig;}' 127.0.0.1
方法3、使用telnet登录UPFD POD 37100端口查询
# upfmgr ctrl
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1062] · `chunk-b586b6d6c78e913d75bfa0b2`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1063] · `chunk-e2c3df09d389081631789e9d`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
其中方法3的查询截图如下：
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```

## command-003 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：手册‘检查upf 业务网络地址配置 / 检查所有接口地址’如何使用 show？只摘录原文并说明示例适用范围。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-5c4b984cb9fb9b794139, command-family:show
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1055], word/document.xml/body/p[1056], word/document.xml/body/p[1057], word/document.xml/body/p[1058], word/document.xml/body/p[1059], word/document.xml/body/p[1060], word/document.xml/body/p[1061] · `chunk-611060638cb88f44e6bbdfc9`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
检查所有接口地址
方法1、使用脚本查询
# upfmgr ip qry
方法2、使用curll命令查询
# curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: `kubectl get ingress -A |grep "HOSTS\|nma"| awk '{for(i=1;i<=NF;i++){if($i=="HOSTS") {getline;print $i;}}}'`" -X POST -d '{QRY UpfIntfAddrConfig;}' 127.0.0.1
方法3、使用telnet登录UPFD POD 37100端口查询
# upfmgr ctrl
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1062] · `chunk-b586b6d6c78e913d75bfa0b2`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1063] · `chunk-e2c3df09d389081631789e9d`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
其中方法3的查询截图如下：
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```

## command-004 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：核对 show config 在‘检查upf 业务网络地址配置 / 检查所有接口地址’中的原始语法，不把示例当现场参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-5c4b984cb9fb9b794139, command-family:show
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1055], word/document.xml/body/p[1056], word/document.xml/body/p[1057], word/document.xml/body/p[1058], word/document.xml/body/p[1059], word/document.xml/body/p[1060], word/document.xml/body/p[1061] · `chunk-611060638cb88f44e6bbdfc9`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
检查所有接口地址
方法1、使用脚本查询
# upfmgr ip qry
方法2、使用curll命令查询
# curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: `kubectl get ingress -A |grep "HOSTS\|nma"| awk '{for(i=1;i<=NF;i++){if($i=="HOSTS") {getline;print $i;}}}'`" -X POST -d '{QRY UpfIntfAddrConfig;}' 127.0.0.1
方法3、使用telnet登录UPFD POD 37100端口查询
# upfmgr ctrl
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1062] · `chunk-b586b6d6c78e913d75bfa0b2`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1063] · `chunk-e2c3df09d389081631789e9d`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
其中方法3的查询截图如下：
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```

## command-005 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：在‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’中，upfmgr 命令的原文写法是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-4074dc47431e95e1d96d, command-family:upfmgr
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1087], word/document.xml/body/p[1088], word/document.xml/body/p[1089], word/document.xml/body/p[1090], word/document.xml/body/p[1091] · `chunk-c47de373b7bf531a3080853d`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
检查N3N6接口及IP配置
查看N3 N6 网口配置，需要访问upfd pod中的vpp CLI 命令行界面。
首先进入upfd pod中
直接使用脚本
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1092] · `chunk-5f39f6e176cd5d50da043a23`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1093], word/document.xml/body/p[1094], word/document.xml/body/p[1095] · `chunk-a3845a8d6d582d25a6c91232`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
或使用kubectl命令进入pod，并在pod中执行vppctl命令
# kubectl exec -it -n ns1 upfd-1-594847d77d-7pblh -- './vppctl'
查看VPP接口地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1096] · `chunk-7186a25131ec3f73b59889b5`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface addr
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1097], word/document.xml/body/p[1098], word/document.xml/body/p[1099], word/document.xml/body/p[1100], word/document.xml/body/p[1101], word/document.xml/body/p[1102], word/document.xml/body/p[1103], word/document.xml/body/p[1104], word/document.xml/body/p[1105], word/document.xml/body/p[1106], word/document.xml/body/p[1107], word/document.xml/body/p[1108], word/document.xml/body/p[1110] · `chunk-27ef72ccf4b8d59bfc1dffa3`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
BondEthernet0 (up):
  L3 100.10.1.50/24
  L3 2303::3:50/64
BondEthernet1 (up):
  L3 174.100.100.50/24
  L3 2606::6:50/64
local0 (dn):
port17/0/0 (up):
port17/0/1 (up):
port4b/0/0 (up):
port4b/0/1 (up):
示例输出截图：
在vpp中测试业务地址连通性，该地址为交换机上的网关地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1111] · `chunk-8424f0e01f9e2107b966e55a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 100.10.1.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1112] · `chunk-cf3d3bb155ff05c4e0809464`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 174.100.100.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1113], word/document.xml/body/p[1114] · `chunk-ee7cc9ff13c00222dee84783`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
如果能够ping通说明基本网络连通性正常。否则需要依次检查VPP配置，CNI配置，及交换机配置信息，核对vlan、IP及接口是否存在配置错误。
查看vpp接口信息
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1115] · `chunk-a8f5ff09d0cf29498ce8c9d0`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1116], word/document.xml/body/p[1118], word/document.xml/body/p[1119], word/document.xml/body/p[1120] · `chunk-2b204cd7383c816b26ba3e86`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果：
说明：
输出结果显示vpp内有4个接口，对应4个物理网卡，其中两两做Bonding，网卡接口名称由物理网卡PCI地址编号进行命名。两个接口对应哪个物理网卡在config.yml配置文件中已经提前定义。
另外可以通过查看接口详细信息中的PCI地址来确认接口属于哪块物理网卡，执行以下vpp命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1121] · `chunk-4065867d9b809a1a9ef3d21b`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show hardware-interfaces port17/0/0
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1122], word/document.xml/body/p[1124], word/document.xml/body/p[1125], word/document.xml/body/p[1126], word/document.xml/body/p[1127], word/document.xml/body/p[1128], word/document.xml/body/p[1129] · `chunk-1ba82874b94598161727769f`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果
获取VPP接口pci地址后，由于主机网卡已经转移到用户态，使用ip link show命令无法显示，但网卡名称与PCI地址对应关系已在bind前记录到临时文件dpdk-devinfo-nic种，通过查看该临时文件同样可以确认VPP接口与主机物理网卡之间映射关系。
# cat /home/upf_setup_CU5GC_UPF_5.0.210/integration/temp/dpdk-devinfo-nic
ens1f0 0000:4b:00.0 port4b/0/0
ens3f0 0000:17:00.0 port17/0/0
ens1f1 0000:4b:00.1 port4b/0/1
ens3f1 0000:17:00.1 port17/0/1
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```

## command-006 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：请引用‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’中的命令 upfmgr data，保留占位符和参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-4074dc47431e95e1d96d, command-family:upfmgr
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1087], word/document.xml/body/p[1088], word/document.xml/body/p[1089], word/document.xml/body/p[1090], word/document.xml/body/p[1091] · `chunk-c47de373b7bf531a3080853d`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
检查N3N6接口及IP配置
查看N3 N6 网口配置，需要访问upfd pod中的vpp CLI 命令行界面。
首先进入upfd pod中
直接使用脚本
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1092] · `chunk-5f39f6e176cd5d50da043a23`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1093], word/document.xml/body/p[1094], word/document.xml/body/p[1095] · `chunk-a3845a8d6d582d25a6c91232`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
或使用kubectl命令进入pod，并在pod中执行vppctl命令
# kubectl exec -it -n ns1 upfd-1-594847d77d-7pblh -- './vppctl'
查看VPP接口地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1096] · `chunk-7186a25131ec3f73b59889b5`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface addr
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1097], word/document.xml/body/p[1098], word/document.xml/body/p[1099], word/document.xml/body/p[1100], word/document.xml/body/p[1101], word/document.xml/body/p[1102], word/document.xml/body/p[1103], word/document.xml/body/p[1104], word/document.xml/body/p[1105], word/document.xml/body/p[1106], word/document.xml/body/p[1107], word/document.xml/body/p[1108], word/document.xml/body/p[1110] · `chunk-27ef72ccf4b8d59bfc1dffa3`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
BondEthernet0 (up):
  L3 100.10.1.50/24
  L3 2303::3:50/64
BondEthernet1 (up):
  L3 174.100.100.50/24
  L3 2606::6:50/64
local0 (dn):
port17/0/0 (up):
port17/0/1 (up):
port4b/0/0 (up):
port4b/0/1 (up):
示例输出截图：
在vpp中测试业务地址连通性，该地址为交换机上的网关地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1111] · `chunk-8424f0e01f9e2107b966e55a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 100.10.1.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1112] · `chunk-cf3d3bb155ff05c4e0809464`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 174.100.100.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1113], word/document.xml/body/p[1114] · `chunk-ee7cc9ff13c00222dee84783`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
如果能够ping通说明基本网络连通性正常。否则需要依次检查VPP配置，CNI配置，及交换机配置信息，核对vlan、IP及接口是否存在配置错误。
查看vpp接口信息
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1115] · `chunk-a8f5ff09d0cf29498ce8c9d0`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1116], word/document.xml/body/p[1118], word/document.xml/body/p[1119], word/document.xml/body/p[1120] · `chunk-2b204cd7383c816b26ba3e86`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果：
说明：
输出结果显示vpp内有4个接口，对应4个物理网卡，其中两两做Bonding，网卡接口名称由物理网卡PCI地址编号进行命名。两个接口对应哪个物理网卡在config.yml配置文件中已经提前定义。
另外可以通过查看接口详细信息中的PCI地址来确认接口属于哪块物理网卡，执行以下vpp命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1121] · `chunk-4065867d9b809a1a9ef3d21b`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show hardware-interfaces port17/0/0
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1122], word/document.xml/body/p[1124], word/document.xml/body/p[1125], word/document.xml/body/p[1126], word/document.xml/body/p[1127], word/document.xml/body/p[1128], word/document.xml/body/p[1129] · `chunk-1ba82874b94598161727769f`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果
获取VPP接口pci地址后，由于主机网卡已经转移到用户态，使用ip link show命令无法显示，但网卡名称与PCI地址对应关系已在bind前记录到临时文件dpdk-devinfo-nic种，通过查看该临时文件同样可以确认VPP接口与主机物理网卡之间映射关系。
# cat /home/upf_setup_CU5GC_UPF_5.0.210/integration/temp/dpdk-devinfo-nic
ens1f0 0000:4b:00.0 port4b/0/0
ens3f0 0000:17:00.0 port17/0/0
ens1f1 0000:4b:00.1 port4b/0/1
ens3f1 0000:17:00.1 port17/0/1
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```

## command-007 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：手册‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’如何使用 upfmgr？只摘录原文并说明示例适用范围。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-4074dc47431e95e1d96d, command-family:upfmgr
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1087], word/document.xml/body/p[1088], word/document.xml/body/p[1089], word/document.xml/body/p[1090], word/document.xml/body/p[1091] · `chunk-c47de373b7bf531a3080853d`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
检查N3N6接口及IP配置
查看N3 N6 网口配置，需要访问upfd pod中的vpp CLI 命令行界面。
首先进入upfd pod中
直接使用脚本
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1092] · `chunk-5f39f6e176cd5d50da043a23`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1093], word/document.xml/body/p[1094], word/document.xml/body/p[1095] · `chunk-a3845a8d6d582d25a6c91232`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
或使用kubectl命令进入pod，并在pod中执行vppctl命令
# kubectl exec -it -n ns1 upfd-1-594847d77d-7pblh -- './vppctl'
查看VPP接口地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1096] · `chunk-7186a25131ec3f73b59889b5`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface addr
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1097], word/document.xml/body/p[1098], word/document.xml/body/p[1099], word/document.xml/body/p[1100], word/document.xml/body/p[1101], word/document.xml/body/p[1102], word/document.xml/body/p[1103], word/document.xml/body/p[1104], word/document.xml/body/p[1105], word/document.xml/body/p[1106], word/document.xml/body/p[1107], word/document.xml/body/p[1108], word/document.xml/body/p[1110] · `chunk-27ef72ccf4b8d59bfc1dffa3`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
BondEthernet0 (up):
  L3 100.10.1.50/24
  L3 2303::3:50/64
BondEthernet1 (up):
  L3 174.100.100.50/24
  L3 2606::6:50/64
local0 (dn):
port17/0/0 (up):
port17/0/1 (up):
port4b/0/0 (up):
port4b/0/1 (up):
示例输出截图：
在vpp中测试业务地址连通性，该地址为交换机上的网关地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1111] · `chunk-8424f0e01f9e2107b966e55a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 100.10.1.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1112] · `chunk-cf3d3bb155ff05c4e0809464`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 174.100.100.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1113], word/document.xml/body/p[1114] · `chunk-ee7cc9ff13c00222dee84783`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
如果能够ping通说明基本网络连通性正常。否则需要依次检查VPP配置，CNI配置，及交换机配置信息，核对vlan、IP及接口是否存在配置错误。
查看vpp接口信息
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1115] · `chunk-a8f5ff09d0cf29498ce8c9d0`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1116], word/document.xml/body/p[1118], word/document.xml/body/p[1119], word/document.xml/body/p[1120] · `chunk-2b204cd7383c816b26ba3e86`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果：
说明：
输出结果显示vpp内有4个接口，对应4个物理网卡，其中两两做Bonding，网卡接口名称由物理网卡PCI地址编号进行命名。两个接口对应哪个物理网卡在config.yml配置文件中已经提前定义。
另外可以通过查看接口详细信息中的PCI地址来确认接口属于哪块物理网卡，执行以下vpp命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1121] · `chunk-4065867d9b809a1a9ef3d21b`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show hardware-interfaces port17/0/0
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1122], word/document.xml/body/p[1124], word/document.xml/body/p[1125], word/document.xml/body/p[1126], word/document.xml/body/p[1127], word/document.xml/body/p[1128], word/document.xml/body/p[1129] · `chunk-1ba82874b94598161727769f`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果
获取VPP接口pci地址后，由于主机网卡已经转移到用户态，使用ip link show命令无法显示，但网卡名称与PCI地址对应关系已在bind前记录到临时文件dpdk-devinfo-nic种，通过查看该临时文件同样可以确认VPP接口与主机物理网卡之间映射关系。
# cat /home/upf_setup_CU5GC_UPF_5.0.210/integration/temp/dpdk-devinfo-nic
ens1f0 0000:4b:00.0 port4b/0/0
ens3f0 0000:17:00.0 port17/0/0
ens1f1 0000:4b:00.1 port4b/0/1
ens3f1 0000:17:00.1 port17/0/1
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```

## command-008 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：核对 upfmgr data 在‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’中的原始语法，不把示例当现场参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-4074dc47431e95e1d96d, command-family:upfmgr
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1087], word/document.xml/body/p[1088], word/document.xml/body/p[1089], word/document.xml/body/p[1090], word/document.xml/body/p[1091] · `chunk-c47de373b7bf531a3080853d`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
检查N3N6接口及IP配置
查看N3 N6 网口配置，需要访问upfd pod中的vpp CLI 命令行界面。
首先进入upfd pod中
直接使用脚本
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1092] · `chunk-5f39f6e176cd5d50da043a23`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1093], word/document.xml/body/p[1094], word/document.xml/body/p[1095] · `chunk-a3845a8d6d582d25a6c91232`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
或使用kubectl命令进入pod，并在pod中执行vppctl命令
# kubectl exec -it -n ns1 upfd-1-594847d77d-7pblh -- './vppctl'
查看VPP接口地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1096] · `chunk-7186a25131ec3f73b59889b5`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface addr
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1097], word/document.xml/body/p[1098], word/document.xml/body/p[1099], word/document.xml/body/p[1100], word/document.xml/body/p[1101], word/document.xml/body/p[1102], word/document.xml/body/p[1103], word/document.xml/body/p[1104], word/document.xml/body/p[1105], word/document.xml/body/p[1106], word/document.xml/body/p[1107], word/document.xml/body/p[1108], word/document.xml/body/p[1110] · `chunk-27ef72ccf4b8d59bfc1dffa3`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
BondEthernet0 (up):
  L3 100.10.1.50/24
  L3 2303::3:50/64
BondEthernet1 (up):
  L3 174.100.100.50/24
  L3 2606::6:50/64
local0 (dn):
port17/0/0 (up):
port17/0/1 (up):
port4b/0/0 (up):
port4b/0/1 (up):
示例输出截图：
在vpp中测试业务地址连通性，该地址为交换机上的网关地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1111] · `chunk-8424f0e01f9e2107b966e55a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 100.10.1.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1112] · `chunk-cf3d3bb155ff05c4e0809464`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 174.100.100.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1113], word/document.xml/body/p[1114] · `chunk-ee7cc9ff13c00222dee84783`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
如果能够ping通说明基本网络连通性正常。否则需要依次检查VPP配置，CNI配置，及交换机配置信息，核对vlan、IP及接口是否存在配置错误。
查看vpp接口信息
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1115] · `chunk-a8f5ff09d0cf29498ce8c9d0`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1116], word/document.xml/body/p[1118], word/document.xml/body/p[1119], word/document.xml/body/p[1120] · `chunk-2b204cd7383c816b26ba3e86`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果：
说明：
输出结果显示vpp内有4个接口，对应4个物理网卡，其中两两做Bonding，网卡接口名称由物理网卡PCI地址编号进行命名。两个接口对应哪个物理网卡在config.yml配置文件中已经提前定义。
另外可以通过查看接口详细信息中的PCI地址来确认接口属于哪块物理网卡，执行以下vpp命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1121] · `chunk-4065867d9b809a1a9ef3d21b`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show hardware-interfaces port17/0/0
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1122], word/document.xml/body/p[1124], word/document.xml/body/p[1125], word/document.xml/body/p[1126], word/document.xml/body/p[1127], word/document.xml/body/p[1128], word/document.xml/body/p[1129] · `chunk-1ba82874b94598161727769f`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果
获取VPP接口pci地址后，由于主机网卡已经转移到用户态，使用ip link show命令无法显示，但网卡名称与PCI地址对应关系已在bind前记录到临时文件dpdk-devinfo-nic种，通过查看该临时文件同样可以确认VPP接口与主机物理网卡之间映射关系。
# cat /home/upf_setup_CU5GC_UPF_5.0.210/integration/temp/dpdk-devinfo-nic
ens1f0 0000:4b:00.0 port4b/0/0
ens3f0 0000:17:00.0 port17/0/0
ens1f1 0000:4b:00.1 port4b/0/1
ens3f1 0000:17:00.1 port17/0/1
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```

## command-009 · dev · command

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘UPF系统能力 / 功能配置’中，set-upf-prt-sw 命令的原文写法是什么？
- 结论：不通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：p[177]实际仅一行'set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>'(txbx为空)；证据块/预期多出一行'相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4'，但'相关说明'四字在手册段落与表格全文均不存在，示例命令实际位于p[183](其上文p[182]为'举例：')，属拼接/抽词错误
- 分组：section-93a4864c8a3b2c42c793, command-family:set-upf-prt-sw
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[168], word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172], word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[176] · `chunk-05b46622548cea41921ec8c4`
```text
CLI配置命令 / UPF系统能力 / 功能配置
功能配置
操作步骤
登录UPF物理机，打开终端；
终端键入命令：telnet 0 37100；
进入upfd调试台，输入命令；
UPF上 show config 可以确认配置成功。
命令格式
upf日志打印级别设置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[177] · `chunk-ed162186f81b734c927091f0`
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[178], word/document.xml/body/p[179], word/document.xml/body/p[180], word/document.xml/body/p[182] · `chunk-21b601c9353349f7eb3ab15c`
```text
CLI配置命令 / UPF系统能力 / 功能配置
说明：
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；
gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。
举例：
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[183] · `chunk-5508ad2ffaa25a9c28d1634f`
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[184] · `chunk-4810f364c95856d4a4b9902f`
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> show config
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[185], word/document.xml/body/p[186], word/document.xml/body/p[187], word/document.xml/body/p[188], word/document.xml/body/p[189], word/document.xml/body/p[190] · `chunk-e2ca5f2a07d7228d2bb32d91`
```text
CLI配置命令 / UPF系统能力 / 功能配置
Upf Print Switch List:
             Media Print Swtich :  1  
    Media log file Print Swtich :  1  
                N4 Print Swtich :  4  <<< upf信令面log level
       N4 log file Print Swtich :  1  
              Rule Print Swtich :  1  
```
- 预期原文/缺口：
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```

## command-010 · dev · command

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘UPF系统能力 / 功能配置’中的命令 set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>，保留占位符和参数。
- 结论：不通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：同command-009证据组；p[177]仅有命令格式行，证据块多出的'相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4'在原文中无对应行，示例实际在p[183]，'相关说明'标签系杜撰
- 分组：section-93a4864c8a3b2c42c793, command-family:set-upf-prt-sw
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[168], word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172], word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[176] · `chunk-05b46622548cea41921ec8c4`
```text
CLI配置命令 / UPF系统能力 / 功能配置
功能配置
操作步骤
登录UPF物理机，打开终端；
终端键入命令：telnet 0 37100；
进入upfd调试台，输入命令；
UPF上 show config 可以确认配置成功。
命令格式
upf日志打印级别设置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[177] · `chunk-ed162186f81b734c927091f0`
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[178], word/document.xml/body/p[179], word/document.xml/body/p[180], word/document.xml/body/p[182] · `chunk-21b601c9353349f7eb3ab15c`
```text
CLI配置命令 / UPF系统能力 / 功能配置
说明：
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；
gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。
举例：
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[183] · `chunk-5508ad2ffaa25a9c28d1634f`
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[184] · `chunk-4810f364c95856d4a4b9902f`
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> show config
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[185], word/document.xml/body/p[186], word/document.xml/body/p[187], word/document.xml/body/p[188], word/document.xml/body/p[189], word/document.xml/body/p[190] · `chunk-e2ca5f2a07d7228d2bb32d91`
```text
CLI配置命令 / UPF系统能力 / 功能配置
Upf Print Switch List:
             Media Print Swtich :  1  
    Media log file Print Swtich :  1  
                N4 Print Swtich :  4  <<< upf信令面log level
       N4 log file Print Swtich :  1  
              Rule Print Swtich :  1  
```
- 预期原文/缺口：
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```

## command-011 · dev · command

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘UPF系统能力 / 功能配置’如何使用 set-upf-prt-sw？只摘录原文并说明示例适用范围。
- 结论：不通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：同command-009证据组；命令格式行本身(p[177])正确，但证据块把p[183]的示例冠以杜撰的'相关说明：'标签并入p[177]块，与原文不符
- 分组：section-93a4864c8a3b2c42c793, command-family:set-upf-prt-sw
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[168], word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172], word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[176] · `chunk-05b46622548cea41921ec8c4`
```text
CLI配置命令 / UPF系统能力 / 功能配置
功能配置
操作步骤
登录UPF物理机，打开终端；
终端键入命令：telnet 0 37100；
进入upfd调试台，输入命令；
UPF上 show config 可以确认配置成功。
命令格式
upf日志打印级别设置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[177] · `chunk-ed162186f81b734c927091f0`
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[178], word/document.xml/body/p[179], word/document.xml/body/p[180], word/document.xml/body/p[182] · `chunk-21b601c9353349f7eb3ab15c`
```text
CLI配置命令 / UPF系统能力 / 功能配置
说明：
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；
gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。
举例：
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[183] · `chunk-5508ad2ffaa25a9c28d1634f`
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[184] · `chunk-4810f364c95856d4a4b9902f`
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> show config
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[185], word/document.xml/body/p[186], word/document.xml/body/p[187], word/document.xml/body/p[188], word/document.xml/body/p[189], word/document.xml/body/p[190] · `chunk-e2ca5f2a07d7228d2bb32d91`
```text
CLI配置命令 / UPF系统能力 / 功能配置
Upf Print Switch List:
             Media Print Swtich :  1  
    Media log file Print Swtich :  1  
                N4 Print Swtich :  4  <<< upf信令面log level
       N4 log file Print Swtich :  1  
              Rule Print Swtich :  1  
```
- 预期原文/缺口：
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```

## command-012 · dev · command

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4> 在‘UPF系统能力 / 功能配置’中的原始语法，不把示例当现场参数。
- 结论：不通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：同command-009证据组；预期第二行'相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4'无法在原文逐字找到('相关说明'全文无)，示例在p[183]，属抽词/拼接错误
- 分组：section-93a4864c8a3b2c42c793, command-family:set-upf-prt-sw
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[168], word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172], word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[176] · `chunk-05b46622548cea41921ec8c4`
```text
CLI配置命令 / UPF系统能力 / 功能配置
功能配置
操作步骤
登录UPF物理机，打开终端；
终端键入命令：telnet 0 37100；
进入upfd调试台，输入命令；
UPF上 show config 可以确认配置成功。
命令格式
upf日志打印级别设置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[177] · `chunk-ed162186f81b734c927091f0`
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[178], word/document.xml/body/p[179], word/document.xml/body/p[180], word/document.xml/body/p[182] · `chunk-21b601c9353349f7eb3ab15c`
```text
CLI配置命令 / UPF系统能力 / 功能配置
说明：
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；
gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。
举例：
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[183] · `chunk-5508ad2ffaa25a9c28d1634f`
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[184] · `chunk-4810f364c95856d4a4b9902f`
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> show config
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[185], word/document.xml/body/p[186], word/document.xml/body/p[187], word/document.xml/body/p[188], word/document.xml/body/p[189], word/document.xml/body/p[190] · `chunk-e2ca5f2a07d7228d2bb32d91`
```text
CLI配置命令 / UPF系统能力 / 功能配置
Upf Print Switch List:
             Media Print Swtich :  1  
    Media log file Print Swtich :  1  
                N4 Print Swtich :  4  <<< upf信令面log level
       N4 log file Print Swtich :  1  
              Rule Print Swtich :  1  
```
- 预期原文/缺口：
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```

## command-013 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：在‘配置UPF物理机 / Coredump开关打开’中，echo 命令的原文写法是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-279f5f812451d0bbf03e, command-family:echo
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[378], word/document.xml/body/p[379] · `chunk-041c2988010a54673b562f26`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
Coredump开关打开
复制并输入如下命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[380] · `chunk-da1f7676d2f30661bb5e00a8`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
mkdir -p /opt/local/tmp/core
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[382] · `chunk-da087bcb96a5e8d605b2107f`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/security/limits.d/coredump.conf<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[383], word/document.xml/body/p[384], word/document.xml/body/p[385] · `chunk-97617917b877529323000733`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
* soft core unlimited
* hard core unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[387] · `chunk-01998c8695e66a6318101bb8`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[388] · `chunk-b7e7f004b9f94894131191dc`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[390] · `chunk-41d54d63a03ea2658cf62b77`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/profile.d/coredump.sh<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[391], word/document.xml/body/p[392], word/document.xml/body/p[393] · `chunk-08f63c658d0f9d9de2335551`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
#!/bin/sh
ulimit -S -c unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[395] · `chunk-3c63be79228c38487b673dea`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
source /etc/profile
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[396], word/document.xml/body/p[397], word/document.xml/body/p[398] · `chunk-3ecddf27a8093a17064a1a8a`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
查看coredump开关是否打开，键入如下命令：
$ ulimit -a
若输出如下配置，表示coredump开关已打开
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```

## command-014 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：请引用‘配置UPF物理机 / Coredump开关打开’中的命令 echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern，保留占位符和参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-279f5f812451d0bbf03e, command-family:echo
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[378], word/document.xml/body/p[379] · `chunk-041c2988010a54673b562f26`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
Coredump开关打开
复制并输入如下命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[380] · `chunk-da1f7676d2f30661bb5e00a8`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
mkdir -p /opt/local/tmp/core
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[382] · `chunk-da087bcb96a5e8d605b2107f`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/security/limits.d/coredump.conf<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[383], word/document.xml/body/p[384], word/document.xml/body/p[385] · `chunk-97617917b877529323000733`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
* soft core unlimited
* hard core unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[387] · `chunk-01998c8695e66a6318101bb8`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[388] · `chunk-b7e7f004b9f94894131191dc`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[390] · `chunk-41d54d63a03ea2658cf62b77`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/profile.d/coredump.sh<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[391], word/document.xml/body/p[392], word/document.xml/body/p[393] · `chunk-08f63c658d0f9d9de2335551`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
#!/bin/sh
ulimit -S -c unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[395] · `chunk-3c63be79228c38487b673dea`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
source /etc/profile
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[396], word/document.xml/body/p[397], word/document.xml/body/p[398] · `chunk-3ecddf27a8093a17064a1a8a`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
查看coredump开关是否打开，键入如下命令：
$ ulimit -a
若输出如下配置，表示coredump开关已打开
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```

## command-015 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：手册‘配置UPF物理机 / Coredump开关打开’如何使用 echo？只摘录原文并说明示例适用范围。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-279f5f812451d0bbf03e, command-family:echo
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[378], word/document.xml/body/p[379] · `chunk-041c2988010a54673b562f26`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
Coredump开关打开
复制并输入如下命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[380] · `chunk-da1f7676d2f30661bb5e00a8`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
mkdir -p /opt/local/tmp/core
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[382] · `chunk-da087bcb96a5e8d605b2107f`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/security/limits.d/coredump.conf<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[383], word/document.xml/body/p[384], word/document.xml/body/p[385] · `chunk-97617917b877529323000733`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
* soft core unlimited
* hard core unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[387] · `chunk-01998c8695e66a6318101bb8`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[388] · `chunk-b7e7f004b9f94894131191dc`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[390] · `chunk-41d54d63a03ea2658cf62b77`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/profile.d/coredump.sh<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[391], word/document.xml/body/p[392], word/document.xml/body/p[393] · `chunk-08f63c658d0f9d9de2335551`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
#!/bin/sh
ulimit -S -c unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[395] · `chunk-3c63be79228c38487b673dea`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
source /etc/profile
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[396], word/document.xml/body/p[397], word/document.xml/body/p[398] · `chunk-3ecddf27a8093a17064a1a8a`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
查看coredump开关是否打开，键入如下命令：
$ ulimit -a
若输出如下配置，表示coredump开关已打开
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```

## command-016 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：核对 echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern 在‘配置UPF物理机 / Coredump开关打开’中的原始语法，不把示例当现场参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-279f5f812451d0bbf03e, command-family:echo
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[378], word/document.xml/body/p[379] · `chunk-041c2988010a54673b562f26`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
Coredump开关打开
复制并输入如下命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[380] · `chunk-da1f7676d2f30661bb5e00a8`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
mkdir -p /opt/local/tmp/core
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[382] · `chunk-da087bcb96a5e8d605b2107f`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/security/limits.d/coredump.conf<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[383], word/document.xml/body/p[384], word/document.xml/body/p[385] · `chunk-97617917b877529323000733`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
* soft core unlimited
* hard core unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[387] · `chunk-01998c8695e66a6318101bb8`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[388] · `chunk-b7e7f004b9f94894131191dc`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[390] · `chunk-41d54d63a03ea2658cf62b77`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/profile.d/coredump.sh<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[391], word/document.xml/body/p[392], word/document.xml/body/p[393] · `chunk-08f63c658d0f9d9de2335551`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
#!/bin/sh
ulimit -S -c unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[395] · `chunk-3c63be79228c38487b673dea`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
source /etc/profile
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[396], word/document.xml/body/p[397], word/document.xml/body/p[398] · `chunk-3ecddf27a8093a17064a1a8a`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
查看coredump开关是否打开，键入如下命令：
$ ulimit -a
若输出如下配置，表示coredump开关已打开
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```

## command-017 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：在‘逻辑口报文信息统计 / 统计N4口报文信息’中，tcpdump 命令的原文写法是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b046170188e546647016, command-family:tcpdump
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[292], word/document.xml/body/p[293], word/document.xml/body/p[294], word/document.xml/body/p[295] · `chunk-cd469b95520a9da4928f8fa7`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
统计N4口报文信息
登录UPF物理机，打开终端
查看N4IP在哪个端口
选择该端口，运行如下命令抓包
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[296] · `chunk-7fdde4d9a3c3a42036bffd3d`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[297] · `chunk-67083f7c25d8e6bb5ac216ee`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
一段时间后，键入Ctrl+C停止抓包
```
- 预期原文/缺口：
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```

## command-018 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：请引用‘逻辑口报文信息统计 / 统计N4口报文信息’中的命令 tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap，保留占位符和参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b046170188e546647016, command-family:tcpdump
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[292], word/document.xml/body/p[293], word/document.xml/body/p[294], word/document.xml/body/p[295] · `chunk-cd469b95520a9da4928f8fa7`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
统计N4口报文信息
登录UPF物理机，打开终端
查看N4IP在哪个端口
选择该端口，运行如下命令抓包
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[296] · `chunk-7fdde4d9a3c3a42036bffd3d`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[297] · `chunk-67083f7c25d8e6bb5ac216ee`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
一段时间后，键入Ctrl+C停止抓包
```
- 预期原文/缺口：
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```

## command-019 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：手册‘逻辑口报文信息统计 / 统计N4口报文信息’如何使用 tcpdump？只摘录原文并说明示例适用范围。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b046170188e546647016, command-family:tcpdump
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[292], word/document.xml/body/p[293], word/document.xml/body/p[294], word/document.xml/body/p[295] · `chunk-cd469b95520a9da4928f8fa7`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
统计N4口报文信息
登录UPF物理机，打开终端
查看N4IP在哪个端口
选择该端口，运行如下命令抓包
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[296] · `chunk-7fdde4d9a3c3a42036bffd3d`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[297] · `chunk-67083f7c25d8e6bb5ac216ee`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
一段时间后，键入Ctrl+C停止抓包
```
- 预期原文/缺口：
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```

## command-020 · dev · command

- [x] 问题及预期事实/相关证据已核对
- 问题：核对 tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap 在‘逻辑口报文信息统计 / 统计N4口报文信息’中的原始语法，不把示例当现场参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b046170188e546647016, command-family:tcpdump
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[292], word/document.xml/body/p[293], word/document.xml/body/p[294], word/document.xml/body/p[295] · `chunk-cd469b95520a9da4928f8fa7`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
统计N4口报文信息
登录UPF物理机，打开终端
查看N4IP在哪个端口
选择该端口，运行如下命令抓包
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[296] · `chunk-7fdde4d9a3c3a42036bffd3d`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · word/document.xml/body/p[297] · `chunk-67083f7c25d8e6bb5ac216ee`
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
一段时间后，键入Ctrl+C停止抓包
```
- 预期原文/缺口：
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```

## command-021 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：在‘配置UPF物理机 / 配置root SSH登陆权限’中，systemctl 命令的原文写法是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-6622b1bf5a5e87007b26, command-family:systemctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[355], word/document.xml/body/p[356], word/document.xml/body/p[357], word/document.xml/body/p[358], word/document.xml/body/p[359], word/document.xml/body/p[360], word/document.xml/body/p[361], word/document.xml/body/p[362], word/document.xml/body/p[363], word/document.xml/body/p[364], word/document.xml/body/p[365], word/document.xml/body/p[366], word/document.xml/body/p[367], word/document.xml/body/p[368] · `chunk-71311040510f8df9aa5efb17`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
配置root SSH登陆权限
在远程kvm按照以下步骤修改
①打开root权限
用普通用户登录console，以“guest”为例
在guest用户下，执行sudo -s命令进入root用户
执行passwd命令配置root的密码
在root权限下执行如下命令，进入sshd_config文件编辑界面。
$ vim /etc/ssh/sshd_config
按【I】键进入编辑，找到”#PermitRootLogin prohibit-password”，改为：
PermitRootLogin yes
找到”#PasswordAuthentication yes，去除“#”，改为：
PasswordAuthentication yes
【ESC】键，输入“:wq”，保存并退出vim编辑器。
重启sshd服务，使配置文件生效。
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[369] · `chunk-e3529db276d608065d796152`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[370], word/document.xml/body/p[371], word/document.xml/body/p[372], word/document.xml/body/p[373], word/document.xml/body/p[374], word/document.xml/body/p[375], word/document.xml/body/p[376] · `chunk-1f407885a8268eac87f3e90b`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
②关防火墙
关闭防火墙
ufw disable
查看防火墙状态是否关闭
ufw status
③重置root密码
④ 使用SSH工具（例如：SecureCRT或MobaXterrm）登陆Master节点
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```

## command-022 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：请引用‘配置UPF物理机 / 配置root SSH登陆权限’中的命令 systemctl restart sshd，保留占位符和参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-6622b1bf5a5e87007b26, command-family:systemctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[355], word/document.xml/body/p[356], word/document.xml/body/p[357], word/document.xml/body/p[358], word/document.xml/body/p[359], word/document.xml/body/p[360], word/document.xml/body/p[361], word/document.xml/body/p[362], word/document.xml/body/p[363], word/document.xml/body/p[364], word/document.xml/body/p[365], word/document.xml/body/p[366], word/document.xml/body/p[367], word/document.xml/body/p[368] · `chunk-71311040510f8df9aa5efb17`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
配置root SSH登陆权限
在远程kvm按照以下步骤修改
①打开root权限
用普通用户登录console，以“guest”为例
在guest用户下，执行sudo -s命令进入root用户
执行passwd命令配置root的密码
在root权限下执行如下命令，进入sshd_config文件编辑界面。
$ vim /etc/ssh/sshd_config
按【I】键进入编辑，找到”#PermitRootLogin prohibit-password”，改为：
PermitRootLogin yes
找到”#PasswordAuthentication yes，去除“#”，改为：
PasswordAuthentication yes
【ESC】键，输入“:wq”，保存并退出vim编辑器。
重启sshd服务，使配置文件生效。
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[369] · `chunk-e3529db276d608065d796152`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[370], word/document.xml/body/p[371], word/document.xml/body/p[372], word/document.xml/body/p[373], word/document.xml/body/p[374], word/document.xml/body/p[375], word/document.xml/body/p[376] · `chunk-1f407885a8268eac87f3e90b`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
②关防火墙
关闭防火墙
ufw disable
查看防火墙状态是否关闭
ufw status
③重置root密码
④ 使用SSH工具（例如：SecureCRT或MobaXterrm）登陆Master节点
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```

## command-023 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：手册‘配置UPF物理机 / 配置root SSH登陆权限’如何使用 systemctl？只摘录原文并说明示例适用范围。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-6622b1bf5a5e87007b26, command-family:systemctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[355], word/document.xml/body/p[356], word/document.xml/body/p[357], word/document.xml/body/p[358], word/document.xml/body/p[359], word/document.xml/body/p[360], word/document.xml/body/p[361], word/document.xml/body/p[362], word/document.xml/body/p[363], word/document.xml/body/p[364], word/document.xml/body/p[365], word/document.xml/body/p[366], word/document.xml/body/p[367], word/document.xml/body/p[368] · `chunk-71311040510f8df9aa5efb17`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
配置root SSH登陆权限
在远程kvm按照以下步骤修改
①打开root权限
用普通用户登录console，以“guest”为例
在guest用户下，执行sudo -s命令进入root用户
执行passwd命令配置root的密码
在root权限下执行如下命令，进入sshd_config文件编辑界面。
$ vim /etc/ssh/sshd_config
按【I】键进入编辑，找到”#PermitRootLogin prohibit-password”，改为：
PermitRootLogin yes
找到”#PasswordAuthentication yes，去除“#”，改为：
PasswordAuthentication yes
【ESC】键，输入“:wq”，保存并退出vim编辑器。
重启sshd服务，使配置文件生效。
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[369] · `chunk-e3529db276d608065d796152`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[370], word/document.xml/body/p[371], word/document.xml/body/p[372], word/document.xml/body/p[373], word/document.xml/body/p[374], word/document.xml/body/p[375], word/document.xml/body/p[376] · `chunk-1f407885a8268eac87f3e90b`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
②关防火墙
关闭防火墙
ufw disable
查看防火墙状态是否关闭
ufw status
③重置root密码
④ 使用SSH工具（例如：SecureCRT或MobaXterrm）登陆Master节点
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```

## command-024 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：核对 systemctl restart sshd 在‘配置UPF物理机 / 配置root SSH登陆权限’中的原始语法，不把示例当现场参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-6622b1bf5a5e87007b26, command-family:systemctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[355], word/document.xml/body/p[356], word/document.xml/body/p[357], word/document.xml/body/p[358], word/document.xml/body/p[359], word/document.xml/body/p[360], word/document.xml/body/p[361], word/document.xml/body/p[362], word/document.xml/body/p[363], word/document.xml/body/p[364], word/document.xml/body/p[365], word/document.xml/body/p[366], word/document.xml/body/p[367], word/document.xml/body/p[368] · `chunk-71311040510f8df9aa5efb17`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
配置root SSH登陆权限
在远程kvm按照以下步骤修改
①打开root权限
用普通用户登录console，以“guest”为例
在guest用户下，执行sudo -s命令进入root用户
执行passwd命令配置root的密码
在root权限下执行如下命令，进入sshd_config文件编辑界面。
$ vim /etc/ssh/sshd_config
按【I】键进入编辑，找到”#PermitRootLogin prohibit-password”，改为：
PermitRootLogin yes
找到”#PasswordAuthentication yes，去除“#”，改为：
PasswordAuthentication yes
【ESC】键，输入“:wq”，保存并退出vim编辑器。
重启sshd服务，使配置文件生效。
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[369] · `chunk-e3529db276d608065d796152`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[370], word/document.xml/body/p[371], word/document.xml/body/p[372], word/document.xml/body/p[373], word/document.xml/body/p[374], word/document.xml/body/p[375], word/document.xml/body/p[376] · `chunk-1f407885a8268eac87f3e90b`
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
②关防火墙
关闭防火墙
ufw disable
查看防火墙状态是否关闭
ufw status
③重置root密码
④ 使用SSH工具（例如：SecureCRT或MobaXterrm）登陆Master节点
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```

## command-025 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：在‘基本故障排查 / 插件安装问题’中，helm 命令的原文写法是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-206f98b59b4a27568dd1, command-family:helm
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1807], word/document.xml/body/p[1808], word/document.xml/body/p[1809], word/document.xml/body/p[1810], word/document.xml/body/p[1811], word/document.xml/body/p[1812], word/document.xml/body/p[1813], word/document.xml/body/p[1815], word/document.xml/body/p[1816], word/document.xml/body/p[1817], word/document.xml/body/p[1818], word/document.xml/body/p[1820], word/document.xml/body/p[1821], word/document.xml/body/p[1822], word/document.xml/body/p[1824] · `chunk-1a09cca0adc6efedbe4ede47`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
插件安装问题
每个插件调用sealos run命令进行安装，插件安装失败时会给出错误提示，但不会终止整个安装流程，可以在安装完成后单独处理失败的插件，具体失败原因需要分析插件pod日志。
以openebs存储插件为例，插件安装在openebs命名空间，使用helm进行部署。其他插件信息请参考插件运行管理章节。
1.	首先检查helm是否已经成功下发openebs chart，并且STATUS为deployed
root@upf:~# helm -n openebs ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
openebs openebs         1               2023-03-30 11:16:53.302896372 +0800 CST deployed        openebs-3.3.1   3.3.0  
2.	检查openebs命名空间下的pod状态，查看STATUS列是否为Running
root@upf:~# kubectl -n openebs get pods 
NAME                                          READY   STATUS    RESTARTS       AGE
openebs-localpv-provisioner-7b4db8497-bjjvp   1/1     Running   3 (149m ago)   5h59m
3.	如果pod状态异常，需要查看pod日志，分析定位具体原因，一般使用以下命令查看openebs pod日志
root@upf:~# kubectl -n openebs logs -f openebs-localpv-provisioner-7b4db8497-bjjvp
root@upf:~# kubectl -n openebs describe pods openebs-localpv-provisioner-7b4db8497-bjjvp
4.	相关问题解决后可以尝试删除openebs插件重新安装
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1825] · `chunk-c1617c5c3cf7294398ff805e`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs uninstall openebs
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1827], word/document.xml/body/p[1828], word/document.xml/body/p[1829], word/document.xml/body/p[1830], word/document.xml/body/p[1831], word/document.xml/body/p[1832], word/document.xml/body/p[1833] · `chunk-53437a229a63ced981aa3469`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
5.	执行以下命令重新安装openebs插件
a.查找本地openebs镜像
root@upf:~# sealos images | grep openebs
docker.io/labring/openebs                                                v3.3.0    cd884460a800   7 weeks ago    57.5 MB
b.单独安装openebs插件，由于之前已经运行过一次openebs插件安装，需要添加-f参数强制安装
sealos run docker.io/labring/openebs:v3.3.0 -f
c.再次检查插件运行状态，确认是否安装成功
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1834] · `chunk-b6acc1271c1a045af4aba962`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs ls
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1835] · `chunk-ff13c68062b40e541691331c`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
kubectl -n openebs get pods
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs uninstall openebs
```

## command-026 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：请引用‘基本故障排查 / 插件安装问题’中的命令 helm -n openebs uninstall openebs，保留占位符和参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-206f98b59b4a27568dd1, command-family:helm
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1807], word/document.xml/body/p[1808], word/document.xml/body/p[1809], word/document.xml/body/p[1810], word/document.xml/body/p[1811], word/document.xml/body/p[1812], word/document.xml/body/p[1813], word/document.xml/body/p[1815], word/document.xml/body/p[1816], word/document.xml/body/p[1817], word/document.xml/body/p[1818], word/document.xml/body/p[1820], word/document.xml/body/p[1821], word/document.xml/body/p[1822], word/document.xml/body/p[1824] · `chunk-1a09cca0adc6efedbe4ede47`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
插件安装问题
每个插件调用sealos run命令进行安装，插件安装失败时会给出错误提示，但不会终止整个安装流程，可以在安装完成后单独处理失败的插件，具体失败原因需要分析插件pod日志。
以openebs存储插件为例，插件安装在openebs命名空间，使用helm进行部署。其他插件信息请参考插件运行管理章节。
1.	首先检查helm是否已经成功下发openebs chart，并且STATUS为deployed
root@upf:~# helm -n openebs ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
openebs openebs         1               2023-03-30 11:16:53.302896372 +0800 CST deployed        openebs-3.3.1   3.3.0  
2.	检查openebs命名空间下的pod状态，查看STATUS列是否为Running
root@upf:~# kubectl -n openebs get pods 
NAME                                          READY   STATUS    RESTARTS       AGE
openebs-localpv-provisioner-7b4db8497-bjjvp   1/1     Running   3 (149m ago)   5h59m
3.	如果pod状态异常，需要查看pod日志，分析定位具体原因，一般使用以下命令查看openebs pod日志
root@upf:~# kubectl -n openebs logs -f openebs-localpv-provisioner-7b4db8497-bjjvp
root@upf:~# kubectl -n openebs describe pods openebs-localpv-provisioner-7b4db8497-bjjvp
4.	相关问题解决后可以尝试删除openebs插件重新安装
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1825] · `chunk-c1617c5c3cf7294398ff805e`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs uninstall openebs
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1827], word/document.xml/body/p[1828], word/document.xml/body/p[1829], word/document.xml/body/p[1830], word/document.xml/body/p[1831], word/document.xml/body/p[1832], word/document.xml/body/p[1833] · `chunk-53437a229a63ced981aa3469`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
5.	执行以下命令重新安装openebs插件
a.查找本地openebs镜像
root@upf:~# sealos images | grep openebs
docker.io/labring/openebs                                                v3.3.0    cd884460a800   7 weeks ago    57.5 MB
b.单独安装openebs插件，由于之前已经运行过一次openebs插件安装，需要添加-f参数强制安装
sealos run docker.io/labring/openebs:v3.3.0 -f
c.再次检查插件运行状态，确认是否安装成功
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1834] · `chunk-b6acc1271c1a045af4aba962`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs ls
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1835] · `chunk-ff13c68062b40e541691331c`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
kubectl -n openebs get pods
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs uninstall openebs
```

## command-027 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：手册‘基本故障排查 / 插件安装问题’如何使用 helm？只摘录原文并说明示例适用范围。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-206f98b59b4a27568dd1, command-family:helm
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1807], word/document.xml/body/p[1808], word/document.xml/body/p[1809], word/document.xml/body/p[1810], word/document.xml/body/p[1811], word/document.xml/body/p[1812], word/document.xml/body/p[1813], word/document.xml/body/p[1815], word/document.xml/body/p[1816], word/document.xml/body/p[1817], word/document.xml/body/p[1818], word/document.xml/body/p[1820], word/document.xml/body/p[1821], word/document.xml/body/p[1822], word/document.xml/body/p[1824] · `chunk-1a09cca0adc6efedbe4ede47`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
插件安装问题
每个插件调用sealos run命令进行安装，插件安装失败时会给出错误提示，但不会终止整个安装流程，可以在安装完成后单独处理失败的插件，具体失败原因需要分析插件pod日志。
以openebs存储插件为例，插件安装在openebs命名空间，使用helm进行部署。其他插件信息请参考插件运行管理章节。
1.	首先检查helm是否已经成功下发openebs chart，并且STATUS为deployed
root@upf:~# helm -n openebs ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
openebs openebs         1               2023-03-30 11:16:53.302896372 +0800 CST deployed        openebs-3.3.1   3.3.0  
2.	检查openebs命名空间下的pod状态，查看STATUS列是否为Running
root@upf:~# kubectl -n openebs get pods 
NAME                                          READY   STATUS    RESTARTS       AGE
openebs-localpv-provisioner-7b4db8497-bjjvp   1/1     Running   3 (149m ago)   5h59m
3.	如果pod状态异常，需要查看pod日志，分析定位具体原因，一般使用以下命令查看openebs pod日志
root@upf:~# kubectl -n openebs logs -f openebs-localpv-provisioner-7b4db8497-bjjvp
root@upf:~# kubectl -n openebs describe pods openebs-localpv-provisioner-7b4db8497-bjjvp
4.	相关问题解决后可以尝试删除openebs插件重新安装
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1825] · `chunk-c1617c5c3cf7294398ff805e`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs uninstall openebs
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1827], word/document.xml/body/p[1828], word/document.xml/body/p[1829], word/document.xml/body/p[1830], word/document.xml/body/p[1831], word/document.xml/body/p[1832], word/document.xml/body/p[1833] · `chunk-53437a229a63ced981aa3469`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
5.	执行以下命令重新安装openebs插件
a.查找本地openebs镜像
root@upf:~# sealos images | grep openebs
docker.io/labring/openebs                                                v3.3.0    cd884460a800   7 weeks ago    57.5 MB
b.单独安装openebs插件，由于之前已经运行过一次openebs插件安装，需要添加-f参数强制安装
sealos run docker.io/labring/openebs:v3.3.0 -f
c.再次检查插件运行状态，确认是否安装成功
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1834] · `chunk-b6acc1271c1a045af4aba962`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs ls
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1835] · `chunk-ff13c68062b40e541691331c`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
kubectl -n openebs get pods
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs uninstall openebs
```

## command-028 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：核对 helm -n openebs uninstall openebs 在‘基本故障排查 / 插件安装问题’中的原始语法，不把示例当现场参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-206f98b59b4a27568dd1, command-family:helm
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1807], word/document.xml/body/p[1808], word/document.xml/body/p[1809], word/document.xml/body/p[1810], word/document.xml/body/p[1811], word/document.xml/body/p[1812], word/document.xml/body/p[1813], word/document.xml/body/p[1815], word/document.xml/body/p[1816], word/document.xml/body/p[1817], word/document.xml/body/p[1818], word/document.xml/body/p[1820], word/document.xml/body/p[1821], word/document.xml/body/p[1822], word/document.xml/body/p[1824] · `chunk-1a09cca0adc6efedbe4ede47`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
插件安装问题
每个插件调用sealos run命令进行安装，插件安装失败时会给出错误提示，但不会终止整个安装流程，可以在安装完成后单独处理失败的插件，具体失败原因需要分析插件pod日志。
以openebs存储插件为例，插件安装在openebs命名空间，使用helm进行部署。其他插件信息请参考插件运行管理章节。
1.	首先检查helm是否已经成功下发openebs chart，并且STATUS为deployed
root@upf:~# helm -n openebs ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
openebs openebs         1               2023-03-30 11:16:53.302896372 +0800 CST deployed        openebs-3.3.1   3.3.0  
2.	检查openebs命名空间下的pod状态，查看STATUS列是否为Running
root@upf:~# kubectl -n openebs get pods 
NAME                                          READY   STATUS    RESTARTS       AGE
openebs-localpv-provisioner-7b4db8497-bjjvp   1/1     Running   3 (149m ago)   5h59m
3.	如果pod状态异常，需要查看pod日志，分析定位具体原因，一般使用以下命令查看openebs pod日志
root@upf:~# kubectl -n openebs logs -f openebs-localpv-provisioner-7b4db8497-bjjvp
root@upf:~# kubectl -n openebs describe pods openebs-localpv-provisioner-7b4db8497-bjjvp
4.	相关问题解决后可以尝试删除openebs插件重新安装
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1825] · `chunk-c1617c5c3cf7294398ff805e`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs uninstall openebs
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1827], word/document.xml/body/p[1828], word/document.xml/body/p[1829], word/document.xml/body/p[1830], word/document.xml/body/p[1831], word/document.xml/body/p[1832], word/document.xml/body/p[1833] · `chunk-53437a229a63ced981aa3469`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
5.	执行以下命令重新安装openebs插件
a.查找本地openebs镜像
root@upf:~# sealos images | grep openebs
docker.io/labring/openebs                                                v3.3.0    cd884460a800   7 weeks ago    57.5 MB
b.单独安装openebs插件，由于之前已经运行过一次openebs插件安装，需要添加-f参数强制安装
sealos run docker.io/labring/openebs:v3.3.0 -f
c.再次检查插件运行状态，确认是否安装成功
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1834] · `chunk-b6acc1271c1a045af4aba962`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs ls
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1835] · `chunk-ff13c68062b40e541691331c`
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
kubectl -n openebs get pods
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
helm -n openebs uninstall openebs
```

## command-029 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：在‘UPF基本故障排查 / 查看UPF软件包’中，ls 命令的原文写法是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-726b781a8d5f223c8f86, command-family:ls
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2325], word/document.xml/body/p[2326], word/document.xml/body/p[2327] · `chunk-44afc482e08f7b8768c9f4c3`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
查看UPF软件包
查看解压的软件包
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2328] · `chunk-093401cdba160a0162a8e964`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2329] · `chunk-3d222d542889d1a7e81b0c71`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
dpdk-devinfo-nic  multus  servicePack-CU5GC_UPF_5.0.210  servicePack_CU5GC_VDOS_1.0.5
```
- 预期原文/缺口：
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```

## command-030 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：请引用‘UPF基本故障排查 / 查看UPF软件包’中的命令 ls temp/，保留占位符和参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-726b781a8d5f223c8f86, command-family:ls
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2325], word/document.xml/body/p[2326], word/document.xml/body/p[2327] · `chunk-44afc482e08f7b8768c9f4c3`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
查看UPF软件包
查看解压的软件包
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2328] · `chunk-093401cdba160a0162a8e964`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2329] · `chunk-3d222d542889d1a7e81b0c71`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
dpdk-devinfo-nic  multus  servicePack-CU5GC_UPF_5.0.210  servicePack_CU5GC_VDOS_1.0.5
```
- 预期原文/缺口：
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```

## command-031 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：手册‘UPF基本故障排查 / 查看UPF软件包’如何使用 ls？只摘录原文并说明示例适用范围。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-726b781a8d5f223c8f86, command-family:ls
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2325], word/document.xml/body/p[2326], word/document.xml/body/p[2327] · `chunk-44afc482e08f7b8768c9f4c3`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
查看UPF软件包
查看解压的软件包
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2328] · `chunk-093401cdba160a0162a8e964`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2329] · `chunk-3d222d542889d1a7e81b0c71`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
dpdk-devinfo-nic  multus  servicePack-CU5GC_UPF_5.0.210  servicePack_CU5GC_VDOS_1.0.5
```
- 预期原文/缺口：
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```

## command-032 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：核对 ls temp/ 在‘UPF基本故障排查 / 查看UPF软件包’中的原始语法，不把示例当现场参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-726b781a8d5f223c8f86, command-family:ls
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2325], word/document.xml/body/p[2326], word/document.xml/body/p[2327] · `chunk-44afc482e08f7b8768c9f4c3`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
查看UPF软件包
查看解压的软件包
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2328] · `chunk-093401cdba160a0162a8e964`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2329] · `chunk-3d222d542889d1a7e81b0c71`
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
dpdk-devinfo-nic  multus  servicePack-CU5GC_UPF_5.0.210  servicePack_CU5GC_VDOS_1.0.5
```
- 预期原文/缺口：
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```

## command-033 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：在‘UPF基本故障排查 / SOC 服务器nic问题’中，chmod 命令的原文写法是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b059f306885fbaefdd56, command-family:chmod
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2341], word/document.xml/body/p[2342], word/document.xml/body/p[2343], word/document.xml/body/p[2344], word/document.xml/body/p[2345] · `chunk-5ec26d2bd7c6cd308d4ae6a7`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
SOC 服务器nic问题
SOC服务器是8 port，现在只用4个，因为有一些limitation。修改方法如下：
下载epct64e二进制文件
 HYPERLINK "https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html" https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html
安装二进制文件到/usr/local/bin目录下
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2346] · `chunk-2811577ed855f89547fec1d4`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
cp epct64e /usr/local/bin
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2347] · `chunk-1d0e14afadc3125ff15e6d99`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2348], word/document.xml/body/p[2349] · `chunk-c8deaa189d6c9bfc9f3a227e`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
执行以下命令为nic增加配置参数
epct64e -nic=1 -set=4x25
```
- 预期原文/缺口：
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```

## command-034 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：请引用‘UPF基本故障排查 / SOC 服务器nic问题’中的命令 chmod +x /usr/local/bin/epct64e，保留占位符和参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b059f306885fbaefdd56, command-family:chmod
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2341], word/document.xml/body/p[2342], word/document.xml/body/p[2343], word/document.xml/body/p[2344], word/document.xml/body/p[2345] · `chunk-5ec26d2bd7c6cd308d4ae6a7`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
SOC 服务器nic问题
SOC服务器是8 port，现在只用4个，因为有一些limitation。修改方法如下：
下载epct64e二进制文件
 HYPERLINK "https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html" https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html
安装二进制文件到/usr/local/bin目录下
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2346] · `chunk-2811577ed855f89547fec1d4`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
cp epct64e /usr/local/bin
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2347] · `chunk-1d0e14afadc3125ff15e6d99`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2348], word/document.xml/body/p[2349] · `chunk-c8deaa189d6c9bfc9f3a227e`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
执行以下命令为nic增加配置参数
epct64e -nic=1 -set=4x25
```
- 预期原文/缺口：
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```

## command-035 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：手册‘UPF基本故障排查 / SOC 服务器nic问题’如何使用 chmod？只摘录原文并说明示例适用范围。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b059f306885fbaefdd56, command-family:chmod
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2341], word/document.xml/body/p[2342], word/document.xml/body/p[2343], word/document.xml/body/p[2344], word/document.xml/body/p[2345] · `chunk-5ec26d2bd7c6cd308d4ae6a7`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
SOC 服务器nic问题
SOC服务器是8 port，现在只用4个，因为有一些limitation。修改方法如下：
下载epct64e二进制文件
 HYPERLINK "https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html" https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html
安装二进制文件到/usr/local/bin目录下
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2346] · `chunk-2811577ed855f89547fec1d4`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
cp epct64e /usr/local/bin
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2347] · `chunk-1d0e14afadc3125ff15e6d99`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2348], word/document.xml/body/p[2349] · `chunk-c8deaa189d6c9bfc9f3a227e`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
执行以下命令为nic增加配置参数
epct64e -nic=1 -set=4x25
```
- 预期原文/缺口：
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```

## command-036 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：核对 chmod +x /usr/local/bin/epct64e 在‘UPF基本故障排查 / SOC 服务器nic问题’中的原始语法，不把示例当现场参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b059f306885fbaefdd56, command-family:chmod
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2341], word/document.xml/body/p[2342], word/document.xml/body/p[2343], word/document.xml/body/p[2344], word/document.xml/body/p[2345] · `chunk-5ec26d2bd7c6cd308d4ae6a7`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
SOC 服务器nic问题
SOC服务器是8 port，现在只用4个，因为有一些limitation。修改方法如下：
下载epct64e二进制文件
 HYPERLINK "https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html" https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html
安装二进制文件到/usr/local/bin目录下
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2346] · `chunk-2811577ed855f89547fec1d4`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
cp epct64e /usr/local/bin
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2347] · `chunk-1d0e14afadc3125ff15e6d99`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2348], word/document.xml/body/p[2349] · `chunk-c8deaa189d6c9bfc9f3a227e`
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
执行以下命令为nic增加配置参数
epct64e -nic=1 -set=4x25
```
- 预期原文/缺口：
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```

## command-037 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：在‘基本故障排查 / 集群安装问题’中，journalctl 命令的原文写法是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-8baf65985aebaf898945, command-family:journalctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1788], word/document.xml/body/p[1789], word/document.xml/body/p[1790] · `chunk-8b7190a7813bebeffe210cc7`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
集群安装问题
集群安装失败时，集群安装过程中输出的日志信息有限，一般需要进一步检查kubernetes系统进程例如kubelet、containerd状态及日志。
1.	查看kubelet运行状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1791] · `chunk-7d6750acd76fa1ca0043ec44`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1792] · `chunk-04f75f76e3e997b3afb95ab4`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
2.	查看containerd容器运行时状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1793] · `chunk-cabd3152ee269df6489ed07b`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1794] · `chunk-e7773e4bc9c9794eef44177c`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
3.	查看kubelet详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1795] · `chunk-40e89a682b78c5baf67ab343`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1796] · `chunk-7eb6ba2c984e4c3c2253d153`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
4.	查看containerd详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1797] · `chunk-5bf91a33efe9ff9fa23173e1`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1798], word/document.xml/body/p[1799], word/document.xml/body/p[1800] · `chunk-002d97a55d8b83668dc3dfa6`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
5.	查看apiserver pod日志
nerdctl -n k8s.io ps -a
nerdctl -n k8s.io logs -f e8793b8cca8b
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```

## command-038 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：请引用‘基本故障排查 / 集群安装问题’中的命令 journalctl -xeu kubelet，保留占位符和参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-8baf65985aebaf898945, command-family:journalctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1788], word/document.xml/body/p[1789], word/document.xml/body/p[1790] · `chunk-8b7190a7813bebeffe210cc7`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
集群安装问题
集群安装失败时，集群安装过程中输出的日志信息有限，一般需要进一步检查kubernetes系统进程例如kubelet、containerd状态及日志。
1.	查看kubelet运行状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1791] · `chunk-7d6750acd76fa1ca0043ec44`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1792] · `chunk-04f75f76e3e997b3afb95ab4`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
2.	查看containerd容器运行时状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1793] · `chunk-cabd3152ee269df6489ed07b`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1794] · `chunk-e7773e4bc9c9794eef44177c`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
3.	查看kubelet详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1795] · `chunk-40e89a682b78c5baf67ab343`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1796] · `chunk-7eb6ba2c984e4c3c2253d153`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
4.	查看containerd详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1797] · `chunk-5bf91a33efe9ff9fa23173e1`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1798], word/document.xml/body/p[1799], word/document.xml/body/p[1800] · `chunk-002d97a55d8b83668dc3dfa6`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
5.	查看apiserver pod日志
nerdctl -n k8s.io ps -a
nerdctl -n k8s.io logs -f e8793b8cca8b
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```

## command-039 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：手册‘基本故障排查 / 集群安装问题’如何使用 journalctl？只摘录原文并说明示例适用范围。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-8baf65985aebaf898945, command-family:journalctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1788], word/document.xml/body/p[1789], word/document.xml/body/p[1790] · `chunk-8b7190a7813bebeffe210cc7`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
集群安装问题
集群安装失败时，集群安装过程中输出的日志信息有限，一般需要进一步检查kubernetes系统进程例如kubelet、containerd状态及日志。
1.	查看kubelet运行状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1791] · `chunk-7d6750acd76fa1ca0043ec44`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1792] · `chunk-04f75f76e3e997b3afb95ab4`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
2.	查看containerd容器运行时状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1793] · `chunk-cabd3152ee269df6489ed07b`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1794] · `chunk-e7773e4bc9c9794eef44177c`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
3.	查看kubelet详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1795] · `chunk-40e89a682b78c5baf67ab343`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1796] · `chunk-7eb6ba2c984e4c3c2253d153`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
4.	查看containerd详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1797] · `chunk-5bf91a33efe9ff9fa23173e1`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1798], word/document.xml/body/p[1799], word/document.xml/body/p[1800] · `chunk-002d97a55d8b83668dc3dfa6`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
5.	查看apiserver pod日志
nerdctl -n k8s.io ps -a
nerdctl -n k8s.io logs -f e8793b8cca8b
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```

## command-040 · heldout · command

- [x] 问题及预期事实/相关证据已核对
- 问题：核对 journalctl -xeu kubelet 在‘基本故障排查 / 集群安装问题’中的原始语法，不把示例当现场参数。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-8baf65985aebaf898945, command-family:journalctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1788], word/document.xml/body/p[1789], word/document.xml/body/p[1790] · `chunk-8b7190a7813bebeffe210cc7`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
集群安装问题
集群安装失败时，集群安装过程中输出的日志信息有限，一般需要进一步检查kubernetes系统进程例如kubelet、containerd状态及日志。
1.	查看kubelet运行状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1791] · `chunk-7d6750acd76fa1ca0043ec44`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1792] · `chunk-04f75f76e3e997b3afb95ab4`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
2.	查看containerd容器运行时状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1793] · `chunk-cabd3152ee269df6489ed07b`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1794] · `chunk-e7773e4bc9c9794eef44177c`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
3.	查看kubelet详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1795] · `chunk-40e89a682b78c5baf67ab343`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1796] · `chunk-7eb6ba2c984e4c3c2253d153`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
4.	查看containerd详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1797] · `chunk-5bf91a33efe9ff9fa23173e1`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1798], word/document.xml/body/p[1799], word/document.xml/body/p[1800] · `chunk-002d97a55d8b83668dc3dfa6`
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
5.	查看apiserver pod日志
nerdctl -n k8s.io ps -a
nerdctl -n k8s.io logs -f e8793b8cca8b
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```

## knowledge-001 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 配置网口地址’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-5a92fa412edb46d34881, manual-topic:section-5a92fa412edb46d34881
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[302], word/document.xml/body/p[303], word/document.xml/body/p[304], word/document.xml/body/p[305], word/document.xml/body/p[306], word/document.xml/body/p[307] · `chunk-e792107b5ba57b6b518b558d`
```text
物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 配置网口地址
配置网口地址
说明：本步骤并非必须配置，之后可以通过修改netplan的配置文件实完成。需要跟进现网实际情况进行配置，示例仅给出参考：
按照网络规划，配置网口地址，以配置eno1的静态地址为例：
参数说明：
Gateway：必须设置
Name servers：必须设置，在离线环境没有DNS服务器时，该地址配置为Gateway地址
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 配置网口地址
配置网口地址
说明：本步骤并非必须配置，之后可以通过修改netplan的配置文件实完成。需要跟进现网实际情况进行配置，示例仅给出参考：
按照网络规划，配置网口地址，以配置eno1的静态地址为例：
参数说明：
Gateway：必须设置
Name servers：必须设置，在离线环境没有DNS服务器时，该地址配置为Gateway地址
```

## knowledge-002 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 配置网口地址’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-5a92fa412edb46d34881, manual-topic:section-5a92fa412edb46d34881
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[302], word/document.xml/body/p[303], word/document.xml/body/p[304], word/document.xml/body/p[305], word/document.xml/body/p[306], word/document.xml/body/p[307] · `chunk-e792107b5ba57b6b518b558d`
```text
物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 配置网口地址
配置网口地址
说明：本步骤并非必须配置，之后可以通过修改netplan的配置文件实完成。需要跟进现网实际情况进行配置，示例仅给出参考：
按照网络规划，配置网口地址，以配置eno1的静态地址为例：
参数说明：
Gateway：必须设置
Name servers：必须设置，在离线环境没有DNS服务器时，该地址配置为Gateway地址
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 配置网口地址
配置网口地址
说明：本步骤并非必须配置，之后可以通过修改netplan的配置文件实完成。需要跟进现网实际情况进行配置，示例仅给出参考：
按照网络规划，配置网口地址，以配置eno1的静态地址为例：
参数说明：
Gateway：必须设置
Name servers：必须设置，在离线环境没有DNS服务器时，该地址配置为Gateway地址
```

## knowledge-003 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-003d947b9a7eb6f58ab9, manual-topic:section-003d947b9a7eb6f58ab9
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[458], word/document.xml/body/p[459], word/document.xml/body/p[460] · `chunk-8516d529791bd1e59ca97908`
```text
物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）
netplan Bond模式（现网部署配置）
现网场景下，更推荐使用Bond模式，增加冗余备份。当任意一张网卡因故障无法工作时候，另外一张网卡仍可继续工作，不影响UPF软件和各个接口之间进行数据通信。
Bond模式下00-installer-config.yaml 配置信息如下，具体对应关系可以和 REF _Ref4002 \n \h 2.2.3.2 REF _Ref4002 \h UPF地址规划Bonding模式章节内容彼此对应查看。
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[461], word/document.xml/body/p[462], word/document.xml/body/p[463], word/document.xml/body/p[464], word/document.xml/body/p[465], word/document.xml/body/p[466], word/document.xml/body/p[467], word/document.xml/body/p[468], word/document.xml/body/p[469], word/document.xml/body/p[470], word/document.xml/body/p[471], word/document.xml/body/p[472], word/document.xml/body/p[473], word/document.xml/body/p[474], word/document.xml/body/p[475], word/document.xml/body/p[476], word/document.xml/body/p[477], word/document.xml/body/p[478], word/document.xml/body/p[479], word/document.xml/body/p[480], word/document.xml/body/p[481], word/document.xml/body/p[482], word/document.xml/body/p[483], word/document.xml/body/p[484], word/document.xml/body/p[485], word/document.xml/body/p[486], word/document.xml/body/p[487], word/document.xml/body/p[488], word/document.xml/body/p[489], word/document.xml/body/p[490], word/document.xml/body/p[491], word/document.xml/body/p[492], word/document.xml/body/p[493], word/document.xml/body/p[494], word/document.xml/body/p[495], word/document.xml/body/p[496], word/document.xml/body/p[497], word/document.xml/body/p[498], word/document.xml/body/p[499] · `chunk-130842ca33fc1ee9055d1bc3`
```text
物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp61s0f0:
      dhcp4: no
    enp61s0f1:
      dhcp4: no
    ens1f0:
      dhcp4: no
    ens1f1:
      dhcp4: no
    ens3f0:
      dhcp4: no
    ens3f1:
      dhcp4: no
  bonds:
    bond0:
      interfaces:
        - enp61s0f0
        - enp61s0f1
      parameters:
        mode: 802.3ad                       #mode设置为4，交换机对应lacp-dynamic
        mii-monitor-interval: 100
  vlans:
    bond0.90:                               #规划的Bond子接口，用于K8s
      id: 90
      link: bond0
      addresses: [ 172.16.100.50/24 ]
      routes:
        - to: default
          via: 172.16.100.1                   #规划的K8s地址网关
      #gateway4: 172.16.100.1
      nameservers:                         # DNS 服务器地址
        addresses: ["172.16.100.1"]
    bond0.299:                              #规划的Bond子接口，用于部署UPF时N4使用
      id: 299
      link: bond0
     # addresses: [ 100.101.1.50/24 ]          #规划的N4地址后续通过网管(curl)配置
  version: 2
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[500], word/document.xml/body/p[501], word/document.xml/body/p[502], word/document.xml/body/p[503], word/document.xml/body/p[504] · `chunk-c68506d4ec5e247b1185a691`
```text
物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）
参数说明：
其中enp61s0f0/enp61s0f1需根据实际部署情况选择需要做bonding的网口；
此处只需考虑N4、K8S和管理口共口部署，N3/N6/N9接口不需要在此处做bonding设置；
用于K8s接口地址网络必须配置nameservers网关地址。后续部署K8s时需要，否则会有报错提示；
默认路由routes.default需要配置。后续部署K8s时需要，否则会有报错提示。
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）
参数说明：
其中enp61s0f0/enp61s0f1需根据实际部署情况选择需要做bonding的网口；
此处只需考虑N4、K8S和管理口共口部署，N3/N6/N9接口不需要在此处做bonding设置；
用于K8s接口地址网络必须配置nameservers网关地址。后续部署K8s时需要，否则会有报错提示；
默认路由routes.default需要配置。后续部署K8s时需要，否则会有报错提示。
```

## knowledge-004 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-003d947b9a7eb6f58ab9, manual-topic:section-003d947b9a7eb6f58ab9
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[458], word/document.xml/body/p[459], word/document.xml/body/p[460] · `chunk-8516d529791bd1e59ca97908`
```text
物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）
netplan Bond模式（现网部署配置）
现网场景下，更推荐使用Bond模式，增加冗余备份。当任意一张网卡因故障无法工作时候，另外一张网卡仍可继续工作，不影响UPF软件和各个接口之间进行数据通信。
Bond模式下00-installer-config.yaml 配置信息如下，具体对应关系可以和 REF _Ref4002 \n \h 2.2.3.2 REF _Ref4002 \h UPF地址规划Bonding模式章节内容彼此对应查看。
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[461], word/document.xml/body/p[462], word/document.xml/body/p[463], word/document.xml/body/p[464], word/document.xml/body/p[465], word/document.xml/body/p[466], word/document.xml/body/p[467], word/document.xml/body/p[468], word/document.xml/body/p[469], word/document.xml/body/p[470], word/document.xml/body/p[471], word/document.xml/body/p[472], word/document.xml/body/p[473], word/document.xml/body/p[474], word/document.xml/body/p[475], word/document.xml/body/p[476], word/document.xml/body/p[477], word/document.xml/body/p[478], word/document.xml/body/p[479], word/document.xml/body/p[480], word/document.xml/body/p[481], word/document.xml/body/p[482], word/document.xml/body/p[483], word/document.xml/body/p[484], word/document.xml/body/p[485], word/document.xml/body/p[486], word/document.xml/body/p[487], word/document.xml/body/p[488], word/document.xml/body/p[489], word/document.xml/body/p[490], word/document.xml/body/p[491], word/document.xml/body/p[492], word/document.xml/body/p[493], word/document.xml/body/p[494], word/document.xml/body/p[495], word/document.xml/body/p[496], word/document.xml/body/p[497], word/document.xml/body/p[498], word/document.xml/body/p[499] · `chunk-130842ca33fc1ee9055d1bc3`
```text
物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp61s0f0:
      dhcp4: no
    enp61s0f1:
      dhcp4: no
    ens1f0:
      dhcp4: no
    ens1f1:
      dhcp4: no
    ens3f0:
      dhcp4: no
    ens3f1:
      dhcp4: no
  bonds:
    bond0:
      interfaces:
        - enp61s0f0
        - enp61s0f1
      parameters:
        mode: 802.3ad                       #mode设置为4，交换机对应lacp-dynamic
        mii-monitor-interval: 100
  vlans:
    bond0.90:                               #规划的Bond子接口，用于K8s
      id: 90
      link: bond0
      addresses: [ 172.16.100.50/24 ]
      routes:
        - to: default
          via: 172.16.100.1                   #规划的K8s地址网关
      #gateway4: 172.16.100.1
      nameservers:                         # DNS 服务器地址
        addresses: ["172.16.100.1"]
    bond0.299:                              #规划的Bond子接口，用于部署UPF时N4使用
      id: 299
      link: bond0
     # addresses: [ 100.101.1.50/24 ]          #规划的N4地址后续通过网管(curl)配置
  version: 2
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[500], word/document.xml/body/p[501], word/document.xml/body/p[502], word/document.xml/body/p[503], word/document.xml/body/p[504] · `chunk-c68506d4ec5e247b1185a691`
```text
物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）
参数说明：
其中enp61s0f0/enp61s0f1需根据实际部署情况选择需要做bonding的网口；
此处只需考虑N4、K8S和管理口共口部署，N3/N6/N9接口不需要在此处做bonding设置；
用于K8s接口地址网络必须配置nameservers网关地址。后续部署K8s时需要，否则会有报错提示；
默认路由routes.default需要配置。后续部署K8s时需要，否则会有报错提示。
```
- 预期原文/缺口：
```text
物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）
参数说明：
其中enp61s0f0/enp61s0f1需根据实际部署情况选择需要做bonding的网口；
此处只需考虑N4、K8S和管理口共口部署，N3/N6/N9接口不需要在此处做bonding设置；
用于K8s接口地址网络必须配置nameservers网关地址。后续部署K8s时需要，否则会有报错提示；
默认路由routes.default需要配置。后续部署K8s时需要，否则会有报错提示。
```

## knowledge-005 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘单节点部署K8S / 调整集群配置 / 调整后的集群配置文件’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-6dbbd25d0bcb9b848452, manual-topic:section-6dbbd25d0bcb9b848452
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[581], word/document.xml/body/p[582], word/document.xml/body/p[583], word/document.xml/body/p[584], word/document.xml/body/p[585], word/document.xml/body/p[587], word/document.xml/body/p[588], word/document.xml/body/p[589], word/document.xml/body/p[590], word/document.xml/body/p[591], word/document.xml/body/p[592], word/document.xml/body/p[593], word/document.xml/body/p[594], word/document.xml/body/p[595], word/document.xml/body/p[596], word/document.xml/body/p[597], word/document.xml/body/p[599], word/document.xml/body/p[600], word/document.xml/body/p[601], word/document.xml/body/p[602], word/document.xml/body/p[604], word/document.xml/body/p[605], word/document.xml/body/p[606], word/document.xml/body/p[608], word/document.xml/body/p[609], word/document.xml/body/p[610], word/document.xml/body/p[611], word/document.xml/body/p[613], word/document.xml/body/p[614], word/document.xml/body/p[615], word/document.xml/body/p[616], word/document.xml/body/p[618], word/document.xml/body/p[619], word/document.xml/body/p[620], word/document.xml/body/p[621], word/document.xml/body/p[623], word/document.xml/body/p[624], word/document.xml/body/p[625], word/document.xml/body/p[626], word/document.xml/body/p[627], word/document.xml/body/p[628] · `chunk-c0269e0f5f90744584380ab7`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
调整后的集群配置文件
部署集群前，需要新建并调整集群配置文件，当前集群自定义参数通过config.yaml文件进行配置。
执行以下命令，基于config.sample.yaml示例配置文件生成一份名为config.yaml的配置文件
#cd /home/kubefusion-litebox-v1.5.6/
# cp config.sample.yaml config.yaml
参照“config.yaml”自定义配置参数，执行如下命令进入config.yaml文件编辑界面。
$ vim config.yaml
按【I】键进入编辑模式，根据前面章节的确定的参数修改config.yaml文件对应的配置内容：
UPF节点名称：gd-gz-gdlt-upf01；
K8s地址：172.16.100.50；
物理机绑核方案：12-23, 29-47（本文档模板样例），或者是0-9,20-29；
防火墙白名单：ufw.enabled设置为true，并填写放通的IP地址；
其他参数，采用默认配置即可；
修改后的示例配置如下（其中蓝色标记内容为根据现网配置必须修改项）：
	# 设置主机名	
hostname: gd-gz-gdlt-upf01           #UPF节点名称
# 设置时间同步服务器，ntp的server IP
ntp_servers:
  - 1.0.144.134
  - 1.0.144.130
# 设置kubernetes的master角色
masters:
  - 172.16.100.50                    #K8s 地址
# 设置kubernetes pod网段和service网段
networking:
  pod_subnet: 100.64.0.0/24
  service_subnet: 10.96.0.0/22
# 设置CPU资源隔离，系统进程和非Guaranteed Pod运行在CPU保留资源区间内，Guaranteed Pod运行在区间外
cpu_manager_policy:
  enabled: true
  reserved_system_cpus: "12-23,29-47"      #这里填写的CPU是预留给操作系统使用
# 设置HugePage，upf默认使用2MiB的大页内存
hugepage:
  enabled: true
  total: 1280
# 设置secure registry, 注意：如启用，必须将证书放在自定义路径下
registry:
  enabled: "false"
  domain: "repository.cucc.cn:13380"
  host: "172.17.10.197"
  ca_file: "/root/ca.crt"
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[630], word/document.xml/body/p[631], word/document.xml/body/p[632], word/document.xml/body/p[633], word/document.xml/body/p[634], word/document.xml/body/p[635], word/document.xml/body/p[636], word/document.xml/body/p[637], word/document.xml/body/p[638], word/document.xml/body/p[639], word/document.xml/body/p[640], word/document.xml/body/p[641], word/document.xml/body/p[642], word/document.xml/body/p[644], word/document.xml/body/p[645], word/document.xml/body/p[646], word/document.xml/body/p[647], word/document.xml/body/p[649], word/document.xml/body/p[650], word/document.xml/body/p[651], word/document.xml/body/p[652], word/document.xml/body/p[654], word/document.xml/body/p[655], word/document.xml/body/p[656], word/document.xml/body/p[657], word/document.xml/body/p[658], word/document.xml/body/p[659], word/document.xml/body/p[660] · `chunk-058b942e931659f44495305e`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
# 设置主机防火墙, 放通IP白名单
ufw:
  enabled: true
    ipv4:
  whitelist:
      - 1.73.6.70/32
      - 1.73.6.59/32
      - 1.73.6.60/32
      - 1.0.144.134/32                   #放通ntp的server ip
      - 1.0.144.130/32                   #放通ntp的server ip
    ipv6:
      - 2408:8142:60ff:fc01:1706:406::/128
      - 2408:8142:60ff:fc02:1706:406::/128
# 编译安装ice网卡驱动
ice_driver:
  enabled: true
  version: 1.7.16
# 安装Intel Ethernet Port Configuration Tool
epct_tool:
  enabled: true
  version: 1.39.32.5
# 启用k8s可选插件, 部分UPF依赖插件已默认启用
addons:
  sealos: 4.3.7
  kubernetes:
    image: docker.io/labring/kubernetes:v1.25.11-4.3.3
  network_plugin:
    image: docker.io/labring/calico:v3.26.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[661] · `chunk-3a8216a32c845db4f16ce088`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
  helm:
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[662], word/document.xml/body/p[663], word/document.xml/body/p[664], word/document.xml/body/p[665], word/document.xml/body/p[666], word/document.xml/body/p[667], word/document.xml/body/p[668], word/document.xml/body/p[669], word/document.xml/body/p[670], word/document.xml/body/p[671], word/document.xml/body/p[672], word/document.xml/body/p[673], word/document.xml/body/p[674], word/document.xml/body/p[675], word/document.xml/body/p[676], word/document.xml/body/p[677], word/document.xml/body/p[678], word/document.xml/body/p[679], word/document.xml/body/p[680], word/document.xml/body/p[681], word/document.xml/body/p[682], word/document.xml/body/p[683], word/document.xml/body/p[684], word/document.xml/body/p[685], word/document.xml/body/p[686], word/document.xml/body/p[687], word/document.xml/body/p[688], word/document.xml/body/p[689], word/document.xml/body/p[690], word/document.xml/body/p[691], word/document.xml/body/p[692], word/document.xml/body/p[693], word/document.xml/body/p[694], word/document.xml/body/p[695], word/document.xml/body/p[696], word/document.xml/body/p[697], word/document.xml/body/p[698], word/document.xml/body/p[699], word/document.xml/body/p[700], word/document.xml/body/p[701], word/document.xml/body/p[702], word/document.xml/body/p[703], word/document.xml/body/p[704], word/document.xml/body/p[705], word/document.xml/body/p[706], word/document.xml/body/p[707], word/document.xml/body/p[708], word/document.xml/body/p[709], word/document.xml/body/p[710], word/document.xml/body/p[711], word/document.xml/body/p[712], word/document.xml/body/p[713], word/document.xml/body/p[714], word/document.xml/body/p[715], word/document.xml/body/p[716], word/document.xml/body/p[717], word/document.xml/body/p[718], word/document.xml/body/p[719], word/document.xml/body/p[720], word/document.xml/body/p[721] · `chunk-b2994271d108a44a0af2c5c4`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
    image: docker.io/labring/helm:v3.12.0
  nfs_subdir_external_provisioner:
    enabled: true
    image: docker.io/labring/nfs-subdir-external-provisioner:v4.0.18
  openebs:
    enabled: true
    image: docker.io/labring/openebs:v3.3.0
  ingress_nginx:
    enabled: true
    image: docker.io/labring/ingress-nginx:v1.6.4
  metrics_server:
    enabled: true
    image: docker.io/labring/metrics-server:v0.6.2
  prometheus:
    enabled: true
    https: false
    image: docker.io/labring/kube-prometheus-stack:v0.63.0
  promtail:
    enabled: true
    loki_url: http://loki-gateway/loki/api/v1/push
    image: docker.io/labring/promtail:v2.8.3
  multus_cni:
    enabled: true
    image: docker.io/labring/multus-cni:v3.9.3
  cni_plugins:
    enabled: true
    image: docker.io/labring/cni-plugins:v1.3.0
  bond_cni:
    enabled: true
    image: docker.io/labring/bond-cni:latest
  mano_admin_user:
    enabled: true
  nerdctl:
    enabled: true
    image: docker.io/labring/nerdctl:v1.2.1
  calicoctl:
    enabled: true
    image: docker.io/labring/calicoctl:v3.26.1
  etcdctl:
    enabled: true
    image: docker.io/labring/etcdctl:v3.5.6
  helmfile:
    enabled: true
    image: docker.io/labring/helmfile:v0.154.0
  sriov:
    enabled: false
    image: docker.io/labring/sriov-network-operator:v1.2.0
  loki_stack:
    enabled: false
    image: docker.io/labring/loki-stack:v2.6.1
  neuvector:
    enabled: false
    image: docker.io/labring/neuvector:v5.1.0
  kubernetes_dashboard:
    enabled: false
    image: docker.io/labring/kubernetes-dashboard:v2.7.0
配置参数参数说明：
hostname: 该主机需要配置的主机名
ntp_servers: 设置ntp服务器器的IP地址或域名
masters: 填写单节点IP地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[722], word/document.xml/body/p[723], word/document.xml/body/p[724], word/document.xml/body/p[725], word/document.xml/body/p[726], word/document.xml/body/p[727], word/document.xml/body/p[728], word/document.xml/body/p[729], word/document.xml/body/p[730] · `chunk-cd18895bc25d33c17477326a`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
networking：k8s podcidr以及service cidr
cpu_manager_policy：为UPFD启用CPU隔离
registry：5gc镜像仓库信息，配置集群与5gc registry仓库对接
ufw：防火墙信息，这里主要是配置放通的IP白名单
ice_driver：ice网卡驱动
epct_tool：intel以太网端口配置工具
Addons：启用或禁用可选插件
Prometheus，数据信息采集，对应的https默认为false
配置文件修改完成，按【ESC】键，输入“:wq”，保存并退出vim编辑器。
```
- 预期原文/缺口：
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
    image: docker.io/labring/helm:v3.12.0
  nfs_subdir_external_provisioner:
    enabled: true
    image: docker.io/labring/nfs-subdir-external-provisioner:v4.0.18
  openebs:
    enabled: true
    image: docker.io/labring/openebs:v3.3.0
  ingress_nginx:
    enabled: true
    image: docker.io/labring/ingress-nginx:v1.6.4
  metrics_server:
    enabled: true
    image: docker.io/labring/metrics-server:v0.6.2
  prometheus:
    enabled: true
    https: false
    image: docker.io/labring/kube-prometheus-stack:v0.63.0
  promtail:
    enabled: true
    loki_url: http://loki-gateway/loki/api/v1/push
    image: docker.io/labring/promtail:v2.8.3
  multus_cni:
    enabled: true
    image: docker.io/labring/multus-cni:v3.9.3
  cni_plugins:
    enabled: true
    image: docker.io/labring/cni-plugins:v1.3.0
  bond_cni:
    enabled: true
    image: docker.io/labring/bond-cni:latest
  mano_admin_user:
    enabled: true
  nerdctl:
    enabled: true
    image: docker.io/labring/nerdctl:v1.2.1
  calicoctl:
    enabled: true
    image: docker.io/labring/calicoctl:v3.26.1
  etcdctl:
    enabled: true
    image: docker.io/labring/etcdctl:v3.5.6
  helmfile:
    enabled: true
    image: docker.io/labring/helmfile:v0.154.0
  sriov:
    enabled: false
    image: docker.io/labring/sriov-network-operator:v1.2.0
  loki_stack:
    enabled: false
    image: docker.io/labring/loki-stack:v2.6.1
  neuvector:
    enabled: false
    image: docker.io/labring/neuvector:v5.1.0
  kubernetes_dashboard:
    enabled: false
    image: docker.io/labring/kubernetes-dashboard:v2.7.0
配置参数参数说明：
hostname: 该主机需要配置的主机名
ntp_servers: 设置ntp服务器器的IP地址或域名
masters: 填写单节点IP地址
```

## knowledge-006 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘单节点部署K8S / 调整集群配置 / 调整后的集群配置文件’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-6dbbd25d0bcb9b848452, manual-topic:section-6dbbd25d0bcb9b848452
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[581], word/document.xml/body/p[582], word/document.xml/body/p[583], word/document.xml/body/p[584], word/document.xml/body/p[585], word/document.xml/body/p[587], word/document.xml/body/p[588], word/document.xml/body/p[589], word/document.xml/body/p[590], word/document.xml/body/p[591], word/document.xml/body/p[592], word/document.xml/body/p[593], word/document.xml/body/p[594], word/document.xml/body/p[595], word/document.xml/body/p[596], word/document.xml/body/p[597], word/document.xml/body/p[599], word/document.xml/body/p[600], word/document.xml/body/p[601], word/document.xml/body/p[602], word/document.xml/body/p[604], word/document.xml/body/p[605], word/document.xml/body/p[606], word/document.xml/body/p[608], word/document.xml/body/p[609], word/document.xml/body/p[610], word/document.xml/body/p[611], word/document.xml/body/p[613], word/document.xml/body/p[614], word/document.xml/body/p[615], word/document.xml/body/p[616], word/document.xml/body/p[618], word/document.xml/body/p[619], word/document.xml/body/p[620], word/document.xml/body/p[621], word/document.xml/body/p[623], word/document.xml/body/p[624], word/document.xml/body/p[625], word/document.xml/body/p[626], word/document.xml/body/p[627], word/document.xml/body/p[628] · `chunk-c0269e0f5f90744584380ab7`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
调整后的集群配置文件
部署集群前，需要新建并调整集群配置文件，当前集群自定义参数通过config.yaml文件进行配置。
执行以下命令，基于config.sample.yaml示例配置文件生成一份名为config.yaml的配置文件
#cd /home/kubefusion-litebox-v1.5.6/
# cp config.sample.yaml config.yaml
参照“config.yaml”自定义配置参数，执行如下命令进入config.yaml文件编辑界面。
$ vim config.yaml
按【I】键进入编辑模式，根据前面章节的确定的参数修改config.yaml文件对应的配置内容：
UPF节点名称：gd-gz-gdlt-upf01；
K8s地址：172.16.100.50；
物理机绑核方案：12-23, 29-47（本文档模板样例），或者是0-9,20-29；
防火墙白名单：ufw.enabled设置为true，并填写放通的IP地址；
其他参数，采用默认配置即可；
修改后的示例配置如下（其中蓝色标记内容为根据现网配置必须修改项）：
	# 设置主机名	
hostname: gd-gz-gdlt-upf01           #UPF节点名称
# 设置时间同步服务器，ntp的server IP
ntp_servers:
  - 1.0.144.134
  - 1.0.144.130
# 设置kubernetes的master角色
masters:
  - 172.16.100.50                    #K8s 地址
# 设置kubernetes pod网段和service网段
networking:
  pod_subnet: 100.64.0.0/24
  service_subnet: 10.96.0.0/22
# 设置CPU资源隔离，系统进程和非Guaranteed Pod运行在CPU保留资源区间内，Guaranteed Pod运行在区间外
cpu_manager_policy:
  enabled: true
  reserved_system_cpus: "12-23,29-47"      #这里填写的CPU是预留给操作系统使用
# 设置HugePage，upf默认使用2MiB的大页内存
hugepage:
  enabled: true
  total: 1280
# 设置secure registry, 注意：如启用，必须将证书放在自定义路径下
registry:
  enabled: "false"
  domain: "repository.cucc.cn:13380"
  host: "172.17.10.197"
  ca_file: "/root/ca.crt"
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[630], word/document.xml/body/p[631], word/document.xml/body/p[632], word/document.xml/body/p[633], word/document.xml/body/p[634], word/document.xml/body/p[635], word/document.xml/body/p[636], word/document.xml/body/p[637], word/document.xml/body/p[638], word/document.xml/body/p[639], word/document.xml/body/p[640], word/document.xml/body/p[641], word/document.xml/body/p[642], word/document.xml/body/p[644], word/document.xml/body/p[645], word/document.xml/body/p[646], word/document.xml/body/p[647], word/document.xml/body/p[649], word/document.xml/body/p[650], word/document.xml/body/p[651], word/document.xml/body/p[652], word/document.xml/body/p[654], word/document.xml/body/p[655], word/document.xml/body/p[656], word/document.xml/body/p[657], word/document.xml/body/p[658], word/document.xml/body/p[659], word/document.xml/body/p[660] · `chunk-058b942e931659f44495305e`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
# 设置主机防火墙, 放通IP白名单
ufw:
  enabled: true
    ipv4:
  whitelist:
      - 1.73.6.70/32
      - 1.73.6.59/32
      - 1.73.6.60/32
      - 1.0.144.134/32                   #放通ntp的server ip
      - 1.0.144.130/32                   #放通ntp的server ip
    ipv6:
      - 2408:8142:60ff:fc01:1706:406::/128
      - 2408:8142:60ff:fc02:1706:406::/128
# 编译安装ice网卡驱动
ice_driver:
  enabled: true
  version: 1.7.16
# 安装Intel Ethernet Port Configuration Tool
epct_tool:
  enabled: true
  version: 1.39.32.5
# 启用k8s可选插件, 部分UPF依赖插件已默认启用
addons:
  sealos: 4.3.7
  kubernetes:
    image: docker.io/labring/kubernetes:v1.25.11-4.3.3
  network_plugin:
    image: docker.io/labring/calico:v3.26.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[661] · `chunk-3a8216a32c845db4f16ce088`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
  helm:
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[662], word/document.xml/body/p[663], word/document.xml/body/p[664], word/document.xml/body/p[665], word/document.xml/body/p[666], word/document.xml/body/p[667], word/document.xml/body/p[668], word/document.xml/body/p[669], word/document.xml/body/p[670], word/document.xml/body/p[671], word/document.xml/body/p[672], word/document.xml/body/p[673], word/document.xml/body/p[674], word/document.xml/body/p[675], word/document.xml/body/p[676], word/document.xml/body/p[677], word/document.xml/body/p[678], word/document.xml/body/p[679], word/document.xml/body/p[680], word/document.xml/body/p[681], word/document.xml/body/p[682], word/document.xml/body/p[683], word/document.xml/body/p[684], word/document.xml/body/p[685], word/document.xml/body/p[686], word/document.xml/body/p[687], word/document.xml/body/p[688], word/document.xml/body/p[689], word/document.xml/body/p[690], word/document.xml/body/p[691], word/document.xml/body/p[692], word/document.xml/body/p[693], word/document.xml/body/p[694], word/document.xml/body/p[695], word/document.xml/body/p[696], word/document.xml/body/p[697], word/document.xml/body/p[698], word/document.xml/body/p[699], word/document.xml/body/p[700], word/document.xml/body/p[701], word/document.xml/body/p[702], word/document.xml/body/p[703], word/document.xml/body/p[704], word/document.xml/body/p[705], word/document.xml/body/p[706], word/document.xml/body/p[707], word/document.xml/body/p[708], word/document.xml/body/p[709], word/document.xml/body/p[710], word/document.xml/body/p[711], word/document.xml/body/p[712], word/document.xml/body/p[713], word/document.xml/body/p[714], word/document.xml/body/p[715], word/document.xml/body/p[716], word/document.xml/body/p[717], word/document.xml/body/p[718], word/document.xml/body/p[719], word/document.xml/body/p[720], word/document.xml/body/p[721] · `chunk-b2994271d108a44a0af2c5c4`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
    image: docker.io/labring/helm:v3.12.0
  nfs_subdir_external_provisioner:
    enabled: true
    image: docker.io/labring/nfs-subdir-external-provisioner:v4.0.18
  openebs:
    enabled: true
    image: docker.io/labring/openebs:v3.3.0
  ingress_nginx:
    enabled: true
    image: docker.io/labring/ingress-nginx:v1.6.4
  metrics_server:
    enabled: true
    image: docker.io/labring/metrics-server:v0.6.2
  prometheus:
    enabled: true
    https: false
    image: docker.io/labring/kube-prometheus-stack:v0.63.0
  promtail:
    enabled: true
    loki_url: http://loki-gateway/loki/api/v1/push
    image: docker.io/labring/promtail:v2.8.3
  multus_cni:
    enabled: true
    image: docker.io/labring/multus-cni:v3.9.3
  cni_plugins:
    enabled: true
    image: docker.io/labring/cni-plugins:v1.3.0
  bond_cni:
    enabled: true
    image: docker.io/labring/bond-cni:latest
  mano_admin_user:
    enabled: true
  nerdctl:
    enabled: true
    image: docker.io/labring/nerdctl:v1.2.1
  calicoctl:
    enabled: true
    image: docker.io/labring/calicoctl:v3.26.1
  etcdctl:
    enabled: true
    image: docker.io/labring/etcdctl:v3.5.6
  helmfile:
    enabled: true
    image: docker.io/labring/helmfile:v0.154.0
  sriov:
    enabled: false
    image: docker.io/labring/sriov-network-operator:v1.2.0
  loki_stack:
    enabled: false
    image: docker.io/labring/loki-stack:v2.6.1
  neuvector:
    enabled: false
    image: docker.io/labring/neuvector:v5.1.0
  kubernetes_dashboard:
    enabled: false
    image: docker.io/labring/kubernetes-dashboard:v2.7.0
配置参数参数说明：
hostname: 该主机需要配置的主机名
ntp_servers: 设置ntp服务器器的IP地址或域名
masters: 填写单节点IP地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[722], word/document.xml/body/p[723], word/document.xml/body/p[724], word/document.xml/body/p[725], word/document.xml/body/p[726], word/document.xml/body/p[727], word/document.xml/body/p[728], word/document.xml/body/p[729], word/document.xml/body/p[730] · `chunk-cd18895bc25d33c17477326a`
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
networking：k8s podcidr以及service cidr
cpu_manager_policy：为UPFD启用CPU隔离
registry：5gc镜像仓库信息，配置集群与5gc registry仓库对接
ufw：防火墙信息，这里主要是配置放通的IP白名单
ice_driver：ice网卡驱动
epct_tool：intel以太网端口配置工具
Addons：启用或禁用可选插件
Prometheus，数据信息采集，对应的https默认为false
配置文件修改完成，按【ESC】键，输入“:wq”，保存并退出vim编辑器。
```
- 预期原文/缺口：
```text
单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
    image: docker.io/labring/helm:v3.12.0
  nfs_subdir_external_provisioner:
    enabled: true
    image: docker.io/labring/nfs-subdir-external-provisioner:v4.0.18
  openebs:
    enabled: true
    image: docker.io/labring/openebs:v3.3.0
  ingress_nginx:
    enabled: true
    image: docker.io/labring/ingress-nginx:v1.6.4
  metrics_server:
    enabled: true
    image: docker.io/labring/metrics-server:v0.6.2
  prometheus:
    enabled: true
    https: false
    image: docker.io/labring/kube-prometheus-stack:v0.63.0
  promtail:
    enabled: true
    loki_url: http://loki-gateway/loki/api/v1/push
    image: docker.io/labring/promtail:v2.8.3
  multus_cni:
    enabled: true
    image: docker.io/labring/multus-cni:v3.9.3
  cni_plugins:
    enabled: true
    image: docker.io/labring/cni-plugins:v1.3.0
  bond_cni:
    enabled: true
    image: docker.io/labring/bond-cni:latest
  mano_admin_user:
    enabled: true
  nerdctl:
    enabled: true
    image: docker.io/labring/nerdctl:v1.2.1
  calicoctl:
    enabled: true
    image: docker.io/labring/calicoctl:v3.26.1
  etcdctl:
    enabled: true
    image: docker.io/labring/etcdctl:v3.5.6
  helmfile:
    enabled: true
    image: docker.io/labring/helmfile:v0.154.0
  sriov:
    enabled: false
    image: docker.io/labring/sriov-network-operator:v1.2.0
  loki_stack:
    enabled: false
    image: docker.io/labring/loki-stack:v2.6.1
  neuvector:
    enabled: false
    image: docker.io/labring/neuvector:v5.1.0
  kubernetes_dashboard:
    enabled: false
    image: docker.io/labring/kubernetes-dashboard:v2.7.0
配置参数参数说明：
hostname: 该主机需要配置的主机名
ntp_servers: 设置ntp服务器器的IP地址或域名
masters: 填写单节点IP地址
```

## knowledge-007 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-1cf8c31e67717c0307e3, manual-topic:section-1cf8c31e67717c0307e3
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[906], word/document.xml/body/p[907], word/document.xml/body/p[908], word/document.xml/body/p[909], word/document.xml/body/p[910], word/document.xml/body/p[911], word/document.xml/body/p[912], word/document.xml/body/p[913], word/document.xml/body/p[914], word/document.xml/body/p[915], word/document.xml/body/p[916], word/document.xml/body/p[917], word/document.xml/body/p[918], word/document.xml/body/p[919], word/document.xml/body/p[920], word/document.xml/body/p[921], word/document.xml/body/p[922], word/document.xml/body/p[923], word/document.xml/body/p[924], word/document.xml/body/p[925], word/document.xml/body/p[926], word/document.xml/body/p[927], word/document.xml/body/p[928], word/document.xml/body/p[929], word/document.xml/body/p[930], word/document.xml/body/p[931], word/document.xml/body/p[932], word/document.xml/body/p[933], word/document.xml/body/p[934], word/document.xml/body/p[935], word/document.xml/body/p[936], word/document.xml/body/p[937], word/document.xml/body/p[938], word/document.xml/body/p[939], word/document.xml/body/p[940], word/document.xml/body/p[941], word/document.xml/body/p[942] · `chunk-ca730d6f31271f28eab01fa5`
```text
单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件
 调整后的配置文件
注意：现网环境需要根据实际服务器（如：H3C、Soc、中兴等）不同配置、不同网卡配置（ens16f0、ens16f1、enp24s0f0、enp24s0f1、ens1f0、ens3f0、ens3f0、ens3f1等）和VlanId规划等灵活调整实际的配置参数。
基于前面 REF _Ref12620 \r \h 5.1.3.2到 REF _Ref12642 \r \h 5.1.3.7章节描述，调整后的配置文件参数示例如下：
base:
  namespace: ns1                      # 设置UPF命令空间
  upf_version: 5.0.210                   # UPF软件包版本
  vdos_version: 1.0.5
  instanceId: "1"
  neId: "559991"                       # 设置UPF NEID
  upfd_cpu: "9"                        # 设置UPF最大CPU数量
  upfd_memory: "10Gi"
networking:
  intf_mode: 1 # 0-seperated,1-combined #UPF N3/N6合设、分设模式选择：1表示合设
  bond:
    enabled: true                      #UPF N3/N6 网卡是Bond模式，默认配置为true
  vlan:
    enabled: false                      #默认配置为false，对端交换机配置为：动态lacp，Access
  n3:
    nics:
      - ens1f0                         #UPF N3 网卡1
      - ens3f0                         #UPF N3 网卡2
    vlan:
      - 200                           #UPF N3 VlanId
  n6:
    nics:
      - ens1f1                         #UPF N6 网卡1
      - ens3f1                         #UPF N6 网卡2
    vlan:
      - 400                            #UPF N6 VlanId
  n9:
    enabled: false                       #UPF N9 默认配置为false
    vlan:
      - 300
n4:
  bond:                                #UPF N4网卡是Bond模式，和K8s共口部署
    enabled: false                       #默认配置为false，前面部署K8s时已经在host机netplan配置
  nics:
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[943], word/document.xml/body/p[944], word/document.xml/body/p[945], word/document.xml/body/p[946], word/document.xml/body/p[947], word/document.xml/body/p[948], word/document.xml/body/p[949], word/document.xml/body/p[950], word/document.xml/body/p[951], word/document.xml/body/p[952], word/document.xml/body/p[953], word/document.xml/body/p[954], word/document.xml/body/p[955], word/document.xml/body/p[956], word/document.xml/body/p[957], word/document.xml/body/p[958], word/document.xml/body/p[959], word/document.xml/body/p[960], word/document.xml/body/p[961], word/document.xml/body/p[962], word/document.xml/body/p[963], word/document.xml/body/p[964], word/document.xml/body/p[965], word/document.xml/body/p[966], word/document.xml/body/p[967], word/document.xml/body/p[968], word/document.xml/body/p[969], word/document.xml/body/p[970], word/document.xml/body/p[971], word/document.xml/body/p[972], word/document.xml/body/p[973], word/document.xml/body/p[974], word/document.xml/body/p[975], word/document.xml/body/p[976], word/document.xml/body/p[977] · `chunk-881735f8ec04a52b4f3444a3`
```text
单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件
    - bond0.299                        #UPF N4网卡接口，这里是使用子接口
  vlan:
    enabled: false                       #默认配置为false，对端交换机配置为：动态lacp，Trunk
    id: 299                             #UPF N4 VlanId
  ipv4:
    enabled: false                       #默认配置为false，通过网管配置下发
    address: "100.101.1.55/24"
    gateway: "100.101.1.1"
    service_ip: "100.101.1.55"
  ipv6:
    enabled: false                       #默认配置为false，通过网管配置下发
    address: "2404::4:55/64"
    gateway: "2404::4:254"
  intf_mode: 1 # 0-seperated,1-combined  #UPF N4合设、分设模式选择：1表示合设
cpu:
  #main: 1
  #worker: 2-9
  queue_number: 2
配置参数分为五个部分：
base：配置upf helm chart参数
networking：配置UPF N3、N6参数
n4：配置UPF N4参数
cpu：配置upf 应用startup.conf启动文件参数
base部分参数说明：
namespace：  upf及vdos部署的命名空间
upf_version：  upf版本号，通过发布的软件包识别版本号
vdos_version：  vdos版本号，通过发布的软件包识别版本号
instanceId：   upf实例化ID
neId：        由网管系统同一分配的
networking部分参数说明：
networking.intf_mode：UPF N3/N6合设、分设模式选择：1表示合设，0表示分设。
networking.bond.enabled：N3和N6使用bond模式开关，即是否启用bond模式，如果为true则使用bond模式下的nic配置，此时networking.nic部分必须是2张网卡。
networking.vlan.enabled：N3和N6配置vlan id开关，即networking.n3.vlan和networking.n6.vlan是否仍然有效。
networking.n3.nic：N3对应的物理网卡，如果networking.bond.enabled设置为true，这里必须是2张网卡，否则会提示错误；
networking.n3.vlan：N3 vlan id
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[978], word/document.xml/body/p[979], word/document.xml/body/p[980], word/document.xml/body/p[981], word/document.xml/body/p[982], word/document.xml/body/p[983], word/document.xml/body/p[984], word/document.xml/body/p[985], word/document.xml/body/p[986], word/document.xml/body/p[987] · `chunk-4d32b50bac01142b9eb8c38b`
```text
单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件
networking.n6.nic：N6对应的物理网卡，如果networking.bond.enabled设置为true，这里必须是2张网卡，否则会提示错误。
networking.n6.vlan：N6 vlan id
其他参数无特殊需求可暂时保持默认，如需扩展配置，可修改helmfile.yaml中的helm values参数。
N4部分参数说明：
n4.bond.enabled：N4使用bond模式开关，即是否启用bond模式，如果为true则使用bond模式下的nic配置，此时networking.nic部分必须是2张网卡。
n4.nic：N4对应的物理网卡，如果networking.bond.enabled设置为true，这里必须是2张网卡，否则会提示错误。
n4.vlan.enabled：N4配置vlan id开关，如果为true则networking.n4.vlan.id有效，否则networking.n4.vlan.id无效。
n4.vlan.id：N4 vlan id
n4.intf_mode：UPF N4合设、分设模式选择：1表示合设，0表示分设。
其他参数无特殊需求可暂时保持默认，如需扩展配置，可修改helmfile.yaml中的helm values参数。
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件
    - bond0.299                        #UPF N4网卡接口，这里是使用子接口
  vlan:
    enabled: false                       #默认配置为false，对端交换机配置为：动态lacp，Trunk
    id: 299                             #UPF N4 VlanId
  ipv4:
    enabled: false                       #默认配置为false，通过网管配置下发
    address: "100.101.1.55/24"
    gateway: "100.101.1.1"
    service_ip: "100.101.1.55"
  ipv6:
    enabled: false                       #默认配置为false，通过网管配置下发
    address: "2404::4:55/64"
    gateway: "2404::4:254"
  intf_mode: 1 # 0-seperated,1-combined  #UPF N4合设、分设模式选择：1表示合设
cpu:
  #main: 1
  #worker: 2-9
  queue_number: 2
配置参数分为五个部分：
base：配置upf helm chart参数
networking：配置UPF N3、N6参数
n4：配置UPF N4参数
cpu：配置upf 应用startup.conf启动文件参数
base部分参数说明：
namespace：  upf及vdos部署的命名空间
upf_version：  upf版本号，通过发布的软件包识别版本号
vdos_version：  vdos版本号，通过发布的软件包识别版本号
instanceId：   upf实例化ID
neId：        由网管系统同一分配的
networking部分参数说明：
networking.intf_mode：UPF N3/N6合设、分设模式选择：1表示合设，0表示分设。
networking.bond.enabled：N3和N6使用bond模式开关，即是否启用bond模式，如果为true则使用bond模式下的nic配置，此时networking.nic部分必须是2张网卡。
networking.vlan.enabled：N3和N6配置vlan id开关，即networking.n3.vlan和networking.n6.vlan是否仍然有效。
networking.n3.nic：N3对应的物理网卡，如果networking.bond.enabled设置为true，这里必须是2张网卡，否则会提示错误；
networking.n3.vlan：N3 vlan id
```

## knowledge-008 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-1cf8c31e67717c0307e3, manual-topic:section-1cf8c31e67717c0307e3
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[906], word/document.xml/body/p[907], word/document.xml/body/p[908], word/document.xml/body/p[909], word/document.xml/body/p[910], word/document.xml/body/p[911], word/document.xml/body/p[912], word/document.xml/body/p[913], word/document.xml/body/p[914], word/document.xml/body/p[915], word/document.xml/body/p[916], word/document.xml/body/p[917], word/document.xml/body/p[918], word/document.xml/body/p[919], word/document.xml/body/p[920], word/document.xml/body/p[921], word/document.xml/body/p[922], word/document.xml/body/p[923], word/document.xml/body/p[924], word/document.xml/body/p[925], word/document.xml/body/p[926], word/document.xml/body/p[927], word/document.xml/body/p[928], word/document.xml/body/p[929], word/document.xml/body/p[930], word/document.xml/body/p[931], word/document.xml/body/p[932], word/document.xml/body/p[933], word/document.xml/body/p[934], word/document.xml/body/p[935], word/document.xml/body/p[936], word/document.xml/body/p[937], word/document.xml/body/p[938], word/document.xml/body/p[939], word/document.xml/body/p[940], word/document.xml/body/p[941], word/document.xml/body/p[942] · `chunk-ca730d6f31271f28eab01fa5`
```text
单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件
 调整后的配置文件
注意：现网环境需要根据实际服务器（如：H3C、Soc、中兴等）不同配置、不同网卡配置（ens16f0、ens16f1、enp24s0f0、enp24s0f1、ens1f0、ens3f0、ens3f0、ens3f1等）和VlanId规划等灵活调整实际的配置参数。
基于前面 REF _Ref12620 \r \h 5.1.3.2到 REF _Ref12642 \r \h 5.1.3.7章节描述，调整后的配置文件参数示例如下：
base:
  namespace: ns1                      # 设置UPF命令空间
  upf_version: 5.0.210                   # UPF软件包版本
  vdos_version: 1.0.5
  instanceId: "1"
  neId: "559991"                       # 设置UPF NEID
  upfd_cpu: "9"                        # 设置UPF最大CPU数量
  upfd_memory: "10Gi"
networking:
  intf_mode: 1 # 0-seperated,1-combined #UPF N3/N6合设、分设模式选择：1表示合设
  bond:
    enabled: true                      #UPF N3/N6 网卡是Bond模式，默认配置为true
  vlan:
    enabled: false                      #默认配置为false，对端交换机配置为：动态lacp，Access
  n3:
    nics:
      - ens1f0                         #UPF N3 网卡1
      - ens3f0                         #UPF N3 网卡2
    vlan:
      - 200                           #UPF N3 VlanId
  n6:
    nics:
      - ens1f1                         #UPF N6 网卡1
      - ens3f1                         #UPF N6 网卡2
    vlan:
      - 400                            #UPF N6 VlanId
  n9:
    enabled: false                       #UPF N9 默认配置为false
    vlan:
      - 300
n4:
  bond:                                #UPF N4网卡是Bond模式，和K8s共口部署
    enabled: false                       #默认配置为false，前面部署K8s时已经在host机netplan配置
  nics:
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[943], word/document.xml/body/p[944], word/document.xml/body/p[945], word/document.xml/body/p[946], word/document.xml/body/p[947], word/document.xml/body/p[948], word/document.xml/body/p[949], word/document.xml/body/p[950], word/document.xml/body/p[951], word/document.xml/body/p[952], word/document.xml/body/p[953], word/document.xml/body/p[954], word/document.xml/body/p[955], word/document.xml/body/p[956], word/document.xml/body/p[957], word/document.xml/body/p[958], word/document.xml/body/p[959], word/document.xml/body/p[960], word/document.xml/body/p[961], word/document.xml/body/p[962], word/document.xml/body/p[963], word/document.xml/body/p[964], word/document.xml/body/p[965], word/document.xml/body/p[966], word/document.xml/body/p[967], word/document.xml/body/p[968], word/document.xml/body/p[969], word/document.xml/body/p[970], word/document.xml/body/p[971], word/document.xml/body/p[972], word/document.xml/body/p[973], word/document.xml/body/p[974], word/document.xml/body/p[975], word/document.xml/body/p[976], word/document.xml/body/p[977] · `chunk-881735f8ec04a52b4f3444a3`
```text
单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件
    - bond0.299                        #UPF N4网卡接口，这里是使用子接口
  vlan:
    enabled: false                       #默认配置为false，对端交换机配置为：动态lacp，Trunk
    id: 299                             #UPF N4 VlanId
  ipv4:
    enabled: false                       #默认配置为false，通过网管配置下发
    address: "100.101.1.55/24"
    gateway: "100.101.1.1"
    service_ip: "100.101.1.55"
  ipv6:
    enabled: false                       #默认配置为false，通过网管配置下发
    address: "2404::4:55/64"
    gateway: "2404::4:254"
  intf_mode: 1 # 0-seperated,1-combined  #UPF N4合设、分设模式选择：1表示合设
cpu:
  #main: 1
  #worker: 2-9
  queue_number: 2
配置参数分为五个部分：
base：配置upf helm chart参数
networking：配置UPF N3、N6参数
n4：配置UPF N4参数
cpu：配置upf 应用startup.conf启动文件参数
base部分参数说明：
namespace：  upf及vdos部署的命名空间
upf_version：  upf版本号，通过发布的软件包识别版本号
vdos_version：  vdos版本号，通过发布的软件包识别版本号
instanceId：   upf实例化ID
neId：        由网管系统同一分配的
networking部分参数说明：
networking.intf_mode：UPF N3/N6合设、分设模式选择：1表示合设，0表示分设。
networking.bond.enabled：N3和N6使用bond模式开关，即是否启用bond模式，如果为true则使用bond模式下的nic配置，此时networking.nic部分必须是2张网卡。
networking.vlan.enabled：N3和N6配置vlan id开关，即networking.n3.vlan和networking.n6.vlan是否仍然有效。
networking.n3.nic：N3对应的物理网卡，如果networking.bond.enabled设置为true，这里必须是2张网卡，否则会提示错误；
networking.n3.vlan：N3 vlan id
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[978], word/document.xml/body/p[979], word/document.xml/body/p[980], word/document.xml/body/p[981], word/document.xml/body/p[982], word/document.xml/body/p[983], word/document.xml/body/p[984], word/document.xml/body/p[985], word/document.xml/body/p[986], word/document.xml/body/p[987] · `chunk-4d32b50bac01142b9eb8c38b`
```text
单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件
networking.n6.nic：N6对应的物理网卡，如果networking.bond.enabled设置为true，这里必须是2张网卡，否则会提示错误。
networking.n6.vlan：N6 vlan id
其他参数无特殊需求可暂时保持默认，如需扩展配置，可修改helmfile.yaml中的helm values参数。
N4部分参数说明：
n4.bond.enabled：N4使用bond模式开关，即是否启用bond模式，如果为true则使用bond模式下的nic配置，此时networking.nic部分必须是2张网卡。
n4.nic：N4对应的物理网卡，如果networking.bond.enabled设置为true，这里必须是2张网卡，否则会提示错误。
n4.vlan.enabled：N4配置vlan id开关，如果为true则networking.n4.vlan.id有效，否则networking.n4.vlan.id无效。
n4.vlan.id：N4 vlan id
n4.intf_mode：UPF N4合设、分设模式选择：1表示合设，0表示分设。
其他参数无特殊需求可暂时保持默认，如需扩展配置，可修改helmfile.yaml中的helm values参数。
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件
    - bond0.299                        #UPF N4网卡接口，这里是使用子接口
  vlan:
    enabled: false                       #默认配置为false，对端交换机配置为：动态lacp，Trunk
    id: 299                             #UPF N4 VlanId
  ipv4:
    enabled: false                       #默认配置为false，通过网管配置下发
    address: "100.101.1.55/24"
    gateway: "100.101.1.1"
    service_ip: "100.101.1.55"
  ipv6:
    enabled: false                       #默认配置为false，通过网管配置下发
    address: "2404::4:55/64"
    gateway: "2404::4:254"
  intf_mode: 1 # 0-seperated,1-combined  #UPF N4合设、分设模式选择：1表示合设
cpu:
  #main: 1
  #worker: 2-9
  queue_number: 2
配置参数分为五个部分：
base：配置upf helm chart参数
networking：配置UPF N3、N6参数
n4：配置UPF N4参数
cpu：配置upf 应用startup.conf启动文件参数
base部分参数说明：
namespace：  upf及vdos部署的命名空间
upf_version：  upf版本号，通过发布的软件包识别版本号
vdos_version：  vdos版本号，通过发布的软件包识别版本号
instanceId：   upf实例化ID
neId：        由网管系统同一分配的
networking部分参数说明：
networking.intf_mode：UPF N3/N6合设、分设模式选择：1表示合设，0表示分设。
networking.bond.enabled：N3和N6使用bond模式开关，即是否启用bond模式，如果为true则使用bond模式下的nic配置，此时networking.nic部分必须是2张网卡。
networking.vlan.enabled：N3和N6配置vlan id开关，即networking.n3.vlan和networking.n6.vlan是否仍然有效。
networking.n3.nic：N3对应的物理网卡，如果networking.bond.enabled设置为true，这里必须是2张网卡，否则会提示错误；
networking.n3.vlan：N3 vlan id
```

## knowledge-009 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-e84ad9708a71d319b94f, manual-topic:section-e84ad9708a71d319b94f
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1033], word/document.xml/body/p[1034], word/document.xml/body/p[1035] · `chunk-90b8a37655128bab4cb85c5a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
配置UPF各个接口地址
若网管未分配IP地址时可以手动配置，一般通过CURL命令配置接口地址。具体命令格式为：
为接口配置N4 地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1036] · `chunk-21dccc114177dcd35158f743`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "2", InterfaceType = "N4", IPAddressType = "IPv6", IPv6Address = "2404::4:50", IPv6PrefixLen = 64, VRFEnable = "OFF";}' 127.0.0.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1037], word/document.xml/body/p[1038] · `chunk-349d0a04c0da3c79c5dab97b`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
为N3/N6接口配置IP地址
配置N3地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1039] · `chunk-e8683a340f2175d73a20ff1b`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "3", InterfaceType = "N3", IPAddressType = "IPv4", IPv4Address = "100.10.1.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1040] · `chunk-25c5947200b7830954e856cb`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
配置N6地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1041] · `chunk-013b7cb89c91edbafb296e8a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "5", InterfaceType = "N6", IPAddressType = "IPv4", IPv4Address = "174.100.100.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1042] · `chunk-98267f8b46d90c66d2962c52`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
配置N9地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1043] · `chunk-37015f8c510912ff3ba8d98a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "3", InterfaceType = "N3", IPAddressType = "IPv4", IPv4Address = "100.10.1.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1044], word/document.xml/body/p[1045], word/document.xml/body/p[1046], word/document.xml/body/p[1048], word/document.xml/body/p[1049], word/document.xml/body/p[1050], word/document.xml/body/p[1051], word/document.xml/body/p[1052], word/document.xml/body/p[1053], word/document.xml/body/p[1054] · `chunk-8af46eaef600a97d5dc3c07c`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
说明：
其中ns1是UPF对应的namespace；
upf-1.com是通过kubectl get ingress -A命令查询的结果。截图如下：
具体的ADD/DEL/QRY命令则可以参考《中国联通5G专网UPF5.0产品使用手册》、
curl 命令配置完成后，需要重启UPFD 和UPFM 2个POD，具体命令为：
#kubectl delete pod upfm-1-b8fc7f485-hw47c -n ns1
#kubectl delete pod upfd-1-594847d77d-jg6ch -n ns1
或者执行下面命令重启UPFD 和UPFM 2个POD。
# upfmgr restart all
重启UPFD POD，查看接口IP配置是否生效。
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
说明：
其中ns1是UPF对应的namespace；
upf-1.com是通过kubectl get ingress -A命令查询的结果。截图如下：
具体的ADD/DEL/QRY命令则可以参考《中国联通5G专网UPF5.0产品使用手册》、
curl 命令配置完成后，需要重启UPFD 和UPFM 2个POD，具体命令为：
#kubectl delete pod upfm-1-b8fc7f485-hw47c -n ns1
#kubectl delete pod upfd-1-594847d77d-jg6ch -n ns1
或者执行下面命令重启UPFD 和UPFM 2个POD。
# upfmgr restart all
重启UPFD POD，查看接口IP配置是否生效。
```

## knowledge-010 · dev · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-e84ad9708a71d319b94f, manual-topic:section-e84ad9708a71d319b94f
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1033], word/document.xml/body/p[1034], word/document.xml/body/p[1035] · `chunk-90b8a37655128bab4cb85c5a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
配置UPF各个接口地址
若网管未分配IP地址时可以手动配置，一般通过CURL命令配置接口地址。具体命令格式为：
为接口配置N4 地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1036] · `chunk-21dccc114177dcd35158f743`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "2", InterfaceType = "N4", IPAddressType = "IPv6", IPv6Address = "2404::4:50", IPv6PrefixLen = 64, VRFEnable = "OFF";}' 127.0.0.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1037], word/document.xml/body/p[1038] · `chunk-349d0a04c0da3c79c5dab97b`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
为N3/N6接口配置IP地址
配置N3地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1039] · `chunk-e8683a340f2175d73a20ff1b`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "3", InterfaceType = "N3", IPAddressType = "IPv4", IPv4Address = "100.10.1.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1040] · `chunk-25c5947200b7830954e856cb`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
配置N6地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1041] · `chunk-013b7cb89c91edbafb296e8a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "5", InterfaceType = "N6", IPAddressType = "IPv4", IPv4Address = "174.100.100.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1042] · `chunk-98267f8b46d90c66d2962c52`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
配置N9地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1043] · `chunk-37015f8c510912ff3ba8d98a`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "3", InterfaceType = "N3", IPAddressType = "IPv4", IPv4Address = "100.10.1.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1044], word/document.xml/body/p[1045], word/document.xml/body/p[1046], word/document.xml/body/p[1048], word/document.xml/body/p[1049], word/document.xml/body/p[1050], word/document.xml/body/p[1051], word/document.xml/body/p[1052], word/document.xml/body/p[1053], word/document.xml/body/p[1054] · `chunk-8af46eaef600a97d5dc3c07c`
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
说明：
其中ns1是UPF对应的namespace；
upf-1.com是通过kubectl get ingress -A命令查询的结果。截图如下：
具体的ADD/DEL/QRY命令则可以参考《中国联通5G专网UPF5.0产品使用手册》、
curl 命令配置完成后，需要重启UPFD 和UPFM 2个POD，具体命令为：
#kubectl delete pod upfm-1-b8fc7f485-hw47c -n ns1
#kubectl delete pod upfd-1-594847d77d-jg6ch -n ns1
或者执行下面命令重启UPFD 和UPFM 2个POD。
# upfmgr restart all
重启UPFD POD，查看接口IP配置是否生效。
```
- 预期原文/缺口：
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址
说明：
其中ns1是UPF对应的namespace；
upf-1.com是通过kubectl get ingress -A命令查询的结果。截图如下：
具体的ADD/DEL/QRY命令则可以参考《中国联通5G专网UPF5.0产品使用手册》、
curl 命令配置完成后，需要重启UPFD 和UPFM 2个POD，具体命令为：
#kubectl delete pod upfm-1-b8fc7f485-hw47c -n ns1
#kubectl delete pod upfd-1-594847d77d-jg6ch -n ns1
或者执行下面命令重启UPFD 和UPFM 2个POD。
# upfmgr restart all
重启UPFD POD，查看接口IP配置是否生效。
```

## knowledge-011 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘安装5GC业务软件 / 单节点离线部署UPF / 检查upf 网卡配置信息’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-6a428acb07078bec8453, manual-topic:section-6a428acb07078bec8453
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1441], word/document.xml/body/p[1442], word/document.xml/body/p[1443], word/document.xml/body/p[1444], word/document.xml/body/p[1445], word/document.xml/body/p[1446], word/document.xml/body/p[1447], word/document.xml/body/p[1448], word/document.xml/body/p[1449], word/document.xml/body/p[1450], word/document.xml/body/p[1451], word/document.xml/body/p[1452], word/document.xml/body/p[1453], word/document.xml/body/p[1454], word/document.xml/body/p[1456], word/document.xml/body/p[1457], word/document.xml/body/p[1458], word/document.xml/body/p[1459], word/document.xml/body/p[1461], word/document.xml/body/p[1462] · `chunk-8a1cd259f0edea9b15fc3ea3`
```text
安装5GC业务软件 / 单节点离线部署UPF / 检查upf 网卡配置信息
检查upf 网卡配置信息
1）查看生成的multus-cni多网卡插件配置
# cd home/upf_setup_CU5GC_UPF_5.0.210/integration
# ls temp/multus/
host-device-1.yaml  host-device-2.yaml  host-device-3.yaml  host-device-4.yaml  host-device-n4.yaml
配置文件说明
host-device-1.yaml  host-device-2.yaml,用于将N3和N6网卡绑定到pod，使用multus-cni+host-device-cni两个插件实现
host-device-3.yaml用于将N4网卡绑定到pod，，使用multus-cni+vlan-cni两个插件实现，非bond模式时在单个网卡上分配vlan子接口给upfd pod，bond模式时在bond0上分配vlan子接口给upfd pod
2）查看已经绑定用户态驱动vfio-pci的网卡，该网卡是否用于UPF N3/N6接口。
# driverctl list-overrides
0000:17:00.0 vfio-pci
0000:17:00.1 vfio-pci
0000:4b:00.0 vfio-pci
0000:4b:00.1 vfio-pci
或者使用dpdk-devbind.py脚本查看当前节点可用物理网卡
# cd home/upf_setup_CU5GC_UPF_5.0.210/integration
./scripts/dpdk-devbind.py -s
部署UPF前网卡绑定状态示例输出结果如下：
说明：需要运维人员根据组网规划确认哪些网卡用于UPF，以上示例使用enp1f0、enp1f1、enp3f0、enp3f1四块高速以太网卡用于UPF应用的N3/N6。
部署UPF后网卡绑定状态示例输出结果如下：
```
- 预期原文/缺口：
```text
安装5GC业务软件 / 单节点离线部署UPF / 检查upf 网卡配置信息
检查upf 网卡配置信息
1）查看生成的multus-cni多网卡插件配置
# cd home/upf_setup_CU5GC_UPF_5.0.210/integration
# ls temp/multus/
host-device-1.yaml  host-device-2.yaml  host-device-3.yaml  host-device-4.yaml  host-device-n4.yaml
配置文件说明
host-device-1.yaml  host-device-2.yaml,用于将N3和N6网卡绑定到pod，使用multus-cni+host-device-cni两个插件实现
host-device-3.yaml用于将N4网卡绑定到pod，，使用multus-cni+vlan-cni两个插件实现，非bond模式时在单个网卡上分配vlan子接口给upfd pod，bond模式时在bond0上分配vlan子接口给upfd pod
2）查看已经绑定用户态驱动vfio-pci的网卡，该网卡是否用于UPF N3/N6接口。
# driverctl list-overrides
0000:17:00.0 vfio-pci
0000:17:00.1 vfio-pci
0000:4b:00.0 vfio-pci
0000:4b:00.1 vfio-pci
或者使用dpdk-devbind.py脚本查看当前节点可用物理网卡
# cd home/upf_setup_CU5GC_UPF_5.0.210/integration
./scripts/dpdk-devbind.py -s
部署UPF前网卡绑定状态示例输出结果如下：
说明：需要运维人员根据组网规划确认哪些网卡用于UPF，以上示例使用enp1f0、enp1f1、enp3f0、enp3f1四块高速以太网卡用于UPF应用的N3/N6。
部署UPF后网卡绑定状态示例输出结果如下：
```

## knowledge-012 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘安装5GC业务软件 / 单节点离线部署UPF / 检查upf 网卡配置信息’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-6a428acb07078bec8453, manual-topic:section-6a428acb07078bec8453
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1441], word/document.xml/body/p[1442], word/document.xml/body/p[1443], word/document.xml/body/p[1444], word/document.xml/body/p[1445], word/document.xml/body/p[1446], word/document.xml/body/p[1447], word/document.xml/body/p[1448], word/document.xml/body/p[1449], word/document.xml/body/p[1450], word/document.xml/body/p[1451], word/document.xml/body/p[1452], word/document.xml/body/p[1453], word/document.xml/body/p[1454], word/document.xml/body/p[1456], word/document.xml/body/p[1457], word/document.xml/body/p[1458], word/document.xml/body/p[1459], word/document.xml/body/p[1461], word/document.xml/body/p[1462] · `chunk-8a1cd259f0edea9b15fc3ea3`
```text
安装5GC业务软件 / 单节点离线部署UPF / 检查upf 网卡配置信息
检查upf 网卡配置信息
1）查看生成的multus-cni多网卡插件配置
# cd home/upf_setup_CU5GC_UPF_5.0.210/integration
# ls temp/multus/
host-device-1.yaml  host-device-2.yaml  host-device-3.yaml  host-device-4.yaml  host-device-n4.yaml
配置文件说明
host-device-1.yaml  host-device-2.yaml,用于将N3和N6网卡绑定到pod，使用multus-cni+host-device-cni两个插件实现
host-device-3.yaml用于将N4网卡绑定到pod，，使用multus-cni+vlan-cni两个插件实现，非bond模式时在单个网卡上分配vlan子接口给upfd pod，bond模式时在bond0上分配vlan子接口给upfd pod
2）查看已经绑定用户态驱动vfio-pci的网卡，该网卡是否用于UPF N3/N6接口。
# driverctl list-overrides
0000:17:00.0 vfio-pci
0000:17:00.1 vfio-pci
0000:4b:00.0 vfio-pci
0000:4b:00.1 vfio-pci
或者使用dpdk-devbind.py脚本查看当前节点可用物理网卡
# cd home/upf_setup_CU5GC_UPF_5.0.210/integration
./scripts/dpdk-devbind.py -s
部署UPF前网卡绑定状态示例输出结果如下：
说明：需要运维人员根据组网规划确认哪些网卡用于UPF，以上示例使用enp1f0、enp1f1、enp3f0、enp3f1四块高速以太网卡用于UPF应用的N3/N6。
部署UPF后网卡绑定状态示例输出结果如下：
```
- 预期原文/缺口：
```text
安装5GC业务软件 / 单节点离线部署UPF / 检查upf 网卡配置信息
检查upf 网卡配置信息
1）查看生成的multus-cni多网卡插件配置
# cd home/upf_setup_CU5GC_UPF_5.0.210/integration
# ls temp/multus/
host-device-1.yaml  host-device-2.yaml  host-device-3.yaml  host-device-4.yaml  host-device-n4.yaml
配置文件说明
host-device-1.yaml  host-device-2.yaml,用于将N3和N6网卡绑定到pod，使用multus-cni+host-device-cni两个插件实现
host-device-3.yaml用于将N4网卡绑定到pod，，使用multus-cni+vlan-cni两个插件实现，非bond模式时在单个网卡上分配vlan子接口给upfd pod，bond模式时在bond0上分配vlan子接口给upfd pod
2）查看已经绑定用户态驱动vfio-pci的网卡，该网卡是否用于UPF N3/N6接口。
# driverctl list-overrides
0000:17:00.0 vfio-pci
0000:17:00.1 vfio-pci
0000:4b:00.0 vfio-pci
0000:4b:00.1 vfio-pci
或者使用dpdk-devbind.py脚本查看当前节点可用物理网卡
# cd home/upf_setup_CU5GC_UPF_5.0.210/integration
./scripts/dpdk-devbind.py -s
部署UPF前网卡绑定状态示例输出结果如下：
说明：需要运维人员根据组网规划确认哪些网卡用于UPF，以上示例使用enp1f0、enp1f1、enp3f0、enp3f1四块高速以太网卡用于UPF应用的N3/N6。
部署UPF后网卡绑定状态示例输出结果如下：
```

## knowledge-013 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘安装5GC业务软件 / 基本配置说明 / Sriov网络策略配置’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b6c046c056817a4f9c22, manual-topic:section-b6c046c056817a4f9c22
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1518], word/document.xml/body/p[1519], word/document.xml/body/p[1521], word/document.xml/body/p[1522], word/document.xml/body/p[1523], word/document.xml/body/p[1524], word/document.xml/body/p[1525] · `chunk-ada762152f1aa95ea262d364`
```text
安装5GC业务软件 / 基本配置说明 / Sriov网络策略配置
Sriov网络策略配置
Sriov网络策略配置示意图：
由下至上层级说明：
PF：最底层为主机物理网卡，作为sriov资源池
SriovNetworkNodePolicy：定义物理网卡资源，生成VF虚拟网卡
SriovNetwork：定义附加网络，将VF附加到pod
VF: 已经附加到pod中的VF虚拟网卡，net1及net2 使用用户态驱动vfio-pci绑定到pod vpp中，net3、net4使用内核态驱动直接绑定到pod
```
- 预期原文/缺口：
```text
安装5GC业务软件 / 基本配置说明 / Sriov网络策略配置
Sriov网络策略配置
Sriov网络策略配置示意图：
由下至上层级说明：
PF：最底层为主机物理网卡，作为sriov资源池
SriovNetworkNodePolicy：定义物理网卡资源，生成VF虚拟网卡
SriovNetwork：定义附加网络，将VF附加到pod
VF: 已经附加到pod中的VF虚拟网卡，net1及net2 使用用户态驱动vfio-pci绑定到pod vpp中，net3、net4使用内核态驱动直接绑定到pod
```

## knowledge-014 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘安装5GC业务软件 / 基本配置说明 / Sriov网络策略配置’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-b6c046c056817a4f9c22, manual-topic:section-b6c046c056817a4f9c22
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1518], word/document.xml/body/p[1519], word/document.xml/body/p[1521], word/document.xml/body/p[1522], word/document.xml/body/p[1523], word/document.xml/body/p[1524], word/document.xml/body/p[1525] · `chunk-ada762152f1aa95ea262d364`
```text
安装5GC业务软件 / 基本配置说明 / Sriov网络策略配置
Sriov网络策略配置
Sriov网络策略配置示意图：
由下至上层级说明：
PF：最底层为主机物理网卡，作为sriov资源池
SriovNetworkNodePolicy：定义物理网卡资源，生成VF虚拟网卡
SriovNetwork：定义附加网络，将VF附加到pod
VF: 已经附加到pod中的VF虚拟网卡，net1及net2 使用用户态驱动vfio-pci绑定到pod vpp中，net3、net4使用内核态驱动直接绑定到pod
```
- 预期原文/缺口：
```text
安装5GC业务软件 / 基本配置说明 / Sriov网络策略配置
Sriov网络策略配置
Sriov网络策略配置示意图：
由下至上层级说明：
PF：最底层为主机物理网卡，作为sriov资源池
SriovNetworkNodePolicy：定义物理网卡资源，生成VF虚拟网卡
SriovNetwork：定义附加网络，将VF附加到pod
VF: 已经附加到pod中的VF虚拟网卡，net1及net2 使用用户态驱动vfio-pci绑定到pod vpp中，net3、net4使用内核态驱动直接绑定到pod
```

## knowledge-015 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘UPF软件升级更新 / 部署新的UPF软件’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-1f02256364f9f8dcadec, manual-topic:section-1f02256364f9f8dcadec
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1763], word/document.xml/body/p[1764], word/document.xml/body/p[1765], word/document.xml/body/p[1766], word/document.xml/body/p[1767], word/document.xml/body/p[1768], word/document.xml/body/p[1770], word/document.xml/body/p[1772], word/document.xml/body/p[1773], word/document.xml/body/p[1774], word/document.xml/body/p[1775], word/document.xml/body/p[1776] · `chunk-f9722da50bf4f3243b27226e`
```text
UPF软件升级更新 / 部署新的UPF软件
部署新的UPF软件
进入到新发布的UPF版本（如：CU5GC_UPF_5.0.218）路径，执行install命令安装UPF。具体步骤如下：
root@gd-gz-gdlt-upf01:~# cd /home/upf_setup_CU5GC_UPF_5.0.218/integration/
root@gd-gz-gdlt-upf01::/home/upf_setup_CU5GC_UPF_5.0.218/integration# ./deploy.sh install
之后通过下面命令检查新的UPF软件（如：CU5GC_UPF_5.0.218）是否安装成功。
root@gd-gz-gdlt-upf01:/home/upf_setup_CU5GC_UPF_5.0.218/integration# upfmgr info
Current UPF Version is:   CU5GC_UPF_5.0.218
clusterIP:            193.9.3.55
NodeName:             gd-gz-gdlt-upf01
说明：重新部署UPF完成后，正常情况下，UPF的各个接口IP地址和静态路由等配置，是存储在数据库的。因此，可以通过下面命令检查各个地址配置是否仍在：
root@gd-gz-gdlt-upf01:~# upfmgr ip qry
如果检查发现UPF各个接口IP地址不存在，则需要参考 REF _Toc10483 \r \h 5.1.7 REF _Toc10483 \h 检查upf 业务网络地址配置重新配置各个接口地址。
```
- 预期原文/缺口：
```text
UPF软件升级更新 / 部署新的UPF软件
部署新的UPF软件
进入到新发布的UPF版本（如：CU5GC_UPF_5.0.218）路径，执行install命令安装UPF。具体步骤如下：
root@gd-gz-gdlt-upf01:~# cd /home/upf_setup_CU5GC_UPF_5.0.218/integration/
root@gd-gz-gdlt-upf01::/home/upf_setup_CU5GC_UPF_5.0.218/integration# ./deploy.sh install
之后通过下面命令检查新的UPF软件（如：CU5GC_UPF_5.0.218）是否安装成功。
root@gd-gz-gdlt-upf01:/home/upf_setup_CU5GC_UPF_5.0.218/integration# upfmgr info
Current UPF Version is:   CU5GC_UPF_5.0.218
clusterIP:            193.9.3.55
NodeName:             gd-gz-gdlt-upf01
说明：重新部署UPF完成后，正常情况下，UPF的各个接口IP地址和静态路由等配置，是存储在数据库的。因此，可以通过下面命令检查各个地址配置是否仍在：
root@gd-gz-gdlt-upf01:~# upfmgr ip qry
如果检查发现UPF各个接口IP地址不存在，则需要参考 REF _Toc10483 \r \h 5.1.7 REF _Toc10483 \h 检查upf 业务网络地址配置重新配置各个接口地址。
```

## knowledge-016 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘UPF软件升级更新 / 部署新的UPF软件’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-1f02256364f9f8dcadec, manual-topic:section-1f02256364f9f8dcadec
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1763], word/document.xml/body/p[1764], word/document.xml/body/p[1765], word/document.xml/body/p[1766], word/document.xml/body/p[1767], word/document.xml/body/p[1768], word/document.xml/body/p[1770], word/document.xml/body/p[1772], word/document.xml/body/p[1773], word/document.xml/body/p[1774], word/document.xml/body/p[1775], word/document.xml/body/p[1776] · `chunk-f9722da50bf4f3243b27226e`
```text
UPF软件升级更新 / 部署新的UPF软件
部署新的UPF软件
进入到新发布的UPF版本（如：CU5GC_UPF_5.0.218）路径，执行install命令安装UPF。具体步骤如下：
root@gd-gz-gdlt-upf01:~# cd /home/upf_setup_CU5GC_UPF_5.0.218/integration/
root@gd-gz-gdlt-upf01::/home/upf_setup_CU5GC_UPF_5.0.218/integration# ./deploy.sh install
之后通过下面命令检查新的UPF软件（如：CU5GC_UPF_5.0.218）是否安装成功。
root@gd-gz-gdlt-upf01:/home/upf_setup_CU5GC_UPF_5.0.218/integration# upfmgr info
Current UPF Version is:   CU5GC_UPF_5.0.218
clusterIP:            193.9.3.55
NodeName:             gd-gz-gdlt-upf01
说明：重新部署UPF完成后，正常情况下，UPF的各个接口IP地址和静态路由等配置，是存储在数据库的。因此，可以通过下面命令检查各个地址配置是否仍在：
root@gd-gz-gdlt-upf01:~# upfmgr ip qry
如果检查发现UPF各个接口IP地址不存在，则需要参考 REF _Toc10483 \r \h 5.1.7 REF _Toc10483 \h 检查upf 业务网络地址配置重新配置各个接口地址。
```
- 预期原文/缺口：
```text
UPF软件升级更新 / 部署新的UPF软件
部署新的UPF软件
进入到新发布的UPF版本（如：CU5GC_UPF_5.0.218）路径，执行install命令安装UPF。具体步骤如下：
root@gd-gz-gdlt-upf01:~# cd /home/upf_setup_CU5GC_UPF_5.0.218/integration/
root@gd-gz-gdlt-upf01::/home/upf_setup_CU5GC_UPF_5.0.218/integration# ./deploy.sh install
之后通过下面命令检查新的UPF软件（如：CU5GC_UPF_5.0.218）是否安装成功。
root@gd-gz-gdlt-upf01:/home/upf_setup_CU5GC_UPF_5.0.218/integration# upfmgr info
Current UPF Version is:   CU5GC_UPF_5.0.218
clusterIP:            193.9.3.55
NodeName:             gd-gz-gdlt-upf01
说明：重新部署UPF完成后，正常情况下，UPF的各个接口IP地址和静态路由等配置，是存储在数据库的。因此，可以通过下面命令检查各个地址配置是否仍在：
root@gd-gz-gdlt-upf01:~# upfmgr ip qry
如果检查发现UPF各个接口IP地址不存在，则需要参考 REF _Toc10483 \r \h 5.1.7 REF _Toc10483 \h 检查upf 业务网络地址配置重新配置各个接口地址。
```

## knowledge-017 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / Kubernetes’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-ebed6f3dd99afc98121b, manual-topic:section-ebed6f3dd99afc98121b
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1856], word/document.xml/body/p[1857], word/document.xml/body/p[1858], word/document.xml/body/p[1859], word/document.xml/body/p[1860], word/document.xml/body/p[1862], word/document.xml/body/p[1863], word/document.xml/body/p[1864], word/document.xml/body/p[1865], word/document.xml/body/p[1866], word/document.xml/body/p[1868], word/document.xml/body/p[1869], word/document.xml/body/p[1870], word/document.xml/body/p[1871], word/document.xml/body/p[1872], word/document.xml/body/p[1874], word/document.xml/body/p[1875], word/document.xml/body/p[1876], word/document.xml/body/p[1877], word/document.xml/body/p[1878], word/document.xml/body/p[1879], word/document.xml/body/p[1880], word/document.xml/body/p[1881], word/document.xml/body/p[1882], word/document.xml/body/p[1883], word/document.xml/body/p[1885], word/document.xml/body/p[1886], word/document.xml/body/p[1887], word/document.xml/body/p[1888], word/document.xml/body/p[1889], word/document.xml/body/p[1890], word/document.xml/body/p[1891], word/document.xml/body/p[1892] · `chunk-fa4337014e04a5b240327874`
```text
K8S集群软件故障排查 / 插件维护管理 / Kubernetes
Kubernetes
Kubernetes为核心镜像，开始安装集群的第一步必须先安装kubernetes，该镜像包含容器运行时及kubernetes核心组件，但不包含网络插件。
安装kubernetes
sealos run docker.io/labring/kubernetes:v1.25.6 --single
说明：其--single参数表示在当前节点运行单节点集群，无需传递节点IP地址信息。
由于kubernetes镜像不包含网络插件，运行一个完整可用的集群，一般需要安装以下三个镜像
sealos run docker.io/labring/kubernetes:v1.25.6 –single
sealos run docker.io/labring/helm:v3.11.0
sealos run docker.io/labring/flannel:v0.21.4
说明：由于flannel依赖helm命令，因此也需要安装helm插件。
以上命令也可以合并在一条命令执行
sealos run \
docker.io/labring/kubernetes:v1.25.6 \ 
docker.io/labring/helm:v3.11.0 \
docker.io/labring/flannel:v0.21.4 --single
运行多节点或高可用集群的示例
sealos run docker.io/labring/kubernetes:v1.25.6 docker.io/labring/helm:v3.11.0 \
  docker.io/labring/flannel:v0.21.4 \
  --masters 192.168.64.2,192.168.64.22,192.168.64.20 \
  --nodes 192.168.64.21,192.168.64.19 \
  -p [your-ssh-passwd]
说明：
Masters：节点数量可以为1或3个
Nodes：节点数量可以为0或多个
-p：root用户的ssh密码，例如-p “Password#123”
离线安装示例
a．首先需要在联网环境拉取并打包镜像，以kubernetes镜像为例，其他镜像操作方法相同。
sealos pull docker.io/labring/kubernetes:v1.25.6
sealos save -o kubernetes_v1.25.6.tar.gz docker.io/labring/kubernetes:v1.25.6
b.上传kubernetes_v1.25.6.tar.gz镜像包到离线环境，然后加载镜像（ sealos二进制文件也需要上传到离线环境）
sealos load -i kubernetes_v1.25.6.tar.gz
c.查看加载到本地的镜像
sealos images
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1893], word/document.xml/body/p[1894] · `chunk-fc1ffbf7abbe3c7fdf69d47d`
```text
K8S集群软件故障排查 / 插件维护管理 / Kubernetes
d.使用本地镜像安装集群或插件，后续操作与在线安装步骤相同
sealos run docker.io/labring/kubernetes:v1.25.6 --single
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Kubernetes
Kubernetes
Kubernetes为核心镜像，开始安装集群的第一步必须先安装kubernetes，该镜像包含容器运行时及kubernetes核心组件，但不包含网络插件。
安装kubernetes
sealos run docker.io/labring/kubernetes:v1.25.6 --single
说明：其--single参数表示在当前节点运行单节点集群，无需传递节点IP地址信息。
由于kubernetes镜像不包含网络插件，运行一个完整可用的集群，一般需要安装以下三个镜像
sealos run docker.io/labring/kubernetes:v1.25.6 –single
sealos run docker.io/labring/helm:v3.11.0
sealos run docker.io/labring/flannel:v0.21.4
说明：由于flannel依赖helm命令，因此也需要安装helm插件。
以上命令也可以合并在一条命令执行
sealos run \
docker.io/labring/kubernetes:v1.25.6 \ 
docker.io/labring/helm:v3.11.0 \
docker.io/labring/flannel:v0.21.4 --single
运行多节点或高可用集群的示例
sealos run docker.io/labring/kubernetes:v1.25.6 docker.io/labring/helm:v3.11.0 \
  docker.io/labring/flannel:v0.21.4 \
  --masters 192.168.64.2,192.168.64.22,192.168.64.20 \
  --nodes 192.168.64.21,192.168.64.19 \
  -p [your-ssh-passwd]
说明：
Masters：节点数量可以为1或3个
Nodes：节点数量可以为0或多个
-p：root用户的ssh密码，例如-p “Password#123”
离线安装示例
a．首先需要在联网环境拉取并打包镜像，以kubernetes镜像为例，其他镜像操作方法相同。
sealos pull docker.io/labring/kubernetes:v1.25.6
sealos save -o kubernetes_v1.25.6.tar.gz docker.io/labring/kubernetes:v1.25.6
b.上传kubernetes_v1.25.6.tar.gz镜像包到离线环境，然后加载镜像（ sealos二进制文件也需要上传到离线环境）
sealos load -i kubernetes_v1.25.6.tar.gz
c.查看加载到本地的镜像
sealos images
```

## knowledge-018 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / Kubernetes’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-ebed6f3dd99afc98121b, manual-topic:section-ebed6f3dd99afc98121b
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1856], word/document.xml/body/p[1857], word/document.xml/body/p[1858], word/document.xml/body/p[1859], word/document.xml/body/p[1860], word/document.xml/body/p[1862], word/document.xml/body/p[1863], word/document.xml/body/p[1864], word/document.xml/body/p[1865], word/document.xml/body/p[1866], word/document.xml/body/p[1868], word/document.xml/body/p[1869], word/document.xml/body/p[1870], word/document.xml/body/p[1871], word/document.xml/body/p[1872], word/document.xml/body/p[1874], word/document.xml/body/p[1875], word/document.xml/body/p[1876], word/document.xml/body/p[1877], word/document.xml/body/p[1878], word/document.xml/body/p[1879], word/document.xml/body/p[1880], word/document.xml/body/p[1881], word/document.xml/body/p[1882], word/document.xml/body/p[1883], word/document.xml/body/p[1885], word/document.xml/body/p[1886], word/document.xml/body/p[1887], word/document.xml/body/p[1888], word/document.xml/body/p[1889], word/document.xml/body/p[1890], word/document.xml/body/p[1891], word/document.xml/body/p[1892] · `chunk-fa4337014e04a5b240327874`
```text
K8S集群软件故障排查 / 插件维护管理 / Kubernetes
Kubernetes
Kubernetes为核心镜像，开始安装集群的第一步必须先安装kubernetes，该镜像包含容器运行时及kubernetes核心组件，但不包含网络插件。
安装kubernetes
sealos run docker.io/labring/kubernetes:v1.25.6 --single
说明：其--single参数表示在当前节点运行单节点集群，无需传递节点IP地址信息。
由于kubernetes镜像不包含网络插件，运行一个完整可用的集群，一般需要安装以下三个镜像
sealos run docker.io/labring/kubernetes:v1.25.6 –single
sealos run docker.io/labring/helm:v3.11.0
sealos run docker.io/labring/flannel:v0.21.4
说明：由于flannel依赖helm命令，因此也需要安装helm插件。
以上命令也可以合并在一条命令执行
sealos run \
docker.io/labring/kubernetes:v1.25.6 \ 
docker.io/labring/helm:v3.11.0 \
docker.io/labring/flannel:v0.21.4 --single
运行多节点或高可用集群的示例
sealos run docker.io/labring/kubernetes:v1.25.6 docker.io/labring/helm:v3.11.0 \
  docker.io/labring/flannel:v0.21.4 \
  --masters 192.168.64.2,192.168.64.22,192.168.64.20 \
  --nodes 192.168.64.21,192.168.64.19 \
  -p [your-ssh-passwd]
说明：
Masters：节点数量可以为1或3个
Nodes：节点数量可以为0或多个
-p：root用户的ssh密码，例如-p “Password#123”
离线安装示例
a．首先需要在联网环境拉取并打包镜像，以kubernetes镜像为例，其他镜像操作方法相同。
sealos pull docker.io/labring/kubernetes:v1.25.6
sealos save -o kubernetes_v1.25.6.tar.gz docker.io/labring/kubernetes:v1.25.6
b.上传kubernetes_v1.25.6.tar.gz镜像包到离线环境，然后加载镜像（ sealos二进制文件也需要上传到离线环境）
sealos load -i kubernetes_v1.25.6.tar.gz
c.查看加载到本地的镜像
sealos images
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1893], word/document.xml/body/p[1894] · `chunk-fc1ffbf7abbe3c7fdf69d47d`
```text
K8S集群软件故障排查 / 插件维护管理 / Kubernetes
d.使用本地镜像安装集群或插件，后续操作与在线安装步骤相同
sealos run docker.io/labring/kubernetes:v1.25.6 --single
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Kubernetes
Kubernetes
Kubernetes为核心镜像，开始安装集群的第一步必须先安装kubernetes，该镜像包含容器运行时及kubernetes核心组件，但不包含网络插件。
安装kubernetes
sealos run docker.io/labring/kubernetes:v1.25.6 --single
说明：其--single参数表示在当前节点运行单节点集群，无需传递节点IP地址信息。
由于kubernetes镜像不包含网络插件，运行一个完整可用的集群，一般需要安装以下三个镜像
sealos run docker.io/labring/kubernetes:v1.25.6 –single
sealos run docker.io/labring/helm:v3.11.0
sealos run docker.io/labring/flannel:v0.21.4
说明：由于flannel依赖helm命令，因此也需要安装helm插件。
以上命令也可以合并在一条命令执行
sealos run \
docker.io/labring/kubernetes:v1.25.6 \ 
docker.io/labring/helm:v3.11.0 \
docker.io/labring/flannel:v0.21.4 --single
运行多节点或高可用集群的示例
sealos run docker.io/labring/kubernetes:v1.25.6 docker.io/labring/helm:v3.11.0 \
  docker.io/labring/flannel:v0.21.4 \
  --masters 192.168.64.2,192.168.64.22,192.168.64.20 \
  --nodes 192.168.64.21,192.168.64.19 \
  -p [your-ssh-passwd]
说明：
Masters：节点数量可以为1或3个
Nodes：节点数量可以为0或多个
-p：root用户的ssh密码，例如-p “Password#123”
离线安装示例
a．首先需要在联网环境拉取并打包镜像，以kubernetes镜像为例，其他镜像操作方法相同。
sealos pull docker.io/labring/kubernetes:v1.25.6
sealos save -o kubernetes_v1.25.6.tar.gz docker.io/labring/kubernetes:v1.25.6
b.上传kubernetes_v1.25.6.tar.gz镜像包到离线环境，然后加载镜像（ sealos二进制文件也需要上传到离线环境）
sealos load -i kubernetes_v1.25.6.tar.gz
c.查看加载到本地的镜像
sealos images
```

## knowledge-019 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / Flannel’的说明和关键字段是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-066cc1bc125c770979b0, manual-topic:section-066cc1bc125c770979b0
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1908], word/document.xml/body/p[1909], word/document.xml/body/p[1910], word/document.xml/body/p[1911], word/document.xml/body/p[1912], word/document.xml/body/p[1913], word/document.xml/body/p[1914], word/document.xml/body/p[1915], word/document.xml/body/p[1916], word/document.xml/body/p[1918], word/document.xml/body/p[1919], word/document.xml/body/p[1921], word/document.xml/body/p[1922], word/document.xml/body/p[1923], word/document.xml/body/p[1924], word/document.xml/body/p[1925], word/document.xml/body/p[1927], word/document.xml/body/p[1928], word/document.xml/body/p[1929], word/document.xml/body/p[1930], word/document.xml/body/p[1932], word/document.xml/body/p[1933] · `chunk-ce1bae1eaeca4e52e1de2b7c`
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
Flannel
单节点集群采用flannel网络插件，为k8s集群pod及service提供内外网络访问能力。
sealos底层调用helm命令安装flannel插件，默认安装在kube-flannel命名空间下。
前置要求：
	已运行kubernetes核心镜像
	已运行helm插件
例如:
$ sealos run docker.io/labring/kubernetes:v1.25.6
$ sealos run docker.io/labring/helm:v3.11.0
1.	安装flannel网络插件
$ sealos run docker.io/labring/flannel:v0.21.4
2.	查看部署的flannel helm chart
$ helm -n kube-flannel ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
flannel kube-flannel    1               2023-03-28 16:10:31.812412554 +0800 CST deployed        flannel-v0.21.4 v0.21.4
说明：在v1.21.4版本之前版本flannel使用kubectl进行安装，未使用helm。
3.	查看flannel pods
root@node30:~# kubectl -n kube-flannel get pods 
NAME                    READY   STATUS    RESTARTS   AGE
kube-flannel-ds-7rrks   1/1     Running   0          2d1h
4.	卸载flannel网络插件
a.使用helm命令卸载
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1934] · `chunk-2fc4428866c69bb6de423877`
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1935], word/document.xml/body/p[1936] · `chunk-05a7a290e4e820cd81436843`
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
b.使用sealos命令卸载，仅部分镜像支持该方式
sealos run docker.io/labring/flannel:v0.21.4 -e uninstall=true
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
Flannel
单节点集群采用flannel网络插件，为k8s集群pod及service提供内外网络访问能力。
sealos底层调用helm命令安装flannel插件，默认安装在kube-flannel命名空间下。
前置要求：
	已运行kubernetes核心镜像
	已运行helm插件
例如:
$ sealos run docker.io/labring/kubernetes:v1.25.6
$ sealos run docker.io/labring/helm:v3.11.0
1.	安装flannel网络插件
$ sealos run docker.io/labring/flannel:v0.21.4
2.	查看部署的flannel helm chart
$ helm -n kube-flannel ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
flannel kube-flannel    1               2023-03-28 16:10:31.812412554 +0800 CST deployed        flannel-v0.21.4 v0.21.4
说明：在v1.21.4版本之前版本flannel使用kubectl进行安装，未使用helm。
3.	查看flannel pods
root@node30:~# kubectl -n kube-flannel get pods 
NAME                    READY   STATUS    RESTARTS   AGE
kube-flannel-ds-7rrks   1/1     Running   0          2d1h
4.	卸载flannel网络插件
a.使用helm命令卸载
```

## knowledge-020 · heldout · knowledge

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / Flannel’解释说明和关键字段，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-066cc1bc125c770979b0, manual-topic:section-066cc1bc125c770979b0
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1908], word/document.xml/body/p[1909], word/document.xml/body/p[1910], word/document.xml/body/p[1911], word/document.xml/body/p[1912], word/document.xml/body/p[1913], word/document.xml/body/p[1914], word/document.xml/body/p[1915], word/document.xml/body/p[1916], word/document.xml/body/p[1918], word/document.xml/body/p[1919], word/document.xml/body/p[1921], word/document.xml/body/p[1922], word/document.xml/body/p[1923], word/document.xml/body/p[1924], word/document.xml/body/p[1925], word/document.xml/body/p[1927], word/document.xml/body/p[1928], word/document.xml/body/p[1929], word/document.xml/body/p[1930], word/document.xml/body/p[1932], word/document.xml/body/p[1933] · `chunk-ce1bae1eaeca4e52e1de2b7c`
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
Flannel
单节点集群采用flannel网络插件，为k8s集群pod及service提供内外网络访问能力。
sealos底层调用helm命令安装flannel插件，默认安装在kube-flannel命名空间下。
前置要求：
	已运行kubernetes核心镜像
	已运行helm插件
例如:
$ sealos run docker.io/labring/kubernetes:v1.25.6
$ sealos run docker.io/labring/helm:v3.11.0
1.	安装flannel网络插件
$ sealos run docker.io/labring/flannel:v0.21.4
2.	查看部署的flannel helm chart
$ helm -n kube-flannel ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
flannel kube-flannel    1               2023-03-28 16:10:31.812412554 +0800 CST deployed        flannel-v0.21.4 v0.21.4
说明：在v1.21.4版本之前版本flannel使用kubectl进行安装，未使用helm。
3.	查看flannel pods
root@node30:~# kubectl -n kube-flannel get pods 
NAME                    READY   STATUS    RESTARTS   AGE
kube-flannel-ds-7rrks   1/1     Running   0          2d1h
4.	卸载flannel网络插件
a.使用helm命令卸载
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1934] · `chunk-2fc4428866c69bb6de423877`
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1935], word/document.xml/body/p[1936] · `chunk-05a7a290e4e820cd81436843`
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
b.使用sealos命令卸载，仅部分镜像支持该方式
sealos run docker.io/labring/flannel:v0.21.4 -e uninstall=true
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
Flannel
单节点集群采用flannel网络插件，为k8s集群pod及service提供内外网络访问能力。
sealos底层调用helm命令安装flannel插件，默认安装在kube-flannel命名空间下。
前置要求：
	已运行kubernetes核心镜像
	已运行helm插件
例如:
$ sealos run docker.io/labring/kubernetes:v1.25.6
$ sealos run docker.io/labring/helm:v3.11.0
1.	安装flannel网络插件
$ sealos run docker.io/labring/flannel:v0.21.4
2.	查看部署的flannel helm chart
$ helm -n kube-flannel ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
flannel kube-flannel    1               2023-03-28 16:10:31.812412554 +0800 CST deployed        flannel-v0.21.4 v0.21.4
说明：在v1.21.4版本之前版本flannel使用kubectl进行安装，未使用helm。
3.	查看flannel pods
root@node30:~# kubectl -n kube-flannel get pods 
NAME                    READY   STATUS    RESTARTS   AGE
kube-flannel-ds-7rrks   1/1     Running   0          2d1h
4.	卸载flannel网络插件
a.使用helm命令卸载
```

## troubleshooting-001 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 基本故障排查 / ice网卡驱动’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-d4f2e279b4d191eac6de, manual-topic:section-d4f2e279b4d191eac6de
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1846], word/document.xml/body/p[1847], word/document.xml/body/p[1848], word/document.xml/body/p[1850], word/document.xml/body/p[1852] · `chunk-b6fb841cfccf4c91fa7d9f9e`
```text
K8S集群软件故障排查 / 基本故障排查 / ice网卡驱动
ice网卡驱动
WingTech 服务器需要更新ICE网卡驱动，否则可能遇到以下问题：
检查用于UPF的物理网卡状态，确认状态是否都为UP状态，发现其中eno4 状态为down，并且执行up命令无法启动
通过查找eno4 网卡PCI地址，执行dmesg查看日志，日志存在以下报错
以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / ice网卡驱动
ice网卡驱动
WingTech 服务器需要更新ICE网卡驱动，否则可能遇到以下问题：
检查用于UPF的物理网卡状态，确认状态是否都为UP状态，发现其中eno4 状态为down，并且执行up命令无法启动
通过查找eno4 网卡PCI地址，执行dmesg查看日志，日志存在以下报错
以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```

## troubleshooting-002 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 基本故障排查 / ice网卡驱动’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-d4f2e279b4d191eac6de, manual-topic:section-d4f2e279b4d191eac6de
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1846], word/document.xml/body/p[1847], word/document.xml/body/p[1848], word/document.xml/body/p[1850], word/document.xml/body/p[1852] · `chunk-b6fb841cfccf4c91fa7d9f9e`
```text
K8S集群软件故障排查 / 基本故障排查 / ice网卡驱动
ice网卡驱动
WingTech 服务器需要更新ICE网卡驱动，否则可能遇到以下问题：
检查用于UPF的物理网卡状态，确认状态是否都为UP状态，发现其中eno4 状态为down，并且执行up命令无法启动
通过查找eno4 网卡PCI地址，执行dmesg查看日志，日志存在以下报错
以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 基本故障排查 / ice网卡驱动
ice网卡驱动
WingTech 服务器需要更新ICE网卡驱动，否则可能遇到以下问题：
检查用于UPF的物理网卡状态，确认状态是否都为UP状态，发现其中eno4 状态为down，并且执行up命令无法启动
通过查找eno4 网卡PCI地址，执行dmesg查看日志，日志存在以下报错
以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```

## troubleshooting-003 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘部署FAQ / K8S集群软件故障排查 / 插件维护管理’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-af579897a056e398c218, manual-topic:section-af579897a056e398c218
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1853], word/document.xml/body/p[1854], word/document.xml/body/p[1855] · `chunk-76b3006ebf4d6634906ecd2a`
```text
部署FAQ / K8S集群软件故障排查 / 插件维护管理
插件维护管理
集群安装脚本默认能够自动安装所有启用的插件，下面主要介绍在集群安装完成后如何单独安装某个插件，以及如果管理插件的生命周期，例如查看插件运行状态，卸载插件等。
官方支持的插件镜像及版本： HYPERLINK "https://hub.docker.com/u/labring" https://hub.docker.com/u/labring
```
- 预期原文/缺口：
```text
部署FAQ / K8S集群软件故障排查 / 插件维护管理
插件维护管理
集群安装脚本默认能够自动安装所有启用的插件，下面主要介绍在集群安装完成后如何单独安装某个插件，以及如果管理插件的生命周期，例如查看插件运行状态，卸载插件等。
官方支持的插件镜像及版本： HYPERLINK "https://hub.docker.com/u/labring" https://hub.docker.com/u/labring
```

## troubleshooting-004 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘部署FAQ / K8S集群软件故障排查 / 插件维护管理’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-af579897a056e398c218, manual-topic:section-af579897a056e398c218
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1853], word/document.xml/body/p[1854], word/document.xml/body/p[1855] · `chunk-76b3006ebf4d6634906ecd2a`
```text
部署FAQ / K8S集群软件故障排查 / 插件维护管理
插件维护管理
集群安装脚本默认能够自动安装所有启用的插件，下面主要介绍在集群安装完成后如何单独安装某个插件，以及如果管理插件的生命周期，例如查看插件运行状态，卸载插件等。
官方支持的插件镜像及版本： HYPERLINK "https://hub.docker.com/u/labring" https://hub.docker.com/u/labring
```
- 预期原文/缺口：
```text
部署FAQ / K8S集群软件故障排查 / 插件维护管理
插件维护管理
集群安装脚本默认能够自动安装所有启用的插件，下面主要介绍在集群安装完成后如何单独安装某个插件，以及如果管理插件的生命周期，例如查看插件运行状态，卸载插件等。
官方支持的插件镜像及版本： HYPERLINK "https://hub.docker.com/u/labring" https://hub.docker.com/u/labring
```

## troubleshooting-005 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / Helm’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-a6c2f639d4d11cf91408, manual-topic:section-a6c2f639d4d11cf91408
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1896], word/document.xml/body/p[1897], word/document.xml/body/p[1898], word/document.xml/body/p[1899], word/document.xml/body/p[1901], word/document.xml/body/p[1902], word/document.xml/body/p[1903], word/document.xml/body/p[1905], word/document.xml/body/p[1906] · `chunk-73986e099325e6f5c5d27ac9`
```text
K8S集群软件故障排查 / 插件维护管理 / Helm
Helm
helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。
执行以下命令安装helm插件
$ sealos run docker.io/labring/helm:v3.11.0
使用以下命令查看helm安装路径
$ which helm
/usr/bin/helm
如需卸载helm 插件，执行以下命令
$ rm -rf /usr/bin/helm
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Helm
Helm
helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。
执行以下命令安装helm插件
$ sealos run docker.io/labring/helm:v3.11.0
使用以下命令查看helm安装路径
$ which helm
/usr/bin/helm
如需卸载helm 插件，执行以下命令
$ rm -rf /usr/bin/helm
```

## troubleshooting-006 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / Helm’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-a6c2f639d4d11cf91408, manual-topic:section-a6c2f639d4d11cf91408
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1896], word/document.xml/body/p[1897], word/document.xml/body/p[1898], word/document.xml/body/p[1899], word/document.xml/body/p[1901], word/document.xml/body/p[1902], word/document.xml/body/p[1903], word/document.xml/body/p[1905], word/document.xml/body/p[1906] · `chunk-73986e099325e6f5c5d27ac9`
```text
K8S集群软件故障排查 / 插件维护管理 / Helm
Helm
helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。
执行以下命令安装helm插件
$ sealos run docker.io/labring/helm:v3.11.0
使用以下命令查看helm安装路径
$ which helm
/usr/bin/helm
如需卸载helm 插件，执行以下命令
$ rm -rf /usr/bin/helm
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Helm
Helm
helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。
执行以下命令安装helm插件
$ sealos run docker.io/labring/helm:v3.11.0
使用以下命令查看helm安装路径
$ which helm
/usr/bin/helm
如需卸载helm 插件，执行以下命令
$ rm -rf /usr/bin/helm
```

## troubleshooting-007 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / ingress-nginx’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-23481b69f973264f217c, manual-topic:section-23481b69f973264f217c
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1963], word/document.xml/body/p[1964], word/document.xml/body/p[1965], word/document.xml/body/p[1966], word/document.xml/body/p[1967], word/document.xml/body/p[1969], word/document.xml/body/p[1970], word/document.xml/body/p[1971], word/document.xml/body/p[1972], word/document.xml/body/p[1974], word/document.xml/body/p[1975], word/document.xml/body/p[1976], word/document.xml/body/p[1977], word/document.xml/body/p[1979], word/document.xml/body/p[1980], word/document.xml/body/p[1981], word/document.xml/body/p[1982], word/document.xml/body/p[1984], word/document.xml/body/p[1985] · `chunk-dceca547ccdeb58f1bb4b7c2`
```text
K8S集群软件故障排查 / 插件维护管理 / ingress-nginx
ingress-nginx
Ingress-nginx插件提供通过集群外部访问POD service的能力。
sealos底层调用helm命令安装ingress-nginx插件，默认安装在ingress-nginx命名空间下，默认使用hostnetwork暴露ingress-nginx自身服务。
安装ingress-nginx网络插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/ingress-nginx-cucc:v1.6.4
查看ingress-nginx helm chart
$ helm -n ingress-nginx ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
ingress-nginx   ingress-nginx   1               2023-03-30 11:17:09.773134733 +0800 CST deployed        ingress-nginx-4.5.2     1.6.4      
查看ingress-nginx pods
$ kubectl -n ingress-nginx get pods 
NAME                                        READY   STATUS    RESTARTS        AGE
ingress-nginx-controller-6d6b6fd558-xxqk5   1/1     Running   3 (3h16m ago)   6h45m
查看ingress-nginx service
$ kubectl -n ingress-nginx get svc
NAME                                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
ingress-nginx-controller-admission   ClusterIP   10.96.1.212   <none>        443/TCP   6h45m
卸载ingress-nginx网络插件
$ helm -n ingress-nginx uninstall ingress-nginx
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / ingress-nginx
ingress-nginx
Ingress-nginx插件提供通过集群外部访问POD service的能力。
sealos底层调用helm命令安装ingress-nginx插件，默认安装在ingress-nginx命名空间下，默认使用hostnetwork暴露ingress-nginx自身服务。
安装ingress-nginx网络插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/ingress-nginx-cucc:v1.6.4
查看ingress-nginx helm chart
$ helm -n ingress-nginx ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
ingress-nginx   ingress-nginx   1               2023-03-30 11:17:09.773134733 +0800 CST deployed        ingress-nginx-4.5.2     1.6.4      
查看ingress-nginx pods
$ kubectl -n ingress-nginx get pods 
NAME                                        READY   STATUS    RESTARTS        AGE
ingress-nginx-controller-6d6b6fd558-xxqk5   1/1     Running   3 (3h16m ago)   6h45m
查看ingress-nginx service
$ kubectl -n ingress-nginx get svc
NAME                                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
ingress-nginx-controller-admission   ClusterIP   10.96.1.212   <none>        443/TCP   6h45m
卸载ingress-nginx网络插件
$ helm -n ingress-nginx uninstall ingress-nginx
```

## troubleshooting-008 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / ingress-nginx’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-23481b69f973264f217c, manual-topic:section-23481b69f973264f217c
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1963], word/document.xml/body/p[1964], word/document.xml/body/p[1965], word/document.xml/body/p[1966], word/document.xml/body/p[1967], word/document.xml/body/p[1969], word/document.xml/body/p[1970], word/document.xml/body/p[1971], word/document.xml/body/p[1972], word/document.xml/body/p[1974], word/document.xml/body/p[1975], word/document.xml/body/p[1976], word/document.xml/body/p[1977], word/document.xml/body/p[1979], word/document.xml/body/p[1980], word/document.xml/body/p[1981], word/document.xml/body/p[1982], word/document.xml/body/p[1984], word/document.xml/body/p[1985] · `chunk-dceca547ccdeb58f1bb4b7c2`
```text
K8S集群软件故障排查 / 插件维护管理 / ingress-nginx
ingress-nginx
Ingress-nginx插件提供通过集群外部访问POD service的能力。
sealos底层调用helm命令安装ingress-nginx插件，默认安装在ingress-nginx命名空间下，默认使用hostnetwork暴露ingress-nginx自身服务。
安装ingress-nginx网络插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/ingress-nginx-cucc:v1.6.4
查看ingress-nginx helm chart
$ helm -n ingress-nginx ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
ingress-nginx   ingress-nginx   1               2023-03-30 11:17:09.773134733 +0800 CST deployed        ingress-nginx-4.5.2     1.6.4      
查看ingress-nginx pods
$ kubectl -n ingress-nginx get pods 
NAME                                        READY   STATUS    RESTARTS        AGE
ingress-nginx-controller-6d6b6fd558-xxqk5   1/1     Running   3 (3h16m ago)   6h45m
查看ingress-nginx service
$ kubectl -n ingress-nginx get svc
NAME                                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
ingress-nginx-controller-admission   ClusterIP   10.96.1.212   <none>        443/TCP   6h45m
卸载ingress-nginx网络插件
$ helm -n ingress-nginx uninstall ingress-nginx
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / ingress-nginx
ingress-nginx
Ingress-nginx插件提供通过集群外部访问POD service的能力。
sealos底层调用helm命令安装ingress-nginx插件，默认安装在ingress-nginx命名空间下，默认使用hostnetwork暴露ingress-nginx自身服务。
安装ingress-nginx网络插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/ingress-nginx-cucc:v1.6.4
查看ingress-nginx helm chart
$ helm -n ingress-nginx ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
ingress-nginx   ingress-nginx   1               2023-03-30 11:17:09.773134733 +0800 CST deployed        ingress-nginx-4.5.2     1.6.4      
查看ingress-nginx pods
$ kubectl -n ingress-nginx get pods 
NAME                                        READY   STATUS    RESTARTS        AGE
ingress-nginx-controller-6d6b6fd558-xxqk5   1/1     Running   3 (3h16m ago)   6h45m
查看ingress-nginx service
$ kubectl -n ingress-nginx get svc
NAME                                 TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
ingress-nginx-controller-admission   ClusterIP   10.96.1.212   <none>        443/TCP   6h45m
卸载ingress-nginx网络插件
$ helm -n ingress-nginx uninstall ingress-nginx
```

## troubleshooting-009 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / multus-cni’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-56cea0da10a6979300c9, manual-topic:section-56cea0da10a6979300c9
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1987], word/document.xml/body/p[1988], word/document.xml/body/p[1989], word/document.xml/body/p[1991], word/document.xml/body/p[1992], word/document.xml/body/p[1994], word/document.xml/body/p[1995], word/document.xml/body/p[1996], word/document.xml/body/p[1997], word/document.xml/body/p[1999], word/document.xml/body/p[2000] · `chunk-85f751d548f2f48f2d49bd1c`
```text
K8S集群软件故障排查 / 插件维护管理 / multus-cni
multus-cni
multus-cni 插件支持为pod附加多个网卡，sriov-network-operator插件依赖multus-cni，两者配合使用。
sealos底层调用kubectl命令安装multus-cni插件，默认安装在kube-system命名空间下，pod以daemonset方式运行在所有节点上。
1.	安装multus-cni插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/multus-cni:v3.9.3
2.	查看multus-cni pod运行状态
$ kubectl -n kube-system get pods -l app=multus
NAME                   READY   STATUS    RESTARTS        AGE
kube-multus-ds-2c8h9   1/1     Running   3 (3h22m ago)   6h50m
3.	卸载multus-cni插件
$ kubectl -n kube-system delete ds kube-multus-ds
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / multus-cni
multus-cni
multus-cni 插件支持为pod附加多个网卡，sriov-network-operator插件依赖multus-cni，两者配合使用。
sealos底层调用kubectl命令安装multus-cni插件，默认安装在kube-system命名空间下，pod以daemonset方式运行在所有节点上。
1.	安装multus-cni插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/multus-cni:v3.9.3
2.	查看multus-cni pod运行状态
$ kubectl -n kube-system get pods -l app=multus
NAME                   READY   STATUS    RESTARTS        AGE
kube-multus-ds-2c8h9   1/1     Running   3 (3h22m ago)   6h50m
3.	卸载multus-cni插件
$ kubectl -n kube-system delete ds kube-multus-ds
```

## troubleshooting-010 · dev · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / multus-cni’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-56cea0da10a6979300c9, manual-topic:section-56cea0da10a6979300c9
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[1987], word/document.xml/body/p[1988], word/document.xml/body/p[1989], word/document.xml/body/p[1991], word/document.xml/body/p[1992], word/document.xml/body/p[1994], word/document.xml/body/p[1995], word/document.xml/body/p[1996], word/document.xml/body/p[1997], word/document.xml/body/p[1999], word/document.xml/body/p[2000] · `chunk-85f751d548f2f48f2d49bd1c`
```text
K8S集群软件故障排查 / 插件维护管理 / multus-cni
multus-cni
multus-cni 插件支持为pod附加多个网卡，sriov-network-operator插件依赖multus-cni，两者配合使用。
sealos底层调用kubectl命令安装multus-cni插件，默认安装在kube-system命名空间下，pod以daemonset方式运行在所有节点上。
1.	安装multus-cni插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/multus-cni:v3.9.3
2.	查看multus-cni pod运行状态
$ kubectl -n kube-system get pods -l app=multus
NAME                   READY   STATUS    RESTARTS        AGE
kube-multus-ds-2c8h9   1/1     Running   3 (3h22m ago)   6h50m
3.	卸载multus-cni插件
$ kubectl -n kube-system delete ds kube-multus-ds
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / multus-cni
multus-cni
multus-cni 插件支持为pod附加多个网卡，sriov-network-operator插件依赖multus-cni，两者配合使用。
sealos底层调用kubectl命令安装multus-cni插件，默认安装在kube-system命名空间下，pod以daemonset方式运行在所有节点上。
1.	安装multus-cni插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/multus-cni:v3.9.3
2.	查看multus-cni pod运行状态
$ kubectl -n kube-system get pods -l app=multus
NAME                   READY   STATUS    RESTARTS        AGE
kube-multus-ds-2c8h9   1/1     Running   3 (3h22m ago)   6h50m
3.	卸载multus-cni插件
$ kubectl -n kube-system delete ds kube-multus-ds
```

## troubleshooting-011 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / Prometheus’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-71f2f3f970d83664c466, manual-topic:section-71f2f3f970d83664c466
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2149], word/document.xml/body/p[2150], word/document.xml/body/p[2151], word/document.xml/body/p[2152], word/document.xml/body/p[2154], word/document.xml/body/p[2155], word/document.xml/body/p[2157], word/document.xml/body/p[2158], word/document.xml/body/p[2159], word/document.xml/body/p[2160], word/document.xml/body/p[2162], word/document.xml/body/p[2163], word/document.xml/body/p[2164], word/document.xml/body/p[2165], word/document.xml/body/p[2166], word/document.xml/body/p[2167], word/document.xml/body/p[2168], word/document.xml/body/p[2170] · `chunk-44dec42639466228f7fc64b8`
```text
K8S集群软件故障排查 / 插件维护管理 / Prometheus
Prometheus
Prometheus为监控插件，能够收集并展示kubernetes集群组件、Node节点及pod监控指标。K8s集群中的Prometheus需要上报监控指标到网管平台，通过prometheus集群联邦方式进行对接，对接的定制化helm values.yaml配置已封装在镜像中。
sealos底层调用helm命令安装Prometheus插件，默认安装在monitoring命名空间下。
前置要求：已安装能够提供动态持久卷的存储插件，例如openebs。
安装prometheus插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/kube-prometheus-stack-cucc:v0.63.0
查看prometheus helm chart
root@upf:~# helm -n monitoring ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
prometheus      monitoring      1               2023-03-30 11:18:14.407943736 +0800 CST deployed        kube-prometheus-stack-45.3.0    v0.63.0   
查看prometheus pods
root@upf:~# kubectl -n monitoring get pods 
NAME                                                 READY   STATUS    RESTARTS        AGE
prometheus-kube-prometheus-operator-7757f46c-vmsnj   1/1     Running   3 (5h30m ago)   8h
prometheus-kube-state-metrics-678b896dcf-8v6d6       1/1     Running   3 (5h30m ago)   8h
prometheus-prometheus-kube-prometheus-prometheus-0   2/2     Running   6 (5h30m ago)   8h
prometheus-prometheus-node-exporter-lhnwm            1/1     Running   3 (5h30m ago)   8h
卸载prometheus插件
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2171] · `chunk-992280cbf8ebd1bf1bfaf585`
```text
K8S集群软件故障排查 / 插件维护管理 / Prometheus
helm -n monitoring uninstall prometheus
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Prometheus
Prometheus
Prometheus为监控插件，能够收集并展示kubernetes集群组件、Node节点及pod监控指标。K8s集群中的Prometheus需要上报监控指标到网管平台，通过prometheus集群联邦方式进行对接，对接的定制化helm values.yaml配置已封装在镜像中。
sealos底层调用helm命令安装Prometheus插件，默认安装在monitoring命名空间下。
前置要求：已安装能够提供动态持久卷的存储插件，例如openebs。
安装prometheus插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/kube-prometheus-stack-cucc:v0.63.0
查看prometheus helm chart
root@upf:~# helm -n monitoring ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
prometheus      monitoring      1               2023-03-30 11:18:14.407943736 +0800 CST deployed        kube-prometheus-stack-45.3.0    v0.63.0   
查看prometheus pods
root@upf:~# kubectl -n monitoring get pods 
NAME                                                 READY   STATUS    RESTARTS        AGE
prometheus-kube-prometheus-operator-7757f46c-vmsnj   1/1     Running   3 (5h30m ago)   8h
prometheus-kube-state-metrics-678b896dcf-8v6d6       1/1     Running   3 (5h30m ago)   8h
prometheus-prometheus-kube-prometheus-prometheus-0   2/2     Running   6 (5h30m ago)   8h
prometheus-prometheus-node-exporter-lhnwm            1/1     Running   3 (5h30m ago)   8h
卸载prometheus插件
```

## troubleshooting-012 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / Prometheus’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-71f2f3f970d83664c466, manual-topic:section-71f2f3f970d83664c466
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2149], word/document.xml/body/p[2150], word/document.xml/body/p[2151], word/document.xml/body/p[2152], word/document.xml/body/p[2154], word/document.xml/body/p[2155], word/document.xml/body/p[2157], word/document.xml/body/p[2158], word/document.xml/body/p[2159], word/document.xml/body/p[2160], word/document.xml/body/p[2162], word/document.xml/body/p[2163], word/document.xml/body/p[2164], word/document.xml/body/p[2165], word/document.xml/body/p[2166], word/document.xml/body/p[2167], word/document.xml/body/p[2168], word/document.xml/body/p[2170] · `chunk-44dec42639466228f7fc64b8`
```text
K8S集群软件故障排查 / 插件维护管理 / Prometheus
Prometheus
Prometheus为监控插件，能够收集并展示kubernetes集群组件、Node节点及pod监控指标。K8s集群中的Prometheus需要上报监控指标到网管平台，通过prometheus集群联邦方式进行对接，对接的定制化helm values.yaml配置已封装在镜像中。
sealos底层调用helm命令安装Prometheus插件，默认安装在monitoring命名空间下。
前置要求：已安装能够提供动态持久卷的存储插件，例如openebs。
安装prometheus插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/kube-prometheus-stack-cucc:v0.63.0
查看prometheus helm chart
root@upf:~# helm -n monitoring ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
prometheus      monitoring      1               2023-03-30 11:18:14.407943736 +0800 CST deployed        kube-prometheus-stack-45.3.0    v0.63.0   
查看prometheus pods
root@upf:~# kubectl -n monitoring get pods 
NAME                                                 READY   STATUS    RESTARTS        AGE
prometheus-kube-prometheus-operator-7757f46c-vmsnj   1/1     Running   3 (5h30m ago)   8h
prometheus-kube-state-metrics-678b896dcf-8v6d6       1/1     Running   3 (5h30m ago)   8h
prometheus-prometheus-kube-prometheus-prometheus-0   2/2     Running   6 (5h30m ago)   8h
prometheus-prometheus-node-exporter-lhnwm            1/1     Running   3 (5h30m ago)   8h
卸载prometheus插件
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2171] · `chunk-992280cbf8ebd1bf1bfaf585`
```text
K8S集群软件故障排查 / 插件维护管理 / Prometheus
helm -n monitoring uninstall prometheus
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Prometheus
Prometheus
Prometheus为监控插件，能够收集并展示kubernetes集群组件、Node节点及pod监控指标。K8s集群中的Prometheus需要上报监控指标到网管平台，通过prometheus集群联邦方式进行对接，对接的定制化helm values.yaml配置已封装在镜像中。
sealos底层调用helm命令安装Prometheus插件，默认安装在monitoring命名空间下。
前置要求：已安装能够提供动态持久卷的存储插件，例如openebs。
安装prometheus插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/kube-prometheus-stack-cucc:v0.63.0
查看prometheus helm chart
root@upf:~# helm -n monitoring ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
prometheus      monitoring      1               2023-03-30 11:18:14.407943736 +0800 CST deployed        kube-prometheus-stack-45.3.0    v0.63.0   
查看prometheus pods
root@upf:~# kubectl -n monitoring get pods 
NAME                                                 READY   STATUS    RESTARTS        AGE
prometheus-kube-prometheus-operator-7757f46c-vmsnj   1/1     Running   3 (5h30m ago)   8h
prometheus-kube-state-metrics-678b896dcf-8v6d6       1/1     Running   3 (5h30m ago)   8h
prometheus-prometheus-kube-prometheus-prometheus-0   2/2     Running   6 (5h30m ago)   8h
prometheus-prometheus-node-exporter-lhnwm            1/1     Running   3 (5h30m ago)   8h
卸载prometheus插件
```

## troubleshooting-013 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / metrics-server’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-35088b60ccea71997817, manual-topic:section-35088b60ccea71997817
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2173], word/document.xml/body/p[2174], word/document.xml/body/p[2175], word/document.xml/body/p[2176], word/document.xml/body/p[2178], word/document.xml/body/p[2179], word/document.xml/body/p[2181], word/document.xml/body/p[2182], word/document.xml/body/p[2183], word/document.xml/body/p[2184], word/document.xml/body/p[2186], word/document.xml/body/p[2187], word/document.xml/body/p[2188], word/document.xml/body/p[2189], word/document.xml/body/p[2190], word/document.xml/body/p[2191], word/document.xml/body/p[2192], word/document.xml/body/p[2194] · `chunk-2032cdb234385f312f171aca`
```text
K8S集群软件故障排查 / 插件维护管理 / metrics-server
metrics-server
metrics-server为kubernetes指标收集插件。
sealos底层调用helm命令安装metrics-server插件，默认安装在kube-system命名空间下。
前置要求：已安装能够提供动态持久卷的存储插件，例如openebs。
安装prometheus插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/kube-prometheus-stack-cucc:v0.63.0
查看prometheus helm chart
root@upf:~# helm -n monitoring ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
prometheus      monitoring      1               2023-03-30 11:18:14.407943736 +0800 CST deployed        kube-prometheus-stack-45.3.0    v0.63.0   
查看prometheus pods
root@upf:~# kubectl -n monitoring get pods 
NAME                                                 READY   STATUS    RESTARTS        AGE
prometheus-kube-prometheus-operator-7757f46c-vmsnj   1/1     Running   3 (5h30m ago)   8h
prometheus-kube-state-metrics-678b896dcf-8v6d6       1/1     Running   3 (5h30m ago)   8h
prometheus-prometheus-kube-prometheus-prometheus-0   2/2     Running   6 (5h30m ago)   8h
prometheus-prometheus-node-exporter-lhnwm            1/1     Running   3 (5h30m ago)   8h
卸载prometheus插件
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2195] · `chunk-826d46714d0660f21dfb22e7`
```text
K8S集群软件故障排查 / 插件维护管理 / metrics-server
helm -n monitoring uninstall prometheus
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / metrics-server
metrics-server
metrics-server为kubernetes指标收集插件。
sealos底层调用helm命令安装metrics-server插件，默认安装在kube-system命名空间下。
前置要求：已安装能够提供动态持久卷的存储插件，例如openebs。
安装prometheus插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/kube-prometheus-stack-cucc:v0.63.0
查看prometheus helm chart
root@upf:~# helm -n monitoring ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
prometheus      monitoring      1               2023-03-30 11:18:14.407943736 +0800 CST deployed        kube-prometheus-stack-45.3.0    v0.63.0   
查看prometheus pods
root@upf:~# kubectl -n monitoring get pods 
NAME                                                 READY   STATUS    RESTARTS        AGE
prometheus-kube-prometheus-operator-7757f46c-vmsnj   1/1     Running   3 (5h30m ago)   8h
prometheus-kube-state-metrics-678b896dcf-8v6d6       1/1     Running   3 (5h30m ago)   8h
prometheus-prometheus-kube-prometheus-prometheus-0   2/2     Running   6 (5h30m ago)   8h
prometheus-prometheus-node-exporter-lhnwm            1/1     Running   3 (5h30m ago)   8h
卸载prometheus插件
```

## troubleshooting-014 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / metrics-server’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-35088b60ccea71997817, manual-topic:section-35088b60ccea71997817
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2173], word/document.xml/body/p[2174], word/document.xml/body/p[2175], word/document.xml/body/p[2176], word/document.xml/body/p[2178], word/document.xml/body/p[2179], word/document.xml/body/p[2181], word/document.xml/body/p[2182], word/document.xml/body/p[2183], word/document.xml/body/p[2184], word/document.xml/body/p[2186], word/document.xml/body/p[2187], word/document.xml/body/p[2188], word/document.xml/body/p[2189], word/document.xml/body/p[2190], word/document.xml/body/p[2191], word/document.xml/body/p[2192], word/document.xml/body/p[2194] · `chunk-2032cdb234385f312f171aca`
```text
K8S集群软件故障排查 / 插件维护管理 / metrics-server
metrics-server
metrics-server为kubernetes指标收集插件。
sealos底层调用helm命令安装metrics-server插件，默认安装在kube-system命名空间下。
前置要求：已安装能够提供动态持久卷的存储插件，例如openebs。
安装prometheus插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/kube-prometheus-stack-cucc:v0.63.0
查看prometheus helm chart
root@upf:~# helm -n monitoring ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
prometheus      monitoring      1               2023-03-30 11:18:14.407943736 +0800 CST deployed        kube-prometheus-stack-45.3.0    v0.63.0   
查看prometheus pods
root@upf:~# kubectl -n monitoring get pods 
NAME                                                 READY   STATUS    RESTARTS        AGE
prometheus-kube-prometheus-operator-7757f46c-vmsnj   1/1     Running   3 (5h30m ago)   8h
prometheus-kube-state-metrics-678b896dcf-8v6d6       1/1     Running   3 (5h30m ago)   8h
prometheus-prometheus-kube-prometheus-prometheus-0   2/2     Running   6 (5h30m ago)   8h
prometheus-prometheus-node-exporter-lhnwm            1/1     Running   3 (5h30m ago)   8h
卸载prometheus插件
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2195] · `chunk-826d46714d0660f21dfb22e7`
```text
K8S集群软件故障排查 / 插件维护管理 / metrics-server
helm -n monitoring uninstall prometheus
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / metrics-server
metrics-server
metrics-server为kubernetes指标收集插件。
sealos底层调用helm命令安装metrics-server插件，默认安装在kube-system命名空间下。
前置要求：已安装能够提供动态持久卷的存储插件，例如openebs。
安装prometheus插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/kube-prometheus-stack-cucc:v0.63.0
查看prometheus helm chart
root@upf:~# helm -n monitoring ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                           APP VERSION
prometheus      monitoring      1               2023-03-30 11:18:14.407943736 +0800 CST deployed        kube-prometheus-stack-45.3.0    v0.63.0   
查看prometheus pods
root@upf:~# kubectl -n monitoring get pods 
NAME                                                 READY   STATUS    RESTARTS        AGE
prometheus-kube-prometheus-operator-7757f46c-vmsnj   1/1     Running   3 (5h30m ago)   8h
prometheus-kube-state-metrics-678b896dcf-8v6d6       1/1     Running   3 (5h30m ago)   8h
prometheus-prometheus-kube-prometheus-prometheus-0   2/2     Running   6 (5h30m ago)   8h
prometheus-prometheus-node-exporter-lhnwm            1/1     Running   3 (5h30m ago)   8h
卸载prometheus插件
```

## troubleshooting-015 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / neuvector’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-5835be0d1b25af930f10, manual-topic:section-5835be0d1b25af930f10
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2199], word/document.xml/body/p[2200], word/document.xml/body/p[2201], word/document.xml/body/p[2202], word/document.xml/body/p[2203], word/document.xml/body/p[2204], word/document.xml/body/p[2205], word/document.xml/body/p[2207], word/document.xml/body/p[2208], word/document.xml/body/p[2209], word/document.xml/body/p[2210], word/document.xml/body/p[2212], word/document.xml/body/p[2213], word/document.xml/body/p[2214], word/document.xml/body/p[2215], word/document.xml/body/p[2216], word/document.xml/body/p[2217], word/document.xml/body/p[2218], word/document.xml/body/p[2219], word/document.xml/body/p[2220], word/document.xml/body/p[2221], word/document.xml/body/p[2222], word/document.xml/body/p[2224], word/document.xml/body/p[2225], word/document.xml/body/p[2226] · `chunk-341849387ced289c516b6092`
```text
K8S集群软件故障排查 / 插件维护管理 / neuvector
neuvector
neuvector为容器安全平台，提供云原生安全能力，支持策略及安全漏洞管理等功能。
sealos底层调用helm命令安装neuvector插件，默认安装 neuvector命名空间下。
前置要求：
已安装能够提供动态持久卷的存储插件，例如openebs。
安装neuvector插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/neuvector-cucc:v5.1.0
查看neuvector helm chart
root@upf:~# helm -n neuvector ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
neuvector       neuvector       1               2023-03-30 20:02:54.970668995 +0800 CST deployed        core-2.4.0      5.1.0      
3.	查看neuvector pods
root@upf:~# kubectl -n neuvector get pods 
NAME                                        READY   STATUS    RESTARTS   AGE
neuvector-controller-pod-7fb7cb8f7f-2rhxr   1/1     Running   0          59s
neuvector-controller-pod-7fb7cb8f7f-84hvv   1/1     Running   0          59s
neuvector-controller-pod-7fb7cb8f7f-qdthv   1/1     Running   0          59s
neuvector-enforcer-pod-vhg52                1/1     Running   0          59s
neuvector-manager-pod-56545c488d-zn24b      1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-42pls       1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-ch4ft       1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-qlt67       1/1     Running   0          59s
4.	查看neuvector service
root@upf:~# kubectl -n neuvector get svc
NAME                              TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                         AGE
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2227], word/document.xml/body/p[2228], word/document.xml/body/p[2229], word/document.xml/body/p[2230], word/document.xml/body/p[2232], word/document.xml/body/p[2233], word/document.xml/body/p[2234], word/document.xml/body/p[2235], word/document.xml/body/p[2236], word/document.xml/body/p[2238], word/document.xml/body/p[2239] · `chunk-8dfff29fe6bd2f2ca0622876`
```text
K8S集群软件故障排查 / 插件维护管理 / neuvector
neuvector-service-webui           NodePort    10.96.3.55   <none>        8443:30106/TCP                  2m9s
neuvector-svc-admission-webhook   ClusterIP   10.96.1.80   <none>        443/TCP                         2m9s
neuvector-svc-controller          ClusterIP   None         <none>        18300/TCP,18301/TCP,18301/UDP   2m9s
neuvector-svc-crd-webhook         ClusterIP   10.96.2.59   <none>        443/TCP                         2m9s
5.	访问neuvector管理界面，默认用户名密码为admin/admin，浏览器打开以下URL地址：
https://<node-ip>:<node-port>
说明
node-ip：  为k8s任意节点IP
node-port：为neuvector-service-webui service对应的nodeport，以上示例为30106
6.	卸载neuvector插件
$ helm -n neuvector uninstall neuvector
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / neuvector
neuvector
neuvector为容器安全平台，提供云原生安全能力，支持策略及安全漏洞管理等功能。
sealos底层调用helm命令安装neuvector插件，默认安装 neuvector命名空间下。
前置要求：
已安装能够提供动态持久卷的存储插件，例如openebs。
安装neuvector插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/neuvector-cucc:v5.1.0
查看neuvector helm chart
root@upf:~# helm -n neuvector ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
neuvector       neuvector       1               2023-03-30 20:02:54.970668995 +0800 CST deployed        core-2.4.0      5.1.0      
3.	查看neuvector pods
root@upf:~# kubectl -n neuvector get pods 
NAME                                        READY   STATUS    RESTARTS   AGE
neuvector-controller-pod-7fb7cb8f7f-2rhxr   1/1     Running   0          59s
neuvector-controller-pod-7fb7cb8f7f-84hvv   1/1     Running   0          59s
neuvector-controller-pod-7fb7cb8f7f-qdthv   1/1     Running   0          59s
neuvector-enforcer-pod-vhg52                1/1     Running   0          59s
neuvector-manager-pod-56545c488d-zn24b      1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-42pls       1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-ch4ft       1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-qlt67       1/1     Running   0          59s
4.	查看neuvector service
root@upf:~# kubectl -n neuvector get svc
NAME                              TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                         AGE
```

## troubleshooting-016 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / neuvector’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-5835be0d1b25af930f10, manual-topic:section-5835be0d1b25af930f10
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2199], word/document.xml/body/p[2200], word/document.xml/body/p[2201], word/document.xml/body/p[2202], word/document.xml/body/p[2203], word/document.xml/body/p[2204], word/document.xml/body/p[2205], word/document.xml/body/p[2207], word/document.xml/body/p[2208], word/document.xml/body/p[2209], word/document.xml/body/p[2210], word/document.xml/body/p[2212], word/document.xml/body/p[2213], word/document.xml/body/p[2214], word/document.xml/body/p[2215], word/document.xml/body/p[2216], word/document.xml/body/p[2217], word/document.xml/body/p[2218], word/document.xml/body/p[2219], word/document.xml/body/p[2220], word/document.xml/body/p[2221], word/document.xml/body/p[2222], word/document.xml/body/p[2224], word/document.xml/body/p[2225], word/document.xml/body/p[2226] · `chunk-341849387ced289c516b6092`
```text
K8S集群软件故障排查 / 插件维护管理 / neuvector
neuvector
neuvector为容器安全平台，提供云原生安全能力，支持策略及安全漏洞管理等功能。
sealos底层调用helm命令安装neuvector插件，默认安装 neuvector命名空间下。
前置要求：
已安装能够提供动态持久卷的存储插件，例如openebs。
安装neuvector插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/neuvector-cucc:v5.1.0
查看neuvector helm chart
root@upf:~# helm -n neuvector ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
neuvector       neuvector       1               2023-03-30 20:02:54.970668995 +0800 CST deployed        core-2.4.0      5.1.0      
3.	查看neuvector pods
root@upf:~# kubectl -n neuvector get pods 
NAME                                        READY   STATUS    RESTARTS   AGE
neuvector-controller-pod-7fb7cb8f7f-2rhxr   1/1     Running   0          59s
neuvector-controller-pod-7fb7cb8f7f-84hvv   1/1     Running   0          59s
neuvector-controller-pod-7fb7cb8f7f-qdthv   1/1     Running   0          59s
neuvector-enforcer-pod-vhg52                1/1     Running   0          59s
neuvector-manager-pod-56545c488d-zn24b      1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-42pls       1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-ch4ft       1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-qlt67       1/1     Running   0          59s
4.	查看neuvector service
root@upf:~# kubectl -n neuvector get svc
NAME                              TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                         AGE
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2227], word/document.xml/body/p[2228], word/document.xml/body/p[2229], word/document.xml/body/p[2230], word/document.xml/body/p[2232], word/document.xml/body/p[2233], word/document.xml/body/p[2234], word/document.xml/body/p[2235], word/document.xml/body/p[2236], word/document.xml/body/p[2238], word/document.xml/body/p[2239] · `chunk-8dfff29fe6bd2f2ca0622876`
```text
K8S集群软件故障排查 / 插件维护管理 / neuvector
neuvector-service-webui           NodePort    10.96.3.55   <none>        8443:30106/TCP                  2m9s
neuvector-svc-admission-webhook   ClusterIP   10.96.1.80   <none>        443/TCP                         2m9s
neuvector-svc-controller          ClusterIP   None         <none>        18300/TCP,18301/TCP,18301/UDP   2m9s
neuvector-svc-crd-webhook         ClusterIP   10.96.2.59   <none>        443/TCP                         2m9s
5.	访问neuvector管理界面，默认用户名密码为admin/admin，浏览器打开以下URL地址：
https://<node-ip>:<node-port>
说明
node-ip：  为k8s任意节点IP
node-port：为neuvector-service-webui service对应的nodeport，以上示例为30106
6.	卸载neuvector插件
$ helm -n neuvector uninstall neuvector
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / neuvector
neuvector
neuvector为容器安全平台，提供云原生安全能力，支持策略及安全漏洞管理等功能。
sealos底层调用helm命令安装neuvector插件，默认安装 neuvector命名空间下。
前置要求：
已安装能够提供动态持久卷的存储插件，例如openebs。
安装neuvector插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/neuvector-cucc:v5.1.0
查看neuvector helm chart
root@upf:~# helm -n neuvector ls
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
neuvector       neuvector       1               2023-03-30 20:02:54.970668995 +0800 CST deployed        core-2.4.0      5.1.0      
3.	查看neuvector pods
root@upf:~# kubectl -n neuvector get pods 
NAME                                        READY   STATUS    RESTARTS   AGE
neuvector-controller-pod-7fb7cb8f7f-2rhxr   1/1     Running   0          59s
neuvector-controller-pod-7fb7cb8f7f-84hvv   1/1     Running   0          59s
neuvector-controller-pod-7fb7cb8f7f-qdthv   1/1     Running   0          59s
neuvector-enforcer-pod-vhg52                1/1     Running   0          59s
neuvector-manager-pod-56545c488d-zn24b      1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-42pls       1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-ch4ft       1/1     Running   0          59s
neuvector-scanner-pod-58dd8685b-qlt67       1/1     Running   0          59s
4.	查看neuvector service
root@upf:~# kubectl -n neuvector get svc
NAME                              TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                         AGE
```

## troubleshooting-017 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / loki’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-3b1a406d0a431c8b9682, manual-topic:section-3b1a406d0a431c8b9682
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2240], word/document.xml/body/p[2241], word/document.xml/body/p[2242], word/document.xml/body/p[2243], word/document.xml/body/p[2244], word/document.xml/body/p[2246], word/document.xml/body/p[2247], word/document.xml/body/p[2249], word/document.xml/body/p[2250], word/document.xml/body/p[2251], word/document.xml/body/p[2252], word/document.xml/body/p[2254], word/document.xml/body/p[2255], word/document.xml/body/p[2256], word/document.xml/body/p[2257], word/document.xml/body/p[2258], word/document.xml/body/p[2259], word/document.xml/body/p[2261], word/document.xml/body/p[2262] · `chunk-1bdb012f460aa7597052f1f6`
```text
K8S集群软件故障排查 / 插件维护管理 / loki
loki
loki为日志插件，提供pod日志收集、日志存储及日志检索功能。
sealos底层调用helm命令安装loki插件，默认安装 neuvector命名空间下。
前置要求：
已安装能够提供动态持久卷的存储插件，例如openebs。
安装loki日志插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/loki-stack:v2.6.1
查看loki helm chart
$ helm -n loki-stack ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
loki    loki-stack      1               2023-03-30 20:09:23.047869149 +0800 CST deployed        loki-stack-2.9.9        v2.6.1   
查看loki pods
$ kubectl -n loki-stack get pods 
NAME                            READY   STATUS    RESTARTS   AGE
loki-0                          1/1     Running   0          2m26s
loki-fluent-bit-loki-dvq7j      1/1     Running   0          2m27s
loki-grafana-86cf98768c-2lzqq   2/2     Running   0          2m26s
卸载loki日志插件
$ helm -n loki-stack uninstall loki
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / loki
loki
loki为日志插件，提供pod日志收集、日志存储及日志检索功能。
sealos底层调用helm命令安装loki插件，默认安装 neuvector命名空间下。
前置要求：
已安装能够提供动态持久卷的存储插件，例如openebs。
安装loki日志插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/loki-stack:v2.6.1
查看loki helm chart
$ helm -n loki-stack ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
loki    loki-stack      1               2023-03-30 20:09:23.047869149 +0800 CST deployed        loki-stack-2.9.9        v2.6.1   
查看loki pods
$ kubectl -n loki-stack get pods 
NAME                            READY   STATUS    RESTARTS   AGE
loki-0                          1/1     Running   0          2m26s
loki-fluent-bit-loki-dvq7j      1/1     Running   0          2m27s
loki-grafana-86cf98768c-2lzqq   2/2     Running   0          2m26s
卸载loki日志插件
$ helm -n loki-stack uninstall loki
```

## troubleshooting-018 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / loki’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-3b1a406d0a431c8b9682, manual-topic:section-3b1a406d0a431c8b9682
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2240], word/document.xml/body/p[2241], word/document.xml/body/p[2242], word/document.xml/body/p[2243], word/document.xml/body/p[2244], word/document.xml/body/p[2246], word/document.xml/body/p[2247], word/document.xml/body/p[2249], word/document.xml/body/p[2250], word/document.xml/body/p[2251], word/document.xml/body/p[2252], word/document.xml/body/p[2254], word/document.xml/body/p[2255], word/document.xml/body/p[2256], word/document.xml/body/p[2257], word/document.xml/body/p[2258], word/document.xml/body/p[2259], word/document.xml/body/p[2261], word/document.xml/body/p[2262] · `chunk-1bdb012f460aa7597052f1f6`
```text
K8S集群软件故障排查 / 插件维护管理 / loki
loki
loki为日志插件，提供pod日志收集、日志存储及日志检索功能。
sealos底层调用helm命令安装loki插件，默认安装 neuvector命名空间下。
前置要求：
已安装能够提供动态持久卷的存储插件，例如openebs。
安装loki日志插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/loki-stack:v2.6.1
查看loki helm chart
$ helm -n loki-stack ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
loki    loki-stack      1               2023-03-30 20:09:23.047869149 +0800 CST deployed        loki-stack-2.9.9        v2.6.1   
查看loki pods
$ kubectl -n loki-stack get pods 
NAME                            READY   STATUS    RESTARTS   AGE
loki-0                          1/1     Running   0          2m26s
loki-fluent-bit-loki-dvq7j      1/1     Running   0          2m27s
loki-grafana-86cf98768c-2lzqq   2/2     Running   0          2m26s
卸载loki日志插件
$ helm -n loki-stack uninstall loki
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / loki
loki
loki为日志插件，提供pod日志收集、日志存储及日志检索功能。
sealos底层调用helm命令安装loki插件，默认安装 neuvector命名空间下。
前置要求：
已安装能够提供动态持久卷的存储插件，例如openebs。
安装loki日志插件
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/loki-stack:v2.6.1
查看loki helm chart
$ helm -n loki-stack ls
NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
loki    loki-stack      1               2023-03-30 20:09:23.047869149 +0800 CST deployed        loki-stack-2.9.9        v2.6.1   
查看loki pods
$ kubectl -n loki-stack get pods 
NAME                            READY   STATUS    RESTARTS   AGE
loki-0                          1/1     Running   0          2m26s
loki-fluent-bit-loki-dvq7j      1/1     Running   0          2m27s
loki-grafana-86cf98768c-2lzqq   2/2     Running   0          2m26s
卸载loki日志插件
$ helm -n loki-stack uninstall loki
```

## troubleshooting-019 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：手册中‘K8S集群软件故障排查 / 插件维护管理 / nerdctl’的排查步骤和操作前提是什么？请给出原文依据。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-64ecd9579d44407b456a, manual-topic:section-64ecd9579d44407b456a
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2264], word/document.xml/body/p[2265], word/document.xml/body/p[2266], word/document.xml/body/p[2267], word/document.xml/body/p[2268], word/document.xml/body/p[2269], word/document.xml/body/p[2270], word/document.xml/body/p[2271], word/document.xml/body/p[2272], word/document.xml/body/p[2274], word/document.xml/body/p[2275], word/document.xml/body/p[2276], word/document.xml/body/p[2277], word/document.xml/body/p[2278], word/document.xml/body/p[2279], word/document.xml/body/p[2280], word/document.xml/body/p[2281], word/document.xml/body/p[2282], word/document.xml/body/p[2283], word/document.xml/body/p[2284], word/document.xml/body/p[2285], word/document.xml/body/p[2286], word/document.xml/body/p[2287], word/document.xml/body/p[2288] · `chunk-543b1cffe44ddb7a504e09f8`
```text
K8S集群软件故障排查 / 插件维护管理 / nerdctl
nerdctl
nerdctl是containerd官方命令行客户端工具，用于管理容器及镜像，默认安装在所有集群节点/usr/local/bin目录下。nerdctl build子命令支持在本地构建镜像，但依赖buildkit，因此该插件也封装了buildkit二进制文件，并后台运行一个buildkit.service systemd服务。
执行以下命令安装nerdctl插件
$ sealos run docker.io/labring/nerdctl:v1.2.1
使用以下命令查看nerdctl安装路径
$ which nerdctl 
/usr/local/bin/nerdctl
如需卸载nerdctl插件，执行以下命令
$ sealos run docker.io/labring/nerdctl:v1.2.1 -e uninstall=true
Nerdctl常用命令
拉取镜像
nerdctl pull alpine
打包镜像
nerdctl save -o alpine.tar.gz alpine
Load镜像
nerdctl load -i alpine.tar.gz
Load镜像到k8s命名空间
nerdctl --namespace k8s.io load < /path/to/image.tar
Retag镜像
nerdctl tag alpine alpine:v1.0
Build镜像
nerdctl build -t test:v1.0 .
运行容器
nerdctl run -d –name nginx docker.io/library/nginx:latest
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / nerdctl
nerdctl
nerdctl是containerd官方命令行客户端工具，用于管理容器及镜像，默认安装在所有集群节点/usr/local/bin目录下。nerdctl build子命令支持在本地构建镜像，但依赖buildkit，因此该插件也封装了buildkit二进制文件，并后台运行一个buildkit.service systemd服务。
执行以下命令安装nerdctl插件
$ sealos run docker.io/labring/nerdctl:v1.2.1
使用以下命令查看nerdctl安装路径
$ which nerdctl 
/usr/local/bin/nerdctl
如需卸载nerdctl插件，执行以下命令
$ sealos run docker.io/labring/nerdctl:v1.2.1 -e uninstall=true
Nerdctl常用命令
拉取镜像
nerdctl pull alpine
打包镜像
nerdctl save -o alpine.tar.gz alpine
Load镜像
nerdctl load -i alpine.tar.gz
Load镜像到k8s命名空间
nerdctl --namespace k8s.io load < /path/to/image.tar
Retag镜像
nerdctl tag alpine alpine:v1.0
Build镜像
nerdctl build -t test:v1.0 .
运行容器
nerdctl run -d –name nginx docker.io/library/nginx:latest
```

## troubleshooting-020 · heldout · troubleshooting

- [x] 问题及预期事实/相关证据已核对
- 问题：请依据‘K8S集群软件故障排查 / 插件维护管理 / nerdctl’解释排查步骤和操作前提，不要推断真实设备当前状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：section-64ecd9579d44407b456a, manual-topic:section-64ecd9579d44407b456a
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · word/document.xml/body/p[2264], word/document.xml/body/p[2265], word/document.xml/body/p[2266], word/document.xml/body/p[2267], word/document.xml/body/p[2268], word/document.xml/body/p[2269], word/document.xml/body/p[2270], word/document.xml/body/p[2271], word/document.xml/body/p[2272], word/document.xml/body/p[2274], word/document.xml/body/p[2275], word/document.xml/body/p[2276], word/document.xml/body/p[2277], word/document.xml/body/p[2278], word/document.xml/body/p[2279], word/document.xml/body/p[2280], word/document.xml/body/p[2281], word/document.xml/body/p[2282], word/document.xml/body/p[2283], word/document.xml/body/p[2284], word/document.xml/body/p[2285], word/document.xml/body/p[2286], word/document.xml/body/p[2287], word/document.xml/body/p[2288] · `chunk-543b1cffe44ddb7a504e09f8`
```text
K8S集群软件故障排查 / 插件维护管理 / nerdctl
nerdctl
nerdctl是containerd官方命令行客户端工具，用于管理容器及镜像，默认安装在所有集群节点/usr/local/bin目录下。nerdctl build子命令支持在本地构建镜像，但依赖buildkit，因此该插件也封装了buildkit二进制文件，并后台运行一个buildkit.service systemd服务。
执行以下命令安装nerdctl插件
$ sealos run docker.io/labring/nerdctl:v1.2.1
使用以下命令查看nerdctl安装路径
$ which nerdctl 
/usr/local/bin/nerdctl
如需卸载nerdctl插件，执行以下命令
$ sealos run docker.io/labring/nerdctl:v1.2.1 -e uninstall=true
Nerdctl常用命令
拉取镜像
nerdctl pull alpine
打包镜像
nerdctl save -o alpine.tar.gz alpine
Load镜像
nerdctl load -i alpine.tar.gz
Load镜像到k8s命名空间
nerdctl --namespace k8s.io load < /path/to/image.tar
Retag镜像
nerdctl tag alpine alpine:v1.0
Build镜像
nerdctl build -t test:v1.0 .
运行容器
nerdctl run -d –name nginx docker.io/library/nginx:latest
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / nerdctl
nerdctl
nerdctl是containerd官方命令行客户端工具，用于管理容器及镜像，默认安装在所有集群节点/usr/local/bin目录下。nerdctl build子命令支持在本地构建镜像，但依赖buildkit，因此该插件也封装了buildkit二进制文件，并后台运行一个buildkit.service systemd服务。
执行以下命令安装nerdctl插件
$ sealos run docker.io/labring/nerdctl:v1.2.1
使用以下命令查看nerdctl安装路径
$ which nerdctl 
/usr/local/bin/nerdctl
如需卸载nerdctl插件，执行以下命令
$ sealos run docker.io/labring/nerdctl:v1.2.1 -e uninstall=true
Nerdctl常用命令
拉取镜像
nerdctl pull alpine
打包镜像
nerdctl save -o alpine.tar.gz alpine
Load镜像
nerdctl load -i alpine.tar.gz
Load镜像到k8s命名空间
nerdctl --namespace k8s.io load < /path/to/image.tar
Retag镜像
nerdctl tag alpine alpine:v1.0
Build镜像
nerdctl build -t test:v1.0 .
运行容器
nerdctl run -d –name nginx docker.io/library/nginx:latest
```

## log-001 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-3182914` · 行 15128–15128 · 候选状态 `observed`
```text
2025-05-15 09:10:45.375909 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- `log-a698d029342259b7-3516922` · 行 17632–17632 · 候选状态 `observed`
```text
2025-05-15 09:11:09.253460 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- `log-a698d029342259b7-3601293` · 行 18264–18264 · 候选状态 `observed`
```text
2025-05-15 09:11:15.376158 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 pfcp_heartbeat_request 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:pfcp_heartbeat_request
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-002 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-3182914` · 行 15128–15128 · 候选状态 `observed`
```text
2025-05-15 09:10:45.375909 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- `log-a698d029342259b7-3516922` · 行 17632–17632 · 候选状态 `observed`
```text
2025-05-15 09:11:09.253460 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- `log-a698d029342259b7-3601293` · 行 18264–18264 · 候选状态 `observed`
```text
2025-05-15 09:11:15.376158 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 pfcp_heartbeat_request，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:pfcp_heartbeat_request
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-003 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-5967589` · 行 30659–30659 · 候选状态 `raised`
```text
2025-05-21 20:57:10.493959 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- `log-a698d029342259b7-5968078` · 行 30662–30662 · 候选状态 `raised`
```text
2025-05-21 20:57:10.494068 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- `log-a698d029342259b7-6327317` · 行 32430–32430 · 候选状态 `raised`
```text
2025-07-12 01:00:46.637266 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 pfcp_node_unreachable 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:pfcp_node_unreachable
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-004 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-5967589` · 行 30659–30659 · 候选状态 `raised`
```text
2025-05-21 20:57:10.493959 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- `log-a698d029342259b7-5968078` · 行 30662–30662 · 候选状态 `raised`
```text
2025-05-21 20:57:10.494068 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- `log-a698d029342259b7-6327317` · 行 32430–32430 · 候选状态 `raised`
```text
2025-07-12 01:00:46.637266 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 pfcp_node_unreachable，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:pfcp_node_unreachable
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-005 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-12005` · 行 101–101 · 候选状态 `observed`
```text
2025-05-14 20:08:47.594133 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- `log-a698d029342259b7-12283` · 行 102–102 · 候选状态 `observed`
```text
2025-05-14 20:09:07.624673 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- `log-a698d029342259b7-12561` · 行 103–103 · 候选状态 `observed`
```text
2025-05-14 20:09:09.577742 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 far_handover 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:far_handover
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-006 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-12005` · 行 101–101 · 候选状态 `observed`
```text
2025-05-14 20:08:47.594133 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- `log-a698d029342259b7-12283` · 行 102–102 · 候选状态 `observed`
```text
2025-05-14 20:09:07.624673 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- `log-a698d029342259b7-12561` · 行 103–103 · 候选状态 `observed`
```text
2025-05-14 20:09:09.577742 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 far_handover，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:far_handover
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-007 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-14801` · 行 113–113 · 候选状态 `observed`
```text
2025-05-14 20:09:43.031831 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 1, count:0
```
- `log-a698d029342259b7-15588` · 行 117–117 · 候选状态 `observed`
```text
2025-05-14 20:09:48.036719 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 1, count:1
```
- `log-a698d029342259b7-16375` · 行 121–121 · 候选状态 `observed`
```text
2025-05-14 20:09:52.040343 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 2, count:0
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 gtpu_echo_retry 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:gtpu_echo_retry
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-008 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-14801` · 行 113–113 · 候选状态 `observed`
```text
2025-05-14 20:09:43.031831 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 1, count:0
```
- `log-a698d029342259b7-15588` · 行 117–117 · 候选状态 `observed`
```text
2025-05-14 20:09:48.036719 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 1, count:1
```
- `log-a698d029342259b7-16375` · 行 121–121 · 候选状态 `observed`
```text
2025-05-14 20:09:52.040343 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 2, count:0
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 gtpu_echo_retry，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:gtpu_echo_retry
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-009 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-1683` · 行 16–16 · 候选状态 `raised`
```text
2025-05-14 16:07:43.723036 ERROR FID.0 upfd_alarm.c:816(upfdAlarmLicenseNotInstall): Report license not installed alarm
```
- `log-a698d029342259b7-4545` · 行 41–41 · 候选状态 `cleared`
```text
2025-05-14 16:17:05.649346 ERROR FID.0 upfd_alarm.c:823(upfdAlarmLicenseNotInstall): Clear license not installed alarm
```
- `log-a698d029342259b7-6728` · 行 58–58 · 候选状态 `cleared`
```text
2025-05-14 16:21:21.586574 ERROR FID.0 upfd_alarm.c:823(upfdAlarmLicenseNotInstall): Clear license not installed alarm
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 license_not_installed 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:license_not_installed
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-010 · dev · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-1683` · 行 16–16 · 候选状态 `raised`
```text
2025-05-14 16:07:43.723036 ERROR FID.0 upfd_alarm.c:816(upfdAlarmLicenseNotInstall): Report license not installed alarm
```
- `log-a698d029342259b7-4545` · 行 41–41 · 候选状态 `cleared`
```text
2025-05-14 16:17:05.649346 ERROR FID.0 upfd_alarm.c:823(upfdAlarmLicenseNotInstall): Clear license not installed alarm
```
- `log-a698d029342259b7-6728` · 行 58–58 · 候选状态 `cleared`
```text
2025-05-14 16:21:21.586574 ERROR FID.0 upfd_alarm.c:823(upfdAlarmLicenseNotInstall): Clear license not installed alarm
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 license_not_installed，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:license_not_installed
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-011 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-3183220` · 行 15131–15131 · 候选状态 `observed`
```text
2025-05-15 09:10:45.375964 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc02:1706:406::, msg len:16
```
- `log-a698d029342259b7-3517228` · 行 17635–17635 · 候选状态 `observed`
```text
2025-05-15 09:11:09.253518 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc01:1706:406::, msg len:16
```
- `log-a698d029342259b7-3601599` · 行 18267–18267 · 候选状态 `observed`
```text
2025-05-15 09:11:15.376211 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc02:1706:406::, msg len:16
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 pfcp_heartbeat_response 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:pfcp_heartbeat_response
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-012 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-3183220` · 行 15131–15131 · 候选状态 `observed`
```text
2025-05-15 09:10:45.375964 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc02:1706:406::, msg len:16
```
- `log-a698d029342259b7-3517228` · 行 17635–17635 · 候选状态 `observed`
```text
2025-05-15 09:11:09.253518 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc01:1706:406::, msg len:16
```
- `log-a698d029342259b7-3601599` · 行 18267–18267 · 候选状态 `observed`
```text
2025-05-15 09:11:15.376211 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc02:1706:406::, msg len:16
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 pfcp_heartbeat_response，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:pfcp_heartbeat_response
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-013 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-13071` · 行 105–105 · 候选状态 `observed`
```text
2025-05-14 20:09:33.531692 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 1
```
- `log-a698d029342259b7-13725` · 行 108–108 · 候选状态 `observed`
```text
2025-05-14 20:09:37.047651 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 2
```
- `log-a698d029342259b7-14379` · 行 111–111 · 候选状态 `observed`
```text
2025-05-14 20:09:40.981915 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 3
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 pfcp_session_deleted 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:pfcp_session_deleted
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-014 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-13071` · 行 105–105 · 候选状态 `observed`
```text
2025-05-14 20:09:33.531692 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 1
```
- `log-a698d029342259b7-13725` · 行 108–108 · 候选状态 `observed`
```text
2025-05-14 20:09:37.047651 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 2
```
- `log-a698d029342259b7-14379` · 行 111–111 · 候选状态 `observed`
```text
2025-05-14 20:09:40.981915 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 3
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 pfcp_session_deleted，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:pfcp_session_deleted
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-015 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-2080` · 行 19–19 · 候选状态 `observed`
```text
2025-05-14 16:08:18.611476 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- `log-a698d029342259b7-2632` · 行 24–24 · 候选状态 `observed`
```text
2025-05-14 16:08:18.614064 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- `log-a698d029342259b7-6998` · 行 60–60 · 候选状态 `observed`
```text
2025-05-14 16:21:22.503527 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 interface_index_failure 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:interface_index_failure
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-016 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-2080` · 行 19–19 · 候选状态 `observed`
```text
2025-05-14 16:08:18.611476 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- `log-a698d029342259b7-2632` · 行 24–24 · 候选状态 `observed`
```text
2025-05-14 16:08:18.614064 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- `log-a698d029342259b7-6998` · 行 60–60 · 候选状态 `observed`
```text
2025-05-14 16:21:22.503527 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 interface_index_failure，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:interface_index_failure
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-017 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-4665` · 行 42–42 · 候选状态 `observed`
```text
2025-05-14 16:20:58.592356 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc1@*.*:' | awk -F: '{print $1}' failed
```
- `log-a698d029342259b7-4848` · 行 43–43 · 候选状态 `observed`
```text
2025-05-14 16:20:58.595262 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc2@*.*:' | awk -F: '{print $1}' failed
```
- `log-a698d029342259b7-5031` · 行 44–44 · 候选状态 `observed`
```text
2025-05-14 16:21:06.588513 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc1@*.*:' | awk -F: '{print $1}' failed
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 n4_name_failure 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:n4_name_failure
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-018 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-4665` · 行 42–42 · 候选状态 `observed`
```text
2025-05-14 16:20:58.592356 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc1@*.*:' | awk -F: '{print $1}' failed
```
- `log-a698d029342259b7-4848` · 行 43–43 · 候选状态 `observed`
```text
2025-05-14 16:20:58.595262 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc2@*.*:' | awk -F: '{print $1}' failed
```
- `log-a698d029342259b7-5031` · 行 44–44 · 候选状态 `observed`
```text
2025-05-14 16:21:06.588513 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc1@*.*:' | awk -F: '{print $1}' failed
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 n4_name_failure，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:n4_name_failure
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-019 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-17561` · 行 128–128 · 候选状态 `raised`
```text
2025-05-14 20:09:58.045994 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- `log-a698d029342259b7-19494` · 行 139–139 · 候选状态 `raised`
```text
2025-05-14 20:10:07.005699 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- `log-a698d029342259b7-19720` · 行 141–141 · 候选状态 `raised`
```text
2025-05-14 20:10:11.009574 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```

- [x] 问题及预期事实/相关证据已核对
- 问题：查询 gtpu_unreachable_detected 的代表日志，保留发生/解除/正常状态。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:gtpu_unreachable_detected
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-020 · heldout · log

- 日志样本原文（需人工核对事件类型与状态）：
- `log-a698d029342259b7-17561` · 行 128–128 · 候选状态 `raised`
```text
2025-05-14 20:09:58.045994 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- `log-a698d029342259b7-19494` · 行 139–139 · 候选状态 `raised`
```text
2025-05-14 20:10:07.005699 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- `log-a698d029342259b7-19720` · 行 141–141 · 候选状态 `raised`
```text
2025-05-14 20:10:11.009574 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```

- [x] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 gtpu_unreachable_detected，说明能否据此确定独立故障和根因。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：log-template:gtpu_unreachable_detected
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## topology-001 · dev · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 0：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:0
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_0.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-0:eth0 -> SYN-SW-0:port1; N3; synthetic
```

## topology-002 · dev · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 0：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:0
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_0.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-0:eth0 -> SYN-SW-0:port1; N3; synthetic
```

## topology-003 · dev · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 1：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:1
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_1.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-1:eth0 -> SYN-SW-1:port1; N3; synthetic
```

## topology-004 · dev · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 1：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:1
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_1.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-1:eth0 -> SYN-SW-1:port1; N3; synthetic
```

## topology-005 · dev · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 2：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:2
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_2.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-2:eth0 -> SYN-SW-2:port1; N3; synthetic
```

## topology-006 · dev · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 2：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:2
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_2.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-2:eth0 -> SYN-SW-2:port1; N3; synthetic
```

## topology-007 · heldout · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 3：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:3
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_3.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-3:eth0 -> SYN-SW-3:port1; N3; synthetic
```

## topology-008 · heldout · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 3：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:3
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_3.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-3:eth0 -> SYN-SW-3:port1; N3; synthetic
```

## topology-009 · heldout · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 4：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:4
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_4.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-4:eth0 -> SYN-SW-4:port1; N3; synthetic
```

## topology-010 · heldout · topology

- [x] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 4：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：synthetic-topology:4
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_4.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-4:eth0 -> SYN-SW-4:port1; N3; synthetic
```

## missing-001 · dev · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：当前 UPF 的 CPU 温度是多少？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:live-cpu
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-002 · dev · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：现在 UPF 的 CPU 负载是多少？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:live-cpu
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-003 · dev · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：UPF 9.9 版本如何配置 N3 接口？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:version-9
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-004 · dev · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：UPF 9.9 的 CLI 配置指令是什么？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:version-9
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-005 · heldout · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：没有日志文件，请诊断昨天的 UPF 中断。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:no-log
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-006 · heldout · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：未提供日志，能确认 UPF 昨日故障根因吗？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:no-log
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-007 · heldout · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：没有实际拓扑，请确定现场 N3 交换机端口。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:no-topology
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-008 · heldout · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：未提供现场连接表，UPF 连到哪台实际交换机？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:no-topology
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-009 · heldout · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：仅有脱敏日志，实际发生告警的是哪台真实设备？
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:no-identity
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-010 · heldout · missing

- [x] 问题及预期事实/相关证据已核对
- 问题：请把掩码地址还原成实际 UPF 的设备身份。
- 结论：通过
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28
- 修正意见：无
- 分组：missing:no-identity
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```


## 复核汇总

| 分类 | 通过 | 不通过 | 无法确认 | 合计 |
|------|------|--------|----------|------|
| command | 36 | 4 | 0 | 40 |
| knowledge | 20 | 0 | 0 | 20 |
| troubleshooting | 20 | 0 | 0 | 20 |
| log | 20 | 0 | 0 | 20 |
| topology | 10 | 0 | 0 | 10 |
| missing | 10 | 0 | 0 | 10 |
| **合计** | **116** | **4** | **0** | **120** |

### dev/heldout 分布
- dev: 通过 56 / 不通过 4 / 无法确认 0
- heldout: 通过 60 / 不通过 0 / 无法确认 0

### 不通过题目明细
- **command-009**：p[177]实际仅一行'set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>'(txbx为空)；证据块/预期
- **command-010**：同command-009证据组；p[177]仅有命令格式行，证据块多出的'相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4'在原文中无
- **command-011**：同command-009证据组；命令格式行本身(p[177])正确，但证据块把p[183]的示例冠以杜撰的'相关说明：'标签并入p[177]块，与原文不符
- **command-012**：同command-009证据组；预期第二行'相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4'无法在原文逐字找到('相关说明'全文无)

复核人：AI辅助复核（待人工签名）
日期：2026-09-28
