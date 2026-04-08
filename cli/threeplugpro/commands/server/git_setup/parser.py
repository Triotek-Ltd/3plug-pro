from __future__ import annotations

import argparse

from threeplugpro.commands.server.git_setup.handlers import run_server_git_setup


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    server_git_setup = subparsers.add_parser(
        "git-setup",
        help="Show or execute Git identity setup for the operator user before install/update flows.",
    )
    server_git_setup.add_argument("--execute", action="store_true", help="Execute the local Linux Git setup script instead of only printing guidance.")
    server_git_setup.add_argument("--user", default="threeplug", help="Operator user name.")
    server_git_setup.add_argument("--git-name", default="", help="Git user.name to configure.")
    server_git_setup.add_argument("--git-email", default="", help="Git user.email to configure.")
    server_git_setup.set_defaults(handler=run_server_git_setup)
