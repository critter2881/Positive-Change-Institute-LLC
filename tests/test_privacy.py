"""Guard: a protected personal surname must not appear in published files.

Only a SHA-256 hash of the lowercase word is stored, so this test does not
itself reveal the name. To protect another name, add the hash of the
lowercase word to _BLOCKED_HASHES.
"""

import hashlib
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_BLOCKED_HASHES = {
    "6a83384e3d1a13d74bd8c0fc699a403fe0b1b264a050b21fdbed90da09e53ac9",
}
_SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}


def _blocked(text: str) -> bool:
    for word in set(re.findall(r"[a-z]+", text.lower())):
        if hashlib.sha256(word.encode()).hexdigest() in _BLOCKED_HASHES:
            return True
    return False


def test_no_protected_name_in_published_files():
    hits = []
    for path in _ROOT.rglob("*"):
        if not path.is_file() or _SKIP_DIRS & set(path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if _blocked(text):
            hits.append(str(path.relative_to(_ROOT)))
    assert not hits, f"Protected name found in: {sorted(hits)}"


def test_detector_catches_name():
    assert _blocked("Founded by Mr. " + "Row" + "land Sr.")
    assert not _blocked("Founded by the Founder")
