"""CLI for the repository-local continuous product runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from runtime_validation.loader import DocumentLoadError, load_document

from .service import ProjectRuntime, RuntimeFailure


def _document(path: str, root: str | Path) -> dict:
    source = Path(path)
    if not source.is_absolute():
        source = Path(root) / source
    try:
        return load_document(source)
    except DocumentLoadError as exc:
        raise RuntimeFailure("DOCUMENT_INVALID", str(exc)) from exc


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="product repository root")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--input", required=True)
    init.add_argument("--project-id", required=True)
    commands.add_parser("validate")
    commands.add_parser("status")
    commands.add_parser("complete")
    commands.add_parser("next")
    checkpoint = commands.add_parser("checkpoint", aliases=["save"])
    checkpoint.add_argument("--unresolved", action="append", default=[])
    commands.add_parser("resume")
    profile = commands.add_parser("update-profile")
    profile.add_argument("--input", required=True)
    task = commands.add_parser("task")
    task.add_argument("--id", required=True)
    task.add_argument("--status", required=True)
    task.add_argument("--validation-pass", action="store_true")
    record = commands.add_parser("register-record")
    record.add_argument("--input", required=True)
    artifact = commands.add_parser("commit-artifact")
    artifact.add_argument("--input", required=True)
    artifact.add_argument("--validation-pass", action="store_true")
    replan = commands.add_parser("replan")
    replan.add_argument("--input", required=True)
    args = parser.parse_args(argv)
    runtime = ProjectRuntime(Path(args.root))
    try:
        if args.command == "init":
            result = runtime.init(_document(args.input, args.root), args.project_id)
        elif args.command == "validate":
            result = runtime.validate()
        elif args.command == "status":
            result = runtime.status()
        elif args.command == "complete":
            result = runtime.complete()
        elif args.command == "next":
            result = runtime.next()
        elif args.command in {"checkpoint", "save"}:
            result = runtime.checkpoint(args.unresolved)
        elif args.command == "resume":
            result = runtime.resume()
        elif args.command == "update-profile":
            result = runtime.update_profile(_document(args.input, args.root))
        elif args.command == "task":
            result = runtime.update_task(args.id, args.status, args.validation_pass)
        elif args.command == "register-record":
            result = runtime.register_record(_document(args.input, args.root))
        elif args.command == "commit-artifact":
            result = runtime.commit_artifact(_document(args.input, args.root), args.validation_pass)
        else:
            result = runtime.replan(_document(args.input, args.root))
    except RuntimeFailure as exc:
        print(json.dumps({"ok": False, "error": {"code": exc.code, "message": str(exc)}}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"ok": True, "result": result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
