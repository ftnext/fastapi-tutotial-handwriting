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


def find_original_file(translation_file_path: Path) -> Path:
    """
    >>> from pathlib import PosixPath
    >>> find_original_file(Path("fastapi/docs/ja/docs/tutorial/query-params.md"))  # NOQA
    PosixPath('fastapi/docs/en/docs/tutorial/query-params.md')
    >>> find_original_file(Path("fastapi/docs/ja/docs/tutorial/security/first-steps.md"))  # NOQA
    PosixPath('fastapi/docs/en/docs/tutorial/security/first-steps.md')
    """
    docs_count = 0
    directory_names = []

    parent_path = translation_file_path.parent
    while True:
        if parent_path.name == "docs":
            docs_count += 1
            if docs_count == 2:
                break
        if parent_path.name != "ja":
            directory_names.append(parent_path.name)
        parent_path = parent_path.parent
    original_path = parent_path / "en"
    for name in reversed(directory_names):
        original_path = original_path / name
    return original_path / translation_file_path.name


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("translation", type=Path)
    args = parser.parse_args()

    translation_hl_lines = build_hl_lines_mapping(args.translation)

    original_file = find_original_file(args.translation)
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
