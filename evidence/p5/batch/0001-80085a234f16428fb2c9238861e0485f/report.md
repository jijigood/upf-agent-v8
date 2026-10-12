问题：统计日志消息数量
任务：80085a234f16428fb2c9238861e0485f
状态：partial

观测事实与手册原文：
- 所选范围包含 32539 条日志事件，覆盖 32539 行；计数单位为消息，不是独立故障。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- unclassified / unknown：22718 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_session_deleted / observed：5715 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- far_handover / observed：3238 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- gtpu_echo_retry / observed：382 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- gtpu_unreachable_detected / raised：120 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- gtpu_unreachable_report / raised：120 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- interface_index_failure / observed：111 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- n4_name_failure / observed：30 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_heartbeat_request / observed：23 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- upfd_start / observed：21 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- timer_init_failure / observed：16 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_node_unreachable / raised：14 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_node_unreachable / cleared：12 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- license_not_installed / cleared：11 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- pfcp_heartbeat_response / observed：7 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]
- license_not_installed / raised：1 条消息。 [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e]

候选解释（未验证因果）：

缺失信息：
- 没有真实拓扑，无法确认实际链路/交换机端口与传播路径。
- 源时区未知，未计算绝对时间关联或故障持续时间。
- 缺少原始真实设备身份，脱敏值不能用于事件配对。

建议检查：
- 按报告来源位置复核原文，并补充列出的现场资料；建议不自动执行。

提示：
- Counts represent log messages, not independent faults; FATAL remains raw severity.
- Timezone unknown: UTC timeline unavailable for unresolved events; no cross-source time correlation.

来源：
- [80085a234f16428fb2c9238861e0485f:aggregate:a6f18ac81a18aa2125fa:317917850655208e] log-a698d029342259b7；full selected scope; {"log_id":"a6f18ac81a18aa2125fa","window":null,"device_id":null,"event_type":null,"bucket_minutes":60}；SHA256=a698d029342259b717db6f0520f4e9b006e59ae6e8ae743d0cc482199b242fcc
  {"total_events": 32539, "physical_lines": 32539, "source_bytes": 6347974, "generation": "a6f18ac81a18aa2125fa", "counts": [{"event_type": "unclassified", "event_state": "unknown", "messages": 22718}, {"event_type": "pfcp_session_deleted", "event_state": "observed", "messages": 5715}, {"event_type": "far_handover", "event_state": "observed", "messages": 3238}, {"event_type": "gtpu_echo_retry", "event_state": "observed", "messages": 382}, {"event_type": "gtpu_unreachable_detected", "event_state": "raised", "messages": 120}, {"event_type": "gtpu_unreachable_report", "event_state": "raised", "messages": 120}, {"event_type": "interface_index_failure", "event_state": "observed", "messages": 111}, {"event_type": "n4_name_failure", "event_state": "observed", "messages": 30}, {"event_type": "pfcp_heartbeat_request", "event_state": "observed", "messages": 23}, {"event_type": "upfd_start", "event_state": "observed", "messages": 21}, {"event_type": "timer_init_failure", "event_state": "observed", "messages": 16}, {"event_type": "pfcp_node_unreachable", "event_state": "raised", "messages": 14}, {"event_type": "pfcp_node_unreachable", "event_state": "cleared", "messages": 12}, {"event_type": "license_not_installed", "event_state": "cleared", "messages": 11}, {"event_type": "pfcp_heartbeat_response", "event_state": "observed", "messages": 7}, {"event_type": "license_not_installed", "event_state": "raised", "messages": 1}], "representatives": [{"event_type": "far_handover", "first_event_id": "log-a698d029342259b7-12005", "last_event_id": "log-a698d029342259b7-6337704"}, {"event_type": "gtp
