from __future__ import annotations

import argparse

from threeplugpro.commands.install.bench.handlers import run_install_bench


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    install_bench = subparsers.add_parser(
        "bench",
        help="Show or execute the Bench install flow for the managed server.",
    )
    install_bench.add_argument("--execute", action="store_true", help="Execute the Bench install script.")
    install_bench.add_argument("--user", default="threeplug", help="Operator user name.")
    install_bench.add_argument(
        "--bench-source",
        default="git+ssh://git@github.com/Triotek-Ltd/triotek-bench.git",
        help="Bench package source to install. SSH is the default for private Triotek bench sources, and the repo default branch is used unless you override it.",
    )
    install_bench.set_defaults(handler=run_install_bench)
