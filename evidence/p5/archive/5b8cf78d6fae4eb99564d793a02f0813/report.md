问题：请分析PFCP不可达与正常心跳是否混淆，查看代表原文，并说明能否关联根因。
任务：5b8cf78d6fae4eb99564d793a02f0813
状态：partial

观测事实与手册原文：
- 所选范围包含 32539 条日志事件，覆盖 32539 行；计数单位为消息，不是独立故障。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- unclassified / unknown：22718 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_session_deleted / observed：5715 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- far_handover / observed：3238 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- gtpu_echo_retry / observed：382 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- gtpu_unreachable_detected / raised：120 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- gtpu_unreachable_report / raised：120 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- interface_index_failure / observed：111 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- n4_name_failure / observed：30 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_heartbeat_request / observed：23 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- upfd_start / observed：21 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- timer_init_failure / observed：16 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_node_unreachable / raised：14 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_node_unreachable / cleared：12 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- license_not_installed / cleared：11 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_heartbeat_response / observed：7 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- license_not_installed / raised：1 条消息。 [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e]

候选解释（未验证因果）：

缺失信息：
- 规划失败，保留确定性证据：工具参数错误：[None, None, 'scope_denied']
- 没有真实拓扑，无法确认实际链路/交换机端口与传播路径。
- 源时区未知，未计算绝对时间关联或故障持续时间。
- 缺少原始真实设备身份，脱敏值不能用于事件配对。

建议检查：
- 按报告来源位置复核原文，并补充列出的现场资料；建议不自动执行。

提示：
- Counts represent log messages, not independent faults; FATAL remains raw severity.
- Timezone unknown: UTC timeline unavailable for unresolved events; no cross-source time correlation.
- Result capped; counts must use analyze, not sample length.

来源：
- [5b8cf78d6fae4eb99564d793a02f0813:aggregate:a6f18ac81a18aa2125fa:317917850655208e] log-a698d029342259b7；full selected scope; {"log_id":"a6f18ac81a18aa2125fa","window":null,"device_id":null,"event_type":null,"bucket_minutes":60}；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  {"total_events": 32539, "physical_lines": 32539, "source_bytes": 6347974, "generation": "a6f18ac81a18aa2125fa", "counts": [{"event_type": "unclassified", "event_state": "unknown", "messages": 22718}, {"event_type": "pfcp_session_deleted", "event_state": "observed", "messages": 5715}, {"event_type": "far_handover", "event_state": "observed", "messages": 3238}, {"event_type": "gtpu_echo_retry", "event_state": "observed", "messages": 382}, {"event_type": "gtpu_unreachable_detected", "event_state": "raised", "messages": 120}, {"event_type": "gtpu_unreachable_report", "event_state": "raised", "messages": 120}, {"event_type": "interface_index_failure", "event_state": "observed", "messages": 111}, {"event_type": "n4_name_failure", "event_state": "observed", "messages": 30}, {"event_type": "pfcp_heartbeat_request", "event_state": "observed", "messages": 23}, {"event_type": "upfd_start", "event_state": "observed", "messages": 21}, {"event_type": "timer_init_failure", "event_state": "observed", "messages": 16}, {"event_type": "pfcp_node_unreachable", "event_state": "raised", "messages": 14}, {"event_type": "pfcp_node_unreachable", "event_state": "cleared", "messages": 12}, {"event_type": "license_not_installed", "event_state": "cleared", "messages": 11}, {"event_type": "pfcp_heartbeat_response", "event_state": "observed", "messages": 7}, {"event_type": "license_not_installed", "event_state": "raised", "messages": 1}], "representatives": [{"event_type": "far_handover", "first_event_id": "log-a698d029342259b7-12005", "last_event_id": "log-a698d029342259b7-6337704"}, {"event_type": "gtp
- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-5967589] log-a698d029342259b7；lines=30659-30659;offset=5967589；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-21 20:57:10.493959 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-5968078] log-a698d029342259b7；lines=30662-30662;offset=5968078；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-21 20:57:10.494068 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6327317] log-a698d029342259b7；lines=32430-32430;offset=6327317；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 01:00:46.637266 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6327806] log-a698d029342259b7；lines=32433-32433;offset=6327806；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 01:00:46.637374 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6328295] log-a698d029342259b7；lines=32436-32436;offset=6328295；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 01:00:46.637458 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6328784] log-a698d029342259b7；lines=32439-32439;offset=6328784；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 01:00:46.637527 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6329273] log-a698d029342259b7；lines=32442-32442;offset=6329273；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 01:00:46.637598 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6329762] log-a698d029342259b7；lines=32445-32445;offset=6329762；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 01:00:46.637671 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6340340] log-a698d029342259b7；lines=32496-32496;offset=6340340；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 09:50:44.003279 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6340829] log-a698d029342259b7；lines=32499-32499;offset=6340829；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 09:50:44.209777 ERROR FID.0 upfd_alarm.c:314(upfdAlarmPfcpNodeUnreachable): #Alarm# report PFCP node unreachable!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-3182914] log-a698d029342259b7；lines=15128-15128;offset=3182914；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-15 09:10:45.375909 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-3516922] log-a698d029342259b7；lines=17632-17632;offset=3516922；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-15 09:11:09.253460 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-3601293] log-a698d029342259b7；lines=18264-18264;offset=3601293；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-15 09:11:15.376158 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-3882229] log-a698d029342259b7；lines=20349-20349;offset=3882229；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-15 09:11:39.253818 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-3962881] log-a698d029342259b7；lines=20941-20941;offset=3962881；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-15 09:11:45.376668 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-4210715] log-a698d029342259b7；lines=22786-22786;offset=4210715；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-15 09:12:09.254708 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-4296988] log-a698d029342259b7；lines=23439-23439;offset=4296988；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-15 09:12:15.376707 DEBUG FID.0 upfd_pfcp.c:2031(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp.

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6331886] log-a698d029342259b7；lines=32455-32455;offset=6331886；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 02:14:23.451114 ERROR FID.0 upfd_pfcp.c:2067(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp:2408:8142:60ff:fc0b:1721:406:: but status down!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6332054] log-a698d029342259b7；lines=32456-32456;offset=6332054；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 02:14:23.802190 ERROR FID.0 upfd_pfcp.c:2067(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp:2408:8142:60ff:fc02:1706:406:: but status down!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-6332472] log-a698d029342259b7；lines=32459-32459;offset=6332472；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-07-12 02:14:24.882058 ERROR FID.0 upfd_pfcp.c:2067(upfdPfcpMsgEntryHeartBeatReq): Recv #MsgHeartbeat# Req from cp:2408:8142:60ff:fc0b:171f:406:: but status down!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-17561] log-a698d029342259b7；lines=128-128;offset=17561；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:09:58.045994 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-19494] log-a698d029342259b7；lines=139-139;offset=19494；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:10:07.005699 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-19720] log-a698d029342259b7；lines=141-141;offset=19720；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:10:11.009574 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-20744] log-a698d029342259b7；lines=149-149;offset=20744；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:10:29.026475 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-20970] log-a698d029342259b7；lines=151-151;offset=20970；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:10:33.030562 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-22260] log-a698d029342259b7；lines=161-161;offset=22260；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:10:58.004618 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-23673] log-a698d029342259b7；lines=170-170;offset=23673；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:11:06.012404 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-24032] log-a698d029342259b7；lines=173-173;offset=24032；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:11:07.013576 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-24392] log-a698d029342259b7；lines=176-176;offset=24392；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:11:11.017658 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

- [5b8cf78d6fae4eb99564d793a02f0813:log-a698d029342259b7-25119] log-a698d029342259b7；lines=181-181;offset=25119；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  2025-05-14 20:11:18.024429 ERROR FID.0 upfd_rq.c:748(upfdV4ResendAlarm): alarm gtpu unreachable ipv4!

