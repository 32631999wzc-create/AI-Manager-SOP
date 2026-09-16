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

    def test_contiguous_range_chunks_are_verified(self):
        content = "\n".join(f"line {index}" for index in range(135))
        events = []
        for index, (start, end, selector) in enumerate((
            (0, 60, "-First 60"),
            (60, 120, "-Skip 60 -First 60"),
            (120, 135, "-Skip 120"),
        )):
            events.append({"type": "item.completed", "item": {
                "id": f"chunk-{index}", "type": "command_execution",
                "command": "Get-Content -LiteralPath 'skill/SKILL.md' -Encoding UTF8 | "
                           f"Select-Object {selector}",
                "status": "completed", "exit_code": 0,
                "aggregated_output": "\n".join(content.splitlines()[start:end]),
            }})
        result = module.assess_reads(
            events, {"required": ["SKILL.md"], "support": {}}, {"SKILL.md": content}
        )
        self.assertEqual(result["status"], "PASS")

    def test_gapped_range_chunks_are_rejected(self):
        content = "\n".join(f"line {index}" for index in range(135))
        events = [{"type": "item.completed", "item": {
            "id": "chunk-0", "type": "command_execution",
            "command": "Get-Content -LiteralPath 'skill/SKILL.md' -Encoding UTF8 | Select-Object -First 60",
            "status": "completed", "exit_code": 0,
            "aggregated_output": "\n".join(content.splitlines()[:60]),
        }}, {"type": "item.completed", "item": {
            "id": "chunk-2", "type": "command_execution",
            "command": "Get-Content -LiteralPath 'skill/SKILL.md' -Encoding UTF8 | Select-Object -Skip 120",
            "status": "completed", "exit_code": 0,
            "aggregated_output": "\n".join(content.splitlines()[120:]),
        }}]
        result = module.assess_reads(
            events, {"required": ["SKILL.md"], "support": {}}, {"SKILL.md": content}
        )
        self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
