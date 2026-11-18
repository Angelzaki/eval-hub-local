from __future__ import annotations

import json
from pathlib import Path


KNOWN = {
    "rag-eval-platform": ["results/scenario_a.json", "results/baseline.json"],
    "chunk-lab": ["results/chunk_experiment.json"],
    "prompt-bench-local": ["results/prompt_bench.json"],
    "faithfulness-guard": [],
    "rag-trace-local": ["results/traces.jsonl"],
    "retrieval-tuner-local": ["results/retrieval_tune.json"],
    "citation-auditor-local": ["results/citation_audit.json"],
    "synthetic-qa-local": ["output/questions.synthetic.jsonl"],
    "context-overlap-lab": ["results/overlap_report.json"],
    "abstention-lab-local": ["results/abstention_calibration.json"],
    "doc-drift-lab": ["results/doc_drift.json"],
    "rag-smoke-local": ["results/smoke_report.json"],
    "model-router-local": ["results/router_bench.json"],
    "agent-failure-lab": ["results/agent_failures.json"],
    "llm-cost-radar": ["results/calls.json"],
    "prompt-firewall": [],
    "llm-ci-gates": [],
    "support-copilot-lab": [],
    "local-rag-pipeline": [],
    "local-ai-agents": [],
    "eval-hub-local": [],
}


def _read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def collect(workspace: Path) -> list[dict]:
    cards = []
    for repo, relatives in KNOWN.items():
        root = workspace / repo
        card = {
            "repo": repo,
            "exists": root.exists(),
            "artifacts": [],
            "summary": "sin artefactos todavía",
            "score": None,
        }
        if not root.exists():
            cards.append(card)
            continue

        for rel in relatives:
            path = root / rel
            if not path.exists():
                continue
            if path.suffix == ".jsonl":
                lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
                card["artifacts"].append({"path": rel, "type": "jsonl", "count": len(lines)})
                card["summary"] = f"{len(lines)} traces" if "trace" in rel else f"{len(lines)} items"
                continue
            data = _read_json(path)
            if not data:
                continue
            card["artifacts"].append({"path": rel, "type": "json"})
            if "overall" in data:
                card["score"] = data["overall"]
                card["summary"] = f"overall {data['overall']:.0%}"
            elif "best" in data and "strategies" in data:
                best = data["best"]
                score = data["strategies"][best]["retrieval_score"]
                card["score"] = score
                card["summary"] = f"best={best} ({score:.0%})"
            elif "best" in data and "prompts" in data:
                best = data["best"]
                score = data["prompts"][best]["avg_score"]
                card["score"] = score
                card["summary"] = f"best={best} ({score:.0%})"
            elif "best" in data and isinstance(data["best"], dict) and "hit_rate" in data["best"]:
                best = data["best"]
                card["score"] = best["hit_rate"]
                card["summary"] = (
                    f"top_k={best['top_k']} min_score={best['min_score']} ({best['hit_rate']:.0%})"
                )
            elif "best" in data and isinstance(data["best"], dict) and "accuracy" in data["best"]:
                best = data["best"]
                card["score"] = best["accuracy"]
                card["summary"] = (
                    f"score={best['min_score']} overlap={best['min_overlap']} ({best['accuracy']:.0%})"
                )
            elif "score" in data and "passed" in data:
                card["score"] = data["score"]
                card["summary"] = f"passed {data['passed']}/{data['total']}"
            elif "score" in data and "avg" in data:
                card["score"] = data["score"]
                card["summary"] = f"answer_context {data['score']:.0%}"
            elif "delta" in data and "scenario_b" in data:
                card["score"] = data.get("score", data["scenario_b"]["hit_rate"])
                card["summary"] = f"delta={data['delta']:+.0%} B={data['scenario_b']['hit_rate']:.0%}"
        if not card["artifacts"]:
            card["summary"] = "repo listo, sin runs recientes" if relatives else "componente activo"
        cards.append(card)
    return cards
