"""Run all E3 methods with an explicitly pinned, unmodified native P5 deployment."""

import argparse
import hashlib
import json
from pathlib import Path

from upf_agent.config import load_model_config
from upf_agent.v8 import e3_p5
from upf_agent.v8.e3 import run_e3
from upf_agent.v8.phase1 import write_json


def run(project, output, deployment):
    profile = json.loads(deployment.read_text())
    original = load_model_config

    def pinned(path):
        config = original(path)
        config.generation["baseline"] = config.generation["baseline"].model_copy(
            update={
                "endpoint": profile["endpoint"],
                "max_num_seqs": 8,
                "gpu_memory_utilization": 0.82,
            }
        )
        return config

    e3_p5.load_model_config = pinned
    try:
        result = run_e3(project, output, native_p5=True, shared_public_tools=True)
    finally:
        e3_p5.load_model_config = original
    write_json(output / "actual-deployment.json", profile)
    write_json(
        output / "driver-provenance.json",
        {
            "driver_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "deployment_sha256": hashlib.sha256(deployment.read_bytes()).hexdigest(),
            "endpoint_pinned_before_calls": profile["endpoint"],
            "shared_host": True,
            "latency_superiority_claim": False,
            "production_source_changed": False,
            "heldout_consumed": False,
        },
    )
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--deployment", type=Path, required=True)
    p.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    a = p.parse_args()
    result = run(a.project.resolve(), a.output.resolve(), a.deployment.resolve())
    print(json.dumps({k: v for k, v in result.items() if k != "source"}))
