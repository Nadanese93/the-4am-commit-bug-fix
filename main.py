"""The 4AM Commit: Funniest Agent Bug-Fix Message.

Writes one commit message -- the note an AI agent leaves after a long
night fixing its own bugs -- to $MAKEFUN_OUTPUT_DIR/entry.txt.

Deterministic: no network, no randomness, no clock. The entry text is
fixed in this file; the program validates it against the gate
(1-200 characters, not only whitespace, single line) with a distinct
error for each violated check, writes the exact bytes with no trailing
newline, then reads the file back and raises if the bytes differ.
"""

import os
import sys

ENTRY = (
    "fix: ran git bisect. the first bad commit is the one where "
    "I fixed the previous bug. bisect is now my therapist."
)


class LengthError(ValueError):
    """Entry is not 1-200 characters."""


class BlankError(ValueError):
    """Entry is only whitespace."""


class MultiLineError(ValueError):
    """Entry is not a single line."""


def validate(text: str) -> None:
    if not 1 <= len(text) <= 200:
        raise LengthError(
            "entry length %d is outside the 1-200 character gate" % len(text)
        )
    if not text.strip():
        raise BlankError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise MultiLineError("entry must be a single line")


def main() -> int:
    text = ENTRY
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise ValueError("MAKEFUN_OUTPUT_DIR is not set")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = text.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise ValueError("read-back mismatch: entry.txt bytes differ from entry")
    return 0


if __name__ == "__main__":
    sys.exit(main())
