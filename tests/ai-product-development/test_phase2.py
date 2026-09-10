"""Executable Phase 2 validation and fixture regression tests."""

from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
import importlib.util
import json
import re
import sys
import unittest

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCRIPTS = REPO / "skills/ai-product-development/scripts"
sys.path.insert(0, str(SCRIPTS))

from runtime_validation.cli import main as cli_main
from runtime_validation.validators import validate_document

FIXTURES = HERE / "phase2/fixtures"
SCENARIOS = FIXTURES / "scenarios"
EXPECTED = FIXTURES / "expected"


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def select(document, path):
    current = document
    for name, index in re.findall(r"([^.\[\]]+)(?:\[(\d+)\])?", path):
        current = current[name]
        if index:
            current = current[int(index)]
    return current


def parent_and_key(document, path):
    parts = re.findall(r"([^.\[\]]+)(?:\[(\d+)\])?", path)
    current = document
    for name, index in parts[:-1]:
        current = current[name]
        if index:
            current = current[int(index)]
    name, index = parts[-1]
    return current, name, int(index) if index else None


def apply_operation(document, operation):
    parent, name, index = parent_and_key(document, operation["path"])
    target = parent[name]
    if operation["op"] == "set":
        if index is None:
            parent[name] = operation["value"]
        else:
            target[index] = operation["value"]
    elif operation["op"] == "append":
        target.append(operation["value"])
    elif operation["op"] == "delete":
        if index is None:
            del parent[name]
        else:
            del target[index]
    else:
        raise AssertionError("unknown fixture operation")


class RuntimeObjectTests(unittest.TestCase):
    def test_all_eight_objects_parse(self):
        document = load(FIXTURES / "objects.yaml")
        self.assertEqual(validate_document(document, "objects"), [])
        self.assertEqual(len(document), 8)

    def test_missing_unknown_enum_and_version_are_distinct(self):
        document = load(FIXTURES / "objects.yaml")
        del document["Task"]["goal"]
        document["NodeProfile"]["level"] = "DEEP"
        document["Artifact"]["extra"] = True
        document["Artifact"]["version"] = "1"
        codes = {error.code for error in validate_document(document, "objects")}
        self.assertTrue({"FIELD_MISSING", "FIELD_UNKNOWN", "ENUM_INVALID", "VERSION_INVALID"} <= codes)


class ScenarioRegressionTests(unittest.TestCase):
    def test_eight_positive_scenarios(self):
        scenario_files = sorted(SCENARIOS.glob("*.yaml"))
        self.assertEqual(len(scenario_files), 8)
        for path in scenario_files:
            with self.subTest(path=path.name):
                document = load(path)
                expected = json.loads((EXPECTED / (path.stem + ".json")).read_text(encoding="utf-8"))
                errors = validate_document(document, "combined")
                self.assertEqual(errors, [])
                self.assertTrue(expected["valid"])
                self.assertEqual(document["profile"]["delivery_target"], expected["delivery_target"])
                self.assertEqual(document["profile"]["assignment_scope"]["mode"], expected["scope_mode"])
                self.assertEqual({item["node"]: item["level"] for item in document["profile"]["nodes"]}, expected["node_levels"])

    def test_fixed_negative_matrix(self):
        cases = json.loads((FIXTURES / "negative-cases.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 20)
        for case in cases:
            with self.subTest(case=case["id"]):
                combined = load(SCENARIOS / (case["base"] + ".yaml"))
                document = deepcopy(combined[case["mode"]])
                for operation in case["operations"]:
                    apply_operation(document, operation)
                codes = {error.code for error in validate_document(document, case["mode"])}
                self.assertIn(case["expected_code"], codes)

    def test_validation_is_deterministic_and_read_only(self):
        path = SCENARIOS / "06-enterprise-release.yaml"
        before = path.read_bytes()
        document = load(path)
        first = [error.as_dict() for error in validate_document(document, "combined")]
        second = [error.as_dict() for error in validate_document(deepcopy(document), "combined")]
        self.assertEqual(first, second)
        self.assertEqual(path.read_bytes(), before)


class MalformedInputTests(unittest.TestCase):
    def test_nested_non_mapping_returns_stable_error(self):
        self.assertEqual(validate_document({"profile": [], "plan": {}}, "combined")[0].code, "TYPE_MAPPING")

    def test_non_string_list_entries_do_not_raise(self):
        document = load(SCENARIOS / "01-greenfield-prototype.yaml")["plan"]
        document["available_inputs"] = [{"invalid": True}]
        document["write_targets"]["T1"] = [{"invalid": True}]
        errors = validate_document(document, "plan")
        self.assertIn("TYPE_LIST", {error.code for error in errors})

    def test_optional_design_does_not_satisfy_implementation_floor(self):
        profile = load(SCENARIOS / "01-greenfield-prototype.yaml")["profile"]
        profile["nodes"][3]["level"] = "OPTIONAL"
        codes = {error.code for error in validate_document(profile, "profile")}
        self.assertIn("PROFILE_DESIGN_REQUIRED", codes)

    def test_verify_depth_does_not_define_missing_acceptance_criteria(self):
        profile = load(SCENARIOS / "01-greenfield-prototype.yaml")["profile"]
        profile["validation_context"]["acceptance_criteria_defined"] = False
        profile["nodes"][3]["depth"] = "VERIFY"
        profile["nodes"][3]["active_capabilities"] = ["Evaluation Design"]
        codes = {error.code for error in validate_document(profile, "profile")}
        self.assertIn("PROFILE_EVALUATION_DESIGN_REQUIRED", codes)

    def test_evaluation_design_components_satisfy_capability(self):
        profile = load(SCENARIOS / "04-rag-evaluation-only.yaml")["profile"]
        profile["nodes"][3]["active_capabilities"] = [
            "evaluation task", "cases / dataset", "metrics", "judge strategy", "pass criteria",
        ]
        self.assertEqual(validate_document(profile, "profile"), [])

    def test_chinese_canonical_capability_names_are_supported(self):
        profile = load(SCENARIOS / "04-rag-evaluation-only.yaml")["profile"]
        profile["nodes"][3]["active_capabilities"] = ["评估设计"]
        self.assertEqual(validate_document(profile, "profile"), [])

        release = load(SCENARIOS / "06-enterprise-release.yaml")["profile"]
        release["nodes"][6]["gaps"] = ["发布前补齐生产监控"]
        release["nodes"][6]["active_capabilities"] = []
        self.assertEqual(validate_document(release, "profile"), [])


class ContractAndCliTests(unittest.TestCase):
    def test_contract_sources_exist_and_codes_are_unique(self):
        contract = load(HERE / "phase2/validation-contract.yaml")["rules"]
        codes = [item["code"] for item in contract]
        self.assertEqual(len(codes), len(set(codes)))
        validator_source = (SCRIPTS / "runtime_validation/validators.py").read_text(encoding="utf-8")
        cli_source = (SCRIPTS / "runtime_validation/cli.py").read_text(encoding="utf-8")
        emitted = set(re.findall(r"(?:code=|_error\(errors, )[\"' ]*([A-Z_]+)", validator_source + cli_source))
        self.assertTrue(emitted <= set(codes), sorted(emitted - set(codes)))
        for item in contract:
            source = item["source"].split("#", 1)[0]
            if "*" not in source:
                self.assertTrue((REPO / source).is_file(), item["source"])

    def test_cli_success_and_validation_failure_exit_codes(self):
        good = str(SCENARIOS / "01-greenfield-prototype.yaml")
        with redirect_stdout(StringIO()) as output:
            self.assertEqual(cli_main(["combined", good]), 0)
        self.assertTrue(json.loads(output.getvalue())["valid"])

        bad_path = FIXTURES / "invalid-root.yaml"
        try:
            bad_path.write_text("- not-a-mapping\n", encoding="utf-8")
            with redirect_stdout(StringIO()) as output:
                self.assertEqual(cli_main(["combined", str(bad_path)]), 2)
            result = json.loads(output.getvalue())
            self.assertEqual(result["errors"][0]["code"], "DOCUMENT_INVALID")
        finally:
            bad_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
