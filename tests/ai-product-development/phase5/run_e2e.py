"""Run one isolated, read-only Phase 5 end-to-end scenario."""

from __future__ import annotations

from pathlib import Path
import argparse
import datetime
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
TEST_ROOT = HERE.parent
REPO = HERE.parents[2]
SKILL = REPO / "skills" / "ai-product-development"
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(TEST_ROOT / "routing"))

from run_routing import inventory
from runtime_validation.validators import validate_document, validate_object


def _load_behavior_helpers():
    source = TEST_ROOT / "phase2" / "behavior" / "run_behavior.py"
    spec = importlib.util.spec_from_file_location("phase2_behavior_helpers", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Phase 2 behavior helpers")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BEHAVIOR = _load_behavior_helpers()
SCENARIOS = json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))

CAPABILITY_ALIASES = {
    "用户与机会发现": "discovery",
    "User & Opportunity Discovery": "discovery",
    "产品需求定义": "product-requirements",
    "Product Requirements": "product-requirements",
    "数据策略与治理": "data-strategy",
    "Data Strategy & Governance": "data-strategy",
    "Human-AI 体验": "human-ai-experience",
    "Human-AI Experience": "human-ai-experience",
    "AI 可行性与原型": "ai-feasibility",
    "AI Feasibility & Prototyping": "ai-feasibility",
    "评测与质量": "evaluation",
    "Evaluation & Quality": "evaluation",
    "责任 AI、安全与风险": "responsible-ai",
    "实验与试点": "experimentation",
    "Experimentation & Pilots": "experimentation",
    "生产观测与学习闭环": "production-learning",
}


def _capability_id(value) -> str:
    return CAPABILITY_ALIASES.get(value, value) if isinstance(value, str) else value


def _issue(issues: list[str], code: str, detail: str = "") -> None:
    issues.append(code + (":" + detail if detail else ""))


def _nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def grade(events: list[dict], scenario: dict, contents: dict[str, str]) -> dict:
    routing = BEHAVIOR.assess_reads(events, scenario, contents)
    issues: list[str] = []
    validation_errors: list[dict] = []
    envelope = None
    try:
        envelope = BEHAVIOR.agent_json(events)
    except (ValueError, json.JSONDecodeError) as exc:
        _issue(issues, "RESULT_JSON_INVALID", str(exc))

    expected = scenario["expected"]
    if envelope is not None:
        required_envelope = {"profile", "capability_needs", "evidence", "gate", "replan", "claims"}
        if set(envelope) != required_envelope:
            _issue(issues, "RESULT_ENVELOPE_INVALID")
        else:
            profile = envelope["profile"]
            validation_errors.extend(error.as_dict() for error in validate_document(profile, "profile"))
            if isinstance(profile, dict):
                if profile.get("delivery_target") != expected["delivery_target"]:
                    _issue(issues, "DELIVERY_TARGET_MISMATCH")
                if profile.get("project_mode") != expected["project_mode"]:
                    _issue(issues, "PROJECT_MODE_MISMATCH")
                if profile.get("assignment_scope", {}).get("mode") != expected["scope_mode"]:
                    _issue(issues, "SCOPE_MODE_MISMATCH")
                nodes = {
                    item.get("node"): item
                    for item in profile.get("nodes", [])
                    if isinstance(item, dict)
                }
                for node_name in expected["active_nodes"]:
                    node = nodes.get(node_name, {})
                    if node.get("level") == "SKIP" or node.get("depth") == "SKIP" or node.get("scope_role") == "OUT_OF_SCOPE":
                        _issue(issues, "REQUIRED_NODE_INACTIVE", node_name)

            needs = envelope["capability_needs"]
            capability_names: list[str] = []
            if not isinstance(needs, list):
                _issue(issues, "CAPABILITY_NEEDS_INVALID")
            else:
                for index, need in enumerate(needs):
                    fields = {"capability", "mode", "reason", "supported_lifecycle_node", "decision_to_unlock"}
                    if not isinstance(need, dict) or set(need) != fields:
                        _issue(issues, "CAPABILITY_NEED_SHAPE", str(index))
                        continue
                    capability_names.append(_capability_id(need["capability"]))
                    if need["mode"] not in {"EXECUTE", "VERIFY", "REUSE"}:
                        _issue(issues, "CAPABILITY_MODE_INVALID", str(index))
                    if not all(_nonempty(need[field]) for field in ("reason", "supported_lifecycle_node", "decision_to_unlock")):
                        _issue(issues, "CAPABILITY_NEED_EMPTY", str(index))
                if set(capability_names) != set(expected["capabilities"]) or len(capability_names) != len(set(capability_names)):
                    _issue(issues, "CAPABILITY_SELECTION_MISMATCH")
                for capability, mode in expected.get("capability_modes", {}).items():
                    matches = [
                        need for need in needs
                        if isinstance(need, dict) and _capability_id(need.get("capability")) == capability
                    ]
                    if len(matches) != 1 or matches[0].get("mode") != mode:
                        _issue(issues, "CAPABILITY_MODE_MISMATCH", capability)

            evidence = envelope["evidence"]
            evidence_ids: set[str] = set()
            evidence_by_id: dict[str, dict] = {}
            if not isinstance(evidence, list) or not evidence:
                _issue(issues, "EVIDENCE_MISSING")
            else:
                for index, record in enumerate(evidence):
                    validation_errors.extend(
                        error.as_dict()
                        for error in validate_object("EvidenceRecord", record, f"evidence[{index}]")
                    )
                    if isinstance(record, dict) and isinstance(record.get("id"), str):
                        if record["id"] in evidence_ids:
                            _issue(issues, "EVIDENCE_ID_DUPLICATE", record["id"])
                        evidence_ids.add(record["id"])
                        evidence_by_id[record["id"]] = record
                joined_sources = " ".join(
                    str(record.get("source", "")) for record in evidence if isinstance(record, dict)
                )
                for marker in expected["sources"]:
                    if marker not in joined_sources:
                        _issue(issues, "EVIDENCE_SOURCE_MISSING", marker)

            gate = envelope["gate"]
            gate_fields = {"name", "result", "evidence_refs", "rationale", "missing_evidence"}
            if not isinstance(gate, dict) or set(gate) != gate_fields:
                _issue(issues, "GATE_SHAPE_INVALID")
            else:
                if gate["name"] != expected["gate_name"] or gate["result"] != expected["gate_result"]:
                    _issue(issues, "GATE_RESULT_MISMATCH")
                if not isinstance(gate["evidence_refs"], list) or not gate["evidence_refs"]:
                    _issue(issues, "GATE_EVIDENCE_MISSING")
                elif set(gate["evidence_refs"]) - evidence_ids:
                    _issue(issues, "GATE_EVIDENCE_UNKNOWN")
                if not _nonempty(gate["rationale"]):
                    _issue(issues, "GATE_RATIONALE_MISSING")
                missing = gate["missing_evidence"]
                if not isinstance(missing, list):
                    _issue(issues, "GATE_MISSING_EVIDENCE_INVALID")
                elif expected["missing_evidence_min"] == 0 and missing:
                    _issue(issues, "GATE_UNEXPECTED_EVIDENCE_GAP")
                elif len(missing) < expected["missing_evidence_min"]:
                    _issue(issues, "GATE_EVIDENCE_GAP_UNDISCLOSED")

            replan = envelope["replan"]
            replan_fields = {"required", "change_type", "reopen_trigger", "actions"}
            if not isinstance(replan, dict) or set(replan) != replan_fields:
                _issue(issues, "REPLAN_SHAPE_INVALID")
            else:
                if replan["required"] is not expected["replan_required"]:
                    _issue(issues, "REPLAN_REQUIRED_MISMATCH")
                if replan["change_type"] != expected["change_type"]:
                    _issue(issues, "REPLAN_CHANGE_TYPE_MISMATCH")
                actions = replan["actions"]
                actual_actions: set[tuple[str, str]] = set()
                if not isinstance(actions, list):
                    _issue(issues, "REPLAN_ACTIONS_INVALID")
                else:
                    for index, action in enumerate(actions):
                        if not isinstance(action, dict) or set(action) != {"action", "target"}:
                            _issue(issues, "REPLAN_ACTION_SHAPE", str(index))
                        else:
                            actual_actions.add((action["action"], action["target"]))
                    expected_actions = {tuple(item) for item in expected["actions"]}
                    if actual_actions != expected_actions or len(actions) != len(actual_actions):
                        _issue(issues, "REPLAN_SCOPE_MISMATCH")
                trigger = replan["reopen_trigger"]
                if expected.get("decision_id"):
                    if not isinstance(trigger, dict) or set(trigger) != {"decision_id", "trigger", "evidence_refs"}:
                        _issue(issues, "REOPEN_TRIGGER_INVALID")
                    else:
                        if trigger["decision_id"] != expected["decision_id"] or trigger["trigger"] != expected["trigger"]:
                            _issue(issues, "OLD_DECISION_NOT_REOPENED")
                        if not isinstance(trigger["evidence_refs"], list) or not trigger["evidence_refs"]:
                            _issue(issues, "REOPEN_EVIDENCE_MISSING")
                        elif set(trigger["evidence_refs"]) - evidence_ids:
                            _issue(issues, "REOPEN_EVIDENCE_UNKNOWN")
                elif trigger is not None:
                    _issue(issues, "REOPEN_TRIGGER_UNEXPECTED")

            if envelope["claims"] != {"external_write_performed": False, "invented_evidence": False}:
                _issue(issues, "BOUNDARY_CLAIMS_INVALID")

    status = "PASS" if routing["status"] == "PASS" and not issues and not validation_errors else "FAIL"
    return {
        "scenario": scenario["id"],
        "routing": routing,
        "validation_errors": validation_errors,
        "behavior_issues": issues,
        "normalized_result": envelope,
        "status": status,
    }


def prompt_for(scenario: dict, kernel_line_count: int) -> str:
    case_text = (HERE / "cases" / f'{scenario["case"]}.md').read_text(encoding="utf-8")
    selectors = []
    for start in range(0, kernel_line_count, 60):
        if start == 0:
            selectors.append("Select-Object -First 60")
        elif start + 60 < kernel_line_count:
            selectors.append(f"Select-Object -Skip {start} -First 60")
        else:
            selectors.append(f"Select-Object -Skip {start}")
    kernel_commands = "; ".join(
        "Get-Content -LiteralPath 'skill/SKILL.md' -Encoding UTF8 | " + selector
        for selector in selectors
    )
    return f"""Use the AI product development skill copied to skill/SKILL.md. This is an independent read-only Phase 5 assessment. Do not write files, execute product work, use external services, install tools, or request permissions.

Read SKILL.md first using every one of these as a separate command, in this exact order: {kernel_commands}. Before chunking any other selected file, use a separate `(Get-Content -LiteralPath 'skill/...' -Encoding UTF8).Count` command to determine its length. Read a file of 100 lines or fewer once; read a longer file in contiguous 60-line Select-Object chunks, and never issue a chunk whose starting line is at or beyond the measured length. Do not list or bulk-read directories. Select supporting files from the router based only on the scenario; do not load capability templates or examples because no formal artifact is being authored.

All paths shown in SKILL.md are relative to the copied skill directory. Prefix every selected router path with `skill/` when reading it from this temporary workspace. This assessment performs Profile, lifecycle-state, Capability Need, Evidence, Gate, and Replan decisions; load the applicable lifecycle and runtime rules for those decisions. Read Replan rules only when the scenario contains a material input, artifact, task, decision, or scope change. It identifies capability needs but does not execute their professional methods, so do not read a capability contract merely because you emit its name. Read a capability contract only if its detailed boundary is necessary to distinguish a real trigger from a non-trigger.

Capability needs cover concrete gaps required to deliver the stated assignment, including dependency-blocked downstream gaps, but exclude generic catalog coverage. If runnable AI feasibility or offline validation is explicitly in scope and lacks evidence, retain those concrete needs even when Discovery must run first. For a required canonical string whose value was not supplied, use the literal `not supplied`; never use an empty string and never invent a date, owner, or observation.

NodeProfile `active_capabilities` uses the canonical Profile labels from Execution Profile. In particular, when Validation lacks acceptance criteria, Solution Design must contain the exact label `Evaluation Design`; a translated professional-domain title is not a substitute.

Return exactly one JSON object and no prose with this shape:
{{
  "profile": {{"delivery_target":"PROTOTYPE|DEMO|MVP|ENTERPRISE|UNDECIDED","project_mode":"GREENFIELD|BROWNFIELD|HYBRID","assignment_scope":{{all canonical AssignmentScope fields}},"nodes":[eight canonical NodeProfile objects in order],"validation_context":{{"existing_repository_modification":false,"verified_design":false,"acceptance_criteria_defined":false,"production_release":false,"release_execution":false,"monitoring_covered":false,"release_readiness":"PASS|PASS_WITH_ASSUMPTIONS|BLOCKED"}}}},
  "capability_needs":[{{"capability":"canonical capability-domain label or directory slug from the main router","mode":"EXECUTE|VERIFY|REUSE","reason":"...","supported_lifecycle_node":"...","decision_to_unlock":"..."}}],
  "evidence":[{{all canonical EvidenceRecord fields; source must preserve the supplied SRC-* identifier; version uses vN}}],
  "gate":{{"name":"Qualification|Build Readiness|Release Readiness","result":"PASS|PASS_WITH_ASSUMPTIONS|BLOCKED","evidence_refs":["EvidenceRecord id"],"rationale":"...","missing_evidence":[]}},
  "replan":{{"required":true,"change_type":"INPUT_CHANGE|ARTIFACT_CHANGE|TASK_FAILURE|DECISION_CHANGE|SCOPE_CHANGE|null","reopen_trigger":{{"decision_id":"...","trigger":"...","evidence_refs":["EvidenceRecord id"]}},"actions":[{{"action":"PRESERVE|OUTDATE|ADD|CANCEL","target":"task id"}}]}},
  "claims":{{"external_write_performed":false,"invented_evidence":false}}
}}

When no replan or reopen is required, use null for change_type/reopen_trigger and an empty actions list. Capability needs must include only current gaps: use REUSE for a still-valid capability result, VERIFY when changed inputs require checking it, and EXECUTE for unresolved work. Do not emit capability entries merely because a domain exists. Evidence may only restate supplied observations; interpretations and limitations must remain separate. A Gate must cite emitted Evidence IDs and disclose missing evidence. Preserve unrelated tasks in a replan and change only the explicitly affected tasks.

Scenario:
{case_text}"""


def run(scenario: dict, output: Path, codex: str, timeout: int, model: str, thinking: str) -> str:
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="ai-skill-phase5-") as temporary:
        work = Path(temporary)
        copy = work / "skill"
        shutil.copytree(SKILL, copy)
        before = inventory(copy)
        contents = {
            name: (copy / name).read_text(encoding="utf-8")
            for name in before
            if name.endswith((".md", ".yaml", ".py"))
        }
        prompt = prompt_for(scenario, len(contents["SKILL.md"].splitlines()))
        command = [
            codex, "exec", "--json", "--ephemeral", "--ignore-user-config",
            "-m", model, "-c", f'model_reasoning_effort="{thinking}"',
            "-s", "read-only", "-c", 'windows.sandbox="elevated"',
            "--skip-git-repo-check", "-C", str(work), "-",
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
                command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                text=True, encoding="utf-8",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=[item["id"] for item in SCENARIOS], required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--codex", default=shutil.which("codex"))
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument("--thinking", default="low")
    args = parser.parse_args()
    if not args.codex:
        parser.error("Codex CLI not found")
    scenario = next(item for item in SCENARIOS if item["id"] == args.scenario)
    return 0 if run(scenario, args.output, args.codex, args.timeout, args.model, args.thinking) == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
