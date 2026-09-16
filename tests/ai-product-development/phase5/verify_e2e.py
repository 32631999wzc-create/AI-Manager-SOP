"""Regrade existing Phase 5 traces against the current skill and scenario contract."""

from __future__ import annotations

from pathlib import Path
import argparse
import json

import run_e2e


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    args = parser.parse_args()

    current_hashes = run_e2e.inventory(run_e2e.SKILL)
    contents = {
        name: (run_e2e.SKILL / name).read_text(encoding="utf-8")
        for name in current_hashes
        if name.endswith((".md", ".yaml", ".py"))
    }
    by_id = {scenario["id"]: scenario for scenario in run_e2e.SCENARIOS}
    summaries = []
    for run_dir in args.runs:
        prior = json.loads((run_dir / "result.json").read_text(encoding="utf-8"))
        metadata = json.loads((run_dir / "metadata.json").read_text(encoding="utf-8"))
        scenario = by_id[prior["scenario"]]
        events = [
            json.loads(line)
            for line in (run_dir / "trace.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        result = run_e2e.grade(events, scenario, contents)
        hash_matches = metadata.get("skill_sha256") == current_hashes
        if not hash_matches:
            result["status"] = "FAIL"
        summaries.append({
            "scenario": scenario["id"],
            "run": run_dir.as_posix(),
            "skill_hash_matches": hash_matches,
            "routing": result["routing"]["status"],
            "behavior_issues": result["behavior_issues"],
            "validation_errors": result["validation_errors"],
            "status": result["status"],
        })
    print(json.dumps(summaries, ensure_ascii=False, indent=2))
    return 0 if all(item["status"] == "PASS" for item in summaries) else 1


if __name__ == "__main__":
    raise SystemExit(main())
