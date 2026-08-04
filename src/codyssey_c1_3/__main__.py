"""Command-line interface for repository checks."""

from __future__ import annotations

import argparse
from pathlib import Path

from .evidence import validate_manifest


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(prog="codyssey-c1-3")
    parser.add_argument("command", choices=("validate",))
    parser.add_argument("--root", type=Path, default=Path.cwd())
    return parser


def main() -> int:
    """Run the selected repository check."""

    args = build_parser().parse_args()
    findings = validate_manifest(args.root.resolve())
    if findings:
        for finding in findings:
            print(f"[FAIL] {finding.requirement_id}: {finding.message}")
        return 1

    print("[OK] evidence manifest is consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
