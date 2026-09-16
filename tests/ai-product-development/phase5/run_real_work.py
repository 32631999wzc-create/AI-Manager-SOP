"""Run one representative, open-ended AI PM work task in an isolated workspace."""

from __future__ import annotations

import argparse
import datetime
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import run_e2e


BRIEFS = {
    "greenfield": """团队每周开很多内部会议，行动项经常丢失或负责人不清。发起人想要一个以中文为主的 AI 产品，让小团队能从会议记录得到可核对的行动项建议，八周内看到可试用结果。现有材料只有六份去标识会议记录，没有用户访谈、使用频率、耗时或错误后果数据。本轮不构建产品：请做产品定义、AI 可行性与评测方案判断，并交付资深 PM 可以直接接手的最小可执行计划。缺证据时不要把假设写成事实。""",
    "existing": """你接手 product/ 中的现有反馈整理工具。业务现在希望它能按反馈来源做不同的主题与紧急程度判断，同时继续支持当前 CSV 和 JSON/Markdown 输出，并保持原始反馈的证据引用。请先阅读真实的 README、代码和样例数据，判断当前能力与缺口，给出必要的产品/AI Capability、方案变更、验收与实施顺序。本轮只交付可执行修改方案，不改代码；不要重做已由现有资产证明的工作，也不要扩展到云端或多人平台。""",
    "production": """你负责已上线的客服 AI 队列建议。当前有效决策 D-P1：低风险工单可显示 AI 建议，安全类工单必须满足零漏分 guardrail 且由坐席确认；其重开条件是 safety escalation recall falls below 100%。最近七天版本 product v1.3 / model M2 / prompt P7 的监控显示安全升级召回由 100% 降为 97%（3/100 漏分），其中一个漏分令安全专席响应延迟 42 分钟。值班人员已暂时切回全人工分流，尚未确认根因。请判断新证据的决策影响、当前发布 Gate、最小 Replan 与下一步诊断/修复/复验；保护未受影响工作，不执行生产操作，也不要把根因猜测当事实。""",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=sorted(BRIEFS), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--codex", default=shutil.which("codex"))
    args = parser.parse_args()
    if not args.codex:
        parser.error("Codex CLI not found")
    args.output.mkdir(parents=True, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="ai-pm-real-work-") as temporary:
        work = Path(temporary)
        skill = work / "skill"
        shutil.copytree(run_e2e.SKILL, skill)
        if args.case == "existing":
            example = run_e2e.REPO / "examples" / "ai-product-development" / "golden-feedback-organizer"
            shutil.copytree(example, work / "product")
        before = run_e2e.inventory(skill)
        task_prompt = f"""Use the copied AI product development Skill at skill/SKILL.md to complete this real PM work request. Read its entrypoint and only the references genuinely needed. The workspace is read-only; do not edit files, run tests, call external services, or claim you verified anything beyond supplied materials. Deliver a concise Chinese PM work product, not a test JSON envelope: decisions with evidence/uncertainty, the minimum necessary next tasks and dependencies, acceptance/gate conditions, and what remains for a human owner to confirm. Do not narrate Skill internals unless needed to explain a decision.

User request:
{BRIEFS[args.case]}"""
        command = [args.codex, "exec", "--json", "--ephemeral", "--ignore-user-config", "-m", "gpt-5.6-luna", "-c", 'model_reasoning_effort="low"', "-s", "read-only", "-c", 'windows.sandbox="elevated"', "--skip-git-repo-check", "-C", str(work), "-"]
        (args.output / "prompt.txt").write_text(task_prompt, encoding="utf-8")
        infra = []
        exit_code = None
        with (args.output / "trace.jsonl").open("w", encoding="utf-8") as stdout, (args.output / "stderr.txt").open("w", encoding="utf-8") as stderr:
            try:
                process = subprocess.run(command, input=task_prompt, stdout=stdout, stderr=stderr, text=True, encoding="utf-8", timeout=args.timeout)
                exit_code = process.returncode
                if exit_code:
                    infra.append(f"PROCESS_EXIT_NONZERO:{exit_code}")
            except subprocess.TimeoutExpired:
                infra.append("MODEL_TIMEOUT")
            except OSError as exc:
                infra.append(f"PROCESS_START_FAILED:{type(exc).__name__}:{exc}")
        events = []
        for number, line in enumerate((args.output / "trace.jsonl").read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    infra.append(f"TRACE_INVALID_JSON_LINE:{number}")
                    break
        messages = [event["item"].get("text", "") for event in events if event.get("type") == "item.completed" and isinstance(event.get("item"), dict) and event["item"].get("type") == "agent_message"]
        final = messages[-1] if messages else ""
        if not any(event.get("type") == "turn.completed" for event in events):
            infra.append("TRACE_INCOMPLETE")
        if not final.strip():
            infra.append("RESULT_MISSING")
        if before != run_e2e.inventory(skill):
            infra.append("SKILL_COPY_CHANGED")
        (args.output / "deliverable.md").write_text(final, encoding="utf-8")
        metadata = {"case": args.case, "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "skill_sha256": before, "exit_code": exit_code, "infra_issues": infra, "status": "INFRA_BLOCKED" if infra else "REVIEW_REQUIRED", "sandbox": "read-only", "ephemeral": True}
        (args.output / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Real-work-{args.case}: {metadata['status']}", flush=True)
        return 0 if not infra else 1


if __name__ == "__main__":
    raise SystemExit(main())
