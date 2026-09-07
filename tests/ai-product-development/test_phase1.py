"""Focused negative tests for structure and trace evidence; not product behavior."""
from pathlib import Path
import copy
import importlib.util
import shutil
import tempfile
import unittest

from structure_contract import inspect_contract
from validate_structure import NODES, SKILL

spec = importlib.util.spec_from_file_location("routing", Path(__file__).parent / "routing/run_routing.py")
routing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(routing)

class StructureContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="phase1-contract-")
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "skill"
        shutil.copytree(SKILL, self.skill)
        self.kernel = (self.skill / "SKILL.md").read_text(encoding="utf-8")

    def errors(self, kernel=None):
        errors = []
        inspect_contract(self.skill, self.kernel if kernel is None else kernel, NODES,
                         lambda ok, msg: errors.append(msg) if not ok else None)
        return errors

    def test_valid(self):
        self.assertEqual(self.errors(), [])

    def test_wrong_module_name_same_count(self):
        p = self.skill / "references/runtime/context.md"
        p.rename(p.with_name("wrong.md"))
        self.assertTrue(self.errors())

    def test_swapped_valid_routes(self):
        text = self.kernel.replace("references/lifecycle/01-qualification.md", "SWAP")
        text = text.replace("references/lifecycle/02-cognition.md", "references/lifecycle/01-qualification.md")
        text = text.replace("SWAP", "references/lifecycle/02-cognition.md")
        self.assertTrue(self.errors(text))

    def test_missing_kernel_section(self):
        self.assertTrue(self.errors(self.kernel.replace("## Rule Precedence", "## Precedence")))

    def test_new_gate(self):
        p = self.skill / "references/runtime/gates.md"
        p.write_text(p.read_text(encoding="utf-8")+"\n## Fourth Gate\n", encoding="utf-8")
        self.assertTrue(self.errors())

    def test_copied_detailed_rule(self):
        source = (self.skill / "references/runtime/executor.md").read_text(encoding="utf-8")
        p = self.skill / "references/runtime/context.md"
        p.write_text(p.read_text(encoding="utf-8")+"\n"+source, encoding="utf-8")
        self.assertTrue(any("Duplicate detail" in e for e in self.errors()))

class TraceEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.contents = {"SKILL.md": "# kernel content"}
        for group, count in (("lifecycle", 8), ("runtime", 7)):
            self.contents.update({f"references/{group}/{i}.md": f"# {group} module {i} full content" for i in range(count)})
        self.case = {"id":"test", "title":"test", "task":"test",
                     "required":["SKILL.md", "references/lifecycle/0.md"],
                     "support":{}, "closure":"none"}

    def events(self, files):
        return [{"type":"item.completed","item":{"id":str(i),"type":"command_execution",
                 "command":f"Get-Content -LiteralPath 'skill/{name}' -Encoding UTF8",
                 "status":"completed","exit_code":0,"aggregated_output":self.contents[name]}}
                for i, name in enumerate(files)] + [{"type":"turn.completed"}]

    def grade(self, events, case=None):
        return routing.assess(events, case or self.case, self.contents)["status"]

    def test_real_reads_pass(self):
        self.assertEqual(self.grade(self.events(self.case["required"])), "PASS")

    def test_self_report_is_not_evidence(self):
        e=[{"type":"item.completed","item":{"type":"agent_message","text":"Read all required files, PASS"}},
           {"type":"turn.completed"}]
        self.assertEqual(self.grade(e), "FAIL")

    def test_missing_required_fails(self):
        self.assertEqual(self.grade(self.events(["SKILL.md"])), "FAIL")

    def test_failed_tool_does_not_count(self):
        e=self.events(self.case["required"]);e[1]["item"]["exit_code"]=1
        self.assertEqual(self.grade(e), "FAIL")

    def test_truncated_output_does_not_count(self):
        e=self.events(self.case["required"]);e[1]["item"]["aggregated_output"]="# truncated"
        self.assertEqual(self.grade(e), "FAIL")

    def test_listing_is_not_read(self):
        e=self.events(self.case["required"]);e[1]["item"]["command"]="rg --files skill"
        self.assertEqual(self.grade(e), "FAIL")

    def test_absolute_windows_paths(self):
        e=self.events(self.case["required"])
        for event in e[:-1]:
            item=event["item"]
            item["command"]='"pwsh.exe" -Command "'+item["command"].replace("skill/", "C:/Temp/isolation/skill/")+'"'
        self.assertEqual(self.grade(e), "PASS")

    def test_echoed_read_command_is_not_evidence(self):
        e=self.events(self.case["required"])
        e[1]["item"]["command"]="echo " + e[1]["item"]["command"]
        self.assertEqual(self.grade(e), "FAIL")

    def test_unexplained_extra_warns(self):
        self.assertEqual(self.grade(self.events(self.case["required"]+["references/runtime/1.md"])), "WARN")

    def test_supported_extra_passes(self):
        case=copy.deepcopy(self.case);case["support"]["references/runtime/1.md"]="local dependency check"
        self.assertEqual(self.grade(self.events(case["required"]+["references/runtime/1.md"]),case), "PASS")

    def test_eager_loading_fails(self):
        all_nodes=["SKILL.md"]+[f"references/lifecycle/{i}.md" for i in range(8)]
        self.assertEqual(self.grade(self.events(all_nodes)), "FAIL")

    def test_bulk_output_cannot_hide_behind_unrecognized_command(self):
        e=self.events(self.case["required"])
        e.insert(-1, {"type":"item.completed", "item":{
            "id":"bulk", "type":"command_execution", "status":"completed", "exit_code":0,
            "command":"Get-Content skill/references/lifecycle/*.md",
            "aggregated_output":"\n".join(v for n,v in self.contents.items() if "lifecycle" in n)}})
        self.assertEqual(self.grade(e), "FAIL")

    def test_legitimate_closure_is_not_eager(self):
        case=copy.deepcopy(self.case)
        all_nodes=["SKILL.md"]+[f"references/lifecycle/{i}.md" for i in range(8)]
        case["required"]=all_nodes
        case["closure"]="Synthetic full-lifecycle task requires all nodes"
        self.assertEqual(self.grade(self.events(all_nodes),case), "PASS")

if __name__ == "__main__":
    unittest.main()
