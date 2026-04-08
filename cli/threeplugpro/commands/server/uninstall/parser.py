from __future__ import annotations

import argparse

from threeplugpro.commands.server.uninstall.handlers import run_server_uninstall


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    server_uninstall = subparsers.add_parser(
        "uninstall",
        help="Show or execute the uninstall flow for removing 3plug from a server.",
    )
    server_uninstall.add_argument("--execute", action="store_true", help="Execute the local Linux uninstall script instead of only printing guidance.")
    server_uninstall.add_argument("--user", default="threeplug", help="Operator user name.")
    server_uninstall.add_argument("--workdir", default="/opt/3plug-pro", help="Server workspace path managed by 3plug.")
    server_uninstall.add_argument("--remove-user", action="store_true", help="Also remove the operator user and home directory.")
    server_uninstall.add_argument("--keep-workdir", action="store_true", help="Keep the managed workspace instead of removing it.")
    server_uninstall.add_argument("--keep-venv", action="store_true", help="Keep the operator virtual environment instead of removing it.")
    server_uninstall.add_argument("--force", action="store_true", help="Skip the uninstall confirmation prompt.")
    server_uninstall.set_defaults(handler=run_server_uninstall)
