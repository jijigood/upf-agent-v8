"""Bounded plain IPv4/ICMP observations; no delivery, loss or RCA oracle.

Linux cooked layouts follow libpcap pcap/sll.h; ICMP echo follows RFC 792.
UDP/GTP, IPv6, fragmentation and unsupported links remain explicit unknowns.
"""

import base64
import hashlib
import ipaddress
import struct
from collections import Counter

VERSION = "v8-e1-plain-icmp-observations-1"


def observations(capture):
    raw = base64.b64decode(capture["capture_base64"], validate=True)
    if len(raw) > 64 * 1024 * 1024 or len(raw) < 24:
        raise ValueError("invalid/bounded classic pcap size")
    magic = raw[:4].hex()
    endian = "<" if magic in {"d4c3b2a1", "4d3cb2a1"} else ">"
    if magic not in {"d4c3b2a1", "4d3cb2a1", "a1b2c3d4", "a1b23c4d"}:
        raise ValueError("classic pcap required")
    scale = 1_000_000_000 if magic in {"4d3cb2a1", "a1b23c4d"} else 1_000_000
    link = struct.unpack(endian + "I", raw[20:24])[0]
    offset, ordinal, rows, skipped = 24, 0, [], Counter()
    while offset < len(raw):
        if offset + 16 > len(raw) or ordinal >= 100_000:
            raise ValueError("partial or unbounded capture records")
        sec, fraction, included, original = struct.unpack(
            endian + "IIII", raw[offset : offset + 16]
        )
        offset += 16
        if fraction >= scale or included > original or offset + included > len(raw):
            raise ValueError("invalid record length/time")
        packet = raw[offset : offset + included]
        offset += included
        ordinal += 1
        if included < original:
            skipped["truncated"] += 1
            continue
        prefix, protocol, ifindex, packet_type = 0, 0x0800, None, None
        if link == 276 and len(packet) >= 20:
            prefix, protocol = 20, struct.unpack("!H", packet[:2])[0]
            ifindex = struct.unpack("!I", packet[4:8])[0]
            packet_type = packet[10]
        elif link == 113 and len(packet) >= 16:
            prefix, protocol = 16, struct.unpack("!H", packet[14:16])[0]
            packet_type = struct.unpack("!H", packet[:2])[0]
        elif link == 1 and len(packet) >= 14:
            prefix, protocol = 14, struct.unpack("!H", packet[12:14])[0]
        elif link != 101:
            skipped["unsupported_link_or_short_header"] += 1
            continue
        packet = packet[prefix:]
        if protocol != 0x0800 or len(packet) < 20 or packet[0] >> 4 != 4:
            skipped["not_plain_ipv4"] += 1
            continue
        ihl = (packet[0] & 15) * 4
        total, fragment = struct.unpack("!HH", packet[2:4] + packet[6:8])
        if ihl < 20 or total < ihl or total > len(packet):
            skipped["invalid_ipv4_length"] += 1
            continue
        if fragment & 0x3FFF:
            skipped["fragmented_ipv4"] += 1
            continue
        if packet[9] != 1:
            skipped["other_ip_protocol_including_gtp_pfcp"] += 1
            continue
        icmp = packet[ihl:total]
        if len(icmp) < 8 or icmp[0] not in {0, 8} or icmp[1] != 0:
            skipped["not_complete_icmp_echo"] += 1
            continue
        identifier, sequence = struct.unpack("!HH", icmp[4:8])
        rows.append(
            {
                "record": ordinal,
                "epoch": sec + fraction / scale,
                "src": str(ipaddress.IPv4Address(packet[12:16])),
                "dst": str(ipaddress.IPv4Address(packet[16:20])),
                "icmp_type": icmp[0],
                "identifier": identifier,
                "sequence": sequence,
                "payload_sha256": hashlib.sha256(icmp[8:]).hexdigest(),
                "interface_index": ifindex,
                "cooked_packet_type": packet_type,
            }
        )
    return {
        "version": VERSION,
        "capture_sha256": hashlib.sha256(raw).hexdigest(),
        "rows": rows,
        "skipped": dict(skipped),
        "packet_records": ordinal,
        "delivery_or_cause_proved": False,
        "checksum_validation": False,
    }


def compare(left, right, *, tolerance_seconds=2):
    if left["capture_sha256"] == right["capture_sha256"]:
        raise ValueError("independent capture bytes required")
    if not 0 <= tolerance_seconds <= 5:
        raise ValueError("bounded time tolerance required")

    def key(r):
        return tuple(
            r[k] for k in ("src", "dst", "icmp_type", "identifier", "sequence", "payload_sha256")
        )

    # Each physical observation can match at most one peer; retain repeated interface records.
    used, pairs = set(), []
    for row in left["rows"]:
        candidates = [
            (abs(row["epoch"] - peer["epoch"]), i, peer)
            for i, peer in enumerate(right["rows"])
            if i not in used
            and key(row) == key(peer)
            and abs(row["epoch"] - peer["epoch"]) <= tolerance_seconds
        ]
        if candidates:
            delta, i, peer = min(candidates, key=lambda c: (c[0], c[1]))
            used.add(i)
            pairs.append(
                {
                    "left_record": row["record"],
                    "right_record": peer["record"],
                    "icmp_type": row["icmp_type"],
                    "seconds_apart": delta,
                }
            )
    return {
        "matching_rule": "IPv4 endpoints/type/id/sequence/payload hash plus bounded time",
        "pairs": pairs,
        "matched_observations": len(pairs),
        "left_unmatched": len(left["rows"]) - len(pairs),
        "right_unmatched": len(right["rows"]) - len(pairs),
        "unmatched_means_packet_loss": False,
        "delivery_or_cause_proved": False,
    }
