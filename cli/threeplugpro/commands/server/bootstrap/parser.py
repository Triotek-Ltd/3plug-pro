from __future__ import annotations

import argparse

from threeplugpro.commands.server.bootstrap.handlers import run_server_bootstrap


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    server_bootstrap = subparsers.add_parser(
        "bootstrap",
        help="Show or execute the bootstrap flow for onboarding a server.",
    )
    server_bootstrap.add_argument("--execute", action="store_true", help="Execute the local Linux bootstrap script instead of only printing guidance.")
    server_bootstrap.add_argument("--user", default="threeplug", help="Operator user name.")
    server_bootstrap.add_argument("--workdir", default="/opt/3plug-pro", help="Server workspace path managed by 3plug.")
    server_bootstrap.add_argument("--no-firewall-enable", action="store_true", help="Skip automatic UFW enablement in the bootstrap script.")
    server_bootstrap.add_argument("--ssh-ufw-profile", default="OpenSSH", help="UFW SSH profile to allow before firewall enablement.")
    server_bootstrap.set_defaults(handler=run_server_bootstrap)
