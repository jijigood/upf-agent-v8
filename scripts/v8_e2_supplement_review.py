"""Read-only replay of E2 mixed pilot, PPR sensitivity and actual Ledger probes."""

import argparse
import json
import sqlite3
from pathlib import Path

from v8_e2_supplement import SELECTED, load_case

from upf_agent.v8.actions import full_actions
from upf_agent.v8.dependency import LocalEvaluator, complete_results
from upf_agent.v8.e2 import METHODS, score_hits
from upf_agent.v8.evaluator import full_evaluate
from upf_agent.v8.models import EvidenceBinding, OrchestrationData
from upf_agent.v8.phase1 import write_json
from upf_agent.v8.plan_source_verifier import verify_plan_source


def review(batch, root):
    def read(path):
        return json.loads(path.read_text())
    assert read(root / "protocol.json")["development_selection_after_initial_full_batch"]
    rows = []
    hit_count = 0
    for number in SELECTED:
        case, _, _, _, _ = load_case(batch, number)
        for method, alpha, scope, filename in [
            *[
                (
                    m,
                    0.85 if m == METHODS[3] else None,
                    "mixed-pilot",
                    root / "pilot" / f"query-{number:03d}" / f"{m}.json",
                )
                for m in METHODS
            ],
            *[
                (
                    METHODS[3],
                    a,
                    "sensitivity",
                    root / "sensitivity" / f"query-{number:03d}" / f"alpha-{a}.json",
                )
                for a in [0.7, 0.95]
            ],
        ]:
            result = read(filename)
            for hit in result["hits"]:
                assert verify_plan_source(
                    batch / "corpus", EvidenceBinding.model_validate(hit["binding"]), case["task"]
                )
                hit_count += 1
            row = {
                **score_hits(case, result, 20),
                "method": method,
                "alpha": alpha,
                "scope": scope,
                "scan": result["scan"],
            }
            if scope == "sensitivity":
                row.update(
                    converged=result["ranking"]["converged"],
                    iterations=result["ranking"]["iterations"],
                )
            rows.append(row)
    assert rows == read(root / "observations.json")
    probes = []
    for folder in sorted((root / "ledger-probes").iterdir()):
        p = read(folder / "probe.json")
        db = sqlite3.connect(
            f"file:{folder / 'data/v8/ledger.sqlite3'}?mode=ro&immutable=1", uri=True
        )
        try:
            values = db.execute("SELECT data FROM runs").fetchall()
            assert len(values) == 1
            saved = OrchestrationData.model_validate_json(values[0][0])
            bindings = [
                EvidenceBinding.model_validate_json(row[0])
                for row in db.execute("SELECT payload FROM evidence")
            ]
            assert sorted(b.model_dump_json() for b in bindings) == sorted(
                b.model_dump_json() for b in saved.bindings
            )
            assert len(bindings) == p["accepted_bindings"]
            assert all(verify_plan_source(folder, b, saved.task) for b in bindings)
            receipts = db.execute("SELECT kind,status,result FROM receipts").fetchall()
            assert len(receipts) == 1 and receipts[0][:2] == ("tool", "committed")
            assert len(json.loads(receipts[0][2])["bindings"]) == len(bindings)
            states = full_evaluate(saved.task, saved.contract, bindings, saved.batch_id)
            actions = full_actions(saved.task, saved.contract, bindings, states, saved.batch_id)
            local = LocalEvaluator(saved.task, saved.contract, bindings, saved.batch_id)
            assert complete_results(states, actions) == complete_results(
                local.states, local.actions
            )
            assert complete_results(states, actions) == complete_results(
                saved.states, {a.action_id: a for a in saved.actions}
            )
            rid = read(folder / "query.json")["requirement"]["requirement_id"]
            assert states[rid].code.value == p["primary_K_state"]
            assert states[rid].valid == p["primary_K_closed"]
            if p["strategy"] == "tampered-source":
                assert not bindings and p["rejected_bindings"] == 19
            elif p["strategy"] == "multi-block-conflict":
                assert len(bindings) == 19 and not states[rid].valid
            else:
                assert len(bindings) == 1 and states[rid].valid
            probes.append(p)
        finally:
            db.close()
    return {
        "pilot_retrievals": 120,
        "sensitivity_retrievals": 48,
        "source_checked_hits": hit_count,
        "actual_committed_Ledger_probes": len(probes),
        "probes": probes,
        "new_P3_calls": 0,
        "new_model_calls": 0,
        "formal_acceptance": False,
        "pass": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("new read-only audit ID required")
    result = review(args.batch, args.root)
    write_json(args.output, result)
    print({k: v for k, v in result.items() if k != "probes"})
