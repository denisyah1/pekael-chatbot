"""Block commits that contain secrets (NFR-01). Standard library only.

    python scripts/check_secrets.py          # scan lines added in staged changes (pre-commit hook)
    python scripts/check_secrets.py --all    # scan every tracked file
"""

import re
import subprocess
import sys

KEY_PATTERNS = {
    "OpenAI API key": re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    "Google API key": re.compile(r"AIza[0-9A-Za-z_-]{35}"),
    "Google auth token": re.compile(r"AQ\.[A-Za-z0-9_-]{20,}"),
}
SECRET_ASSIGNMENT = re.compile(r"^\s*(GEMINI_API_KEY|OPENAI_API_KEY|ADMIN_PASSWORD)\s*=\s*(\S+)")
PLACEHOLDER_PREFIX = "replace_with_"
ENV_FILE = re.compile(r"(^|/)\.env(\..+)?$")


def is_forbidden_file(path: str) -> bool:
    return bool(ENV_FILE.search(path)) and not path.endswith(".env.example")


def find_secrets(line: str) -> list[str]:
    """Return the kinds of secret found in one line of text."""
    found = [kind for kind, pattern in KEY_PATTERNS.items() if pattern.search(line)]
    match = SECRET_ASSIGNMENT.match(line)
    if match and not match.group(2).startswith(PLACEHOLDER_PREFIX):
        found.append(f"nilai {match.group(1)}")
    return found


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", check=True).stdout


def _staged_lines() -> list[tuple[str, int, str]]:
    lines, path, number = [], "", 0
    for raw in _git("diff", "--cached", "--unified=0", "--no-color").splitlines():
        if raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else ""
        elif raw.startswith("@@"):
            number = int(re.search(r"\+(\d+)", raw).group(1))
        elif raw.startswith("+") and path:
            lines.append((path, number, raw[1:]))
            number += 1
    return lines


def _tracked_lines() -> list[tuple[str, int, str]]:
    lines = []
    for path in _git("ls-files").splitlines():
        try:
            with open(path, encoding="utf-8") as handle:
                lines.extend((path, number, text) for number, text in enumerate(handle, start=1))
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    return lines


def main() -> int:
    scan_all = "--all" in sys.argv
    if scan_all:
        paths = _git("ls-files").splitlines()
    else:
        paths = _git("diff", "--cached", "--name-only", "--diff-filter=AM").splitlines()
    problems = [f"{path}: file .env tidak boleh di-commit" for path in paths if is_forbidden_file(path)]

    for path, number, text in _tracked_lines() if scan_all else _staged_lines():
        for kind in find_secrets(text):
            problems.append(f"{path}:{number}: kemungkinan {kind}")

    if problems:
        print("Commit diblokir - terdeteksi kemungkinan secret:")
        print("\n".join(f"  {p}" for p in problems))
        print("Pindahkan nilai asli ke .env (sudah di-ignore) dan pakai placeholder di file yang di-commit.")
        return 1
    print("Pemeriksaan secret: bersih.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
