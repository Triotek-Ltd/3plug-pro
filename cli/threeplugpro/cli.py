from __future__ import annotations

import argparse
from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from threeplugpro.commands import bench, catalog, install, jobs, planning, server, workspace


def build_parser(prog: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=prog,
        description="3plug-pro CLI for Triotek's Bench control plane.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Path to the 3plug-pro repo root. Defaults to auto-discovery.",
    )
    parser.add_argument(
        "--config-path",
        type=Path,
        default=None,
        help="Path to local 3plug-pro config. Defaults to .3plug/config.json.",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Path to local 3plug-pro data. Defaults to .3plug/data.",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        dest="output_format",
        help="Output format for commands that support structured output.",
    )
    subparsers = parser.add_subparsers(dest="command")

    for module in (workspace, server, install, bench, catalog, jobs, planning):
        module.register(subparsers)

    return parser


def main(argv: list[str] | None = None) -> int:
    prog = Path(sys.argv[0]).name if sys.argv else "3plug"
    parser = build_parser(prog=prog)
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 1
    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
