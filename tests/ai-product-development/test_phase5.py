from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml


REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / "skills" / "ai-product-development"
SCRIPTS = SKILL / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from project_runtime import ProjectRuntime, RuntimeFailure
from project_runtime.store import load_yaml


def base_scenario() -> dict:
    path = REPO / "tests" / "ai-product-development" / "phase2" / "fixtures" / "scenarios" / "01-greenfield-prototype.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class Phase5RuntimeDecisionChainTests(unittest.TestCase):
    def test_missing_monitoring_evidence_blocks_release_without_state_change(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "fixtures").mkdir()
            (root / "fixtures" / "design.md").write_text("# design\n", encoding="utf-8")
            fixture = REPO / "tests" / "ai-product-development" / "phase2" / "fixtures" / "scenarios" / "06-enterprise-release.yaml"
            runtime = ProjectRuntime(root)
            runtime.init(yaml.safe_load(fixture.read_text(encoding="utf-8")), "phase5-blocked-release")
            before = load_yaml(runtime.plan_path)
            self.assertEqual("no_ready_task", runtime.next()["status"])
            result = runtime.complete()
            self.assertFalse(result["complete"])
            self.assertIn("Release Readiness", result["reasons"]["blocked_gates"])
            self.assertIn("T2", result["reasons"]["blocking_tasks"])
            self.assertEqual(before, load_yaml(runtime.plan_path))

    def test_task_failure_replans_only_affected_work_and_rejects_bad_change(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "fixtures").mkdir()
            (root / "fixtures" / "design.md").write_text("# design\n", encoding="utf-8")
            runtime = ProjectRuntime(root)
            runtime.init(base_scenario(), "phase5-task-failure")
            runtime.update_task("T2", "FAILED")
            failed_plan = load_yaml(runtime.plan_path)
            replacement = deepcopy(failed_plan)
            replacement["plan"]["version"] = "v2"
            replacement["plan"]["tasks"][1]["status"] = "OUTDATED"
            retry = deepcopy(failed_plan["plan"]["tasks"][1])
            retry.update({
                "id": "T3", "name": "Retry affected work", "status": "READY",
                "goal": "Retry the failed work after diagnosis",
                "expected_output": "validated replacement output",
                "acceptance_criteria": ["Replacement output passes validation"],
            })
            replacement["plan"]["tasks"].append(retry)
            replacement["plan"]["dependencies"].append({"from": "T1", "to": "T3", "type": "HARD"})
            replacement["plan"]["critical_path"] = ["T1", "T3"]
            replacement["write_targets"]["T3"] = ["retry-output:v1"]
            with self.assertRaises(RuntimeFailure):
                runtime.replan({"change_type": "TASK_FAILURE", "actions": [], "plan": replacement})
            self.assertEqual(failed_plan, load_yaml(runtime.plan_path))
            result = runtime.replan({
                "change_type": "TASK_FAILURE",
                "actions": [
                    {"action": "PRESERVE", "target": "T1"},
                    {"action": "OUTDATE", "target": "T2"},
                    {"action": "ADD", "target": "T3"},
                ],
                "plan": replacement,
            })
            self.assertEqual("v2", result["plan_version"])
            states = {task["id"]: task["status"] for task in load_yaml(runtime.plan_path)["plan"]["tasks"]}
            self.assertEqual({"T1": "COMPLETED", "T2": "OUTDATED", "T3": "READY"}, states)
            self.assertTrue(runtime.validate()["valid"])

    def test_production_evidence_reopens_decision_and_preserves_unaffected_work(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "fixtures").mkdir()
            (root / "fixtures" / "design.md").write_text("# design\n", encoding="utf-8")
            runtime = ProjectRuntime(root)
            runtime.init(base_scenario(), "phase5-decision-chain")

            baseline = {
                "id": "E-BASE", "type": "PRODUCTION_METRIC", "source": "baseline-monitoring",
                "observed_at": "2026-09-01", "context": "routing v1",
                "supports": ["D-P1"], "contradicts": [],
                "observation": "Safety escalation recall was 100%.",
                "interpretation": "The release guardrail was satisfied.",
                "confidence": "HIGH", "limitations": ["Historical seven-day window"],
                "version": "v1", "owner": "quality-owner",
            }
            runtime.register_evidence(baseline)
            decision = {
                "id": "D-P1", "question": "May routing suggestions remain enabled?",
                "options": ["Keep enabled", "Disable"], "selected": "Keep enabled",
                "rationale": "The safety guardrail was satisfied in baseline evidence.",
                "evidence_refs": ["E-BASE"], "assumptions": [], "dissent": [],
                "owner": "release-owner", "made_at": "2026-09-01", "valid_until": None,
                "reopen_trigger": "safety escalation recall falls below 100%", "supersedes": None,
            }
            runtime.register_decision(decision)
            production = {
                "id": "E-PROD", "type": "PRODUCTION_METRIC", "source": "SRC-P1 production-monitoring",
                "observed_at": "2026-09-15", "context": "product v1.3 / model M2 / prompt P7",
                "supports": [], "contradicts": ["D-P1"],
                "observation": "Safety escalation recall fell to 97% over the last seven days.",
                "interpretation": "The active decision's release guardrail is no longer satisfied.",
                "confidence": "HIGH", "limitations": ["One seven-day window"],
                "version": "v1", "owner": "quality-owner",
            }
            runtime.register_evidence(production)

            replacement = deepcopy(load_yaml(runtime.plan_path))
            replacement["plan"]["version"] = "v2"
            replacement["plan"]["tasks"][1]["status"] = "OUTDATED"
            incident = deepcopy(replacement["plan"]["tasks"][1])
            incident.update({
                "id": "T3", "name": "Diagnose routing incident",
                "goal": "Identify and contain the safety recall regression", "status": "READY",
                "dependencies": ["T1"], "expected_output": "validated incident diagnosis",
                "acceptance_criteria": ["Safety recall regression has evidence-backed causes and containment"],
                "context_requirements": ["D-P1"],
            })
            replacement["plan"]["tasks"].append(incident)
            replacement["plan"]["dependencies"].append({"from": "T1", "to": "T3", "type": "HARD"})
            replacement["plan"]["critical_path"] = ["T1", "T3"]
            replacement["write_targets"]["T3"] = ["incident-note:v1"]
            result = runtime.replan({
                "change_type": "DECISION_CHANGE",
                "reopen_trigger": {
                    "decision_id": "D-P1",
                    "trigger": "safety escalation recall falls below 100%",
                    "evidence_refs": ["E-PROD"],
                },
                "actions": [
                    {"action": "PRESERVE", "target": "T1"},
                    {"action": "OUTDATE", "target": "T2"},
                    {"action": "ADD", "target": "T3"},
                ],
                "plan": replacement,
            })
            self.assertEqual("D-P1", result["reopened_decision"])
            states = {task["id"]: task["status"] for task in load_yaml(runtime.plan_path)["plan"]["tasks"]}
            self.assertEqual({"T1": "COMPLETED", "T2": "OUTDATED", "T3": "READY"}, states)

            replacement_decision = {
                **decision,
                "id": "D-P2", "selected": "Disable",
                "rationale": "Production evidence shows the zero-miss guardrail failed.",
                "evidence_refs": ["E-PROD"], "made_at": "2026-09-15", "supersedes": "D-P1",
            }
            runtime.register_decision(replacement_decision)
            selection = runtime.next()
            self.assertEqual("T3", selection["task"]["id"])
            self.assertEqual(["D-P2"], selection["context"]["relevant_decisions"])
            self.assertEqual(["E-PROD"], selection["context"]["relevant_evidence"])

            (root / "incident-note.md").write_text("# incident\n", encoding="utf-8")
            artifact = {
                "id": "incident-note-v1", "type": "INCIDENT_NOTE", "name": "Routing incident",
                "version": "v1", "status": "ACTIVE", "summary": "Decision and evidence chain",
                "location": "incident-note.md", "source_tasks": [], "source_records": [],
                "evidence_refs": ["E-PROD"], "decision_refs": ["D-P2"], "dependencies": [],
            }
            runtime.commit_artifact(artifact, validation_pass=True)
            self.assertTrue(runtime.validate()["valid"])

    def test_phase5_declares_three_required_scenario_types(self):
        path = REPO / "tests" / "ai-product-development" / "phase5" / "scenarios.json"
        scenarios = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(
            ["Greenfield AI product", "Existing product feature change", "Production quality / risk issue"],
            [item["title"] for item in scenarios],
        )


if __name__ == "__main__":
    unittest.main()
