# P6 开发草案模型答案对照

同一检索文件；机器检查与相关章节命中均不是人工业务正确率。
此处不包含heldout。旧草案兼容/预算实测，不是新版完整业务集成绩。
正式业务真值复核入口是eval/p6/business_v3/truth_review.md。

## command-001 · command

在‘检查upf 业务网络地址配置 / 检查所有接口地址’中，show 命令的原文写法是什么？

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：False

```text
UPF# show interface addr
UPF# show interface
```
引用：chunk-7186a25131ec3f73b59889b5, chunk-a8f5ff09d0cf29498ce8c9d0, chunk-2240fc70509e9a8763a0d4e8, chunk-7c368ab71b09d9c8ec2524fd

```text
BondEthernet0 (up):

UPF# show interface
```
引用：chunk-27ef72ccf4b8d59bfc1dffa3, chunk-66eebf965019c2bb84329aaf

### target

状态：completed；机器契约：True

```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址

show config
```
引用：chunk-b586b6d6c78e913d75bfa0b2, chunk-b586b6d6c78e913d75bfa0b2

## command-002 · command

请引用‘检查upf 业务网络地址配置 / 检查所有接口地址’中的命令 show config，保留占位符和参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
show config
UPF上 show config 可以确认配置成功。

UPF上 show config确认配置。UPF上抓包可以看到UPF开始发的asso req

表格：接口地址配置 / 功能配置

```
引用：chunk-b586b6d6c78e913d75bfa0b2, chunk-05b46622548cea41921ec8c4, chunk-174a818f8701a3268e3feec6, chunk-fafb030542846a960f60d97d

### target

状态：completed；机器契约：True

```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查所有接口地址

show config
```
引用：chunk-b586b6d6c78e913d75bfa0b2, chunk-b586b6d6c78e913d75bfa0b2

## command-003 · command

手册‘检查upf 业务网络地址配置 / 检查所有接口地址’如何使用 show？只摘录原文并说明示例适用范围。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：False

```text
UPF# show interface addr
```
引用：chunk-7186a25131ec3f73b59889b5

```text
UPF# show interface
BondEthernet0 (up):

BondEthernet1 (up):

port17/0/0 (up):

```
引用：chunk-a8f5ff09d0cf29498ce8c9d0, chunk-27ef72ccf4b8d59bfc1dffa3, chunk-27ef72ccf4b8d59bfc1dffa3, chunk-27ef72ccf4b8d59bfc1dffa3

```text
UPF# show hardware-interfaces port17/0/0
```
引用：chunk-4065867d9b809a1a9ef3d21b

### target

状态：failed；机器契约：False

## command-004 · command

核对 show config 在‘检查upf 业务网络地址配置 / 检查所有接口地址’中的原始语法，不把示例当现场参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
show config
```
引用：chunk-b586b6d6c78e913d75bfa0b2

```text
UPF# show interface addr
```
引用：chunk-7186a25131ec3f73b59889b5

```text
UPF# show interface
```
引用：chunk-a8f5ff09d0cf29498ce8c9d0

### target

状态：missing_source；机器契约：False

## command-005 · command

在‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’中，upfmgr 命令的原文写法是什么？

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：False

```text
# upfmgr ip qry

root@gd-gz-gdlt-upf01:~# upfmgr ip qry

```
引用：chunk-611060638cb88f44e6bbdfc9, chunk-f9722da50bf4f3243b27226e

### target

状态：missing_source；机器契约：False

## command-006 · command

请引用‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’中的命令 upfmgr data，保留占位符和参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
upfmgr data
```
引用：chunk-5f39f6e176cd5d50da043a23

```text
// 进CLI，upfmgr data
```
引用：chunk-fae3b3a752f928d12a123d27

```text
使用upfmgr data 命令进入vppctl 控制台，执行show interface addr 命令查看 N6 网卡（一般是BondEthernet1，或者BondEthernet1.400,子接口以具体规划为准）状态地址是否正常：
```
引用：chunk-3a86073cea37c9440d9e705a

### target

状态：missing_source；机器契约：False

## command-007 · command

手册‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’如何使用 upfmgr？只摘录原文并说明示例适用范围。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：failed；机器契约：False

### target

状态：failed；机器契约：False

## command-008 · command

核对 upfmgr data 在‘检查upf 业务网络地址配置 / 检查N3N6接口及IP配置’中的原始语法，不把示例当现场参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：failed；机器契约：False

### target

状态：missing_source；机器契约：False

## command-009 · command

在‘UPF系统能力 / 功能配置’中，set-upf-prt-sw 命令的原文写法是什么？

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>

```
引用：chunk-ed162186f81b734c927091f0

### target

状态：completed；机器契约：True

```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>

```
引用：chunk-ed162186f81b734c927091f0

## command-010 · command

请引用‘UPF系统能力 / 功能配置’中的命令 set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>，保留占位符和参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>

```
引用：chunk-ed162186f81b734c927091f0

### target

状态：completed；机器契约：True

```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>

```
引用：chunk-ed162186f81b734c927091f0

## command-011 · command

手册‘UPF系统能力 / 功能配置’如何使用 set-upf-prt-sw？只摘录原文并说明示例适用范围。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>

命令格式

```
引用：chunk-ed162186f81b734c927091f0, chunk-05b46622548cea41921ec8c4

```text
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；

gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。

```
引用：chunk-21b601c9353349f7eb3ab15c, chunk-21b601c9353349f7eb3ab15c

```text
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
UPFD> set-upf-prt-sw n4-prt-sw 4
```
引用：chunk-ed162186f81b734c927091f0, chunk-5508ad2ffaa25a9c28d1634f

### target

状态：partial；机器契约：True

```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>

upf日志打印级别设置
```
引用：chunk-ed162186f81b734c927091f0, chunk-05b46622548cea41921ec8c4

```text
n4-prt-sw: upf信令面日志打印级别设置。级别：fatal(1), error(2), alert(3), debug(4)；

gtpu-prt-sw: upf数据面日志打印级别设置。级别：off(0), on(1)。

```
引用：chunk-21b601c9353349f7eb3ab15c, chunk-21b601c9353349f7eb3ab15c

```text
相关说明：UPFD> set-upf-prt-sw n4-prt-sw 4
UPFD> set-upf-prt-sw n4-prt-sw 4
```
引用：chunk-ed162186f81b734c927091f0, chunk-5508ad2ffaa25a9c28d1634f

## command-012 · command

核对 set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4> 在‘UPF系统能力 / 功能配置’中的原始语法，不把示例当现场参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>

```
引用：chunk-ed162186f81b734c927091f0

### target

状态：partial；机器契约：True

```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>

```
引用：chunk-ed162186f81b734c927091f0

## command-013 · command

在‘配置UPF物理机 / Coredump开关打开’中，echo 命令的原文写法是什么？

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
引用：chunk-01998c8695e66a6318101bb8

```text
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
引用：chunk-01998c8695e66a6318101bb8

### target

状态：failed；机器契约：False

## command-014 · command

请引用‘配置UPF物理机 / Coredump开关打开’中的命令 echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern，保留占位符和参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
引用：chunk-01998c8695e66a6318101bb8

### target

状态：failed；机器契约：False

## command-015 · command

手册‘配置UPF物理机 / Coredump开关打开’如何使用 echo？只摘录原文并说明示例适用范围。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
引用：chunk-b7e7f004b9f94894131191dc, chunk-01998c8695e66a6318101bb8

```text
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开

```
引用：chunk-b7e7f004b9f94894131191dc, chunk-01998c8695e66a6318101bb8, chunk-da1f7676d2f30661bb5e00a8

```text
echo "kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%" > /etc/sysctl.d/coredump.conf
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
$ ulimit -a

```
引用：chunk-b7e7f004b9f94894131191dc, chunk-01998c8695e66a6318101bb8, chunk-3ecddf27a8093a17064a1a8a

### target

状态：failed；机器契约：False

## command-016 · command

核对 echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern 在‘配置UPF物理机 / Coredump开关打开’中的原始语法，不把示例当现场参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
echo "/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t" > /proc/sys/kernel/core_pattern
```
引用：chunk-01998c8695e66a6318101bb8

### target

状态：failed；机器契约：False

## command-017 · command

在‘逻辑口报文信息统计 / 统计N4口报文信息’中，tcpdump 命令的原文写法是什么？

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
引用：chunk-7fdde4d9a3c3a42036bffd3d

### target

状态：completed；机器契约：True

```text
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
引用：chunk-7fdde4d9a3c3a42036bffd3d

## command-018 · command

请引用‘逻辑口报文信息统计 / 统计N4口报文信息’中的命令 tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap，保留占位符和参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
引用：chunk-7fdde4d9a3c3a42036bffd3d

### target

状态：completed；机器契约：True

```text
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息

```
引用：chunk-7fdde4d9a3c3a42036bffd3d, chunk-7fdde4d9a3c3a42036bffd3d

## command-019 · command

手册‘逻辑口报文信息统计 / 统计N4口报文信息’如何使用 tcpdump？只摘录原文并说明示例适用范围。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
选择该端口，运行如下命令抓包
```
引用：chunk-7fdde4d9a3c3a42036bffd3d, chunk-cd469b95520a9da4928f8fa7

```text
登录UPF物理机，打开终端

查看N4IP在哪个端口

```
引用：chunk-cd469b95520a9da4928f8fa7, chunk-cd469b95520a9da4928f8fa7

```text
一段时间后，键入Ctrl+C停止抓包
```
引用：chunk-67083f7c25d8e6bb5ac216ee

### target

状态：partial；机器契约：True

```text
登录UPF物理机，打开终端

查看N4IP在哪个端口

选择该端口，运行如下命令抓包
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
引用：chunk-cd469b95520a9da4928f8fa7, chunk-cd469b95520a9da4928f8fa7, chunk-cd469b95520a9da4928f8fa7, chunk-7fdde4d9a3c3a42036bffd3d

```text
一段时间后，键入Ctrl+C停止抓包
```
引用：chunk-67083f7c25d8e6bb5ac216ee

## command-020 · command

核对 tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap 在‘逻辑口报文信息统计 / 统计N4口报文信息’中的原始语法，不把示例当现场参数。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
业务信息监控 / 逻辑口报文信息统计 / 统计N4口报文信息

```
引用：chunk-7fdde4d9a3c3a42036bffd3d, chunk-67083f7c25d8e6bb5ac216ee

### target

状态：completed；机器契约：True

```text
tcpdump -i {N4口逻辑ID} port 8805 -vv -w {数据包名}.pcap
```
引用：chunk-7fdde4d9a3c3a42036bffd3d

## knowledge-001 · knowledge

手册中‘物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 配置网口地址’的说明和关键字段是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
Gateway：必须设置

Name servers：必须设置，在离线环境没有DNS服务器时，该地址配置为Gateway地址
```
引用：chunk-e792107b5ba57b6b518b558d, chunk-e792107b5ba57b6b518b558d

```text
按照网络规划，配置网口地址，以配置eno1的静态地址为例：

说明：本步骤并非必须配置，之后可以通过修改netplan的配置文件实完成。需要跟进现网实际情况进行配置，示例仅给出参考：

```
引用：chunk-e792107b5ba57b6b518b558d, chunk-e792107b5ba57b6b518b558d

```text
各网口配置的IP地址仿照 REF _Toc5403 \n \h 2.2.3 REF _Toc5403 \h UPF节点IP规划，按照局点现场申请到的IP资源进行配置，其中N9接口是和N3接口共物理口部署，通过不同Vlan划分子接口进行区分。
```
引用：chunk-f524ca5abe39582dd582c6d5

### target

状态：completed；机器契约：True

```text
说明：本步骤并非必须配置，之后可以通过修改netplan的配置文件实完成。需要跟进现网实际情况进行配置，示例仅给出参考：

```
引用：chunk-e792107b5ba57b6b518b558d

```text
按照网络规划，配置网口地址，以配置eno1的静态地址为例：

```
引用：chunk-e792107b5ba57b6b518b558d

```text
参数说明：

Gateway：必须设置

Name servers：必须设置，在离线环境没有DNS服务器时，该地址配置为Gateway地址
```
引用：chunk-e792107b5ba57b6b518b558d, chunk-e792107b5ba57b6b518b558d, chunk-e792107b5ba57b6b518b558d

## knowledge-002 · knowledge

请依据‘物理机安装操作系统并配置 / 安装Ubuntu操作系统 / 配置网口地址’解释说明和关键字段，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
按照网络规划，配置网口地址，以配置eno1的静态地址为例：

Gateway：必须设置

Name servers：必须设置，在离线环境没有DNS服务器时，该地址配置为Gateway地址
```
引用：chunk-e792107b5ba57b6b518b558d, chunk-e792107b5ba57b6b518b558d, chunk-e792107b5ba57b6b518b558d

```text
局点现场获取到新服务器之后，需要先对服务器进行新物理机预装配置，预装配置包括新物理机接线，U盘启动盘制作，配置RAID阵列，配置IPMI地址。进一步地，安装Ubuntu22.04.2操作系统并配置。
对于全新的物理机服务器，在安装Ubuntu 22.04.2操作系统之前，需要先配置RAID阵列，配置IPMI地址等预装机配置。下面逐一阐述每个步骤：
```
引用：chunk-3912dfe744eb7e6aa847727f, chunk-d973015bdd2cb66d8e222e59

### target

状态：completed；机器契约：True

```text
说明：本步骤并非必须配置，之后可以通过修改netplan的配置文件实完成。需要跟进现网实际情况进行配置，示例仅给出参考：

```
引用：chunk-e792107b5ba57b6b518b558d

```text
Gateway：必须设置

Name servers：必须设置，在离线环境没有DNS服务器时，该地址配置为Gateway地址
```
引用：chunk-e792107b5ba57b6b518b558d, chunk-e792107b5ba57b6b518b558d

## knowledge-003 · knowledge

手册中‘物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）’的说明和关键字段是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
      interfaces:

        - enp61s0f0

        - enp61s0f1

        mode: 802.3ad                       #mode设置为4，交换机对应lacp-dynamic

```
引用：chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3

```text
    bond0.90:                               #规划的Bond子接口，用于K8s

      id: 90

      link: bond0

      addresses: [ 172.16.100.50/24 ]

```
引用：chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3

```text
用于K8s接口地址网络必须配置nameservers网关地址。后续部署K8s时需要，否则会有报错提示；

默认路由routes.default需要配置。后续部署K8s时需要，否则会有报错提示。
```
引用：chunk-c68506d4ec5e247b1185a691, chunk-c68506d4ec5e247b1185a691

### target

状态：failed；机器契约：False

## knowledge-004 · knowledge

请依据‘物理机安装操作系统并配置 / 配置netplan bond0口与bond0子接口（虚拟机跳过该步骤） / netplan Bond模式（现网部署配置）’解释说明和关键字段，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
其中enp61s0f0/enp61s0f1需根据实际部署情况选择需要做bonding的网口；

此处只需考虑N4、K8S和管理口共口部署，N3/N6/N9接口不需要在此处做bonding设置；

```
引用：chunk-c68506d4ec5e247b1185a691, chunk-c68506d4ec5e247b1185a691

```text
        mode: 802.3ad                       #mode设置为4，交换机对应lacp-dynamic

        mii-monitor-interval: 100

```
引用：chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3

```text
      addresses: [ 172.16.100.50/24 ]

        - to: default

          via: 172.16.100.1                   #规划的K8s地址网关

      nameservers:                         # DNS 服务器地址

```
引用：chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3, chunk-130842ca33fc1ee9055d1bc3

### target

状态：failed；机器契约：False

## knowledge-005 · knowledge

手册中‘单节点部署K8S / 调整集群配置 / 调整后的集群配置文件’的说明和关键字段是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：missing_source；机器契约：False

### target

状态：completed；机器契约：True

```text
部署集群前，需要新建并调整集群配置文件，当前集群自定义参数通过config.yaml文件进行配置。

```
引用：chunk-c0269e0f5f90744584380ab7

```text
hostname: 该主机需要配置的主机名

ntp_servers: 设置ntp服务器器的IP地址或域名

masters: 填写单节点IP地址
```
引用：chunk-b2994271d108a44a0af2c5c4, chunk-b2994271d108a44a0af2c5c4, chunk-b2994271d108a44a0af2c5c4

```text
networking：k8s podcidr以及service cidr

cpu_manager_policy：为UPFD启用CPU隔离

registry：5gc镜像仓库信息，配置集群与5gc registry仓库对接

ufw：防火墙信息，这里主要是配置放通的IP白名单

```
引用：chunk-cd18895bc25d33c17477326a, chunk-cd18895bc25d33c17477326a, chunk-cd18895bc25d33c17477326a, chunk-cd18895bc25d33c17477326a

## knowledge-006 · knowledge

请依据‘单节点部署K8S / 调整集群配置 / 调整后的集群配置文件’解释说明和关键字段，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
部署集群前，需要新建并调整集群配置文件，当前集群自定义参数通过config.yaml文件进行配置。

UPF节点名称：gd-gz-gdlt-upf01；

K8s地址：172.16.100.50；

物理机绑核方案：12-23, 29-47（本文档模板样例），或者是0-9,20-29；

```
引用：chunk-c0269e0f5f90744584380ab7, chunk-c0269e0f5f90744584380ab7, chunk-c0269e0f5f90744584380ab7, chunk-c0269e0f5f90744584380ab7

```text
hostname: gd-gz-gdlt-upf01           #UPF节点名称

  - 172.16.100.50                    #K8s 地址

  pod_subnet: 100.64.0.0/24

  service_subnet: 10.96.0.0/22

```
引用：chunk-c0269e0f5f90744584380ab7, chunk-c0269e0f5f90744584380ab7, chunk-c0269e0f5f90744584380ab7, chunk-c0269e0f5f90744584380ab7

```text
  prometheus:

    enabled: true

    https: false

```
引用：chunk-b2994271d108a44a0af2c5c4, chunk-b2994271d108a44a0af2c5c4, chunk-b2994271d108a44a0af2c5c4, chunk-b2994271d108a44a0af2c5c4

### target

状态：failed；机器契约：False

## knowledge-007 · knowledge

手册中‘单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件’的说明和关键字段是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
注意：现网环境需要根据实际服务器（如：H3C、Soc、中兴等）不同配置、不同网卡配置（ens16f0、ens16f1、enp24s0f0、enp24s0f1、ens1f0、ens3f0、ens3f0、ens3f1等）和VlanId规划等灵活调整实际的配置参数。

```
引用：chunk-ca730d6f31271f28eab01fa5

```text
  namespace: ns1                      # 设置UPF命令空间

  upf_version: 5.0.210                   # UPF软件包版本

  vdos_version: 1.0.5

  instanceId: "1"

```
引用：chunk-ca730d6f31271f28eab01fa5, chunk-ca730d6f31271f28eab01fa5, chunk-ca730d6f31271f28eab01fa5, chunk-ca730d6f31271f28eab01fa5

```text
  intf_mode: 1 # 0-seperated,1-combined  #UPF N4合设、分设模式选择：1表示合设

    enabled: false                       #默认配置为false，对端交换机配置为：动态lacp，Trunk

    id: 299                             #UPF N4 VlanId

    address: "100.101.1.55/24"

```
引用：chunk-881735f8ec04a52b4f3444a3, chunk-881735f8ec04a52b4f3444a3, chunk-881735f8ec04a52b4f3444a3, chunk-881735f8ec04a52b4f3444a3

### target

状态：missing_source；机器契约：False

## knowledge-008 · knowledge

请依据‘单节点离线部署UPF / 调整UPF配置（现网部署方式） / 调整后的配置文件’解释说明和关键字段，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
UPF命令空间。默认设置为ns1；

  namespace: ns1                      # 设置UPF命令空间

```
引用：chunk-e7842ebabe313127d0ade883, chunk-ca730d6f31271f28eab01fa5

```text
N3/N6/N4 对应网卡配置，根据服务器网卡配置填写，intf_mode默认是合设模式；

  intf_mode: 1 # 0-seperated,1-combined  #UPF N4合设、分设模式选择：1表示合设

n4.intf_mode：UPF N4合设、分设模式选择：1表示合设，0表示分设。

n4.bond.enabled：N4使用bond模式开关，即是否启用bond模式，如果为true则使用bond模式下的nic配置，此时networking.nic部分必须是2张网卡。

```
引用：chunk-e7842ebabe313127d0ade883, chunk-881735f8ec04a52b4f3444a3, chunk-4d32b50bac01142b9eb8c38b, chunk-4d32b50bac01142b9eb8c38b

```text
NEID具体值；

  neId: "559991"                       # 设置UPF NEID

```
引用：chunk-e7842ebabe313127d0ade883, chunk-ca730d6f31271f28eab01fa5, chunk-a3be36a9bb0bf67ddeca1d77

### target

状态：missing_source；机器契约：False

## knowledge-009 · knowledge

手册中‘单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址’的说明和关键字段是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
若网管未分配IP地址时可以手动配置，一般通过CURL命令配置接口地址。具体命令格式为：

curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "3", InterfaceType = "N3", IPAddressType = "IPv4", IPv4Address = "100.10.1.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "5", InterfaceType = "N6", IPAddressType = "IPv4", IPv4Address = "174.100.100.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "2", InterfaceType = "N4", IPAddressType = "IPv6", IPv6Address = "2404::4:50", IPv6PrefixLen = 64, VRFEnable = "OFF";}' 127.0.0.1
```
引用：chunk-90b8a37655128bab4cb85c5a, chunk-37015f8c510912ff3ba8d98a, chunk-013b7cb89c91edbafb296e8a, chunk-21dccc114177dcd35158f743

```text
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "3", InterfaceType = "N3", IPAddressType = "IPv4", IPv4Address = "100.10.1.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
引用：chunk-37015f8c510912ff3ba8d98a, chunk-e8683a340f2175d73a20ff1b

```text
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "5", InterfaceType = "N6", IPAddressType = "IPv4", IPv4Address = "174.100.100.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
引用：chunk-013b7cb89c91edbafb296e8a

### target

状态：failed；机器契约：False

## knowledge-010 · knowledge

请依据‘单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址’解释说明和关键字段，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
检查upf 业务网络地址配置
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址

curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "3", InterfaceType = "N3", IPAddressType = "IPv4", IPv4Address = "100.10.1.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
引用：chunk-0a6f7d1d943a62614770907f, chunk-37015f8c510912ff3ba8d98a, chunk-37015f8c510912ff3ba8d98a, chunk-349d0a04c0da3c79c5dab97b

```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址

curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "5", InterfaceType = "N6", IPAddressType = "IPv4", IPv4Address = "174.100.100.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
配置UPF各个接口地址

```
引用：chunk-013b7cb89c91edbafb296e8a, chunk-013b7cb89c91edbafb296e8a, chunk-90b8a37655128bab4cb85c5a, chunk-90b8a37655128bab4cb85c5a

```text
单节点离线部署UPF / 检查upf 业务网络地址配置 / 配置UPF各个接口地址

curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "2", InterfaceType = "N4", IPAddressType = "IPv6", IPv6Address = "2404::4:50", IPv6PrefixLen = 64, VRFEnable = "OFF";}' 127.0.0.1
```
引用：chunk-21dccc114177dcd35158f743, chunk-21dccc114177dcd35158f743

### target

状态：completed；机器契约：True

```text
若网管未分配IP地址时可以手动配置，一般通过CURL命令配置接口地址。具体命令格式为：

curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "5", InterfaceType = "N6", IPAddressType = "IPv4", IPv4Address = "174.100.100.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
引用：chunk-90b8a37655128bab4cb85c5a, chunk-013b7cb89c91edbafb296e8a

```text
curl -H "Content-Type:application/json" -H "User-Agent: okhttp/3.6.0" -H "Host: ns1.upf-1.com" -X POST -d '{ADD UpfIntfAddrConfig : InterfaceId = "3", InterfaceType = "N3", IPAddressType = "IPv4", IPv4Address = "100.10.1.50", IPv4Mask = "255.255.255.0", VRFEnable = "OFF";}' 127.0.0.1
```
引用：chunk-e8683a340f2175d73a20ff1b

```text
curl 命令配置完成后，需要重启UPFD 和UPFM 2个POD，具体命令为：

#kubectl delete pod upfm-1-b8fc7f485-hw47c -n ns1

#kubectl delete pod upfd-1-594847d77d-jg6ch -n ns1

```
引用：chunk-8af46eaef600a97d5dc3c07c, chunk-8af46eaef600a97d5dc3c07c, chunk-8af46eaef600a97d5dc3c07c

## troubleshooting-001 · troubleshooting

手册中‘K8S集群软件故障排查 / 基本故障排查 / ice网卡驱动’的排查步骤和操作前提是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
检查用于UPF的物理网卡状态，确认状态是否都为UP状态，发现其中eno4 状态为down，并且执行up命令无法启动

通过查找eno4 网卡PCI地址，执行dmesg查看日志，日志存在以下报错

以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```
引用：chunk-b6fb841cfccf4c91fa7d9f9e, chunk-b6fb841cfccf4c91fa7d9f9e, chunk-b6fb841cfccf4c91fa7d9f9e

```text
WingTech 服务器需要更新ICE网卡驱动，否则可能遇到以下问题：

以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```
引用：chunk-b6fb841cfccf4c91fa7d9f9e, chunk-b6fb841cfccf4c91fa7d9f9e

```text
通过查找eno4 网卡PCI地址，执行dmesg查看日志，日志存在以下报错

```
引用：chunk-b6fb841cfccf4c91fa7d9f9e

### target

状态：completed；机器契约：True

```text
检查用于UPF的物理网卡状态，确认状态是否都为UP状态，发现其中eno4 状态为down，并且执行up命令无法启动

通过查找eno4 网卡PCI地址，执行dmesg查看日志，日志存在以下报错

```
引用：chunk-b6fb841cfccf4c91fa7d9f9e, chunk-b6fb841cfccf4c91fa7d9f9e

```text
WingTech 服务器需要更新ICE网卡驱动，否则可能遇到以下问题：

以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```
引用：chunk-b6fb841cfccf4c91fa7d9f9e, chunk-b6fb841cfccf4c91fa7d9f9e

## troubleshooting-002 · troubleshooting

请依据‘K8S集群软件故障排查 / 基本故障排查 / ice网卡驱动’解释排查步骤和操作前提，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
WingTech 服务器需要更新ICE网卡驱动，否则可能遇到以下问题：

检查用于UPF的物理网卡状态，确认状态是否都为UP状态，发现其中eno4 状态为down，并且执行up命令无法启动

以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```
引用：chunk-b6fb841cfccf4c91fa7d9f9e, chunk-b6fb841cfccf4c91fa7d9f9e, chunk-b6fb841cfccf4c91fa7d9f9e

```text
检查用于UPF的物理网卡状态，确认状态是否都为UP状态，发现其中eno4 状态为down，并且执行up命令无法启动

通过查找eno4 网卡PCI地址，执行dmesg查看日志，日志存在以下报错

```
引用：chunk-b6fb841cfccf4c91fa7d9f9e, chunk-b6fb841cfccf4c91fa7d9f9e

```text
以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```
引用：chunk-b6fb841cfccf4c91fa7d9f9e

### target

状态：completed；机器契约：True

```text
WingTech 服务器需要更新ICE网卡驱动，否则可能遇到以下问题：

以上问题需要更新ICE网卡驱动解决，否则影响sriov对网卡的识别以及VF的生成。
```
引用：chunk-b6fb841cfccf4c91fa7d9f9e, chunk-b6fb841cfccf4c91fa7d9f9e

```text
检查用于UPF的物理网卡状态，确认状态是否都为UP状态，发现其中eno4 状态为down，并且执行up命令无法启动

```
引用：chunk-b6fb841cfccf4c91fa7d9f9e

```text
通过查找eno4 网卡PCI地址，执行dmesg查看日志，日志存在以下报错

```
引用：chunk-b6fb841cfccf4c91fa7d9f9e

## troubleshooting-003 · troubleshooting

手册中‘部署FAQ / K8S集群软件故障排查 / 插件维护管理’的排查步骤和操作前提是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
每个插件调用sealos run命令进行安装，插件安装失败时会给出错误提示，但不会终止整个安装流程，可以在安装完成后单独处理失败的插件，具体失败原因需要分析插件pod日志。

```
引用：chunk-1a09cca0adc6efedbe4ede47

```text
1.	首先检查helm是否已经成功下发openebs chart，并且STATUS为deployed

root@upf:~# helm -n openebs ls

NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION

openebs openebs         1               2023-03-30 11:16:53.302896372 +0800 CST deployed        openebs-3.3.1   3.3.0  

```
引用：chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47

```text
helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。

$ sealos run docker.io/labring/helm:v3.11.0

```
引用：chunk-73986e099325e6f5c5d27ac9, chunk-73986e099325e6f5c5d27ac9

### target

状态：partial；机器契约：True

```text
集群安装脚本默认能够自动安装所有启用的插件，下面主要介绍在集群安装完成后如何单独安装某个插件，以及如果管理插件的生命周期，例如查看插件运行状态，卸载插件等。

```
引用：chunk-76b3006ebf4d6634906ecd2a

```text
集群安装脚本默认能够自动安装所有启用的插件，下面主要介绍在集群安装完成后如何单独安装某个插件，以及如果管理插件的生命周期，例如查看插件运行状态，卸载插件等。

helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。

```
引用：chunk-76b3006ebf4d6634906ecd2a, chunk-73986e099325e6f5c5d27ac9

## troubleshooting-004 · troubleshooting

请依据‘部署FAQ / K8S集群软件故障排查 / 插件维护管理’解释排查步骤和操作前提，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
每个插件调用sealos run命令进行安装，插件安装失败时会给出错误提示，但不会终止整个安装流程，可以在安装完成后单独处理失败的插件，具体失败原因需要分析插件pod日志。

```
引用：chunk-1a09cca0adc6efedbe4ede47

```text
1.	首先检查helm是否已经成功下发openebs chart，并且STATUS为deployed

root@upf:~# helm -n openebs ls

NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION

openebs openebs         1               2023-03-30 11:16:53.302896372 +0800 CST deployed        openebs-3.3.1   3.3.0  

```
引用：chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47

```text
kubectl -n <namespace> describe pods <pod-name>
kubectl -n <namespace> logs -f <pod-name>
```
引用：chunk-5433f2361d7cbceae8092553, chunk-d228af64df28fdea95b91934

### target

状态：completed；机器契约：True

```text
集群安装脚本默认能够自动安装所有启用的插件，下面主要介绍在集群安装完成后如何单独安装某个插件，以及如果管理插件的生命周期，例如查看插件运行状态，卸载插件等。

helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。

```
引用：chunk-76b3006ebf4d6634906ecd2a, chunk-73986e099325e6f5c5d27ac9

```text
每个插件调用sealos run命令进行安装，插件安装失败时会给出错误提示，但不会终止整个安装流程，可以在安装完成后单独处理失败的插件，具体失败原因需要分析插件pod日志。

1.	首先检查helm是否已经成功下发openebs chart，并且STATUS为deployed

2.	检查openebs命名空间下的pod状态，查看STATUS列是否为Running

3.	如果pod状态异常，需要查看pod日志，分析定位具体原因，一般使用以下命令查看openebs pod日志

```
引用：chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47

```text
4.	相关问题解决后可以尝试删除openebs插件重新安装
helm -n openebs uninstall openebs
```
引用：chunk-1a09cca0adc6efedbe4ede47, chunk-c1617c5c3cf7294398ff805e

## troubleshooting-005 · troubleshooting

手册中‘K8S集群软件故障排查 / 插件维护管理 / Helm’的排查步骤和操作前提是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：failed；机器契约：False

### target

状态：completed；机器契约：True

```text
helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。

```
引用：chunk-73986e099325e6f5c5d27ac9

```text
执行以下命令安装helm插件

$ sealos run docker.io/labring/helm:v3.11.0

使用以下命令查看helm安装路径

$ which helm

```
引用：chunk-73986e099325e6f5c5d27ac9, chunk-73986e099325e6f5c5d27ac9, chunk-73986e099325e6f5c5d27ac9, chunk-73986e099325e6f5c5d27ac9

```text
如需卸载helm 插件，执行以下命令

$ rm -rf /usr/bin/helm
```
引用：chunk-73986e099325e6f5c5d27ac9, chunk-73986e099325e6f5c5d27ac9

## troubleshooting-006 · troubleshooting

请依据‘K8S集群软件故障排查 / 插件维护管理 / Helm’解释排查步骤和操作前提，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
每个插件调用sealos run命令进行安装，插件安装失败时会给出错误提示，但不会终止整个安装流程，可以在安装完成后单独处理失败的插件，具体失败原因需要分析插件pod日志。

```
引用：chunk-1a09cca0adc6efedbe4ede47

```text
1.	首先检查helm是否已经成功下发openebs chart，并且STATUS为deployed

2.	检查openebs命名空间下的pod状态，查看STATUS列是否为Running

3.	如果pod状态异常，需要查看pod日志，分析定位具体原因，一般使用以下命令查看openebs pod日志

```
引用：chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47, chunk-1a09cca0adc6efedbe4ede47

```text
helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。

前置要求：已安装能够提供动态持久卷的存储插件，例如openebs。

```
引用：chunk-73986e099325e6f5c5d27ac9, chunk-44dec42639466228f7fc64b8

### target

状态：completed；机器契约：True

```text
helm插件是一个二进制文件，默认安装在集群所有master节点的 /usr/bin目录下，大部分插件的安装依赖helm命令，因此部署集群后，应该首先安装helm插件。

```
引用：chunk-73986e099325e6f5c5d27ac9

```text
执行以下命令安装helm插件

$ sealos run docker.io/labring/helm:v3.11.0

使用以下命令查看helm安装路径

$ which helm

```
引用：chunk-73986e099325e6f5c5d27ac9, chunk-73986e099325e6f5c5d27ac9, chunk-73986e099325e6f5c5d27ac9, chunk-73986e099325e6f5c5d27ac9

```text
如需卸载helm 插件，执行以下命令

$ rm -rf /usr/bin/helm
```
引用：chunk-73986e099325e6f5c5d27ac9, chunk-73986e099325e6f5c5d27ac9

## troubleshooting-007 · troubleshooting

手册中‘K8S集群软件故障排查 / 插件维护管理 / ingress-nginx’的排查步骤和操作前提是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
$ helm -n ingress-nginx ls

$ kubectl -n ingress-nginx get pods 

$ kubectl -n ingress-nginx get svc

```
引用：chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2

```text
ingress-nginx：ingress网关插件，用于集群外部访问UPF

检查ingress-nginx插件是否已经安装，并且STATUS列显示为Running

sealos底层调用helm命令安装ingress-nginx插件，默认安装在ingress-nginx命名空间下，默认使用hostnetwork暴露ingress-nginx自身服务。

```
引用：chunk-df4636eabc07becc6fd71dcd, chunk-df4636eabc07becc6fd71dcd, chunk-dceca547ccdeb58f1bb4b7c2

```text
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/ingress-nginx-cucc:v1.6.4

$ helm -n ingress-nginx uninstall ingress-nginx
```
引用：chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2

### target

状态：completed；机器契约：True

```text
Ingress-nginx插件提供通过集群外部访问POD service的能力。

sealos底层调用helm命令安装ingress-nginx插件，默认安装在ingress-nginx命名空间下，默认使用hostnetwork暴露ingress-nginx自身服务。

```
引用：chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2

```text
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/ingress-nginx-cucc:v1.6.4

```
引用：chunk-dceca547ccdeb58f1bb4b7c2

```text
$ helm -n ingress-nginx ls

$ kubectl -n ingress-nginx get pods 

$ kubectl -n ingress-nginx get svc

$ helm -n ingress-nginx uninstall ingress-nginx
```
引用：chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2

## troubleshooting-008 · troubleshooting

请依据‘K8S集群软件故障排查 / 插件维护管理 / ingress-nginx’解释排查步骤和操作前提，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
Ingress-nginx插件提供通过集群外部访问POD service的能力。

```
引用：chunk-dceca547ccdeb58f1bb4b7c2

```text
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/ingress-nginx-cucc:v1.6.4

```
引用：chunk-dceca547ccdeb58f1bb4b7c2

```text
$ helm -n ingress-nginx ls

$ kubectl -n ingress-nginx get pods 

```
引用：chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2

### target

状态：completed；机器契约：True

```text
Ingress-nginx插件提供通过集群外部访问POD service的能力。

sealos底层调用helm命令安装ingress-nginx插件，默认安装在ingress-nginx命名空间下，默认使用hostnetwork暴露ingress-nginx自身服务。

```
引用：chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2

```text
$ helm -n ingress-nginx ls

$ kubectl -n ingress-nginx get pods 

$ kubectl -n ingress-nginx get svc

```
引用：chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2

```text
集群安装脚本默认能够自动安装所有启用的插件，下面主要介绍在集群安装完成后如何单独安装某个插件，以及如果管理插件的生命周期，例如查看插件运行状态，卸载插件等。

$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/ingress-nginx-cucc:v1.6.4

$ helm -n ingress-nginx uninstall ingress-nginx
```
引用：chunk-76b3006ebf4d6634906ecd2a, chunk-dceca547ccdeb58f1bb4b7c2, chunk-dceca547ccdeb58f1bb4b7c2

## troubleshooting-009 · troubleshooting

手册中‘K8S集群软件故障排查 / 插件维护管理 / multus-cni’的排查步骤和操作前提是什么？请给出原文依据。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
multus-cni 插件支持为pod附加多个网卡，sriov-network-operator插件依赖multus-cni，两者配合使用。

```
引用：chunk-85f751d548f2f48f2d49bd1c

```text
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/multus-cni:v3.9.3

$ kubectl -n kube-system get pods -l app=multus

$ kubectl -n kube-system delete ds kube-multus-ds
```
引用：chunk-85f751d548f2f48f2d49bd1c, chunk-85f751d548f2f48f2d49bd1c, chunk-85f751d548f2f48f2d49bd1c

### target

状态：failed；机器契约：False

## troubleshooting-010 · troubleshooting

请依据‘K8S集群软件故障排查 / 插件维护管理 / multus-cni’解释排查步骤和操作前提，不要推断真实设备当前状态。

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：completed；机器契约：True

```text
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/multus-cni:v3.9.3

sealos底层调用kubectl命令安装multus-cni插件，默认安装在kube-system命名空间下，pod以daemonset方式运行在所有节点上。

```
引用：chunk-85f751d548f2f48f2d49bd1c, chunk-85f751d548f2f48f2d49bd1c

```text
$ kubectl -n kube-system get pods -l app=multus

```
引用：chunk-85f751d548f2f48f2d49bd1c

```text
$ kubectl -n kube-system delete ds kube-multus-ds
```
引用：chunk-85f751d548f2f48f2d49bd1c

### target

状态：completed；机器契约：True

```text
multus-cni 插件支持为pod附加多个网卡，sriov-network-operator插件依赖multus-cni，两者配合使用。

```
引用：chunk-85f751d548f2f48f2d49bd1c

```text
sealos底层调用kubectl命令安装multus-cni插件，默认安装在kube-system命名空间下，pod以daemonset方式运行在所有节点上。

```
引用：chunk-85f751d548f2f48f2d49bd1c

```text
$ sealos run registry.cn-shenzhen.aliyuncs.com/cnmirror/multus-cni:v3.9.3

$ kubectl -n kube-system get pods -l app=multus

$ kubectl -n kube-system delete ds kube-multus-ds
```
引用：chunk-85f751d548f2f48f2d49bd1c, chunk-85f751d548f2f48f2d49bd1c, chunk-85f751d548f2f48f2d49bd1c

## missing-003 · missing

UPF 9.9 版本如何配置 N3 接口？

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：partial；机器契约：True

```text
网管界面，依次点击【配置管理】>【UPF】> 【接口地址配置】> 【添加】，进入业务口地址管理界面，如下图所示

其中，接口配置选择“N3”，IP地址类型选择“Ipv4”，IPv4地址填入规划的N3地址，按照《UPF安装部署指导书(h3c服务器版)_V3.3》2.2.3节IP规划，子网掩码填入“255.255.255.0”，配置完上述参数之后，点击执行，完成N3地址的配置。

```
引用：chunk-6b96204074b53ada6b717bf2, chunk-6b96204074b53ada6b717bf2

```text
其中，接口配置选择“N3”，IP地址类型选择“Ipv4”，IPv4地址填入规划的N3地址，按照《UPF安装部署指导书(h3c服务器版)_V3.3》2.2.3节IP规划，子网掩码填入“255.255.255.0”，配置完上述参数之后，点击执行，完成N3地址的配置。

参数名称：接口类型 | 参数值类型：枚举型 | 取值范围：N3,N6,N9,N4 | 是否必选：必选 | 默认值：无 | 参数说明：示例：N6

参数名称：IP地址类型 | 参数值类型：枚举型 | 取值范围：IPv4,IPv6 | 是否必选
```
引用：chunk-6b96204074b53ada6b717bf2, chunk-fafb030542846a960f60d97d, chunk-fafb030542846a960f60d97d

```text
注意：首次配置接口地址，N3、N4、N6三个服务化接口的ipv4地址必须配全！！！
```
引用：chunk-6b96204074b53ada6b717bf2

### target

状态：partial；机器契约：True

```text
网管界面，依次点击【配置管理】>【UPF】> 【接口地址配置】> 【添加】，进入业务口地址管理界面，如下图所示

```
引用：chunk-6b96204074b53ada6b717bf2

```text
其中，接口配置选择“N3”，IP地址类型选择“Ipv4”，IPv4地址填入规划的N3地址，按照《UPF安装部署指导书(h3c服务器版)_V3.3》2.2.3节IP规划，子网掩码填入“255.255.255.0”，配置完上述参数之后，点击执行，完成N3地址的配置。

```
引用：chunk-6b96204074b53ada6b717bf2

```text
注意：首次配置接口地址，N3、N4、N6三个服务化接口的ipv4地址必须配全！！！
```
引用：chunk-6b96204074b53ada6b717bf2

## missing-004 · missing

UPF 9.9 的 CLI 配置指令是什么？

- 人工相关性/完整性/版本/关键参数判断：待复核

### baseline

状态：missing_source；机器契约：True

### target

状态：partial；机器契约：True

```text
CLI命令的格式：命令由一行关键词组成，词语跟词语间用空格分开。CLI命令中的各个关键词有唯一解释。

 用户可以通过telnet命令进入CLI(Command Line Interface, 命令行界面)。使用输入的指令进行配置。通过 "?"获取输入提示。

```
引用：chunk-f526d9f9745532f316c7e439, chunk-f526d9f9745532f316c7e439

```text
set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>

show config

```
引用：chunk-ed162186f81b734c927091f0, chunk-af31d71436dfc30b6e215672

