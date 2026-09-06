"""Validate relocation integrity; does not execute model behavioral regressions."""
from pathlib import Path
import argparse
import hashlib
import json
import re
from urllib.parse import unquote
import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/ai-product-development"
MANIFEST = Path(__file__).with_name("migration-manifest.json")
NODES = [
    "Qualification", "Cognition", "Product Definition & Scope",
    "Solution Design", "Implementation", "Validation & Iteration",
    "Release & Operation", "Retrospective",
]
RUNTIME = ["Profile", "Planner", "Context", "Executor", "Registry", "Replan"]

def digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def norm(line):
    line = line.strip()
    if line.startswith("# "):
        line = line[2:]
    line = re.sub(r"^\*\*(Purpose|Capabilities|Primary outputs|Primary output|Completion):\*\*\s*", "", line)
    line = re.sub(r"^(?:[-*] |\d+\. )", "", line)
    return re.sub(r"\s+", " ", line).strip()

def anchors(text):
    result, counts, fenced = set(), {}, False
    for line in text.splitlines():
        if line.startswith(chr(96) * 3):
            fenced = not fenced
        if fenced:
            continue
        match = re.match(r"^#{1,6}\s+(.+)", line)
        if match:
            title = match.group(1).strip().lower().replace(chr(96), "")
            slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
            count = counts.get(slug, 0)
            counts[slug] = count + 1
            result.add(slug if not count else f"{slug}-{count}")
    return result

def validate(source=None):
    failures = []
    def check(ok, message):
        if not ok:
            failures.append(message)

    baseline = json.loads(MANIFEST.read_text(encoding="utf-8"))
    kernel = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    front = kernel.split("---", 2)[1]
    check(digest(front) == baseline["frontmatter_sha256"], "Frontmatter changed")
    parsed = yaml.safe_load(front)
    check(parsed.get("name") == "ai-product-development" and bool(parsed.get("description")), "Invalid activation metadata")
    lifecycle = kernel.split("## 2. Lifecycle", 1)[1].split("## 3. Runtime", 1)[0]
    check(re.findall(r"^\d+\. \x60(.+)\x60$", lifecycle, re.M) == NODES, "Lifecycle names/order changed")
    runtime = kernel.split("## 3. Runtime", 1)[1].split("## Global Invariants", 1)[0]
    check(re.findall(r"^- \x60([^\x60]+)\x60", runtime, re.M) == RUNTIME, "Runtime capability model changed")
    lifecycle_files = sorted((SKILL / "references/lifecycle").glob("*.md"))
    check(len(lifecycle_files) == 8, "Expected eight lifecycle references")
    check(len(list((SKILL / "references/runtime").glob("*.md"))) == 7, "Expected seven runtime responsibility references")
    headings = ["Purpose", "Activation Conditions", "Required Inputs", "Capabilities", "Procedure", "Outputs", "Completion Criteria", "Dependencies", "Load With", "Do Not"]
    for node, path in zip(NODES, lifecycle_files):
        text = path.read_text(encoding="utf-8")
        check(text.splitlines()[0] == "# " + node, f"Wrong node: {path.name}")
        check(all("## " + h in text for h in headings), f"Missing lifecycle section: {path.name}")

    md_files = list(SKILL.rglob("*.md")) + list(Path(__file__).parent.rglob("*.md"))
    md_files += [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "docs/architecture.md"]
    md_files += list((ROOT / "docs/decisions").glob("*.md"))
    links = 0
    for path in md_files:
        text = path.read_text(encoding="utf-8")
        for link in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in link or link.startswith("mailto:"):
                continue
            name, _, anchor = unquote(link).partition("#")
            target = (path.parent / name).resolve() if name else path
            check(target.is_relative_to(ROOT), f"Link outside repository: {path}: {link}")
            check(target.exists(), f"Missing link: {path}: {link}")
            if target.is_file() and anchor:
                check(anchor in anchors(target.read_text(encoding="utf-8")), f"Missing anchor: {path}: {link}")
            links += 1

    objects = {}
    schema_paths = sorted((SKILL / "schemas").glob("*.yaml"))
    check(len(schema_paths) == 5, "Expected five schema files")
    for path in schema_paths:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        for name, fields in value.items():
            check(name not in objects, f"Duplicate schema object: {name}")
            objects[name] = digest(json.dumps(fields, sort_keys=True, ensure_ascii=False))
    check(objects == baseline["schema_objects"], "Source schema fields/enums/values changed")

    by_path = {}
    for rule in baseline["rules"]:
        name = rule["canonical_file"]
        if name not in by_path:
            path = ROOT / name
            check(path.is_file(), f"Missing canonical file: {name}")
            by_path[name] = {digest(norm(line)) for line in path.read_text(encoding="utf-8").splitlines()} if path.is_file() else set()
        check(rule["canonical_sha256"] in by_path[name], f"Source line {rule['source_line']} lost from {name}")

    cases = {p.stem for p in Path(__file__).with_name("cases").glob("*.md")}
    expected = {p.stem for p in Path(__file__).with_name("expected").glob("*.md")}
    check(len(cases) == 8 and cases == expected, "Eight matching case/expected pairs required")
    if source:
        original = Path(source).read_text(encoding="utf-8-sig")
        check(digest(original) == baseline["source_sha256"], "Original source fingerprint mismatch")
        original_lines = original.splitlines()
        for rule in baseline["rules"]:
            check(digest(norm(original_lines[rule["source_line"] - 1])) == rule["source_sha256"], "Source line fingerprint mismatch")
    if failures:
        raise SystemExit("FAIL\n" + "\n".join(failures))
    print(f"PASS: {len(kernel.splitlines())} kernel lines, 8 lifecycle nodes, 6 runtime capabilities, {links} links.")
    print(f"PASS: {len(objects)} source schema objects; {len(baseline['rules'])} source lines retained or explicitly deduplicated.")
    print("PASS: 8 manual case/expected pairs. Behavioral execution: NOT RUN.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", help="Optional original SKILL.md for source fingerprint verification")
    args = parser.parse_args()
    validate(args.source)
