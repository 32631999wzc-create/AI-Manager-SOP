"""Replay the eight accepted Phase 2 traces against the current Skill."""
from pathlib import Path
import hashlib
import json

from run_behavior import HERE, SKILL, SCENARIOS, grade, inventory, prompt_for


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify() -> None:
    accepted = json.loads((HERE / "accepted-runs.json").read_text(encoding="utf-8"))
    scenario_ids = {scenario["id"] for scenario in SCENARIOS}
    assert set(accepted) == scenario_ids, "Eight accepted scenarios required"
    files = inventory(SKILL)
    contents = {
        name: (SKILL / name).read_text(encoding="utf-8")
        for name in files
        if name.endswith((".md", ".yaml", ".py"))
    }
    threads, roots = set(), set()
    required_evidence = {"prompt.txt", "trace.jsonl", "stderr.txt", "metadata.json", "result.json"}
    for scenario in SCENARIOS:
        entry = accepted[scenario["id"]]
        folder = (HERE / entry["directory"]).resolve()
        assert folder.is_relative_to(HERE / "evidence"), "Evidence path outside fixture"
        assert set(entry["files_sha256"]) == required_evidence
        for name, digest in entry["files_sha256"].items():
            assert sha((folder / name).read_bytes()) == digest, "Evidence changed: " + name
        metadata = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert metadata["skill_sha256"] == files, "Accepted trace is for another Skill version"
        assert metadata["skill_unchanged"] and metadata["exit_code"] == 0 and not metadata.get("timeout")
        args = metadata["command"]
        assert args[args.index("-s") + 1] == "read-only"
        assert "--ephemeral" in args and "--ignore-user-config" in args
        assert not any(flag in args for flag in [
            "--approve-for-me", "--ignore-rules", "--dangerously-bypass-approvals-and-sandbox",
            "resume", "--add-dir",
        ])
        roots.add(args[args.index("-C") + 1])
        assert (folder / "prompt.txt").read_text(encoding="utf-8") == prompt_for(scenario), "Prompt drift"
        events = [
            json.loads(line)
            for line in (folder / "trace.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        assert not any(event.get("type") == "turn.failed" for event in events), "Failed turn in accepted trace"
        started = [event["thread_id"] for event in events if event.get("type") == "thread.started"]
        assert len(started) == 1, "Exactly one independent session per scenario"
        threads.update(started)
        replay = grade(events, scenario, contents)
        stored = json.loads((folder / "result.json").read_text(encoding="utf-8"))
        assert replay == stored, "Saved result differs from trace replay"
        assert replay["status"] == "PASS", scenario["id"] + " did not pass"
        print(f'{scenario["id"]}: PASS, {len(replay["routing"]["reads_in_order"])} verified reads')
    assert len(threads) == 8 and len(roots) == 8, "Scenarios are not independent"
    print("PASS: current Skill hashes, evidence hashes, eight read-only sessions and trace replay")


if __name__ == "__main__":
    verify()
