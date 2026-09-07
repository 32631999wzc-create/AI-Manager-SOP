"""Replay the accepted raw traces against the current Skill; no new model execution."""
import json
from pathlib import Path
from run_routing import HERE, SKILL, SCENARIOS, inventory, sha, assess

def verify():
    accepted = json.loads((HERE / "accepted-runs.json").read_text(encoding="utf-8"))
    assert set(accepted) == {s["id"] for s in SCENARIOS}, "Three accepted scenarios required"
    files = inventory(SKILL)
    contents = {n: (SKILL / n).read_text(encoding="utf-8") for n in files}
    threads, roots = set(), set()
    for case in SCENARIOS:
        entry = accepted[case["id"]]
        folder = (HERE / entry["directory"]).resolve()
        assert folder.is_relative_to(HERE / "evidence"), "Evidence path outside fixture"
        for name, digest in entry["files_sha256"].items():
            assert sha((folder / name).read_bytes()) == digest, "Evidence changed: " + name
        assert set(entry["files_sha256"]) == {"prompt.txt", "trace.jsonl", "stderr.txt", "metadata.json", "result.json"}
        meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
        assert meta["skill_sha256"] == files, "Accepted trace is for another Skill version"
        assert meta["skill_unchanged"] and meta["exit_code"] == 0 and not meta.get("timeout")
        args = meta["command"]
        assert args[args.index("-s") + 1] == "read-only"
        assert "--ephemeral" in args and "--ignore-user-config" in args
        assert not any(flag in args for flag in ["--approve-for-me", "--ignore-rules",
                      "--dangerously-bypass-approvals-and-sandbox", "resume", "--add-dir"])
        roots.add(args[args.index("-C") + 1])
        events = [json.loads(line) for line in (folder / "trace.jsonl").read_text(encoding="utf-8").splitlines()]
        started = [e["thread_id"] for e in events if e.get("type") == "thread.started"]
        assert len(started) == 1, "Exactly one independent session per scenario"
        threads.update(started)
        replay = assess(events, case, contents)
        stored = json.loads((folder / "result.json").read_text(encoding="utf-8"))
        assert replay == stored, "Saved result differs from tool trace replay"
        assert replay["status"] == "PASS", case["id"] + " did not pass"
        assert (folder / "prompt.txt").read_text(encoding="utf-8").endswith(case["task"]), "Scenario input drift"
        print(case["id"] + ": PASS, verified " + str(len(replay["reads_in_order"])) + " actual file reads")
    assert len(threads) == 3 and len(roots) == 3, "Scenarios are not independent"
    print("PASS: current Skill hashes, raw evidence hashes, separate read-only sessions and trace replay")

if __name__ == "__main__":
    verify()
