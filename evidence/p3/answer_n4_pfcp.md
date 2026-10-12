问题：N4 PFCP 链路故障如何排查？
状态：partial

- 检查UPF链路是否异常，结合UPF组网图排查链路故障。 [chunk-f862dec7c5463231da13444f]
- 使用upfmgr bash命令进入pod内部，执行ip a检查网卡状态，使用ping命令检查自身IP、对端SMF N4接口地址及N4网关地址的连通性。 [chunk-0101383eb18f2d012e10d7a6, chunk-0101383eb18f2d012e10d7a6, chunk-0101383eb18f2d012e10d7a6, chunk-77beb9ec6530fb26ec9f73cd]
- 若N4链路异常，可尝试执行upfmgr restart命令重启upfd pod，再检查链路状态；若网关地址未配置，需添加UPF_N4_GW_IPv6_ADDRES配置。 [chunk-b3585cf70dc08b7a26681d9d, chunk-b3585cf70dc08b7a26681d9d]
- 待补充：证据版本为unknown，无法确认是否适用于 requested_version: 5.0
- 待补充：引用资料版本未知，无法确认对请求版本的适用性。

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。
提示：引用手册版本未知，需核对目标设备版本与操作前提。

来源 chunk-f862dec7c5463231da13444f：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：通用指引步骤 / 通用排查步骤
位置：word/document.xml/body/p[12], word/document.xml/body/p[13]/txbxContent[1]/p[1]

来源 chunk-0101383eb18f2d012e10d7a6：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 信息收集
位置：word/document.xml/body/p[202], word/document.xml/body/p[203], word/document.xml/body/p[204], word/document.xml/body/p[205]

来源 chunk-77beb9ec6530fb26ec9f73cd：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / UPF N4 IPv6 接口地址到网关链路异常 / 信息收集
位置：word/document.xml/body/p[217], word/document.xml/body/p[218], word/document.xml/body/p[219], word/document.xml/body/p[220]

来源 chunk-b3585cf70dc08b7a26681d9d：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / UPF N4 IPv6 接口地址到网关链路异常 / 解决方法
位置：word/document.xml/body/p[221], word/document.xml/body/p[222], word/document.xml/body/p[223], word/document.xml/body/p[224]
