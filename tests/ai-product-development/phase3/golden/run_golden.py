"""Run four fresh Codex sessions against one persistent Golden MVP workspace."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = Path(__file__).resolve().parent
TEST_ROOT = HERE.parents[1]
REPO = HERE.parents[3]
SKILL = REPO / "skills/ai-product-development"
GOLDEN = REPO / "examples/ai-product-development/golden-feedback-organizer"
sys.path.insert(0, str(SKILL / "scripts"))

from project_runtime import ProjectRuntime
from runtime_validation.validators import validate_document


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root: Path) -> dict[str, str]:
    return {path.relative_to(root).as_posix(): sha(path) for path in sorted(root.rglob("*")) if path.is_file()}


def task(task_id, name, goal, node, status, dependencies, artifacts, output):
    return {
        "id": task_id, "name": name, "goal": goal, "type": "WORK", "status": status,
        "priority": "P1", "lifecycle_node": node, "execution_depth": "FULL",
        "dependencies": dependencies, "required_inputs": ["scope"],
        "required_capabilities": ["SKILL"], "expected_output": output,
        "acceptance_criteria": [f"{output} is validated"], "context_requirements": [],
        "artifact_requirements": artifacts, "retry_policy": "LOCAL_ONCE",
    }


def prepare(work: Path) -> tuple[Path, dict[str, str]]:
    shutil.copytree(SKILL, work / "skill")
    product = work / "product"
    shutil.copytree(GOLDEN, product)
    base = yaml.safe_load((TEST_ROOT / "phase2/fixtures/scenarios/01-greenfield-prototype.yaml").read_text(encoding="utf-8"))
    profile = deepcopy(base["profile"])
    profile["delivery_target"] = "DEMO"
    for node in profile["nodes"]:
        if node["node"] in {"Qualification", "Cognition", "Product Definition & Scope", "Solution Design"}:
            node["status"] = "SATISFIED"
            node["gaps"] = []
        elif node["node"] == "Implementation":
            node["status"] = "ACTIVE"
        elif node["level"] != "SKIP":
            node["status"] = "NOT_STARTED"
    tasks = [
        task("T1", "Define feedback MVP", "Confirm the Golden MVP scope", "Product Definition & Scope", "COMPLETED", [], ["design-v1"], "accepted MVP definition"),
        task("T2", "Run feedback organizer", "Produce evidence-linked feedback insights", "Implementation", "READY", ["T1"], ["design-v1"], "feedback report"),
        task("T3", "Validate feedback report", "Validate the unfiltered Golden output", "Validation & Iteration", "NOT_STARTED", ["T2"], ["report-v1"], "validated feedback report"),
    ]
    plan = {
        "plan": {"version": "v1", "objective": "Deliver the Feedback Organizer Runnable Demo", "tasks": tasks,
                 "dependencies": [{"from": "T1", "to": "T2", "type": "HARD"}, {"from": "T2", "to": "T3", "type": "HARD"}],
                 "critical_path": ["T1", "T2", "T3"], "assumptions": []},
        "available_inputs": ["scope", "sample-feedback"],
        "artifacts": [{"id": "design-v1", "type": "DESIGN", "name": "Golden MVP design", "version": "v1", "status": "ACTIVE", "summary": "Runnable behavior and boundaries", "location": "README.md", "source_tasks": ["T1"], "source_records": [], "dependencies": []}],
        "gates": {"Build Readiness": "PASS"}, "blocked_inputs": [],
        "write_targets": {"T1": ["design-v1"], "T2": ["report-v1"], "T3": ["validation-v1"]},
    }
    initial = {"profile": profile, "plan": plan}
    errors = validate_document(initial, "combined")
    assert not errors, errors
    (product / "initial.yaml").write_text(yaml.safe_dump(initial, allow_unicode=True, sort_keys=False), encoding="utf-8")
    artifact = {"id": "report-v1", "type": "REPORT", "name": "Feedback insights", "version": "v1", "status": "ACTIVE", "summary": "Full feedback report", "location": "report.md", "source_tasks": ["T2"], "source_records": [], "dependencies": ["design-v1"]}
    (product / "artifact.yaml").write_text(yaml.safe_dump(artifact, sort_keys=False), encoding="utf-8")
    record = {"id": "R1", "type": "DECISION", "topic": "delivery", "content": "Local deterministic Runnable Demo", "status": "ACTIVE", "source": "user", "version": "v1", "affected_scope": ["Implementation", "Validation & Iteration"]}
    (product / "record.yaml").write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")

    changed = deepcopy(plan)
    changed.pop("artifacts")
    changed["plan"]["version"] = "v2"
    changed["plan"]["tasks"][1]["status"] = "COMPLETED"
    changed["plan"]["tasks"][2]["status"] = "CANCELLED"
    changed["plan"]["tasks"][2]["dependencies"] = []
    changed["plan"]["tasks"].extend([
        task("T4", "Add source filter", "Produce a support-only feedback report", "Implementation", "READY", ["T2"], ["report-v1"], "filtered feedback report"),
        task("T5", "Validate changed MVP", "Validate source filtering and final outputs", "Validation & Iteration", "NOT_STARTED", ["T4"], ["filtered-v1"], "validated changed MVP"),
    ])
    changed["plan"]["dependencies"] = [
        {"from": "T1", "to": "T2", "type": "HARD"},
        {"from": "T2", "to": "T4", "type": "HARD"},
        {"from": "T4", "to": "T5", "type": "HARD"},
    ]
    changed["plan"]["critical_path"] = ["T1", "T2", "T4", "T5"]
    changed["write_targets"].update({"T4": ["filtered-v1"], "T5": ["validation-v2"]})
    change = {"change_type": "INPUT_CHANGE", "actions": [{"action": "CANCEL", "target": "T3"}, {"action": "ADD", "target": "T4"}, {"action": "ADD", "target": "T5"}], "plan": changed}
    change_validation = {**deepcopy(changed), "artifacts": [*plan["artifacts"], artifact]}
    change_errors = validate_document(change_validation, "plan")
    assert not change_errors, change_errors
    (product / "change.yaml").write_text(yaml.safe_dump(change, allow_unicode=True, sort_keys=False), encoding="utf-8")
    filtered = {"id": "filtered-v1", "type": "REPORT", "name": "Filtered feedback insights", "version": "v1", "status": "ACTIVE", "summary": "Support-only feedback report", "location": "filtered-report.md", "source_tasks": ["T4"], "source_records": ["R1"], "dependencies": ["report-v1"]}
    (product / "filtered-artifact.yaml").write_text(yaml.safe_dump(filtered, sort_keys=False), encoding="utf-8")
    final_profile = deepcopy(profile)
    for node in final_profile["nodes"]:
        if node["level"] == "REQUIRED" or node["node"] == "Validation & Iteration":
            node["status"] = "SATISFIED"
            node["gaps"] = []
    (product / "final-profile.yaml").write_text(yaml.safe_dump(final_profile, allow_unicode=True, sort_keys=False), encoding="utf-8")
    verifier = '''import json\nfrom pathlib import Path\nroot=Path(__file__).parent\nfull=json.loads((root/"output.json").read_text(encoding="utf-8"))\nassert full["summary"]=={"received":5,"unique":4,"duplicates":1}\nassert all(theme["evidence"] for theme in full["themes"])\nfiltered_path=root/"filtered-output.json"\nif filtered_path.exists():\n    filtered=json.loads(filtered_path.read_text(encoding="utf-8"))\n    assert filtered["summary"]["received"]==2\n    assert all(item["source"]=="support" for item in filtered["items"])\n    assert all(theme["evidence"] for theme in filtered["themes"])\nprint("PASS: available Golden outputs are complete and evidence-linked")\n'''
    (product / "verify_outputs.py").write_text(verifier, encoding="utf-8")
    return product, inventory(work / "skill")


PHASES = [
    {
        "id": "G1-init",
        "required_reads": ["SKILL.md", "scripts/project_runtime/README.md"],
        "required_commands": ["project_runtime.py", " init ", " next", " checkpoint"],
        "prompt": "Initialize the supplied product with initial.yaml and project id golden-feedback-organizer. Then select the next task and create a checkpoint.",
    },
    {
        "id": "G2-resume-build",
        "required_reads": ["SKILL.md", "scripts/project_runtime/README.md", "references/runtime/replan-recovery.md", "references/runtime/context.md", "references/runtime/executor.md", "references/runtime/registry-versioning.md", "references/lifecycle/05-implementation.md"],
        "required_commands": [" resume", "feedback_organizer.py", " task ", "commit-artifact", "register-record", " checkpoint"],
        "prompt": "Your first state command must be `python -B -X utf8 skill/scripts/project_runtime.py --root product resume`; do not substitute status or next. Then run feedback_organizer.py on sample-feedback.csv to create product/output.json and product/report.md. Mark T2 COMPLETED with validation PASS, register record.yaml, commit artifact.yaml with validation PASS, set T3 READY, then checkpoint.",
    },
    {
        "id": "G3-local-replan",
        "required_reads": ["SKILL.md", "scripts/project_runtime/README.md", "references/runtime/replan-recovery.md", "references/runtime/planner.md", "references/runtime/context.md", "references/runtime/executor.md", "references/runtime/registry-versioning.md", "references/lifecycle/05-implementation.md"],
        "required_commands": [" resume", " replan ", " next", "--source", " task ", "commit-artifact", " checkpoint"],
        "prompt": "Your first state command must be `python -B -X utf8 skill/scripts/project_runtime.py --root product resume`; do not substitute status or next. Then apply change.yaml as a local replan and select the next task. Run the organizer with --source support to create product/filtered-output.json and product/filtered-report.md. Mark T4 COMPLETED with validation PASS, commit filtered-artifact.yaml with validation PASS, set T5 READY, then checkpoint.",
    },
    {
        "id": "G4-resume-complete",
        "required_reads": ["SKILL.md", "scripts/project_runtime/README.md", "references/runtime/replan-recovery.md", "references/runtime/context.md", "references/runtime/executor.md", "references/runtime/execution-profile.md", "references/lifecycle/06-validation-iteration.md"],
        "required_commands": [" resume", "verify_outputs.py", " task ", "update-profile", " checkpoint", " complete"],
        "prompt": "Your first state command must be `python -B -X utf8 skill/scripts/project_runtime.py --root product resume`; do not substitute status or next. Then run product/verify_outputs.py. Mark T5 COMPLETED with validation PASS, update the Profile from final-profile.yaml, checkpoint, then run the completion check.",
    },
]


def run_phase(work: Path, output: Path, phase: dict, codex: str, timeout: int, skill_hashes: dict[str, str], model: str, thinking: str, folder_name: str | None = None) -> dict:
    folder = output / (folder_name or phase["id"])
    folder.mkdir()
    required = ", ".join(f"skill/{name}" for name in phase["required_reads"])
    prompt = f'''Use the AI product development skill copied to skill/SKILL.md for an existing persistent product workspace at product/. Read SKILL.md first, then use its router. The dependency closure already determined for this focused phase is: {required}. Read every file in that list and do not load unrelated lifecycle/runtime modules. Read every selected file in full with a separate Get-Content -LiteralPath command using UTF-8. Do not list or bulk-read directories. Do not modify skill/. Do not use external services or install tools. Execute the requested local commands; all writes must stay under product/. Use `python -B -X utf8 skill/scripts/project_runtime.py --root product ...` for state operations. Stop on any failed command. End with a short factual result.\n\nTask: {phase["prompt"]}'''
    command = [codex, "exec", "--json", "--ephemeral", "--ignore-user-config", "-m", model, "-c", f'model_reasoning_effort="{thinking}"', "-s", "workspace-write", "-c", 'windows.sandbox="elevated"', "--skip-git-repo-check", "-C", str(work), "-"]
    (folder / "prompt.txt").write_text(prompt, encoding="utf-8")
    metadata = {"started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "command": command, "skill_sha256": skill_hashes, "codex_version": subprocess.check_output([codex, "--version"], text=True).strip(), "sandbox": "workspace-write", "ephemeral": True}
    with (folder / "trace.jsonl").open("w", encoding="utf-8") as stdout, (folder / "stderr.txt").open("w", encoding="utf-8") as stderr:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True, encoding="utf-8")
        try:
            process.communicate(prompt, timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill(); process.communicate(); metadata["timeout"] = True
    metadata["exit_code"] = process.returncode
    metadata["skill_unchanged"] = inventory(work / "skill") == skill_hashes
    (folder / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    events = [json.loads(line) for line in (folder / "trace.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    commands = [event.get("item", {}) for event in events if event.get("type") == "item.completed" and event.get("item", {}).get("type") == "command_execution"]
    successful = [item.get("command", "") for item in commands if item.get("status") == "completed" and item.get("exit_code") == 0]
    joined = "\n".join(successful)
    missing_commands = [marker for marker in phase["required_commands"] if marker not in joined]
    read_files = []
    for item in commands:
        command_text = item.get("command", "").replace("\\", "/")
        if item.get("status") != "completed" or item.get("exit_code") != 0:
            continue
        for name in phase["required_reads"]:
            if f"skill/{name}" in command_text and item.get("aggregated_output", "").strip():
                read_files.append(name)
    missing_reads = sorted(set(phase["required_reads"]) - set(read_files))
    threads = [event["thread_id"] for event in events if event.get("type") == "thread.started"]
    result = {"phase": phase["id"], "required_reads": phase["required_reads"], "verified_reads": read_files, "missing_reads": missing_reads, "required_command_markers": phase["required_commands"], "missing_command_markers": missing_commands, "thread_ids": threads, "status": "PASS" if not missing_reads and not missing_commands and len(threads) == 1 and process.returncode == 0 and metadata["skill_unchanged"] and not metadata.get("timeout") else "FAIL"}
    (folder / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f'{phase["id"]}: {result["status"]}', flush=True)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex", default=shutil.which("codex"))
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument("--thinking", default="low", choices=("low", "medium", "high"))
    parser.add_argument("--retries", type=int, default=2, help="retry a failed phase from its pre-phase product state")
    args = parser.parse_args(argv)
    if not args.codex:
        parser.error("Codex CLI not found")
    args.output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="ai-skill-phase3-") as temporary:
        work = Path(temporary)
        product, skill_hashes = prepare(work)
        results = []
        failures = []
        for phase in PHASES:
            backup = work / "product-before-phase"
            shutil.copytree(product, backup)
            result = None
            for attempt in range(1, args.retries + 2):
                folder_name = f'{phase["id"]}-attempt-{attempt}'
                result = run_phase(work, args.output, phase, args.codex, args.timeout, skill_hashes, args.model, args.thinking, folder_name)
                if result["status"] == "PASS":
                    (args.output / folder_name).replace(args.output / phase["id"])
                    break
                failures.append({"phase": phase["id"], "attempt": attempt, "result": result})
                shutil.rmtree(args.output / folder_name)
                shutil.rmtree(product)
                shutil.copytree(backup, product)
            shutil.rmtree(backup)
            results.append(result)
            if result["status"] != "PASS":
                break
        if len(results) == len(PHASES) and all(item["status"] == "PASS" for item in results):
            runtime = ProjectRuntime(product)
            final = runtime.complete()
            if not final["complete"]:
                results[-1]["status"] = "FAIL"
                results[-1]["completion"] = final
            shutil.copytree(product, args.output / "final-product")
        (args.output / "summary.json").write_text(json.dumps({"phases": results, "failed_attempts": failures}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if len(results) == len(PHASES) and all(item["status"] == "PASS" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
