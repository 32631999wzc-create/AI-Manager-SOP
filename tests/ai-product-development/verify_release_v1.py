from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import re
import subprocess

import yaml


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "docs/release-v1-manifest.yaml"
LOCAL_REPO_PATTERNS = ("D:\\\\GitHub\\\\AI-Manager-sop", "D:\\GitHub\\AI-Manager-sop")
CREDENTIAL = re.compile(
    r"(?i)(api[_-]?key\s*[:=]|authorization\s*[:=]|bearer\s+[A-Za-z0-9._-]{12,}|"
    r"BEGIN [A-Z ]*PRIVATE KEY)"
)


def tree_hash(directory: Path) -> tuple[int, str]:
    pairs = []
    files = sorted(path for path in directory.rglob("*") if path.is_file())
    for path in files:
        relative = path.relative_to(directory).as_posix()
        pairs.append(f"{relative}={sha256(path.read_bytes()).hexdigest()}")
    return len(files), sha256("\n".join(pairs).encode("utf-8")).hexdigest()


def git_paths(*args: str) -> set[str]:
    output = subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True, encoding="utf-8"
    )
    return {line.replace("\\", "/") for line in output.splitlines() if line.strip()}


def main() -> None:
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    adopted = manifest["evidence_policy"]["adopted_forward_evidence"]
    adopted_dirs = {item["path"] for item in adopted}
    assert adopted_dirs == set(manifest["commit_whitelist"]["adopted_evidence_directories"])

    for item in adopted:
        directory = ROOT / item["path"]
        assert directory.is_dir(), f"missing adopted evidence: {item['path']}"
        count, digest = tree_hash(directory)
        assert count == item["files"], f"file-count drift: {item['path']}"
        assert digest == item["tree_sha256"], f"evidence drift: {item['path']}"
        for path in directory.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            assert not any(value in text for value in LOCAL_REPO_PATTERNS), (
                f"local repository path in adopted evidence: {path.relative_to(ROOT)}"
            )
            assert not CREDENTIAL.search(text), f"credential pattern in adopted evidence: {path.relative_to(ROOT)}"

    whitelist = set(manifest["commit_whitelist"]["exact_files"])
    changed_tracked = git_paths("diff", "--name-only") | git_paths(
        "diff", "--cached", "--name-only"
    )
    untracked = git_paths("ls-files", "--others", "--exclude-standard")
    evidence_prefixes = tuple(path + "/" for path in adopted_dirs)
    missing = sorted(
        path for path in changed_tracked
        if path not in whitelist and not path.startswith(evidence_prefixes)
    )
    missing += sorted(
        path for path in untracked
        if "/evidence/" not in path and path not in whitelist
    )
    assert not missing, "release whitelist is missing changed files: " + ", ".join(missing)
    adopted_release_files = {
        path for path in (untracked | git_paths("ls-files"))
        if path.startswith(evidence_prefixes)
    }
    assert adopted_release_files, "no adopted forward evidence selected"
    print(
        f"PASS: {len(adopted)} adopted evidence directories, "
        f"{len(whitelist)} exact release files, no local-repository or credential indicators"
    )


if __name__ == "__main__":
    main()
