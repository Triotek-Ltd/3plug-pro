from __future__ import annotations

import argparse

from threeplugpro.commands.install.handlers import (
    run_install_bench,
    run_install_server_dependencies,
)


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    install = subparsers.add_parser("install", help="Install helper commands.")
    install_sub = install.add_subparsers(dest="install_command")

    install_bench = install_sub.add_parser(
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

    install_deps = install_sub.add_parser(
        "server-dependencies",
        help="Show or execute the Frappe v16 server dependency install flow.",
    )
    install_deps.add_argument("--execute", action="store_true", help="Execute the dependency install script.")
    install_deps.add_argument(
        "--production-tools",
        action="store_true",
        help="Also install nginx, supervisor, and fail2ban.",
    )
    install_deps.set_defaults(handler=run_install_server_dependencies)
