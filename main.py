# SPDX-License-Identifier: MIT
"""Write the battery's last text to its charger to /output/entry.txt.

One line of plain text, at most 200 characters, as required by the
make.fun bounty "The Battery's Last Text to Its Charger".
"""

from pathlib import Path

ENTRY_TEXT = (
    "hey, don't cry for me. you gave me 100% every morning and I spent it "
    "all scrolling. if anyone asks, tell them I died doing what I loved: "
    "ignoring the low battery warning at 20, 15, 10, 5 and"
)


def main() -> None:
    output_path = Path("/output/entry.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(ENTRY_TEXT, encoding="utf-8")


if __name__ == "__main__":
    main()
