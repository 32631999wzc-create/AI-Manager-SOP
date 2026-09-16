"""Phase 1 structural contracts only; no domain-object instance validation."""
from pathlib import Path
import re
from collections import defaultdict

LIFECYCLE = [
    "01-qualification.md", "02-cognition.md", "03-product-definition.md",
    "04-solution-design.md", "05-implementation.md", "06-validation-iteration.md",
    "07-release-operation.md", "08-retrospective.md",
]
RUNTIME = ["execution-profile.md", "planner.md", "context.md", "executor.md",
           "registry-versioning.md", "replan-recovery.md", "gates.md"]
CAPABILITIES = [
    "discovery", "competitive-intelligence", "business-case", "roadmap",
    "product-requirements", "requirement-review", "ai-feasibility", "data-strategy",
    "human-ai-experience", "evaluation", "responsible-ai", "delivery",
    "experimentation", "launch", "production-learning", "retrospective",
]
CAPABILITY_CONTRACT = [
    "Purpose", "When to use", "When NOT to use", "Decision / Unknown",
    "Required Inputs", "Method", "Evidence Rules", "Decision Rules",
    "Output Contract", "Handoff", "Completion Criteria", "Boundaries",
]
LIFECYCLE_CONTRACT = [
    "Purpose", "Activation Conditions", "Required Inputs", "Required Decisions / State",
    "Capability Routing", "Outputs", "Completion Criteria", "Dependencies", "Boundaries",
]
PLACEHOLDER_MARKERS = ["原文未单列固定输入", "原文未规定独立固定输出", "原文未单列节点完成"]
SCHEMAS = [
    "task.yaml", "project-state.yaml", "evidence-record.yaml", "decision-record.yaml",
    "execution-profile.yaml", "plan.yaml", "context-pack.yaml",
]
KERNEL_SECTIONS = [
    "1. Operating Principles", "2. Lifecycle", "3. Runtime", "Global Invariants",
    "Progressive Disclosure Router", "Lifecycle Routing", "Runtime Routing",
    "Data and Output Routing", "Rule Precedence", "14. Complexity Guardrails",
    "15. User-Facing Execution Style", "16. End-to-End Procedure", "17. Completion Criteria",
]
RUNTIME_OPERATIONS = [
    "判断交付目标、范围、资产、深度、风险与依赖闭包，或 Profile Replan",
    "从缺口规划、拆任务、排依赖、并行或优先级，检查计划",
    "检索项目状态、组装或裁剪任务上下文", "选择 Worker、执行、验证或局部重试",
    "判断正式产物状态、写入项目记录、提交正式产物或更新版本", "实质变更、不可重试失败或恢复执行",
    "判断 Qualification / Build / Release Gate",
]

def inspect_contract(skill, kernel, nodes, check):
    headings = re.findall(r"^#{1,6} (.+)$", kernel, re.M)
    for heading in KERNEL_SECTIONS:
        check(headings.count(heading) == 1, "Missing/duplicate Kernel section: " + heading)
    for folder, expected in [
            ("references/lifecycle", LIFECYCLE), ("references/runtime", RUNTIME),
            ("schemas", SCHEMAS), ("templates", ["execution-plan.md"])]:
        actual = {p.name for p in (skill / folder).iterdir() if p.is_file()}
        check(actual == set(expected), "Wrong module inventory: " + folder)
    actual_capabilities = {
        p.name for p in (skill / "references/capabilities").iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file()
    }
    check(actual_capabilities == set(CAPABILITIES), "Wrong module inventory: references/capabilities")

    rows = re.findall(r"^\| (.*?) \| \[[^\]]+\]\(([^)]+)\) \|$", kernel, re.M)
    for label, name in zip(nodes, LIFECYCLE):
        check(rows.count((label, "references/lifecycle/" + name)) == 1, "Wrong lifecycle route: " + label)
    for label, name in zip(RUNTIME_OPERATIONS, RUNTIME):
        check(rows.count((label, "references/runtime/" + name)) == 1, "Wrong runtime route: " + label)
    for name in SCHEMAS:
        check(sum(target == "schemas/" + name for _, target in rows) == 1, "Wrong schema route: " + name)
    check(sum(target == "templates/execution-plan.md" for _, target in rows) == 1, "Missing template route")

    for name in LIFECYCLE:
        path = skill / "references/lifecycle" / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        headings = re.findall(r"^## (.+)$", text, re.M)
        check(headings == LIFECYCLE_CONTRACT, "Wrong lifecycle contract/order: " + name)
        for heading in LIFECYCLE_CONTRACT:
            match = re.search(
                rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text, re.M | re.S
            )
            check(bool(match and match.group(1).strip()),
                  f"Empty lifecycle contract section: {name}#{heading}")
        for marker in PLACEHOLDER_MARKERS:
            check(marker not in text, f"Lifecycle placeholder remains: {name}: {marker}")

    capability_rows = re.findall(
        r"^\| .*? \| .*? \| \[[^\]]+\]\(references/capabilities/([^/]+)/SKILL\.md\) \|$",
        kernel, re.M,
    )
    check(capability_rows == CAPABILITIES, "Wrong capability playbook routes/order")
    for name in CAPABILITIES:
        path = skill / "references/capabilities" / name / "SKILL.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        headings = re.findall(r"^## (.+)$", text, re.M)
        check(headings == CAPABILITY_CONTRACT, "Wrong capability contract/order: " + name)
        for heading in CAPABILITY_CONTRACT:
            match = re.search(
                rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text, re.M | re.S
            )
            check(bool(match and match.group(1).strip()),
                  f"Empty capability contract section: {name}#{heading}")

    lifecycle_text = "\n".join(
        (skill / "references/lifecycle" / name).read_text(encoding="utf-8")
        for name in LIFECYCLE if (skill / "references/lifecycle" / name).exists()
    )
    for name in CAPABILITIES:
        check(f"../capabilities/{name}/SKILL.md" in lifecycle_text,
              "Capability not reachable from lifecycle: " + name)

    gate = skill / "references/runtime/gates.md"
    if gate.exists():
        check(re.findall(r"^## (.+)$", gate.read_text(encoding="utf-8"), re.M) ==
              ["Qualification Gate", "Build Readiness", "Release Readiness"], "Top-level Gates changed")

    # Long identical detail lines / multi-line detail paragraphs are suspicious.
    # Navigation, headings and short shared lifecycle scaffolding are not detailed rules.
    seen = defaultdict(set)
    for path in sorted((skill / "references").rglob("*.md")):
        if "examples" in path.parts or "templates" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for block in text.split("\n\n"):
            lines = [line.strip() for line in block.splitlines() if line.strip()]
            if not lines or any(line.startswith("#") or re.search(r"\[[^]]+\]\(", line) for line in lines):
                continue
            tokens = [line for line in lines if len(line) >= 90 and not line.startswith("|")]
            if len(lines) >= 2 and len(" ".join(lines)) >= 120:
                tokens.append(" ".join(lines))
            for token in tokens:
                seen[token].add(path.relative_to(skill).as_posix())
    for token, paths in seen.items():
        check(len(paths) == 1, "Duplicate detail: " + ", ".join(sorted(paths)) + ": " + token[:90])
