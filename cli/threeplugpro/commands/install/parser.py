from __future__ import annotations

import argparse

from threeplugpro.commands.install.handlers import (
    run_install_bench_plan,
    run_install_server_dependencies_plan,
)


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    install = subparsers.add_parser("install", help="Install helper commands.")
    install_sub = install.add_subparsers(dest="install_command")

    install_bench = install_sub.add_parser(
        "bench",
        help="Show the Bench install plan for the managed server.",
    )
    install_bench.set_defaults(handler=run_install_bench_plan)

    install_deps = install_sub.add_parser(
        "server-dependencies",
        help="Show the Frappe v16 server dependency install plan.",
    )
    install_deps.set_defaults(handler=run_install_server_dependencies_plan)
