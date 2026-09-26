from pathlib import Path
import importlib.util
import sys
import unittest

HERE = Path(__file__).resolve().parent
MODULE_PATH = HERE / "phase2/behavior/run_behavior.py"
spec = importlib.util.spec_from_file_location("phase2_run_behavior", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.modules["run_behavior"] = module

VERIFY_PATH = HERE / "phase2/behavior/verify_behavior.py"
verify_spec = importlib.util.spec_from_file_location("phase2_verify_behavior", VERIFY_PATH)
verify_module = importlib.util.module_from_spec(verify_spec)
verify_spec.loader.exec_module(verify_module)


class BehaviorTraceClassificationTests(unittest.TestCase):
    def scenario(self):
        return {"required": [], "support": {}}

    def test_output_schema_has_strict_nested_objects(self):
        def check(value):
            if isinstance(value, dict):
                if value.get("type") == "object":
                    self.assertFalse(value["additionalProperties"])
                    self.assertEqual(set(value["required"]), set(value["properties"]))
                for child in value.values():
                    check(child)
            elif isinstance(value, list):
                for child in value:
                    check(child)

        check(module.output_schema())

    def test_legacy_metadata_without_output_schema_fingerprint_is_supported(self):
        verify_module.verify_output_schema_fingerprint({})

    def test_output_schema_fingerprint_mismatch_is_rejected(self):
        with self.assertRaisesRegex(AssertionError, "another output schema"):
            verify_module.verify_output_schema_fingerprint({"output_schema_sha256": "wrong"})

    def test_verifier_builds_prompt_with_current_kernel_line_count(self):
        original = verify_module.prompt_for
        try:
            verify_module.prompt_for = lambda scenario, count: f"{scenario['id']}:{count}"
            self.assertEqual(
                "B-test:3",
                verify_module.current_prompt({"id": "B-test"}, {"SKILL.md": "one\ntwo\nthree\n"}),
            )
        finally:
            verify_module.prompt_for = original

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

    def test_wrapped_measure_line_count_is_classified_as_read_only(self):
        events = [{"type": "item.completed", "item": {
            "id": "count", "type": "command_execution",
            "command": "(Get-Content -LiteralPath 'skill/SKILL.md' -Encoding UTF8 | Measure-Object -Line).Lines",
            "status": "completed", "exit_code": 0, "aggregated_output": "1",
        }}]
        result = module.assess_reads(events, self.scenario(), {"SKILL.md": "content"})
        self.assertEqual(result["trace_issues"], [])
        self.assertEqual(result["allowed_tool_calls"][0]["reason"], "read-only line count")

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

    def test_empty_chunk_past_eof_is_not_unverified_read(self):
        content = "\n".join(f"line {index}" for index in range(120))
        events = []
        for index, selector, output in (
            (0, "-First 60", "\n".join(content.splitlines()[:60])),
            (1, "-Skip 60 -First 60", "\n".join(content.splitlines()[60:])),
            (2, "-Skip 120", ""),
        ):
            events.append({"type": "item.completed", "item": {
                "id": f"chunk-{index}", "type": "command_execution",
                "command": "Get-Content -LiteralPath 'skill/SKILL.md' -Encoding UTF8 | "
                           f"Select-Object {selector}",
                "status": "completed", "exit_code": 0,
                "aggregated_output": output,
            }})
        result = module.assess_reads(
            events, {"required": ["SKILL.md"], "support": {}}, {"SKILL.md": content}
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["allowed_tool_calls"][0]["reason"], "empty read past end of file")

    def test_successful_read_with_incomplete_tool_output_is_trace_mismatch(self):
        result = module.assess_reads([{"type": "item.completed", "item": {
            "id": "partial", "type": "command_execution",
            "command": "Get-Content -LiteralPath 'skill/SKILL.md' -Encoding UTF8",
            "status": "completed", "exit_code": 0, "aggregated_output": "only a fragment",
        }}], {"required": ["SKILL.md"], "support": {}}, {"SKILL.md": "complete content"})
        self.assertEqual(result["trace_issues"], ["TRACE_OUTPUT_MISMATCH: partial"])

    def test_grouped_reads_require_exact_combined_output(self):
        command = (
            'pwsh -Command "Get-Content -LiteralPath \'skill/SKILL.md\' -Encoding UTF8; '
            'Get-Content -LiteralPath \'skill/schemas/plan.yaml\' -Encoding UTF8"'
        )
        contents = {"SKILL.md": "first\nsecond", "schemas/plan.yaml": "third"}
        scenario = {"required": list(contents), "support": {}}
        event = {"type": "item.completed", "item": {
            "id": "group", "type": "command_execution", "command": command,
            "status": "completed", "exit_code": 0,
            "aggregated_output": "first\nsecond\nthird",
        }}
        result = module.assess_reads([event], scenario, contents)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            [read["file"] for read in result["reads_in_order"]], list(contents)
        )
        event["item"]["aggregated_output"] = "first\nthird"
        result = module.assess_reads([event], scenario, contents)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["trace_issues"], ["TRACE_OUTPUT_MISMATCH: group"])


if __name__ == "__main__":
    unittest.main()
