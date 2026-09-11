"""Run one isolated, read-only Phase 2 behavioral regression."""

from pathlib import Path
import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
TEST_ROOT = HERE.parents[1]
REPO = HERE.parents[3]
SKILL = REPO / "skills/ai-product-development"
sys.path.insert(0, str(TEST_ROOT / "routing"))
sys.path.insert(0, str(SKILL / "scripts"))

from run_routing import inventory
from runtime_validation.validators import validate_document

SCENARIOS = json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))
FIXTURES = TEST_ROOT / "phase2/fixtures"


def agent_json(events):
    messages = [
        event.get("item", {}).get("text", "")
        for event in events
        if event.get("type") == "item.completed"
        and event.get("item", {}).get("type") == "agent_message"
    ]
    if not messages:
        raise ValueError("no agent message")
    text = messages[-1].strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("agent message contains no JSON object")
    return json.loads(text[start : end + 1])


def assess_reads(events, scenario, contents):
    reads, issues, allowed_commands = [], [], []
    chunks = {}
    sequence = 0
    full_pattern = re.compile(
        r"Get-Content\s+-LiteralPath\s+'([^']+)'(?:\s+-Encoding\s+UTF8)?$", re.I
    )
    chunk_pattern = re.compile(
        r"Get-Content\s+-LiteralPath\s+'([^']+)'(?:\s+-Encoding\s+UTF8)?"
        r"\s*\|\s*Select-Object\s+(?:-First\s+(\d+)|-Skip\s+(\d+))$",
        re.I,
    )

    def normalize(value):
        return value.replace("\r\n", "\n").strip()

    def relative_name(path):
        name = re.sub(r"[\\/]+", "/", path)
        if "/skill/" in name:
            return name.split("/skill/", 1)[1]
        return name[6:] if name.startswith("skill/") else name

    for event in events:
        item = event.get("item", {})
        if event.get("type") != "item.completed" or item.get("type") != "command_execution":
            continue
        sequence += 1
        command = item.get("command", "")
        validator_call = "validate_runtime.py" in command or "validate_document" in command
        exit_code = item.get("exit_code")
        completed = item.get("status") in {"completed", "failed"}
        if validator_call and completed and exit_code in {0, 1, 2}:
            allowed_commands.append({"item_id": item.get("id"),
                                     "reason": "read-only runtime validation",
                                     "exit_code": exit_code})
            continue
        if item.get("status") != "completed" or exit_code != 0:
            issues.append("FAILED_COMMAND: " + item.get("id", "?"))
            continue
        read_command = command.split(" -Command ", 1)[-1].strip().strip(chr(34))
        full = full_pattern.fullmatch(read_command)
        chunk = chunk_pattern.fullmatch(read_command)
        selected_path = full.group(1) if full else (chunk.group(1) if chunk else "")
        name = relative_name(selected_path) if selected_path else ""
        output = normalize(item.get("aggregated_output", ""))
        if full and name in contents and output == normalize(contents[name]):
            reads.append({"file": name, "item_id": item.get("id"), "command": command,
                          "_sequence": sequence})
            continue
        if chunk and name in contents:
            lines = contents[name].splitlines()
            start_line = 0 if chunk.group(2) else int(chunk.group(3))
            end_line = min(len(lines), int(chunk.group(2))) if chunk.group(2) else len(lines)
            if start_line <= end_line and output == normalize("\n".join(lines[start_line:end_line])):
                chunks.setdefault(name, []).append({"start": start_line, "end": end_line,
                                                     "sequence": sequence,
                                                     "item_id": item.get("id"),
                                                     "command": command})
                continue
        issues.append("UNVERIFIED_READ: " + item.get("id", "?") if selected_path
                      else "UNCLASSIFIED_COMMAND: " + item.get("id", "?"))

    for name, parts in chunks.items():
        ordered = sorted(parts, key=lambda part: part["start"])
        cursor = 0
        for part in ordered:
            if part["start"] != cursor:
                break
            cursor = part["end"]
        if cursor == len(contents[name].splitlines()):
            reads.append({"file": name,
                          "item_id": "+".join(part["item_id"] for part in ordered),
                          "command": " + ".join(part["command"] for part in ordered),
                          "_sequence": min(part["sequence"] for part in ordered)})
    reads.sort(key=lambda read: read["_sequence"])
    for read in reads:
        read.pop("_sequence")
    loaded = [item["file"] for item in reads]
    loaded_set = set(loaded)
    missing = sorted(set(scenario["required"]) - loaded_set)
    extras = sorted(loaded_set - set(scenario["required"]))
    unexplained = sorted(set(extras) - set(scenario["support"]))
    eager = []
    justified = set(scenario["required"]) | set(scenario["support"])
    for group in ("lifecycle", "runtime"):
        universe = {name for name in contents if name.startswith(f"references/{group}/")}
        observed = {name for name in loaded_set if name.startswith(f"references/{group}/")}
        if len(observed) >= len(universe) - 1 and observed - justified:
            eager.append(group)
    if loaded and loaded[0] != "SKILL.md":
        issues.append("KERNEL_NOT_FIRST")
    status = "FAIL" if missing or eager or unexplained or issues or not loaded else "PASS"
    return {"required": scenario["required"], "reads_in_order": reads, "missing": missing,
            "extra_reads": {name: scenario["support"].get(name) for name in extras},
            "unexplained": unexplained, "eager_loading_groups": eager,
            "allowed_tool_calls": allowed_commands, "trace_issues": issues, "status": status}

def grade(events, scenario, contents):
    routing = assess_reads(events, scenario, contents)

    issues = []
    validation_errors = []
    envelope = None
    try:
        envelope = agent_json(events)
    except (ValueError, json.JSONDecodeError) as exc:
        issues.append("RESULT_JSON_INVALID: " + str(exc))

    if envelope is not None:
        if set(envelope) != {"document", "claims"}:
            issues.append("RESULT_ENVELOPE_INVALID")
        else:
            validation_errors = [
                error.as_dict()
                for error in validate_document(envelope["document"], "combined")
            ]
            expected = json.loads(
                (FIXTURES / "expected" / (scenario["case"] + ".json")).read_text(
                    encoding="utf-8"
                )
            )
            profile = envelope["document"].get("profile", {})
            levels = {
                node.get("node"): node.get("level")
                for node in profile.get("nodes", [])
                if isinstance(node, dict)
            }
            if profile.get("delivery_target") != expected["delivery_target"]:
                issues.append("DELIVERY_TARGET_MISMATCH")
            if profile.get("assignment_scope", {}).get("mode") != expected["scope_mode"]:
                issues.append("SCOPE_MODE_MISMATCH")
            allowed_project_modes = expected.get(
                "behavior_project_modes", [expected.get("project_mode")]
            )
            if profile.get("project_mode") not in allowed_project_modes:
                issues.append("PROJECT_MODE_MISMATCH")
            actual_context = profile.get("validation_context", {})
            for key, value in expected.get("validation_context", {}).items():
                if actual_context.get(key) != value:
                    issues.append("VALIDATION_CONTEXT_MISMATCH:" + key)
            behavior_levels = expected.get("behavior_node_levels")
            if behavior_levels is None:
                levels_match = levels == expected["node_levels"]
            else:
                levels_match = set(levels) == set(behavior_levels) and all(
                    levels[node] in allowed
                    for node, allowed in behavior_levels.items()
                )
            if not levels_match:
                issues.append("NODE_LEVELS_MISMATCH")
            if envelope["claims"] != {
                "assignment_complete": False,
                "external_write_performed": False,
            }:
                issues.append("BOUNDARY_CLAIMS_INVALID")
            if not envelope["document"].get("plan", {}).get("plan", {}).get("tasks"):
                issues.append("PLAN_EMPTY")

    status = (
        "PASS"
        if routing["status"] == "PASS" and not issues and not validation_errors
        else "FAIL"
    )
    return {
        "scenario": scenario["id"],
        "routing": routing,
        "validation_errors": validation_errors,
        "behavior_issues": issues,
        "normalized_result": envelope,
        "status": status,
    }


def prompt_for(scenario):
    case_text = (
        TEST_ROOT / "cases" / (scenario["case"] + ".md")
    ).read_text(encoding="utf-8")
    return f"""Use the AI product development skill copied to skill/SKILL.md. Read SKILL.md first, then select supporting files from its router. This is an isolated read-only planning exercise: do not write files, execute product work, install tools, use external services, or request broader permissions. Read SKILL.md first in two deterministic line chunks using separate Get-Content -LiteralPath commands with UTF-8, piped to Select-Object -First 120 and Select-Object -Skip 120. Read every other selected file in full with a separate Get-Content -LiteralPath command using UTF-8. Do not list or bulk-read directories. Do not read outside this temporary workspace.

Derive the Execution Profile and a concise valid Plan of at most three tasks only; keep strings short and do not perform lifecycle work. Return exactly one JSON object and no prose:
{{"document":{{"profile":{{"delivery_target":"...","project_mode":"...","assignment_scope":{{all canonical fields}},"nodes":[eight canonical NodeProfile objects in order],"validation_context":{{"existing_repository_modification":false,"verified_design":false,"acceptance_criteria_defined":false,"production_release":false,"release_execution":false,"monitoring_covered":false,"release_readiness":"PASS|PASS_WITH_ASSUMPTIONS|BLOCKED"}}}},"plan":{{"plan":{{all canonical Plan fields; tasks use every canonical Task field; dependency records use from/to/type}},"available_inputs":[],"artifacts":[],"gates":{{}},"blocked_inputs":[],"write_targets":{{"task-id":["artifact-id:version"]}}}}}},"claims":{{"assignment_complete":false,"external_write_performed":false}}}}

Use empty artifact_requirements unless you include the corresponding full canonical Artifact in artifacts. A task may remain NOT_STARTED or BLOCKED when inputs or gates are unresolved. Every task needs a non-empty goal, output, and acceptance criteria. Task.dependencies must equal the incoming dependency source ids in Plan.dependencies. Use a GATE source name only with type GATE. The planning-only assignment is not complete.

The test executes only planning, but that does not narrow the user's AssignmentScope. Derive FULL_PROJECT or PARTIAL_PROJECT only from the scenario's stated ownership boundary. Validation context describes the product assignment, not the test action: set production_release true when production release is in scope, but keep release_execution false while Release Readiness is blocked.

Values explicitly marked as fixed test input in the scenario are authoritative.

Scenario:
{case_text}"""


def run(scenario, output, codex, timeout, model, thinking):
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="ai-skill-phase2-") as temp:
        work = Path(temp)
        copy = work / "skill"
        shutil.copytree(SKILL, copy)
        before = inventory(copy)
        contents = {
            name: (copy / name).read_text(encoding="utf-8")
            for name in before
            if name.endswith((".md", ".yaml", ".py"))
        }
        prompt = prompt_for(scenario)
        command = [
            codex,
            "exec",
            "--json",
            "--ephemeral",
            "--ignore-user-config",
            "-m",
            model,
            "-c",
            f'model_reasoning_effort="{thinking}"',
            "-s",
            "read-only",
            "-c",
            'windows.sandbox="elevated"',
            "--skip-git-repo-check",
            "-C",
            str(work),
            "-",
        ]
        (output / "prompt.txt").write_text(prompt, encoding="utf-8")
        metadata = {
            "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "command": command,
            "skill_sha256": before,
            "codex_version": subprocess.check_output([codex, "--version"], text=True).strip(),
            "sandbox": "read-only",
            "ephemeral": True,
        }
        with (output / "trace.jsonl").open("w", encoding="utf-8") as stdout, (
            output / "stderr.txt"
        ).open("w", encoding="utf-8") as stderr:
            process = subprocess.Popen(
                command,
                stdin=subprocess.PIPE,
                stdout=stdout,
                stderr=stderr,
                text=True,
                encoding="utf-8",
            )
            try:
                process.communicate(prompt, timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                metadata["timeout"] = True
        metadata["exit_code"] = process.returncode
        metadata["skill_unchanged"] = before == inventory(copy)
        events = [
            json.loads(line)
            for line in (output / "trace.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        result = grade(events, scenario, contents)
        if process.returncode or not metadata["skill_unchanged"] or metadata.get("timeout"):
            result["status"] = "FAIL"
        (output / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (output / "result.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f'{scenario["id"]}: {result["status"]}', flush=True)
        return result["status"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario", choices=[item["id"] for item in SCENARIOS], required=True
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex", default=shutil.which("codex"))
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument("--thinking", default="low")
    args = parser.parse_args()
    if not args.codex:
        parser.error("Codex CLI not found")
    selected = next(item for item in SCENARIOS if item["id"] == args.scenario)
    raise SystemExit(
        0 if run(selected, args.output, args.codex, args.timeout, args.model, args.thinking) == "PASS" else 1
    )
