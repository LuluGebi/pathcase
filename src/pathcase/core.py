"""Case-conversion helpers for path names.

Only name *stems* are converted; file extensions are left untouched.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterator

# Split on explicit separators, then split CamelCase chunks into words.
# Alternatives are order-sensitive: acronym runs must be tried before
# single-cap-with-digits, otherwise "V2" in "myFileV2" splits apart.
_HUNKS = re.compile(r"[ _\-]+")
_WORD = re.compile(
    r"""
      [A-Z]+(?=[A-Z][a-z])   # acronym head, e.g. HTTP in HTTPServer
    | [A-Z][a-z0-9]+         # cap + attached lower/digits, e.g. File, V2
    | [A-Z]+                 # bare caps run, e.g. ABC
    | [a-z0-9]+              # plain lowercase/digit run
    """,
    re.VERBOSE,
)


def words(name: str) -> list[str]:
    """Break a file stem into lowercase words.

    Handles ``snake_case``, ``kebab-case``, ``camelCase``, ``PascalCase``
    and plain ``spaced names`` in any mixture.
    """
    out: list[str] = []
    for hunk in _HUNKS.split(name):
        out.extend(m.group(0).lower() for m in _WORD.finditer(hunk))
    return out


def snake_case(name: str) -> str:
    return "_".join(words(name))


def kebab_case(name: str) -> str:
    return "-".join(words(name))


def pascal_case(name: str) -> str:
    return "".join(w.capitalize() for w in words(name))


def camel_case(name: str) -> str:
    s = pascal_case(name)
    return s[:1].lower() + s[1:]


STYLES: dict[str, callable] = {
    "snake": snake_case,
    "kebab": kebab_case,
    "camel": camel_case,
    "pascal": pascal_case,
}


def plan_renames(paths: Iterator[Path], style: str) -> list[tuple[Path, Path]]:
    """Build a list of ``(old, new)`` rename pairs for the given style.

    Entries whose stem would not change are skipped.
    """
    convert = STYLES[style]
    plan: list[tuple[Path, Path]] = []
    for path in paths:
        new_stem = convert(path.stem)
        if new_stem != path.stem:
            plan.append((path, path.with_stem(new_stem)))
    return plan


def apply_renames(plan: list[tuple[Path, Path]]) -> list[str]:
    """Execute a rename plan. Returns error messages, one per failure."""
    errors: list[str] = []
    for old, new in plan:
        try:
            old.rename(new)
        except OSError as exc:
            errors.append(f"{old} -> {new}: {exc}")
    return errors
