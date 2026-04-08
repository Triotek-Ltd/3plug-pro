from __future__ import annotations

import argparse

from threeplugpro.commands.server.bootstrap.parser import register as register_server_bootstrap
from threeplugpro.commands.server.git_setup.parser import register as register_server_git_setup
from threeplugpro.commands.server.install_cli.parser import register as register_server_install_cli
from threeplugpro.commands.server.preflight.parser import register as register_server_preflight
from threeplugpro.commands.server.uninstall.parser import register as register_server_uninstall
from threeplugpro.commands.server.update.parser import register as register_server_update


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    server = subparsers.add_parser("server", help="Managed server helper commands.")
    server_sub = server.add_subparsers(dest="server_command")
    register_server_preflight(server_sub)
    register_server_bootstrap(server_sub)
    register_server_git_setup(server_sub)
    register_server_install_cli(server_sub)
    register_server_update(server_sub)
    register_server_uninstall(server_sub)
