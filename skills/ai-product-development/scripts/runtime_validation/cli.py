"""Command line entry point for read-only runtime validation."""

import argparse
import json
import sys

from .loader import DocumentLoadError, load_document
from .validators import validate_document


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("objects", "profile", "plan", "combined"))
    parser.add_argument("document")
    args = parser.parse_args(argv)
    try:
        document = load_document(args.document)
    except DocumentLoadError as exc:
        print(json.dumps({"valid": False, "errors": [{"code": "DOCUMENT_INVALID", "path": "$", "message": str(exc)}]}, ensure_ascii=False))
        return 2
    errors = validate_document(document, args.mode)
    print(json.dumps({"valid": not errors, "errors": [error.as_dict() for error in errors]}, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
