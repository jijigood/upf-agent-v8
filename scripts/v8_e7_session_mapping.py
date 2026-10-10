"""Capture-only PFCP establishment/modification to N3 peer/TEID consistency audit.

No private labels are read. Unsupported, incomplete or mismatching fields stay
explicit; wire consistency does not certify application acceptance or repair.
"""

import argparse
import hashlib
import json
from pathlib import Path

import yaml
from v8_e7_evidence_rca import enriched_facts, session_pairs, walk_ies


def map_sessions(snapshot):
    facts = enriched_facts(snapshot)
    configs = {
        name: yaml.safe_load(snapshot["core"]["logs_and_config"].get(name + ".yaml", "{}"))
        for name in ("smf", "upf", "gnb")
    }

    def address(name, interface):
        servers = configs[name].get(name, {}).get(interface, {}).get("server", [])
        return servers[0].get("address") if servers else None

    smf, upf = address("smf", "pfcp"), address("upf", "pfcp")
    upf_gtp = address("upf", "gtpu")
    gnb_gtp = configs["gnb"].get("gtpIp")
    advertised = configs["gnb"].get("gtpAdvertiseIp", gnb_gtp)
    packets = [
        (f["evidence_id"], p)
        for f in facts
        if isinstance(f["value"], dict) and "packets" in f["value"]
        for p in f["value"]["packets"]
    ]
    addresses = [
        address["local"]
        for interface in json.loads(snapshot["ue"]["interfaces"]["stdout"])
        if interface.get("ifname") == "uesimtun0"
        for address in interface.get("addr_info", [])
        if address.get("family") == "inet"
    ]
    ue_ip = addresses[0] if len(addresses) == 1 else None
    mappings = []
    for session in session_pairs(facts, smf, upf):
        established_at = next(
            p["timestamp_utc_epoch"]
            for ref, p in packets
            if ref == session["response_evidence_id"]
            and p["packet_index"] == session["response_packet_index"]
        )
        modifications = []
        for ref, req in packets:
            parsed = req.get("pfcp", {})
            if (
                (req.get("src"), req.get("dst")) != (smf, upf)
                or parsed.get("message_type") != 52
                or parsed.get("header_seid") != session["up"]["seid"]
            ):
                continue
            if req["timestamp_utc_epoch"] < established_at:
                continue
            for reply_ref, resp in packets:
                reply = resp.get("pfcp", {})
                if (
                    (resp.get("src"), resp.get("dst")) != (upf, smf)
                    or reply.get("message_type") != 53
                    or reply.get("sequence") != parsed["sequence"]
                    or reply.get("header_seid") != session["cp"]["seid"]
                ):
                    continue
                if not 0 <= resp["timestamp_utc_epoch"] - req["timestamp_utc_epoch"] <= 10:
                    continue
                if [ie.get("cause") for ie in reply["ies"] if ie["type"] == 19] != [1]:
                    continue
                modifications.append(
                    {
                        "sequence": parsed["sequence"],
                        "up_header_seid": parsed["header_seid"],
                        "cp_header_seid": reply["header_seid"],
                        "request_fact": ref,
                        "request_packet_index": req["packet_index"],
                        "response_fact": reply_ref,
                        "response_packet_index": resp["packet_index"],
                        "response_timestamp_utc_epoch": resp["timestamp_utc_epoch"],
                        "forwarding_peers": [
                            ie for ie in walk_ies(parsed["ies"]) if ie["type"] == 84
                        ],
                    }
                )
        local_teids = {
            ie["teid"]
            for ie in session["created_fteids"]
            if ie.get("ipv4") == upf_gtp and "teid" in ie
        }
        forwarding_mods = [m for m in modifications if m["forwarding_peers"]]
        current_mod = max(
            forwarding_mods, key=lambda m: m["response_timestamp_utc_epoch"], default=None
        )
        peer_teids = {
            (ie.get("ipv4"), ie.get("teid"))
            for mod in ([current_mod] if current_mod else [])
            for ie in mod["forwarding_peers"]
        }
        uplink = [
            {"fact": ref, "packet_index": p["packet_index"], "dst": p["dst"], "teid": p["teid"]}
            for ref, p in packets
            if p.get("gtp_type_numeric") == 255
            and p.get("dst_port") == 2152
            and p.get("dst") == upf_gtp
            and p.get("src") == gnb_gtp
            and p.get("teid") in local_teids
            and ue_ip is not None
            and p.get("inner_src") == ue_ip
            and p["timestamp_utc_epoch"] >= established_at
        ]
        downlink = [
            {"fact": ref, "packet_index": p["packet_index"], "dst": p["dst"], "teid": p["teid"]}
            for ref, p in packets
            if p.get("gtp_type_numeric") == 255
            and p.get("dst_port") == 2152
            and p.get("src") == upf_gtp
            and (p.get("dst"), p.get("teid")) in peer_teids
            and ue_ip is not None
            and p.get("inner_dst") == ue_ip
            and current_mod is not None
            and p["timestamp_utc_epoch"] >= current_mod["response_timestamp_utc_epoch"]
        ]
        mappings.append(
            {
                "establishment": session,
                "modifications": modifications,
                "n3_uplink_matching_packets": uplink,
                "n3_downlink_matching_packets": downlink,
                "ran_bound_address": gnb_gtp,
                "ran_advertised_address": advertised,
                "observed_unique_ue_ip": ue_ip,
                "ran_bound_advertised_consistent": gnb_gtp == advertised
                if gnb_gtp and advertised
                else None,
                "observed_bidirectional_n3_mapping": bool(uplink and downlink and modifications),
                "application_acceptance_proven": False,
                "scope": "one-session wire joins; incomplete PDR/FAR/QER and PFCP coverage",
            }
        )
    return {
        "mappings": mappings,
        "facts": facts,
        "source_scope": "normal snapshots only",
        "synthetic": False,
        "agent_execution": False,
        "formal_quality": False,
        "unsupported_scope": [
            "all protocol IEs",
            "full PDR/FAR/QER lifecycle",
            "independent application-side state",
            "multiple concurrent UE disambiguation",
        ],
    }


def run(dataset, output):
    if output.exists():
        raise ValueError("fresh mapping audit output required")
    output.mkdir(parents=True)
    rows = []
    for path in sorted(dataset.glob("rounds/*/input/snapshot.json")):
        raw = path.read_bytes()
        result = map_sessions(json.loads(raw))
        number = path.parent.parent.name
        result["input_sha256"] = hashlib.sha256(raw).hexdigest()
        (output / (number + ".json")).write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        )
        rows.append(
            {
                "round": number,
                "input_sha256": result["input_sha256"],
                "establishments": len(result["mappings"]),
                "bidirectional_n3_mappings": sum(
                    m["observed_bidirectional_n3_mapping"] for m in result["mappings"]
                ),
                "ran_config_mismatches": sum(
                    m["ran_bound_advertised_consistent"] is False for m in result["mappings"]
                ),
            }
        )
    summary = {
        "rounds": len(rows),
        "rows": rows,
        "establishments": sum(r["establishments"] for r in rows),
        "bidirectional_n3_mappings": sum(r["bidirectional_n3_mappings"] for r in rows),
        "ran_config_mismatches": sum(r["ran_config_mismatches"] for r in rows),
        "model_calls": 0,
        "formal_quality": False,
        "method_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    (output / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.dataset, args.output)))
