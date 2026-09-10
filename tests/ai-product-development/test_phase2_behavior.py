from pathlib import Path
import importlib.util
import unittest

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "phase2/behavior/run_behavior.py"
spec = importlib.util.spec_from_file_location("phase2_run_behavior", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BehaviorTraceClassificationTests(unittest.TestCase):
    def scenario(self):
        return {"required": [], "support": {}}

    def test_validation_exit_one_is_allowed(self):
        events = [{
            "type": "item.completed",
            "item": {
                "id": "validation",
                "type": "command_execution",
                "command": "python -c 'from runtime_validation.validators import validate_document'",
                "status": "failed",
                "exit_code": 1,
            },
        }]
        result = module.assess_reads(events, self.scenario(), {})
        self.assertEqual(result["trace_issues"], [])
        self.assertEqual(result["allowed_tool_calls"][0]["exit_code"], 1)

    def test_validator_cli_document_error_is_allowed(self):
        events = [{
            "type": "item.completed",
            "item": {
                "id": "validation-cli",
                "type": "command_execution",
                "command": "python skill/scripts/validate_runtime.py combined -",
                "status": "failed",
                "exit_code": 2,
            },
        }]
        result = module.assess_reads(events, self.scenario(), {})
        self.assertEqual(result["trace_issues"], [])
        self.assertEqual(result["allowed_tool_calls"][0]["exit_code"], 2)

    def test_unrelated_failed_command_is_rejected(self):
        events = [{
            "type": "item.completed",
            "item": {
                "id": "other",
                "type": "command_execution",
                "command": "unknown-command",
                "status": "failed",
                "exit_code": 1,
            },
        }]
        result = module.assess_reads(events, self.scenario(), {})
        self.assertEqual(result["trace_issues"], ["FAILED_COMMAND: other"])


if __name__ == "__main__":
    unittest.main()
