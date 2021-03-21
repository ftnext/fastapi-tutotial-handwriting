"""Check hl_lines mismatches about tutorial."""

import argparse
import re
from collections.abc import Mapping
from pathlib import Path

# ref: https://squidfunk.github.io/mkdocs-material/reference/code-blocks/#highlighting-specific-lines  # NOQA
highlight_pattern = r"""```[Pp]ython (hl_lines="(\d+|\d+\s+\d+|\d+\-\d+)")
\{\!(.+)\!\}
```
"""


def build_hl_lines_mapping(file_path: Path) -> Mapping:
    text = file_path.read_text("utf-8")
    source_to_hl_lines = {}
    for m in re.finditer(highlight_pattern, text):
        source_to_hl_lines[m[3]] = m[1]
    return source_to_hl_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("translation", type=Path)
    args = parser.parse_args()

    translation_hl_lines = build_hl_lines_mapping(args.translation)

    docs_root = args.translation.parent.parent.parent.parent
    original_file = (
        docs_root / "en" / "docs" / "tutorial" / args.translation.name
    )
    original_hl_lines = build_hl_lines_mapping(original_file)

    # ref: https://teratail.com/questions/171217#reply-255067
    difference = dict(translation_hl_lines.items() - original_hl_lines.items())
    if difference:
        for file_path, hl_lines in sorted(
            difference.items(), key=lambda d: d[0]
        ):
            print(file_path)
            print(
                f"\tActual: {hl_lines}, "
                f"Expected: {original_hl_lines[file_path]}"
            )
            print()
