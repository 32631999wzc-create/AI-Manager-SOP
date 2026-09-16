"""Run one isolated Capability Need routing boundary without executing a capability."""

from __future__ import annotations

import argparse
import datetime
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from run_targeted_repair import read_commands, run_e2e


CASES = {
    "E": ("ABSENT", "EXECUTE", "The current scope is to decide Build Readiness for an editable AI queue suggestion. No requirements artifact exists; acceptance criteria, human override, and timeout behavior are undefined. The decision whether the feature is specified enough to build is pending."),
    "V": ("UNVERIFIED", "VERIFY", "The same Build Readiness decision is pending. A relevant PRD draft exists with acceptance criteria, human override, and timeout behavior, but it has not been checked against the current queue taxonomy or reviewed by the owners."),
    "R": ("VERIFIED", "REUSE", "The same Build Readiness decision is pending. The current approved PRD v2 has been checked against the current queue taxonomy and covers acceptance criteria, human override, and timeout behavior; no new requirements work is needed."),
    "N": ("IRRELEVANT", None, "The current assignment only asks to report the status of an already approved plan. Build Readiness is decided; there is no unresolved lifecycle gap, decision to unlock, or new evidence to assess."),
}
REQUIRED = ["SKILL.md", "references/runtime/planner.md"]


def prompt_for(case: str, contents: dict[str, str]) -> str:
    commands = [
        command
        for name in REQUIRED
        for command in read_commands(name, len(contents[name].splitlines()))
    ]
    return f"""Use the copied AI product development skill for one read-only Capability Need routing decision. Do not execute any capability, write files, or do product work.

Execute each command below separately and in exact order; read no other file:
{'; '.join(commands)}

Assignment facts: {CASES[case][2]}

Return exactly one JSON object and no prose:
{{"gap_exists":true,"evidence_state":"ABSENT|UNVERIFIED|VERIFIED|IRRELEVANT","decision_to_unlock":"specific pending decision or null","capability_need":{{"capability":"router domain slug or label","mode":"EXECUTE|VERIFY|REUSE","reason":"specific gap and asset state","supported_lifecycle_node":"node","decision_to_unlock":"specific pending decision"}}}}

Use capability_need=null when there is no gap. Select at most one primary domain for the requirements decision. An existing asset is not a reason to repeat its work; do not activate a capability merely because it is usually relevant."""


def grade(case: str, events: list[dict], contents: dict[str, str]) -> dict:
    routing = run_e2e.BEHAVIOR.assess_reads(events, {"required": REQUIRED, "support": {}}, contents)
    result = run_e2e.BEHAVIOR.agent_json(events)
    issues = []
    state, mode, _ = CASES[case]
    if result.get("gap_exists") is not (mode is not None):
        issues.append("GAP_MISMATCH")
    if result.get("evidence_state") != state:
        issues.append("EVIDENCE_STATE_MISMATCH")
    need = result.get("capability_need")
    if mode is None:
        if need is not None or result.get("decision_to_unlock") is not None:
            issues.append("UNNEEDED_CAPABILITY")
    elif not isinstance(need, dict):
        issues.append("CAPABILITY_MISSING")
    else:
        capability = {"需求评审与决策": "requirement-review"}.get(
            need.get("capability"), run_e2e._capability_id(need.get("capability"))
        )
        allowed = {"E": {"product-requirements"}, "V": {"product-requirements", "requirement-review"}, "R": {"product-requirements"}}[case]
        if capability not in allowed:
            issues.append("CAPABILITY_MISMATCH")
        if need.get("mode") != mode:
            issues.append("MODE_MISMATCH")
        if need.get("supported_lifecycle_node") != "Product Definition & Scope":
            issues.append("NODE_MISMATCH")
        for field in ("reason", "decision_to_unlock"):
            if not isinstance(need.get(field), str) or not need[field].strip():
                issues.append(f"{field.upper()}_MISSING")
        if result.get("decision_to_unlock") != need.get("decision_to_unlock"):
            issues.append("DECISION_MISMATCH")
    status = "PASS" if routing["status"] == "PASS" and not issues else "CONTRACT_FAIL"
    return {"case": case, "routing": routing, "issues": issues, "result": result, "status": status}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=sorted(CASES), required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--regrade-existing", type=Path)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--codex", default=shutil.which("codex"))
    args = parser.parse_args()
    if not args.codex:
        parser.error("Codex CLI not found")
    if args.regrade_existing:
        previous = args.regrade_existing
        metadata = json.loads((previous / "metadata.json").read_text(encoding="utf-8"))
        if metadata["skill_sha256"] != run_e2e.inventory(run_e2e.SKILL):
            parser.error("Current Skill differs from the captured trace; cannot regrade")
        events = [json.loads(line) for line in (previous / "trace.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        contents = {name: (run_e2e.SKILL / name).read_text(encoding="utf-8") for name in REQUIRED}
        outcome = grade(args.case, events, contents)
        outcome["regraded_from"] = "result.json"
        (previous / "regraded-result.json").write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Capability-{args.case} regraded: {outcome['status']}", flush=True)
        return 0 if outcome["status"] == "PASS" else 1
    if args.output is None:
        parser.error("--output is required unless --regrade-existing is used")
    args.output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="ai-skill-capability-") as temporary:
        work = Path(temporary)
        copied = work / "skill"
        shutil.copytree(run_e2e.SKILL, copied)
        hashes = run_e2e.inventory(copied)
        contents = {name: (copied / name).read_text(encoding="utf-8") for name in REQUIRED}
        task_prompt = prompt_for(args.case, contents)
        command = [args.codex, "exec", "--json", "--ephemeral", "--ignore-user-config", "-m", "gpt-5.6-luna", "-c", 'model_reasoning_effort="low"', "-s", "read-only", "-c", 'windows.sandbox="elevated"', "--skip-git-repo-check", "-C", str(work), "-"]
        (args.output / "prompt.txt").write_text(task_prompt, encoding="utf-8")
        infra = []
        exit_code = None
        with (args.output / "trace.jsonl").open("w", encoding="utf-8") as stdout, (args.output / "stderr.txt").open("w", encoding="utf-8") as stderr:
            try:
                process = subprocess.run(command, input=task_prompt, stdout=stdout, stderr=stderr, text=True, encoding="utf-8", timeout=args.timeout)
                exit_code = process.returncode
                if exit_code:
                    infra.append(f"PROCESS_EXIT_NONZERO:{exit_code}")
            except subprocess.TimeoutExpired:
                infra.append("MODEL_TIMEOUT")
            except OSError as exc:
                infra.append(f"PROCESS_START_FAILED:{type(exc).__name__}:{exc}")
        events = []
        for number, line in enumerate((args.output / "trace.jsonl").read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    event = json.loads(line)
                    if not isinstance(event, dict):
                        raise ValueError("not an object")
                    events.append(event)
                except (ValueError, json.JSONDecodeError):
                    infra.append(f"TRACE_INVALID_JSON_LINE:{number}")
                    break
        if not any(event.get("type") == "turn.completed" for event in events):
            infra.append("TRACE_INCOMPLETE")
        if not any(event.get("type") == "item.completed" and isinstance(event.get("item"), dict) and event["item"].get("type") == "agent_message" for event in events):
            infra.append("RESULT_MISSING")
        if hashes != run_e2e.inventory(copied):
            infra.append("SKILL_COPY_CHANGED")
        if infra:
            outcome = {"case": args.case, "routing": None, "issues": [], "result": None, "status": "INFRA_BLOCKED"}
        else:
            try:
                outcome = grade(args.case, events, contents)
            except (ValueError, json.JSONDecodeError) as exc:
                outcome = {"case": args.case, "routing": None, "issues": [f"RESULT_JSON_INVALID:{exc}"], "result": None, "status": "CONTRACT_FAIL"}
        outcome["infra_issues"] = infra
        metadata = {"started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "skill_sha256": hashes, "exit_code": exit_code, "sandbox": "read-only", "ephemeral": True}
        (args.output / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "result.json").write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Capability-{args.case}: {outcome['status']}", flush=True)
        return 0 if outcome["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
