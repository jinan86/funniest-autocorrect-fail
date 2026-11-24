#!/usr/bin/env python3
"""Funniest Autocorrect Fail -- make.fun entry.

Writes one single-line autocorrect fail to /output/entry.txt
(or $OUTPUT_DIR/entry.txt when set, for local testing).
Deterministic, no network, reads no file outside this repo.
"""

import os
import sys

ENTRY = "Hi boss, can we move the mating to 3pm? I have a conflict at 2."


def main() -> int:
    text = ENTRY

    # Internal validation: the gate requires UTF-8 text of 1-199
    # characters, not only whitespace, exactly one line.
    if not 1 <= len(text) <= 199:
        print(f"entry length {len(text)} outside 1-199", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    try:
        data = text.encode("utf-8")
    except UnicodeEncodeError as exc:
        print(f"entry is not valid UTF-8: {exc}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as fh:
        fh.write(data)  # no trailing newline
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
