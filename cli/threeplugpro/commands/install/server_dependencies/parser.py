from __future__ import annotations

import argparse

from threeplugpro.commands.install.server_dependencies.handlers import run_install_server_dependencies


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    install_deps = subparsers.add_parser(
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
