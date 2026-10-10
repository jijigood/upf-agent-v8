"""Finite, evidence-joined RCA control; no model, injector input, or repair execution.

Both modes receive the same normal snapshot. Graph mode additionally joins sourced
observations through the actual MemoryGraphStore. This is an experimental diagnostic
adapter, not unrestricted RCA or independently approved domain knowledge.
"""

import argparse
import base64
import hashlib
import json
import re
import socket
import struct
from datetime import datetime
from pathlib import Path
from time import perf_counter

import yaml
from v8_e7_diagnosis import build_facts, guard

from upf_agent.v8.graph import GraphEdge, GraphNode, GraphQueryPlan, MemoryGraphStore
from upf_agent.v8.models import SourcePointer

VERSION = "evidence-joined-rca-1"
GROUPED_IES = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 16, 17, 18}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def decode_ies(raw, depth=0):
    if depth > 8:
        raise ValueError("PFCP grouped IE depth exceeds bound")
    result, offset = [], 0
    while offset < len(raw):
        if len(raw) - offset < 4:
            raise ValueError("truncated PFCP IE header")
        kind, size = struct.unpack_from("!HH", raw, offset)
        end = offset + 4 + size
        if end > len(raw):
            raise ValueError("truncated PFCP IE value")
        value = raw[offset + 4 : end]
        item = {"type": kind, "length": size, "sha256": hashlib.sha256(value).hexdigest()}
        if kind in GROUPED_IES:
            item["children"] = decode_ies(value, depth + 1)
        elif kind == 19 and size:
            item["cause"] = value[0]
        elif kind == 57:  # TS 29.244 8.2.37: flags V4 bit 2, V6 bit 1.
            required = (
                9 + (4 if value and value[0] & 2 else 0) + (16 if value and value[0] & 1 else 0)
            )
            if size < required:
                raise ValueError("truncated F-SEID")
            item["seid"] = struct.unpack_from("!Q", value, 1)[0]
            p = 9
            if value[0] & 2:
                item["ipv4"] = socket.inet_ntoa(value[p : p + 4])
                p += 4
            if value[0] & 1:
                item["ipv6"] = socket.inet_ntop(socket.AF_INET6, value[p : p + 16])
        elif kind == 21:
            if not size:
                raise ValueError("truncated F-TEID flags")
            flags = value[0]
            item["choose"] = bool(flags & 4)
            if flags & 4:
                if flags & 8:
                    if size < 2:
                        raise ValueError("truncated F-TEID choose ID")
                    item["choose_id"] = value[1]
            else:
                required = 5 + (4 if flags & 1 else 0) + (16 if flags & 2 else 0)
                if size < required:
                    raise ValueError("truncated F-TEID")
                item["teid"] = struct.unpack_from("!I", value, 1)[0]
                p = 5
                if flags & 1:
                    item["ipv4"] = socket.inet_ntoa(value[p : p + 4])
                    p += 4
                if flags & 2:
                    item["ipv6"] = socket.inet_ntop(socket.AF_INET6, value[p : p + 16])
        elif kind == 84:
            if size < 2:
                raise ValueError("truncated Outer Header Creation")
            # Description uses octet 5 flags, not a network-order integer bitmask.
            flags, p = value[0], 2
            item["description_octets"] = value[:2].hex()
            if flags & 3:
                if size < p + 4:
                    raise ValueError("truncated Outer Header Creation TEID")
                item["teid"] = struct.unpack_from("!I", value, p)[0]
                p += 4
            if flags & (1 | 4 | 16):
                if size < p + 4:
                    raise ValueError("truncated Outer Header Creation IPv4")
                item["ipv4"] = socket.inet_ntoa(value[p : p + 4])
                p += 4
            if flags & (2 | 8 | 32):
                if size < p + 16:
                    raise ValueError("truncated Outer Header Creation IPv6")
                item["ipv6"] = socket.inet_ntop(socket.AF_INET6, value[p : p + 16])
        result.append(item)
        offset = end
    return result


def decode_pfcp(payload):
    if len(payload) < 8:
        raise ValueError("truncated PFCP header")
    if payload[0] >> 5 != 1:
        raise ValueError("unsupported PFCP version")
    size = struct.unpack_from("!H", payload, 2)[0] + 4
    session = bool(payload[0] & 1)
    header = 16 if session else 8
    if size < header or len(payload) < size:
        raise ValueError("truncated PFCP declared message")
    p = 12 if session else 4
    return {
        "message_type": payload[1],
        "sequence": int.from_bytes(payload[p : p + 3], "big"),
        "header_seid": struct.unpack_from("!Q", payload, 4)[0] if session else None,
        "ies": decode_ies(payload[header:size]),
        "message_sha256": hashlib.sha256(payload[:size]).hexdigest(),
    }


def enriched_facts(snapshot):
    facts = build_facts(snapshot)
    for fact in facts:
        if "/packet_captures/" not in fact["locator"]:
            continue
        name = fact["locator"].split("/")[2]
        data = base64.b64decode(snapshot["packet_captures"][name]["capture_base64"], validate=True)
        endian = "<" if data[:4] in (b"\xd4\xc3\xb2\xa1", b"\x4d\x3c\xb2\xa1") else ">"
        link = struct.unpack_from(endian + "I", data, 20)[0]
        link_offset = {1: 14, 113: 16, 276: 20, 101: 0}[link]
        for packet in fact["value"]["packets"]:
            if packet.get("dst_port") != 8805:
                continue
            start = packet["file_byte_start"]
            ip = data[start + link_offset : start + packet["captured_bytes"]]
            ihl = (ip[0] & 15) * 4
            try:
                if ihl < 20 or len(ip) < ihl + 8:
                    raise ValueError("truncated IPv4 UDP header")
                udp_length = struct.unpack_from("!H", ip, ihl + 4)[0]
                if udp_length < 8 or len(ip) < ihl + udp_length:
                    raise ValueError("truncated UDP payload; full PFCP unavailable")
                packet["pfcp"] = decode_pfcp(ip[ihl + 8 : ihl + udp_length])
            except ValueError as exc:
                packet["pfcp_decode_error"] = str(exc)
    return facts


def walk_ies(ies):
    for ie in ies:
        yield ie
        yield from walk_ies(ie.get("children", []))


def session_pairs(facts, smf, upf):
    """Pair source-qualified transactions before correlating local SEIDs.

    Seeing a response before INPUT filtering never proves CP application acceptance.
    Only observed establishment request/response pairs are returned; arbitrary
    modifications cannot fabricate the missing establishment mapping.
    """
    packets = [
        (f["evidence_id"], p)
        for f in facts
        if isinstance(f["value"], dict) and "packets" in f["value"]
        for p in f["value"]["packets"]
        if "pfcp" in p
    ]
    result, seen = [], set()
    for fid, req in packets:
        parsed = req["pfcp"]
        if parsed["message_type"] != 50 or (req["src"], req["dst"]) != (smf, upf):
            continue
        cp = [ie for ie in parsed["ies"] if ie["type"] == 57 and ie.get("ipv4") == smf]
        if len(cp) != 1:
            continue
        for rid, resp in packets:
            reply = resp["pfcp"]
            if (
                reply["message_type"] != 51
                or reply["sequence"] != parsed["sequence"]
                or (resp["src"], resp["dst"]) != (upf, smf)
                or resp["timestamp_utc_epoch"] < req["timestamp_utc_epoch"]
                or resp["timestamp_utc_epoch"] - req["timestamp_utc_epoch"] > 10
                or reply["header_seid"] != cp[0]["seid"]
            ):
                continue
            causes = [ie["cause"] for ie in reply["ies"] if ie["type"] == 19 and "cause" in ie]
            ups = [ie for ie in reply["ies"] if ie["type"] == 57 and ie.get("ipv4") == upf]
            if causes != [1] or len(ups) != 1:
                continue
            key = (smf, cp[0]["seid"], upf, ups[0]["seid"], parsed["sequence"])
            if key in seen:
                continue
            seen.add(key)
            result.append(
                {
                    "cp": cp[0],
                    "up": ups[0],
                    "sequence": parsed["sequence"],
                    "request_evidence_id": fid,
                    "request_packet_index": req["packet_index"],
                    "response_evidence_id": rid,
                    "response_packet_index": resp["packet_index"],
                    "created_fteids": [ie for ie in walk_ies(reply["ies"]) if ie["type"] == 21],
                    "forwarding_peers": [ie for ie in walk_ies(parsed["ies"]) if ie["type"] == 84],
                    "application_acceptance_proven": False,
                }
            )
    return result


def diagnose(snapshot, mode, source_sha):
    if mode not in {"flat", "joined", "graph"}:
        raise ValueError("unknown diagnostic mode")
    started = perf_counter()
    facts = enriched_facts(snapshot)
    by_locator = {f["locator"]: f for f in facts}
    rules = []

    def add(cause, score, refs, rationale, joint=False):
        if refs and all(r in {f["evidence_id"] for f in facts} for r in refs):
            rules.append(
                {
                    "id": f"r{len(rules):03}",
                    "cause": cause,
                    "score": score,
                    "evidence_ids": sorted(set(refs)),
                    "rationale": rationale,
                    "joint": joint,
                }
            )

    def lookup(path):
        return by_locator.get(path)

    def config(role, obj):
        f = lookup(f"/{role}/logs_and_config/{obj}.yaml")
        return (f, yaml.safe_load(f["value"])) if f else (None, {})

    states = []
    for role, obj, cause in [
        ("core", "upf", "upf_process_suspended"),
        ("core", "smf", "smf_process_suspended"),
        ("core", "gnb", "ran_process_suspended"),
        ("ue", "ue", "ue_process_suspended"),
    ]:
        f = lookup(f"/{role}/process_states/{obj}")
        if f:
            states.append(f)
            if f["value"]["state"].startswith("T"):
                add(cause, 100, [f["evidence_id"]], "进程State T：停止调度；不能由S推断暂停")
    normal_states = len(states) == 4 and all(
        f["value"]["state"].startswith(("S", "R", "I")) for f in states
    )
    ue_log = lookup("/ue/logs_and_config/ue.log")
    if ue_log and any(
        "DNN_NOT_SUPPORTED_OR_NOT_SUBSCRIBED" in e["message"] for e in ue_log["value"]["events"]
    ):
        add("ue_dnn_not_subscribed", 95, [ue_log["evidence_id"]], "UE日志明确记录DNN不支持或未订阅")
    gnb_fact, gnb_cfg = config("core", "gnb")
    smf_fact, smf_cfg = config("core", "smf")
    upf_fact, upf_cfg = config("core", "upf")

    def server_address(cfg, role, interface):
        section = cfg.get(role, {}).get(interface, {}).get("server", [])
        return section[0].get("address") if section else None

    smf_ip = server_address(smf_cfg, "smf", "pfcp")
    upf_ip = server_address(upf_cfg, "upf", "pfcp")
    upf_gtp = server_address(upf_cfg, "upf", "gtpu")
    gnb_gtp = gnb_cfg.get("gtpIp")
    caps = {
        name: lookup(f"/packet_captures/{name}/capture_base64")
        for name in ("uplink", "downlink", "session")
    }
    probes = {name: lookup(f"/diagnostic_probes/{name}") for name in ("uplink", "downlink")}
    probe_refs = [f["evidence_id"] for f in probes.values() if f]
    probe_failure = len(probe_refs) == 2 and all(
        f["value"]["returncode"] != 0 for f in probes.values()
    )
    # Do not infer an anomaly from process sleeping or missing log events.
    probe_success = len(probe_refs) == 2 and all(
        f["value"]["returncode"] == 0
        and re.search(r"5 packets transmitted, 5 (?:packets )?received", f["value"]["stdout"])
        for f in probes.values()
    )
    if probe_success and normal_states:
        add(
            "no_fault_observed",
            90,
            probe_refs + [f["evidence_id"] for f in states],
            "双向五包探针成功且四进程正常；仅覆盖本次测试业务",
            joint=True,
        )
    # UE requested DNN, AMF rejection, and UE status are distinct normal evidence.
    amf_fact = lookup("/core/logs_and_config/amf.log")
    if ue_log and amf_fact:
        if any(
            "Not Supported OR Not Subscribed" in e["message"] for e in amf_fact["value"]["events"]
        ):
            if any(
                "DNN_NOT_SUPPORTED_OR_NOT_SUBSCRIBED" in e["message"]
                for e in ue_log["value"]["events"]
            ):
                add(
                    "ue_dnn_not_subscribed",
                    99,
                    [ue_log["evidence_id"], amf_fact["evidence_id"]],
                    "UE拒绝码与AMF订阅/DNN拒绝记录相符",
                    joint=True,
                )
    config_refs = [f["evidence_id"] for f in (gnb_fact, upf_fact, smf_fact) if f]
    if normal_states and probe_failure and gnb_gtp and upf_gtp and caps["uplink"]:
        packets = caps["uplink"]["value"]["packets"]
        wrong_peer = [
            p
            for p in packets
            if p.get("gtp_type_numeric") == 255
            and p.get("src") == upf_gtp
            and p.get("dst") != gnb_gtp
        ]
        advertised = gnb_cfg.get("gtpAdvertiseIp", gnb_gtp)
        if advertised != gnb_gtp and any(p.get("dst") == advertised for p in wrong_peer):
            add(
                "gnb_gtp_endpoint_mismatch",
                98,
                config_refs + probe_refs + [caps["uplink"]["evidence_id"]],
                "RAN通告地址与绑定地址不同，UPF回复流向通告地址；待核验部署意图",
                joint=True,
            )
        if advertised == gnb_gtp and all(caps[n] for n in ("uplink", "downlink")):

            def counts(name, src, dst, icmp):
                return sum(
                    p.get("src") == src
                    and p.get("dst") == dst
                    and p.get("icmp_type_numeric") == icmp
                    for p in caps[name]["value"]["packets"]
                )

            ul_req, ul_resp = (
                counts("uplink", gnb_gtp, upf_gtp, 8),
                counts("uplink", upf_gtp, gnb_gtp, 0),
            )
            dl_req, dl_resp = (
                counts("downlink", upf_gtp, gnb_gtp, 8),
                counts("downlink", gnb_gtp, upf_gtp, 0),
            )
            if ul_req and dl_req:
                refs = (
                    config_refs
                    + probe_refs
                    + [caps[n]["evidence_id"] for n in ("uplink", "downlink")]
                )
                if not ul_resp and dl_resp:
                    add(
                        "n3_uplink_transport_loss",
                        70,
                        refs,
                        "下行请求触发RAN上行回复，上行请求未触发UPF回复：上行路径候选",
                        joint=True,
                    )
                elif ul_resp and not dl_resp:
                    add(
                        "n3_downlink_transport_loss",
                        70,
                        refs,
                        "上行请求触发UPF下行回复，下行请求未触发RAN回复：下行路径候选",
                        joint=True,
                    )
                elif not ul_resp and not dl_resp:
                    add(
                        "n3_bidirectional_transport_loss",
                        65,
                        refs,
                        "双向请求可见但均无回复：双向路径候选，抓包不证明应用收到",
                        joint=True,
                    )
    packets = [p for f in caps.values() if f for p in f["value"]["packets"] if "pfcp" in p]
    if normal_states and probe_failure and smf_ip and upf_ip and packets:

        def heartbeat_pair(src, dst):
            requests = [
                p
                for p in packets
                if (p["src"], p["dst"]) == (src, dst) and p["pfcp"]["message_type"] == 1
            ]
            matched = any(
                (resp["src"], resp["dst"]) == (dst, src)
                and resp["pfcp"]["message_type"] == 2
                and resp["pfcp"]["sequence"] == req["pfcp"]["sequence"]
                and 0 <= resp["timestamp_utc_epoch"] - req["timestamp_utc_epoch"] <= 10
                for req in requests
                for resp in packets
            )
            return bool(requests), matched

        cp_req, cp_pair = heartbeat_pair(smf_ip, upf_ip)
        up_req, up_pair = heartbeat_pair(upf_ip, smf_ip)
        if cp_req and up_req:
            refs = config_refs + probe_refs + [f["evidence_id"] for f in caps.values() if f]
            if not cp_pair and up_pair:
                add(
                    "pfcp_smf_to_upf_loss",
                    70,
                    refs,
                    "SMF心跳无匹配回复、UPF心跳有匹配回复：SMF到UPF路径候选",
                    joint=True,
                )
            elif cp_pair and not up_pair:
                add(
                    "pfcp_upf_to_smf_loss",
                    70,
                    refs,
                    "UPF心跳无匹配回复、SMF心跳有匹配回复：UPF到SMF路径候选",
                    joint=True,
                )
            elif not cp_pair and not up_pair:
                add(
                    "pfcp_bidirectional_loss",
                    65,
                    refs,
                    "两端心跳均无匹配回复：双向路径候选，需补接收点证据",
                    joint=True,
                )

    graph = MemoryGraphStore()
    query_receipt = None
    if mode == "graph":
        pointer = SourcePointer(
            source_id="visible-snapshot",
            sha256=source_sha,
            locator="/",
            relative_path="snapshot.json",
        )
        nodes = [
            GraphNode(
                node_id=f["evidence_id"],
                kind="DiagnosticFact",
                layer="diagnostic",
                object_ids=[f["object_id"]],
                source=pointer.model_copy(update={"locator": f["locator"]}),
                attributes={"value": f["value"]},
            )
            for f in facts
        ]
        edges = []
        for rule in rules:
            candidate_id = "cause:" + rule["cause"]
            if not any(n.node_id == candidate_id for n in nodes):
                nodes.append(
                    GraphNode(
                        node_id=candidate_id,
                        kind="RootCauseCandidate",
                        layer="diagnostic",
                        source=pointer,
                        attributes={"candidate_only": True},
                    )
                )
            nodes.append(
                GraphNode(
                    node_id=rule["id"],
                    kind="EvidenceJoin",
                    layer="diagnostic",
                    source=pointer,
                    attributes=rule,
                )
            )
            for a, b in [
                (candidate_id, rule["id"]),
                *[(rule["id"], ref) for ref in rule["evidence_ids"]],
            ]:
                edges.append(
                    GraphEdge(
                        edge_id=f"edge:{len(edges):03}",
                        source_id=a,
                        target_id=b,
                        relation="SUPPORTED_BY",
                        source=pointer,
                        attributes={"derived_relation": True, "independent_corroboration": False},
                    )
                )
        graph.build(nodes, edges)
        query = GraphQueryPlan(
            seed_ids=["cause:" + r["cause"] for r in rules],
            objects=sorted({f["object_id"] for f in facts}),
            relations=["SUPPORTED_BY"],
            as_of=datetime.fromisoformat(snapshot["window_end"]),
            require_version=False,
            max_hops=2,
            max_nodes=100,
            max_edges=200,
            contract_id="readonly-e7-diagnostic",
        )
        result = graph.query(query)
        available_nodes = {n.node_id for n in result.nodes}
        available_edges = {(e.source_id, e.target_id) for e in result.edges}
        rules = [
            r
            for r in rules
            if r["id"] in available_nodes
            and ("cause:" + r["cause"], r["id"]) in available_edges
            and all((r["id"], ref) in available_edges for ref in r["evidence_ids"])
        ]
        query_receipt = result.model_dump(mode="json")
    elif mode == "flat":
        rules = [r for r in rules if not r["joint"]]
        # Healthy flat control also checks both independent probes; no graph traverse.
        if probe_success and normal_states:
            rules.append(
                {
                    "id": "healthy-direct",
                    "cause": "no_fault_observed",
                    "score": 90,
                    "evidence_ids": probe_refs,
                    "rationale": "双向探针成功，无本次业务异常",
                    "joint": False,
                }
            )
    ranked = sorted(rules, key=lambda r: (-r["score"], r["cause"], r["id"]))
    hypotheses = []
    for rule in ranked:
        if rule["cause"] not in [h["cause"] for h in hypotheses]:
            hypotheses.append(rule)
    if not hypotheses:
        hypotheses = [
            {
                "cause": "unknown",
                "score": 0,
                "evidence_ids": probe_refs,
                "rationale": "当前可见事实不足以区分根因；补接收点与会话映射证据",
            }
        ]
    return {
        "version": VERSION,
        "mode": mode,
        "graph_enabled": mode == "graph",
        "hypotheses": hypotheses[:3],
        "facts": facts,
        "graph": graph.snapshot() if mode == "graph" else None,
        "graph_query": query_receipt,
        "session_pairs": session_pairs(facts, smf_ip, upf_ip),
        "physical_capture_sha256": source_sha,
        "diagnosis_seconds": perf_counter() - started,
        "model_calls": 0,
        "agent_repairs": 0,
        "execute_authorized": False,
        "formal_quality": False,
        "domain_rules_approved": False,
        "scope": "finite diagnostic adapter; graph comparison includes evidence joins",
    }


def run(input_root, output, private):
    if output.exists():
        raise ValueError("new output required")
    output.mkdir(parents=True)
    guard(input_root.resolve(), output.resolve(), private.resolve(), 1)
    raw = (input_root / "snapshot.json").read_bytes()
    snapshot, sha = json.loads(raw), hashlib.sha256(raw).hexdigest()
    results = {mode: diagnose(snapshot, mode, sha) for mode in ("flat", "joined", "graph")}
    for mode, result in results.items():
        write(output / f"{mode}.json", result)
    summary = {
        "physical_capture_sha256": sha,
        "version": VERSION,
        "hypotheses": {m: [h["cause"] for h in r["hypotheses"]] for m, r in results.items()},
        "model_calls": 0,
        "formal_quality": False,
        "pass": not results["graph"]["graph_query"]["truncated"]
        if results["graph"]["graph_query"]
        else True,
    }
    write(output / "diagnosis.json", summary)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--private-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.input, args.output, args.private_root)))
