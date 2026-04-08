from __future__ import annotations

import argparse

from threeplugpro.commands.server.update.handlers import run_server_update


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    server_update = subparsers.add_parser(
        "update",
        help="Show or execute the update flow for an existing server install.",
    )
    server_update.add_argument("--execute", action="store_true", help="Execute the local Linux update script instead of only printing guidance.")
    server_update.add_argument("--user", default="threeplug", help="Operator user name.")
    server_update.add_argument("--workdir", default="/opt/3plug-pro", help="Server workspace path managed by 3plug.")
    server_update.add_argument(
        "--package-url",
        default="git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli",
        help="Package URL used to update the installed 3plug CLI. Defaults to the current pre-release source on main until stable releases are in regular use.",
    )
    server_update.set_defaults(handler=run_server_update)
