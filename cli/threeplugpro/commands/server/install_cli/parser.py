from __future__ import annotations

import argparse

from threeplugpro.commands.server.install_cli.handlers import run_server_install_cli


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    server_install_cli = subparsers.add_parser(
        "install-cli",
        help="Show or execute the first 3plug CLI install flow after Git identity is configured.",
    )
    server_install_cli.add_argument("--execute", action="store_true", help="Execute the local Linux install script instead of only printing guidance.")
    server_install_cli.add_argument("--user", default="threeplug", help="Operator user name.")
    server_install_cli.add_argument(
        "--package-url",
        default="git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli",
        help="Package URL used to install the 3plug CLI. Defaults to the current pre-release source on main until stable releases are in regular use.",
    )
    server_install_cli.set_defaults(handler=run_server_install_cli)
