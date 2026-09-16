"""Run one isolated Replan-trigger boundary check without replaying full E2E."""

from __future__ import annotations

from pathlib import Path
import argparse
import datetime
import json
import shutil
import subprocess
import tempfile

import run_e2e


CASES = {
    "A": {
        "required": ["SKILL.md", "references/runtime/planner.md"],
        "facts": "baseline_exists=false; change_event_exists=false; material_impact_exists=false. This is the first Greenfield request and initial plan.",
        "mode": "INITIAL_PLAN", "required_replan": False, "change_type": None,
    },
    "B": {
        "required": ["SKILL.md", "references/runtime/planner.md", "references/runtime/replan-recovery.md"],
        "facts": "baseline_exists=true with active Profile and Plan v1; after baseline the queue taxonomy changed from 8 to 10; T-ROUTING-DESIGN, T-ROUTING-IMPLEMENT and T-ROUTING-EVAL are affected; T-EXPORT is unaffected; delivery target and assignment scope are unchanged.",
        "mode": "LOCAL_REPLAN", "required_replan": True, "change_type": "INPUT_CHANGE",
    },
    "C": {
        "required": ["SKILL.md", "references/runtime/planner.md"],
        "facts": "baseline_exists=true with active Profile and Plan v1; after baseline a stakeholder supplied a new explanatory note; it changes no Task, Artifact, Decision, Assumption, Dependency, Acceptance Criteria, Scope or Node Profile.",
        "mode": "CONTINUE", "required_replan": False, "change_type": None,
    },
    "D": {
        "required": ["SKILL.md", "references/runtime/planner.md", "references/runtime/replan-recovery.md", "references/runtime/execution-profile.md"],
        "facts": "baseline_exists=true with active Prototype Profile and Plan v1; after baseline the authorized delivery target changed to MVP and assignment scope now includes a controlled pilot; T-PROTOTYPE remains valid and T-MVP-PROFILE must be added.",
        "mode": "PROFILE_REPLAN", "required_replan": True, "change_type": "SCOPE_CHANGE",
    },
}


def read_commands(name: str, line_count: int) -> list[str]:
    path = f"skill/{name}"
    commands = []
    for start in range(0, line_count, 40):
        if start == 0:
            selector = "Select-Object -First 40"
        elif start + 40 < line_count:
            selector = f"Select-Object -Skip {start} -First 40"
        else:
            selector = f"Select-Object -Skip {start}"
        commands.append(f"Get-Content -LiteralPath '{path}' -Encoding UTF8 | {selector}")
    return commands


def prompt(case: dict, contents: dict[str, str]) -> str:
    commands = [
        command
        for name in case["required"]
        for command in read_commands(name, len(contents[name].splitlines()))
    ]
    return f"""Use the copied AI product development skill for one targeted, read-only Replan trigger check. Do not write files, use external services, or perform product work.

Execute every command below separately and in exact order. Read no other file:
{'; '.join(commands)}

Facts: {case['facts']}

Return exactly one JSON object and no prose:
{{
  "trigger_assessment":{{"baseline_exists":true,"change_event_exists":true,"material_impact_exists":true,"operation_mode":"INITIAL_PLAN|CONTINUE|LOCAL_REPLAN|PROFILE_REPLAN"}},
  "replan":{{"required":true,"change_type":"INPUT_CHANGE|SCOPE_CHANGE|null","reopen_trigger":null,"actions":[{{"action":"PRESERVE|OUTDATE|ADD|CANCEL","target":"task id"}}]}},
  "claims":{{"external_write_performed":false,"invented_evidence":false}}
}}

Use only the supplied facts. INITIAL_PLAN and CONTINUE have required=false, null change_type/reopen_trigger and no actions. A Replan must preserve unaffected named work and change only named affected work."""


def grade(case_id: str, events: list[dict], contents: dict[str, str]) -> dict:
    case = CASES[case_id]
    routing = run_e2e.BEHAVIOR.assess_reads(
        events, {"required": case["required"], "support": {}}, contents
    )
    issues = []
    try:
        result = run_e2e.BEHAVIOR.agent_json(events)
    except (ValueError, json.JSONDecodeError) as exc:
        result = None
        issues.append(f"RESULT_JSON_INVALID:{exc}")
    if result is not None:
        trigger = result.get("trigger_assessment", {})
        replan = result.get("replan", {})
        if trigger.get("operation_mode") != case["mode"]:
            issues.append("OPERATION_MODE_MISMATCH")
        if replan.get("required") is not case["required_replan"]:
            issues.append("REPLAN_REQUIRED_MISMATCH")
        if replan.get("change_type") != case["change_type"]:
            issues.append("CHANGE_TYPE_MISMATCH")
        if replan.get("reopen_trigger") is not None:
            issues.append("REOPEN_TRIGGER_UNEXPECTED")
        actions = {(item.get("action"), item.get("target")) for item in replan.get("actions", []) if isinstance(item, dict)}
        if case_id in {"A", "C"} and actions:
            issues.append("ACTIONS_UNEXPECTED")
        if case_id == "B" and actions != {
            ("PRESERVE", "T-EXPORT"),
            ("OUTDATE", "T-ROUTING-DESIGN"),
            ("OUTDATE", "T-ROUTING-IMPLEMENT"),
            ("OUTDATE", "T-ROUTING-EVAL"),
        }:
            issues.append("LOCAL_SCOPE_MISMATCH")
        if case_id == "D" and actions != {
            ("PRESERVE", "T-PROTOTYPE"), ("ADD", "T-MVP-PROFILE")
        }:
            issues.append("PROFILE_SCOPE_MISMATCH")
        expected_flags = {
            "A": (False, False, False), "B": (True, True, True),
            "C": (True, True, False), "D": (True, True, True),
        }[case_id]
        actual_flags = (
            trigger.get("baseline_exists"), trigger.get("change_event_exists"),
            trigger.get("material_impact_exists"),
        )
        if actual_flags != expected_flags:
            issues.append("TRIGGER_FACTS_MISMATCH")
        if result.get("claims") != {"external_write_performed": False, "invented_evidence": False}:
            issues.append("BOUNDARY_CLAIMS_INVALID")
    status = "PASS" if routing["status"] == "PASS" and not issues else "CONTRACT_FAIL"
    return {"case": case_id, "routing": routing, "issues": issues, "result": result, "status": status}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=sorted(CASES), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--codex", default=shutil.which("codex"))
    args = parser.parse_args()
    if not args.codex:
        parser.error("Codex CLI not found")
    args.output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="ai-skill-replan-") as temporary:
        work = Path(temporary)
        copied = work / "skill"
        shutil.copytree(run_e2e.SKILL, copied)
        hashes = run_e2e.inventory(copied)
        contents = {name: (copied / name).read_text(encoding="utf-8") for name in hashes if name.endswith((".md", ".yaml", ".py"))}
        task_prompt = prompt(CASES[args.case], contents)
        command = [args.codex, "exec", "--json", "--ephemeral", "--ignore-user-config", "-m", "gpt-5.6-luna", "-c", 'model_reasoning_effort="low"', "-s", "read-only", "-c", 'windows.sandbox="elevated"', "--skip-git-repo-check", "-C", str(work), "-"]
        (args.output / "prompt.txt").write_text(task_prompt, encoding="utf-8")
        metadata = {
            "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "skill_sha256": hashes, "exit_code": None, "timeout": False,
            "sandbox": "read-only", "ephemeral": True,
        }
        infra_issues = []
        process = None
        with (args.output / "trace.jsonl").open("w", encoding="utf-8") as stdout, (args.output / "stderr.txt").open("w", encoding="utf-8") as stderr:
            try:
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True, encoding="utf-8")
                try:
                    process.communicate(task_prompt, timeout=args.timeout)
                except subprocess.TimeoutExpired:
                    metadata["timeout"] = True
                    infra_issues.append("MODEL_TIMEOUT")
                    process.kill()
                    process.communicate()
            except OSError as exc:
                infra_issues.append(f"PROCESS_START_FAILED:{type(exc).__name__}:{exc}")
        if process is not None:
            metadata["exit_code"] = process.returncode
            if process.returncode != 0:
                infra_issues.append(f"PROCESS_EXIT_NONZERO:{process.returncode}")
        events = []
        for number, line in enumerate((args.output / "trace.jsonl").read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
                if not isinstance(event, dict):
                    raise ValueError("trace event is not an object")
                events.append(event)
            except (json.JSONDecodeError, ValueError):
                infra_issues.append(f"TRACE_INVALID_JSON_LINE:{number}")
                break
        if not any(event.get("type") == "turn.completed" for event in events):
            infra_issues.append("TRACE_INCOMPLETE")
        if not any(event.get("type") == "item.completed" and isinstance(event.get("item"), dict) and event["item"].get("type") == "agent_message" for event in events):
            infra_issues.append("RESULT_MISSING")
        metadata["skill_unchanged"] = hashes == run_e2e.inventory(copied)
        if not metadata["skill_unchanged"]:
            infra_issues.append("SKILL_COPY_CHANGED")
        outcome = (
            {"case": args.case, "routing": None, "issues": [], "result": None, "status": "INFRA_BLOCKED"}
            if infra_issues else grade(args.case, events, contents)
        )
        outcome["infra_issues"] = infra_issues
        (args.output / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "result.json").write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Replan-{args.case}: {outcome['status']}")
        return 0 if outcome["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
