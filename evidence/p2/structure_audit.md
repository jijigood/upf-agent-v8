# 60 条结构抽样核对

当前 generation：`c05fe621e37ebdb1c663`。20 命令、20 表行、20 操作步骤已进行助手原件/语义核对；人工签署仍为 0/60。
原件疑点单独保留，不把忠实抽取解释成原手册事实无误。

## 01 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[390]`
```text
cat >/etc/profile.d/coredump.sh<<EOF
```
此行是 heredoc 起始命令，不能把单行当成完整脚本；须连同同节 EOF 与脚本主体查看。
人工复核：待签署。

## 02 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[1096]`
```text
UPF# show interface addr
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 03 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[380]`
```text
mkdir -p /opt/local/tmp/core
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 04 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[1485]`
```text
kubectl -n ns1-ee0e0 delete pods -l app=upfd-1
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 05 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[1793]`
```text
systemctl status containerd
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 06 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[388]`
```text
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
```
core_pattern 原文以单独 % 结尾；提取忠实保留，不能自动推断丢失的格式字符。
人工复核：待签署。

## 07 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[1806]`
```text
kubectl -n <namespace> logs -f <pod-name>
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 08 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[1803]`
```text
kubectl -n <namespace> describe pods <pod-name>
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 09 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[410]`
```text
reboot
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 10 · command
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[1834]`
```text
helm -n openebs ls
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 11 · command
原件：`中国联通5G专网UPF产品使用手册(1).docx`；定位：`word/document.xml/body/p[177]`
```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 12 · command
原件：`中国联通5G专网UPF产品使用手册(1).docx`；定位：`word/document.xml/body/p[427]`
```text
ip route add {UE地址池网段} via gre3（业务运行前配置）
```
原文末尾含中文括号说明“业务运行前配置”；当前属于候选语法，不可直接作为可执行命令。
人工复核：待签署。

## 13 · command
原件：`中国联通5G专网UPF产品使用手册(1).docx`；定位：`word/document.xml/body/p[260]`
```text
UPFD> show cp-node
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 14 · command
原件：`中国联通5G专网UPF产品使用手册(1).docx`；定位：`word/document.xml/body/p[226]`
```text
show config
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 15 · command
原件：`中国联通5G专网UPF紧急故障指引0429(1).docx`；定位：`word/document.xml/body/p[25]/txbxContent[1]/p[1]`
```text
upfmgr restart
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 16 · command
原件：`中国联通5G专网UPF紧急故障指引0429(1).docx`；定位：`word/document.xml/body/p[281]/txbxContent[1]/p[1]`
```text
UPF# show interface
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 17 · command
原件：`中国联通5G专网UPF紧急故障指引0429(1).docx`；定位：`word/document.xml/body/p[239]/txbxContent[1]/p[1]`
```text
UPF# show bond
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 18 · command
原件：`中国联通5G专网UPF紧急故障指引0429(1).docx`；定位：`word/document.xml/body/p[128]/txbxContent[1]/p[22]`
```text
UPF# show interface addr
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 19 · command
原件：`中国联通5G专网UPF紧急故障指引0429(1).docx`；定位：`word/document.xml/body/p[303]/txbxContent[1]/p[1]`
```text
UPF# show interface addr
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 20 · command
原件：`中国联通5G专网UPF紧急故障指引0429(1).docx`；定位：`word/document.xml/body/p[13]/txbxContent[1]/p[6]`
```text
ping <n3_gateway_ip>
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 21 · table
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/tbl[1]/tr[1]`
```text
符号	意义
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 22 · table
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/tbl[8]/tr[1]`
```text
节点	网口规划	网口	VLAN子接口	VLANID	IP规划	说明
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 23 · table
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/tbl[13]/tr[8]`
```text
N9光口上		ens1f0
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 24 · table
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/tbl[21]/tr[2]`
```text
1	servicePack-CU5GC_UPF_5.0.210.zip	UPF镜像及helm chart
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 25 · table
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/tbl[24]/tr[27]`
```text
生产厂家manufacturer	自定义参数	默认为CUCC
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 26 · table
原件：`中国联通5G专网UPF产品使用手册(1).docx`；定位：`word/document.xml/body/tbl[7]/tr[1]`
```text
参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 27 · table
原件：`中国联通5G专网UPF产品使用手册(1).docx`；定位：`word/document.xml/body/tbl[11]/tr[1]`
```text
参数名称	参数值类型	取值范围	是否必选	默认值	参数说明
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 28 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[2]/tr[4]`
```text
IP地址类型		无
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 29 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[9]/tr[12]`
```text
UDBC	UL/DL缓存控制
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 30 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[16]/tr[3]`
```text
Create Time	创建时间
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 31 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[23]/tr[5]`
```text
NF ID	NF名
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 32 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[30]/tr[1]`
```text
统计参数	说明
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 33 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[38]/tr[3]`
```text
4G Handover To 5G Success		成功从4G切换到5G次数
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 34 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[44]/tr[5]`
```text
Roaming Not Allowed	不允许漫游
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 35 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[47]/tr[12]`
```text
CreateUeContextRsp Send	创建UE上下文回复发送
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 36 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[51]/tr[14]`
```text
NfDiscoveryReq Send		NF发现成功
```
原文将 NfDiscoveryReq Send 解释为 NF发现成功；请求发送与成功含义存在疑点，需业务复核原手册。
人工复核：待签署。

## 37 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[54]/tr[11]`
```text
Initial ContextSetup Request		下行RAN状态传递
```
Initial ContextSetup Request 的中文列为下行RAN状态传递；疑似原手册指标映射问题，不改写原始文档。
人工复核：待签署。

## 38 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[63]/tr[4]`
```text
Update SM Policy Fail Number	更新SM 策略请求失败的次数
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 39 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[73]/tr[6]`
```text
association update request received	接收的关联更新请求
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 40 · table
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/tbl[78]/tr[3]`
```text
current ipv6 session number	当前的ipv6会话数
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 41 · step
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[206]`
```text
选择Configuration Management
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 42 · step
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[316]`
```text
选择默认“Continue without updating”
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 43 · step
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[766]`
```text
检查K8s层面reservedSystemCpus配置
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 44 · step
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[1314]`
```text
执行以上脚本，会自动重新配置CNI及N4网络，并且重启UPF各个pod
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 45 · step
原件：`UPF 5.0安装部署指导书(新网管版)(1).docx`；定位：`word/document.xml/body/p[1738]`
```text
点击已同步ntp服务器右侧操作列的立刻同步按钮进行一次性时间同步。
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 46 · step
原件：`中国联通5G专网UPF产品使用手册(1).docx`；定位：`word/document.xml/body/p[300]`
```text
登录UPF物理机，打开终端
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 47 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[362]`
```text
查询步骤：从下拉框选择数据，点击“展示”即可。
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 48 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[466]`
```text
步骤：点击“Add Route”-->填写弹框中的配置信息-->点击“Add”按钮，添加成功。
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 49 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[570]`
```text
解锁：点击需要锁定的User Name的勾选框，点击“Unlock”按钮完成对用户的解锁。
```
Unlock 操作原文写“需要锁定的User Name”；动作是解锁，文字有原手册表述疑点。
人工复核：待签署。

## 50 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[657]`
```text
步骤：点击需要拷贝的用户的User Group Name弹出详情页（见图4-19），然后点击“Copy”按钮会弹出拷贝用户详情页，在弹窗中填写新的用户组名，完毕后，点击“Save”按钮完成用户组拷贝。
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 51 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[812]`
```text
步骤：点击“交换”按钮，切换安装包。
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 52 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[883]`
```text
步骤：点击自动确认按钮-->选择告警等级、告警类型、确认时间-->点击保存，达到指定时间后自动确认告警。
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 53 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[951]`
```text
步骤：点击确认按钮-->提示确认告警成功。
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 54 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[1549]`
```text
步骤：点击每一条列表信息的删除按钮，即可删除当前的配置，如图所示：
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 55 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[1675]`
```text
步骤：点击列表的修改按钮，在弹出框内修改所属局点、集群名称、显示名称、IP地址、端口、授权码，点击“Save”保存集群
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 56 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[1741]`
```text
步骤：点击列表中删除按钮，在弹出框内点击确定删除模板
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 57 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[1794]`
```text
步骤：在表格中点击Docker镜像名称，查看Docker镜像版本
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 58 · step
原件：`5GC网管使用手册_V1.3_20220916(1).docx`；定位：`word/document.xml/body/p[1874]`
```text
步骤：点击“Modify”，在弹出框内修改时间和时区，点击“Save”保存
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 59 · step
原件：`中国联通5G专网UPF紧急故障指引0429(1).docx`；定位：`word/document.xml/body/p[91]`
```text
执行上述命令后，检查/usr/lib/tmpfiles.d/tmp.conf文件是否已经在末尾添加x /tmp/lic
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。

## 60 · step
原件：`中国联通5G专网UPF紧急故障指引0429(1).docx`；定位：`word/document.xml/body/p[240]`
```text
检查/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf 有无配N3网关地址。
```
已核对原件定位、字符保留、类别与邻近上下文；不代表现场可执行或人工业务验收。
人工复核：待签署。
