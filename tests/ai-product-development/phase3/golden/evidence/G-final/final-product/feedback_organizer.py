"""Deterministic feedback organizer used by the Phase 3 Golden MVP."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
from typing import Iterable


THEMES = {
    "reliability": ("crash", "error", "failed", "失败", "崩溃", "丢失"),
    "performance": ("slow", "latency", "卡", "慢", "延迟"),
    "usability": ("confusing", "hard to", "difficult", "难用", "找不到", "不清楚"),
    "billing": ("price", "billing", "refund", "价格", "付费", "退款"),
    "feature-request": ("please add", "wish", "feature", "希望", "建议", "能否"),
}
NEGATIVE = ("crash", "error", "failed", "slow", "confusing", "难用", "失败", "崩溃", "慢", "退款", "丢失")
POSITIVE = ("love", "great", "helpful", "喜欢", "很好", "有用")
URGENT = ("crash", "blocked", "data loss", "cannot use", "崩溃", "无法使用", "丢失")


def _normalized(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\u4e00-\u9fff]+", " ", text.casefold())).strip()


def _contains(text: str, words: Iterable[str]) -> bool:
    return any(word in text for word in words)


def load_feedback(path: Path) -> list[dict[str, str]]:
    if path.suffix.casefold() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON input must be a list")
        rows = data
    else:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
    result = []
    for index, row in enumerate(rows, 1):
        if not isinstance(row, dict) or not str(row.get("text", "")).strip():
            raise ValueError(f"feedback row {index} requires text")
        result.append({"id": str(row.get("id") or f"F{index}"), "source": str(row.get("source") or "unknown"), "text": str(row["text"]).strip()})
    return result


def organize(rows: list[dict[str, str]], source: str | None = None) -> dict:
    if source is not None:
        rows = [row for row in rows if row["source"] == source]
    unique: list[dict] = []
    duplicate_of: dict[str, str] = {}
    seen: dict[str, str] = {}
    for row in rows:
        normalized = _normalized(row["text"])
        if normalized in seen:
            duplicate_of[row["id"]] = seen[normalized]
            continue
        seen[normalized] = row["id"]
        matched = [name for name, words in THEMES.items() if _contains(normalized, words)]
        theme = matched[0] if matched else "other"
        sentiment = "negative" if _contains(normalized, NEGATIVE) else "positive" if _contains(normalized, POSITIVE) else "neutral"
        urgency = "high" if _contains(normalized, URGENT) else "normal"
        unique.append({**row, "theme": theme, "sentiment": sentiment, "urgency": urgency})

    themes = []
    for theme in sorted({item["theme"] for item in unique}):
        items = [item for item in unique if item["theme"] == theme]
        high = sum(item["urgency"] == "high" for item in items)
        negative = sum(item["sentiment"] == "negative" for item in items)
        themes.append({"theme": theme, "count": len(items), "priority_score": len(items) + high * 3 + negative, "evidence": [item["id"] for item in items]})
    themes.sort(key=lambda item: (-item["priority_score"], -item["count"], item["theme"]))
    return {"summary": {"received": len(rows), "unique": len(unique), "duplicates": len(duplicate_of)}, "themes": themes, "items": unique, "duplicates": duplicate_of}


def markdown_report(result: dict) -> str:
    summary = result["summary"]
    lines = ["# Feedback Insights", "", f"Received {summary['received']} feedback items; {summary['unique']} unique; {summary['duplicates']} duplicates.", "", "## Prioritized themes", "", "| Theme | Unique items | Priority score | Evidence |", "|---|---:|---:|---|"]
    for theme in result["themes"]:
        lines.append(f"| {theme['theme']} | {theme['count']} | {theme['priority_score']} | {', '.join(theme['evidence'])} |")
    lines.extend(["", "## Normalized feedback", ""])
    for item in result["items"]:
        lines.append(f"- **{item['id']}** [{item['source']}; {item['theme']}; {item['sentiment']}; {item['urgency']}] {item['text']}")
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--source", help="only include feedback from this source")
    args = parser.parse_args(argv)
    result = organize(load_feedback(Path(args.input)), source=args.source)
    Path(args.json_output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    Path(args.markdown_output).write_text(markdown_report(result), encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
