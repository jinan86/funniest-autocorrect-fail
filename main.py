#!/usr/bin/env python3
"""Funniest Autocorrect Fail -- make.fun entry.

Writes a single-line autocorrect fail to ``/output/entry.txt``
(or ``$OUTPUT_DIR/entry.txt`` when set, for local testing).

Deterministic: no network access, no files read outside this repo,
no secrets, no randomness. The output is always the same bytes.
"""

import os
import sys
from pathlib import Path

# The entry: a text to the boss where autocorrect turns "meeting"
# into "mating". Exactly 63 characters, one line, no trailing newline.
ENTRY = "Hi boss, can we move the mating to 3pm? I have a conflict at 2."

MAX_ENTRY_CHARS = 199


def build_entry() -> str:
    """Return the entry text exactly as submitted."""
    return ENTRY


def validate(text: str) -> str | None:
    """Check the entry against the competition's output gate.

    Returns an error message when the text is invalid, else ``None``.
    """
    if not 1 <= len(text) <= MAX_ENTRY_CHARS:
        return f"entry length {len(text)} outside 1-{MAX_ENTRY_CHARS}"
    if not text.strip():
        return "entry is only whitespace"
    if text != text.strip():
        return "entry must not start or end with whitespace"
    if "\n" in text or "\r" in text:
        return "entry must be a single line"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        return f"entry is not valid UTF-8: {exc}"
    return None


def output_path() -> Path:
    """Resolve the output file path (``/output/entry.txt`` by default)."""
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    return Path(out_dir) / "entry.txt"


def main() -> int:
    text = build_entry()

    error = validate(text)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))  # no trailing newline
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
