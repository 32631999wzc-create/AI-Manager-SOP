"""Run one minimal, read-only adjacent Capability routing case."""

from __future__ import annotations

import argparse
import datetime
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from run_targeted_repair import run_e2e


CASES = {
    "prd": ("product-requirements", "EXECUTE", "An approved opportunity and release slice exist for an AI support-ticket summary feature. User interviews and scope are supplied, but no PRD or acceptance contract exists. Drafting the product requirements is the pending decision; there is no cross-functional disagreement or review request."),
    "review": ("requirement-review", "EXECUTE", "An approved PRD v2 exists. Product and safety owners disagree materially about whether reply suggestions may be sent automatically; the designated decision owner must resolve the trade-off before Build Readiness. Do not redraft the PRD as the primary work."),
    "evaluation": ("evaluation", "EXECUTE", "The product claim and release threshold are approved. The pending decision is whether an AI answer is factually grounded on a fixed representative offline case set; no eval plan, grader, or run evidence exists. No user adoption question or live pilot is requested."),
    "experimentation": ("experimentation", "EXECUTE", "Offline quality evaluation has already passed. The pending decision is whether support agents actually use the feature and save time without increasing workload in a controlled six-week pilot; no pilot design exists. Do not repeat offline model evaluation."),
    "roadmap": ("roadmap", "EXECUTE", "The product outcome and priorities are approved. The pending decision is how to slice three future releases around learning milestones, dependencies, and commitment levels; no cross-version roadmap exists. This is not a single implementation task list."),
    "planner": (None, None, "A validated product plan already contains one scoped READY implementation task with owner, inputs, acceptance criteria, and dependencies. The assignment is only to select and schedule that task in the runtime DAG. No cross-version direction, product-domain uncertainty, or new Capability deliverable is needed."),
    "production": ("production-learning", "EXECUTE", "The AI feature is live. A new seven-day production bad-case signal may invalidate an active quality decision; the owner must triage the signal, relate it to version and guardrail, and decide containment and reopening. The incident is ongoing, not a completed-stage retrospective."),
    "retrospective": ("retrospective", "EXECUTE", "A pilot has ended and final quality, adoption, cost, and incident evidence is available. The pending decision is what was learned against the original goals and which assets or debts to carry forward. No live monitoring or ongoing incident triage is requested."),
    "no-gap": (None, None, "The current assignment is only to report the status of an already approved plan. All decisions and evidence are current; there is no unresolved lifecycle gap, new evidence, or task to execute."),
}
REQUIRED = ["SKILL.md", "references/runtime/planner.md"]
ALIASES = {
    "产品需求定义": "product-requirements", "product-requirements": "product-requirements", "product requirements": "product-requirements",
    "需求评审与决策": "requirement-review", "requirement-review-decisions": "requirement-review", "requirement-review-and-decision": "requirement-review", "requirement-review": "requirement-review",
    "评测与质量": "evaluation", "evaluation-quality": "evaluation", "evaluation": "evaluation",
    "实验与试点": "experimentation", "experimentation-pilot": "experimentation", "experimentation": "experimentation",
    "路线图与版本规划": "roadmap", "roadmap-release-planning": "roadmap", "roadmap": "roadmap",
    "生产观测与学习闭环": "production-learning", "production-observability-learning": "production-learning", "production-learning": "production-learning",
    "复盘与组合学习": "retrospective", "retrospective-portfolio-learning": "retrospective", "retrospective": "retrospective",
}


def prompt_for(case: str, contents: dict[str, str]) -> str:
    commands = [f"Get-Content -Raw -LiteralPath 'skill/{name}'" for name in REQUIRED]
    command_lines = "\n".join(f"- {command}" for command in commands)
    return f"""Use the copied AI product development Skill for one Capability Need routing decision only. Read the two files in separate tool calls for each command below; do not read other references, execute a Capability, write files, or do product work:
{command_lines}

Assignment facts: {CASES[case][2]}

Return exactly one JSON object, no prose:
{{"gap_exists":true,"decision_to_unlock":"specific decision or null","capability_need":{{"capability":"primary professional domain slug or label","mode":"EXECUTE|VERIFY|REUSE","reason":"specific gap and evidence state","decision_to_unlock":"same specific decision"}}}}

Use capability_need=null when no professional domain is needed. Runtime Planner is not a Professional Capability. Select at most one primary domain; do not activate a domain merely because it is usually relevant."""


def grade(case: str, events: list[dict], contents: dict[str, str]) -> dict:
    routing = run_e2e.BEHAVIOR.assess_reads(events, {"required": REQUIRED, "support": {}}, contents)
    commands = [event["item"] for event in events if event.get("type") == "item.completed" and isinstance(event.get("item"), dict) and event["item"].get("type") == "command_execution"]
    successful = [item for item in commands if item.get("status") == "completed" and item.get("exit_code") == 0]
    if routing["status"] != "PASS":
        missing = [name for name in REQUIRED if not any(name in item.get("command", "") and contents[name].replace("\r\n", "\n").strip() in item.get("aggregated_output", "").replace("\r\n", "\n") for item in successful)]
        if not missing and len(successful) == len(commands):
            routing = {"required": REQUIRED, "missing": [], "successful_commands": len(successful), "verification": "full content in successful combined command output", "status": "PASS"}
    result = run_e2e.BEHAVIOR.agent_json(events)
    expected, mode, _ = CASES[case]
    issues = []
    should_have_gap = case not in ("no-gap", "planner")
    if result.get("gap_exists") is not should_have_gap:
        issues.append("GAP_MISMATCH")
    need = result.get("capability_need")
    if expected is None:
        if need is not None:
            issues.append("UNNEEDED_CAPABILITY")
        if case == "no-gap" and result.get("decision_to_unlock") is not None:
            issues.append("UNNEEDED_DECISION")
    elif not isinstance(need, dict):
        issues.append("CAPABILITY_MISSING")
    else:
        chosen = ALIASES.get(str(need.get("capability", "")).strip().lower(), str(need.get("capability", "")).strip())
        if chosen != expected:
            issues.append("CAPABILITY_MISMATCH")
        if need.get("mode") != mode:
            issues.append("MODE_MISMATCH")
        if not str(need.get("reason", "")).strip():
            issues.append("REASON_MISSING")
        if not str(need.get("decision_to_unlock", "")).strip() or need.get("decision_to_unlock") != result.get("decision_to_unlock"):
            issues.append("DECISION_MISMATCH")
    return {"case": case, "status": "PASS" if routing["status"] == "PASS" and not issues else "CONTRACT_FAIL", "issues": issues, "routing": routing, "result": result}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=sorted(CASES), required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--regrade-existing", type=Path)
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--codex", default=shutil.which("codex"))
    args = parser.parse_args()
    if not args.codex:
        parser.error("Codex CLI not found")
    if args.regrade_existing:
        previous = args.regrade_existing
        metadata = json.loads((previous / "metadata.json").read_text(encoding="utf-8"))
        if metadata["skill_sha256"] != run_e2e.inventory(run_e2e.SKILL):
            parser.error("Current Skill differs from captured trace; cannot regrade")
        events = [json.loads(line) for line in (previous / "trace.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        contents = {name: (run_e2e.SKILL / name).read_text(encoding="utf-8") for name in REQUIRED}
        outcome = grade(args.case, events, contents)
        outcome["regraded_from"] = "result.json"
        (previous / "regraded-result.json").write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Adjacent-{args.case} regraded: {outcome['status']}", flush=True)
        return 0 if outcome["status"] == "PASS" else 1
    if args.output is None:
        parser.error("--output is required unless --regrade-existing is used")
    args.output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="ai-pm-adjacent-") as temporary:
        work = Path(temporary)
        copied = work / "skill"
        shutil.copytree(run_e2e.SKILL, copied)
        before = run_e2e.inventory(copied)
        contents = {name: (copied / name).read_text(encoding="utf-8") for name in REQUIRED}
        prompt = prompt_for(args.case, contents)
        (args.output / "prompt.txt").write_text(prompt, encoding="utf-8")
        command = [args.codex, "exec", "--json", "--ephemeral", "--ignore-user-config", "-m", "gpt-5.6-luna", "-c", 'model_reasoning_effort="low"', "-s", "read-only", "-c", 'windows.sandbox="elevated"', "--skip-git-repo-check", "-C", str(work), "-"]
        infra = []
        exit_code = None
        with (args.output / "trace.jsonl").open("w", encoding="utf-8") as stdout, (args.output / "stderr.txt").open("w", encoding="utf-8") as stderr:
            try:
                completed = subprocess.run(command, input=prompt, stdout=stdout, stderr=stderr, text=True, encoding="utf-8", timeout=args.timeout)
                exit_code = completed.returncode
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
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    infra.append(f"TRACE_INVALID_JSON_LINE:{number}")
                    break
        if not any(event.get("type") == "turn.completed" for event in events):
            infra.append("TRACE_INCOMPLETE")
        if before != run_e2e.inventory(copied):
            infra.append("SKILL_COPY_CHANGED")
        if infra:
            outcome = {"case": args.case, "status": "INFRA_BLOCKED", "issues": [], "routing": None, "result": None}
        else:
            try:
                outcome = grade(args.case, events, contents)
            except (ValueError, json.JSONDecodeError) as exc:
                outcome = {"case": args.case, "status": "CONTRACT_FAIL", "issues": [f"RESULT_JSON_INVALID:{exc}"], "routing": None, "result": None}
        outcome["infra_issues"] = infra
        metadata = {"case": args.case, "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "skill_sha256": before, "exit_code": exit_code, "sandbox": "read-only", "ephemeral": True}
        (args.output / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "result.json").write_text(json.dumps(outcome, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Adjacent-{args.case}: {outcome['status']}", flush=True)
        return 0 if outcome["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
