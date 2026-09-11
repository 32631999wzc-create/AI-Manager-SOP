"""Verify the accepted four-session Phase 3 Golden evidence."""

from __future__ import annotations

from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SKILL = REPO / "skills/ai-product-development"
sys.path.insert(0, str(SKILL / "scripts"))

from project_runtime import ProjectRuntime
from run_golden import PHASES, inventory


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    accepted = json.loads((HERE / "accepted-run.json").read_text(encoding="utf-8"))
    folder = (HERE / accepted["directory"]).resolve()
    assert folder.is_relative_to(HERE / "evidence"), "evidence path escapes evidence root"
    assert folder.name == "G-final"
    actual_files = {path.relative_to(folder).as_posix(): digest(path) for path in sorted(folder.rglob("*")) if path.is_file()}
    assert actual_files == accepted["files_sha256"], "accepted evidence files changed"

    summary = json.loads((folder / "summary.json").read_text(encoding="utf-8"))
    assert summary["failed_attempts"] == []
    assert [item["phase"] for item in summary["phases"]] == [item["id"] for item in PHASES]
    assert all(item["status"] == "PASS" and not item["missing_reads"] and not item["missing_command_markers"] for item in summary["phases"])

    current_skill = inventory(SKILL)
    threads = set()
    for phase in PHASES:
        phase_folder = folder / phase["id"]
        result = json.loads((phase_folder / "result.json").read_text(encoding="utf-8"))
        metadata = json.loads((phase_folder / "metadata.json").read_text(encoding="utf-8"))
        assert result["status"] == "PASS"
        assert result["required_reads"] == phase["required_reads"]
        assert result["required_command_markers"] == phase["required_commands"]
        assert not result["missing_reads"] and not result["missing_command_markers"]
        assert len(result["thread_ids"]) == 1
        threads.update(result["thread_ids"])
        assert metadata["skill_sha256"] == current_skill
        assert metadata["skill_unchanged"] and metadata["exit_code"] == 0 and not metadata.get("timeout")
        assert metadata["sandbox"] == "workspace-write" and metadata["ephemeral"]
        command = metadata["command"]
        assert "--ignore-user-config" in command and "--ephemeral" in command
        assert not any(flag in command for flag in ["--approve-for-me", "--ignore-rules", "--dangerously-bypass-approvals-and-sandbox"])
        events = [json.loads(line) for line in (phase_folder / "trace.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        assert not any(event.get("type") == "turn.failed" for event in events)
    assert len(threads) == 4, "Golden phases are not four independent sessions"

    product = folder / "final-product"
    runtime = ProjectRuntime(product)
    assert runtime.validate()["valid"]
    completion = runtime.complete()
    assert completion["complete"], completion
    manifest = json.loads(json.dumps(__import__("yaml").safe_load((product / ".ai-product/manifest.yaml").read_text(encoding="utf-8"))))
    assert manifest["current_plan_version"] == "v2" and manifest["snapshot_sequence"] == 4
    plan = __import__("yaml").safe_load((product / ".ai-product/plan.yaml").read_text(encoding="utf-8"))
    states = {task["id"]: task["status"] for task in plan["plan"]["tasks"]}
    assert states == {"T1": "COMPLETED", "T2": "COMPLETED", "T3": "CANCELLED", "T4": "COMPLETED", "T5": "COMPLETED"}
    artifacts = __import__("yaml").safe_load((product / ".ai-product/registry/artifacts.yaml").read_text(encoding="utf-8"))["artifacts"]
    assert {item["id"] for item in artifacts if item["status"] == "ACTIVE"} == {"design-v1", "report-v1", "filtered-v1"}
    full = json.loads((product / "output.json").read_text(encoding="utf-8"))
    filtered = json.loads((product / "filtered-output.json").read_text(encoding="utf-8"))
    assert full["summary"] == {"received": 5, "unique": 4, "duplicates": 1}
    assert filtered["summary"]["received"] == 2 and all(item["source"] == "support" for item in filtered["items"])
    check = subprocess.run([sys.executable, "-B", "-X", "utf8", str(product / "verify_outputs.py")], capture_output=True, text=True, encoding="utf-8")
    assert check.returncode == 0, check.stdout + check.stderr
    print("PASS: four independent sessions, accepted hashes, v2 plan, four snapshots, active artifacts and complete Golden MVP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
