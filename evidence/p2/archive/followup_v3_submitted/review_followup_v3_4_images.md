# P2 修正后复核 · 仅 4 张截图

原 v3 复核单保留不变：60 条结构样本通过，26 张截图通过；截图 01/07/17/20 不通过。已按提交的正确原文修正并由助手回查原图，本页仍需用户确认修正结果。

只需确认下面 4 项，可回复“4 项修正均通过”，或在此文件逐项勾选并记录问题；无需重做其余 86 项。原有 7 条模糊/遮挡行继续隔离，本轮未将 OCR 提升为权威命令或纳入 P3 索引。

GRUB 保留原始 OCR 段号和坐标，下方额外提供按原图拼接的配置行。

## 截图 01

- [x] 修正后的可见内容与原图一致
- 原图：[查看截图](/home/huangxiaolin/upf-agent/data/p2/media/18e5f23d85f9a73e01ad3416da8934720b6d32c01d03f72377aa7376309ac2ed.png)
- 定位：`word/document.xml/body/p[1077]/image[1]`
- 结论：通过
- 问题：无。已对照原图核对：003 行 `1: lo:`、023 行 `2: tunl0@NONE:`、030 行 `4: eth0@if655:` 三个接口索引号前缀在原图中确实存在；另核 039 行 `12: n4-svc@if10`、IPv6 段 `2404::5c77:4aff:fe3b:a443/64` 与原图一致。
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28

本轮修正的 OCR 段：

```text
003: 1: lo:
023: 2: tunl0@NONE:
030: 4: eth0@if655:
```

当前整张截图的 OCR 对照：

```text
001: root@upfd-1-77c9989f8b-99ts2:/5gc/upfd/bin# ip
002: a
003: 1: lo:
004: <LOOPBACK,UP,LOWER
005: UP>
006: mtu
007: 65536
008: qdisc noqueue state UNKNOWN group default qlen 1000
009: link/loopback
010: 00:00:00:00:00:00
011: brd
012: 00:00:00:00:00:00
013: inet 127.0.0.1/8 scope host lo
014: valid_lft
015: forever preferred_lft forever
016: inet6
017: ::1/128
018: scope
019: host
020: valid
021: lft
022: forever preferred_lft forever
023: 2: tunl0@NONE:
024: <NOARP>
025: mtu 1480 qdisc noop state DOWN group default qlen 1000
026: link/ipip
027: 0.0.0.0
028: brd
029: 0.0.0.0
030: 4: eth0@if655:
031: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1480 qdisc noqueue state UP group default qlen 1000
032: link/ether
033: 4a:bb:73:9b:e8:7d brd ff:ff:ff:ff:ff:ff link-netnsid
034: 0
035: inet 100.64.0.165/32 scope global eth0
036: valid_lft forever preferred_lft forever
037: inet6 fe80::48bb:73ff:fe9b:e87d/64 scope link
038: valid_lft forever preferred_lft forever
039: 12:
040: n4-svc@if10: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
041: link/ether 5e:77:4a:3b:a4:43 brd ff:ff:ff:ff:ff:ff link-netnsid 0
042: inet 100.101.1.50/24 brd 100.101.1.255 scope global n4-svc
043: valid_lft forever preferred_lft forever
044: inet6 2404::4:50/64 scope global
045: valid_lft forever preferred_lft forever
046: inet6 2404::5c77:4aff:fe3b:a443/64 scope global dynamic mngtmpaddr
047: valid_lft forever preferred_lft
048: forever
049: inet6 fe80::5c77:4aff:fe3b:a443/64
050: scope link
051: valid_lft forever preferred_lft
052: forever
```

## 截图 07

- [x] 修正后的可见内容与原图一致
- 原图：[查看截图](/home/huangxiaolin/upf-agent/data/p2/media/b515315b943da363ce2c29a3b67c30c279c24d0f0fc7ad8150ecf2b20b62f4f7.png)
- 定位：`word/document.xml/body/p[382]/image[1]`
- 结论：通过（本轮修正确认；附 1 条残留问题请下轮处理）
- 问题：本轮修正（027 行 `EMPU(结束标记发送)` 补回右括号）与原图一致，已确认。另请复核：016 行原图实际为 `PFDM(PFD管理程序)`（第二字母为 F，与同排 `FTUP` 的 F 同形），现有 OCR 文本仍作 `PEDM`，疑为残留 E/F 误识；建议下轮修正，不影响本轮签署。
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28

本轮修正的 OCR 段：

```text
027: EMPU(结束标记发送)
```

当前整张截图的 OCR 对照：

```text
001: 配置>UPF>广州黄埔区>test5822>k8s_upf1_177>UPF配置>UPF功能特性
002: 默认UP功能特性
003: 额外UP功能特性1
004: 额外UP功能特性2
005: BUCP（CP功能中的下行数据缓冲）
006: DDND（下行数据通知）
007: true
008: <
009: true
010: DLBD（DL缓冲持续时间）
011: TRST(Traffic Steering）
012: false
013: false
014: V
015: FTUP（UP功能中的F-TEID分配/释放）
016: PEDM（PFD管理程序）
017: true
018: V
019: false
020: V
021: HEEU（上行流量的头增强）
022: TREU（UP功能中的强制流量重定向）
023: true
024: <
025: false
026: V
027: EMPU(结束标记发送)
028: PDIU(PDI优化）
029: true
030: V
031: false
032: V
033: UDBC（UL/DL缓存控制）
034: QUOAC（达到配额时应用配额操作）
035: false
036: V
037: true
038: V
039: TRACE(跟踪)
040: FRRT(帧路由)
041: false
042: true
043: 7
044: V
045: PFDE(PFD Contents IE包括具有多个值
046: EPFAR（增强PFCP的偶联释放）
047: 的属性)
048: true
049: V
050: false
051: 修改
```

## 截图 17

- [x] 修正后的可见内容与原图一致
- 原图：[查看截图](/home/huangxiaolin/upf-agent/data/p2/media/35ee747b640de189c34859bbf0a4be9b5ea3af6f5511c7831a4213650f5b095f.jpeg)
- 定位：`word/document.xml/body/p[908]/image[1]`
- 结论：通过
- 问题：无。已对照原图核对：040 行统计行 `Critical 0 / Major 111 / Minor 0`（红/黄/蓝圆点两侧计数）、042 列头 `Alarm Info`、046 列头 `Limit Set`、049 列头 `Alarm Remarks` / 右侧被裁切为 `Ack Nar`，均与原图一致；NF ID 列冒号写法 `192.168.16.79:9100` 亦与原图一致。
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28

本轮修正的 OCR 段：

```text
040: Critical 0  Major 111  Minor 0
042: Alarm Info
046: Limit Set
049: Alarm Remarks Ack Nar
```

当前整张截图的 OCR 对照：

```text
001: Alarm / History Alarm
002: NF Type
003: Region
004: Point
005: NF ID
006: Select Alarm Level
007: Select Alarm Type
008: Start
009: End
010: 全部
011: V
012: 全部
013: V
014: 全部
015: V
016: 全部
017: V
018: 全部
019: V
020: 全部
021: √
022: 2022-07-25 16:30:44
023: B
024: 2022-07-26 16:30:44
025: Alarm Code
026: Alarm NE ID
027: Alarm Sync Mode
028: 全部
029: V
030: ALL
031: V
032: Q Query
033: Remarks
034: Download
035: Print
036: Level Edit
037: C Sync
038: AutoAckConfig
039: CancelAutoAckConfig
040: Critical 0  Major 111  Minor 0
041: Alarm LevelvAlarm CodevAlarm Type
042: Alarm Info
043: NF Type NF ID
044: Region Point
045: Cluster Event Time
046: Limit Set
047: Alarm Status
048: End Time
049: Alarm Remarks Ack Nar
050: 机器
051: major
052: 45501
053: SystemAlarm
054: 192.168.16.79:9100
055: UPF
056: 192.168.16.79:9100
057: 2022-07-26
058: Cleared
059: 2022-07-26
060: 。
061: cpu已用超过设定
062: 16:07:02
063: 16:07:42
064: 值
065: 机器
066: 。
067: major
068: 45501
069: SystemAlarm
070: 192.168.16.79:9100
071: UPF
072: 192.168.16.79:9100
073: 2022-07-26
074: Cleared
075: 2022-07-26
076: cpu已用超过设定
077: 15:10:02
078: 16:05:42
079: 值
080: 机器
081: 。
082: major
083: 45501
084: SystemAlarm
085: 192.168.16.79:9100
086: UPF
087: 2022-07-26
088: Cleared
089: 2022-07-26
090: cpu已用超过设定
091: 192.168.16.79:9100
092: 14:39:02
093: 15:05:42
094: 值
095: 机器
096: 。
097: 45501
098: SystemAlarm
099: 192.168.16.79:9100
100: UPF
101: 2022-07-26
102: Cleared
103: 2022-07-26
104: major
105: cpu已用超过设定
106: 192.168.16.79:9100
107: 14:09:12
108: 14:37:42
109: 值
110: 机器
111: 45501
112: SystemAlarm
113: 192.168.16.79:9100
114: UPF
115: 192.168.16.79:9100
116: 2022-07-26
117: Cleared
118: 2022-07-26
119: 。
120: major
121: cpu已用超过设定
122: 13:14:32
123: 14:05:32
124: 值
125: 机器
126: 。
127: major
128: 45501
129: SystemAlarm
130: 192.168.16.79:9100
131: UPF
132: 192.168.16.79:9100
133: 2022-07-26
134: Cleared
135: 2022-07-26
136: cpu已用超过设定
137: 13:07:02
138: 13:13:12
139: 值
```

## 截图 20

- [x] 修正后的可见内容与原图一致
- 原图：[查看截图](/home/huangxiaolin/upf-agent/data/p2/media/c71ab1e00cc5e4487894130038c73d3ed35b9e2246ebb25c930ee24f50dbfc51.png)
- 定位：`word/document.xml/body/p[407]/image[1]`
- 结论：通过
- 问题：无。已对照原图逐行核对：第 6 行 `GRUB_DEFAULT=0`、第 7 行 `GRUB_TIMEOUT_STYLE=hidden`、第 8 行 `GRUB_TIMEOUT=0`、第 9 行 `GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian``（含 `lsb_release` 下划线与 `||`）、第 10 行 `GRUB_CMDLINE_LINUX_DEFAULT=""`（单等号，无双等号）、第 11 行 `GRUB_CMDLINE_LINUX="irqaffinity=0,10 noirqbalance"`（红框内），与原图逐字符一致。
- 复核人：AI辅助复核（待人工签名）
- 日期：2026-09-28

本轮修正的 OCR 段：

```text
015:  || echo Debian`
020: ""
002: GRUB_
005: GRUB_
006: TIMEOUT_
009: GRUB_
012: GRUB_
017: GRUB_
018: CMDLINE_
019: LINUX_DEFAULT=
022: GRUB_
023: CMDLINE_
```

按原图恢复的完整配置行（不是可直接执行的脚本）：

```text
GRUB_DEFAULT=0
GRUB_TIMEOUT_STYLE=hidden
GRUB_TIMEOUT=0
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT=""
GRUB_CMDLINE_LINUX="irqaffinity=0,10 noirqbalance"
```

当前整张截图的 OCR 对照：

```text
001: 6
002: GRUB_
003: DEFAULT=0
004: 7
005: GRUB_
006: TIMEOUT_
007: STYLE=hidden
008: 8
009: GRUB_
010: TIMEOUT=0
011: 9
012: GRUB_
013: DISTRIBUTOR=`lsb_release
014:  -i -s 2> /dev/null
015:  || echo Debian`
016: 10
017: GRUB_
018: CMDLINE_
019: LINUX_DEFAULT=
020: ""
021: 11
022: GRUB_
023: CMDLINE_
024: LINUX=
025: "irqaffinity=0,10 noirqbalance"
026: 12
```

