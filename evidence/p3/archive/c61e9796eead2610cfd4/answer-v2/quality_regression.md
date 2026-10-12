# P3 本地问答回归

只衡量状态、引用原文、固定关键字和拒答契约；不是人工业务准确率或正式测试集验收。
{"cases": 16, "machine_contract_pass": 15, "quote_integrity_pass": 16, "generation_failed": 1, "human_semantic_completed": 0}

## answer-01
问题：如何执行 show cp-node 查询对端 SMF 信息？
状态：partial

- 执行 show cp-node 命令可查询对端SMF信息。 [chunk-a95707dc20bc358dc01eba2e, chunk-8c359c6b97c3c3bb5bfa01d9, chunk-bbf13cab6aca8034ef1d180e, chunk-bcfb4b79a1fc297be1d1d5e6]
- 该命令需在 telnet 0 37100 连接的 upfd 调试台中输入。 [chunk-a95707dc20bc358dc01eba2e, chunk-da79f1572c8b981ab1f34446]
- 命令执行后可查看对端SMF的CP-IP-ADDR、NODE-ID、ASSO-STATUS等信息。 [chunk-9e79662334e774bfb1b81c4b, chunk-9e79662334e774bfb1b81c4b]
- 待补充：所请求的版本为5.0，但所有证据版本均为unknown，无法确认该操作在5.0版本中是否适用。
- 待补充：引用资料版本未知，无法确认对请求版本的适用性。

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。
提示：引用手册版本未知，需核对目标设备版本与操作前提。

来源 chunk-a95707dc20bc358dc01eba2e：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能配置
位置：word/document.xml/body/p[257]

来源 chunk-8c359c6b97c3c3bb5bfa01d9：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能配置
位置：word/document.xml/body/p[260]

来源 chunk-bbf13cab6aca8034ef1d180e：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / 偶联建立失败：SMF open upf开关 / 信息收集
位置：word/document.xml/body/p[115], word/document.xml/body/p[116], word/document.xml/body/p[117]

来源 chunk-bcfb4b79a1fc297be1d1d5e6：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / UPF 终端负载情况异常 / 信息收集
位置：word/document.xml/body/p[328]/txbxContent[1]/p[2], word/document.xml/body/p[329], word/document.xml/body/p[330]

来源 chunk-da79f1572c8b981ab1f34446：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能配置
位置：word/document.xml/body/p[251], word/document.xml/body/p[252], word/document.xml/body/p[253], word/document.xml/body/p[254], word/document.xml/body/p[255]

来源 chunk-9e79662334e774bfb1b81c4b：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能配置
位置：word/document.xml/body/p[261], word/document.xml/body/p[262], word/document.xml/body/p[263]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": true, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-02
问题：show config 用于查询哪些网元配置信息？
状态：completed

- show config 命令用于查询UPF的网元配置信息，包括N3、N6、N9、N4接口的IPv4/IPv6地址、CP IP地址、UE IPv4地址池配置、IP地址池名称及类型等。 [chunk-1a48b47560e5aec2eb0b8ce6, chunk-1a48b47560e5aec2eb0b8ce6, chunk-1a48b47560e5aec2eb0b8ce6, chunk-1a48b47560e5aec2eb0b8ce6]
- show config 命令可在UPF物理机终端通过telnet 0 37100进入upfd调试台后执行，用于查看当前网元配置。 [chunk-c590bc00f87ad7cae47ce7d4, chunk-c590bc00f87ad7cae47ce7d4]
- show config 命令可用于确认IP地址池配置和接口地址配置是否生效，如N3、N6地址配置后可通过该命令查看。 [chunk-5606f53468d9a54c876eb7de, chunk-d4340ab4f0ea6f40f65fc77c]
- 待补充：版本适用性未确认，证据版本为unknown

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。
提示：引用手册版本未知，需核对目标设备版本与操作前提。

来源 chunk-1a48b47560e5aec2eb0b8ce6：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询网元配置信息 / 功能配置
位置：word/document.xml/body/p[230], word/document.xml/body/p[231], word/document.xml/body/p[232], word/document.xml/body/p[233], word/document.xml/body/p[234], word/document.xml/body/p[235], word/document.xml/body/p[236], word/document.xml/body/p[237], word/document.xml/body/p[238], word/document.xml/body/p[239], word/document.xml/body/p[240], word/document.xml/body/p[241], word/document.xml/body/p[242], word/document.xml/body/p[243], word/document.xml/body/p[244], word/document.xml/body/p[245], word/document.xml/body/p[246], word/document.xml/body/p[247]

来源 chunk-c590bc00f87ad7cae47ce7d4：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询网元配置信息 / 功能配置
位置：word/document.xml/body/p[217], word/document.xml/body/p[218], word/document.xml/body/p[219], word/document.xml/body/p[220], word/document.xml/body/p[221], word/document.xml/body/p[223], word/document.xml/body/p[224]

来源 chunk-5606f53468d9a54c876eb7de：中国联通5G专网UPF产品使用手册(1).docx
章节：产品配置 / 网管配置管理 / IP地址池配置 / 功能配置
位置：word/document.xml/body/p[73], word/document.xml/body/p[74], word/document.xml/body/p[75], word/document.xml/body/p[76], word/document.xml/body/p[77], word/document.xml/body/p[78]

来源 chunk-d4340ab4f0ea6f40f65fc77c：中国联通5G专网UPF产品使用手册(1).docx
章节：产品配置 / 网管配置管理 / 接口地址配置 / 功能配置
位置：word/document.xml/body/p[50], word/document.xml/body/p[51], word/document.xml/body/p[52], word/document.xml/body/p[53], word/document.xml/body/p[54]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-03
问题：set-upf-prt-sw 的参数格式是什么？
状态：completed

- set-upf-prt-sw 命令的参数格式为：set-upf-prt-sw (n4-prt-sw | gtpu-prt-sw) <level=0:4>。 [chunk-ed162186f81b734c927091f0]
- n4-prt-sw 参数用于设置UPF信令面日志打印级别，取值范围为：fatal(1)、error(2)、alert(3)、debug(4)。 [chunk-21b601c9353349f7eb3ab15c]
- gtpu-prt-sw 参数用于设置UPF数据面日志打印级别，取值范围为：off(0)、on(1)。 [chunk-21b601c9353349f7eb3ab15c]
- 待补充：证据版本为unknown，无法确认该参数格式适用于具体版本。

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。
提示：引用手册版本未知，需核对目标设备版本与操作前提。

来源 chunk-ed162186f81b734c927091f0：中国联通5G专网UPF产品使用手册(1).docx
章节：产品配置 / CLI配置命令 / UPF系统能力 / 功能配置
位置：word/document.xml/body/p[177]

来源 chunk-21b601c9353349f7eb3ab15c：中国联通5G专网UPF产品使用手册(1).docx
章节：产品配置 / CLI配置命令 / UPF系统能力 / 功能配置
位置：word/document.xml/body/p[178], word/document.xml/body/p[179], word/document.xml/body/p[180], word/document.xml/body/p[182]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": true, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-04
问题：N4 IPv6 到 SMF 链路不通应收集什么信息？
状态：partial

- 应使用upfmgr bash命令进入pod内部，执行ip a命令查看网卡状态是否正常，可使用ping命令ping自身IP检查自己的IP状态是否正常。 [chunk-56ec8a20dfecb151d3a6e382, chunk-fb7ad782d3b7f73e77f1b25b]
- 应使用ping命令ping对端SMF的N4接口地址IP，检查是否正常响应。 [chunk-56ec8a20dfecb151d3a6e382]
- 应使用ping命令检查到UPF N4网关地址是否正常响应。 [chunk-56ec8a20dfecb151d3a6e382, chunk-fb7ad782d3b7f73e77f1b25b]
- 待补充：版本适用性未确认，证据版本为unknown

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。
提示：引用手册版本未知，需核对目标设备版本与操作前提。

来源 chunk-56ec8a20dfecb151d3a6e382：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / UPF N4 IPv6 接口地址到 SMF 链路异常 / 信息收集
位置：word/document.xml/body/p[202], word/document.xml/body/p[203], word/document.xml/body/p[204], word/document.xml/body/p[205]

来源 chunk-fb7ad782d3b7f73e77f1b25b：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / UPF N4 IPv6 接口地址到网关链路异常 / 信息收集
位置：word/document.xml/body/p[217], word/document.xml/body/p[218], word/document.xml/body/p[219], word/document.xml/body/p[220]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-05
问题：UPF N6 IPv4 到网关不通应如何处理？
状态：partial

- 若检查发现自身IP地址状态异常，首先尝试执行 `upfmgr restart` 命令重启upfd pod后再检查到UPF N6网关是否正常。 [chunk-153f077d0acebd6573a938ab, chunk-5ec751e7281d9c8ea6ae8357]
- 若检查UPF N6网关地址不通，首先联系交换机运维人员排查交换机接口有无收到N6接口的数据报文。 [chunk-153f077d0acebd6573a938ab, chunk-5ec751e7281d9c8ea6ae8357]
- 若检查发现 `/root/${HOSTNAME}_CU5GC_UPF_${VERSION}_IP.conf` 未配置 `UPF_N6_GW_IPv4_ADDRES` 网关地址，则需添加该配置。 [chunk-153f077d0acebd6573a938ab, chunk-5ec751e7281d9c8ea6ae8357]
- 待补充：证据版本为unknown，无法确认该处理流程是否适用于指定版本。

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。
提示：引用手册版本未知，需核对目标设备版本与操作前提。

来源 chunk-153f077d0acebd6573a938ab：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / UPF N6 IPv4 接口地址到网关链路异常 / 解决方法
位置：word/document.xml/body/p[260], word/document.xml/body/p[261], word/document.xml/body/p[262], word/document.xml/body/p[263]

来源 chunk-5ec751e7281d9c8ea6ae8357：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / UPF 到客户内网链路异常 / 解决方法
位置：word/document.xml/body/p[315], word/document.xml/body/p[316], word/document.xml/body/p[317], word/document.xml/body/p[318], word/document.xml/body/p[319]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-06
问题：UPF 5.0 物理机如何打开 Coredump？
状态：completed

- 打开Coredump需执行命令：echo 'kernel.core_pattern=/opt/local/tmp/core/core_%h_%e_%p_%i_%s_%t' > /etc/sysctl.d/coredump.conf [chunk-b7e7f004b9f94894131191dc]
- 需配置ulimit参数以允许无限大小的core文件：ulimit -S -c unlimited [chunk-08f63c658d0f9d9de2335551]
- 需设置系统级coredump限制：echo '* soft core unlimited' > /etc/security/limits.d/coredump.conf 和 echo '* hard core unlimited' > /etc/security/limits.d/coredump.conf [chunk-97617917b877529323000733, chunk-97617917b877529323000733]

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

来源 chunk-b7e7f004b9f94894131191dc：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
位置：word/document.xml/body/p[388]

来源 chunk-08f63c658d0f9d9de2335551：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
位置：word/document.xml/body/p[391], word/document.xml/body/p[392], word/document.xml/body/p[393]

来源 chunk-97617917b877529323000733：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装并配置操作系统 / 物理机安装操作系统并配置 / 配置UPF物理机 / Coredump开关打开
位置：word/document.xml/body/p[383], word/document.xml/body/p[384], word/document.xml/body/p[385]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-07
问题：5GC网管 V1.3 实时告警在哪里查询？
状态：completed

- 5GC网管 V1.3 的实时告警可在 Alarm-->Active Alarm 路径下查询。 [chunk-0d555a667d8458f08194b6fa, chunk-e4853f57767ab702e0cb20e7, chunk-8155920f16768dca1cb872d8, chunk-a014cd03bfc802738d470de9]
- 查询实时告警的步骤为：在各个下拉框中选择选项，点击“Query Alarm”或“Refresh”，查询结果将在列表中显示。 [chunk-0d555a667d8458f08194b6fa, chunk-e4853f57767ab702e0cb20e7]
- 实时告警页面支持通过 NF Type、Region、Point、NF ID、Alarm Level、Alarm Type、Start 时间、End 时间、Alarm Code、Alarm Ne ID、Alarm Sync Mode 和 Alarm Info 等配置项进行筛选查询。 [chunk-a014cd03bfc802738d470de9, chunk-a014cd03bfc802738d470de9, chunk-a014cd03bfc802738d470de9, chunk-a014cd03bfc802738d470de9]

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

来源 chunk-0d555a667d8458f08194b6fa：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
位置：word/document.xml/body/p[839], word/document.xml/body/p[840], word/document.xml/body/p[841], word/document.xml/body/p[843], word/document.xml/body/p[844]

来源 chunk-e4853f57767ab702e0cb20e7：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.7 刷新告警
位置：word/document.xml/body/p[871], word/document.xml/body/p[872], word/document.xml/body/p[873], word/document.xml/body/p[875]

来源 chunk-8155920f16768dca1cb872d8：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.3 告警下载
位置：word/document.xml/body/p[851], word/document.xml/body/p[852], word/document.xml/body/p[853], word/document.xml/body/p[855]

来源 chunk-a014cd03bfc802738d470de9：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
位置：word/document.xml/body/tbl[22]/tr[2], word/document.xml/body/tbl[22]/tr[3], word/document.xml/body/tbl[22]/tr[4], word/document.xml/body/tbl[22]/tr[5], word/document.xml/body/tbl[22]/tr[6], word/document.xml/body/tbl[22]/tr[7], word/document.xml/body/tbl[22]/tr[8], word/document.xml/body/tbl[22]/tr[9], word/document.xml/body/tbl[22]/tr[10], word/document.xml/body/tbl[22]/tr[11], word/document.xml/body/tbl[22]/tr[12], word/document.xml/body/tbl[22]/tr[13]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": true, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-08
问题：5GC网管如何查询历史告警？
状态：completed

- 在5GC网管V1.3版本中，查询历史告警的路径为：Alarm-->History Alarm。 [chunk-a528fb300a44cacc043b895f, chunk-e419fcbf253aa038abee8bcf, chunk-60eaacce4241c4248095b1e4, chunk-dd2e543b1b103c701f4ecda2]
- 在历史告警查询页面，可通过选择NF Type（NF类型）、Region（区域）、Point（局点）、NF ID（NF名）等配置项进行筛选查询。 [chunk-661622cf6af43287238b3f1f, chunk-661622cf6af43287238b3f1f, chunk-661622cf6af43287238b3f1f, chunk-661622cf6af43287238b3f1f]
- 查询历史告警的步骤为：在各个下拉框中选择选项，然后点击“Query”，查询结果将在列表中显示。 [chunk-a528fb300a44cacc043b895f, chunk-661622cf6af43287238b3f1f]

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

来源 chunk-a528fb300a44cacc043b895f：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.2 历史告警 / 7.2.1 历史告警查询
位置：word/document.xml/body/p[905], word/document.xml/body/p[906], word/document.xml/body/p[907], word/document.xml/body/p[909], word/document.xml/body/p[911], word/document.xml/body/p[912]

来源 chunk-e419fcbf253aa038abee8bcf：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.2 历史告警 / 7.2.3 历史告警下载
位置：word/document.xml/body/p[918], word/document.xml/body/p[919], word/document.xml/body/p[920], word/document.xml/body/p[922]

来源 chunk-60eaacce4241c4248095b1e4：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.2 历史告警 / 7.2.4 打印历史告警
位置：word/document.xml/body/p[923], word/document.xml/body/p[924], word/document.xml/body/p[925], word/document.xml/body/p[927]

来源 chunk-dd2e543b1b103c701f4ecda2：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.2 历史告警 / 7.2.9 确认历史告警
位置：word/document.xml/body/p[949], word/document.xml/body/p[950], word/document.xml/body/p[951], word/document.xml/body/p[954]

来源 chunk-661622cf6af43287238b3f1f：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.2 历史告警 / 7.2.1 历史告警查询
位置：word/document.xml/body/tbl[23]/tr[2], word/document.xml/body/tbl[23]/tr[3], word/document.xml/body/tbl[23]/tr[4], word/document.xml/body/tbl[23]/tr[5], word/document.xml/body/tbl[23]/tr[6], word/document.xml/body/tbl[23]/tr[7], word/document.xml/body/tbl[23]/tr[8], word/document.xml/body/tbl[23]/tr[9], word/document.xml/body/tbl[23]/tr[10], word/document.xml/body/tbl[23]/tr[11], word/document.xml/body/tbl[23]/tr[12], word/document.xml/body/tbl[23]/tr[13]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": true, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-09
问题：网管如何建立 PFCP 偶联？
状态：completed

- 在网管中建立PFCP偶联的路径为：Configuration → UPF → 区域名称 → 局点名称 → NF名称 → UPF Configuration → PFCP Configuration → PFCP 偶联建立。 [chunk-2ae84b0b3caa15b8bea991cd]
- 建立PFCP偶联时，需在输入框中填入SMF ID，然后点击“查询”按钮。 [chunk-2ae84b0b3caa15b8bea991cd]
- PFCP偶联建立支持添加、修改和删除操作，添加时点击“添加”按钮，填写表单后点击保存即可。 [chunk-2ae84b0b3caa15b8bea991cd, chunk-2ae84b0b3caa15b8bea991cd]

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

来源 chunk-2ae84b0b3caa15b8bea991cd：5GC网管使用手册_V1.3_20220916(1).docx
章节：2 网元配置（Configuration） / 2.2 UPF / 2.2.2 PFCP 配置 / 2.2.2.3 PFCP 偶联建立
位置：word/document.xml/body/p[293], word/document.xml/body/p[294], word/document.xml/body/p[295], word/document.xml/body/p[298], word/document.xml/body/p[300], word/document.xml/body/p[302], word/document.xml/body/p[304], word/document.xml/body/p[306]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-10
问题：UPF 5.0 怎样检查 N3N6 接口和 IP 地址？
状态：completed

- 进入upfd pod后，可通过执行`UPF# show interface addr`命令查看N3N6接口的IP配置。 [chunk-7186a25131ec3f73b59889b5, chunk-a3845a8d6d582d25a6c91232]
- 通过执行`UPF# show interface`命令可查看VPP接口信息，确认N3N6接口状态及IP地址配置。 [chunk-a8f5ff09d0cf29498ce8c9d0, chunk-27ef72ccf4b8d59bfc1dffa3]
- 使用`UPF# ping 174.100.100.1`和`UPF# ping 100.10.1.1`测试N3N6接口与网关的连通性，验证IP配置是否正常。 [chunk-cf3d3bb155ff05c4e0809464, chunk-8424f0e01f9e2107b966e55a]

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

来源 chunk-7186a25131ec3f73b59889b5：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
位置：word/document.xml/body/p[1096]

来源 chunk-a3845a8d6d582d25a6c91232：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
位置：word/document.xml/body/p[1093], word/document.xml/body/p[1094], word/document.xml/body/p[1095]

来源 chunk-a8f5ff09d0cf29498ce8c9d0：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
位置：word/document.xml/body/p[1115]

来源 chunk-27ef72ccf4b8d59bfc1dffa3：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
位置：word/document.xml/body/p[1097], word/document.xml/body/p[1098], word/document.xml/body/p[1099], word/document.xml/body/p[1100], word/document.xml/body/p[1101], word/document.xml/body/p[1102], word/document.xml/body/p[1103], word/document.xml/body/p[1104], word/document.xml/body/p[1105], word/document.xml/body/p[1106], word/document.xml/body/p[1107], word/document.xml/body/p[1108], word/document.xml/body/p[1110]

来源 chunk-cf3d3bb155ff05c4e0809464：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
位置：word/document.xml/body/p[1112]

来源 chunk-8424f0e01f9e2107b966e55a：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装5GC业务软件 / 单节点离线部署UPF / 检查upf 业务网络地址配置 / 检查N3N6接口及IP配置
位置：word/document.xml/body/p[1111]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-11
问题：UPF 5.0 网管如何设置网元时间同步？
状态：completed

- 登录网管，在左边菜单栏点击配置，输入区域、局点、网元编号关键词查找网元，点击目标网元右侧的配置图标进入配置界面。 [chunk-54d6b634e00bbfeab5b6b8f7, chunk-54d6b634e00bbfeab5b6b8f7]
- 进入UPF配置-系统配置-ntp配置界面，添加ntp服务器1.0.144.134和1.0.144.130，待状态显示Synced后，点击立刻同步按钮进行一次性时间同步。 [chunk-54d6b634e00bbfeab5b6b8f7, chunk-54d6b634e00bbfeab5b6b8f7]
- 在config.yaml文件中配置ntp_servers参数，指定1.0.144.134和1.0.144.130作为时间同步服务器，并确保防火墙白名单中放通这两个IP地址。 [chunk-c0269e0f5f90744584380ab7, chunk-c0269e0f5f90744584380ab7, chunk-c0269e0f5f90744584380ab7, chunk-058b942e931659f44495305e]

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

来源 chunk-54d6b634e00bbfeab5b6b8f7：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：网管配置网元的时间
位置：word/document.xml/body/p[1732], word/document.xml/body/p[1733], word/document.xml/body/p[1734], word/document.xml/body/p[1736], word/document.xml/body/p[1738], word/document.xml/body/p[1739]

来源 chunk-c0269e0f5f90744584380ab7：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装K8S集群软件 / 单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
位置：word/document.xml/body/p[581], word/document.xml/body/p[582], word/document.xml/body/p[583], word/document.xml/body/p[584], word/document.xml/body/p[585], word/document.xml/body/p[587], word/document.xml/body/p[588], word/document.xml/body/p[589], word/document.xml/body/p[590], word/document.xml/body/p[591], word/document.xml/body/p[592], word/document.xml/body/p[593], word/document.xml/body/p[594], word/document.xml/body/p[595], word/document.xml/body/p[596], word/document.xml/body/p[597], word/document.xml/body/p[599], word/document.xml/body/p[600], word/document.xml/body/p[601], word/document.xml/body/p[602], word/document.xml/body/p[604], word/document.xml/body/p[605], word/document.xml/body/p[606], word/document.xml/body/p[608], word/document.xml/body/p[609], word/document.xml/body/p[610], word/document.xml/body/p[611], word/document.xml/body/p[613], word/document.xml/body/p[614], word/document.xml/body/p[615], word/document.xml/body/p[616], word/document.xml/body/p[618], word/document.xml/body/p[619], word/document.xml/body/p[620], word/document.xml/body/p[621], word/document.xml/body/p[623], word/document.xml/body/p[624], word/document.xml/body/p[625], word/document.xml/body/p[626], word/document.xml/body/p[627], word/document.xml/body/p[628]

来源 chunk-058b942e931659f44495305e：UPF 5.0安装部署指导书(新网管版)(1).docx
章节：安装K8S集群软件 / 单节点部署K8S / 调整集群配置 / 调整后的集群配置文件
位置：word/document.xml/body/p[630], word/document.xml/body/p[631], word/document.xml/body/p[632], word/document.xml/body/p[633], word/document.xml/body/p[634], word/document.xml/body/p[635], word/document.xml/body/p[636], word/document.xml/body/p[637], word/document.xml/body/p[638], word/document.xml/body/p[639], word/document.xml/body/p[640], word/document.xml/body/p[641], word/document.xml/body/p[642], word/document.xml/body/p[644], word/document.xml/body/p[645], word/document.xml/body/p[646], word/document.xml/body/p[647], word/document.xml/body/p[649], word/document.xml/body/p[650], word/document.xml/body/p[651], word/document.xml/body/p[652], word/document.xml/body/p[654], word/document.xml/body/p[655], word/document.xml/body/p[656], word/document.xml/body/p[657], word/document.xml/body/p[658], word/document.xml/body/p[659], word/document.xml/body/p[660]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": true, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-12
问题：网管如何下载实时告警？
状态：completed

- 在5GC网管V1.3版本中，下载实时告警的路径为：Alarm-->Active Alarm。 [chunk-8155920f16768dca1cb872d8, chunk-0d555a667d8458f08194b6fa, chunk-e4853f57767ab702e0cb20e7, chunk-de099c30517a742759b73e73]
- 在实时告警页面，点击“Download”按钮，可选择打开或保存下载的Excel文件。 [chunk-8155920f16768dca1cb872d8]
- 下载实时告警前，需确保已通过“Query Alarm”和“Refresh”操作查询并刷新告警列表。 [chunk-0d555a667d8458f08194b6fa, chunk-e4853f57767ab702e0cb20e7]

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

来源 chunk-8155920f16768dca1cb872d8：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.3 告警下载
位置：word/document.xml/body/p[851], word/document.xml/body/p[852], word/document.xml/body/p[853], word/document.xml/body/p[855]

来源 chunk-0d555a667d8458f08194b6fa：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.1 告警查询
位置：word/document.xml/body/p[839], word/document.xml/body/p[840], word/document.xml/body/p[841], word/document.xml/body/p[843], word/document.xml/body/p[844]

来源 chunk-e4853f57767ab702e0cb20e7：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.7 刷新告警
位置：word/document.xml/body/p[871], word/document.xml/body/p[872], word/document.xml/body/p[873], word/document.xml/body/p[875]

来源 chunk-de099c30517a742759b73e73：5GC网管使用手册_V1.3_20220916(1).docx
章节：7 故障管理（Fault Management） / 7.1 实时告警 / 7.1.8 告警同步
位置：word/document.xml/body/p[876], word/document.xml/body/p[877], word/document.xml/body/p[878], word/document.xml/body/p[880]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": true, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-13
问题：现场 UPF 当前 CPU 温度是多少摄氏度？请给出精确数值。
状态：missing_source

- 待补充：手册中未提供查询UPF当前CPU温度的命令或方法。
- 待补充：手册中未提及任何与CPU温度监控相关的功能、参数或配置项。
- 待补充：手册中所有内容均围绕配置、部署、资源分配和网络设置展开，无实时硬件状态（如温度）监控信息。
- 待补充：虽然提到了`show cp-node`命令，但该命令仅用于查询CP节点信息，不包含CPU温度数据。
- 待补充：无任何引用支持从系统中获取实时CPU温度的精确数值。

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-14
问题：UPF 的 Wi-Fi 7 无线信道切换命令和全部参数是什么？
状态：failed

- 待补充：生成或引用校验失败，未发布未经验证的回答。

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

自动检查：{"status_expected": false, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": false, "business_semantics": "pending_human_review"}
## answer-15
问题：如何执行 show cp-node？
状态：missing_source

- 待补充：没有匹配产品/版本的手册证据。

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
## answer-16
问题：UPF 999.9 如何执行 show cp-node？
状态：partial

- 执行 show cp-node 命令需通过 telnet 0 37100 登录后在 upfd 调试台中输入 [chunk-a95707dc20bc358dc01eba2e, chunk-8c359c6b97c3c3bb5bfa01d9, chunk-da79f1572c8b981ab1f34446, chunk-05b46622548cea41921ec8c4]
- 命令格式为 UPFD> show cp-node [chunk-a95707dc20bc358dc01eba2e, chunk-bcfb4b79a1fc297be1d1d5e6, chunk-8c359c6b97c3c3bb5bfa01d9, chunk-bbf13cab6aca8034ef1d180e]
- 该命令用于查询 CP Node 信息，显示内容包括 CP-IP-ADDR、NODE-ID、ASSO-STATUS 等字段 [chunk-9e79662334e774bfb1b81c4b, chunk-9e79662334e774bfb1b81c4b, chunk-9e79662334e774bfb1b81c4b]
- 待补充：版本 999.9 未在证据中确认，仅基于 unknown 版本信息提供部分支持
- 待补充：引用资料版本未知，无法确认对请求版本的适用性。

提示：P2 命令与截图人工复核尚未完成；引用存在不等于现场适用。
提示：引用手册版本未知，需核对目标设备版本与操作前提。

来源 chunk-a95707dc20bc358dc01eba2e：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能配置
位置：word/document.xml/body/p[257]

来源 chunk-8c359c6b97c3c3bb5bfa01d9：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能配置
位置：word/document.xml/body/p[260]

来源 chunk-da79f1572c8b981ab1f34446：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能配置
位置：word/document.xml/body/p[251], word/document.xml/body/p[252], word/document.xml/body/p[253], word/document.xml/body/p[254], word/document.xml/body/p[255]

来源 chunk-05b46622548cea41921ec8c4：中国联通5G专网UPF产品使用手册(1).docx
章节：产品配置 / CLI配置命令 / UPF系统能力 / 功能配置
位置：word/document.xml/body/p[168], word/document.xml/body/p[169], word/document.xml/body/p[170], word/document.xml/body/p[171], word/document.xml/body/p[172], word/document.xml/body/p[173], word/document.xml/body/p[174], word/document.xml/body/p[176]

来源 chunk-bcfb4b79a1fc297be1d1d5e6：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / UPF 终端负载情况异常 / 信息收集
位置：word/document.xml/body/p[328]/txbxContent[1]/p[2], word/document.xml/body/p[329], word/document.xml/body/p[330]

来源 chunk-bbf13cab6aca8034ef1d180e：中国联通5G专网UPF紧急故障指引0429(1).docx
章节：业务故障案例 / 偶联建立失败：SMF open upf开关 / 信息收集
位置：word/document.xml/body/p[115], word/document.xml/body/p[116], word/document.xml/body/p[117]

来源 chunk-9e79662334e774bfb1b81c4b：中国联通5G专网UPF产品使用手册(1).docx
章节：产品监控 / 业务信息监控 / 查询cp node信息 / 功能配置
位置：word/document.xml/body/p[261], word/document.xml/body/p[262], word/document.xml/body/p[263]

自动检查：{"status_expected": true, "quote_integrity": true, "refusal_contract": true, "critical_literal_coverage": null, "machine_contract_pass": true, "business_semantics": "pending_human_review"}
