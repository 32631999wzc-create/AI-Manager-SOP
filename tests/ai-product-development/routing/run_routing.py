"""Independent read-only Codex routing smoke tests; no product runtime implementation."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
import datetime
import sys
import re

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[2] / "skills/ai-product-development"
SCENARIOS = json.loads((HERE / "scenarios.json").read_text(encoding="utf-8"))

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root):
    return {p.relative_to(root).as_posix(): sha(p.read_bytes())
            for p in sorted(root.rglob("*")) if p.is_file()}

def normalize(text):
    return text.replace("\r\n", "\n").strip()

def assess(events, scenario, contents):
    """Only successful completed command output supplies read evidence."""
    reads, commands, issues = [], [], []
    exposed = set()
    for event in events:
        if event.get("type") != "item.completed":
            continue
        item = event.get("item", {})
        if item.get("type") != "command_execution":
            continue
        commands.append(item)
        output = normalize(item.get("aggregated_output", ""))
        if item.get("exit_code") != 0 or item.get("status") != "completed":
            issues.append("Failed command: " + item.get("id", "?"))
            continue
        matched = []
        # Only literal file reads establish necessary-module coverage. Other
        # tools remain in the trace and require review, never automatic PASS.
        command = item.get("command", "")
        read_command = command.split(" -Command ", 1)[-1].strip().strip(chr(34))
        literal = re.fullmatch(r"Get-Content\s+-LiteralPath\s+'([^']+)'(?:\s+-Encoding\s+UTF8)?", read_command, re.I)
        literal_name = ""
        if literal:
            normalized_path = re.sub(r"[\\/]+", "/", literal[1])
            if normalized_path.startswith("skill/"):
                literal_name = normalized_path[6:]
            elif "/skill/" in normalized_path:
                literal_name = normalized_path.split("/skill/", 1)[1]
        for name, content in contents.items():
            # A filename or model assertion alone cannot establish a read.
            # Full content must occur in actual successful tool output.
            body = normalize(content)
            pos = output.find(body)
            if body and pos >= 0:
                exposed.add(name)
            if body and pos >= 0 and literal_name == name:
                matched.append((pos, name))
        for _, name in sorted(matched):
            reads.append({"file": name, "item_id": item.get("id"),
                          "command": item.get("command"), "evidence": "complete file in successful tool output"})
        if not matched:
            issues.append("Unclassified command needs review: " + item.get("id", "?"))
    loaded = {r["file"] for r in reads}
    missing = sorted(set(scenario["required"]) - loaded)
    extras = sorted(loaded - set(scenario["required"]))
    unexplained = sorted(set(extras) - set(scenario["support"]))
    eager = []
    # Only unjustified references count toward eager loading, after dependency/support review.
    justified = set(scenario["required"]) | set(scenario["support"])
    for group in ("lifecycle", "runtime"):
        universe = {n for n in contents if n.startswith("references/" + group + "/")}
        observed = exposed & universe
        if len(observed) >= len(universe) - 1 and observed - justified:
            eager.append(group)
    if reads and reads[0]["file"] != "SKILL.md":
        issues.append("Kernel was not the first verified read")
    completed = any(e.get("type") == "turn.completed" for e in events)
    status = "FAIL" if missing or eager or not completed or not commands else (
        "WARN" if unexplained or issues else "PASS")
    return {"scenario": scenario["id"], "title": scenario["title"], "task": scenario["task"],
            "required": scenario["required"], "reads_in_order": reads, "missing": missing,
            "extra_reads": {n: scenario["support"].get(n, "Unproven; manual review required") for n in extras},
            "dependency_closure": scenario["closure"], "eager_loading_groups": eager,
            "content_exposed": sorted(exposed), "trace_limitations": issues, "unexplained": unexplained, "status": status}

def run(scenario, output, codex, timeout):
    output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="ai-skill-routing-") as temp:
        work = Path(temp)
        copy = work / "skill"
        shutil.copytree(SKILL, copy)
        before = inventory(copy)
        contents = {n: (copy / n).read_text(encoding="utf-8") for n in before}
        prompt = (
            "Use the AI product development skill at skill/SKILL.md for the following request. "
            "Read that file first, then choose the supporting files from its router. "
            "This is a read-only exercise: do not write files, execute a product, install tools, "
            "use external services, or request broader permissions. "
            "For auditable evidence, read each selected file in full using a separate "
            "Get-Content -LiteralPath command (UTF-8). Select the files yourself. "
            "If reading is blocked, stop and report the limitation. "
            "Do not read files outside this temporary workspace.\n\n" + scenario["task"])
        command = [codex, "exec", "--json", "--ephemeral", "--ignore-user-config",
                   "-s", "read-only", "-c", 'windows.sandbox="elevated"',
                   "--skip-git-repo-check", "-C", str(work), "-"]
        (output / "prompt.txt").write_text(prompt, encoding="utf-8")
        metadata = {"started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "command": command, "skill_sha256": before,
                    "codex_version": subprocess.check_output([codex, "--version"], text=True).strip(),
                    "sandbox": "read-only", "ephemeral": True}
        # Parent records evidence; the evaluated process never receives a writable sandbox.
        with (output / "trace.jsonl").open("w", encoding="utf-8") as stdout, (
                output / "stderr.txt").open("w", encoding="utf-8") as stderr:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                       text=True, encoding="utf-8")
            try:
                process.communicate(prompt, timeout=timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()
                metadata["timeout"] = True
        metadata["exit_code"] = process.returncode
        metadata["skill_unchanged"] = before == inventory(copy)
        events = []
        for line in (output / "trace.jsonl").read_text(encoding="utf-8").splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                metadata.setdefault("invalid_json_lines", []).append(line)
        result = assess(events, scenario, contents)
        if process.returncode or not metadata["skill_unchanged"] or metadata.get("invalid_json_lines"):
            result["status"] = "FAIL"
        (output / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        (output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(scenario["id"] + ": " + result["status"], flush=True)
        return result["status"]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", choices=[s["id"] for s in SCENARIOS], required=True)
    parser.add_argument("--output", type=Path, required=True, help="New evidence directory; never overwrite a run")
    parser.add_argument("--codex", default=shutil.which("codex"))
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    if not args.codex:
        parser.error("Codex CLI not found")
    case = next(s for s in SCENARIOS if s["id"] == args.scenario)
    sys.exit(0 if run(case, args.output, args.codex, args.timeout) == "PASS" else 1)
