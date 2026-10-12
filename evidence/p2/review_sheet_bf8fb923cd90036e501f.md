# P2 人工复核单 · bf8fb923cd90036e501f

请对照本地 `data/raw/` 原件和截图检查；机器 XML 回查已通过，不代表人工确认。
在每项下填写“通过 / 不通过 / 无法确认；问题与正确原文；复核人；日期”，通过才勾选。只需填写本文件，JSON 状态由程序维护者根据复核记录同步。

原始 DOCX 位于 [data/raw](../../data/raw/)；截图对应识别文字见 [OCR 逐行对照](ocr_review_text.md)。这一步只核对资料，不执行命令。

## 命令（20 条）

- [ ] 命令 01 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[390]`
  - 章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
  - 原文：cat >/etc/profile.d/coredump.sh<<EOF
  - 复核记录：

- [ ] 命令 02 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1096]`
  - 章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
  - 原文：UPF# show interface addr
  - 复核记录：

- [ ] 命令 03 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[380]`
  - 章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
  - 原文：mkdir -p /opt/local/tmp/core
  - 复核记录：

- [ ] 命令 04 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1485]`
  - 章节：安装5GC业务软件 / 基本配置说明 / 更换upfd镜像
  - 原文：kubectl -n ns1-ee0e0 delete pods -l app=upfd-1
  - 复核记录：

- [ ] 命令 05 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1793]`
  - 章节：部署FAQ / K8S集群软件故障排查 / 基本故障排查 / 集群安装问题
  - 原文：systemctl status containerd
  - 复核记录：

- [ ] 命令 06 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[395]`
  - 章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
  - 原文：source /etc/profile
  - 复核记录：

- [ ] 命令 07 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1022]`
  - 章节：安装5GC业务软件 / 单节点离线部署UPF / 安装补丁脚本 / 部署upfMonitor.sh
  - 原文：cp: './upfMonitor.sh' and '/opt/5gc/upfd/etc/upfMonitor.sh' are the same file
  - 复核记录：

- [ ] 命令 08 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1803]`
  - 章节：部署FAQ / K8S集群软件故障排查 / 基本故障排查 / Pod状态异常
  - 原文：kubectl -n <namespace> describe pods <pod-name>
  - 复核记录：

- [ ] 命令 09 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[410]`
  - 章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 配置UPF物理机 / 修改CPU中断配置
  - 原文：reboot
  - 复核记录：

- [ ] 命令 10 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1834]`
  - 章节：部署FAQ / K8S集群软件故障排查 / 基本故障排查 / 插件安装问题
  - 原文：helm -n openebs ls
  - 复核记录：

- [ ] 命令 11 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[177]`
  - 章节：产品配置 / CLI配置命令 / UPF系统能力 / 功能配置
  - 原文：set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
  - 复核记录：

- [ ] 命令 12 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[427]`
  - 章节：交付配置 / GRE隧道配置
  - 原文：ip route add {UE地址池网段} via gre3（业务运行前配置）
  - 复核记录：

- [ ] 命令 13 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[260]`
  - 章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能配置
  - 原文：UPFD> show cp-node
  - 复核记录：

- [ ] 命令 14 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[226]`
  - 章节：产品监控 / 业务信息监控 / 查询网元配置信息 / 功能配置
  - 原文：show config
  - 复核记录：

- [ ] 命令 15 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[277]/txbxContent[1]/p[1]`
  - 章节：业务故障案例 / UPF 到基站链路异常 / 信息收集
  - 原文：UPF# show interface addr
  - 复核记录：

- [ ] 命令 16 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[281]/txbxContent[1]/p[1]`
  - 章节：业务故障案例 / UPF 到基站链路异常 / 信息收集
  - 原文：UPF# show interface
  - 复核记录：

- [ ] 命令 17 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[253]/txbxContent[1]/p[1]`
  - 章节：业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 信息收集
  - 原文：UPF# show interface addr
  - 复核记录：

- [ ] 命令 18 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[13]/txbxContent[1]/p[3]`
  - 章节：通用指引步骤 / 通用排查步骤
  - 原文：ping <smf_ip>
  - 复核记录：

- [ ] 命令 19 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[128]/txbxContent[1]/p[2]`
  - 章节：业务故障案例 / N3N6接口地址未配置进data plane / 症状现象
  - 原文：UPFD> show config
  - 复核记录：

- [ ] 命令 20 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[19]/txbxContent[1]/p[1]`
  - 章节：通用指引步骤 / 通用处理步骤
  - 原文：upfmgr n4switch
  - 复核记录：

## 表行（20 条）

- [ ] 表行 01 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/tbl[1]/tr[1]`
  - 章节：目录 / 标识符号约定
  - 原文：符号	意义
  - 复核记录：

- [ ] 表行 02 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/tbl[8]/tr[1]`
  - 章节：安装准备 / 安装规划 / UPF节点IP规划 / UPF地址规划Bonding模式
  - 原文：节点	网口规划	网口	VLAN子接口	VLANID	IP规划	说明
  - 复核记录：

- [ ] 表行 03 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/tbl[13]/tr[8]`
  - 章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 确定网卡映射关系
  - 原文：N9光口上		ens1f0
  - 复核记录：

- [ ] 表行 04 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/tbl[21]/tr[2]`
  - 章节：安装5GC业务软件 / 单节点离线部署UPF / 上传upf安装包
  - 原文：1	servicePack-CU5GC_UPF_5.0.210.zip	UPF镜像及helm chart
  - 复核记录：

- [ ] 表行 05 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/tbl[24]/tr[27]`
  - 章节：网管纳管存量UPF / 填入存量UPF环境信息 / sheet3 (网元pod)填写
  - 原文：生产厂家manufacturer	自定义参数	默认为CUCC
  - 复核记录：

- [ ] 表行 06 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/tbl[7]/tr[1]`
  - 章节：产品配置 / 网管配置管理 / GRE隧道配置 / 功能配置
  - 原文：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
  - 复核记录：

- [ ] 表行 07 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/tbl[11]/tr[1]`
  - 章节：产品配置 / 网管配置管理 / PFCP定时器配置 / 功能配置
  - 原文：参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
  - 复核记录：

- [ ] 表行 08 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[2]/tr[4]`
  - 章节：2 网元配置（Configuration） / 2.2 UPF / 2.2.1 接口配置
  - 原文：IP地址类型		无
  - 复核记录：

- [ ] 表行 09 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[9]/tr[12]`
  - 章节：2 网元配置（Configuration） / 2.2 UPF / 2.2.5 系统配置 / 2.2.5.1 UPF功能特性
  - 原文：UDBC	UL/DL缓存控制
  - 复核记录：

- [ ] 表行 10 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[16]/tr[3]`
  - 章节：4 安全管理（Security Management） / 4.2 用户组管理 / 4.2.1 添加用户组
  - 原文：Create Time	创建时间
  - 复核记录：

- [ ] 表行 11 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[23]/tr[5]`
  - 章节：7 故障管理（Fault Management） / 7.2 历史告警 / 7.2.1 历史告警查询
  - 原文：NF ID	NF名
  - 复核记录：

- [ ] 表行 12 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[30]/tr[1]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.1 Manage-AMF / 8.2.1.3 Registration Update Procedure / 8.2.1.3.2 Registration Update Success
  - 原文：统计参数	说明
  - 复核记录：

- [ ] 表行 13 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[38]/tr[3]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.1 Manage-AMF / 8.2.1.8 Inter RAT Handover Procedure / 8.2.1.8.1 4G Handover To 5G
  - 原文：4G Handover To 5G Success		成功从4G切换到5G次数
  - 复核记录：

- [ ] 表行 14 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[44]/tr[5]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.1 Manage-AMF / 8.2.1.9 Service Base Interface Message / 8.2.1.9.5 Ue Context Management Registration Failed
  - 原文：Roaming Not Allowed	不允许漫游
  - 复核记录：

- [ ] 表行 15 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[47]/tr[12]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.1 Manage-AMF / 8.2.1.9 Service Base Interface Message / 8.2.1.9.8 Namf Communication Service
  - 原文：CreateUeContextRsp Send	创建UE上下文回复发送
  - 复核记录：

- [ ] 表行 16 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[51]/tr[14]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.1 Manage-AMF / 8.2.1.9 Service Base Interface Message / 8.2.1.9.12 Nnrf Service
  - 原文：NfDiscoveryReq Send		NF发现成功
  - 复核记录：

- [ ] 表行 17 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[54]/tr[11]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.1 Manage-AMF / 8.2.1.10 N2 Interface Message / 8.2.1.10.2 Outgoing Messages
  - 原文：Initial ContextSetup Request		下行RAN状态传递
  - 复核记录：

- [ ] 表行 18 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[63]/tr[4]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.2 Manage-SMF / 8.2.2.5 N7 Interface Measurement Data / 8.2.2.5.2 Modify SM Policy Number
  - 原文：Update SM Policy Fail Number	更新SM 策略请求失败的次数
  - 复核记录：

- [ ] 表行 19 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[73]/tr[6]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.5 N4 Node Level Procedures / 8.2.3.5.1 PFCP Assosication Related Statistics
  - 原文：association update request received	接收的关联更新请求
  - 复核记录：

- [ ] 表行 20 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/tbl[78]/tr[3]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.7 N4 Session Loading Statistics / 8.2.3.7.2 Live Session Statistic
  - 原文：current ipv6 session number	当前的ipv6会话数
  - 复核记录：

## 操作步骤（20 条）

- [ ] 操作步骤 01 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/tbl[4]/tr[4]/tc[2]/p[1]`
  - 章节：安装准备 / 硬件参数 / 物理机要求
  - 原文：1.3T
  - 复核记录：

- [ ] 操作步骤 02 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[546]`
  - 章节：安装K8S集群软件 / 单节点部署K8S / 调整集群配置 / 配置物理机绑核方案
  - 原文：确定物理机绑核方案
  - 复核记录：

- [ ] 操作步骤 03 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/tbl[16]/tr[5]/tc[8]/p[1]`
  - 章节：安装5GC业务软件 / 单节点离线部署UPF / 前置条件 / 纯5G场景节点规划
  - 原文：100.10.1.50/24
  - 复核记录：

- [ ] 操作步骤 04 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[995]`
  - 章节：安装5GC业务软件 / 单节点离线部署UPF / 安装UPF应用
  - 原文：解析config.yaml中的配置参数，用于脚本及helmfile.yaml
  - 复核记录：

- [ ] 操作步骤 05 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1716]`
  - 章节：网管纳管存量UPF / 添加系统信息
  - 原文：	点击系统管理子页面；
  - 复核记录：

- [ ] 操作步骤 06 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[2046]`
  - 章节：部署FAQ / K8S集群软件故障排查 / 插件维护管理 / sriov-network-operator
  - 原文：name：物理网卡的名称
  - 复核记录：

- [ ] 操作步骤 07 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[75]`
  - 章节：产品配置 / 网管配置管理 / IP地址池配置 / 功能配置
  - 原文：配置管理 > 基本配置 > 业务配置 > IP地址池配置
  - 复核记录：

- [ ] 操作步骤 08 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[249]`
  - 章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能描述
  - 原文：功能描述
  - 复核记录：

- [ ] 操作步骤 09 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[368]`
  - 章节：故障诊断 / 网管信令管理 / 信令跟踪任务创建 / 功能描述
  - 原文：功能描述
  - 复核记录：

- [ ] 操作步骤 10 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[422]`
  - 章节：3 设备管理（Device Management） / 3.1 系统服务管理
  - 原文：3.1 系统服务管理
  - 复核记录：

- [ ] 操作步骤 11 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[769]`
  - 章节：4 安全管理（Security Management） / 4.3 权限管理 / 4.3.2 权限类型 / 4.3.2.2删除权限类型
  - 原文：4.3.2.2删除权限类型
  - 复核记录：

- [ ] 操作步骤 12 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1123]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.1 Manage-AMF / 8.2.1.7 Intra RAT Handover Procedure / 8.2.1.7.2 N2 Handover
  - 原文：8.2.1.7.2 N2 Handover
  - 复核记录：

- [ ] 操作步骤 13 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1474]`
  - 章节：8 性能管理（Performance Management） / 8.2 Manage / 8.2.3 Manage-UPF / 8.2.3.9 Data Plane Packet Loss Statistics / 8.2.3.9.1 IP Packets Reassembly Timeout
  - 原文：8.2.3.9.1 IP Packets Reassembly Timeout
  - 复核记录：

- [ ] 操作步骤 14 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1688]`
  - 章节：11 K8S / 11.2集群管理 / 11.2.2查看集群信息 / 11.2.2.1集群详情
  - 原文：11.2.2.1集群详情
  - 复核记录：

- [ ] 操作步骤 15 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1902]`
  - 章节：12 其他系统功能 / 12.2 网管信息管理
  - 原文：12.2 网管信息管理
  - 复核记录：

- [ ] 操作步骤 16 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[57]/txbxContent[1]/p[2]`
  - 章节：系统平台故障案例 / upfmgr hc执行报错/UPF_OM_Inspect.sh: line 29 / 症状现象
  - 原文：/opt/5gc/upfd/etc/UPF_OM_Inspect.sh: line 29: /root/ylx-upf-5_CU5GC_UPF_25.03_IP.conf: No such file or directory
  - 复核记录：

- [ ] 操作步骤 17 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[133]`
  - 章节：业务故障案例 / N3N6接口地址未配置进data plane / 解决方法
  - 原文：手动修改index文件，如果能修复则找文件被改的原因。
  - 复核记录：

- [ ] 操作步骤 18 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[221]`
  - 章节：业务故障案例 / UPF N4 IPv6 接口地址到网关链路异常 / 解决方法
  - 原文：解决方法
  - 复核记录：

- [ ] 操作步骤 19 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[281]/txbxContent[1]/p[5]`
  - 章节：业务故障案例 / UPF 到基站链路异常 / 信息收集
  - 原文：                            tx packets        13730
  - 复核记录：

- [ ] 操作步骤 20 · `中国联通5G专网UPF紧急故障指引0429(1).docx` · `word/document.xml/body/p[303]/txbxContent[1]/p[17]`
  - 章节：业务故障案例 / UPF 到客户内网链路异常 / 信息收集
  - 原文：portf4/0/3 (up):
  - 复核记录：

## 截图 OCR（30 张）

- [ ] 截图 01 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1077]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/18e5f23d85f9a73e01ad3416da8934720b6d32c01d03f72377aa7376309ac2ed.png)；章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N4接口及IP配置
  - OCR 行数：52；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 02 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[200]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/d93979849672d11a4884de2150dc402478f09ca042a7310ab5687b1e3f50d805.png)；章节：安装并配置操作系统 / 新物理机预装配置 / 配置RAID阵列 / 将BIOS Setup界面配置成文本模式
  - OCR 行数：49；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 03 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1117]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/43be38ab72c78351f68168c6b24fd8c42f66c22de302a706f676e2bcb7380215.png)；章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
  - OCR 行数：106；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 04 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1562]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/6c7a208ef1225555d206e7703dab95f6e3c2670cac59f13628eed3ee146d09a3.png)；章节：9 配置管理（Configure Management） / 9.3 开局配置生成 / 9.3.2 配置UPF
  - OCR 行数：66；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 05 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[303]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/377526527cf39a6ceb5042783dc071ee1894c3fafa788b183d508a76d0dc90e3.png)；章节：2 网元配置（Configuration） / 2.2 UPF / 2.2.2 PFCP 配置 / 2.2.2.3 PFCP 偶联建立
  - OCR 行数：24；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 06 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[297]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/583b0cef2ee77ffa55c5cd7855a0794790e95f54c506551dd2cb114d2c33dbca.png)；章节：2 网元配置（Configuration） / 2.2 UPF / 2.2.2 PFCP 配置 / 2.2.2.3 PFCP 偶联建立
  - OCR 行数：19；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 07 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[382]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/b515315b943da363ce2c29a3b67c30c279c24d0f0fc7ad8150ecf2b20b62f4f7.png)；章节：2 网元配置（Configuration） / 2.2 UPF / 2.2.5 系统配置 / 2.2.5.1 UPF功能特性
  - OCR 行数：51；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 08 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[57]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/b7854e0961763dc23b11079e56570b7b5e62243661e1b1298e55696af8b6ab75.png)；章节：产品配置 / 网管配置管理 / 接口地址配置 / 功能配置
  - OCR 行数：60；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 09 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[61]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/549bad17d31ac219529ca90a1912d38dd975b0468aef7a40cf23a6a2ed1b903e.png)；章节：产品配置 / 网管配置管理 / 接口地址配置 / 功能配置
  - OCR 行数：56；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 10 · `中国联通5G专网UPF产品使用手册(1).docx` · `word/document.xml/body/p[84]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/1daa7a5b62a5821a8d0565fdd9905f7892b5fbaff353cf043b301ff5c7a85648.png)；章节：产品配置 / 网管配置管理 / IP地址池配置 / 功能配置
  - OCR 行数：49；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 11 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[389]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/c62df741549aee25069e8d1949596649bcd00b8e990edf610bcdc9222ace66f3.png)；章节：2 网元配置（Configuration） / 2.2 UPF / 2.2.5 系统配置 / 2.2.5.1 UPF功能特性
  - OCR 行数：34；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 12 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[285]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/ba5ff5dec309d081325a170c37c9011767ffd25ab7c569192776f2dfcda10f13.png)；章节：2 网元配置（Configuration） / 2.2 UPF / 2.2.2 PFCP 配置 / 2.2.2.1 PFCP属性
  - OCR 行数：7；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 13 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[264]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/41e7fe0488bfa6768d3ef0c053d4fc6f2f3213a9172884a44f3d2afd72e65cb1.png)；章节：安装并配置操作系统 / 新物理机预装配置 / IPMI地址配置
  - OCR 行数：30；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 14 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[895]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/b8ed3f8d4ad4746d48f7fede396e0c12ad8f25b232f4433368bfadc98d281af2.jpeg)；章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.11 确认告警
  - OCR 行数：135；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 15 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[921]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/46755ce9a26e108eee3f313e0f5c126f91ab95b403f6a63f1ba652e465c30011.png)；章节：7 故障管理（Fault Management） / 7.2 历史告警 / 7.2.3 历史告警下载
  - OCR 行数：145；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 16 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1123]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/b270a4d9c8e498e803ee688bc794dd5c693b09c83b6d58e5fa933d38a43aa34c.png)；章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
  - OCR 行数：82；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 17 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[908]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/35ee747b640de189c34859bbf0a4be9b5ea3af6f5511c7831a4213650f5b095f.jpeg)；章节：7 故障管理（Fault Management） / 7.2 历史告警 / 7.2.1 历史告警查询
  - OCR 行数：139；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 18 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[1083]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/02dfcfdaf07805fb9becdf50ee1cda45a35e5f05f38c7c3be5cd8d8aa4c7df88.png)；章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N4接口及IP配置
  - OCR 行数：57；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 19 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[197]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/04ccbcaff82a82ba41a88b1a4765c4c40979cfd1356c380f6ea07154fa080f11.png)；章节：安装并配置操作系统 / 新物理机预装配置 / 配置RAID阵列 / 启动服务器后，按[Del]进去BIOS界面
  - OCR 行数：24；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 20 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[407]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/c71ab1e00cc5e4487894130038c73d3ed35b9e2246ebb25c930ee24f50dbfc51.png)；章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 配置UPF物理机 / 修改CPU中断配置
  - OCR 行数：26；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 21 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1504]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/610183b87c67c858f24d562528e8e3ee124f2e79047dae34ea2974a739ad00a2.png)；章节：9 配置管理（Configure Management） / 9.1 配置导入与导出 / 9.1.1 配置导入
  - OCR 行数：49；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 22 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[842]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/e9d11104a04806e380b28abe7fa77d991044b5de8b0773f2bfb1ec55317b7f5d.jpeg)；章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
  - OCR 行数：153；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 23 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1534]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/dbed20e9c101ce5117fb11f3d957ff6778ccac53a8ab30b4b6e8219d693d220d.png)；章节：9 配置管理（Configure Management） / 9.2 配置备份与恢复 / 9.2.1 配置备份
  - OCR 行数：31；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 24 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1545]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/a8ce761bbe869451b6ff9ca246a58aab35f685c3d8cb0ebe8823703a6a931ead.png)；章节：9 配置管理（Configure Management） / 9.2 配置备份与恢复 / 9.2.3 配置下载
  - OCR 行数：34；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 25 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[270]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/a0dde79c146771561908870be7dded255bbbb1dd545aaf502124479c4473a573.png)；章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 远程登录IPMI
  - OCR 行数：26；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 26 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1540]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/6bc235b9c33485df5824e29472008ed51db0998b4d3123f0900519de7bb0a6ee.png)；章节：9 配置管理（Configure Management） / 9.2 配置备份与恢复 / 9.2.2 配置恢复
  - OCR 行数：34；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 27 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1550]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/c9265e256db1773f4facca0bec9b9df700f47c73fb6e52f960ab7e1dd674d070.png)；章节：9 配置管理（Configure Management） / 9.2 配置备份与恢复 / 9.2.4 配置删除
  - OCR 行数：34；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 28 · `UPF 5.0安装部署指导书(新网管版)(1).docx` · `word/document.xml/body/p[332]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/65405ae35bd6030e86971b460ddb533334cda6a41d178a395eb739fe5eeda49e.png)；章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 配置磁盘分区
  - OCR 行数：77；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 29 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1510]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/bfff4c928dcafb7ef233df10b375d65d45d8aa45ece53ae27af253eeb7a21b63.png)；章节：9 配置管理（Configure Management） / 9.1 配置导入与导出 / 9.1.2 配置导出
  - OCR 行数：34；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：

- [ ] 截图 30 · `5GC网管使用手册_V1.3_20220916(1).docx` · `word/document.xml/body/p[1515]/image[1]`
  - [查看原图](/home/huangxiaolin/upf-agent/data/p2/media/84ae592ca6071b0ecfa6c76c059c7e127bd7238ba15c575cfa201d5062e4891b.png)；章节：9 配置管理（Configure Management） / 9.1 配置导入与导出 / 9.1.3 配置下载
  - OCR 行数：29；重点核对：大小写、冒号/等号、连字符/下划线、I/l/1、O/0、IP地址、端口
  - 复核记录：
