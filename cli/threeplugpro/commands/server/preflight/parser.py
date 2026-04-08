from __future__ import annotations

import argparse

from threeplugpro.commands.server.preflight.handlers import run_server_preflight


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    server_preflight = subparsers.add_parser(
        "preflight",
        help="Check Frappe v16 non-Docker server prerequisites without installing.",
    )
    server_preflight.set_defaults(handler=run_server_preflight)
