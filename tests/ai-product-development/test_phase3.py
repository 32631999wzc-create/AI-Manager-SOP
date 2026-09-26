from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest

import yaml


REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "skills" / "ai-product-development" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from project_runtime import ProjectRuntime, RuntimeFailure
from project_runtime.store import atomic_write, load_yaml


def scenario() -> dict:
    path = REPO / "tests" / "ai-product-development" / "phase2" / "fixtures" / "scenarios" / "01-greenfield-prototype.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


class RuntimeTestCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "fixtures").mkdir()
        (self.root / "fixtures" / "design.md").write_text("# Design\n", encoding="utf-8")
        self.runtime = ProjectRuntime(self.root)

    def tearDown(self):
        self.temporary.cleanup()

    def initialize(self):
        return self.runtime.init(scenario(), "golden-feedback-organizer")

    def test_init_is_safe_and_idempotent_for_same_input(self):
        self.assertEqual("initialized", self.initialize()["status"])
        self.assertEqual("already_initialized", self.initialize()["status"])
        self.assertTrue(self.runtime.validate()["valid"])
        self.assertFalse((self.root / ".ai-product.init.tmp").exists())

    def test_init_refuses_different_input(self):
        self.initialize()
        changed = scenario()
        changed["plan"]["plan"]["objective"] = "different"
        with self.assertRaisesRegex(RuntimeFailure, "different initialization input"):
            self.runtime.init(changed, "golden-feedback-organizer")

    def test_next_checkpoint_and_fresh_instance_resume(self):
        self.initialize()
        selected = self.runtime.next()
        self.assertEqual("T2", selected["task"]["id"])
        self.assertEqual(["design-v1"], selected["context"]["relevant_artifacts"])
        checkpoint = self.runtime.checkpoint(["confirm sample language"])
        self.assertEqual(1, checkpoint["sequence"])
        resumed = ProjectRuntime(self.root).resume()
        self.assertEqual("T2", resumed["selection"]["task"]["id"])
        self.assertEqual(["confirm sample language"], resumed["snapshot"]["unresolved_items"])

    def test_resume_rejects_tampered_snapshot(self):
        self.initialize()
        self.runtime.checkpoint()
        snapshot = load_yaml(self.runtime.latest_snapshot_path)
        snapshot["plan_version"] = "v99"
        atomic_write(self.runtime.latest_snapshot_path, snapshot)
        with self.assertRaisesRegex(RuntimeFailure, "snapshot plan version"):
            ProjectRuntime(self.root).resume()

    def test_missing_active_artifact_is_detected(self):
        self.initialize()
        (self.root / "fixtures" / "design.md").unlink()
        with self.assertRaisesRegex(RuntimeFailure, "ACTIVE artifact is missing"):
            self.runtime.validate()

    def test_completed_task_requires_human_review_and_artifact_commit_versions(self):
        self.initialize()
        (self.root / "report-v1.md").write_text("v1", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeFailure, "human review"):
            self.runtime.update_task("T2", "COMPLETED", validation_pass=True)
        with self.assertRaisesRegex(RuntimeFailure, "validation PASS"):
            self.runtime.submit_result("T2", {"result": "First report", "output_files": ["report-v1.md"]})
        self.runtime.submit_result("T2", {"result": "First report", "output_files": ["report-v1.md"]}, validation_pass=True)
        self.assertEqual("review_blocked", self.runtime.next()["status"])
        self.runtime.review_task({"task_id": "T2", "decision": "APPROVED", "reviewer": "PM owner", "feedback": ""})
        first = {
            "id": "report-v1", "type": "REPORT", "name": "Feedback report", "version": "v1",
            "status": "ACTIVE", "summary": "First report", "location": "report-v1.md",
            "source_tasks": ["T2"], "source_records": [], "evidence_refs": [], "decision_refs": [], "dependencies": ["design-v1"],
        }
        self.runtime.commit_artifact(first, validation_pass=True)
        (self.root / "report-v2.md").write_text("v2", encoding="utf-8")
        second = {**first, "id": "report-v2", "version": "v2", "location": "report-v2.md", "summary": "Updated report"}
        with self.assertRaisesRegex(RuntimeFailure, "approved source-task outputs"):
            self.runtime.commit_artifact(second, validation_pass=True)
        self.runtime.review_task({"task_id": "T2", "decision": "APPROVED", "reviewer": "PM owner", "feedback": "Use v2", "output_files": ["report-v2.md"]})
        self.runtime.commit_artifact(second, validation_pass=True)
        artifacts = load_yaml(self.runtime.artifacts_path)["artifacts"]
        by_id = {item["id"]: item for item in artifacts}
        self.assertEqual("SUPERSEDED", by_id["report-v1"]["status"])
        self.assertEqual("ACTIVE", by_id["report-v2"]["status"])

    def test_register_record_and_snapshot_reference(self):
        self.initialize()
        record = {
            "id": "R1", "type": "DECISION", "topic": "delivery", "content": "local demo",
            "status": "ACTIVE", "source": "user", "version": "v1", "affected_scope": ["Implementation"],
        }
        self.runtime.register_record(record)
        snapshot = self.runtime.checkpoint()["snapshot"]
        self.assertEqual(["R1"], snapshot["active_records"])

    def test_local_replan_adds_task_and_increments_version(self):
        self.initialize()
        replacement = deepcopy(load_yaml(self.runtime.plan_path))
        replacement["plan"]["version"] = "v2"
        new_task = deepcopy(replacement["plan"]["tasks"][1])
        new_task.update({"id": "T3", "name": "Source filter", "goal": "Add source filter", "status": "NOT_STARTED", "dependencies": ["T2"], "expected_output": "source filter", "acceptance_criteria": ["source filter is validated"]})
        replacement["plan"]["tasks"].append(new_task)
        replacement["plan"]["dependencies"].append({"from": "T2", "to": "T3", "type": "HARD"})
        replacement["plan"]["critical_path"].append("T3")
        replacement["write_targets"]["T3"] = ["filter:v1"]
        result = self.runtime.replan({"change_type": "INPUT_CHANGE", "actions": [{"action": "ADD", "target": "T3"}], "plan": replacement})
        self.assertTrue(result["dag_changed"])
        self.assertEqual("v2", result["plan_version"])

    def test_replan_rejects_missing_action(self):
        self.initialize()
        replacement = deepcopy(load_yaml(self.runtime.plan_path))
        replacement["plan"]["tasks"][1]["status"] = "OUTDATED"
        with self.assertRaisesRegex(RuntimeFailure, "lacks an action"):
            self.runtime.replan({"change_type": "INPUT_CHANGE", "actions": [], "plan": replacement})


    def test_profile_update_and_completion_check(self):
        self.initialize()
        self.assertFalse(self.runtime.complete()["complete"])
        self.runtime.submit_result("T2", {"result": "Validated feedback report", "output_files": []}, validation_pass=True)
        self.runtime.review_task({"task_id": "T2", "decision": "APPROVED", "reviewer": "PM owner", "feedback": ""})
        profile = deepcopy(load_yaml(self.runtime.profile_path))
        for node in profile["nodes"]:
            if node["level"] == "REQUIRED":
                node["status"] = "SATISFIED"
        self.runtime.update_profile(profile)
        result = self.runtime.complete()
        self.assertTrue(result["complete"], result["reasons"])

    def test_human_edit_and_feedback_are_forwarded_without_restoring_old_output(self):
        self.initialize()
        replacement = deepcopy(load_yaml(self.runtime.plan_path))
        new_task = deepcopy(replacement["plan"]["tasks"][1])
        new_task.update({"id": "T3", "name": "Follow approved direction", "goal": "Use current reviewed result",
                         "status": "NOT_STARTED", "dependencies": ["T2"], "expected_output": "follow-up",
                         "acceptance_criteria": ["uses approved result"]})
        replacement["plan"]["tasks"].append(new_task)
        replacement["plan"]["dependencies"].append({"from": "T2", "to": "T3", "type": "HARD"})
        replacement["plan"]["critical_path"].append("T3")
        replacement["plan"]["version"] = "v2"
        replacement["write_targets"]["T3"] = ["follow-up:v1"]
        self.runtime.replan({"change_type": "INPUT_CHANGE", "actions": [{"action": "ADD", "target": "T3"}], "plan": replacement})
        output = self.root / "reviewed.md"
        output.write_text("draft", encoding="utf-8")
        self.runtime.submit_result("T2", {"result": "draft direction", "output_files": ["reviewed.md"]}, validation_pass=True)
        output.write_text("human revised direction", encoding="utf-8")
        approved = self.runtime.review_task({
            "task_id": "T2", "decision": "APPROVED", "reviewer": "PM owner",
            "feedback": "Prioritize the human-revised direction", "result": "human revised direction",
        })
        self.assertTrue(approved["changed"])
        self.assertEqual("review_blocked", self.runtime.next()["status"])
        self.runtime.assess_review_impact({
            "task_id": "T2", "review_sha256": approved["review_sha256"],
            "assessment": "CONTINUE", "reason": "T3 already follows this direction",
        })
        self.runtime.update_task("T3", "READY")
        next_task = self.runtime.next()
        self.assertEqual("T3", next_task["task"]["id"])
        self.assertEqual("human revised direction", next_task["review_inputs"][0]["result"])
        self.assertEqual("Prioritize the human-revised direction", next_task["review_inputs"][0]["feedback"])
        self.assertEqual("human revised direction", output.read_text(encoding="utf-8"))
        output.write_text("later edit", encoding="utf-8")
        self.assertEqual("APPROVED_OUTPUT_CHANGED", self.runtime.next()["blockers"][0]["reason"])
        amended = self.runtime.review_task({
            "task_id": "T2", "decision": "APPROVED", "reviewer": "PM owner",
            "feedback": "Use this latest edit",
        })
        self.assertTrue(amended["changed"])
        self.assertEqual("", amended["authoritative_result"])
        self.runtime.assess_review_impact({
            "task_id": "T2", "review_sha256": amended["review_sha256"],
            "assessment": "CONTINUE", "reason": "The pending follow-up can use the latest reviewed file",
        })
        self.assertEqual("T3", self.runtime.next()["task"]["id"])

    def test_rejected_result_returns_same_task_with_feedback(self):
        self.initialize()
        self.runtime.submit_result("T2", {"result": "wrong direction", "output_files": []}, validation_pass=True)
        rejected = self.runtime.review_task({
            "task_id": "T2", "decision": "REJECTED", "reviewer": "PM owner",
            "feedback": "Use the existing evidence instead",
        })
        self.assertEqual("rework_required", rejected["status"])
        selected = self.runtime.next()
        self.assertEqual("T2", selected["task"]["id"])
        self.assertEqual("Use the existing evidence instead", selected["review_inputs"][0]["feedback"])
        self.runtime.submit_result("T2", {"result": "reworked direction", "output_files": []}, validation_pass=True)
        self.assertEqual("review_blocked", self.runtime.next()["status"])

    def test_approved_feedback_requires_impact_assessment_and_real_replan(self):
        self.initialize()
        self.runtime.submit_result("T2", {"result": "initial direction", "output_files": []}, validation_pass=True)
        approved = self.runtime.review_task({
            "task_id": "T2", "decision": "APPROVED", "reviewer": "PM owner",
            "feedback": "Change the next work to a narrower audience",
        })
        self.assertEqual("REVIEW_IMPACT_PENDING", self.runtime.next()["blockers"][0]["reason"])
        self.runtime.assess_review_impact({
            "task_id": "T2", "review_sha256": approved["review_sha256"],
            "assessment": "REPLAN", "reason": "Audience change affects the next task",
        })
        self.assertEqual("REVIEW_REPLAN_REQUIRED", self.runtime.next()["blockers"][0]["reason"])
        replacement = deepcopy(load_yaml(self.runtime.plan_path))
        replacement["plan"]["objective"] = "Deliver to the narrower audience"
        self.runtime.replan({"change_type": "INPUT_CHANGE", "actions": [], "plan": replacement})
        self.assertNotEqual("review_blocked", self.runtime.next()["status"])
    def test_cli_init_save_and_resume_across_processes(self):
        source = self.root / "init.yaml"
        source.write_text(yaml.safe_dump(scenario(), sort_keys=False), encoding="utf-8")
        cli = SCRIPTS / "project_runtime.py"

        def run(*arguments):
            completed = subprocess.run(
                [sys.executable, "-B", "-X", "utf8", str(cli), "--root", str(self.root), *arguments],
                check=False, capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            return json.loads(completed.stdout)["result"]

        self.assertEqual("initialized", run("init", "--input", "init.yaml", "--project-id", "cli-golden")["status"])
        self.assertEqual("T2", run("next")["task"]["id"])
        self.assertEqual("checkpointed", run("save")["status"])
        self.assertEqual("T2", run("resume")["selection"]["task"]["id"])
        submission = self.root / "submission.yaml"
        submission.write_text(yaml.safe_dump({"result": "Ready for review", "output_files": []}), encoding="utf-8")
        self.assertEqual("waiting_for_review", run("submit-result", "--id", "T2", "--input", "submission.yaml", "--validation-pass")["status"])
        self.assertEqual("review_blocked", run("next")["status"])
        self.assertEqual("review_blocked", run("resume")["selection"]["status"])
        bypass = subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(cli), "--root", str(self.root),
             "task", "--id", "T2", "--status", "COMPLETED", "--validation-pass"],
            check=False, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(1, bypass.returncode)
        review = self.root / "human-review.yaml"
        review.write_text(yaml.safe_dump({
            "task_id": "T2", "decision": "APPROVED", "reviewer": "PM owner", "feedback": "",
        }), encoding="utf-8")
        self.assertEqual("approved", run("review", "--input", "human-review.yaml")["status"])
        self.assertEqual("no_ready_task", run("resume")["selection"]["status"])

class GoldenFeedbackOrganizerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = REPO / "examples" / "ai-product-development" / "golden-feedback-organizer" / "feedback_organizer.py"
        spec = importlib.util.spec_from_file_location("feedback_organizer", path)
        cls.module = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(cls.module)

    def test_golden_sample_is_deduplicated_prioritized_and_traceable(self):
        base = REPO / "examples" / "ai-product-development" / "golden-feedback-organizer"
        rows = self.module.load_feedback(base / "sample-feedback.csv")
        result = self.module.organize(rows)
        self.assertEqual({"received": 5, "unique": 4, "duplicates": 1}, result["summary"])
        self.assertEqual("F1", result["duplicates"]["F2"])
        self.assertEqual("reliability", result["themes"][0]["theme"])
        self.assertEqual(["F1"], result["themes"][0]["evidence"])
        report = self.module.markdown_report(result)
        self.assertIn("| reliability |", report)
        self.assertIn("**F3**", report)


    def test_source_filter_and_cli_outputs(self):
        base = REPO / "examples" / "ai-product-development" / "golden-feedback-organizer"
        rows = self.module.load_feedback(base / "sample-feedback.csv")
        filtered = self.module.organize(rows, source="support")
        self.assertEqual(2, filtered["summary"]["received"])
        with tempfile.TemporaryDirectory() as temporary:
            json_output = Path(temporary) / "output.json"
            markdown_output = Path(temporary) / "report.md"
            completed = subprocess.run([
                sys.executable, "-B", "-X", "utf8", str(base / "feedback_organizer.py"),
                str(base / "sample-feedback.csv"), "--json-output", str(json_output),
                "--markdown-output", str(markdown_output), "--source", "support",
            ], check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual(2, json.loads(json_output.read_text(encoding="utf-8"))["summary"]["received"])
            self.assertIn("Feedback Insights", markdown_output.read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
