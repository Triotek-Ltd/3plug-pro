from __future__ import annotations

import argparse

from threeplugpro.commands.server.handlers import run_server_preflight


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    server = subparsers.add_parser("server", help="Managed server helper commands.")
    server_sub = server.add_subparsers(dest="server_command")

    server_preflight = server_sub.add_parser(
        "preflight",
        help="Check Frappe v16 non-Docker server prerequisites without installing.",
    )
    server_preflight.set_defaults(handler=run_server_preflight)
