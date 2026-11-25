# SPDX-License-Identifier: MIT
"""The Battery's Last Text to Its Charger — make.fun entry (program/v1).

Writes one line of plain text — the phone battery's final message to
the charger it waited for all day — to /output/entry.txt as UTF-8 with
no trailing newline. The sealed gate accepts UTF-8 text of 1 to 200
characters that is not only whitespace, so the message is validated
against those limits before anything is written.
"""

from pathlib import Path

OUTPUT_PATH = Path("/output/entry.txt")

# Gate limits from the competition rules.
MIN_CHARS = 1
MAX_CHARS = 200

# The farewell itself, assembled from its three beats: the plea, the
# confession about how the charge was spent, and the last-words joke
# that runs out mid-sentence, exactly like the battery does.
_OPENING = "hey, don't cry for me. "
_CONFESSION = (
    "you gave me 100% every morning and I spent it all scrolling. "
)
_LAST_WORDS = (
    "if anyone asks, tell them I died doing what I loved: "
    "ignoring the low battery warning at 20, 15, 10, 5 and"
)


def build_message() -> str:
    """Return the entry text, checked against the gate limits."""
    text = _OPENING + _CONFESSION + _LAST_WORDS
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, gate wants 1..200")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main(output_path: Path = OUTPUT_PATH) -> None:
    payload = build_message().encode("utf-8")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(payload)
    verify_written(output_path, payload)


def verify_written(output_path: Path, expected: bytes) -> None:
    """Round-trip self-check: re-read the file just written and confirm
    it is byte-for-byte what was intended and still inside the gate.

    The grader runs this program twice in separate sandboxes, so a
    silent short write or encoding slip would sink the entry; failing
    loudly here is strictly better than emitting a corrupt artifact.
    """
    on_disk = output_path.read_bytes()
    if on_disk != expected:
        raise IOError(
            f"round-trip mismatch: wrote {len(expected)} bytes, "
            f"read back {len(on_disk)}"
        )
    decoded = on_disk.decode("utf-8")
    if not MIN_CHARS <= len(decoded) <= MAX_CHARS or not decoded.strip():
        raise ValueError("written file falls outside the gate limits")


if __name__ == "__main__":
    main()
