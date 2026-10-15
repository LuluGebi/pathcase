"""Command-line entry point for pathcase."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import STYLES, apply_renames, plan_renames


def collect(paths: list[Path], recursive: bool) -> list[Path]:
    """Gather candidate paths, deepest first so children rename before parents."""
    out: list[Path] = []
    if not recursive:
        for p in paths:
            if p.is_dir():
                out.extend(x for x in p.iterdir() if not x.name.startswith("."))
            else:
                out.append(p)
    else:
        for base in paths:
            if base.is_dir():
                out.extend(
                    x
                    for x in base.rglob("*")
                    if not x.name.startswith(".") and not any(part.startswith(".") for part in x.parts)
                )
            else:
                out.append(base)
    out.sort(key=lambda p: (len(p.parts), str(p)), reverse=True)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pathcase",
        description="Batch-rename files and directories between case conventions.",
    )
    parser.add_argument("style", choices=sorted(STYLES), help="target naming style")
    parser.add_argument("paths", nargs="+", type=Path, help="files or directories to process")
    parser.add_argument("-r", "--recursive", action="store_true", help="recurse into subdirectories")
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="print the rename plan without touching the filesystem",
    )
    args = parser.parse_args(argv)

    candidates = collect(args.paths, args.recursive)
    plan = plan_renames(candidates, args.style)
    if not plan:
        print("nothing to rename")
        return 0

    width = max(len(str(old)) for old, _ in plan)
    for old, new in plan:
        print(f"{str(old):<{width}}  ->  {new}")

    if args.dry_run:
        return 0

    errors = apply_renames(plan)
    for err in errors:
        print(f"error: {err}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
