from __future__ import annotations

import argparse

from threeplugpro.commands.install.bench.parser import register as register_install_bench
from threeplugpro.commands.install.server_dependencies.parser import register as register_install_server_dependencies


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    install = subparsers.add_parser("install", help="Install helper commands.")
    install_sub = install.add_subparsers(dest="install_command")
    register_install_bench(install_sub)
    register_install_server_dependencies(install_sub)
