# P6 业务真值复核单 v3

120题助手候选、全部待人工确认。此版本补入UPF真实手册故障案例与网管/协议功能，替换初轮偏安装维护的40题，并替换4道已曝光来源的保留命令题；共44题替换、76题保留。
初轮模型对照属于旧草案的兼容、选择与预算实测，v3完整业务集尚未评测，保留题的历史输出不能当作新版整集成绩。
命令40题仍为10个命令族各4种问法，不是40种独立命令。两次核对关键语法与版本。
开发/保留各60，分组不得跨集；历史已曝光源不能移入新保留集。
日志仅有未知时区与脱敏身份；拓扑仅是合成CSV。原件矛盾、截图缺字段必须标注，不能补猜。
问题、相关块与事实有错误时写修正意见；结论、人名和日期必须真实填写。

## command-001 · dev · command

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘检查upf 业务网络地址配置 / 检查所有接口地址’中，show 命令的原文写法是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-5c4b984cb9fb9b794139, command-family:show
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-611060638cb88f44e6bbdfc9`
- 定位：word/document.xml/body/p[1055], word/document.xml/body/p[1056], word/document.xml/body/p[1057], word/document.xml/body/p[1058], word/document.xml/body/p[1059], word/document.xml/body/p[1060], word/document.xml/body/p[1061]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-b586b6d6c78e913d75bfa0b2`
- 定位：word/document.xml/body/p[1062]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e2c3df09d389081631789e9d`
- 定位：word/document.xml/body/p[1063]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘检查upf 业务网络地址配置 / 检查所有接口地址’中的命令 show config，保留占位符和参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-5c4b984cb9fb9b794139, command-family:show
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-611060638cb88f44e6bbdfc9`
- 定位：word/document.xml/body/p[1055], word/document.xml/body/p[1056], word/document.xml/body/p[1057], word/document.xml/body/p[1058], word/document.xml/body/p[1059], word/document.xml/body/p[1060], word/document.xml/body/p[1061]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-b586b6d6c78e913d75bfa0b2`
- 定位：word/document.xml/body/p[1062]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e2c3df09d389081631789e9d`
- 定位：word/document.xml/body/p[1063]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘检查upf 业务网络地址配置 / 检查所有接口地址’如何使用 show？只摘录原文并说明示例适用范围。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-5c4b984cb9fb9b794139, command-family:show
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-611060638cb88f44e6bbdfc9`
- 定位：word/document.xml/body/p[1055], word/document.xml/body/p[1056], word/document.xml/body/p[1057], word/document.xml/body/p[1058], word/document.xml/body/p[1059], word/document.xml/body/p[1060], word/document.xml/body/p[1061]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-b586b6d6c78e913d75bfa0b2`
- 定位：word/document.xml/body/p[1062]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e2c3df09d389081631789e9d`
- 定位：word/document.xml/body/p[1063]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 show config 在‘检查upf 业务网络地址配置 / 检查所有接口地址’中的原始语法，不把示例当现场参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-5c4b984cb9fb9b794139, command-family:show
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-611060638cb88f44e6bbdfc9`
- 定位：word/document.xml/body/p[1055], word/document.xml/body/p[1056], word/document.xml/body/p[1057], word/document.xml/body/p[1058], word/document.xml/body/p[1059], word/document.xml/body/p[1060], word/document.xml/body/p[1061]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-b586b6d6c78e913d75bfa0b2`
- 定位：word/document.xml/body/p[1062]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址
show config
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e2c3df09d389081631789e9d`
- 定位：word/document.xml/body/p[1063]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’中，upfmgr 命令的原文写法是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-4074dc47431e95e1d96d, command-family:upfmgr
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-c47de373b7bf531a3080853d`
- 定位：word/document.xml/body/p[1087], word/document.xml/body/p[1088], word/document.xml/body/p[1089], word/document.xml/body/p[1090], word/document.xml/body/p[1091]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
检查N3N6接口及IP配置
查看N3 N6 网口配置，需要访问upfd pod中的vpp CLI 命令行界面。
首先进入upfd pod中
直接使用脚本
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5f39f6e176cd5d50da043a23`
- 定位：word/document.xml/body/p[1092]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-a3845a8d6d582d25a6c91232`
- 定位：word/document.xml/body/p[1093], word/document.xml/body/p[1094], word/document.xml/body/p[1095]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
或使用kubectl命令进入pod，并在pod中执行vppctl命令
# kubectl exec -it -n ns1 upfd-1-594847d77d-7pblh -- './vppctl'
查看VPP接口地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7186a25131ec3f73b59889b5`
- 定位：word/document.xml/body/p[1096]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface addr
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-27ef72ccf4b8d59bfc1dffa3`
- 定位：word/document.xml/body/p[1097], word/document.xml/body/p[1098], word/document.xml/body/p[1099], word/document.xml/body/p[1100], word/document.xml/body/p[1101], word/document.xml/body/p[1102], word/document.xml/body/p[1103], word/document.xml/body/p[1104], word/document.xml/body/p[1105], word/document.xml/body/p[1106], word/document.xml/body/p[1107], word/document.xml/body/p[1108], word/document.xml/body/p[1110]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-8424f0e01f9e2107b966e55a`
- 定位：word/document.xml/body/p[1111]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 100.10.1.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-cf3d3bb155ff05c4e0809464`
- 定位：word/document.xml/body/p[1112]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 174.100.100.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-ee7cc9ff13c00222dee84783`
- 定位：word/document.xml/body/p[1113], word/document.xml/body/p[1114]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
如果能够ping通说明基本网络连通性正常。否则需要依次检查VPP配置，CNI配置，及交换机配置信息，核对vlan、IP及接口是否存在配置错误。
查看vpp接口信息
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-a8f5ff09d0cf29498ce8c9d0`
- 定位：word/document.xml/body/p[1115]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2b204cd7383c816b26ba3e86`
- 定位：word/document.xml/body/p[1116], word/document.xml/body/p[1118], word/document.xml/body/p[1119], word/document.xml/body/p[1120]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果：
说明：
输出结果显示vpp内有4个接口，对应4个物理网卡，其中两两做Bonding，网卡接口名称由物理网卡PCI地址编号进行命名。两个接口对应哪个物理网卡在config.yml配置文件中已经提前定义。
另外可以通过查看接口详细信息中的PCI地址来确认接口属于哪块物理网卡，执行以下vpp命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-4065867d9b809a1a9ef3d21b`
- 定位：word/document.xml/body/p[1121]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show hardware-interfaces port17/0/0
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1ba82874b94598161727769f`
- 定位：word/document.xml/body/p[1122], word/document.xml/body/p[1124], word/document.xml/body/p[1125], word/document.xml/body/p[1126], word/document.xml/body/p[1127], word/document.xml/body/p[1128], word/document.xml/body/p[1129]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’中的命令 upfmgr data，保留占位符和参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-4074dc47431e95e1d96d, command-family:upfmgr
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-c47de373b7bf531a3080853d`
- 定位：word/document.xml/body/p[1087], word/document.xml/body/p[1088], word/document.xml/body/p[1089], word/document.xml/body/p[1090], word/document.xml/body/p[1091]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
检查N3N6接口及IP配置
查看N3 N6 网口配置，需要访问upfd pod中的vpp CLI 命令行界面。
首先进入upfd pod中
直接使用脚本
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5f39f6e176cd5d50da043a23`
- 定位：word/document.xml/body/p[1092]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-a3845a8d6d582d25a6c91232`
- 定位：word/document.xml/body/p[1093], word/document.xml/body/p[1094], word/document.xml/body/p[1095]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
或使用kubectl命令进入pod，并在pod中执行vppctl命令
# kubectl exec -it -n ns1 upfd-1-594847d77d-7pblh -- './vppctl'
查看VPP接口地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7186a25131ec3f73b59889b5`
- 定位：word/document.xml/body/p[1096]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface addr
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-27ef72ccf4b8d59bfc1dffa3`
- 定位：word/document.xml/body/p[1097], word/document.xml/body/p[1098], word/document.xml/body/p[1099], word/document.xml/body/p[1100], word/document.xml/body/p[1101], word/document.xml/body/p[1102], word/document.xml/body/p[1103], word/document.xml/body/p[1104], word/document.xml/body/p[1105], word/document.xml/body/p[1106], word/document.xml/body/p[1107], word/document.xml/body/p[1108], word/document.xml/body/p[1110]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-8424f0e01f9e2107b966e55a`
- 定位：word/document.xml/body/p[1111]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 100.10.1.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-cf3d3bb155ff05c4e0809464`
- 定位：word/document.xml/body/p[1112]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 174.100.100.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-ee7cc9ff13c00222dee84783`
- 定位：word/document.xml/body/p[1113], word/document.xml/body/p[1114]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
如果能够ping通说明基本网络连通性正常。否则需要依次检查VPP配置，CNI配置，及交换机配置信息，核对vlan、IP及接口是否存在配置错误。
查看vpp接口信息
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-a8f5ff09d0cf29498ce8c9d0`
- 定位：word/document.xml/body/p[1115]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2b204cd7383c816b26ba3e86`
- 定位：word/document.xml/body/p[1116], word/document.xml/body/p[1118], word/document.xml/body/p[1119], word/document.xml/body/p[1120]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果：
说明：
输出结果显示vpp内有4个接口，对应4个物理网卡，其中两两做Bonding，网卡接口名称由物理网卡PCI地址编号进行命名。两个接口对应哪个物理网卡在config.yml配置文件中已经提前定义。
另外可以通过查看接口详细信息中的PCI地址来确认接口属于哪块物理网卡，执行以下vpp命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-4065867d9b809a1a9ef3d21b`
- 定位：word/document.xml/body/p[1121]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show hardware-interfaces port17/0/0
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1ba82874b94598161727769f`
- 定位：word/document.xml/body/p[1122], word/document.xml/body/p[1124], word/document.xml/body/p[1125], word/document.xml/body/p[1126], word/document.xml/body/p[1127], word/document.xml/body/p[1128], word/document.xml/body/p[1129]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’如何使用 upfmgr？只摘录原文并说明示例适用范围。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-4074dc47431e95e1d96d, command-family:upfmgr
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-c47de373b7bf531a3080853d`
- 定位：word/document.xml/body/p[1087], word/document.xml/body/p[1088], word/document.xml/body/p[1089], word/document.xml/body/p[1090], word/document.xml/body/p[1091]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
检查N3N6接口及IP配置
查看N3 N6 网口配置，需要访问upfd pod中的vpp CLI 命令行界面。
首先进入upfd pod中
直接使用脚本
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5f39f6e176cd5d50da043a23`
- 定位：word/document.xml/body/p[1092]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-a3845a8d6d582d25a6c91232`
- 定位：word/document.xml/body/p[1093], word/document.xml/body/p[1094], word/document.xml/body/p[1095]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
或使用kubectl命令进入pod，并在pod中执行vppctl命令
# kubectl exec -it -n ns1 upfd-1-594847d77d-7pblh -- './vppctl'
查看VPP接口地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7186a25131ec3f73b59889b5`
- 定位：word/document.xml/body/p[1096]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface addr
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-27ef72ccf4b8d59bfc1dffa3`
- 定位：word/document.xml/body/p[1097], word/document.xml/body/p[1098], word/document.xml/body/p[1099], word/document.xml/body/p[1100], word/document.xml/body/p[1101], word/document.xml/body/p[1102], word/document.xml/body/p[1103], word/document.xml/body/p[1104], word/document.xml/body/p[1105], word/document.xml/body/p[1106], word/document.xml/body/p[1107], word/document.xml/body/p[1108], word/document.xml/body/p[1110]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-8424f0e01f9e2107b966e55a`
- 定位：word/document.xml/body/p[1111]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 100.10.1.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-cf3d3bb155ff05c4e0809464`
- 定位：word/document.xml/body/p[1112]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 174.100.100.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-ee7cc9ff13c00222dee84783`
- 定位：word/document.xml/body/p[1113], word/document.xml/body/p[1114]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
如果能够ping通说明基本网络连通性正常。否则需要依次检查VPP配置，CNI配置，及交换机配置信息，核对vlan、IP及接口是否存在配置错误。
查看vpp接口信息
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-a8f5ff09d0cf29498ce8c9d0`
- 定位：word/document.xml/body/p[1115]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2b204cd7383c816b26ba3e86`
- 定位：word/document.xml/body/p[1116], word/document.xml/body/p[1118], word/document.xml/body/p[1119], word/document.xml/body/p[1120]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果：
说明：
输出结果显示vpp内有4个接口，对应4个物理网卡，其中两两做Bonding，网卡接口名称由物理网卡PCI地址编号进行命名。两个接口对应哪个物理网卡在config.yml配置文件中已经提前定义。
另外可以通过查看接口详细信息中的PCI地址来确认接口属于哪块物理网卡，执行以下vpp命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-4065867d9b809a1a9ef3d21b`
- 定位：word/document.xml/body/p[1121]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show hardware-interfaces port17/0/0
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1ba82874b94598161727769f`
- 定位：word/document.xml/body/p[1122], word/document.xml/body/p[1124], word/document.xml/body/p[1125], word/document.xml/body/p[1126], word/document.xml/body/p[1127], word/document.xml/body/p[1128], word/document.xml/body/p[1129]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 upfmgr data 在‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’中的原始语法，不把示例当现场参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-4074dc47431e95e1d96d, command-family:upfmgr
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-c47de373b7bf531a3080853d`
- 定位：word/document.xml/body/p[1087], word/document.xml/body/p[1088], word/document.xml/body/p[1089], word/document.xml/body/p[1090], word/document.xml/body/p[1091]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
检查N3N6接口及IP配置
查看N3 N6 网口配置，需要访问upfd pod中的vpp CLI 命令行界面。
首先进入upfd pod中
直接使用脚本
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5f39f6e176cd5d50da043a23`
- 定位：word/document.xml/body/p[1092]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
upfmgr data
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-a3845a8d6d582d25a6c91232`
- 定位：word/document.xml/body/p[1093], word/document.xml/body/p[1094], word/document.xml/body/p[1095]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
或使用kubectl命令进入pod，并在pod中执行vppctl命令
# kubectl exec -it -n ns1 upfd-1-594847d77d-7pblh -- './vppctl'
查看VPP接口地址
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7186a25131ec3f73b59889b5`
- 定位：word/document.xml/body/p[1096]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface addr
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-27ef72ccf4b8d59bfc1dffa3`
- 定位：word/document.xml/body/p[1097], word/document.xml/body/p[1098], word/document.xml/body/p[1099], word/document.xml/body/p[1100], word/document.xml/body/p[1101], word/document.xml/body/p[1102], word/document.xml/body/p[1103], word/document.xml/body/p[1104], word/document.xml/body/p[1105], word/document.xml/body/p[1106], word/document.xml/body/p[1107], word/document.xml/body/p[1108], word/document.xml/body/p[1110]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-8424f0e01f9e2107b966e55a`
- 定位：word/document.xml/body/p[1111]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 100.10.1.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-cf3d3bb155ff05c4e0809464`
- 定位：word/document.xml/body/p[1112]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# ping 174.100.100.1
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-ee7cc9ff13c00222dee84783`
- 定位：word/document.xml/body/p[1113], word/document.xml/body/p[1114]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
如果能够ping通说明基本网络连通性正常。否则需要依次检查VPP配置，CNI配置，及交换机配置信息，核对vlan、IP及接口是否存在配置错误。
查看vpp接口信息
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-a8f5ff09d0cf29498ce8c9d0`
- 定位：word/document.xml/body/p[1115]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show interface
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2b204cd7383c816b26ba3e86`
- 定位：word/document.xml/body/p[1116], word/document.xml/body/p[1118], word/document.xml/body/p[1119], word/document.xml/body/p[1120]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
示例输出结果：
说明：
输出结果显示vpp内有4个接口，对应4个物理网卡，其中两两做Bonding，网卡接口名称由物理网卡PCI地址编号进行命名。两个接口对应哪个物理网卡在config.yml配置文件中已经提前定义。
另外可以通过查看接口详细信息中的PCI地址来确认接口属于哪块物理网卡，执行以下vpp命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-4065867d9b809a1a9ef3d21b`
- 定位：word/document.xml/body/p[1121]
```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
UPF# show hardware-interfaces port17/0/0
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1ba82874b94598161727769f`
- 定位：word/document.xml/body/p[1122], word/document.xml/body/p[1124], word/document.xml/body/p[1125], word/document.xml/body/p[1126], word/document.xml/body/p[1127], word/document.xml/body/p[1128], word/document.xml/body/p[1129]
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
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-93a4864c8a3b2c42c793, command-family:set-upf-prt-sw
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-05b46622548cea41921ec8c4`
- 定位：word/document.xml/body/p[168], word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172], word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[176]
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
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-ed162186f81b734c927091f0`
- 定位：word/document.xml/body/p[177]
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-21b601c9353349f7eb3ab15c`
- 定位：word/document.xml/body/p[178], word/document.xml/body/p[179], word/document.xml/body/p[180], word/document.xml/body/p[182]
```text
CLI配置命令 / UPF系统能力 / 功能配置
说明：
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；
gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。
举例：
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-5508ad2ffaa25a9c28d1634f`
- 定位：word/document.xml/body/p[183]
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-4810f364c95856d4a4b9902f`
- 定位：word/document.xml/body/p[184]
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> show config
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-e2ca5f2a07d7228d2bb32d91`
- 定位：word/document.xml/body/p[185], word/document.xml/body/p[186], word/document.xml/body/p[187], word/document.xml/body/p[188], word/document.xml/body/p[189], word/document.xml/body/p[190]
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
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-93a4864c8a3b2c42c793, command-family:set-upf-prt-sw
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-05b46622548cea41921ec8c4`
- 定位：word/document.xml/body/p[168], word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172], word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[176]
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
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-ed162186f81b734c927091f0`
- 定位：word/document.xml/body/p[177]
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-21b601c9353349f7eb3ab15c`
- 定位：word/document.xml/body/p[178], word/document.xml/body/p[179], word/document.xml/body/p[180], word/document.xml/body/p[182]
```text
CLI配置命令 / UPF系统能力 / 功能配置
说明：
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；
gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。
举例：
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-5508ad2ffaa25a9c28d1634f`
- 定位：word/document.xml/body/p[183]
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-4810f364c95856d4a4b9902f`
- 定位：word/document.xml/body/p[184]
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> show config
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-e2ca5f2a07d7228d2bb32d91`
- 定位：word/document.xml/body/p[185], word/document.xml/body/p[186], word/document.xml/body/p[187], word/document.xml/body/p[188], word/document.xml/body/p[189], word/document.xml/body/p[190]
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
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-93a4864c8a3b2c42c793, command-family:set-upf-prt-sw
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-05b46622548cea41921ec8c4`
- 定位：word/document.xml/body/p[168], word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172], word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[176]
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
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-ed162186f81b734c927091f0`
- 定位：word/document.xml/body/p[177]
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-21b601c9353349f7eb3ab15c`
- 定位：word/document.xml/body/p[178], word/document.xml/body/p[179], word/document.xml/body/p[180], word/document.xml/body/p[182]
```text
CLI配置命令 / UPF系统能力 / 功能配置
说明：
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；
gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。
举例：
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-5508ad2ffaa25a9c28d1634f`
- 定位：word/document.xml/body/p[183]
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-4810f364c95856d4a4b9902f`
- 定位：word/document.xml/body/p[184]
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> show config
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-e2ca5f2a07d7228d2bb32d91`
- 定位：word/document.xml/body/p[185], word/document.xml/body/p[186], word/document.xml/body/p[187], word/document.xml/body/p[188], word/document.xml/body/p[189], word/document.xml/body/p[190]
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
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-93a4864c8a3b2c42c793, command-family:set-upf-prt-sw
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-05b46622548cea41921ec8c4`
- 定位：word/document.xml/body/p[168], word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172], word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[176]
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
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-ed162186f81b734c927091f0`
- 定位：word/document.xml/body/p[177]
```text
CLI配置命令 / UPF系统能力 / 功能配置
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-21b601c9353349f7eb3ab15c`
- 定位：word/document.xml/body/p[178], word/document.xml/body/p[179], word/document.xml/body/p[180], word/document.xml/body/p[182]
```text
CLI配置命令 / UPF系统能力 / 功能配置
说明：
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；
gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。
举例：
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-5508ad2ffaa25a9c28d1634f`
- 定位：word/document.xml/body/p[183]
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> set-upf-prt-sw n4-prt-sw 4
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-4810f364c95856d4a4b9902f`
- 定位：word/document.xml/body/p[184]
```text
CLI配置命令 / UPF系统能力 / 功能配置
UPFD> show config
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-e2ca5f2a07d7228d2bb32d91`
- 定位：word/document.xml/body/p[185], word/document.xml/body/p[186], word/document.xml/body/p[187], word/document.xml/body/p[188], word/document.xml/body/p[189], word/document.xml/body/p[190]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘配置UPF物理机 / Coredump开关打开’中，echo 命令的原文写法是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-279f5f812451d0bbf03e, command-family:echo
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-041c2988010a54673b562f26`
- 定位：word/document.xml/body/p[378], word/document.xml/body/p[379]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
Coredump开关打开
复制并输入如下命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-da1f7676d2f30661bb5e00a8`
- 定位：word/document.xml/body/p[380]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
mkdir -p /opt/local/tmp/core
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-da087bcb96a5e8d605b2107f`
- 定位：word/document.xml/body/p[382]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/security/limits.d/coredump.conf<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-97617917b877529323000733`
- 定位：word/document.xml/body/p[383], word/document.xml/body/p[384], word/document.xml/body/p[385]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
* soft core unlimited
* hard core unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-01998c8695e66a6318101bb8`
- 定位：word/document.xml/body/p[387]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-b7e7f004b9f94894131191dc`
- 定位：word/document.xml/body/p[388]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-41d54d63a03ea2658cf62b77`
- 定位：word/document.xml/body/p[390]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/profile.d/coredump.sh<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-08f63c658d0f9d9de2335551`
- 定位：word/document.xml/body/p[391], word/document.xml/body/p[392], word/document.xml/body/p[393]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
#!/bin/sh
ulimit -S -c unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3c63be79228c38487b673dea`
- 定位：word/document.xml/body/p[395]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
source /etc/profile
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3ecddf27a8093a17064a1a8a`
- 定位：word/document.xml/body/p[396], word/document.xml/body/p[397], word/document.xml/body/p[398]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘配置UPF物理机 / Coredump开关打开’中的命令 echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern，保留占位符和参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-279f5f812451d0bbf03e, command-family:echo
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-041c2988010a54673b562f26`
- 定位：word/document.xml/body/p[378], word/document.xml/body/p[379]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
Coredump开关打开
复制并输入如下命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-da1f7676d2f30661bb5e00a8`
- 定位：word/document.xml/body/p[380]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
mkdir -p /opt/local/tmp/core
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-da087bcb96a5e8d605b2107f`
- 定位：word/document.xml/body/p[382]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/security/limits.d/coredump.conf<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-97617917b877529323000733`
- 定位：word/document.xml/body/p[383], word/document.xml/body/p[384], word/document.xml/body/p[385]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
* soft core unlimited
* hard core unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-01998c8695e66a6318101bb8`
- 定位：word/document.xml/body/p[387]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-b7e7f004b9f94894131191dc`
- 定位：word/document.xml/body/p[388]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-41d54d63a03ea2658cf62b77`
- 定位：word/document.xml/body/p[390]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/profile.d/coredump.sh<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-08f63c658d0f9d9de2335551`
- 定位：word/document.xml/body/p[391], word/document.xml/body/p[392], word/document.xml/body/p[393]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
#!/bin/sh
ulimit -S -c unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3c63be79228c38487b673dea`
- 定位：word/document.xml/body/p[395]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
source /etc/profile
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3ecddf27a8093a17064a1a8a`
- 定位：word/document.xml/body/p[396], word/document.xml/body/p[397], word/document.xml/body/p[398]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘配置UPF物理机 / Coredump开关打开’如何使用 echo？只摘录原文并说明示例适用范围。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-279f5f812451d0bbf03e, command-family:echo
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-041c2988010a54673b562f26`
- 定位：word/document.xml/body/p[378], word/document.xml/body/p[379]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
Coredump开关打开
复制并输入如下命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-da1f7676d2f30661bb5e00a8`
- 定位：word/document.xml/body/p[380]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
mkdir -p /opt/local/tmp/core
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-da087bcb96a5e8d605b2107f`
- 定位：word/document.xml/body/p[382]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/security/limits.d/coredump.conf<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-97617917b877529323000733`
- 定位：word/document.xml/body/p[383], word/document.xml/body/p[384], word/document.xml/body/p[385]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
* soft core unlimited
* hard core unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-01998c8695e66a6318101bb8`
- 定位：word/document.xml/body/p[387]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-b7e7f004b9f94894131191dc`
- 定位：word/document.xml/body/p[388]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-41d54d63a03ea2658cf62b77`
- 定位：word/document.xml/body/p[390]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/profile.d/coredump.sh<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-08f63c658d0f9d9de2335551`
- 定位：word/document.xml/body/p[391], word/document.xml/body/p[392], word/document.xml/body/p[393]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
#!/bin/sh
ulimit -S -c unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3c63be79228c38487b673dea`
- 定位：word/document.xml/body/p[395]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
source /etc/profile
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3ecddf27a8093a17064a1a8a`
- 定位：word/document.xml/body/p[396], word/document.xml/body/p[397], word/document.xml/body/p[398]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern 在‘配置UPF物理机 / Coredump开关打开’中的原始语法，不把示例当现场参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-279f5f812451d0bbf03e, command-family:echo
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-041c2988010a54673b562f26`
- 定位：word/document.xml/body/p[378], word/document.xml/body/p[379]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
Coredump开关打开
复制并输入如下命令：
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-da1f7676d2f30661bb5e00a8`
- 定位：word/document.xml/body/p[380]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
mkdir -p /opt/local/tmp/core
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-da087bcb96a5e8d605b2107f`
- 定位：word/document.xml/body/p[382]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/security/limits.d/coredump.conf<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-97617917b877529323000733`
- 定位：word/document.xml/body/p[383], word/document.xml/body/p[384], word/document.xml/body/p[385]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
* soft core unlimited
* hard core unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-01998c8695e66a6318101bb8`
- 定位：word/document.xml/body/p[387]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-b7e7f004b9f94894131191dc`
- 定位：word/document.xml/body/p[388]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-41d54d63a03ea2658cf62b77`
- 定位：word/document.xml/body/p[390]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
cat >/etc/profile.d/coredump.sh<<EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-08f63c658d0f9d9de2335551`
- 定位：word/document.xml/body/p[391], word/document.xml/body/p[392], word/document.xml/body/p[393]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
#!/bin/sh
ulimit -S -c unlimited
EOF
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3c63be79228c38487b673dea`
- 定位：word/document.xml/body/p[395]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
source /etc/profile
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3ecddf27a8093a17064a1a8a`
- 定位：word/document.xml/body/p[396], word/document.xml/body/p[397], word/document.xml/body/p[398]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘逻辑口报文信息统计 / 统计N4口报文信息’中，tcpdump 命令的原文写法是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-b046170188e546647016, command-family:tcpdump
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-cd469b95520a9da4928f8fa7`
- 定位：word/document.xml/body/p[292], word/document.xml/body/p[293], word/document.xml/body/p[294], word/document.xml/body/p[295]
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
统计N4口报文信息
登录UPF物理机，打开终端
查看N4IP在哪个端口
选择该端口，运行如下命令抓包
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-7fdde4d9a3c3a42036bffd3d`
- 定位：word/document.xml/body/p[296]
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-67083f7c25d8e6bb5ac216ee`
- 定位：word/document.xml/body/p[297]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘逻辑口报文信息统计 / 统计N4口报文信息’中的命令 tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap，保留占位符和参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-b046170188e546647016, command-family:tcpdump
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-cd469b95520a9da4928f8fa7`
- 定位：word/document.xml/body/p[292], word/document.xml/body/p[293], word/document.xml/body/p[294], word/document.xml/body/p[295]
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
统计N4口报文信息
登录UPF物理机，打开终端
查看N4IP在哪个端口
选择该端口，运行如下命令抓包
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-7fdde4d9a3c3a42036bffd3d`
- 定位：word/document.xml/body/p[296]
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-67083f7c25d8e6bb5ac216ee`
- 定位：word/document.xml/body/p[297]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘逻辑口报文信息统计 / 统计N4口报文信息’如何使用 tcpdump？只摘录原文并说明示例适用范围。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-b046170188e546647016, command-family:tcpdump
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-cd469b95520a9da4928f8fa7`
- 定位：word/document.xml/body/p[292], word/document.xml/body/p[293], word/document.xml/body/p[294], word/document.xml/body/p[295]
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
统计N4口报文信息
登录UPF物理机，打开终端
查看N4IP在哪个端口
选择该端口，运行如下命令抓包
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-7fdde4d9a3c3a42036bffd3d`
- 定位：word/document.xml/body/p[296]
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-67083f7c25d8e6bb5ac216ee`
- 定位：word/document.xml/body/p[297]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap 在‘逻辑口报文信息统计 / 统计N4口报文信息’中的原始语法，不把示例当现场参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-b046170188e546647016, command-family:tcpdump
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-cd469b95520a9da4928f8fa7`
- 定位：word/document.xml/body/p[292], word/document.xml/body/p[293], word/document.xml/body/p[294], word/document.xml/body/p[295]
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
统计N4口报文信息
登录UPF物理机，打开终端
查看N4IP在哪个端口
选择该端口，运行如下命令抓包
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-7fdde4d9a3c3a42036bffd3d`
- 定位：word/document.xml/body/p[296]
```text
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-67083f7c25d8e6bb5ac216ee`
- 定位：word/document.xml/body/p[297]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘配置UPF物理机 / 配置root SSH登陆权限’中，systemctl 命令的原文写法是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-6622b1bf5a5e87007b26, command-family:systemctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-71311040510f8df9aa5efb17`
- 定位：word/document.xml/body/p[355], word/document.xml/body/p[356], word/document.xml/body/p[357], word/document.xml/body/p[358], word/document.xml/body/p[359], word/document.xml/body/p[360], word/document.xml/body/p[361], word/document.xml/body/p[362], word/document.xml/body/p[363], word/document.xml/body/p[364], word/document.xml/body/p[365], word/document.xml/body/p[366], word/document.xml/body/p[367], word/document.xml/body/p[368]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e3529db276d608065d796152`
- 定位：word/document.xml/body/p[369]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1f407885a8268eac87f3e90b`
- 定位：word/document.xml/body/p[370], word/document.xml/body/p[371], word/document.xml/body/p[372], word/document.xml/body/p[373], word/document.xml/body/p[374], word/document.xml/body/p[375], word/document.xml/body/p[376]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘配置UPF物理机 / 配置root SSH登陆权限’中的命令 systemctl restart sshd，保留占位符和参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-6622b1bf5a5e87007b26, command-family:systemctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-71311040510f8df9aa5efb17`
- 定位：word/document.xml/body/p[355], word/document.xml/body/p[356], word/document.xml/body/p[357], word/document.xml/body/p[358], word/document.xml/body/p[359], word/document.xml/body/p[360], word/document.xml/body/p[361], word/document.xml/body/p[362], word/document.xml/body/p[363], word/document.xml/body/p[364], word/document.xml/body/p[365], word/document.xml/body/p[366], word/document.xml/body/p[367], word/document.xml/body/p[368]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e3529db276d608065d796152`
- 定位：word/document.xml/body/p[369]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1f407885a8268eac87f3e90b`
- 定位：word/document.xml/body/p[370], word/document.xml/body/p[371], word/document.xml/body/p[372], word/document.xml/body/p[373], word/document.xml/body/p[374], word/document.xml/body/p[375], word/document.xml/body/p[376]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘配置UPF物理机 / 配置root SSH登陆权限’如何使用 systemctl？只摘录原文并说明示例适用范围。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-6622b1bf5a5e87007b26, command-family:systemctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-71311040510f8df9aa5efb17`
- 定位：word/document.xml/body/p[355], word/document.xml/body/p[356], word/document.xml/body/p[357], word/document.xml/body/p[358], word/document.xml/body/p[359], word/document.xml/body/p[360], word/document.xml/body/p[361], word/document.xml/body/p[362], word/document.xml/body/p[363], word/document.xml/body/p[364], word/document.xml/body/p[365], word/document.xml/body/p[366], word/document.xml/body/p[367], word/document.xml/body/p[368]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e3529db276d608065d796152`
- 定位：word/document.xml/body/p[369]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1f407885a8268eac87f3e90b`
- 定位：word/document.xml/body/p[370], word/document.xml/body/p[371], word/document.xml/body/p[372], word/document.xml/body/p[373], word/document.xml/body/p[374], word/document.xml/body/p[375], word/document.xml/body/p[376]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 systemctl restart sshd 在‘配置UPF物理机 / 配置root SSH登陆权限’中的原始语法，不把示例当现场参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-6622b1bf5a5e87007b26, command-family:systemctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-71311040510f8df9aa5efb17`
- 定位：word/document.xml/body/p[355], word/document.xml/body/p[356], word/document.xml/body/p[357], word/document.xml/body/p[358], word/document.xml/body/p[359], word/document.xml/body/p[360], word/document.xml/body/p[361], word/document.xml/body/p[362], word/document.xml/body/p[363], word/document.xml/body/p[364], word/document.xml/body/p[365], word/document.xml/body/p[366], word/document.xml/body/p[367], word/document.xml/body/p[368]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e3529db276d608065d796152`
- 定位：word/document.xml/body/p[369]
```text
物理机安装操作系统并配置 / 配置UPF物理机 / 配置root SSH登陆权限
systemctl restart sshd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1f407885a8268eac87f3e90b`
- 定位：word/document.xml/body/p[370], word/document.xml/body/p[371], word/document.xml/body/p[372], word/document.xml/body/p[373], word/document.xml/body/p[374], word/document.xml/body/p[375], word/document.xml/body/p[376]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘插件维护管理 / Flannel’中，helm 命令的原文写法是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-066cc1bc125c770979b0, command-family:helm
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-ce1bae1eaeca4e52e1de2b7c`
- 定位：word/document.xml/body/p[1908], word/document.xml/body/p[1909], word/document.xml/body/p[1910], word/document.xml/body/p[1911], word/document.xml/body/p[1912], word/document.xml/body/p[1913], word/document.xml/body/p[1914], word/document.xml/body/p[1915], word/document.xml/body/p[1916], word/document.xml/body/p[1918], word/document.xml/body/p[1919], word/document.xml/body/p[1921], word/document.xml/body/p[1922], word/document.xml/body/p[1923], word/document.xml/body/p[1924], word/document.xml/body/p[1925], word/document.xml/body/p[1927], word/document.xml/body/p[1928], word/document.xml/body/p[1929], word/document.xml/body/p[1930], word/document.xml/body/p[1932], word/document.xml/body/p[1933]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2fc4428866c69bb6de423877`
- 定位：word/document.xml/body/p[1934]
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-05a7a290e4e820cd81436843`
- 定位：word/document.xml/body/p[1935], word/document.xml/body/p[1936]
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
b.使用sealos命令卸载，仅部分镜像支持该方式
sealos run docker.io/labring/flannel:v0.21.4 -e uninstall=true
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```

## command-026 · heldout · command

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘插件维护管理 / Flannel’中的命令 helm -n kube-flannel uninstall flannel，保留参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-066cc1bc125c770979b0, command-family:helm
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-ce1bae1eaeca4e52e1de2b7c`
- 定位：word/document.xml/body/p[1908], word/document.xml/body/p[1909], word/document.xml/body/p[1910], word/document.xml/body/p[1911], word/document.xml/body/p[1912], word/document.xml/body/p[1913], word/document.xml/body/p[1914], word/document.xml/body/p[1915], word/document.xml/body/p[1916], word/document.xml/body/p[1918], word/document.xml/body/p[1919], word/document.xml/body/p[1921], word/document.xml/body/p[1922], word/document.xml/body/p[1923], word/document.xml/body/p[1924], word/document.xml/body/p[1925], word/document.xml/body/p[1927], word/document.xml/body/p[1928], word/document.xml/body/p[1929], word/document.xml/body/p[1930], word/document.xml/body/p[1932], word/document.xml/body/p[1933]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2fc4428866c69bb6de423877`
- 定位：word/document.xml/body/p[1934]
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-05a7a290e4e820cd81436843`
- 定位：word/document.xml/body/p[1935], word/document.xml/body/p[1936]
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
b.使用sealos命令卸载，仅部分镜像支持该方式
sealos run docker.io/labring/flannel:v0.21.4 -e uninstall=true
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```

## command-027 · heldout · command

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘插件维护管理 / Flannel’如何使用 helm？摘录原文并说明命名空间的示例适用范围。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-066cc1bc125c770979b0, command-family:helm
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-ce1bae1eaeca4e52e1de2b7c`
- 定位：word/document.xml/body/p[1908], word/document.xml/body/p[1909], word/document.xml/body/p[1910], word/document.xml/body/p[1911], word/document.xml/body/p[1912], word/document.xml/body/p[1913], word/document.xml/body/p[1914], word/document.xml/body/p[1915], word/document.xml/body/p[1916], word/document.xml/body/p[1918], word/document.xml/body/p[1919], word/document.xml/body/p[1921], word/document.xml/body/p[1922], word/document.xml/body/p[1923], word/document.xml/body/p[1924], word/document.xml/body/p[1925], word/document.xml/body/p[1927], word/document.xml/body/p[1928], word/document.xml/body/p[1929], word/document.xml/body/p[1930], word/document.xml/body/p[1932], word/document.xml/body/p[1933]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2fc4428866c69bb6de423877`
- 定位：word/document.xml/body/p[1934]
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-05a7a290e4e820cd81436843`
- 定位：word/document.xml/body/p[1935], word/document.xml/body/p[1936]
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
b.使用sealos命令卸载，仅部分镜像支持该方式
sealos run docker.io/labring/flannel:v0.21.4 -e uninstall=true
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```

## command-028 · heldout · command

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 helm -n kube-flannel uninstall flannel 在‘插件维护管理 / Flannel’中的原始语法。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-066cc1bc125c770979b0, command-family:helm
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-ce1bae1eaeca4e52e1de2b7c`
- 定位：word/document.xml/body/p[1908], word/document.xml/body/p[1909], word/document.xml/body/p[1910], word/document.xml/body/p[1911], word/document.xml/body/p[1912], word/document.xml/body/p[1913], word/document.xml/body/p[1914], word/document.xml/body/p[1915], word/document.xml/body/p[1916], word/document.xml/body/p[1918], word/document.xml/body/p[1919], word/document.xml/body/p[1921], word/document.xml/body/p[1922], word/document.xml/body/p[1923], word/document.xml/body/p[1924], word/document.xml/body/p[1925], word/document.xml/body/p[1927], word/document.xml/body/p[1928], word/document.xml/body/p[1929], word/document.xml/body/p[1930], word/document.xml/body/p[1932], word/document.xml/body/p[1933]
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
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2fc4428866c69bb6de423877`
- 定位：word/document.xml/body/p[1934]
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-05a7a290e4e820cd81436843`
- 定位：word/document.xml/body/p[1935], word/document.xml/body/p[1936]
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
b.使用sealos命令卸载，仅部分镜像支持该方式
sealos run docker.io/labring/flannel:v0.21.4 -e uninstall=true
```
- 预期原文/缺口：
```text
K8S集群软件故障排查 / 插件维护管理 / Flannel
helm -n kube-flannel uninstall flannel
```

## command-029 · heldout · command

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘UPF基本故障排查 / 查看UPF软件包’中，ls 命令的原文写法是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-726b781a8d5f223c8f86, command-family:ls
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-44afc482e08f7b8768c9f4c3`
- 定位：word/document.xml/body/p[2325], word/document.xml/body/p[2326], word/document.xml/body/p[2327]
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
查看UPF软件包
查看解压的软件包
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-093401cdba160a0162a8e964`
- 定位：word/document.xml/body/p[2328]
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3d222d542889d1a7e81b0c71`
- 定位：word/document.xml/body/p[2329]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘UPF基本故障排查 / 查看UPF软件包’中的命令 ls temp/，保留占位符和参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-726b781a8d5f223c8f86, command-family:ls
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-44afc482e08f7b8768c9f4c3`
- 定位：word/document.xml/body/p[2325], word/document.xml/body/p[2326], word/document.xml/body/p[2327]
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
查看UPF软件包
查看解压的软件包
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-093401cdba160a0162a8e964`
- 定位：word/document.xml/body/p[2328]
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3d222d542889d1a7e81b0c71`
- 定位：word/document.xml/body/p[2329]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘UPF基本故障排查 / 查看UPF软件包’如何使用 ls？只摘录原文并说明示例适用范围。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-726b781a8d5f223c8f86, command-family:ls
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-44afc482e08f7b8768c9f4c3`
- 定位：word/document.xml/body/p[2325], word/document.xml/body/p[2326], word/document.xml/body/p[2327]
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
查看UPF软件包
查看解压的软件包
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-093401cdba160a0162a8e964`
- 定位：word/document.xml/body/p[2328]
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3d222d542889d1a7e81b0c71`
- 定位：word/document.xml/body/p[2329]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 ls temp/ 在‘UPF基本故障排查 / 查看UPF软件包’中的原始语法，不把示例当现场参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-726b781a8d5f223c8f86, command-family:ls
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-44afc482e08f7b8768c9f4c3`
- 定位：word/document.xml/body/p[2325], word/document.xml/body/p[2326], word/document.xml/body/p[2327]
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
查看UPF软件包
查看解压的软件包
# cd /home/upf_setup_CU5GC_UPF_5.0.210/integration/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-093401cdba160a0162a8e964`
- 定位：word/document.xml/body/p[2328]
```text
部署FAQ / UPF基本故障排查 / 查看UPF软件包
ls temp/
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-3d222d542889d1a7e81b0c71`
- 定位：word/document.xml/body/p[2329]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘UPF基本故障排查 / SOC 服务器nic问题’中，chmod 命令的原文写法是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-b059f306885fbaefdd56, command-family:chmod
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5ec26d2bd7c6cd308d4ae6a7`
- 定位：word/document.xml/body/p[2341], word/document.xml/body/p[2342], word/document.xml/body/p[2343], word/document.xml/body/p[2344], word/document.xml/body/p[2345]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
SOC 服务器nic问题
SOC服务器是8 port，现在只用4个，因为有一些limitation。修改方法如下：
下载epct64e二进制文件
 HYPERLINK "https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html" https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html
安装二进制文件到/usr/local/bin目录下
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2811577ed855f89547fec1d4`
- 定位：word/document.xml/body/p[2346]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
cp epct64e /usr/local/bin
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1d0e14afadc3125ff15e6d99`
- 定位：word/document.xml/body/p[2347]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-c8deaa189d6c9bfc9f3a227e`
- 定位：word/document.xml/body/p[2348], word/document.xml/body/p[2349]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘UPF基本故障排查 / SOC 服务器nic问题’中的命令 chmod +x /usr/local/bin/epct64e，保留占位符和参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-b059f306885fbaefdd56, command-family:chmod
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5ec26d2bd7c6cd308d4ae6a7`
- 定位：word/document.xml/body/p[2341], word/document.xml/body/p[2342], word/document.xml/body/p[2343], word/document.xml/body/p[2344], word/document.xml/body/p[2345]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
SOC 服务器nic问题
SOC服务器是8 port，现在只用4个，因为有一些limitation。修改方法如下：
下载epct64e二进制文件
 HYPERLINK "https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html" https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html
安装二进制文件到/usr/local/bin目录下
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2811577ed855f89547fec1d4`
- 定位：word/document.xml/body/p[2346]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
cp epct64e /usr/local/bin
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1d0e14afadc3125ff15e6d99`
- 定位：word/document.xml/body/p[2347]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-c8deaa189d6c9bfc9f3a227e`
- 定位：word/document.xml/body/p[2348], word/document.xml/body/p[2349]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘UPF基本故障排查 / SOC 服务器nic问题’如何使用 chmod？只摘录原文并说明示例适用范围。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-b059f306885fbaefdd56, command-family:chmod
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5ec26d2bd7c6cd308d4ae6a7`
- 定位：word/document.xml/body/p[2341], word/document.xml/body/p[2342], word/document.xml/body/p[2343], word/document.xml/body/p[2344], word/document.xml/body/p[2345]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
SOC 服务器nic问题
SOC服务器是8 port，现在只用4个，因为有一些limitation。修改方法如下：
下载epct64e二进制文件
 HYPERLINK "https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html" https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html
安装二进制文件到/usr/local/bin目录下
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2811577ed855f89547fec1d4`
- 定位：word/document.xml/body/p[2346]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
cp epct64e /usr/local/bin
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1d0e14afadc3125ff15e6d99`
- 定位：word/document.xml/body/p[2347]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-c8deaa189d6c9bfc9f3a227e`
- 定位：word/document.xml/body/p[2348], word/document.xml/body/p[2349]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 chmod +x /usr/local/bin/epct64e 在‘UPF基本故障排查 / SOC 服务器nic问题’中的原始语法，不把示例当现场参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-b059f306885fbaefdd56, command-family:chmod
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5ec26d2bd7c6cd308d4ae6a7`
- 定位：word/document.xml/body/p[2341], word/document.xml/body/p[2342], word/document.xml/body/p[2343], word/document.xml/body/p[2344], word/document.xml/body/p[2345]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
SOC 服务器nic问题
SOC服务器是8 port，现在只用4个，因为有一些limitation。修改方法如下：
下载epct64e二进制文件
 HYPERLINK "https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html" https://www.intel.com/content/www/us/en/download/19435/ethernet-port-configuration-tool-all-supported-oss.html
安装二进制文件到/usr/local/bin目录下
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-2811577ed855f89547fec1d4`
- 定位：word/document.xml/body/p[2346]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
cp epct64e /usr/local/bin
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-1d0e14afadc3125ff15e6d99`
- 定位：word/document.xml/body/p[2347]
```text
部署FAQ / UPF基本故障排查 / SOC 服务器nic问题
chmod +x /usr/local/bin/epct64e
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-c8deaa189d6c9bfc9f3a227e`
- 定位：word/document.xml/body/p[2348], word/document.xml/body/p[2349]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：在‘基本故障排查 / 集群安装问题’中，journalctl 命令的原文写法是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-8baf65985aebaf898945, command-family:journalctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-8b7190a7813bebeffe210cc7`
- 定位：word/document.xml/body/p[1788], word/document.xml/body/p[1789], word/document.xml/body/p[1790]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
集群安装问题
集群安装失败时，集群安装过程中输出的日志信息有限，一般需要进一步检查kubernetes系统进程例如kubelet、containerd状态及日志。
1.	查看kubelet运行状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7d6750acd76fa1ca0043ec44`
- 定位：word/document.xml/body/p[1791]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-04f75f76e3e997b3afb95ab4`
- 定位：word/document.xml/body/p[1792]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
2.	查看containerd容器运行时状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-cabd3152ee269df6489ed07b`
- 定位：word/document.xml/body/p[1793]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e7773e4bc9c9794eef44177c`
- 定位：word/document.xml/body/p[1794]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
3.	查看kubelet详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-40e89a682b78c5baf67ab343`
- 定位：word/document.xml/body/p[1795]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7eb6ba2c984e4c3c2253d153`
- 定位：word/document.xml/body/p[1796]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
4.	查看containerd详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5bf91a33efe9ff9fa23173e1`
- 定位：word/document.xml/body/p[1797]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-002d97a55d8b83668dc3dfa6`
- 定位：word/document.xml/body/p[1798], word/document.xml/body/p[1799], word/document.xml/body/p[1800]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用‘基本故障排查 / 集群安装问题’中的命令 journalctl -xeu kubelet，保留占位符和参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-8baf65985aebaf898945, command-family:journalctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-8b7190a7813bebeffe210cc7`
- 定位：word/document.xml/body/p[1788], word/document.xml/body/p[1789], word/document.xml/body/p[1790]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
集群安装问题
集群安装失败时，集群安装过程中输出的日志信息有限，一般需要进一步检查kubernetes系统进程例如kubelet、containerd状态及日志。
1.	查看kubelet运行状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7d6750acd76fa1ca0043ec44`
- 定位：word/document.xml/body/p[1791]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-04f75f76e3e997b3afb95ab4`
- 定位：word/document.xml/body/p[1792]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
2.	查看containerd容器运行时状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-cabd3152ee269df6489ed07b`
- 定位：word/document.xml/body/p[1793]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e7773e4bc9c9794eef44177c`
- 定位：word/document.xml/body/p[1794]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
3.	查看kubelet详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-40e89a682b78c5baf67ab343`
- 定位：word/document.xml/body/p[1795]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7eb6ba2c984e4c3c2253d153`
- 定位：word/document.xml/body/p[1796]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
4.	查看containerd详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5bf91a33efe9ff9fa23173e1`
- 定位：word/document.xml/body/p[1797]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-002d97a55d8b83668dc3dfa6`
- 定位：word/document.xml/body/p[1798], word/document.xml/body/p[1799], word/document.xml/body/p[1800]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：手册‘基本故障排查 / 集群安装问题’如何使用 journalctl？只摘录原文并说明示例适用范围。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-8baf65985aebaf898945, command-family:journalctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-8b7190a7813bebeffe210cc7`
- 定位：word/document.xml/body/p[1788], word/document.xml/body/p[1789], word/document.xml/body/p[1790]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
集群安装问题
集群安装失败时，集群安装过程中输出的日志信息有限，一般需要进一步检查kubernetes系统进程例如kubelet、containerd状态及日志。
1.	查看kubelet运行状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7d6750acd76fa1ca0043ec44`
- 定位：word/document.xml/body/p[1791]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-04f75f76e3e997b3afb95ab4`
- 定位：word/document.xml/body/p[1792]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
2.	查看containerd容器运行时状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-cabd3152ee269df6489ed07b`
- 定位：word/document.xml/body/p[1793]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e7773e4bc9c9794eef44177c`
- 定位：word/document.xml/body/p[1794]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
3.	查看kubelet详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-40e89a682b78c5baf67ab343`
- 定位：word/document.xml/body/p[1795]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7eb6ba2c984e4c3c2253d153`
- 定位：word/document.xml/body/p[1796]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
4.	查看containerd详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5bf91a33efe9ff9fa23173e1`
- 定位：word/document.xml/body/p[1797]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-002d97a55d8b83668dc3dfa6`
- 定位：word/document.xml/body/p[1798], word/document.xml/body/p[1799], word/document.xml/body/p[1800]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：核对 journalctl -xeu kubelet 在‘基本故障排查 / 集群安装问题’中的原始语法，不把示例当现场参数。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-8baf65985aebaf898945, command-family:journalctl
- synthetic：False
- 禁止结论：执行了设备命令；示例地址就是当前现场地址
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-8b7190a7813bebeffe210cc7`
- 定位：word/document.xml/body/p[1788], word/document.xml/body/p[1789], word/document.xml/body/p[1790]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
集群安装问题
集群安装失败时，集群安装过程中输出的日志信息有限，一般需要进一步检查kubernetes系统进程例如kubelet、containerd状态及日志。
1.	查看kubelet运行状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7d6750acd76fa1ca0043ec44`
- 定位：word/document.xml/body/p[1791]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-04f75f76e3e997b3afb95ab4`
- 定位：word/document.xml/body/p[1792]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
2.	查看containerd容器运行时状态
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-cabd3152ee269df6489ed07b`
- 定位：word/document.xml/body/p[1793]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
systemctl status containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-e7773e4bc9c9794eef44177c`
- 定位：word/document.xml/body/p[1794]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
3.	查看kubelet详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-40e89a682b78c5baf67ab343`
- 定位：word/document.xml/body/p[1795]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu kubelet
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-7eb6ba2c984e4c3c2253d153`
- 定位：word/document.xml/body/p[1796]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
4.	查看containerd详细运行日志
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-5bf91a33efe9ff9fa23173e1`
- 定位：word/document.xml/body/p[1797]
```text
K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
journalctl -xeu containerd
```
- 来源：UPF 5.0安装部署指导书(新网管版)(1).docx · `chunk-002d97a55d8b83668dc3dfa6`
- 定位：word/document.xml/body/p[1798], word/document.xml/body/p[1799], word/document.xml/body/p[1800]
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

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，UPF接口地址配置功能有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-47801797ff967c3d955d, section-a64f290aecf26f8aac93, section-d4ce23a67f85b23bb481, business-topic:产品使用:产品配置 / 网管配置管理 / 接口地址配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-41fa90a727141e4d152acb95`
- 定位：word/document.xml/body/p[47]
```text
产品配置 / 网管配置管理 / 接口地址配置
接口地址配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-df5b58cb3e57cebf7145f57a`
- 定位：word/document.xml/body/p[48], word/document.xml/body/p[49]
```text
网管配置管理 / 接口地址配置 / 功能描述
功能描述
配置UPF N3, N6, N9等接口IP。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-d4340ab4f0ea6f40f65fc77c`
- 定位：word/document.xml/body/p[50], word/document.xml/body/p[51], word/document.xml/body/p[52], word/document.xml/body/p[53], word/document.xml/body/p[54]
```text
网管配置管理 / 接口地址配置 / 功能配置
功能配置
操作步骤：
配置管理 > 基本配置 > 业务配置 > 接口地址配置
N3, N6地址都配置完后，UPF上 show config 可以看到N3, N6地址。
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-fafb030542846a960f60d97d`
- 定位：word/document.xml/body/tbl[1]/tr[2], word/document.xml/body/tbl[1]/tr[3], word/document.xml/body/tbl[1]/tr[4], word/document.xml/body/tbl[1]/tr[5], word/document.xml/body/tbl[1]/tr[6], word/document.xml/body/tbl[1]/tr[7]
```text
网管配置管理 / 接口地址配置 / 功能配置
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口ID | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：必选 | 默认值：无 | 参数说明：示例：6
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口类型 | 参数值类型：枚举型 | 取值范围：N3,N6,N9,N4 | 是否必选：必选 | 默认值：无 | 参数说明：示例：N6
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IP地址类型 | 参数值类型：枚举型 | 取值范围：IPv4,IPv6 | 是否必选：必选 | 默认值：无 | 参数说明：示例：IPv4
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4地址 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173.1.6.151
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4子网掩码 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：255.255.255.0
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6地址 | 参数值类型：Ipv6型 | 取值范围：40 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173:1:6::151
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-e29d930f9c6ce0051acf08f2`
- 定位：word/document.xml/body/tbl[1]/tr[8]
```text
网管配置管理 / 接口地址配置 / 功能配置
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6前缀长度 | 参数值类型：整型 | 取值范围：(1,128) | 是否必选：可选 | 默认值：无 | 参数说明：示例：96
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-4990c609f0442fe1fa34911d`
- 定位：word/document.xml/body/p[55], word/document.xml/body/p[59]
```text
网管配置管理 / 接口地址配置 / 功能配置
配置操作
查询操作
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / 接口地址配置
接口地址配置
网管配置管理 / 接口地址配置 / 功能描述
功能描述
配置UPF N3, N6, N9等接口IP。
网管配置管理 / 接口地址配置 / 功能配置
功能配置
操作步骤：
配置管理 > 基本配置 > 业务配置 > 接口地址配置
N3, N6地址都配置完后，UPF上 show config 可以看到N3, N6地址。
参数配置
网管配置管理 / 接口地址配置 / 功能配置
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口ID | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：必选 | 默认值：无 | 参数说明：示例：6
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口类型 | 参数值类型：枚举型 | 取值范围：N3,N6,N9,N4 | 是否必选：必选 | 默认值：无 | 参数说明：示例：N6
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IP地址类型 | 参数值类型：枚举型 | 取值范围：IPv4,IPv6 | 是否必选：必选 | 默认值：无 | 参数说明：示例：IPv4
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4地址 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173.1.6.151
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4子网掩码 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：255.255.255.0
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6地址 | 参数值类型：Ipv6型 | 取值范围：40 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173:1:6::151
网管配置管理 / 接口地址配置 / 功能配置
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6前缀长度 | 参数值类型：整型 | 取值范围：(1,128) | 是否必选：可选 | 默认值：无 | 参数说明：示例：96
网管配置管理 / 接口地址配置 / 功能配置
配置操作
查询操作
```

## knowledge-002 · dev · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对UPF接口地址配置功能的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-47801797ff967c3d955d, section-a64f290aecf26f8aac93, section-d4ce23a67f85b23bb481, business-topic:产品使用:产品配置 / 网管配置管理 / 接口地址配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-41fa90a727141e4d152acb95`
- 定位：word/document.xml/body/p[47]
```text
产品配置 / 网管配置管理 / 接口地址配置
接口地址配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-df5b58cb3e57cebf7145f57a`
- 定位：word/document.xml/body/p[48], word/document.xml/body/p[49]
```text
网管配置管理 / 接口地址配置 / 功能描述
功能描述
配置UPF N3, N6, N9等接口IP。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-d4340ab4f0ea6f40f65fc77c`
- 定位：word/document.xml/body/p[50], word/document.xml/body/p[51], word/document.xml/body/p[52], word/document.xml/body/p[53], word/document.xml/body/p[54]
```text
网管配置管理 / 接口地址配置 / 功能配置
功能配置
操作步骤：
配置管理 > 基本配置 > 业务配置 > 接口地址配置
N3, N6地址都配置完后，UPF上 show config 可以看到N3, N6地址。
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-fafb030542846a960f60d97d`
- 定位：word/document.xml/body/tbl[1]/tr[2], word/document.xml/body/tbl[1]/tr[3], word/document.xml/body/tbl[1]/tr[4], word/document.xml/body/tbl[1]/tr[5], word/document.xml/body/tbl[1]/tr[6], word/document.xml/body/tbl[1]/tr[7]
```text
网管配置管理 / 接口地址配置 / 功能配置
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口ID | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：必选 | 默认值：无 | 参数说明：示例：6
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口类型 | 参数值类型：枚举型 | 取值范围：N3,N6,N9,N4 | 是否必选：必选 | 默认值：无 | 参数说明：示例：N6
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IP地址类型 | 参数值类型：枚举型 | 取值范围：IPv4,IPv6 | 是否必选：必选 | 默认值：无 | 参数说明：示例：IPv4
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4地址 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173.1.6.151
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4子网掩码 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：255.255.255.0
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6地址 | 参数值类型：Ipv6型 | 取值范围：40 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173:1:6::151
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-e29d930f9c6ce0051acf08f2`
- 定位：word/document.xml/body/tbl[1]/tr[8]
```text
网管配置管理 / 接口地址配置 / 功能配置
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6前缀长度 | 参数值类型：整型 | 取值范围：(1,128) | 是否必选：可选 | 默认值：无 | 参数说明：示例：96
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-4990c609f0442fe1fa34911d`
- 定位：word/document.xml/body/p[55], word/document.xml/body/p[59]
```text
网管配置管理 / 接口地址配置 / 功能配置
配置操作
查询操作
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / 接口地址配置
接口地址配置
网管配置管理 / 接口地址配置 / 功能描述
功能描述
配置UPF N3, N6, N9等接口IP。
网管配置管理 / 接口地址配置 / 功能配置
功能配置
操作步骤：
配置管理 > 基本配置 > 业务配置 > 接口地址配置
N3, N6地址都配置完后，UPF上 show config 可以看到N3, N6地址。
参数配置
网管配置管理 / 接口地址配置 / 功能配置
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口ID | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：必选 | 默认值：无 | 参数说明：示例：6
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口类型 | 参数值类型：枚举型 | 取值范围：N3,N6,N9,N4 | 是否必选：必选 | 默认值：无 | 参数说明：示例：N6
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IP地址类型 | 参数值类型：枚举型 | 取值范围：IPv4,IPv6 | 是否必选：必选 | 默认值：无 | 参数说明：示例：IPv4
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4地址 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173.1.6.151
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4子网掩码 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：255.255.255.0
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6地址 | 参数值类型：Ipv6型 | 取值范围：40 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173:1:6::151
网管配置管理 / 接口地址配置 / 功能配置
表格：接口地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6前缀长度 | 参数值类型：整型 | 取值范围：(1,128) | 是否必选：可选 | 默认值：无 | 参数说明：示例：96
网管配置管理 / 接口地址配置 / 功能配置
配置操作
查询操作
```

## knowledge-003 · dev · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，CP IP地址配置功能有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-5a7b99e84fb9e4da50fd, section-87f442ad4b4271e34473, section-a271d803f032a8b639d1, business-topic:产品使用:产品配置 / 网管配置管理 / CP IP地址配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-88f6a3a53d500903d6f89ac1`
- 定位：word/document.xml/body/p[62]
```text
产品配置 / 网管配置管理 / CP IP地址配置
CP IP地址配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-a55e1e871bdf4172e73da591`
- 定位：word/document.xml/body/p[63], word/document.xml/body/p[64]
```text
网管配置管理 / CP IP地址配置 / 功能描述
功能描述
配置SMF的IP，然后后就会往这个IP发Associate消息建立偶联。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-174a818f8701a3268e3feec6`
- 定位：word/document.xml/body/p[65], word/document.xml/body/p[66], word/document.xml/body/p[67], word/document.xml/body/p[68], word/document.xml/body/p[69]
```text
网管配置管理 / CP IP地址配置 / 功能配置
功能配置
操作步骤：
配置管理 > 基本配置 > 业务配置 > CP IP地址配置
UPF上 show config确认配置。UPF上抓包可以看到UPF开始发的asso req
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-a48d02ff7ece42bb23281fef`
- 定位：word/document.xml/body/tbl[2]/tr[2], word/document.xml/body/tbl[2]/tr[3], word/document.xml/body/tbl[2]/tr[4], word/document.xml/body/tbl[2]/tr[5], word/document.xml/body/tbl[2]/tr[6]
```text
网管配置管理 / CP IP地址配置 / 功能配置
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：ID | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：必选 | 默认值：无 | 参数说明：示例：1
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IP地址类型 | 参数值类型：枚举型 | 取值范围：IPv4,IPv6 | 是否必选：必选 | 默认值：无 | 参数说明：示例：IPv4
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4地址 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173.1.4.152
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6地址 | 参数值类型：Ipv6型 | 取值范围：40 字节 | 是否必选：可选 | 默认值：无
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口ID索引 | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：可选 | 默认值：无
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / CP IP地址配置
CP IP地址配置
网管配置管理 / CP IP地址配置 / 功能描述
功能描述
配置SMF的IP，然后后就会往这个IP发Associate消息建立偶联。
网管配置管理 / CP IP地址配置 / 功能配置
功能配置
操作步骤：
配置管理 > 基本配置 > 业务配置 > CP IP地址配置
UPF上 show config确认配置。UPF上抓包可以看到UPF开始发的asso req
参数配置
网管配置管理 / CP IP地址配置 / 功能配置
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：ID | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：必选 | 默认值：无 | 参数说明：示例：1
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IP地址类型 | 参数值类型：枚举型 | 取值范围：IPv4,IPv6 | 是否必选：必选 | 默认值：无 | 参数说明：示例：IPv4
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4地址 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173.1.4.152
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6地址 | 参数值类型：Ipv6型 | 取值范围：40 字节 | 是否必选：可选 | 默认值：无
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口ID索引 | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：可选 | 默认值：无
```

## knowledge-004 · dev · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对CP IP地址配置功能的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-5a7b99e84fb9e4da50fd, section-87f442ad4b4271e34473, section-a271d803f032a8b639d1, business-topic:产品使用:产品配置 / 网管配置管理 / CP IP地址配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-88f6a3a53d500903d6f89ac1`
- 定位：word/document.xml/body/p[62]
```text
产品配置 / 网管配置管理 / CP IP地址配置
CP IP地址配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-a55e1e871bdf4172e73da591`
- 定位：word/document.xml/body/p[63], word/document.xml/body/p[64]
```text
网管配置管理 / CP IP地址配置 / 功能描述
功能描述
配置SMF的IP，然后后就会往这个IP发Associate消息建立偶联。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-174a818f8701a3268e3feec6`
- 定位：word/document.xml/body/p[65], word/document.xml/body/p[66], word/document.xml/body/p[67], word/document.xml/body/p[68], word/document.xml/body/p[69]
```text
网管配置管理 / CP IP地址配置 / 功能配置
功能配置
操作步骤：
配置管理 > 基本配置 > 业务配置 > CP IP地址配置
UPF上 show config确认配置。UPF上抓包可以看到UPF开始发的asso req
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-a48d02ff7ece42bb23281fef`
- 定位：word/document.xml/body/tbl[2]/tr[2], word/document.xml/body/tbl[2]/tr[3], word/document.xml/body/tbl[2]/tr[4], word/document.xml/body/tbl[2]/tr[5], word/document.xml/body/tbl[2]/tr[6]
```text
网管配置管理 / CP IP地址配置 / 功能配置
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：ID | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：必选 | 默认值：无 | 参数说明：示例：1
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IP地址类型 | 参数值类型：枚举型 | 取值范围：IPv4,IPv6 | 是否必选：必选 | 默认值：无 | 参数说明：示例：IPv4
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4地址 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173.1.4.152
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6地址 | 参数值类型：Ipv6型 | 取值范围：40 字节 | 是否必选：可选 | 默认值：无
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口ID索引 | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：可选 | 默认值：无
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / CP IP地址配置
CP IP地址配置
网管配置管理 / CP IP地址配置 / 功能描述
功能描述
配置SMF的IP，然后后就会往这个IP发Associate消息建立偶联。
网管配置管理 / CP IP地址配置 / 功能配置
功能配置
操作步骤：
配置管理 > 基本配置 > 业务配置 > CP IP地址配置
UPF上 show config确认配置。UPF上抓包可以看到UPF开始发的asso req
参数配置
网管配置管理 / CP IP地址配置 / 功能配置
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：ID | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：必选 | 默认值：无 | 参数说明：示例：1
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IP地址类型 | 参数值类型：枚举型 | 取值范围：IPv4,IPv6 | 是否必选：必选 | 默认值：无 | 参数说明：示例：IPv4
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv4地址 | 参数值类型：Ipv4型 | 取值范围：16 字节 | 是否必选：可选 | 默认值：无 | 参数说明：示例：173.1.4.152
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：IPv6地址 | 参数值类型：Ipv6型 | 取值范围：40 字节 | 是否必选：可选 | 默认值：无
表格：CP IP地址配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：接口ID索引 | 参数值类型：整型 | 取值范围：(1,16) | 是否必选：可选 | 默认值：无
```

## knowledge-005 · dev · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，UPF网管清除告警功能有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-0de95f0d065e91684891, section-5a92e98717ee3705b409, section-a6d242ce1ceeae9c0c7a, business-topic:产品使用:产品监控 / 网管告警监控 / 清除告警
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-8848301e8d910817d18cd923`
- 定位：word/document.xml/body/p[329]
```text
产品监控 / 网管告警监控 / 清除告警
清除告警
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-be83a0c07f1a366e427ed769`
- 定位：word/document.xml/body/p[330], word/document.xml/body/p[331]
```text
网管告警监控 / 清除告警 / 功能描述
功能描述
当告警上报到UNMS系统，可排除故障后按照处理步骤进行操作，以确保能快速并成功处理告警。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-ce7ccc3c93eedd055c2b932e`
- 定位：word/document.xml/body/p[332], word/document.xml/body/p[333], word/document.xml/body/p[335], word/document.xml/body/p[336], word/document.xml/body/p[337]
```text
网管告警监控 / 清除告警 / 功能配置
功能配置
操作步骤：
1. 在菜单栏选择“告警管理 > 当前告警”，进入当前告警界面，查看相关告警信息。
2. 排除相关故障。 告警一般会自动清除。
3. 如果告警未自动清除，可在“告警处理”界面选中该告警，单击“清除”图标 或鼠标右键选择“清除”。 已确认已清除的告警，将会自动移入历史告警列表中。
```
- 预期原文/缺口：
```text
产品监控 / 网管告警监控 / 清除告警
清除告警
网管告警监控 / 清除告警 / 功能描述
功能描述
当告警上报到UNMS系统，可排除故障后按照处理步骤进行操作，以确保能快速并成功处理告警。
网管告警监控 / 清除告警 / 功能配置
功能配置
操作步骤：
1. 在菜单栏选择“告警管理 > 当前告警”，进入当前告警界面，查看相关告警信息。
2. 排除相关故障。 告警一般会自动清除。
3. 如果告警未自动清除，可在“告警处理”界面选中该告警，单击“清除”图标 或鼠标右键选择“清除”。 已确认已清除的告警，将会自动移入历史告警列表中。
```

## knowledge-006 · dev · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对UPF网管清除告警功能的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-0de95f0d065e91684891, section-5a92e98717ee3705b409, section-a6d242ce1ceeae9c0c7a, business-topic:产品使用:产品监控 / 网管告警监控 / 清除告警
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-8848301e8d910817d18cd923`
- 定位：word/document.xml/body/p[329]
```text
产品监控 / 网管告警监控 / 清除告警
清除告警
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-be83a0c07f1a366e427ed769`
- 定位：word/document.xml/body/p[330], word/document.xml/body/p[331]
```text
网管告警监控 / 清除告警 / 功能描述
功能描述
当告警上报到UNMS系统，可排除故障后按照处理步骤进行操作，以确保能快速并成功处理告警。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-ce7ccc3c93eedd055c2b932e`
- 定位：word/document.xml/body/p[332], word/document.xml/body/p[333], word/document.xml/body/p[335], word/document.xml/body/p[336], word/document.xml/body/p[337]
```text
网管告警监控 / 清除告警 / 功能配置
功能配置
操作步骤：
1. 在菜单栏选择“告警管理 > 当前告警”，进入当前告警界面，查看相关告警信息。
2. 排除相关故障。 告警一般会自动清除。
3. 如果告警未自动清除，可在“告警处理”界面选中该告警，单击“清除”图标 或鼠标右键选择“清除”。 已确认已清除的告警，将会自动移入历史告警列表中。
```
- 预期原文/缺口：
```text
产品监控 / 网管告警监控 / 清除告警
清除告警
网管告警监控 / 清除告警 / 功能描述
功能描述
当告警上报到UNMS系统，可排除故障后按照处理步骤进行操作，以确保能快速并成功处理告警。
网管告警监控 / 清除告警 / 功能配置
功能配置
操作步骤：
1. 在菜单栏选择“告警管理 > 当前告警”，进入当前告警界面，查看相关告警信息。
2. 排除相关故障。 告警一般会自动清除。
3. 如果告警未自动清除，可在“告警处理”界面选中该告警，单击“清除”图标 或鼠标右键选择“清除”。 已确认已清除的告警，将会自动移入历史告警列表中。
```

## knowledge-007 · dev · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，5GC网管实时告警查询有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-314d5be1655ed1806639, business-topic:网管使用:7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-0d555a667d8458f08194b6fa`
- 定位：word/document.xml/body/p[839], word/document.xml/body/p[840], word/document.xml/body/p[841], word/document.xml/body/p[843], word/document.xml/body/p[844]
```text
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
7.1.1 告警查询
路径：Alarm-->Active Alarm
步骤：在各个下拉框中选择选项-->点击“Query Alarm”-->点击“Refresh”，查询接果将在列表显示。
图7.1.1-1 Active Alarm页面
配置项及说明：
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-a014cd03bfc802738d470de9`
- 定位：word/document.xml/body/tbl[22]/tr[2], word/document.xml/body/tbl[22]/tr[3], word/document.xml/body/tbl[22]/tr[4], word/document.xml/body/tbl[22]/tr[5], word/document.xml/body/tbl[22]/tr[6], word/document.xml/body/tbl[22]/tr[7], word/document.xml/body/tbl[22]/tr[8], word/document.xml/body/tbl[22]/tr[9], word/document.xml/body/tbl[22]/tr[10], word/document.xml/body/tbl[22]/tr[11], word/document.xml/body/tbl[22]/tr[12], word/document.xml/body/tbl[22]/tr[13]
```text
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：NF Type | 说明：NF类型
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Region | 说明：区域
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Point | 说明：局点
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：NF ID | 说明：NF ID
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Select Alarm Level | 说明：选择告警等级，可选All Status/minor/major/critical
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Select Alarm Type | 说明：选择告警类型，可选All/AppAlarm/LinkAlarm/SystemAlarm
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Start | 说明：起始时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：End | 说明：终止时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Code | 说明：告警编码
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Ne ID | 说明：告警模块名
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Sync Mode | 说明：告警同步模式
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Info | 说明：告警信息
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-1849be592ac7bae7c748f3f9`
- 定位：word/document.xml/body/tbl[22]/tr[14], word/document.xml/body/tbl[22]/tr[15], word/document.xml/body/tbl[22]/tr[16]
```text
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Event Time | 说明：触发告警时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Limit Set | 说明：阈值
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Status | 说明：告警状态
```
- 预期原文/缺口：
```text
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
7.1.1 告警查询
路径：Alarm-->Active Alarm
步骤：在各个下拉框中选择选项-->点击“Query Alarm”-->点击“Refresh”，查询接果将在列表显示。
图7.1.1-1 Active Alarm页面
配置项及说明：
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：NF Type | 说明：NF类型
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Region | 说明：区域
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Point | 说明：局点
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：NF ID | 说明：NF ID
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Select Alarm Level | 说明：选择告警等级，可选All Status/minor/major/critical
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Select Alarm Type | 说明：选择告警类型，可选All/AppAlarm/LinkAlarm/SystemAlarm
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Start | 说明：起始时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：End | 说明：终止时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Code | 说明：告警编码
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Ne ID | 说明：告警模块名
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Sync Mode | 说明：告警同步模式
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Info | 说明：告警信息
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Event Time | 说明：触发告警时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Limit Set | 说明：阈值
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Status | 说明：告警状态
```

## knowledge-008 · dev · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对5GC网管实时告警查询的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-314d5be1655ed1806639, business-topic:网管使用:7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-0d555a667d8458f08194b6fa`
- 定位：word/document.xml/body/p[839], word/document.xml/body/p[840], word/document.xml/body/p[841], word/document.xml/body/p[843], word/document.xml/body/p[844]
```text
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
7.1.1 告警查询
路径：Alarm-->Active Alarm
步骤：在各个下拉框中选择选项-->点击“Query Alarm”-->点击“Refresh”，查询接果将在列表显示。
图7.1.1-1 Active Alarm页面
配置项及说明：
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-a014cd03bfc802738d470de9`
- 定位：word/document.xml/body/tbl[22]/tr[2], word/document.xml/body/tbl[22]/tr[3], word/document.xml/body/tbl[22]/tr[4], word/document.xml/body/tbl[22]/tr[5], word/document.xml/body/tbl[22]/tr[6], word/document.xml/body/tbl[22]/tr[7], word/document.xml/body/tbl[22]/tr[8], word/document.xml/body/tbl[22]/tr[9], word/document.xml/body/tbl[22]/tr[10], word/document.xml/body/tbl[22]/tr[11], word/document.xml/body/tbl[22]/tr[12], word/document.xml/body/tbl[22]/tr[13]
```text
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：NF Type | 说明：NF类型
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Region | 说明：区域
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Point | 说明：局点
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：NF ID | 说明：NF ID
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Select Alarm Level | 说明：选择告警等级，可选All Status/minor/major/critical
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Select Alarm Type | 说明：选择告警类型，可选All/AppAlarm/LinkAlarm/SystemAlarm
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Start | 说明：起始时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：End | 说明：终止时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Code | 说明：告警编码
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Ne ID | 说明：告警模块名
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Sync Mode | 说明：告警同步模式
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Info | 说明：告警信息
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-1849be592ac7bae7c748f3f9`
- 定位：word/document.xml/body/tbl[22]/tr[14], word/document.xml/body/tbl[22]/tr[15], word/document.xml/body/tbl[22]/tr[16]
```text
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Event Time | 说明：触发告警时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Limit Set | 说明：阈值
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Status | 说明：告警状态
```
- 预期原文/缺口：
```text
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
7.1.1 告警查询
路径：Alarm-->Active Alarm
步骤：在各个下拉框中选择选项-->点击“Query Alarm”-->点击“Refresh”，查询接果将在列表显示。
图7.1.1-1 Active Alarm页面
配置项及说明：
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：NF Type | 说明：NF类型
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Region | 说明：区域
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Point | 说明：局点
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：NF ID | 说明：NF ID
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Select Alarm Level | 说明：选择告警等级，可选All Status/minor/major/critical
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Select Alarm Type | 说明：选择告警类型，可选All/AppAlarm/LinkAlarm/SystemAlarm
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Start | 说明：起始时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：End | 说明：终止时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Code | 说明：告警编码
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Ne ID | 说明：告警模块名
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Sync Mode | 说明：告警同步模式
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Info | 说明：告警信息
7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Event Time | 说明：触发告警时间
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Limit Set | 说明：阈值
表格：7.1 实时告警 / 7.1.1 告警查询
表头：配置项	说明
配置项：Alarm Status | 说明：告警状态
```

## knowledge-009 · dev · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，UP功能特性配置有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-2bb4970b30ab3c2060fe, section-32e17708e55f914d81a1, section-d0bc1b12a42f4aca09f5, business-topic:产品使用:产品配置 / 网管配置管理 / UP功能特性配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-c8cf8cae162ff90103610086`
- 定位：word/document.xml/body/p[114]
```text
产品配置 / 网管配置管理 / UP功能特性配置
UP功能特性配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-86573082351baac25639c711`
- 定位：word/document.xml/body/p[115], word/document.xml/body/p[116]
```text
网管配置管理 / UP功能特性配置 / 功能描述
功能描述
用于编码Associate消息的IE：feature flag
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-857a81c6e6430cc4a55c3bf1`
- 定位：word/document.xml/body/p[117], word/document.xml/body/p[118], word/document.xml/body/p[119]
```text
网管配置管理 / UP功能特性配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > UP功能特性配置
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-0ca8a1cfc4b1cd97b3f413b2`
- 定位：word/document.xml/body/tbl[8]/tr[2], word/document.xml/body/tbl[8]/tr[3], word/document.xml/body/tbl[8]/tr[4], word/document.xml/body/tbl[8]/tr[5], word/document.xml/body/tbl[8]/tr[6], word/document.xml/body/tbl[8]/tr[7], word/document.xml/body/tbl[8]/tr[8], word/document.xml/body/tbl[8]/tr[9]
```text
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：BUCP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DDND | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DLBD | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TRST | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：FTUP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFDM | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：HEEU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TREU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-42359eedabf592cf36ef38d1`
- 定位：word/document.xml/body/tbl[8]/tr[10], word/document.xml/body/tbl[8]/tr[11], word/document.xml/body/tbl[8]/tr[12], word/document.xml/body/tbl[8]/tr[13], word/document.xml/body/tbl[8]/tr[14], word/document.xml/body/tbl[8]/tr[15], word/document.xml/body/tbl[8]/tr[16], word/document.xml/body/tbl[8]/tr[17]
```text
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：EMPU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：Ture
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PDIU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：UDBC | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：QUOAC | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TRACE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：FRRT | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFDE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：EPFAR | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-bb3e665f6b54bf7ce9595476`
- 定位：word/document.xml/body/tbl[8]/tr[18], word/document.xml/body/tbl[8]/tr[19], word/document.xml/body/tbl[8]/tr[20], word/document.xml/body/tbl[8]/tr[21], word/document.xml/body/tbl[8]/tr[22], word/document.xml/body/tbl[8]/tr[23], word/document.xml/body/tbl[8]/tr[24], word/document.xml/body/tbl[8]/tr[25]
```text
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DPDRA | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：ADPDP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：UEIP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：SSET | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MNOP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MTE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：BUNDL | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：GCOM | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-1f58da08b9301892a9299f2e`
- 定位：word/document.xml/body/tbl[8]/tr[26]
```text
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MPAS | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：Ture
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / UP功能特性配置
UP功能特性配置
网管配置管理 / UP功能特性配置 / 功能描述
功能描述
用于编码Associate消息的IE：feature flag
网管配置管理 / UP功能特性配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > UP功能特性配置
参数配置
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：BUCP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DDND | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DLBD | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TRST | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：FTUP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFDM | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：HEEU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TREU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：EMPU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：Ture
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PDIU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：UDBC | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：QUOAC | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TRACE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：FRRT | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFDE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：EPFAR | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DPDRA | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：ADPDP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：UEIP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：SSET | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MNOP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MTE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：BUNDL | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：GCOM | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MPAS | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：Ture
```

## knowledge-010 · dev · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对UP功能特性配置的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-2bb4970b30ab3c2060fe, section-32e17708e55f914d81a1, section-d0bc1b12a42f4aca09f5, business-topic:产品使用:产品配置 / 网管配置管理 / UP功能特性配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-c8cf8cae162ff90103610086`
- 定位：word/document.xml/body/p[114]
```text
产品配置 / 网管配置管理 / UP功能特性配置
UP功能特性配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-86573082351baac25639c711`
- 定位：word/document.xml/body/p[115], word/document.xml/body/p[116]
```text
网管配置管理 / UP功能特性配置 / 功能描述
功能描述
用于编码Associate消息的IE：feature flag
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-857a81c6e6430cc4a55c3bf1`
- 定位：word/document.xml/body/p[117], word/document.xml/body/p[118], word/document.xml/body/p[119]
```text
网管配置管理 / UP功能特性配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > UP功能特性配置
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-0ca8a1cfc4b1cd97b3f413b2`
- 定位：word/document.xml/body/tbl[8]/tr[2], word/document.xml/body/tbl[8]/tr[3], word/document.xml/body/tbl[8]/tr[4], word/document.xml/body/tbl[8]/tr[5], word/document.xml/body/tbl[8]/tr[6], word/document.xml/body/tbl[8]/tr[7], word/document.xml/body/tbl[8]/tr[8], word/document.xml/body/tbl[8]/tr[9]
```text
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：BUCP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DDND | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DLBD | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TRST | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：FTUP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFDM | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：HEEU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TREU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-42359eedabf592cf36ef38d1`
- 定位：word/document.xml/body/tbl[8]/tr[10], word/document.xml/body/tbl[8]/tr[11], word/document.xml/body/tbl[8]/tr[12], word/document.xml/body/tbl[8]/tr[13], word/document.xml/body/tbl[8]/tr[14], word/document.xml/body/tbl[8]/tr[15], word/document.xml/body/tbl[8]/tr[16], word/document.xml/body/tbl[8]/tr[17]
```text
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：EMPU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：Ture
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PDIU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：UDBC | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：QUOAC | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TRACE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：FRRT | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFDE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：EPFAR | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-bb3e665f6b54bf7ce9595476`
- 定位：word/document.xml/body/tbl[8]/tr[18], word/document.xml/body/tbl[8]/tr[19], word/document.xml/body/tbl[8]/tr[20], word/document.xml/body/tbl[8]/tr[21], word/document.xml/body/tbl[8]/tr[22], word/document.xml/body/tbl[8]/tr[23], word/document.xml/body/tbl[8]/tr[24], word/document.xml/body/tbl[8]/tr[25]
```text
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DPDRA | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：ADPDP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：UEIP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：SSET | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MNOP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MTE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：BUNDL | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：GCOM | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-1f58da08b9301892a9299f2e`
- 定位：word/document.xml/body/tbl[8]/tr[26]
```text
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MPAS | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：Ture
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / UP功能特性配置
UP功能特性配置
网管配置管理 / UP功能特性配置 / 功能描述
功能描述
用于编码Associate消息的IE：feature flag
网管配置管理 / UP功能特性配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > UP功能特性配置
参数配置
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：BUCP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DDND | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DLBD | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TRST | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：FTUP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFDM | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：HEEU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TREU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：EMPU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：Ture
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PDIU | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：UDBC | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：QUOAC | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：TRACE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：FRRT | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFDE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：EPFAR | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DPDRA | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：ADPDP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：True
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：UEIP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：SSET | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MNOP | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MTE | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：BUNDL | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：GCOM | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：无
网管配置管理 / UP功能特性配置 / 功能配置
表格：UP功能特性配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：MPAS | 参数值类型：Bool型 | 取值范围：False,True | 是否必选：可选 | 默认值：Ture
```

## knowledge-011 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，PFCP定时器配置有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-531ad8156a93b35355a3, section-54cfb44a5f298863bf9c, section-acdf403848b6952db4bd, business-topic:产品使用:产品配置 / 网管配置管理 / PFCP定时器配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-0fae5a7712703c38358f0ce2`
- 定位：word/document.xml/body/p[133]
```text
产品配置 / 网管配置管理 / PFCP定时器配置
PFCP定时器配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-b2f9c385e55e5546094a89e7`
- 定位：word/document.xml/body/p[134], word/document.xml/body/p[135]
```text
网管配置管理 / PFCP定时器配置 / 功能描述
功能描述
控制heartbeat消息发送间隔等。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-c010c6ac67a3df2fe37ac535`
- 定位：word/document.xml/body/p[136], word/document.xml/body/p[137], word/document.xml/body/p[138]
```text
网管配置管理 / PFCP定时器配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > PFCP定时器配置
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-e778f08f509edf905d2e9e24`
- 定位：word/document.xml/body/tbl[11]/tr[2], word/document.xml/body/tbl[11]/tr[3]
```text
网管配置管理 / PFCP定时器配置 / 功能配置
表格：PFCP定时器配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFCP消息重发次数 | 参数值类型：整型 | 取值范围：(3,5) | 是否必选：可选 | 默认值：3
表格：PFCP定时器配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFCP消息重发间隔 | 参数值类型：整型 | 取值范围：(1,5) | 是否必选：可选 | 默认值：3
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / PFCP定时器配置
PFCP定时器配置
网管配置管理 / PFCP定时器配置 / 功能描述
功能描述
控制heartbeat消息发送间隔等。
网管配置管理 / PFCP定时器配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > PFCP定时器配置
参数配置
网管配置管理 / PFCP定时器配置 / 功能配置
表格：PFCP定时器配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFCP消息重发次数 | 参数值类型：整型 | 取值范围：(3,5) | 是否必选：可选 | 默认值：3
表格：PFCP定时器配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFCP消息重发间隔 | 参数值类型：整型 | 取值范围：(1,5) | 是否必选：可选 | 默认值：3
```

## knowledge-012 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对PFCP定时器配置的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-531ad8156a93b35355a3, section-54cfb44a5f298863bf9c, section-acdf403848b6952db4bd, business-topic:产品使用:产品配置 / 网管配置管理 / PFCP定时器配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-0fae5a7712703c38358f0ce2`
- 定位：word/document.xml/body/p[133]
```text
产品配置 / 网管配置管理 / PFCP定时器配置
PFCP定时器配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-b2f9c385e55e5546094a89e7`
- 定位：word/document.xml/body/p[134], word/document.xml/body/p[135]
```text
网管配置管理 / PFCP定时器配置 / 功能描述
功能描述
控制heartbeat消息发送间隔等。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-c010c6ac67a3df2fe37ac535`
- 定位：word/document.xml/body/p[136], word/document.xml/body/p[137], word/document.xml/body/p[138]
```text
网管配置管理 / PFCP定时器配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > PFCP定时器配置
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-e778f08f509edf905d2e9e24`
- 定位：word/document.xml/body/tbl[11]/tr[2], word/document.xml/body/tbl[11]/tr[3]
```text
网管配置管理 / PFCP定时器配置 / 功能配置
表格：PFCP定时器配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFCP消息重发次数 | 参数值类型：整型 | 取值范围：(3,5) | 是否必选：可选 | 默认值：3
表格：PFCP定时器配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFCP消息重发间隔 | 参数值类型：整型 | 取值范围：(1,5) | 是否必选：可选 | 默认值：3
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / PFCP定时器配置
PFCP定时器配置
网管配置管理 / PFCP定时器配置 / 功能描述
功能描述
控制heartbeat消息发送间隔等。
网管配置管理 / PFCP定时器配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > PFCP定时器配置
参数配置
网管配置管理 / PFCP定时器配置 / 功能配置
表格：PFCP定时器配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFCP消息重发次数 | 参数值类型：整型 | 取值范围：(3,5) | 是否必选：可选 | 默认值：3
表格：PFCP定时器配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：PFCP消息重发间隔 | 参数值类型：整型 | 取值范围：(1,5) | 是否必选：可选 | 默认值：3
```

## knowledge-013 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，DNN带宽配置有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-54a50fc2c2e43e9f2b46, section-5f913a60ca3aaec84484, section-db9e4a3ff24b441944f1, business-topic:产品使用:产品配置 / 网管配置管理 / DNN带宽配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-cd98620837e3fc0a022e679f`
- 定位：word/document.xml/body/p[120]
```text
产品配置 / 网管配置管理 / DNN带宽配置
DNN带宽配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-88eba38020c3ed9d76f77714`
- 定位：word/document.xml/body/p[121]
```text
网管配置管理 / DNN带宽配置 / 功能描述
功能描述
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-ce2597b37a05ab3effe3f68e`
- 定位：word/document.xml/body/p[122], word/document.xml/body/p[123], word/document.xml/body/p[124]
```text
网管配置管理 / DNN带宽配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > DNN带宽配置
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-2370b7312c9eb4a1cb19a256`
- 定位：word/document.xml/body/tbl[9]/tr[2], word/document.xml/body/tbl[9]/tr[3]
```text
网管配置管理 / DNN带宽配置 / 功能配置
表格：DNN带宽配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DNN | 参数值类型：Text型 | 取值范围：101 字节 | 默认值：无
表格：DNN带宽配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：带宽(Mbps) | 参数值类型：整型 | 取值范围：(0,20480) | 默认值：1024
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / DNN带宽配置
DNN带宽配置
网管配置管理 / DNN带宽配置 / 功能描述
功能描述
网管配置管理 / DNN带宽配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > DNN带宽配置
参数配置
网管配置管理 / DNN带宽配置 / 功能配置
表格：DNN带宽配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DNN | 参数值类型：Text型 | 取值范围：101 字节 | 默认值：无
表格：DNN带宽配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：带宽(Mbps) | 参数值类型：整型 | 取值范围：(0,20480) | 默认值：1024
```

## knowledge-014 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对DNN带宽配置的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-54a50fc2c2e43e9f2b46, section-5f913a60ca3aaec84484, section-db9e4a3ff24b441944f1, business-topic:产品使用:产品配置 / 网管配置管理 / DNN带宽配置
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-cd98620837e3fc0a022e679f`
- 定位：word/document.xml/body/p[120]
```text
产品配置 / 网管配置管理 / DNN带宽配置
DNN带宽配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-88eba38020c3ed9d76f77714`
- 定位：word/document.xml/body/p[121]
```text
网管配置管理 / DNN带宽配置 / 功能描述
功能描述
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-ce2597b37a05ab3effe3f68e`
- 定位：word/document.xml/body/p[122], word/document.xml/body/p[123], word/document.xml/body/p[124]
```text
网管配置管理 / DNN带宽配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > DNN带宽配置
参数配置
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-2370b7312c9eb4a1cb19a256`
- 定位：word/document.xml/body/tbl[9]/tr[2], word/document.xml/body/tbl[9]/tr[3]
```text
网管配置管理 / DNN带宽配置 / 功能配置
表格：DNN带宽配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DNN | 参数值类型：Text型 | 取值范围：101 字节 | 默认值：无
表格：DNN带宽配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：带宽(Mbps) | 参数值类型：整型 | 取值范围：(0,20480) | 默认值：1024
```
- 预期原文/缺口：
```text
产品配置 / 网管配置管理 / DNN带宽配置
DNN带宽配置
网管配置管理 / DNN带宽配置 / 功能描述
功能描述
网管配置管理 / DNN带宽配置 / 功能配置
功能配置
操作步骤：配置管理 > 基本配置 > 业务配置 > DNN带宽配置
参数配置
网管配置管理 / DNN带宽配置 / 功能配置
表格：DNN带宽配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：DNN | 参数值类型：Text型 | 取值范围：101 字节 | 默认值：无
表格：DNN带宽配置 / 功能配置
表头：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
参数名称：带宽(Mbps) | 参数值类型：整型 | 取值范围：(0,20480) | 默认值：1024
```

## knowledge-015 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，非实时测量任务创建有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-33131b8f0841df928cbd, section-39a3e49702b1eb14879b, section-809076c4afe79e2e32e9, business-topic:产品使用:产品监控 / 网管性能监控 / 非实时测量任务创建
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-b96ae6ea74b429cf717959be`
- 定位：word/document.xml/body/p[349]
```text
产品监控 / 网管性能监控 / 非实时测量任务创建
非实时测量任务创建
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-a4fdd7e54309d2e8191996d3`
- 定位：word/document.xml/body/p[350], word/document.xml/body/p[351], word/document.xml/body/p[353]
```text
网管性能监控 / 非实时测量任务创建 / 功能描述
功能描述
测量任务是一种活动，这个活动允许用户定义需要采集哪些性能数据。网元根据测量任务要求采集相应计数器，网管将采集的计数器入库。
不允许在断链网元上创建非实时测量任务。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-aa165f4d542aaed2126c07c0`
- 定位：word/document.xml/body/p[354], word/document.xml/body/p[356], word/document.xml/body/p[358], word/document.xml/body/p[360]
```text
网管性能监控 / 非实时测量任务创建 / 功能配置
功能配置
操作步骤：
在菜单栏选择“性能管理 > 5GC性能管理 > 周期测量  > 非实时任务管理> 创建任务”。
在如下图所示的对话框中选择资源节点，勾选测量对象，单击“加入下侧”。
```
- 预期原文/缺口：
```text
产品监控 / 网管性能监控 / 非实时测量任务创建
非实时测量任务创建
网管性能监控 / 非实时测量任务创建 / 功能描述
功能描述
测量任务是一种活动，这个活动允许用户定义需要采集哪些性能数据。网元根据测量任务要求采集相应计数器，网管将采集的计数器入库。
不允许在断链网元上创建非实时测量任务。
网管性能监控 / 非实时测量任务创建 / 功能配置
功能配置
操作步骤：
在菜单栏选择“性能管理 > 5GC性能管理 > 周期测量  > 非实时任务管理> 创建任务”。
在如下图所示的对话框中选择资源节点，勾选测量对象，单击“加入下侧”。
```

## knowledge-016 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对非实时测量任务创建的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-33131b8f0841df928cbd, section-39a3e49702b1eb14879b, section-809076c4afe79e2e32e9, business-topic:产品使用:产品监控 / 网管性能监控 / 非实时测量任务创建
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-b96ae6ea74b429cf717959be`
- 定位：word/document.xml/body/p[349]
```text
产品监控 / 网管性能监控 / 非实时测量任务创建
非实时测量任务创建
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-a4fdd7e54309d2e8191996d3`
- 定位：word/document.xml/body/p[350], word/document.xml/body/p[351], word/document.xml/body/p[353]
```text
网管性能监控 / 非实时测量任务创建 / 功能描述
功能描述
测量任务是一种活动，这个活动允许用户定义需要采集哪些性能数据。网元根据测量任务要求采集相应计数器，网管将采集的计数器入库。
不允许在断链网元上创建非实时测量任务。
```
- 来源：中国联通5G专网UPF产品使用手册(1).docx · `chunk-aa165f4d542aaed2126c07c0`
- 定位：word/document.xml/body/p[354], word/document.xml/body/p[356], word/document.xml/body/p[358], word/document.xml/body/p[360]
```text
网管性能监控 / 非实时测量任务创建 / 功能配置
功能配置
操作步骤：
在菜单栏选择“性能管理 > 5GC性能管理 > 周期测量  > 非实时任务管理> 创建任务”。
在如下图所示的对话框中选择资源节点，勾选测量对象，单击“加入下侧”。
```
- 预期原文/缺口：
```text
产品监控 / 网管性能监控 / 非实时测量任务创建
非实时测量任务创建
网管性能监控 / 非实时测量任务创建 / 功能描述
功能描述
测量任务是一种活动，这个活动允许用户定义需要采集哪些性能数据。网元根据测量任务要求采集相应计数器，网管将采集的计数器入库。
不允许在断链网元上创建非实时测量任务。
网管性能监控 / 非实时测量任务创建 / 功能配置
功能配置
操作步骤：
在菜单栏选择“性能管理 > 5GC性能管理 > 周期测量  > 非实时任务管理> 创建任务”。
在如下图所示的对话框中选择资源节点，勾选测量对象，单击“加入下侧”。
```

## knowledge-017 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，PFCP偶联相关统计有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-18a93cc92c8e44ce6a84, business-topic:网管使用:8 性能管理（Performance Management） / 8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-9efb9ba2dbb5128f6e1afead`
- 定位：word/document.xml/body/p[1405], word/document.xml/body/p[1406], word/document.xml/body/p[1407], word/document.xml/body/p[1409], word/document.xml/body/p[1410]
```text
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
8.2.3.5.1 PFCP Assosication Related Statistics
路径：Manage-->UPF-->Instance-->N4 Node Level Procedures
说明：PFCP关联相关统计
图8.2.3.5.1-1 PFCP Assosication Related Statistics
统计参数及说明：
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-2c200872476871529fb5afd1`
- 定位：word/document.xml/body/tbl[73]/tr[2], word/document.xml/body/tbl[73]/tr[3], word/document.xml/body/tbl[73]/tr[4], word/document.xml/body/tbl[73]/tr[5], word/document.xml/body/tbl[73]/tr[6], word/document.xml/body/tbl[73]/tr[7], word/document.xml/body/tbl[73]/tr[8], word/document.xml/body/tbl[73]/tr[9], word/document.xml/body/tbl[73]/tr[10]
```text
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup request received | 说明：接收的关联建立请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup response sent | 说明：发送的关联建立响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup request sent | 说明：发送的关联建立请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup response received | 说明：接收的关联建立响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update request received | 说明：接收的关联更新请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update response sent | 说明：发送的关联更新响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update request sent | 说明：发送的关联更新请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update response received | 说明：接收的关联更新响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association release request received | 说明：接收的关联释放请求
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-78e6d59650145301b6829492`
- 定位：word/document.xml/body/tbl[73]/tr[11]
```text
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association release response sent | 说明：发送的关联释放响应
```
- 预期原文/缺口：
```text
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
8.2.3.5.1 PFCP Assosication Related Statistics
路径：Manage-->UPF-->Instance-->N4 Node Level Procedures
说明：PFCP关联相关统计
图8.2.3.5.1-1 PFCP Assosication Related Statistics
统计参数及说明：
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup request received | 说明：接收的关联建立请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup response sent | 说明：发送的关联建立响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup request sent | 说明：发送的关联建立请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup response received | 说明：接收的关联建立响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update request received | 说明：接收的关联更新请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update response sent | 说明：发送的关联更新响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update request sent | 说明：发送的关联更新请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update response received | 说明：接收的关联更新响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association release request received | 说明：接收的关联释放请求
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association release response sent | 说明：发送的关联释放响应
```

## knowledge-018 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对PFCP偶联相关统计的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-18a93cc92c8e44ce6a84, business-topic:网管使用:8 性能管理（Performance Management） / 8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-9efb9ba2dbb5128f6e1afead`
- 定位：word/document.xml/body/p[1405], word/document.xml/body/p[1406], word/document.xml/body/p[1407], word/document.xml/body/p[1409], word/document.xml/body/p[1410]
```text
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
8.2.3.5.1 PFCP Assosication Related Statistics
路径：Manage-->UPF-->Instance-->N4 Node Level Procedures
说明：PFCP关联相关统计
图8.2.3.5.1-1 PFCP Assosication Related Statistics
统计参数及说明：
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-2c200872476871529fb5afd1`
- 定位：word/document.xml/body/tbl[73]/tr[2], word/document.xml/body/tbl[73]/tr[3], word/document.xml/body/tbl[73]/tr[4], word/document.xml/body/tbl[73]/tr[5], word/document.xml/body/tbl[73]/tr[6], word/document.xml/body/tbl[73]/tr[7], word/document.xml/body/tbl[73]/tr[8], word/document.xml/body/tbl[73]/tr[9], word/document.xml/body/tbl[73]/tr[10]
```text
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup request received | 说明：接收的关联建立请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup response sent | 说明：发送的关联建立响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup request sent | 说明：发送的关联建立请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup response received | 说明：接收的关联建立响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update request received | 说明：接收的关联更新请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update response sent | 说明：发送的关联更新响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update request sent | 说明：发送的关联更新请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update response received | 说明：接收的关联更新响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association release request received | 说明：接收的关联释放请求
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-78e6d59650145301b6829492`
- 定位：word/document.xml/body/tbl[73]/tr[11]
```text
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association release response sent | 说明：发送的关联释放响应
```
- 预期原文/缺口：
```text
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
8.2.3.5.1 PFCP Assosication Related Statistics
路径：Manage-->UPF-->Instance-->N4 Node Level Procedures
说明：PFCP关联相关统计
图8.2.3.5.1-1 PFCP Assosication Related Statistics
统计参数及说明：
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup request received | 说明：接收的关联建立请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup response sent | 说明：发送的关联建立响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup request sent | 说明：发送的关联建立请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association setup response received | 说明：接收的关联建立响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update request received | 说明：接收的关联更新请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update response sent | 说明：发送的关联更新响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update request sent | 说明：发送的关联更新请求
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association update response received | 说明：接收的关联更新响应
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association release request received | 说明：接收的关联释放请求
8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表格：8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
表头：统计参数	说明
统计参数：association release response sent | 说明：发送的关联释放响应
```

## knowledge-019 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：依据手册原生文字，N4 PFCP心跳统计有哪些说明与适用范围？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-ce439c799639f2a8bce7, section-f1f57c594c3a84a9dd18, business-topic:网管使用:8 性能管理（Performance Management） / 8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-b9f05239e67aab2ee65e914d`
- 定位：word/document.xml/body/p[1480], word/document.xml/body/p[1481], word/document.xml/body/p[1482], word/document.xml/body/p[1484]
```text
8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics
8.2.3.10 N4 PFCP Heartbeat Statistics
路径：Manage-->UPF-->Instance
说明：N4 PFCP心跳统计
图8.2.3.10-1 N4 PFCP Heartbeat Statistics
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-73c091f41c6e45cfb163101d`
- 定位：word/document.xml/body/p[1485], word/document.xml/body/p[1486], word/document.xml/body/p[1487], word/document.xml/body/p[1489], word/document.xml/body/p[1490]
```text
8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
8.2.3.10.1 PFCP Heartbeat
路径：Manage-->UPF-->Instance
说明：统计PFCP心跳
图8.2.3.10.1-1 PFCP Heartbeat 
统计参数及说明：
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-46b4cdde87c2e24460b3c91e`
- 定位：word/document.xml/body/tbl[82]/tr[2], word/document.xml/body/tbl[82]/tr[3], word/document.xml/body/tbl[82]/tr[4], word/document.xml/body/tbl[82]/tr[5]
```text
8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat request received | 说明：接收的心跳请求
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat response sent | 说明：发送的心跳响应
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat request sent | 说明：发送的心跳请求
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat response received | 说明：接收的心跳响应
```
- 预期原文/缺口：
```text
8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics
8.2.3.10 N4 PFCP Heartbeat Statistics
路径：Manage-->UPF-->Instance
说明：N4 PFCP心跳统计
图8.2.3.10-1 N4 PFCP Heartbeat Statistics
8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
8.2.3.10.1 PFCP Heartbeat
路径：Manage-->UPF-->Instance
说明：统计PFCP心跳
图8.2.3.10.1-1 PFCP Heartbeat 
统计参数及说明：
8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat request received | 说明：接收的心跳请求
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat response sent | 说明：发送的心跳响应
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat request sent | 说明：发送的心跳请求
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat response received | 说明：接收的心跳响应
```

## knowledge-020 · heldout · knowledge

- [ ] 问题及预期事实/相关证据已核对
- 问题：请核对手册对N4 PFCP心跳统计的描述，哪些内容有文字依据？仅见截图或缺少字段时说明缺口；不要报告当前现场数值。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-ce439c799639f2a8bce7, section-f1f57c594c3a84a9dd18, business-topic:网管使用:8 性能管理（Performance Management） / 8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-b9f05239e67aab2ee65e914d`
- 定位：word/document.xml/body/p[1480], word/document.xml/body/p[1481], word/document.xml/body/p[1482], word/document.xml/body/p[1484]
```text
8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics
8.2.3.10 N4 PFCP Heartbeat Statistics
路径：Manage-->UPF-->Instance
说明：N4 PFCP心跳统计
图8.2.3.10-1 N4 PFCP Heartbeat Statistics
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-73c091f41c6e45cfb163101d`
- 定位：word/document.xml/body/p[1485], word/document.xml/body/p[1486], word/document.xml/body/p[1487], word/document.xml/body/p[1489], word/document.xml/body/p[1490]
```text
8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
8.2.3.10.1 PFCP Heartbeat
路径：Manage-->UPF-->Instance
说明：统计PFCP心跳
图8.2.3.10.1-1 PFCP Heartbeat 
统计参数及说明：
```
- 来源：5GC网管使用手册_V1.3_20220916(1).docx · `chunk-46b4cdde87c2e24460b3c91e`
- 定位：word/document.xml/body/tbl[82]/tr[2], word/document.xml/body/tbl[82]/tr[3], word/document.xml/body/tbl[82]/tr[4], word/document.xml/body/tbl[82]/tr[5]
```text
8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat request received | 说明：接收的心跳请求
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat response sent | 说明：发送的心跳响应
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat request sent | 说明：发送的心跳请求
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat response received | 说明：接收的心跳响应
```
- 预期原文/缺口：
```text
8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics
8.2.3.10 N4 PFCP Heartbeat Statistics
路径：Manage-->UPF-->Instance
说明：N4 PFCP心跳统计
图8.2.3.10-1 N4 PFCP Heartbeat Statistics
8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
8.2.3.10.1 PFCP Heartbeat
路径：Manage-->UPF-->Instance
说明：统计PFCP心跳
图8.2.3.10.1-1 PFCP Heartbeat 
统计参数及说明：
8.2.3 Manage-UPF / 8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat request received | 说明：接收的心跳请求
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat response sent | 说明：发送的心跳响应
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat request sent | 说明：发送的心跳请求
表格：8.2.3.10 N4 PFCP Heartbeat Statistics / 8.2.3.10.1 PFCP Heartbeat
表头：统计参数	说明
统计参数：heartbeat response received | 说明：接收的心跳响应
```

## troubleshooting-001 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘UPF N4 IPv6 接口地址到 SMF 链路异常’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-052138fa6b7209948c58, section-1a37d889d2b57b41d241, section-88ee61405d61db1669e2, section-e4e0dd252fa75830aae0, business-topic:紧急故障:业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-88c0205f5e807670ef012e91`
- 定位：word/document.xml/body/p[197]
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常
UPF N4 IPv6 接口地址到 SMF 链路异常
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-bd23d314719b6eb0285f9fe0`
- 定位：word/document.xml/body/p[198], word/document.xml/body/p[199], word/document.xml/body/p[200], word/document.xml/body/p[201]
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 症状现象
症状现象
N4偶联无法正常建立；
PDU会话无法正常建立；
执行upfmgr hc命令显示“N4(v6)到SMF链路状态 | Error”
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-56ec8a20dfecb151d3a6e382`
- 定位：word/document.xml/body/p[202], word/document.xml/body/p[203], word/document.xml/body/p[204], word/document.xml/body/p[205]
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 信息收集
信息收集
使用upfmgr bash命令进入pod内部，执行ip a命令查看网卡状态是否正常，可使用ping命令ping自身ip检查自己的ip状态是否正常；
使用ping命令ping对端SMF的N4接口地址ip是否正常响应；
使用ping命令检查到UPF N4网关地址是否正常响应；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7e74615619856c2f3908e60b`
- 定位：word/document.xml/body/p[206], word/document.xml/body/p[207], word/document.xml/body/p[208]
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 解决方法
解决方法
若自身ip状态异常，检查upf N4地址是否正常配置，尝试重启pod后再检查到SMF N4链路是否正常；
若N4对端或交换机网关地址无法ping通，需SMF和交换机检查是否有异常；
```
- 预期原文/缺口：
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常
UPF N4 IPv6 接口地址到 SMF 链路异常
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 症状现象
症状现象
N4偶联无法正常建立；
PDU会话无法正常建立；
执行upfmgr hc命令显示“N4(v6)到SMF链路状态 | Error”
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 信息收集
信息收集
使用upfmgr bash命令进入pod内部，执行ip a命令查看网卡状态是否正常，可使用ping命令ping自身ip检查自己的ip状态是否正常；
使用ping命令ping对端SMF的N4接口地址ip是否正常响应；
使用ping命令检查到UPF N4网关地址是否正常响应；
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 解决方法
解决方法
若自身ip状态异常，检查upf N4地址是否正常配置，尝试重启pod后再检查到SMF N4链路是否正常；
若N4对端或交换机网关地址无法ping通，需SMF和交换机检查是否有异常；
```

## troubleshooting-002 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘UPF N4 IPv6 接口地址到 SMF 链路异常’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-052138fa6b7209948c58, section-1a37d889d2b57b41d241, section-88ee61405d61db1669e2, section-e4e0dd252fa75830aae0, business-topic:紧急故障:业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-88c0205f5e807670ef012e91`
- 定位：word/document.xml/body/p[197]
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常
UPF N4 IPv6 接口地址到 SMF 链路异常
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-bd23d314719b6eb0285f9fe0`
- 定位：word/document.xml/body/p[198], word/document.xml/body/p[199], word/document.xml/body/p[200], word/document.xml/body/p[201]
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 症状现象
症状现象
N4偶联无法正常建立；
PDU会话无法正常建立；
执行upfmgr hc命令显示“N4(v6)到SMF链路状态 | Error”
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-56ec8a20dfecb151d3a6e382`
- 定位：word/document.xml/body/p[202], word/document.xml/body/p[203], word/document.xml/body/p[204], word/document.xml/body/p[205]
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 信息收集
信息收集
使用upfmgr bash命令进入pod内部，执行ip a命令查看网卡状态是否正常，可使用ping命令ping自身ip检查自己的ip状态是否正常；
使用ping命令ping对端SMF的N4接口地址ip是否正常响应；
使用ping命令检查到UPF N4网关地址是否正常响应；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7e74615619856c2f3908e60b`
- 定位：word/document.xml/body/p[206], word/document.xml/body/p[207], word/document.xml/body/p[208]
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 解决方法
解决方法
若自身ip状态异常，检查upf N4地址是否正常配置，尝试重启pod后再检查到SMF N4链路是否正常；
若N4对端或交换机网关地址无法ping通，需SMF和交换机检查是否有异常；
```
- 预期原文/缺口：
```text
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常
UPF N4 IPv6 接口地址到 SMF 链路异常
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 症状现象
症状现象
N4偶联无法正常建立；
PDU会话无法正常建立；
执行upfmgr hc命令显示“N4(v6)到SMF链路状态 | Error”
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 信息收集
信息收集
使用upfmgr bash命令进入pod内部，执行ip a命令查看网卡状态是否正常，可使用ping命令ping自身ip检查自己的ip状态是否正常；
使用ping命令ping对端SMF的N4接口地址ip是否正常响应；
使用ping命令检查到UPF N4网关地址是否正常响应；
业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 解决方法
解决方法
若自身ip状态异常，检查upf N4地址是否正常配置，尝试重启pod后再检查到SMF N4链路是否正常；
若N4对端或交换机网关地址无法ping通，需SMF和交换机检查是否有异常；
```

## troubleshooting-003 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘UPF N6 IPv4 接口地址到网关链路异常’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-12574399cf754e91b178, section-12a1ecf22dd858c128a6, section-77e3fa9e9ad882290342, section-807f62178e1fbbf8d558, business-topic:紧急故障:业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-703fe1689aeab4ea8f5415a2`
- 定位：word/document.xml/body/p[245]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常
UPF N6 IPv4 接口地址到网关链路异常
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-22e28203ca9caea117f61d5c`
- 定位：word/document.xml/body/p[246], word/document.xml/body/p[247], word/document.xml/body/p[248]/txbxContent[1]/p[1], word/document.xml/body/p[248]/txbxContent[1]/p[2], word/document.xml/body/p[249]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
症状现象
执行upfmgr hc命令，显示信息如下：
|  UPF链路状态检测 |                   
|                | N6(v4)到网关链路状态 | Error  |  (N6(v4)网关地址) 
或者通过使用upfmgr data 命令进入 vppctl 控制台，执行 ping N6 网关发现不通。现象如下：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-95b7c2487347d470a1774522`
- 定位：word/document.xml/body/p[250]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
UPF# ping 174.100.100.2
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-5678c401ed05218aec20b7ce`
- 定位：word/document.xml/body/p[250]/txbxContent[1]/p[3]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
Statistics: 5 sent, 0 received, 100% packet loss
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-3a86073cea37c9440d9e705a`
- 定位：word/document.xml/body/p[251], word/document.xml/body/p[252]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
信息收集
使用upfmgr data 命令进入vppctl 控制台，执行show interface addr 命令查看 N6 网卡（一般是BondEthernet1，或者BondEthernet1.400,子接口以具体规划为准）状态地址是否正常：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2240fc70509e9a8763a0d4e8`
- 定位：word/document.xml/body/p[253]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface addr
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-1546fd5d5b8b2e98dbd03e4b`
- 定位：word/document.xml/body/p[253]/txbxContent[1]/p[2], word/document.xml/body/p[253]/txbxContent[1]/p[3], word/document.xml/body/p[253]/txbxContent[1]/p[4], word/document.xml/body/p[253]/txbxContent[1]/p[5], word/document.xml/body/p[253]/txbxContent[1]/p[6], word/document.xml/body/p[253]/txbxContent[1]/p[7], word/document.xml/body/p[253]/txbxContent[1]/p[8], word/document.xml/body/p[253]/txbxContent[1]/p[9], word/document.xml/body/p[253]/txbxContent[1]/p[10], word/document.xml/body/p[253]/txbxContent[1]/p[11], word/document.xml/body/p[253]/txbxContent[1]/p[12], word/document.xml/body/p[253]/txbxContent[1]/p[13], word/document.xml/body/p[253]/txbxContent[1]/p[14], word/document.xml/body/p[253]/txbxContent[1]/p[15], word/document.xml/body/p[253]/txbxContent[1]/p[16], word/document.xml/body/p[253]/txbxContent[1]/p[17], word/document.xml/body/p[254], word/document.xml/body/p[255]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
BondEthernet0 (up):
BondEthernet0.200 (up):
  L3 100.10.1.38/24
  L3 2303::3:38/64
BondEthernet0.900 (up):
  L3 100.10.11.38/24
  L3 2909::9:38/64
BondEthernet1 (up):
BondEthernet1.400 (up):
  L3 174.100.100.38/24
  L3 2606::6:38/64
local0 (dn):
portf4/0/0 (up):
portf4/0/1 (up):
portf4/0/2 (up):
portf4/0/3 (up):
使用ping命令检查到UPF N6网关地址是否正常响应；
使用upfmgr data 命令进入vppctl 控制台，执行show interface  命令查看 2 个网口（ 网口名称以具体配置为准，如port7/0/0，port7/0/1）State 是否正常显示 up：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2002b6d4263f96accd63b771`
- 定位：word/document.xml/body/p[256]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-1a7770ae009e8ef364200ef8`
- 定位：word/document.xml/body/p[256]/txbxContent[1]/p[2], word/document.xml/body/p[256]/txbxContent[1]/p[3], word/document.xml/body/p[256]/txbxContent[1]/p[4], word/document.xml/body/p[256]/txbxContent[1]/p[5], word/document.xml/body/p[256]/txbxContent[1]/p[6], word/document.xml/body/p[256]/txbxContent[1]/p[7], word/document.xml/body/p[256]/txbxContent[1]/p[8], word/document.xml/body/p[256]/txbxContent[1]/p[9], word/document.xml/body/p[256]/txbxContent[1]/p[10], word/document.xml/body/p[256]/txbxContent[1]/p[11], word/document.xml/body/p[256]/txbxContent[1]/p[12], word/document.xml/body/p[256]/txbxContent[1]/p[13], word/document.xml/body/p[256]/txbxContent[1]/p[14], word/document.xml/body/p[256]/txbxContent[1]/p[15], word/document.xml/body/p[256]/txbxContent[1]/p[16], word/document.xml/body/p[256]/txbxContent[1]/p[17], word/document.xml/body/p[256]/txbxContent[1]/p[18], word/document.xml/body/p[256]/txbxContent[1]/p[19], word/document.xml/body/p[256]/txbxContent[1]/p[20], word/document.xml/body/p[256]/txbxContent[1]/p[21], word/document.xml/body/p[256]/txbxContent[1]/p[22], word/document.xml/body/p[256]/txbxContent[1]/p[23], word/document.xml/body/p[256]/txbxContent[1]/p[24], word/document.xml/body/p[256]/txbxContent[1]/p[25], word/document.xml/body/p[256]/txbxContent[1]/p[26], word/document.xml/body/p[257]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
    Name  Idx  State MTU (L3/IP4/IP6/MPLS)  Counter Count
port6/0/0 1  up 1675/0/0/0  rx packets      1389730
                            rx bytes      114226333
                            tx packets        13730
                            tx bytes        1618522
                            drops             11573
                            punt              11566
port6/0/1 2  up 1675/0/0/0  rx packets      2811229
                            rx bytes      245678814
                            tx packets        11982
                            tx bytes        1467152
                            drops             11575
                            punt              11566
port7/0/0 3  up 1675/0/0/0  rx packets      2698128
                            rx bytes      239356698
                            tx packets        12075
                            tx bytes        1470760
                            drops             11573
                            punt              11566
port7/0/1 4  up 1675/0/0/0  rx packets      2218144
                            rx bytes      180309539
                            tx packets        14109
                            tx bytes        1638194
                            drops             11573
                            punt              11566
使用upfmgr data 命令进入vppctl 控制台，执行show bond  命令查看 active members是不是2；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-c98d7fd9e8b5317cd802f1b3`
- 定位：word/document.xml/body/p[258]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show bond
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-042ebaf81748a3e11c344601`
- 定位：word/document.xml/body/p[258]/txbxContent[1]/p[2], word/document.xml/body/p[258]/txbxContent[1]/p[3], word/document.xml/body/p[258]/txbxContent[1]/p[4], word/document.xml/body/p[259]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
interface name   sw_if_index  mode          load balance  active members members
BondEthernet0    5            lacp          l34           2              2
BondEthernet1    6            lacp          l34           2              2
检查/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 有无配N6网关地址。
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-153f077d0acebd6573a938ab`
- 定位：word/document.xml/body/p[260], word/document.xml/body/p[261], word/document.xml/body/p[262], word/document.xml/body/p[263]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 解决方法
解决方法
若检查发现自身ip地址状态异常，首先尝试执行 upfmgr restart 命令重启upfd pod 后再检查到UPF N6网关是否正常；
若检查UPF N6网关地址不通，首先联系交换机运维人员排查交换机接口有无收到 N6接口的数据报文；
若检查发现/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 未配 UPF_N6_GW_IPv4_ADDRES 网关地址，则添加 UPF_N6_GW_IPv4_ADDRES 接口网关地址配置。
```
- 预期原文/缺口：
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常
UPF N6 IPv4 接口地址到网关链路异常
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
症状现象
执行upfmgr hc命令，显示信息如下：
|  UPF链路状态检测 |                   
|                | N6(v4)到网关链路状态 | Error  |  (N6(v4)网关地址) 
或者通过使用upfmgr data 命令进入 vppctl 控制台，执行 ping N6 网关发现不通。现象如下：
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
UPF# ping 174.100.100.2
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
Statistics: 5 sent, 0 received, 100% packet loss
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
信息收集
使用upfmgr data 命令进入vppctl 控制台，执行show interface addr 命令查看 N6 网卡（一般是BondEthernet1，或者BondEthernet1.400,子接口以具体规划为准）状态地址是否正常：
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface addr
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
BondEthernet0 (up):
BondEthernet0.200 (up):
  L3 100.10.1.38/24
  L3 2303::3:38/64
BondEthernet0.900 (up):
  L3 100.10.11.38/24
  L3 2909::9:38/64
BondEthernet1 (up):
BondEthernet1.400 (up):
  L3 174.100.100.38/24
  L3 2606::6:38/64
local0 (dn):
portf4/0/0 (up):
portf4/0/1 (up):
portf4/0/2 (up):
portf4/0/3 (up):
使用ping命令检查到UPF N6网关地址是否正常响应；
使用upfmgr data 命令进入vppctl 控制台，执行show interface  命令查看 2 个网口（ 网口名称以具体配置为准，如port7/0/0，port7/0/1）State 是否正常显示 up：
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
    Name  Idx  State MTU (L3/IP4/IP6/MPLS)  Counter Count
port6/0/0 1  up 1675/0/0/0  rx packets      1389730
                            rx bytes      114226333
                            tx packets        13730
                            tx bytes        1618522
                            drops             11573
                            punt              11566
port6/0/1 2  up 1675/0/0/0  rx packets      2811229
                            rx bytes      245678814
                            tx packets        11982
                            tx bytes        1467152
                            drops             11575
                            punt              11566
port7/0/0 3  up 1675/0/0/0  rx packets      2698128
                            rx bytes      239356698
                            tx packets        12075
                            tx bytes        1470760
                            drops             11573
                            punt              11566
port7/0/1 4  up 1675/0/0/0  rx packets      2218144
                            rx bytes      180309539
                            tx packets        14109
                            tx bytes        1638194
                            drops             11573
                            punt              11566
使用upfmgr data 命令进入vppctl 控制台，执行show bond  命令查看 active members是不是2；
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show bond
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
interface name   sw_if_index  mode          load balance  active members members
BondEthernet0    5            lacp          l34           2              2
BondEthernet1    6            lacp          l34           2              2
检查/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 有无配N6网关地址。
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 解决方法
解决方法
若检查发现自身ip地址状态异常，首先尝试执行 upfmgr restart 命令重启upfd pod 后再检查到UPF N6网关是否正常；
若检查UPF N6网关地址不通，首先联系交换机运维人员排查交换机接口有无收到 N6接口的数据报文；
若检查发现/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 未配 UPF_N6_GW_IPv4_ADDRES 网关地址，则添加 UPF_N6_GW_IPv4_ADDRES 接口网关地址配置。
```

## troubleshooting-004 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘UPF N6 IPv4 接口地址到网关链路异常’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-12574399cf754e91b178, section-12a1ecf22dd858c128a6, section-77e3fa9e9ad882290342, section-807f62178e1fbbf8d558, business-topic:紧急故障:业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-703fe1689aeab4ea8f5415a2`
- 定位：word/document.xml/body/p[245]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常
UPF N6 IPv4 接口地址到网关链路异常
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-22e28203ca9caea117f61d5c`
- 定位：word/document.xml/body/p[246], word/document.xml/body/p[247], word/document.xml/body/p[248]/txbxContent[1]/p[1], word/document.xml/body/p[248]/txbxContent[1]/p[2], word/document.xml/body/p[249]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
症状现象
执行upfmgr hc命令，显示信息如下：
|  UPF链路状态检测 |                   
|                | N6(v4)到网关链路状态 | Error  |  (N6(v4)网关地址) 
或者通过使用upfmgr data 命令进入 vppctl 控制台，执行 ping N6 网关发现不通。现象如下：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-95b7c2487347d470a1774522`
- 定位：word/document.xml/body/p[250]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
UPF# ping 174.100.100.2
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-5678c401ed05218aec20b7ce`
- 定位：word/document.xml/body/p[250]/txbxContent[1]/p[3]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
Statistics: 5 sent, 0 received, 100% packet loss
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-3a86073cea37c9440d9e705a`
- 定位：word/document.xml/body/p[251], word/document.xml/body/p[252]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
信息收集
使用upfmgr data 命令进入vppctl 控制台，执行show interface addr 命令查看 N6 网卡（一般是BondEthernet1，或者BondEthernet1.400,子接口以具体规划为准）状态地址是否正常：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2240fc70509e9a8763a0d4e8`
- 定位：word/document.xml/body/p[253]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface addr
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-1546fd5d5b8b2e98dbd03e4b`
- 定位：word/document.xml/body/p[253]/txbxContent[1]/p[2], word/document.xml/body/p[253]/txbxContent[1]/p[3], word/document.xml/body/p[253]/txbxContent[1]/p[4], word/document.xml/body/p[253]/txbxContent[1]/p[5], word/document.xml/body/p[253]/txbxContent[1]/p[6], word/document.xml/body/p[253]/txbxContent[1]/p[7], word/document.xml/body/p[253]/txbxContent[1]/p[8], word/document.xml/body/p[253]/txbxContent[1]/p[9], word/document.xml/body/p[253]/txbxContent[1]/p[10], word/document.xml/body/p[253]/txbxContent[1]/p[11], word/document.xml/body/p[253]/txbxContent[1]/p[12], word/document.xml/body/p[253]/txbxContent[1]/p[13], word/document.xml/body/p[253]/txbxContent[1]/p[14], word/document.xml/body/p[253]/txbxContent[1]/p[15], word/document.xml/body/p[253]/txbxContent[1]/p[16], word/document.xml/body/p[253]/txbxContent[1]/p[17], word/document.xml/body/p[254], word/document.xml/body/p[255]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
BondEthernet0 (up):
BondEthernet0.200 (up):
  L3 100.10.1.38/24
  L3 2303::3:38/64
BondEthernet0.900 (up):
  L3 100.10.11.38/24
  L3 2909::9:38/64
BondEthernet1 (up):
BondEthernet1.400 (up):
  L3 174.100.100.38/24
  L3 2606::6:38/64
local0 (dn):
portf4/0/0 (up):
portf4/0/1 (up):
portf4/0/2 (up):
portf4/0/3 (up):
使用ping命令检查到UPF N6网关地址是否正常响应；
使用upfmgr data 命令进入vppctl 控制台，执行show interface  命令查看 2 个网口（ 网口名称以具体配置为准，如port7/0/0，port7/0/1）State 是否正常显示 up：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2002b6d4263f96accd63b771`
- 定位：word/document.xml/body/p[256]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-1a7770ae009e8ef364200ef8`
- 定位：word/document.xml/body/p[256]/txbxContent[1]/p[2], word/document.xml/body/p[256]/txbxContent[1]/p[3], word/document.xml/body/p[256]/txbxContent[1]/p[4], word/document.xml/body/p[256]/txbxContent[1]/p[5], word/document.xml/body/p[256]/txbxContent[1]/p[6], word/document.xml/body/p[256]/txbxContent[1]/p[7], word/document.xml/body/p[256]/txbxContent[1]/p[8], word/document.xml/body/p[256]/txbxContent[1]/p[9], word/document.xml/body/p[256]/txbxContent[1]/p[10], word/document.xml/body/p[256]/txbxContent[1]/p[11], word/document.xml/body/p[256]/txbxContent[1]/p[12], word/document.xml/body/p[256]/txbxContent[1]/p[13], word/document.xml/body/p[256]/txbxContent[1]/p[14], word/document.xml/body/p[256]/txbxContent[1]/p[15], word/document.xml/body/p[256]/txbxContent[1]/p[16], word/document.xml/body/p[256]/txbxContent[1]/p[17], word/document.xml/body/p[256]/txbxContent[1]/p[18], word/document.xml/body/p[256]/txbxContent[1]/p[19], word/document.xml/body/p[256]/txbxContent[1]/p[20], word/document.xml/body/p[256]/txbxContent[1]/p[21], word/document.xml/body/p[256]/txbxContent[1]/p[22], word/document.xml/body/p[256]/txbxContent[1]/p[23], word/document.xml/body/p[256]/txbxContent[1]/p[24], word/document.xml/body/p[256]/txbxContent[1]/p[25], word/document.xml/body/p[256]/txbxContent[1]/p[26], word/document.xml/body/p[257]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
    Name  Idx  State MTU (L3/IP4/IP6/MPLS)  Counter Count
port6/0/0 1  up 1675/0/0/0  rx packets      1389730
                            rx bytes      114226333
                            tx packets        13730
                            tx bytes        1618522
                            drops             11573
                            punt              11566
port6/0/1 2  up 1675/0/0/0  rx packets      2811229
                            rx bytes      245678814
                            tx packets        11982
                            tx bytes        1467152
                            drops             11575
                            punt              11566
port7/0/0 3  up 1675/0/0/0  rx packets      2698128
                            rx bytes      239356698
                            tx packets        12075
                            tx bytes        1470760
                            drops             11573
                            punt              11566
port7/0/1 4  up 1675/0/0/0  rx packets      2218144
                            rx bytes      180309539
                            tx packets        14109
                            tx bytes        1638194
                            drops             11573
                            punt              11566
使用upfmgr data 命令进入vppctl 控制台，执行show bond  命令查看 active members是不是2；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-c98d7fd9e8b5317cd802f1b3`
- 定位：word/document.xml/body/p[258]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show bond
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-042ebaf81748a3e11c344601`
- 定位：word/document.xml/body/p[258]/txbxContent[1]/p[2], word/document.xml/body/p[258]/txbxContent[1]/p[3], word/document.xml/body/p[258]/txbxContent[1]/p[4], word/document.xml/body/p[259]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
interface name   sw_if_index  mode          load balance  active members members
BondEthernet0    5            lacp          l34           2              2
BondEthernet1    6            lacp          l34           2              2
检查/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 有无配N6网关地址。
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-153f077d0acebd6573a938ab`
- 定位：word/document.xml/body/p[260], word/document.xml/body/p[261], word/document.xml/body/p[262], word/document.xml/body/p[263]
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 解决方法
解决方法
若检查发现自身ip地址状态异常，首先尝试执行 upfmgr restart 命令重启upfd pod 后再检查到UPF N6网关是否正常；
若检查UPF N6网关地址不通，首先联系交换机运维人员排查交换机接口有无收到 N6接口的数据报文；
若检查发现/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 未配 UPF_N6_GW_IPv4_ADDRES 网关地址，则添加 UPF_N6_GW_IPv4_ADDRES 接口网关地址配置。
```
- 预期原文/缺口：
```text
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常
UPF N6 IPv4 接口地址到网关链路异常
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
症状现象
执行upfmgr hc命令，显示信息如下：
|  UPF链路状态检测 |                   
|                | N6(v4)到网关链路状态 | Error  |  (N6(v4)网关地址) 
或者通过使用upfmgr data 命令进入 vppctl 控制台，执行 ping N6 网关发现不通。现象如下：
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
UPF# ping 174.100.100.2
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 症状现象
Statistics: 5 sent, 0 received, 100% packet loss
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
信息收集
使用upfmgr data 命令进入vppctl 控制台，执行show interface addr 命令查看 N6 网卡（一般是BondEthernet1，或者BondEthernet1.400,子接口以具体规划为准）状态地址是否正常：
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface addr
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
BondEthernet0 (up):
BondEthernet0.200 (up):
  L3 100.10.1.38/24
  L3 2303::3:38/64
BondEthernet0.900 (up):
  L3 100.10.11.38/24
  L3 2909::9:38/64
BondEthernet1 (up):
BondEthernet1.400 (up):
  L3 174.100.100.38/24
  L3 2606::6:38/64
local0 (dn):
portf4/0/0 (up):
portf4/0/1 (up):
portf4/0/2 (up):
portf4/0/3 (up):
使用ping命令检查到UPF N6网关地址是否正常响应；
使用upfmgr data 命令进入vppctl 控制台，执行show interface  命令查看 2 个网口（ 网口名称以具体配置为准，如port7/0/0，port7/0/1）State 是否正常显示 up：
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
    Name  Idx  State MTU (L3/IP4/IP6/MPLS)  Counter Count
port6/0/0 1  up 1675/0/0/0  rx packets      1389730
                            rx bytes      114226333
                            tx packets        13730
                            tx bytes        1618522
                            drops             11573
                            punt              11566
port6/0/1 2  up 1675/0/0/0  rx packets      2811229
                            rx bytes      245678814
                            tx packets        11982
                            tx bytes        1467152
                            drops             11575
                            punt              11566
port7/0/0 3  up 1675/0/0/0  rx packets      2698128
                            rx bytes      239356698
                            tx packets        12075
                            tx bytes        1470760
                            drops             11573
                            punt              11566
port7/0/1 4  up 1675/0/0/0  rx packets      2218144
                            rx bytes      180309539
                            tx packets        14109
                            tx bytes        1638194
                            drops             11573
                            punt              11566
使用upfmgr data 命令进入vppctl 控制台，执行show bond  命令查看 active members是不是2；
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show bond
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
interface name   sw_if_index  mode          load balance  active members members
BondEthernet0    5            lacp          l34           2              2
BondEthernet1    6            lacp          l34           2              2
检查/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 有无配N6网关地址。
业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 解决方法
解决方法
若检查发现自身ip地址状态异常，首先尝试执行 upfmgr restart 命令重启upfd pod 后再检查到UPF N6网关是否正常；
若检查UPF N6网关地址不通，首先联系交换机运维人员排查交换机接口有无收到 N6接口的数据报文；
若检查发现/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 未配 UPF_N6_GW_IPv4_ADDRES 网关地址，则添加 UPF_N6_GW_IPv4_ADDRES 接口网关地址配置。
```

## troubleshooting-005 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘UPF N3 IPv4 接口地址到网关链路异常’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-412c762f06d95a9d94c9, section-812966dcd7dc7ef938a3, section-8a57b94539308f9d3e4b, section-ce0259be2fcf2958e689, business-topic:紧急故障:业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7815e735cbafb014c46fa732`
- 定位：word/document.xml/body/p[225]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常
UPF N3 IPv4 接口地址到网关链路异常
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-004d671c1ea165344b932f7a`
- 定位：word/document.xml/body/p[226], word/document.xml/body/p[227], word/document.xml/body/p[228]/txbxContent[1]/p[1], word/document.xml/body/p[228]/txbxContent[1]/p[2], word/document.xml/body/p[229]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
症状现象
执行upfmgr hc命令，显示信息如下：
|  UPF链路状态检测| 
|               | N3(v4)到网关链路状态 | Error |(N3(v4)网关地址) |
或者通过使用upfmgr data 命令进入 vppctl 控制台，执行 ping N3 网关发现不通。现象如下：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-92686233f5fe392f07b200c5`
- 定位：word/document.xml/body/p[230]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
UPF# ping 100.10.1.11
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-d050aab9aceaea7478f56274`
- 定位：word/document.xml/body/p[230]/txbxContent[1]/p[2], word/document.xml/body/p[230]/txbxContent[1]/p[4]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
Aborted due to a keypress.
Statistics: 5 sent, 0 received, 100% packet loss
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-c8020e9cbc9e7b0161691dd8`
- 定位：word/document.xml/body/p[232], word/document.xml/body/p[233]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
信息收集
使用upfmgr data 命令进入vppctl 控制台，执行show interface addr 命令查看 N3 网卡（一般是BondEthernet0，或者BondEthernet0.200）状态地址是否正常；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7c368ab71b09d9c8ec2524fd`
- 定位：word/document.xml/body/p[234]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface addr
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-bfdcd49335e0e1ce847691ac`
- 定位：word/document.xml/body/p[234]/txbxContent[1]/p[2], word/document.xml/body/p[234]/txbxContent[1]/p[3], word/document.xml/body/p[234]/txbxContent[1]/p[4], word/document.xml/body/p[234]/txbxContent[1]/p[5], word/document.xml/body/p[234]/txbxContent[1]/p[6], word/document.xml/body/p[234]/txbxContent[1]/p[7], word/document.xml/body/p[234]/txbxContent[1]/p[8], word/document.xml/body/p[234]/txbxContent[1]/p[9], word/document.xml/body/p[234]/txbxContent[1]/p[10], word/document.xml/body/p[234]/txbxContent[1]/p[11], word/document.xml/body/p[234]/txbxContent[1]/p[12], word/document.xml/body/p[235], word/document.xml/body/p[236]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
BondEthernet0 (up):
  L3 100.10.1.90/24
  L3 2303::3:90/64
BondEthernet1 (up):
  L3 174.100.100.90/24
  L3 2606::6:90/64
local0 (dn):
port6/0/0 (up):
port6/0/1 (up):
port7/0/0 (up):
port7/0/1 (up):
使用ping命令检查到UPF N3网关地址是否正常响应；
使用upfmgr data 命令进入vppctl 控制台，执行show interface  命令查看 2 个网口（一般是port6/0/0 和 port7/0/0 ）State 是否正常显示 up；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2fa4595ab7676474b59fef33`
- 定位：word/document.xml/body/p[237]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-74ed7e4644572a4ce6e24e90`
- 定位：word/document.xml/body/p[237]/txbxContent[1]/p[2], word/document.xml/body/p[237]/txbxContent[1]/p[3], word/document.xml/body/p[237]/txbxContent[1]/p[4], word/document.xml/body/p[237]/txbxContent[1]/p[5], word/document.xml/body/p[237]/txbxContent[1]/p[6], word/document.xml/body/p[237]/txbxContent[1]/p[7], word/document.xml/body/p[237]/txbxContent[1]/p[8], word/document.xml/body/p[237]/txbxContent[1]/p[9], word/document.xml/body/p[237]/txbxContent[1]/p[10], word/document.xml/body/p[237]/txbxContent[1]/p[11], word/document.xml/body/p[237]/txbxContent[1]/p[12], word/document.xml/body/p[237]/txbxContent[1]/p[13], word/document.xml/body/p[237]/txbxContent[1]/p[14], word/document.xml/body/p[237]/txbxContent[1]/p[15], word/document.xml/body/p[237]/txbxContent[1]/p[16], word/document.xml/body/p[237]/txbxContent[1]/p[17], word/document.xml/body/p[237]/txbxContent[1]/p[18], word/document.xml/body/p[237]/txbxContent[1]/p[19], word/document.xml/body/p[237]/txbxContent[1]/p[20], word/document.xml/body/p[237]/txbxContent[1]/p[21], word/document.xml/body/p[237]/txbxContent[1]/p[22], word/document.xml/body/p[237]/txbxContent[1]/p[23], word/document.xml/body/p[237]/txbxContent[1]/p[24], word/document.xml/body/p[237]/txbxContent[1]/p[25], word/document.xml/body/p[237]/txbxContent[1]/p[26], word/document.xml/body/p[238]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
    Name  Idx  State MTU (L3/IP4/IP6/MPLS)  Counter Count
port6/0/0 1  up 1675/0/0/0  rx packets      1389730
                            rx bytes      114226333
                            tx packets        13730
                            tx bytes        1618522
                            drops             11573
                            punt              11566
port6/0/1 2  up 1675/0/0/0  rx packets      2811229
                            rx bytes      245678814
                            tx packets        11982
                            tx bytes        1467152
                            drops             11575
                            punt              11566
port7/0/0 3  up 1675/0/0/0  rx packets      2698128
                            rx bytes      239356698
                            tx packets        12075
                            tx bytes        1470760
                            drops             11573
                            punt              11566
port7/0/1 4  up 1675/0/0/0  rx packets      2218144
                            rx bytes      180309539
                            tx packets        14109
                            tx bytes        1638194
                            drops             11573
                            punt              11566
使用upfmgr data 命令进入vppctl 控制台，执行show bond  命令查看 active members是不是2；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-a42c683bb266a4df548360e7`
- 定位：word/document.xml/body/p[239]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show bond
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-264fe666fa86924e4f51a7ee`
- 定位：word/document.xml/body/p[239]/txbxContent[1]/p[2], word/document.xml/body/p[239]/txbxContent[1]/p[3], word/document.xml/body/p[239]/txbxContent[1]/p[4], word/document.xml/body/p[240]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
interface name sw_if_index mode load balance active members members
BondEthernet0  5           lacp l34          2           2
BondEthernet1  6           lacp l34          2           2
检查/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 有无配N3网关地址。
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-6357170e31e51f6c05b15696`
- 定位：word/document.xml/body/p[241], word/document.xml/body/p[242], word/document.xml/body/p[243], word/document.xml/body/p[244]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 解决方法
解决方法
若检查发现自身ip地址状态异常，首先尝试执行 upfmgr restart 命令重启upfd pod 后再检查到UPF N3网关是否正常；
若检查UPF N3网关地址不通，首先联系交换机运维人员排查交换机接口有无收到 N4接口的数据报文；
若检查发现/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 未配 UPF_N3_GW_IPv4_ADDRES 地址，则添加 UPF_N3_GW_IPv4_ADDRES 接口地址配置。
```
- 预期原文/缺口：
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常
UPF N3 IPv4 接口地址到网关链路异常
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
症状现象
执行upfmgr hc命令，显示信息如下：
|  UPF链路状态检测| 
|               | N3(v4)到网关链路状态 | Error |(N3(v4)网关地址) |
或者通过使用upfmgr data 命令进入 vppctl 控制台，执行 ping N3 网关发现不通。现象如下：
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
UPF# ping 100.10.1.11
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
Aborted due to a keypress.
Statistics: 5 sent, 0 received, 100% packet loss
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
信息收集
使用upfmgr data 命令进入vppctl 控制台，执行show interface addr 命令查看 N3 网卡（一般是BondEthernet0，或者BondEthernet0.200）状态地址是否正常；
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface addr
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
BondEthernet0 (up):
  L3 100.10.1.90/24
  L3 2303::3:90/64
BondEthernet1 (up):
  L3 174.100.100.90/24
  L3 2606::6:90/64
local0 (dn):
port6/0/0 (up):
port6/0/1 (up):
port7/0/0 (up):
port7/0/1 (up):
使用ping命令检查到UPF N3网关地址是否正常响应；
使用upfmgr data 命令进入vppctl 控制台，执行show interface  命令查看 2 个网口（一般是port6/0/0 和 port7/0/0 ）State 是否正常显示 up；
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
    Name  Idx  State MTU (L3/IP4/IP6/MPLS)  Counter Count
port6/0/0 1  up 1675/0/0/0  rx packets      1389730
                            rx bytes      114226333
                            tx packets        13730
                            tx bytes        1618522
                            drops             11573
                            punt              11566
port6/0/1 2  up 1675/0/0/0  rx packets      2811229
                            rx bytes      245678814
                            tx packets        11982
                            tx bytes        1467152
                            drops             11575
                            punt              11566
port7/0/0 3  up 1675/0/0/0  rx packets      2698128
                            rx bytes      239356698
                            tx packets        12075
                            tx bytes        1470760
                            drops             11573
                            punt              11566
port7/0/1 4  up 1675/0/0/0  rx packets      2218144
                            rx bytes      180309539
                            tx packets        14109
                            tx bytes        1638194
                            drops             11573
                            punt              11566
使用upfmgr data 命令进入vppctl 控制台，执行show bond  命令查看 active members是不是2；
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show bond
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
interface name sw_if_index mode load balance active members members
BondEthernet0  5           lacp l34          2           2
BondEthernet1  6           lacp l34          2           2
检查/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 有无配N3网关地址。
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 解决方法
解决方法
若检查发现自身ip地址状态异常，首先尝试执行 upfmgr restart 命令重启upfd pod 后再检查到UPF N3网关是否正常；
若检查UPF N3网关地址不通，首先联系交换机运维人员排查交换机接口有无收到 N4接口的数据报文；
若检查发现/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 未配 UPF_N3_GW_IPv4_ADDRES 地址，则添加 UPF_N3_GW_IPv4_ADDRES 接口地址配置。
```

## troubleshooting-006 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘UPF N3 IPv4 接口地址到网关链路异常’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-412c762f06d95a9d94c9, section-812966dcd7dc7ef938a3, section-8a57b94539308f9d3e4b, section-ce0259be2fcf2958e689, business-topic:紧急故障:业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7815e735cbafb014c46fa732`
- 定位：word/document.xml/body/p[225]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常
UPF N3 IPv4 接口地址到网关链路异常
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-004d671c1ea165344b932f7a`
- 定位：word/document.xml/body/p[226], word/document.xml/body/p[227], word/document.xml/body/p[228]/txbxContent[1]/p[1], word/document.xml/body/p[228]/txbxContent[1]/p[2], word/document.xml/body/p[229]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
症状现象
执行upfmgr hc命令，显示信息如下：
|  UPF链路状态检测| 
|               | N3(v4)到网关链路状态 | Error |(N3(v4)网关地址) |
或者通过使用upfmgr data 命令进入 vppctl 控制台，执行 ping N3 网关发现不通。现象如下：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-92686233f5fe392f07b200c5`
- 定位：word/document.xml/body/p[230]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
UPF# ping 100.10.1.11
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-d050aab9aceaea7478f56274`
- 定位：word/document.xml/body/p[230]/txbxContent[1]/p[2], word/document.xml/body/p[230]/txbxContent[1]/p[4]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
Aborted due to a keypress.
Statistics: 5 sent, 0 received, 100% packet loss
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-c8020e9cbc9e7b0161691dd8`
- 定位：word/document.xml/body/p[232], word/document.xml/body/p[233]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
信息收集
使用upfmgr data 命令进入vppctl 控制台，执行show interface addr 命令查看 N3 网卡（一般是BondEthernet0，或者BondEthernet0.200）状态地址是否正常；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7c368ab71b09d9c8ec2524fd`
- 定位：word/document.xml/body/p[234]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface addr
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-bfdcd49335e0e1ce847691ac`
- 定位：word/document.xml/body/p[234]/txbxContent[1]/p[2], word/document.xml/body/p[234]/txbxContent[1]/p[3], word/document.xml/body/p[234]/txbxContent[1]/p[4], word/document.xml/body/p[234]/txbxContent[1]/p[5], word/document.xml/body/p[234]/txbxContent[1]/p[6], word/document.xml/body/p[234]/txbxContent[1]/p[7], word/document.xml/body/p[234]/txbxContent[1]/p[8], word/document.xml/body/p[234]/txbxContent[1]/p[9], word/document.xml/body/p[234]/txbxContent[1]/p[10], word/document.xml/body/p[234]/txbxContent[1]/p[11], word/document.xml/body/p[234]/txbxContent[1]/p[12], word/document.xml/body/p[235], word/document.xml/body/p[236]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
BondEthernet0 (up):
  L3 100.10.1.90/24
  L3 2303::3:90/64
BondEthernet1 (up):
  L3 174.100.100.90/24
  L3 2606::6:90/64
local0 (dn):
port6/0/0 (up):
port6/0/1 (up):
port7/0/0 (up):
port7/0/1 (up):
使用ping命令检查到UPF N3网关地址是否正常响应；
使用upfmgr data 命令进入vppctl 控制台，执行show interface  命令查看 2 个网口（一般是port6/0/0 和 port7/0/0 ）State 是否正常显示 up；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2fa4595ab7676474b59fef33`
- 定位：word/document.xml/body/p[237]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-74ed7e4644572a4ce6e24e90`
- 定位：word/document.xml/body/p[237]/txbxContent[1]/p[2], word/document.xml/body/p[237]/txbxContent[1]/p[3], word/document.xml/body/p[237]/txbxContent[1]/p[4], word/document.xml/body/p[237]/txbxContent[1]/p[5], word/document.xml/body/p[237]/txbxContent[1]/p[6], word/document.xml/body/p[237]/txbxContent[1]/p[7], word/document.xml/body/p[237]/txbxContent[1]/p[8], word/document.xml/body/p[237]/txbxContent[1]/p[9], word/document.xml/body/p[237]/txbxContent[1]/p[10], word/document.xml/body/p[237]/txbxContent[1]/p[11], word/document.xml/body/p[237]/txbxContent[1]/p[12], word/document.xml/body/p[237]/txbxContent[1]/p[13], word/document.xml/body/p[237]/txbxContent[1]/p[14], word/document.xml/body/p[237]/txbxContent[1]/p[15], word/document.xml/body/p[237]/txbxContent[1]/p[16], word/document.xml/body/p[237]/txbxContent[1]/p[17], word/document.xml/body/p[237]/txbxContent[1]/p[18], word/document.xml/body/p[237]/txbxContent[1]/p[19], word/document.xml/body/p[237]/txbxContent[1]/p[20], word/document.xml/body/p[237]/txbxContent[1]/p[21], word/document.xml/body/p[237]/txbxContent[1]/p[22], word/document.xml/body/p[237]/txbxContent[1]/p[23], word/document.xml/body/p[237]/txbxContent[1]/p[24], word/document.xml/body/p[237]/txbxContent[1]/p[25], word/document.xml/body/p[237]/txbxContent[1]/p[26], word/document.xml/body/p[238]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
    Name  Idx  State MTU (L3/IP4/IP6/MPLS)  Counter Count
port6/0/0 1  up 1675/0/0/0  rx packets      1389730
                            rx bytes      114226333
                            tx packets        13730
                            tx bytes        1618522
                            drops             11573
                            punt              11566
port6/0/1 2  up 1675/0/0/0  rx packets      2811229
                            rx bytes      245678814
                            tx packets        11982
                            tx bytes        1467152
                            drops             11575
                            punt              11566
port7/0/0 3  up 1675/0/0/0  rx packets      2698128
                            rx bytes      239356698
                            tx packets        12075
                            tx bytes        1470760
                            drops             11573
                            punt              11566
port7/0/1 4  up 1675/0/0/0  rx packets      2218144
                            rx bytes      180309539
                            tx packets        14109
                            tx bytes        1638194
                            drops             11573
                            punt              11566
使用upfmgr data 命令进入vppctl 控制台，执行show bond  命令查看 active members是不是2；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-a42c683bb266a4df548360e7`
- 定位：word/document.xml/body/p[239]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show bond
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-264fe666fa86924e4f51a7ee`
- 定位：word/document.xml/body/p[239]/txbxContent[1]/p[2], word/document.xml/body/p[239]/txbxContent[1]/p[3], word/document.xml/body/p[239]/txbxContent[1]/p[4], word/document.xml/body/p[240]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
interface name sw_if_index mode load balance active members members
BondEthernet0  5           lacp l34          2           2
BondEthernet1  6           lacp l34          2           2
检查/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 有无配N3网关地址。
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-6357170e31e51f6c05b15696`
- 定位：word/document.xml/body/p[241], word/document.xml/body/p[242], word/document.xml/body/p[243], word/document.xml/body/p[244]
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 解决方法
解决方法
若检查发现自身ip地址状态异常，首先尝试执行 upfmgr restart 命令重启upfd pod 后再检查到UPF N3网关是否正常；
若检查UPF N3网关地址不通，首先联系交换机运维人员排查交换机接口有无收到 N4接口的数据报文；
若检查发现/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 未配 UPF_N3_GW_IPv4_ADDRES 地址，则添加 UPF_N3_GW_IPv4_ADDRES 接口地址配置。
```
- 预期原文/缺口：
```text
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常
UPF N3 IPv4 接口地址到网关链路异常
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
症状现象
执行upfmgr hc命令，显示信息如下：
|  UPF链路状态检测| 
|               | N3(v4)到网关链路状态 | Error |(N3(v4)网关地址) |
或者通过使用upfmgr data 命令进入 vppctl 控制台，执行 ping N3 网关发现不通。现象如下：
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
UPF# ping 100.10.1.11
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 症状现象
Aborted due to a keypress.
Statistics: 5 sent, 0 received, 100% packet loss
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
信息收集
使用upfmgr data 命令进入vppctl 控制台，执行show interface addr 命令查看 N3 网卡（一般是BondEthernet0，或者BondEthernet0.200）状态地址是否正常；
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface addr
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
BondEthernet0 (up):
  L3 100.10.1.90/24
  L3 2303::3:90/64
BondEthernet1 (up):
  L3 174.100.100.90/24
  L3 2606::6:90/64
local0 (dn):
port6/0/0 (up):
port6/0/1 (up):
port7/0/0 (up):
port7/0/1 (up):
使用ping命令检查到UPF N3网关地址是否正常响应；
使用upfmgr data 命令进入vppctl 控制台，执行show interface  命令查看 2 个网口（一般是port6/0/0 和 port7/0/0 ）State 是否正常显示 up；
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show interface
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
    Name  Idx  State MTU (L3/IP4/IP6/MPLS)  Counter Count
port6/0/0 1  up 1675/0/0/0  rx packets      1389730
                            rx bytes      114226333
                            tx packets        13730
                            tx bytes        1618522
                            drops             11573
                            punt              11566
port6/0/1 2  up 1675/0/0/0  rx packets      2811229
                            rx bytes      245678814
                            tx packets        11982
                            tx bytes        1467152
                            drops             11575
                            punt              11566
port7/0/0 3  up 1675/0/0/0  rx packets      2698128
                            rx bytes      239356698
                            tx packets        12075
                            tx bytes        1470760
                            drops             11573
                            punt              11566
port7/0/1 4  up 1675/0/0/0  rx packets      2218144
                            rx bytes      180309539
                            tx packets        14109
                            tx bytes        1638194
                            drops             11573
                            punt              11566
使用upfmgr data 命令进入vppctl 控制台，执行show bond  命令查看 active members是不是2；
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
UPF# show bond
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 信息收集
interface name sw_if_index mode load balance active members members
BondEthernet0  5           lacp l34          2           2
BondEthernet1  6           lacp l34          2           2
检查/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 有无配N3网关地址。
业务故障案例 / UPF N3 IPv4 接口地址到网关链路异常 / 解决方法
解决方法
若检查发现自身ip地址状态异常，首先尝试执行 upfmgr restart 命令重启upfd pod 后再检查到UPF N3网关是否正常；
若检查UPF N3网关地址不通，首先联系交换机运维人员排查交换机接口有无收到 N4接口的数据报文；
若检查发现/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 未配 UPF_N3_GW_IPv4_ADDRES 地址，则添加 UPF_N3_GW_IPv4_ADDRES 接口地址配置。
```

## troubleshooting-007 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘UPF（4.0版本）upfd pod一直crash：未安装license’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-64a20dd563146c1dab36, section-9f412ceb7fbbc38d3090, section-c84e169233e05a8d2dab, section-d327b5e36e28fe924da0, business-topic:紧急故障:业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7b5bd200c4c96234acd107e8`
- 定位：word/document.xml/body/p[82]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license
UPF（4.0版本）upfd pod一直crash：未安装license
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-bdfa88a3e63bee30063275ec`
- 定位：word/document.xml/body/p[83], word/document.xml/body/p[84]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 症状现象
症状现象
UPF（4.0版本）刚部署好时upfd pod一直crash。
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-156f762806db57a9c62dfb90`
- 定位：word/document.xml/body/p[85], word/document.xml/body/p[86], word/document.xml/body/p[87], word/document.xml/body/p[88], word/document.xml/body/p[89]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
信息收集
检查现网节点/tmp/目录下是否存在lic文件
若不存在则需重新制作license授权
备注：若/tmp/serialnum文件不存在，请执行echo -n `dmidecode -s  system-uuid` > /tmp/serialnum
执行下列命令使license文件固化：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-ca21cf9c87ac143153a9967b`
- 定位：word/document.xml/body/p[90]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
echo "x /tmp/lic"  >> /usr/lib/tmpfiles.d/tmp.conf
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-4cca01344e96ea3199a3e0c5`
- 定位：word/document.xml/body/p[91]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
执行上述命令后，检查/usr/lib/tmpfiles.d/tmp.conf文件是否已经在末尾添加x /tmp/lic
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-520ee6deca63c8e267efb779`
- 定位：word/document.xml/body/p[93], word/document.xml/body/p[94], word/document.xml/body/p[95]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 解决方法
解决方法
重新进行license授权。
重启upfd pod。
```
- 预期原文/缺口：
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license
UPF（4.0版本）upfd pod一直crash：未安装license
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 症状现象
症状现象
UPF（4.0版本）刚部署好时upfd pod一直crash。
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
信息收集
检查现网节点/tmp/目录下是否存在lic文件
若不存在则需重新制作license授权
备注：若/tmp/serialnum文件不存在，请执行echo -n `dmidecode -s  system-uuid` > /tmp/serialnum
执行下列命令使license文件固化：
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
echo "x /tmp/lic"  >> /usr/lib/tmpfiles.d/tmp.conf
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
执行上述命令后，检查/usr/lib/tmpfiles.d/tmp.conf文件是否已经在末尾添加x /tmp/lic
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 解决方法
解决方法
重新进行license授权。
重启upfd pod。
```

## troubleshooting-008 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘UPF（4.0版本）upfd pod一直crash：未安装license’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-64a20dd563146c1dab36, section-9f412ceb7fbbc38d3090, section-c84e169233e05a8d2dab, section-d327b5e36e28fe924da0, business-topic:紧急故障:业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7b5bd200c4c96234acd107e8`
- 定位：word/document.xml/body/p[82]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license
UPF（4.0版本）upfd pod一直crash：未安装license
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-bdfa88a3e63bee30063275ec`
- 定位：word/document.xml/body/p[83], word/document.xml/body/p[84]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 症状现象
症状现象
UPF（4.0版本）刚部署好时upfd pod一直crash。
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-156f762806db57a9c62dfb90`
- 定位：word/document.xml/body/p[85], word/document.xml/body/p[86], word/document.xml/body/p[87], word/document.xml/body/p[88], word/document.xml/body/p[89]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
信息收集
检查现网节点/tmp/目录下是否存在lic文件
若不存在则需重新制作license授权
备注：若/tmp/serialnum文件不存在，请执行echo -n `dmidecode -s  system-uuid` > /tmp/serialnum
执行下列命令使license文件固化：
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-ca21cf9c87ac143153a9967b`
- 定位：word/document.xml/body/p[90]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
echo "x /tmp/lic"  >> /usr/lib/tmpfiles.d/tmp.conf
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-4cca01344e96ea3199a3e0c5`
- 定位：word/document.xml/body/p[91]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
执行上述命令后，检查/usr/lib/tmpfiles.d/tmp.conf文件是否已经在末尾添加x /tmp/lic
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-520ee6deca63c8e267efb779`
- 定位：word/document.xml/body/p[93], word/document.xml/body/p[94], word/document.xml/body/p[95]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 解决方法
解决方法
重新进行license授权。
重启upfd pod。
```
- 预期原文/缺口：
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license
UPF（4.0版本）upfd pod一直crash：未安装license
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 症状现象
症状现象
UPF（4.0版本）刚部署好时upfd pod一直crash。
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
信息收集
检查现网节点/tmp/目录下是否存在lic文件
若不存在则需重新制作license授权
备注：若/tmp/serialnum文件不存在，请执行echo -n `dmidecode -s  system-uuid` > /tmp/serialnum
执行下列命令使license文件固化：
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
echo "x /tmp/lic"  >> /usr/lib/tmpfiles.d/tmp.conf
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 信息收集
执行上述命令后，检查/usr/lib/tmpfiles.d/tmp.conf文件是否已经在末尾添加x /tmp/lic
业务故障案例 / UPF（4.0版本）upfd pod一直crash：未安装license / 解决方法
解决方法
重新进行license授权。
重启upfd pod。
```

## troubleshooting-009 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘upfmgr n4switch后重启upfd pod一直crash’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-1f71a1bc3f17ec0915ba, section-82c5de38187093acfbe5, section-b96d52ec54421084d231, section-cfe63329be77f694298e, business-topic:紧急故障:业务故障案例 / upfmgr n4switch后重启upfd pod一直crash
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-0bf88640726a3778e29533dc`
- 定位：word/document.xml/body/p[146]
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash
upfmgr n4switch后重启upfd pod一直crash
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-64c5b4db5fb15b57f541b2bf`
- 定位：word/document.xml/body/p[147], word/document.xml/body/p[148], word/document.xml/body/p[149]
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 症状现象
症状现象
upfmgr n4switch前后upfd pod正常
重启upfd pod就一直crash，但没有corefile
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-9ff8a4a83edc72192c0a533b`
- 定位：word/document.xml/body/p[151]
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 3.5.2. 信息收集
3.5.2.  信息收集
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7b450ca543c0f7a82e53559d`
- 定位：word/document.xml/body/p[153], word/document.xml/body/p[154], word/document.xml/body/p[155]/txbxContent[1]/p[1], word/document.xml/body/p[155]/txbxContent[1]/p[2], word/document.xml/body/p[155]/txbxContent[1]/p[3]
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 3.5.3. 解决方法
3.5.3.  解决方法
重启前备份好vpp配置文件重启后恢复时拷贝回去。
/opt/5gc/upfd/etc/vpp/index
/opt/5gc/upfd/etc/vpp/intf 
/opt/5gc/upfd/etc/vpp/startup.conf 
```
- 预期原文/缺口：
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash
upfmgr n4switch后重启upfd pod一直crash
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 症状现象
症状现象
upfmgr n4switch前后upfd pod正常
重启upfd pod就一直crash，但没有corefile
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 3.5.2. 信息收集
3.5.2.  信息收集
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 3.5.3. 解决方法
3.5.3.  解决方法
重启前备份好vpp配置文件重启后恢复时拷贝回去。
/opt/5gc/upfd/etc/vpp/index
/opt/5gc/upfd/etc/vpp/intf 
/opt/5gc/upfd/etc/vpp/startup.conf 
```

## troubleshooting-010 · dev · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘upfmgr n4switch后重启upfd pod一直crash’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-1f71a1bc3f17ec0915ba, section-82c5de38187093acfbe5, section-b96d52ec54421084d231, section-cfe63329be77f694298e, business-topic:紧急故障:业务故障案例 / upfmgr n4switch后重启upfd pod一直crash
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-0bf88640726a3778e29533dc`
- 定位：word/document.xml/body/p[146]
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash
upfmgr n4switch后重启upfd pod一直crash
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-64c5b4db5fb15b57f541b2bf`
- 定位：word/document.xml/body/p[147], word/document.xml/body/p[148], word/document.xml/body/p[149]
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 症状现象
症状现象
upfmgr n4switch前后upfd pod正常
重启upfd pod就一直crash，但没有corefile
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-9ff8a4a83edc72192c0a533b`
- 定位：word/document.xml/body/p[151]
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 3.5.2. 信息收集
3.5.2.  信息收集
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-7b450ca543c0f7a82e53559d`
- 定位：word/document.xml/body/p[153], word/document.xml/body/p[154], word/document.xml/body/p[155]/txbxContent[1]/p[1], word/document.xml/body/p[155]/txbxContent[1]/p[2], word/document.xml/body/p[155]/txbxContent[1]/p[3]
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 3.5.3. 解决方法
3.5.3.  解决方法
重启前备份好vpp配置文件重启后恢复时拷贝回去。
/opt/5gc/upfd/etc/vpp/index
/opt/5gc/upfd/etc/vpp/intf 
/opt/5gc/upfd/etc/vpp/startup.conf 
```
- 预期原文/缺口：
```text
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash
upfmgr n4switch后重启upfd pod一直crash
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 症状现象
症状现象
upfmgr n4switch前后upfd pod正常
重启upfd pod就一直crash，但没有corefile
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 3.5.2. 信息收集
3.5.2.  信息收集
业务故障案例 / upfmgr n4switch后重启upfd pod一直crash / 3.5.3. 解决方法
3.5.3.  解决方法
重启前备份好vpp配置文件重启后恢复时拷贝回去。
/opt/5gc/upfd/etc/vpp/index
/opt/5gc/upfd/etc/vpp/intf 
/opt/5gc/upfd/etc/vpp/startup.conf 
```

## troubleshooting-011 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘upf pod都是pending状态’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-6c3970a64219c820317f, section-7f322ad94ea389dd5a8e, section-96852b28457bed09b5ca, section-d494a7abc85e3c903421, business-topic:紧急故障:系统平台故障案例 / upf pod都是pending状态
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-3a02b72827b1cd6b343b0c39`
- 定位：word/document.xml/body/p[42]
```text
系统平台故障案例 / upf pod都是pending状态
upf pod都是pending状态
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-157f73cf35db89f9ebf53505`
- 定位：word/document.xml/body/p[43], word/document.xml/body/p[44], word/document.xml/body/p[45]/txbxContent[1]/p[1], word/document.xml/body/p[45]/txbxContent[1]/p[2], word/document.xml/body/p[45]/txbxContent[1]/p[3], word/document.xml/body/p[45]/txbxContent[1]/p[4], word/document.xml/body/p[45]/txbxContent[1]/p[5], word/document.xml/body/p[45]/txbxContent[1]/p[6], word/document.xml/body/p[45]/txbxContent[1]/p[7], word/document.xml/body/p[45]/txbxContent[1]/p[8], word/document.xml/body/p[45]/txbxContent[1]/p[9], word/document.xml/body/p[45]/txbxContent[1]/p[10], word/document.xml/body/p[45]/txbxContent[1]/p[11], word/document.xml/body/p[45]/txbxContent[1]/p[12], word/document.xml/body/p[45]/txbxContent[1]/p[13], word/document.xml/body/p[45]/txbxContent[1]/p[14], word/document.xml/body/p[45]/txbxContent[1]/p[15], word/document.xml/body/p[45]/txbxContent[1]/p[16], word/document.xml/body/p[45]/txbxContent[1]/p[17], word/document.xml/body/p[45]/txbxContent[1]/p[18]
```text
系统平台故障案例 / upf pod都是pending状态 / 症状现象
症状现象
k8s pod都正常，但是upf pod都是pending状态
# kubectl get pods -A
NAMESPACE          NAME                                                  READY   STATUS    RESTARTS   AGE
calico-apiserver   calico-apiserver-567cd488c9-84bvl                     1/1     Running   0          58m
calico-apiserver   calico-apiserver-567cd488c9-kr446                     1/1     Running   0          58m
calico-system      calico-kube-controllers-69fd7cf568-scdcc              1/1     Running   0          59m
calico-system      calico-node-x47q4                                     1/1     Running   0          59m
calico-system      calico-typha-6ffb8b6566-z8sjp                         1/1     Running   0          59m
calico-system      csi-node-driver-tr42h                                 2/2     Running   0          59m
ingress-nginx      ingress-nginx-controller-tvtzz                        1/1     Running   0          57m
kube-system        coredns-565d847f94-57b9r                              1/1     Running   0          59m
kube-system        coredns-565d847f94-lt5xv                              1/1     Running   0          59m
kube-system        etcd-cq-na-vivo-upf01                                 1/1     Running   0          59m
kube-system        kube-apiserver-cq-na-vivo-upf01                       1/1     Running   0          59m
kube-system        kube-controller-manager-cq-na-vivo-upf01              1/1     Running   0          59m
kube-system        kube-multus-ds-mhn7n                                  1/1     Running   0          56m
kube-system        kube-proxy-q8f7g                                      1/1     Running   0          59m
kube-system        kube-scheduler-cq-na-vivo-upf01                       1/1     Running   0          59m
kube-system        metrics-server-56997495d6-69tfx                       1/1     Running   0          56m
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-98fd28a83efb5875db69122f`
- 定位：word/document.xml/body/p[45]/txbxContent[1]/p[19], word/document.xml/body/p[45]/txbxContent[1]/p[20], word/document.xml/body/p[45]/txbxContent[1]/p[21], word/document.xml/body/p[45]/txbxContent[1]/p[22], word/document.xml/body/p[45]/txbxContent[1]/p[23], word/document.xml/body/p[45]/txbxContent[1]/p[24], word/document.xml/body/p[45]/txbxContent[1]/p[25], word/document.xml/body/p[45]/txbxContent[1]/p[26], word/document.xml/body/p[45]/txbxContent[1]/p[27], word/document.xml/body/p[45]/txbxContent[1]/p[28], word/document.xml/body/p[45]/txbxContent[1]/p[29], word/document.xml/body/p[45]/txbxContent[1]/p[30], word/document.xml/body/p[45]/txbxContent[1]/p[31], word/document.xml/body/p[45]/txbxContent[1]/p[32], word/document.xml/body/p[45]/txbxContent[1]/p[33]
```text
系统平台故障案例 / upf pod都是pending状态 / 症状现象
loki               promtail-rflqp                                        1/1     Running   0          56m
monitoring         prometheus-kube-prometheus-operator-5dc779f7c-26jkb   1/1     Running   0          57m
monitoring         prometheus-kube-state-metrics-9bc7f5984-w2chr         1/1     Running   0          57m
monitoring         prometheus-prometheus-kube-prometheus-prometheus-0    2/2     Running   0          57m
monitoring         prometheus-prometheus-node-exporter-b7kvv             1/1     Running   0          57m
nfs-provisioner    nfs-subdir-external-provisioner-697499d6d7-ncqjd      1/1     Running   0          58m
ns1                upf-1-oam-main-5999cb46c6-chmlp                       0/4     Pending   0          11m
ns1                upf-1-oam-nma-588fc4dff5-wqlpc                        0/1     Pending   0          11m
ns1                upf-1-oam-redis-0                                     0/2     Pending   0          11m
ns1                upf-1-oam-res-ns1-cu5gcupf5.0.0-zz2tm                 0/1     Pending   0          11m
ns1                upfd-1-746b47984d-s4bc5                               0/1     Pending   0          11m
ns1                upfe-1-765557df66-gphwm                               0/1     Pending   0          11m
ns1                upfm-1-754b744dfc-wlg8f                               0/1     Pending   0          11m
ns1                vdos-etcd-0                                           0/1     Pending   0          11m
ns1                vdos-server-577f4c9554-sgsfb                          0/1     Pending   0          11m
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-a1de3f7c22f6b1bc510422ac`
- 定位：word/document.xml/body/p[46], word/document.xml/body/p[47], word/document.xml/body/p[49]/txbxContent[1]/p[1], word/document.xml/body/p[49]/txbxContent[1]/p[2], word/document.xml/body/p[49]/txbxContent[1]/p[3], word/document.xml/body/p[49]/txbxContent[1]/p[4], word/document.xml/body/p[50], word/document.xml/body/p[51]/txbxContent[1]/p[1], word/document.xml/body/p[51]/txbxContent[1]/p[2], word/document.xml/body/p[51]/txbxContent[1]/p[3]
```text
系统平台故障案例 / upf pod都是pending状态 / 信息收集
信息收集
describe pod提示node不存在
Events:
  Type     Reason            Age    From               Message
  ----     ------            ----   ----               -------
  Warning  FailedScheduling  3m20s  default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {node.kubernetes.io/unreachable: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
查看pod发现是主机名(upf02)与node名(upf01)不一致。通常因为装完k8s后改过节点名字。
root@upf02:~# kubectl get node -A
NAME               STATUS     ROLES           AGE   VERSION
upf01   NotReady   control-plane   59m   v1.25.11
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-14d484ec2e21c87c583fbb7e`
- 定位：word/document.xml/body/p[52], word/document.xml/body/p[53]
```text
系统平台故障案例 / upf pod都是pending状态 / 解决办法
解决办法
修改k8s配置文件保持与主机名一致后重装k8s。
```
- 预期原文/缺口：
```text
系统平台故障案例 / upf pod都是pending状态
upf pod都是pending状态
系统平台故障案例 / upf pod都是pending状态 / 症状现象
症状现象
k8s pod都正常，但是upf pod都是pending状态
# kubectl get pods -A
NAMESPACE          NAME                                                  READY   STATUS    RESTARTS   AGE
calico-apiserver   calico-apiserver-567cd488c9-84bvl                     1/1     Running   0          58m
calico-apiserver   calico-apiserver-567cd488c9-kr446                     1/1     Running   0          58m
calico-system      calico-kube-controllers-69fd7cf568-scdcc              1/1     Running   0          59m
calico-system      calico-node-x47q4                                     1/1     Running   0          59m
calico-system      calico-typha-6ffb8b6566-z8sjp                         1/1     Running   0          59m
calico-system      csi-node-driver-tr42h                                 2/2     Running   0          59m
ingress-nginx      ingress-nginx-controller-tvtzz                        1/1     Running   0          57m
kube-system        coredns-565d847f94-57b9r                              1/1     Running   0          59m
kube-system        coredns-565d847f94-lt5xv                              1/1     Running   0          59m
kube-system        etcd-cq-na-vivo-upf01                                 1/1     Running   0          59m
kube-system        kube-apiserver-cq-na-vivo-upf01                       1/1     Running   0          59m
kube-system        kube-controller-manager-cq-na-vivo-upf01              1/1     Running   0          59m
kube-system        kube-multus-ds-mhn7n                                  1/1     Running   0          56m
kube-system        kube-proxy-q8f7g                                      1/1     Running   0          59m
kube-system        kube-scheduler-cq-na-vivo-upf01                       1/1     Running   0          59m
kube-system        metrics-server-56997495d6-69tfx                       1/1     Running   0          56m
系统平台故障案例 / upf pod都是pending状态 / 症状现象
loki               promtail-rflqp                                        1/1     Running   0          56m
monitoring         prometheus-kube-prometheus-operator-5dc779f7c-26jkb   1/1     Running   0          57m
monitoring         prometheus-kube-state-metrics-9bc7f5984-w2chr         1/1     Running   0          57m
monitoring         prometheus-prometheus-kube-prometheus-prometheus-0    2/2     Running   0          57m
monitoring         prometheus-prometheus-node-exporter-b7kvv             1/1     Running   0          57m
nfs-provisioner    nfs-subdir-external-provisioner-697499d6d7-ncqjd      1/1     Running   0          58m
ns1                upf-1-oam-main-5999cb46c6-chmlp                       0/4     Pending   0          11m
ns1                upf-1-oam-nma-588fc4dff5-wqlpc                        0/1     Pending   0          11m
ns1                upf-1-oam-redis-0                                     0/2     Pending   0          11m
ns1                upf-1-oam-res-ns1-cu5gcupf5.0.0-zz2tm                 0/1     Pending   0          11m
ns1                upfd-1-746b47984d-s4bc5                               0/1     Pending   0          11m
ns1                upfe-1-765557df66-gphwm                               0/1     Pending   0          11m
ns1                upfm-1-754b744dfc-wlg8f                               0/1     Pending   0          11m
ns1                vdos-etcd-0                                           0/1     Pending   0          11m
ns1                vdos-server-577f4c9554-sgsfb                          0/1     Pending   0          11m
系统平台故障案例 / upf pod都是pending状态 / 信息收集
信息收集
describe pod提示node不存在
Events:
  Type     Reason            Age    From               Message
  ----     ------            ----   ----               -------
  Warning  FailedScheduling  3m20s  default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {node.kubernetes.io/unreachable: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
查看pod发现是主机名(upf02)与node名(upf01)不一致。通常因为装完k8s后改过节点名字。
root@upf02:~# kubectl get node -A
NAME               STATUS     ROLES           AGE   VERSION
upf01   NotReady   control-plane   59m   v1.25.11
系统平台故障案例 / upf pod都是pending状态 / 解决办法
解决办法
修改k8s配置文件保持与主机名一致后重装k8s。
```

## troubleshooting-012 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘upf pod都是pending状态’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-6c3970a64219c820317f, section-7f322ad94ea389dd5a8e, section-96852b28457bed09b5ca, section-d494a7abc85e3c903421, business-topic:紧急故障:系统平台故障案例 / upf pod都是pending状态
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-3a02b72827b1cd6b343b0c39`
- 定位：word/document.xml/body/p[42]
```text
系统平台故障案例 / upf pod都是pending状态
upf pod都是pending状态
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-157f73cf35db89f9ebf53505`
- 定位：word/document.xml/body/p[43], word/document.xml/body/p[44], word/document.xml/body/p[45]/txbxContent[1]/p[1], word/document.xml/body/p[45]/txbxContent[1]/p[2], word/document.xml/body/p[45]/txbxContent[1]/p[3], word/document.xml/body/p[45]/txbxContent[1]/p[4], word/document.xml/body/p[45]/txbxContent[1]/p[5], word/document.xml/body/p[45]/txbxContent[1]/p[6], word/document.xml/body/p[45]/txbxContent[1]/p[7], word/document.xml/body/p[45]/txbxContent[1]/p[8], word/document.xml/body/p[45]/txbxContent[1]/p[9], word/document.xml/body/p[45]/txbxContent[1]/p[10], word/document.xml/body/p[45]/txbxContent[1]/p[11], word/document.xml/body/p[45]/txbxContent[1]/p[12], word/document.xml/body/p[45]/txbxContent[1]/p[13], word/document.xml/body/p[45]/txbxContent[1]/p[14], word/document.xml/body/p[45]/txbxContent[1]/p[15], word/document.xml/body/p[45]/txbxContent[1]/p[16], word/document.xml/body/p[45]/txbxContent[1]/p[17], word/document.xml/body/p[45]/txbxContent[1]/p[18]
```text
系统平台故障案例 / upf pod都是pending状态 / 症状现象
症状现象
k8s pod都正常，但是upf pod都是pending状态
# kubectl get pods -A
NAMESPACE          NAME                                                  READY   STATUS    RESTARTS   AGE
calico-apiserver   calico-apiserver-567cd488c9-84bvl                     1/1     Running   0          58m
calico-apiserver   calico-apiserver-567cd488c9-kr446                     1/1     Running   0          58m
calico-system      calico-kube-controllers-69fd7cf568-scdcc              1/1     Running   0          59m
calico-system      calico-node-x47q4                                     1/1     Running   0          59m
calico-system      calico-typha-6ffb8b6566-z8sjp                         1/1     Running   0          59m
calico-system      csi-node-driver-tr42h                                 2/2     Running   0          59m
ingress-nginx      ingress-nginx-controller-tvtzz                        1/1     Running   0          57m
kube-system        coredns-565d847f94-57b9r                              1/1     Running   0          59m
kube-system        coredns-565d847f94-lt5xv                              1/1     Running   0          59m
kube-system        etcd-cq-na-vivo-upf01                                 1/1     Running   0          59m
kube-system        kube-apiserver-cq-na-vivo-upf01                       1/1     Running   0          59m
kube-system        kube-controller-manager-cq-na-vivo-upf01              1/1     Running   0          59m
kube-system        kube-multus-ds-mhn7n                                  1/1     Running   0          56m
kube-system        kube-proxy-q8f7g                                      1/1     Running   0          59m
kube-system        kube-scheduler-cq-na-vivo-upf01                       1/1     Running   0          59m
kube-system        metrics-server-56997495d6-69tfx                       1/1     Running   0          56m
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-98fd28a83efb5875db69122f`
- 定位：word/document.xml/body/p[45]/txbxContent[1]/p[19], word/document.xml/body/p[45]/txbxContent[1]/p[20], word/document.xml/body/p[45]/txbxContent[1]/p[21], word/document.xml/body/p[45]/txbxContent[1]/p[22], word/document.xml/body/p[45]/txbxContent[1]/p[23], word/document.xml/body/p[45]/txbxContent[1]/p[24], word/document.xml/body/p[45]/txbxContent[1]/p[25], word/document.xml/body/p[45]/txbxContent[1]/p[26], word/document.xml/body/p[45]/txbxContent[1]/p[27], word/document.xml/body/p[45]/txbxContent[1]/p[28], word/document.xml/body/p[45]/txbxContent[1]/p[29], word/document.xml/body/p[45]/txbxContent[1]/p[30], word/document.xml/body/p[45]/txbxContent[1]/p[31], word/document.xml/body/p[45]/txbxContent[1]/p[32], word/document.xml/body/p[45]/txbxContent[1]/p[33]
```text
系统平台故障案例 / upf pod都是pending状态 / 症状现象
loki               promtail-rflqp                                        1/1     Running   0          56m
monitoring         prometheus-kube-prometheus-operator-5dc779f7c-26jkb   1/1     Running   0          57m
monitoring         prometheus-kube-state-metrics-9bc7f5984-w2chr         1/1     Running   0          57m
monitoring         prometheus-prometheus-kube-prometheus-prometheus-0    2/2     Running   0          57m
monitoring         prometheus-prometheus-node-exporter-b7kvv             1/1     Running   0          57m
nfs-provisioner    nfs-subdir-external-provisioner-697499d6d7-ncqjd      1/1     Running   0          58m
ns1                upf-1-oam-main-5999cb46c6-chmlp                       0/4     Pending   0          11m
ns1                upf-1-oam-nma-588fc4dff5-wqlpc                        0/1     Pending   0          11m
ns1                upf-1-oam-redis-0                                     0/2     Pending   0          11m
ns1                upf-1-oam-res-ns1-cu5gcupf5.0.0-zz2tm                 0/1     Pending   0          11m
ns1                upfd-1-746b47984d-s4bc5                               0/1     Pending   0          11m
ns1                upfe-1-765557df66-gphwm                               0/1     Pending   0          11m
ns1                upfm-1-754b744dfc-wlg8f                               0/1     Pending   0          11m
ns1                vdos-etcd-0                                           0/1     Pending   0          11m
ns1                vdos-server-577f4c9554-sgsfb                          0/1     Pending   0          11m
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-a1de3f7c22f6b1bc510422ac`
- 定位：word/document.xml/body/p[46], word/document.xml/body/p[47], word/document.xml/body/p[49]/txbxContent[1]/p[1], word/document.xml/body/p[49]/txbxContent[1]/p[2], word/document.xml/body/p[49]/txbxContent[1]/p[3], word/document.xml/body/p[49]/txbxContent[1]/p[4], word/document.xml/body/p[50], word/document.xml/body/p[51]/txbxContent[1]/p[1], word/document.xml/body/p[51]/txbxContent[1]/p[2], word/document.xml/body/p[51]/txbxContent[1]/p[3]
```text
系统平台故障案例 / upf pod都是pending状态 / 信息收集
信息收集
describe pod提示node不存在
Events:
  Type     Reason            Age    From               Message
  ----     ------            ----   ----               -------
  Warning  FailedScheduling  3m20s  default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {node.kubernetes.io/unreachable: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
查看pod发现是主机名(upf02)与node名(upf01)不一致。通常因为装完k8s后改过节点名字。
root@upf02:~# kubectl get node -A
NAME               STATUS     ROLES           AGE   VERSION
upf01   NotReady   control-plane   59m   v1.25.11
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-14d484ec2e21c87c583fbb7e`
- 定位：word/document.xml/body/p[52], word/document.xml/body/p[53]
```text
系统平台故障案例 / upf pod都是pending状态 / 解决办法
解决办法
修改k8s配置文件保持与主机名一致后重装k8s。
```
- 预期原文/缺口：
```text
系统平台故障案例 / upf pod都是pending状态
upf pod都是pending状态
系统平台故障案例 / upf pod都是pending状态 / 症状现象
症状现象
k8s pod都正常，但是upf pod都是pending状态
# kubectl get pods -A
NAMESPACE          NAME                                                  READY   STATUS    RESTARTS   AGE
calico-apiserver   calico-apiserver-567cd488c9-84bvl                     1/1     Running   0          58m
calico-apiserver   calico-apiserver-567cd488c9-kr446                     1/1     Running   0          58m
calico-system      calico-kube-controllers-69fd7cf568-scdcc              1/1     Running   0          59m
calico-system      calico-node-x47q4                                     1/1     Running   0          59m
calico-system      calico-typha-6ffb8b6566-z8sjp                         1/1     Running   0          59m
calico-system      csi-node-driver-tr42h                                 2/2     Running   0          59m
ingress-nginx      ingress-nginx-controller-tvtzz                        1/1     Running   0          57m
kube-system        coredns-565d847f94-57b9r                              1/1     Running   0          59m
kube-system        coredns-565d847f94-lt5xv                              1/1     Running   0          59m
kube-system        etcd-cq-na-vivo-upf01                                 1/1     Running   0          59m
kube-system        kube-apiserver-cq-na-vivo-upf01                       1/1     Running   0          59m
kube-system        kube-controller-manager-cq-na-vivo-upf01              1/1     Running   0          59m
kube-system        kube-multus-ds-mhn7n                                  1/1     Running   0          56m
kube-system        kube-proxy-q8f7g                                      1/1     Running   0          59m
kube-system        kube-scheduler-cq-na-vivo-upf01                       1/1     Running   0          59m
kube-system        metrics-server-56997495d6-69tfx                       1/1     Running   0          56m
系统平台故障案例 / upf pod都是pending状态 / 症状现象
loki               promtail-rflqp                                        1/1     Running   0          56m
monitoring         prometheus-kube-prometheus-operator-5dc779f7c-26jkb   1/1     Running   0          57m
monitoring         prometheus-kube-state-metrics-9bc7f5984-w2chr         1/1     Running   0          57m
monitoring         prometheus-prometheus-kube-prometheus-prometheus-0    2/2     Running   0          57m
monitoring         prometheus-prometheus-node-exporter-b7kvv             1/1     Running   0          57m
nfs-provisioner    nfs-subdir-external-provisioner-697499d6d7-ncqjd      1/1     Running   0          58m
ns1                upf-1-oam-main-5999cb46c6-chmlp                       0/4     Pending   0          11m
ns1                upf-1-oam-nma-588fc4dff5-wqlpc                        0/1     Pending   0          11m
ns1                upf-1-oam-redis-0                                     0/2     Pending   0          11m
ns1                upf-1-oam-res-ns1-cu5gcupf5.0.0-zz2tm                 0/1     Pending   0          11m
ns1                upfd-1-746b47984d-s4bc5                               0/1     Pending   0          11m
ns1                upfe-1-765557df66-gphwm                               0/1     Pending   0          11m
ns1                upfm-1-754b744dfc-wlg8f                               0/1     Pending   0          11m
ns1                vdos-etcd-0                                           0/1     Pending   0          11m
ns1                vdos-server-577f4c9554-sgsfb                          0/1     Pending   0          11m
系统平台故障案例 / upf pod都是pending状态 / 信息收集
信息收集
describe pod提示node不存在
Events:
  Type     Reason            Age    From               Message
  ----     ------            ----   ----               -------
  Warning  FailedScheduling  3m20s  default-scheduler  0/1 nodes are available: 1 node(s) had untolerated taint {node.kubernetes.io/unreachable: }. preemption: 0/1 nodes are available: 1 Preemption is not helpful for scheduling.
查看pod发现是主机名(upf02)与node名(upf01)不一致。通常因为装完k8s后改过节点名字。
root@upf02:~# kubectl get node -A
NAME               STATUS     ROLES           AGE   VERSION
upf01   NotReady   control-plane   59m   v1.25.11
系统平台故障案例 / upf pod都是pending状态 / 解决办法
解决办法
修改k8s配置文件保持与主机名一致后重装k8s。
```

## troubleshooting-013 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-0313d51a473bcdcb76e8, section-3f5abbc284592f6753c6, section-a15091a40f3458f3cd99, section-e3adf32f2d5e7d23c1f5, business-topic:紧急故障:系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-79be5558da1f8e692077e724`
- 定位：word/document.xml/body/p[54]
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-a0fd1ff4cf93743de216491a`
- 定位：word/document.xml/body/p[55], word/document.xml/body/p[56], word/document.xml/body/p[57]/txbxContent[1]/p[1], word/document.xml/body/p[57]/txbxContent[1]/p[2]
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 症状现象
症状现象
upfmgr hc执行报错
root@ylx-upf-5:~# upfmgr hc
/opt/5gc/upfd/etc/UPF_OM_Inspect.sh: line 29: /root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf: No such file or directory
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-70ca23007a1343f908de4e7d`
- 定位：word/document.xml/body/p[58], word/document.xml/body/p[59]/txbxContent[1]/p[1], word/document.xml/body/p[59]/txbxContent[1]/p[2], word/document.xml/body/p[59]/txbxContent[1]/p[3]
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 信息收集
信息收集
root@ylx-upf-5:~# ll /root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf
ls: cannot access '/root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf': No such file or directory
root@ylx-upf-5:~#
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2741ae1d6c914eabe88ed25e`
- 定位：word/document.xml/body/p[60], word/document.xml/body/p[61], word/document.xml/body/p[62], word/document.xml/body/p[63], word/document.xml/body/p[64], word/document.xml/body/p[65], word/document.xml/body/p[66], word/document.xml/body/p[67]/txbxContent[1]/p[1], word/document.xml/body/p[67]/txbxContent[1]/p[2], word/document.xml/body/p[67]/txbxContent[1]/p[3], word/document.xml/body/p[67]/txbxContent[1]/p[5], word/document.xml/body/p[67]/txbxContent[1]/p[7], word/document.xml/body/p[67]/txbxContent[1]/p[8], word/document.xml/body/p[67]/txbxContent[1]/p[9], word/document.xml/body/p[67]/txbxContent[1]/p[10], word/document.xml/body/p[67]/txbxContent[1]/p[11], word/document.xml/body/p[67]/txbxContent[1]/p[12], word/document.xml/body/p[67]/txbxContent[1]/p[13], word/document.xml/body/p[67]/txbxContent[1]/p[14], word/document.xml/body/p[67]/txbxContent[1]/p[15], word/document.xml/body/p[67]/txbxContent[1]/p[16], word/document.xml/body/p[67]/txbxContent[1]/p[18], word/document.xml/body/p[67]/txbxContent[1]/p[19], word/document.xml/body/p[67]/txbxContent[1]/p[20], word/document.xml/body/p[67]/txbxContent[1]/p[21], word/document.xml/body/p[67]/txbxContent[1]/p[22], word/document.xml/body/p[67]/txbxContent[1]/p[23], word/document.xml/body/p[67]/txbxContent[1]/p[24], word/document.xml/body/p[67]/txbxContent[1]/p[25], word/document.xml/body/p[67]/txbxContent[1]/p[26], word/document.xml/body/p[67]/txbxContent[1]/p[27], word/document.xml/body/p[67]/txbxContent[1]/p[28], word/document.xml/body/p[67]/txbxContent[1]/p[29]
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 解决办法
解决办法
检查logCollector.sh脚本是否存在
ll /opt/5gc/upfd/etc/logCollector.sh
logCollector.sh存在的话执行安装命令
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh install
根据输出的配置文件名称填写文件内需要监控的N4/N3/N6网关ip等信息
上面三个步骤相关操作记录如下：
root@ylx-upf-5:~# ll /opt/5gc/upfd/etc/logCollector.sh
-rwxrwxr-x 1 1013 1013 41008 Sep  5 15:14 /opt/5gc/upfd/etc/logCollector.sh*
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh
2025-09-15 16:42:44PM
Usage: logCollector.sh all          - Collecting UPF all Logs that required for investigating issues
       logCollector.sh install      - Run 'bash logCollector.sh install' to install shell script
       logCollector.sh upfd         - Collecting UPFD Cli relational logs
       logCollector.sh vpp          - Collecting VPP Cli relational Logs
       logCollector.sh intfstatus   - Collecting UPFD N3/N4/N6 SMFs and gNB Interface link status Logs
       logCollector.sh sysinfo      - Collecting System infomations as Pods/DPDK/CPU/mem/disk...
       logCollector.sh tar          - Tar the Collecting UPFD and VPP Logs
       logCollector.sh clean        - Clean the Old upf Logs have been Collected 3 days ago
----------------------------------------------------------------------------------------------------------
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh install
2025-09-15 16:43:55PM
installing Collecte all Upf Log shell script...
Environment check befor Running this shell...
Environment is ready for Running this shell...
 Install the logCollector.sh shell script File Successfully!!!
 Now you can run 'logCollector.sh all' command to collet All log in any working directory
******************************************************************************
If you want to test N3/N4/N6 SMFs and gNB linking status, Please Modify '/root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf' IP Configuration.
*****************************************************************************
2025-09-15 16:43:55PM
----------------------------------------------------------------------------------------------------------
root@ylx-upf-5:~#
```
- 预期原文/缺口：
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 症状现象
症状现象
upfmgr hc执行报错
root@ylx-upf-5:~# upfmgr hc
/opt/5gc/upfd/etc/UPF_OM_Inspect.sh: line 29: /root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf: No such file or directory
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 信息收集
信息收集
root@ylx-upf-5:~# ll /root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf
ls: cannot access '/root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf': No such file or directory
root@ylx-upf-5:~#
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 解决办法
解决办法
检查logCollector.sh脚本是否存在
ll /opt/5gc/upfd/etc/logCollector.sh
logCollector.sh存在的话执行安装命令
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh install
根据输出的配置文件名称填写文件内需要监控的N4/N3/N6网关ip等信息
上面三个步骤相关操作记录如下：
root@ylx-upf-5:~# ll /opt/5gc/upfd/etc/logCollector.sh
-rwxrwxr-x 1 1013 1013 41008 Sep  5 15:14 /opt/5gc/upfd/etc/logCollector.sh*
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh
2025-09-15 16:42:44PM
Usage: logCollector.sh all          - Collecting UPF all Logs that required for investigating issues
       logCollector.sh install      - Run 'bash logCollector.sh install' to install shell script
       logCollector.sh upfd         - Collecting UPFD Cli relational logs
       logCollector.sh vpp          - Collecting VPP Cli relational Logs
       logCollector.sh intfstatus   - Collecting UPFD N3/N4/N6 SMFs and gNB Interface link status Logs
       logCollector.sh sysinfo      - Collecting System infomations as Pods/DPDK/CPU/mem/disk...
       logCollector.sh tar          - Tar the Collecting UPFD and VPP Logs
       logCollector.sh clean        - Clean the Old upf Logs have been Collected 3 days ago
----------------------------------------------------------------------------------------------------------
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh install
2025-09-15 16:43:55PM
installing Collecte all Upf Log shell script...
Environment check befor Running this shell...
Environment is ready for Running this shell...
 Install the logCollector.sh shell script File Successfully!!!
 Now you can run 'logCollector.sh all' command to collet All log in any working directory
******************************************************************************
If you want to test N3/N4/N6 SMFs and gNB linking status, Please Modify '/root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf' IP Configuration.
*****************************************************************************
2025-09-15 16:43:55PM
----------------------------------------------------------------------------------------------------------
root@ylx-upf-5:~#
```

## troubleshooting-014 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-0313d51a473bcdcb76e8, section-3f5abbc284592f6753c6, section-a15091a40f3458f3cd99, section-e3adf32f2d5e7d23c1f5, business-topic:紧急故障:系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-79be5558da1f8e692077e724`
- 定位：word/document.xml/body/p[54]
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-a0fd1ff4cf93743de216491a`
- 定位：word/document.xml/body/p[55], word/document.xml/body/p[56], word/document.xml/body/p[57]/txbxContent[1]/p[1], word/document.xml/body/p[57]/txbxContent[1]/p[2]
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 症状现象
症状现象
upfmgr hc执行报错
root@ylx-upf-5:~# upfmgr hc
/opt/5gc/upfd/etc/UPF_OM_Inspect.sh: line 29: /root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf: No such file or directory
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-70ca23007a1343f908de4e7d`
- 定位：word/document.xml/body/p[58], word/document.xml/body/p[59]/txbxContent[1]/p[1], word/document.xml/body/p[59]/txbxContent[1]/p[2], word/document.xml/body/p[59]/txbxContent[1]/p[3]
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 信息收集
信息收集
root@ylx-upf-5:~# ll /root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf
ls: cannot access '/root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf': No such file or directory
root@ylx-upf-5:~#
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2741ae1d6c914eabe88ed25e`
- 定位：word/document.xml/body/p[60], word/document.xml/body/p[61], word/document.xml/body/p[62], word/document.xml/body/p[63], word/document.xml/body/p[64], word/document.xml/body/p[65], word/document.xml/body/p[66], word/document.xml/body/p[67]/txbxContent[1]/p[1], word/document.xml/body/p[67]/txbxContent[1]/p[2], word/document.xml/body/p[67]/txbxContent[1]/p[3], word/document.xml/body/p[67]/txbxContent[1]/p[5], word/document.xml/body/p[67]/txbxContent[1]/p[7], word/document.xml/body/p[67]/txbxContent[1]/p[8], word/document.xml/body/p[67]/txbxContent[1]/p[9], word/document.xml/body/p[67]/txbxContent[1]/p[10], word/document.xml/body/p[67]/txbxContent[1]/p[11], word/document.xml/body/p[67]/txbxContent[1]/p[12], word/document.xml/body/p[67]/txbxContent[1]/p[13], word/document.xml/body/p[67]/txbxContent[1]/p[14], word/document.xml/body/p[67]/txbxContent[1]/p[15], word/document.xml/body/p[67]/txbxContent[1]/p[16], word/document.xml/body/p[67]/txbxContent[1]/p[18], word/document.xml/body/p[67]/txbxContent[1]/p[19], word/document.xml/body/p[67]/txbxContent[1]/p[20], word/document.xml/body/p[67]/txbxContent[1]/p[21], word/document.xml/body/p[67]/txbxContent[1]/p[22], word/document.xml/body/p[67]/txbxContent[1]/p[23], word/document.xml/body/p[67]/txbxContent[1]/p[24], word/document.xml/body/p[67]/txbxContent[1]/p[25], word/document.xml/body/p[67]/txbxContent[1]/p[26], word/document.xml/body/p[67]/txbxContent[1]/p[27], word/document.xml/body/p[67]/txbxContent[1]/p[28], word/document.xml/body/p[67]/txbxContent[1]/p[29]
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 解决办法
解决办法
检查logCollector.sh脚本是否存在
ll /opt/5gc/upfd/etc/logCollector.sh
logCollector.sh存在的话执行安装命令
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh install
根据输出的配置文件名称填写文件内需要监控的N4/N3/N6网关ip等信息
上面三个步骤相关操作记录如下：
root@ylx-upf-5:~# ll /opt/5gc/upfd/etc/logCollector.sh
-rwxrwxr-x 1 1013 1013 41008 Sep  5 15:14 /opt/5gc/upfd/etc/logCollector.sh*
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh
2025-09-15 16:42:44PM
Usage: logCollector.sh all          - Collecting UPF all Logs that required for investigating issues
       logCollector.sh install      - Run 'bash logCollector.sh install' to install shell script
       logCollector.sh upfd         - Collecting UPFD Cli relational logs
       logCollector.sh vpp          - Collecting VPP Cli relational Logs
       logCollector.sh intfstatus   - Collecting UPFD N3/N4/N6 SMFs and gNB Interface link status Logs
       logCollector.sh sysinfo      - Collecting System infomations as Pods/DPDK/CPU/mem/disk...
       logCollector.sh tar          - Tar the Collecting UPFD and VPP Logs
       logCollector.sh clean        - Clean the Old upf Logs have been Collected 3 days ago
----------------------------------------------------------------------------------------------------------
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh install
2025-09-15 16:43:55PM
installing Collecte all Upf Log shell script...
Environment check befor Running this shell...
Environment is ready for Running this shell...
 Install the logCollector.sh shell script File Successfully!!!
 Now you can run 'logCollector.sh all' command to collet All log in any working directory
******************************************************************************
If you want to test N3/N4/N6 SMFs and gNB linking status, Please Modify '/root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf' IP Configuration.
*****************************************************************************
2025-09-15 16:43:55PM
----------------------------------------------------------------------------------------------------------
root@ylx-upf-5:~#
```
- 预期原文/缺口：
```text
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 症状现象
症状现象
upfmgr hc执行报错
root@ylx-upf-5:~# upfmgr hc
/opt/5gc/upfd/etc/UPF_OM_Inspect.sh: line 29: /root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf: No such file or directory
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 信息收集
信息收集
root@ylx-upf-5:~# ll /root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf
ls: cannot access '/root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf': No such file or directory
root@ylx-upf-5:~#
系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 解决办法
解决办法
检查logCollector.sh脚本是否存在
ll /opt/5gc/upfd/etc/logCollector.sh
logCollector.sh存在的话执行安装命令
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh install
根据输出的配置文件名称填写文件内需要监控的N4/N3/N6网关ip等信息
上面三个步骤相关操作记录如下：
root@ylx-upf-5:~# ll /opt/5gc/upfd/etc/logCollector.sh
-rwxrwxr-x 1 1013 1013 41008 Sep  5 15:14 /opt/5gc/upfd/etc/logCollector.sh*
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh
2025-09-15 16:42:44PM
Usage: logCollector.sh all          - Collecting UPF all Logs that required for investigating issues
       logCollector.sh install      - Run 'bash logCollector.sh install' to install shell script
       logCollector.sh upfd         - Collecting UPFD Cli relational logs
       logCollector.sh vpp          - Collecting VPP Cli relational Logs
       logCollector.sh intfstatus   - Collecting UPFD N3/N4/N6 SMFs and gNB Interface link status Logs
       logCollector.sh sysinfo      - Collecting System infomations as Pods/DPDK/CPU/mem/disk...
       logCollector.sh tar          - Tar the Collecting UPFD and VPP Logs
       logCollector.sh clean        - Clean the Old upf Logs have been Collected 3 days ago
----------------------------------------------------------------------------------------------------------
root@ylx-upf-5:~# /opt/5gc/upfd/etc/logCollector.sh install
2025-09-15 16:43:55PM
installing Collecte all Upf Log shell script...
Environment check befor Running this shell...
Environment is ready for Running this shell...
 Install the logCollector.sh shell script File Successfully!!!
 Now you can run 'logCollector.sh all' command to collet All log in any working directory
******************************************************************************
If you want to test N3/N4/N6 SMFs and gNB linking status, Please Modify '/root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf' IP Configuration.
*****************************************************************************
2025-09-15 16:43:55PM
----------------------------------------------------------------------------------------------------------
root@ylx-upf-5:~#
```

## troubleshooting-015 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘upfmgr hc执行显示N3和N6的v4/v6地址都为空’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-183a99b66de243bf2756, section-1edd97673fd6c532d0f9, section-4e3a2b23da6ff5443789, section-8b36c9a625381139afe8, business-topic:紧急故障:系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-08630c4b1f06ce898a787d1f`
- 定位：word/document.xml/body/p[69]
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空
upfmgr hc执行显示N3和N6的v4/v6地址都为空
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-23dbf77e259512f04b1b34ad`
- 定位：word/document.xml/body/p[70], word/document.xml/body/p[71], word/document.xml/body/p[72]/txbxContent[1]/p[1], word/document.xml/body/p[72]/txbxContent[1]/p[2], word/document.xml/body/p[72]/txbxContent[1]/p[3], word/document.xml/body/p[72]/txbxContent[1]/p[4]
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 症状现象
症状现象
upfmgr hc执行报错
| N3(v4)接口地址     | Error      |                   
| N3(v6)接口地址     | Error      | ::/0              
| N6(v4)接口地址     | Error      |                    |
| N6(v6)接口地址     | Error      | ::/0               |
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-0de81a0ec40a03b6c44cebc0`
- 定位：word/document.xml/body/p[73], word/document.xml/body/p[74]/txbxContent[1]/p[1], word/document.xml/body/p[74]/txbxContent[1]/p[2], word/document.xml/body/p[74]/txbxContent[1]/p[3], word/document.xml/body/p[74]/txbxContent[1]/p[4], word/document.xml/body/p[74]/txbxContent[1]/p[5], word/document.xml/body/p[74]/txbxContent[1]/p[6], word/document.xml/body/p[74]/txbxContent[1]/p[7], word/document.xml/body/p[74]/txbxContent[1]/p[8]
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 信息收集
信息收集
root@ylx-upf-5:~# upfmgr hc
2025-09-15 08:53:49 - 获取基站gtpu地址中...
2025-09-15 08:53:49 -  Get GTPU Node IP Failed!
。。。。。。
| N3(v4)接口地址     | Error      |                   
| N3(v6)接口地址     | Error      | ::/0              
| N6(v4)接口地址     | Error      |                    |
| N6(v6)接口地址     | Error      | ::/0               |
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-4c21851d9deb5b668916c02a`
- 定位：word/document.xml/body/p[75], word/document.xml/body/p[76], word/document.xml/body/p[77], word/document.xml/body/p[78]
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 解决办法
解决办法
upfmgr ctrl登录37100去show config看N4/N3/N6的地址配置是否存在
如果步骤1 show config配置不存在，则需要执行相关配置N3/N6业务口地址的MML命令。
如果步骤1 show config配置存在，则执行命令：dpkg -l | grep expect 看看是否没有安装expect工具，如果expect和tcl-expect不存在，则需要把工具拷贝过来执行dpkg -i <name>命令安装。
```
- 预期原文/缺口：
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空
upfmgr hc执行显示N3和N6的v4/v6地址都为空
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 症状现象
症状现象
upfmgr hc执行报错
| N3(v4)接口地址     | Error      |                   
| N3(v6)接口地址     | Error      | ::/0              
| N6(v4)接口地址     | Error      |                    |
| N6(v6)接口地址     | Error      | ::/0               |
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 信息收集
信息收集
root@ylx-upf-5:~# upfmgr hc
2025-09-15 08:53:49 - 获取基站gtpu地址中...
2025-09-15 08:53:49 -  Get GTPU Node IP Failed!
。。。。。。
| N3(v4)接口地址     | Error      |                   
| N3(v6)接口地址     | Error      | ::/0              
| N6(v4)接口地址     | Error      |                    |
| N6(v6)接口地址     | Error      | ::/0               |
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 解决办法
解决办法
upfmgr ctrl登录37100去show config看N4/N3/N6的地址配置是否存在
如果步骤1 show config配置不存在，则需要执行相关配置N3/N6业务口地址的MML命令。
如果步骤1 show config配置存在，则执行命令：dpkg -l | grep expect 看看是否没有安装expect工具，如果expect和tcl-expect不存在，则需要把工具拷贝过来执行dpkg -i <name>命令安装。
```

## troubleshooting-016 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘upfmgr hc执行显示N3和N6的v4/v6地址都为空’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-183a99b66de243bf2756, section-1edd97673fd6c532d0f9, section-4e3a2b23da6ff5443789, section-8b36c9a625381139afe8, business-topic:紧急故障:系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-08630c4b1f06ce898a787d1f`
- 定位：word/document.xml/body/p[69]
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空
upfmgr hc执行显示N3和N6的v4/v6地址都为空
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-23dbf77e259512f04b1b34ad`
- 定位：word/document.xml/body/p[70], word/document.xml/body/p[71], word/document.xml/body/p[72]/txbxContent[1]/p[1], word/document.xml/body/p[72]/txbxContent[1]/p[2], word/document.xml/body/p[72]/txbxContent[1]/p[3], word/document.xml/body/p[72]/txbxContent[1]/p[4]
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 症状现象
症状现象
upfmgr hc执行报错
| N3(v4)接口地址     | Error      |                   
| N3(v6)接口地址     | Error      | ::/0              
| N6(v4)接口地址     | Error      |                    |
| N6(v6)接口地址     | Error      | ::/0               |
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-0de81a0ec40a03b6c44cebc0`
- 定位：word/document.xml/body/p[73], word/document.xml/body/p[74]/txbxContent[1]/p[1], word/document.xml/body/p[74]/txbxContent[1]/p[2], word/document.xml/body/p[74]/txbxContent[1]/p[3], word/document.xml/body/p[74]/txbxContent[1]/p[4], word/document.xml/body/p[74]/txbxContent[1]/p[5], word/document.xml/body/p[74]/txbxContent[1]/p[6], word/document.xml/body/p[74]/txbxContent[1]/p[7], word/document.xml/body/p[74]/txbxContent[1]/p[8]
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 信息收集
信息收集
root@ylx-upf-5:~# upfmgr hc
2025-09-15 08:53:49 - 获取基站gtpu地址中...
2025-09-15 08:53:49 -  Get GTPU Node IP Failed!
。。。。。。
| N3(v4)接口地址     | Error      |                   
| N3(v6)接口地址     | Error      | ::/0              
| N6(v4)接口地址     | Error      |                    |
| N6(v6)接口地址     | Error      | ::/0               |
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-4c21851d9deb5b668916c02a`
- 定位：word/document.xml/body/p[75], word/document.xml/body/p[76], word/document.xml/body/p[77], word/document.xml/body/p[78]
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 解决办法
解决办法
upfmgr ctrl登录37100去show config看N4/N3/N6的地址配置是否存在
如果步骤1 show config配置不存在，则需要执行相关配置N3/N6业务口地址的MML命令。
如果步骤1 show config配置存在，则执行命令：dpkg -l | grep expect 看看是否没有安装expect工具，如果expect和tcl-expect不存在，则需要把工具拷贝过来执行dpkg -i <name>命令安装。
```
- 预期原文/缺口：
```text
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空
upfmgr hc执行显示N3和N6的v4/v6地址都为空
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 症状现象
症状现象
upfmgr hc执行报错
| N3(v4)接口地址     | Error      |                   
| N3(v6)接口地址     | Error      | ::/0              
| N6(v4)接口地址     | Error      |                    |
| N6(v6)接口地址     | Error      | ::/0               |
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 信息收集
信息收集
root@ylx-upf-5:~# upfmgr hc
2025-09-15 08:53:49 - 获取基站gtpu地址中...
2025-09-15 08:53:49 -  Get GTPU Node IP Failed!
。。。。。。
| N3(v4)接口地址     | Error      |                   
| N3(v6)接口地址     | Error      | ::/0              
| N6(v4)接口地址     | Error      |                    |
| N6(v6)接口地址     | Error      | ::/0               |
系统平台故障案例 / upfmgr hc执行显示N3和N6的v4/v6地址都为空 / 解决办法
解决办法
upfmgr ctrl登录37100去show config看N4/N3/N6的地址配置是否存在
如果步骤1 show config配置不存在，则需要执行相关配置N3/N6业务口地址的MML命令。
如果步骤1 show config配置存在，则执行命令：dpkg -l | grep expect 看看是否没有安装expect工具，如果expect和tcl-expect不存在，则需要把工具拷贝过来执行dpkg -i <name>命令安装。
```

## troubleshooting-017 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-951f426c18821559e98f, section-9a769c2dab4c043c5224, section-c3f40256239f43faea76, section-f8b70b2493ae0477ad18, business-topic:紧急故障:业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-39848d8edfd180397a999e80`
- 定位：word/document.xml/body/p[97]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2bf3e76ac58698d45df9b2b8`
- 定位：word/document.xml/body/p[98], word/document.xml/body/p[99], word/document.xml/body/p[100]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 症状现象
症状现象
UPF（4.0版本）upfd pod一直crash。查看kubectl log提示
file:upfd_pfcp.c( upfdPfcpInit:315) fatal:UPFD open pfcp v6 socket for pfcp failed!
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-52db515efc441dcf26a40fe3`
- 定位：word/document.xml/body/p[101], word/document.xml/body/p[102], word/document.xml/body/p[103]/txbxContent[1]/p[1], word/document.xml/body/p[104]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 信息收集
信息收集
检查N4 IPV6地址和Linux系统配置的是否一致，如果不一致则将N4地址改成一致。
/opt/5gc/upfd/etc/loam mml 'QRY UpfIntfAddrConfig;'
如果N4配了bond，交换机那边也需要配bond。Lacp没协商好，N4监听不了IPV6。
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-bf85b8cb923178ed3aef0829`
- 定位：word/document.xml/body/p[106], word/document.xml/body/p[107], word/document.xml/body/p[108], word/document.xml/body/p[109]/txbxContent[1]/p[1], word/document.xml/body/p[110]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 解决方法
解决方法
如果N4地址配置不一致则将N4地址改成一致。
如果Lacp没协商好，暂时可以把IPV6的地址先删了，那样UPF能起来。然后再等交换机bond配好后，再把V6地址加上去。
/opt/5gc/upfd/etc/loam mml 'DEL UpfIntfAddrConfig: InterfaceId = "2";'
UPF配bond的时候就会配lacp，交换机需要配静态lacp就可以。
```
- 预期原文/缺口：
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 症状现象
症状现象
UPF（4.0版本）upfd pod一直crash。查看kubectl log提示
file:upfd_pfcp.c( upfdPfcpInit:315) fatal:UPFD open pfcp v6 socket for pfcp failed!
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 信息收集
信息收集
检查N4 IPV6地址和Linux系统配置的是否一致，如果不一致则将N4地址改成一致。
/opt/5gc/upfd/etc/loam mml 'QRY UpfIntfAddrConfig;'
如果N4配了bond，交换机那边也需要配bond。Lacp没协商好，N4监听不了IPV6。
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 解决方法
解决方法
如果N4地址配置不一致则将N4地址改成一致。
如果Lacp没协商好，暂时可以把IPV6的地址先删了，那样UPF能起来。然后再等交换机bond配好后，再把V6地址加上去。
/opt/5gc/upfd/etc/loam mml 'DEL UpfIntfAddrConfig: InterfaceId = "2";'
UPF配bond的时候就会配lacp，交换机需要配静态lacp就可以。
```

## troubleshooting-018 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-951f426c18821559e98f, section-9a769c2dab4c043c5224, section-c3f40256239f43faea76, section-f8b70b2493ae0477ad18, business-topic:紧急故障:业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-39848d8edfd180397a999e80`
- 定位：word/document.xml/body/p[97]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-2bf3e76ac58698d45df9b2b8`
- 定位：word/document.xml/body/p[98], word/document.xml/body/p[99], word/document.xml/body/p[100]/txbxContent[1]/p[1]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 症状现象
症状现象
UPF（4.0版本）upfd pod一直crash。查看kubectl log提示
file:upfd_pfcp.c( upfdPfcpInit:315) fatal:UPFD open pfcp v6 socket for pfcp failed!
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-52db515efc441dcf26a40fe3`
- 定位：word/document.xml/body/p[101], word/document.xml/body/p[102], word/document.xml/body/p[103]/txbxContent[1]/p[1], word/document.xml/body/p[104]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 信息收集
信息收集
检查N4 IPV6地址和Linux系统配置的是否一致，如果不一致则将N4地址改成一致。
/opt/5gc/upfd/etc/loam mml 'QRY UpfIntfAddrConfig;'
如果N4配了bond，交换机那边也需要配bond。Lacp没协商好，N4监听不了IPV6。
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-bf85b8cb923178ed3aef0829`
- 定位：word/document.xml/body/p[106], word/document.xml/body/p[107], word/document.xml/body/p[108], word/document.xml/body/p[109]/txbxContent[1]/p[1], word/document.xml/body/p[110]
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 解决方法
解决方法
如果N4地址配置不一致则将N4地址改成一致。
如果Lacp没协商好，暂时可以把IPV6的地址先删了，那样UPF能起来。然后再等交换机bond配好后，再把V6地址加上去。
/opt/5gc/upfd/etc/loam mml 'DEL UpfIntfAddrConfig: InterfaceId = "2";'
UPF配bond的时候就会配lacp，交换机需要配静态lacp就可以。
```
- 预期原文/缺口：
```text
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 症状现象
症状现象
UPF（4.0版本）upfd pod一直crash。查看kubectl log提示
file:upfd_pfcp.c( upfdPfcpInit:315) fatal:UPFD open pfcp v6 socket for pfcp failed!
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 信息收集
信息收集
检查N4 IPV6地址和Linux系统配置的是否一致，如果不一致则将N4地址改成一致。
/opt/5gc/upfd/etc/loam mml 'QRY UpfIntfAddrConfig;'
如果N4配了bond，交换机那边也需要配bond。Lacp没协商好，N4监听不了IPV6。
业务故障案例 / UPF（4.0版本）upfd pod一直crash：upfd创建不了ipv6 socket / 解决方法
解决方法
如果N4地址配置不一致则将N4地址改成一致。
如果Lacp没协商好，暂时可以把IPV6的地址先删了，那样UPF能起来。然后再等交换机bond配好后，再把V6地址加上去。
/opt/5gc/upfd/etc/loam mml 'DEL UpfIntfAddrConfig: InterfaceId = "2";'
UPF配bond的时候就会配lacp，交换机需要配静态lacp就可以。
```

## troubleshooting-019 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：在手册的‘UPFD 的N4 接口8805端口未侦听’案例中，症状、信息收集和处理建议是什么？区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-8ca3a5ba350a0649d7c1, section-8dd19a4afda364ade0ab, section-94e1049c03de6b88ee2e, section-9944a27c711d13e4651a, business-topic:紧急故障:业务故障案例 / UPFD 的N4 接口8805端口未侦听
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-a5fe4f06446c7d0b912e0a86`
- 定位：word/document.xml/body/p[168]
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听
UPFD 的N4 接口8805端口未侦听
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-29644bf94f2add7cce44a225`
- 定位：word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172]
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 症状现象
症状现象
终端无法正常建立会话；
N4偶联未建立；
UPF N4接口地址未配置；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-3d1e35446073fb46992c0d86`
- 定位：word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[175]
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 信息收集
信息收集
检查UPF N4接口地址是否正常配置：使用upfmgr ctrl命令进入cli交互界面，执行show config 查看接口配置信息；
若接口地址正常配置：使用upfmgr bash命令进入pod，netstat -nap|grep 8805查看端口是否正常监听，若端口未正常监听查看日志信息tail -f /var/log/upf/upfd/upfd-gen.log；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-f1cdd8fb245420276b3bd4f3`
- 定位：word/document.xml/body/p[176], word/document.xml/body/p[177], word/document.xml/body/p[178]
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 解决方法
解决方法
若接口未正常配置，把接口地址配置完后再查看8805端口是否正常监听；
如接口地址配置正确，但是N4的8805端口仍然未正常监听，使用upfmgr restart命令重启upfd后看是否正常监听；
```
- 预期原文/缺口：
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听
UPFD 的N4 接口8805端口未侦听
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 症状现象
症状现象
终端无法正常建立会话；
N4偶联未建立；
UPF N4接口地址未配置；
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 信息收集
信息收集
检查UPF N4接口地址是否正常配置：使用upfmgr ctrl命令进入cli交互界面，执行show config 查看接口配置信息；
若接口地址正常配置：使用upfmgr bash命令进入pod，netstat -nap|grep 8805查看端口是否正常监听，若端口未正常监听查看日志信息tail -f /var/log/upf/upfd/upfd-gen.log；
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 解决方法
解决方法
若接口未正常配置，把接口地址配置完后再查看8805端口是否正常监听；
如接口地址配置正确，但是N4的8805端口仍然未正常监听，使用upfmgr restart命令重启upfd后看是否正常监听；
```

## troubleshooting-020 · heldout · troubleshooting

- [ ] 问题及预期事实/相关证据已核对
- 问题：请引用手册‘UPFD 的N4 接口8805端口未侦听’的排查依据与处理前提。区分历史案例与当前故障；原件有接口、版本或步骤矛盾时指出。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：section-8ca3a5ba350a0649d7c1, section-8dd19a4afda364ade0ab, section-94e1049c03de6b88ee2e, section-9944a27c711d13e4651a, business-topic:紧急故障:业务故障案例 / UPFD 的N4 接口8805端口未侦听
- synthetic：False
- 禁止结论：历史案例原因就是当前根因；实际执行了手册操作；截图缺失字段可以自行补造；已确认现场数值或真实拓扑
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-a5fe4f06446c7d0b912e0a86`
- 定位：word/document.xml/body/p[168]
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听
UPFD 的N4 接口8805端口未侦听
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-29644bf94f2add7cce44a225`
- 定位：word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172]
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 症状现象
症状现象
终端无法正常建立会话；
N4偶联未建立；
UPF N4接口地址未配置；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-3d1e35446073fb46992c0d86`
- 定位：word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[175]
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 信息收集
信息收集
检查UPF N4接口地址是否正常配置：使用upfmgr ctrl命令进入cli交互界面，执行show config 查看接口配置信息；
若接口地址正常配置：使用upfmgr bash命令进入pod，netstat -nap|grep 8805查看端口是否正常监听，若端口未正常监听查看日志信息tail -f /var/log/upf/upfd/upfd-gen.log；
```
- 来源：中国联通5G专网UPF紧急故障指引0429(1).docx · `chunk-f1cdd8fb245420276b3bd4f3`
- 定位：word/document.xml/body/p[176], word/document.xml/body/p[177], word/document.xml/body/p[178]
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 解决方法
解决方法
若接口未正常配置，把接口地址配置完后再查看8805端口是否正常监听；
如接口地址配置正确，但是N4的8805端口仍然未正常监听，使用upfmgr restart命令重启upfd后看是否正常监听；
```
- 预期原文/缺口：
```text
业务故障案例 / UPFD 的N4 接口8805端口未侦听
UPFD 的N4 接口8805端口未侦听
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 症状现象
症状现象
终端无法正常建立会话；
N4偶联未建立；
UPF N4接口地址未配置；
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 信息收集
信息收集
检查UPF N4接口地址是否正常配置：使用upfmgr ctrl命令进入cli交互界面，执行show config 查看接口配置信息；
若接口地址正常配置：使用upfmgr bash命令进入pod，netstat -nap|grep 8805查看端口是否正常监听，若端口未正常监听查看日志信息tail -f /var/log/upf/upfd/upfd-gen.log；
业务故障案例 / UPFD 的N4 接口8805端口未侦听 / 解决方法
解决方法
若接口未正常配置，把接口地址配置完后再查看8805端口是否正常监听；
如接口地址配置正确，但是N4的8805端口仍然未正常监听，使用upfmgr restart命令重启upfd后看是否正常监听；
```

## log-001 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 pfcp_heartbeat_request 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:pfcp_heartbeat_request
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-3182914
- 来源：log-a698d029342259b7-3516922
- 来源：log-a698d029342259b7-3601293
- 原始日志：log-a698d029342259b7-3182914
- 定位：行15128 · 候选状态observed
```text
2025-05-15 09:10:45.375909 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- 原始日志：log-a698d029342259b7-3516922
- 定位：行17632 · 候选状态observed
```text
2025-05-15 09:11:09.253460 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- 原始日志：log-a698d029342259b7-3601293
- 定位：行18264 · 候选状态observed
```text
2025-05-15 09:11:15.376158 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-002 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 pfcp_heartbeat_request，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:pfcp_heartbeat_request
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-3182914
- 来源：log-a698d029342259b7-3516922
- 来源：log-a698d029342259b7-3601293
- 原始日志：log-a698d029342259b7-3182914
- 定位：行15128 · 候选状态observed
```text
2025-05-15 09:10:45.375909 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- 原始日志：log-a698d029342259b7-3516922
- 定位：行17632 · 候选状态observed
```text
2025-05-15 09:11:09.253460 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- 原始日志：log-a698d029342259b7-3601293
- 定位：行18264 · 候选状态observed
```text
2025-05-15 09:11:15.376158 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-003 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 pfcp_node_unreachable 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:pfcp_node_unreachable
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-5967589
- 来源：log-a698d029342259b7-5968078
- 来源：log-a698d029342259b7-6327317
- 原始日志：log-a698d029342259b7-5967589
- 定位：行30659 · 候选状态raised
```text
2025-05-21 20:57:10.493959 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- 原始日志：log-a698d029342259b7-5968078
- 定位：行30662 · 候选状态raised
```text
2025-05-21 20:57:10.494068 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- 原始日志：log-a698d029342259b7-6327317
- 定位：行32430 · 候选状态raised
```text
2025-07-12 01:00:46.637266 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-004 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 pfcp_node_unreachable，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:pfcp_node_unreachable
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-5967589
- 来源：log-a698d029342259b7-5968078
- 来源：log-a698d029342259b7-6327317
- 原始日志：log-a698d029342259b7-5967589
- 定位：行30659 · 候选状态raised
```text
2025-05-21 20:57:10.493959 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- 原始日志：log-a698d029342259b7-5968078
- 定位：行30662 · 候选状态raised
```text
2025-05-21 20:57:10.494068 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- 原始日志：log-a698d029342259b7-6327317
- 定位：行32430 · 候选状态raised
```text
2025-07-12 01:00:46.637266 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-005 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 far_handover 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:far_handover
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-12005
- 来源：log-a698d029342259b7-12283
- 来源：log-a698d029342259b7-12561
- 原始日志：log-a698d029342259b7-12005
- 定位：行101 · 候选状态observed
```text
2025-05-14 20:08:47.594133 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- 原始日志：log-a698d029342259b7-12283
- 定位：行102 · 候选状态observed
```text
2025-05-14 20:09:07.624673 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- 原始日志：log-a698d029342259b7-12561
- 定位：行103 · 候选状态observed
```text
2025-05-14 20:09:09.577742 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-006 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 far_handover，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:far_handover
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-12005
- 来源：log-a698d029342259b7-12283
- 来源：log-a698d029342259b7-12561
- 原始日志：log-a698d029342259b7-12005
- 定位：行101 · 候选状态observed
```text
2025-05-14 20:08:47.594133 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- 原始日志：log-a698d029342259b7-12283
- 定位：行102 · 候选状态observed
```text
2025-05-14 20:09:07.624673 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- 原始日志：log-a698d029342259b7-12561
- 定位：行103 · 候选状态observed
```text
2025-05-14 20:09:09.577742 FATAL FID.0 upfd_pfcp.c:6681(upfdUpdateFar): #GtpuNode# handover old ip: IP_ADDR to new ip: IP_ADDR. CAUSE farId:0x21700002 update, #session# {session: SESSION_MASKED dnn: DNN_MASKED,imsi: IMSI_MASKED,local seid: SEID_MASKED,local teid: TEID_MASKED}
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-007 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 gtpu_echo_retry 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:gtpu_echo_retry
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-14801
- 来源：log-a698d029342259b7-15588
- 来源：log-a698d029342259b7-16375
- 原始日志：log-a698d029342259b7-14801
- 定位：行113 · 候选状态observed
```text
2025-05-14 20:09:43.031831 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 1, count:0
```
- 原始日志：log-a698d029342259b7-15588
- 定位：行117 · 候选状态observed
```text
2025-05-14 20:09:48.036719 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 1, count:1
```
- 原始日志：log-a698d029342259b7-16375
- 定位：行121 · 候选状态observed
```text
2025-05-14 20:09:52.040343 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 2, count:0
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-008 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 gtpu_echo_retry，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:gtpu_echo_retry
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-14801
- 来源：log-a698d029342259b7-15588
- 来源：log-a698d029342259b7-16375
- 原始日志：log-a698d029342259b7-14801
- 定位：行113 · 候选状态observed
```text
2025-05-14 20:09:43.031831 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 1, count:0
```
- 原始日志：log-a698d029342259b7-15588
- 定位：行117 · 候选状态observed
```text
2025-05-14 20:09:48.036719 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 1, count:1
```
- 原始日志：log-a698d029342259b7-16375
- 定位：行121 · 候选状态observed
```text
2025-05-14 20:09:52.040343 ERROR FID.0 upfd_rq.c:807(upfdV4ResendQueue): resend gtpu echo req, peer ip: IP_ADDR, seqnum: 2, count:0
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-009 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 license_not_installed 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:license_not_installed
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-1683
- 来源：log-a698d029342259b7-4545
- 来源：log-a698d029342259b7-6728
- 原始日志：log-a698d029342259b7-1683
- 定位：行16 · 候选状态raised
```text
2025-05-14 16:07:43.723036 ERROR FID.0 upfd_alarm.c:816(upfdAlarmLicenseNotInstall): Report license not installed alarm
```
- 原始日志：log-a698d029342259b7-4545
- 定位：行41 · 候选状态cleared
```text
2025-05-14 16:17:05.649346 ERROR FID.0 upfd_alarm.c:823(upfdAlarmLicenseNotInstall): Clear license not installed alarm
```
- 原始日志：log-a698d029342259b7-6728
- 定位：行58 · 候选状态cleared
```text
2025-05-14 16:21:21.586574 ERROR FID.0 upfd_alarm.c:823(upfdAlarmLicenseNotInstall): Clear license not installed alarm
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-010 · dev · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 license_not_installed，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:license_not_installed
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-1683
- 来源：log-a698d029342259b7-4545
- 来源：log-a698d029342259b7-6728
- 原始日志：log-a698d029342259b7-1683
- 定位：行16 · 候选状态raised
```text
2025-05-14 16:07:43.723036 ERROR FID.0 upfd_alarm.c:816(upfdAlarmLicenseNotInstall): Report license not installed alarm
```
- 原始日志：log-a698d029342259b7-4545
- 定位：行41 · 候选状态cleared
```text
2025-05-14 16:17:05.649346 ERROR FID.0 upfd_alarm.c:823(upfdAlarmLicenseNotInstall): Clear license not installed alarm
```
- 原始日志：log-a698d029342259b7-6728
- 定位：行58 · 候选状态cleared
```text
2025-05-14 16:21:21.586574 ERROR FID.0 upfd_alarm.c:823(upfdAlarmLicenseNotInstall): Clear license not installed alarm
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-011 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 pfcp_heartbeat_response 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:pfcp_heartbeat_response
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-3183220
- 来源：log-a698d029342259b7-3517228
- 来源：log-a698d029342259b7-3601599
- 原始日志：log-a698d029342259b7-3183220
- 定位：行15131 · 候选状态observed
```text
2025-05-15 09:10:45.375964 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc02:1706:406::, msg len:16
```
- 原始日志：log-a698d029342259b7-3517228
- 定位：行17635 · 候选状态observed
```text
2025-05-15 09:11:09.253518 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc01:1706:406::, msg len:16
```
- 原始日志：log-a698d029342259b7-3601599
- 定位：行18267 · 候选状态observed
```text
2025-05-15 09:11:15.376211 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc02:1706:406::, msg len:16
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-012 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 pfcp_heartbeat_response，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:pfcp_heartbeat_response
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-3183220
- 来源：log-a698d029342259b7-3517228
- 来源：log-a698d029342259b7-3601599
- 原始日志：log-a698d029342259b7-3183220
- 定位：行15131 · 候选状态observed
```text
2025-05-15 09:10:45.375964 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc02:1706:406::, msg len:16
```
- 原始日志：log-a698d029342259b7-3517228
- 定位：行17635 · 候选状态observed
```text
2025-05-15 09:11:09.253518 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc01:1706:406::, msg len:16
```
- 原始日志：log-a698d029342259b7-3601599
- 定位：行18267 · 候选状态observed
```text
2025-05-15 09:11:15.376211 DEBUG FID.0 upfd_pfcp.c:2112(upfdPfcpMsgEntryHeartBeatReq): Send #MsgHeartbeat# Rsp to cp node:2408:8142:60ff:fc02:1706:406::, msg len:16
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-013 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 pfcp_session_deleted 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:pfcp_session_deleted
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-13071
- 来源：log-a698d029342259b7-13725
- 来源：log-a698d029342259b7-14379
- 原始日志：log-a698d029342259b7-13071
- 定位：行105 · 候选状态observed
```text
2025-05-14 20:09:33.531692 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 1
```
- 原始日志：log-a698d029342259b7-13725
- 定位：行108 · 候选状态observed
```text
2025-05-14 20:09:37.047651 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 2
```
- 原始日志：log-a698d029342259b7-14379
- 定位：行111 · 候选状态observed
```text
2025-05-14 20:09:40.981915 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 3
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-014 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 pfcp_session_deleted，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:pfcp_session_deleted
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-13071
- 来源：log-a698d029342259b7-13725
- 来源：log-a698d029342259b7-14379
- 原始日志：log-a698d029342259b7-13071
- 定位：行105 · 候选状态observed
```text
2025-05-14 20:09:33.531692 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 1
```
- 原始日志：log-a698d029342259b7-13725
- 定位：行108 · 候选状态observed
```text
2025-05-14 20:09:37.047651 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 2
```
- 原始日志：log-a698d029342259b7-14379
- 定位：行111 · 候选状态observed
```text
2025-05-14 20:09:40.981915 FATAL FID.0 upfd_pm.c:588(upf_free_reason_stats_counter): free reason: 'success pfcp delete req' stats: 3
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-015 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 interface_index_failure 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:interface_index_failure
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-2080
- 来源：log-a698d029342259b7-2632
- 来源：log-a698d029342259b7-6998
- 原始日志：log-a698d029342259b7-2080
- 定位：行19 · 候选状态observed
```text
2025-05-14 16:08:18.611476 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- 原始日志：log-a698d029342259b7-2632
- 定位：行24 · 候选状态observed
```text
2025-05-14 16:08:18.614064 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- 原始日志：log-a698d029342259b7-6998
- 定位：行60 · 候选状态observed
```text
2025-05-14 16:21:22.503527 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-016 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 interface_index_failure，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:interface_index_failure
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-2080
- 来源：log-a698d029342259b7-2632
- 来源：log-a698d029342259b7-6998
- 原始日志：log-a698d029342259b7-2080
- 定位：行19 · 候选状态observed
```text
2025-05-14 16:08:18.611476 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- 原始日志：log-a698d029342259b7-2632
- 定位：行24 · 候选状态observed
```text
2025-05-14 16:08:18.614064 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- 原始日志：log-a698d029342259b7-6998
- 定位：行60 · 候选状态observed
```text
2025-05-14 16:21:22.503527 ERROR FID.0 upfd_main.c:5046(upfdGetVPPInterIndex): upf return error: iface index get fail!
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-017 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 n4_name_failure 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:n4_name_failure
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-4665
- 来源：log-a698d029342259b7-4848
- 来源：log-a698d029342259b7-5031
- 原始日志：log-a698d029342259b7-4665
- 定位：行42 · 候选状态observed
```text
2025-05-14 16:20:58.592356 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc1@*.*:' | awk -F: '{print $1}' failed
```
- 原始日志：log-a698d029342259b7-4848
- 定位：行43 · 候选状态observed
```text
2025-05-14 16:20:58.595262 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc2@*.*:' | awk -F: '{print $1}' failed
```
- 原始日志：log-a698d029342259b7-5031
- 定位：行44 · 候选状态observed
```text
2025-05-14 16:21:06.588513 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc1@*.*:' | awk -F: '{print $1}' failed
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-018 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 n4_name_failure，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:n4_name_failure
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-4665
- 来源：log-a698d029342259b7-4848
- 来源：log-a698d029342259b7-5031
- 原始日志：log-a698d029342259b7-4665
- 定位：行42 · 候选状态observed
```text
2025-05-14 16:20:58.592356 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc1@*.*:' | awk -F: '{print $1}' failed
```
- 原始日志：log-a698d029342259b7-4848
- 定位：行43 · 候选状态observed
```text
2025-05-14 16:20:58.595262 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc2@*.*:' | awk -F: '{print $1}' failed
```
- 原始日志：log-a698d029342259b7-5031
- 定位：行44 · 候选状态observed
```text
2025-05-14 16:21:06.588513 ERROR FID.0 upfd_main.c:1969(getN4CommIntfName): upf return error: get N4 comm name by cmd ifconfig | grep -o 'n4-svc1@*.*:' | awk -F: '{print $1}' failed
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-019 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：查询 gtpu_unreachable_detected 的代表日志，保留发生/解除/正常状态。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:gtpu_unreachable_detected
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-17561
- 来源：log-a698d029342259b7-19494
- 来源：log-a698d029342259b7-19720
- 原始日志：log-a698d029342259b7-17561
- 定位：行128 · 候选状态raised
```text
2025-05-14 20:09:58.045994 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- 原始日志：log-a698d029342259b7-19494
- 定位：行139 · 候选状态raised
```text
2025-05-14 20:10:07.005699 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- 原始日志：log-a698d029342259b7-19720
- 定位：行141 · 候选状态raised
```text
2025-05-14 20:10:11.009574 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## log-020 · heldout · log

- [ ] 问题及预期事实/相关证据已核对
- 问题：从日志原文核对 gtpu_unreachable_detected，说明能否据此确定独立故障和根因。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：log-template:gtpu_unreachable_detected
- synthetic：False
- 禁止结论：已确定根因；根据脱敏地址确定真实设备
- 来源：log-a698d029342259b7-17561
- 来源：log-a698d029342259b7-19494
- 来源：log-a698d029342259b7-19720
- 原始日志：log-a698d029342259b7-17561
- 定位：行128 · 候选状态raised
```text
2025-05-14 20:09:58.045994 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- 原始日志：log-a698d029342259b7-19494
- 定位：行139 · 候选状态raised
```text
2025-05-14 20:10:07.005699 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- 原始日志：log-a698d029342259b7-19720
- 定位：行141 · 候选状态raised
```text
2025-05-14 20:10:11.009574 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!
```
- 预期原文/缺口：
```text
消息数不等于独立故障数；源时区和真实身份未知，不能推断根因。
```

## topology-001 · dev · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 0：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:0
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_0.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-0:eth0 -> SYN-SW-0:port1; N3; synthetic
```

## topology-002 · dev · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 0：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:0
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_0.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-0:eth0 -> SYN-SW-0:port1; N3; synthetic
```

## topology-003 · dev · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 1：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:1
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_1.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-1:eth0 -> SYN-SW-1:port1; N3; synthetic
```

## topology-004 · dev · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 1：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:1
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_1.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-1:eth0 -> SYN-SW-1:port1; N3; synthetic
```

## topology-005 · dev · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 2：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:2
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_2.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-2:eth0 -> SYN-SW-2:port1; N3; synthetic
```

## topology-006 · dev · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 2：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:2
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_2.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-2:eth0 -> SYN-SW-2:port1; N3; synthetic
```

## topology-007 · heldout · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 3：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:3
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_3.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-3:eth0 -> SYN-SW-3:port1; N3; synthetic
```

## topology-008 · heldout · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 3：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:3
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_3.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-3:eth0 -> SYN-SW-3:port1; N3; synthetic
```

## topology-009 · heldout · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 4：查询 N3 邻接设备和端口；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:4
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_4.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-4:eth0 -> SYN-SW-4:port1; N3; synthetic
```

## topology-010 · heldout · topology

- [ ] 问题及预期事实/相关证据已核对
- 问题：合成拓扑样例 4：检查过期关系与 N30 是否能混作 N3；不能当作真实现场。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：synthetic-topology:4
- synthetic：True
- 禁止结论：已确认现场拓扑
- 来源：eval/p6/topology_synthetic_4.csv:row2
- 预期原文/缺口：
```text
SYN-UPF-4:eth0 -> SYN-SW-4:port1; N3; synthetic
```

## missing-001 · dev · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：当前 UPF 的 CPU 温度是多少？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:live-cpu
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-002 · dev · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：现在 UPF 的 CPU 负载是多少？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:live-cpu
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-003 · dev · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：UPF 9.9 版本如何配置 N3 接口？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:version-9
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-004 · dev · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：UPF 9.9 的 CLI 配置指令是什么？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:version-9
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-005 · heldout · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：没有日志文件，请诊断昨天的 UPF 中断。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:no-log
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-006 · heldout · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：未提供日志，能确认 UPF 昨日故障根因吗？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:no-log
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-007 · heldout · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：没有实际拓扑，请确定现场 N3 交换机端口。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:no-topology
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-008 · heldout · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：未提供现场连接表，UPF 连到哪台实际交换机？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:no-topology
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-009 · heldout · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：仅有脱敏日志，实际发生告警的是哪台真实设备？
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:no-identity
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

## missing-010 · heldout · missing

- [ ] 问题及预期事实/相关证据已核对
- 问题：请把掩码地址还原成实际 UPF 的设备身份。
- 结论：待复核
- 复核人：
- 日期：
- 修正意见：
- 分组：missing:no-identity
- synthetic：False
- 禁止结论：已接入实时网管；已还原真实设备
- 预期原文/缺口：
```text
应说明缺资料，不能模拟实时网管或猜测版本命令。
```

