"""Pinned OpsEval 5G MCQ adapter: small zero-shot pilot, separate from UPF VPR."""

import argparse
import hashlib
import json
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from time import perf_counter

import httpx


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def selection(items):
    # Select before inference by ID hash. No answer-dependent sampling.
    eligible = [
        i
        for i in items
        if i.get("qtype") == 0 and i.get("answer") in "ABCDEFGH"[: len(i.get("choices", []))]
    ]
    return sorted(eligible, key=lambda i: hashlib.sha256(i["id"].encode()).hexdigest())[:24]


def run(source, output, deployment):
    if output.exists():
        raise ValueError("fresh output required")
    output.mkdir(parents=True)
    data_file = source / "data/zh/test/5G Communication.json"
    chosen = selection(read(data_file))
    assert len(chosen) == 24 and len({i["id"] for i in chosen}) == 24
    profile = read(deployment)
    from upf_agent.config import load_model_config

    model = load_model_config(Path(__file__).resolve().parents[1] / "config/models.yaml")
    model_name = model.generation["baseline"].served_name
    shutil.copytree(source, output / "source")
    gold = [{"id": i["id"], "answer": i["answer"]} for i in chosen]
    public = [{"id": i["id"], "question": i["question"], "choices": i["choices"]} for i in chosen]
    write(output / "private/official-labels.json", gold)
    write(output / "input/questions.json", public)
    write(
        output / "protocol.json",
        {
            "official_repository": "https://github.com/NetManAIOps/OpsEval-Datasets",
            "commit": read(source / "commit.json")["sha"],
            "language": "zh",
            "domain": "5G Communication",
            "split": "public test",
            "sample_count": 24,
            "selection": "lowest sha256(id) among qtype=0, one valid label; no tuning",
            "dataset_sha256": sha(data_file),
            "question_sha256": sha(output / "input/questions.json"),
            "gold_sha256": sha(output / "private/official-labels.json"),
            "driver_sha256": sha(Path(__file__)),
            "model": model_name,
            "deployment": profile,
            "workers": 4,
            "temperature": 0,
            "max_tokens": 32,
            "method": "naive zero-shot, constrained answer only; no retrieval or UPF tools",
            "official_baseline_scope": (
                "zero-shot method family in README; no released runner found"
            ),
            "published_full_leaderboard_reproduction": False,
            "official_labels_in_model_input": False,
            "new_upf_heldout_consumed": False,
            "metric": "exact option accuracy, errors included in all-24 denominator",
            "dataset_license": "LICENSE MIT; README frontmatter Apache-2.0 conflict retained",
            "redistribution": (
                "local research attachment only, excluded from public synthetic bundle"
            ),
            "model_training_overlap_unknown": True,
            "independent_UPF_Gold": False,
        },
    )

    def execute(index, item):
        folder = output / "runs" / f"item-{index:03d}"
        options = list("ABCDEFGH"[: len(item["choices"])])
        request = {
            "model": model_name,
            "temperature": 0,
            "max_tokens": 32,
            "messages": [
                {
                    "role": "system",
                    "content": "Answer the multiple-choice question. Select one option.",
                },
                {"role": "user", "content": item["question"]},
            ],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "opseval_choice",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {"answer": {"enum": options, "type": "string"}},
                        "required": ["answer"],
                        "additionalProperties": False,
                    },
                },
            },
        }
        write(folder / "request.json", request)
        start = perf_counter()
        result = {"id": item["id"], "model_calls_attempted": 1, "answer": None, "error": None}
        try:
            with httpx.Client(timeout=180, trust_env=False) as client:
                response = client.post(profile["endpoint"] + "/chat/completions", json=request)
            (folder / "response.txt").write_text(response.text)
            result["http_status"] = response.status_code
            response.raise_for_status()
            value = response.json()
            result["usage"] = value.get("usage")
            choice = value["choices"][0]
            result["finish_reason"] = choice["finish_reason"]
            assert choice["finish_reason"] == "stop", "truncated or incomplete output"
            parsed = json.loads(choice["message"]["content"])
            assert set(parsed) == {"answer"} and parsed["answer"] in options
            result["answer"] = parsed["answer"]
        except Exception as exc:
            result["error"] = {"type": type(exc).__name__, "message": str(exc)}
        result["seconds"] = perf_counter() - start
        write(folder / "result.json", result)
        return result

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(execute, n, i) for n, i in enumerate(public, 1)]
        rows = []
        for f in as_completed(futures):
            rows.append(f.result())
            write(output / "progress.json", {"completed": len(rows), "planned": 24})
    result = audit(output)
    write(output / "summary.json", result)
    write(
        output / "artifact-hashes.json",
        {str(p.relative_to(output)): sha(p) for p in output.rglob("*") if p.is_file()},
    )
    return result


def audit(root):
    protocol = read(root / "protocol.json")
    source = root / "source"
    assert sha(source / "data/zh/test/5G Communication.json") == protocol["dataset_sha256"]
    selected = selection(read(source / "data/zh/test/5G Communication.json"))
    public = read(root / "input/questions.json")
    gold = read(root / "private/official-labels.json")
    assert gold == [{"id": i["id"], "answer": i["answer"]} for i in selected]
    assert public == [
        {"id": i["id"], "question": i["question"], "choices": i["choices"]} for i in selected
    ]
    assert sha(root / "input/questions.json") == protocol["question_sha256"]
    assert sha(root / "private/official-labels.json") == protocol["gold_sha256"]
    rows = []
    for n, (item, label) in enumerate(zip(public, gold, strict=True), 1):
        folder = root / "runs" / f"item-{n:03d}"
        request, result = read(folder / "request.json"), read(folder / "result.json")
        assert request["messages"][1] == {"role": "user", "content": item["question"]}
        assert "solution" not in request and result["id"] == item["id"] == label["id"]
        if not result["error"]:
            response = json.loads((folder / "response.txt").read_text())
            assert (
                json.loads(response["choices"][0]["message"]["content"])["answer"]
                == result["answer"]
            )
        rows.append(result | {"correct": result["answer"] == label["answer"]})
    correct = sum(r["correct"] for r in rows)
    dev = read(source / "data/zh/dev/5G Communication.json")
    from collections import Counter

    majority = Counter(i["answer"] for i in dev).most_common(1)[0][0]
    return {
        "domain": "OpsEval zh 5G MCQ",
        "runs": len(rows),
        "correct": correct,
        "exact_option_accuracy": correct / 24,
        "failures": sum(bool(r["error"]) for r in rows),
        "actual_model_calls": sum(r["model_calls_attempted"] for r in rows),
        "model_call_definition": (
            "transport request attempts; processing on failed responses unknown"
        ),
        "successful_inference_receipts": sum(not r["error"] for r in rows),
        "development_majority_option": majority,
        "development_majority_accuracy": sum(i["answer"] == majority for i in gold) / 24,
        "uniform_chance_expected_accuracy": sum(1 / len(i["choices"]) for i in public) / 24,
        "rows": rows,
        "audit_pass": len(rows) == 24,
        "official_full_baseline_reproduced": False,
        "UPF_VPR": None,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("action", choices=["run", "audit"])
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--deployment", type=Path)
    a = p.parse_args()
    result = run(a.root, a.output, a.deployment) if a.action == "run" else audit(a.root)
    if a.action == "audit":
        assert not a.output.exists()
        if (a.root / "artifact-hashes.json").exists():
            assert all(
                sha(a.root / n) == h for n, h in read(a.root / "artifact-hashes.json").items()
            )
        write(a.output, result)
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}))
