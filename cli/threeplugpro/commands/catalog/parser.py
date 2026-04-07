from __future__ import annotations

import argparse

from threeplugpro.commands.catalog.handlers import run_app_list, run_app_show, run_stack_list


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    app = subparsers.add_parser("app", help="App catalog helper commands.")
    app_sub = app.add_subparsers(dest="app_command")

    app_list = app_sub.add_parser("list", help="List approved app sources.")
    app_list.add_argument("--all", action="store_true", help="Include planned apps.")
    app_list.set_defaults(handler=run_app_list)

    app_show = app_sub.add_parser("show", help="Show one approved app source.")
    app_show.add_argument("app")
    app_show.set_defaults(handler=run_app_show)

    stack = subparsers.add_parser("stack", help="Stack catalog helper commands.")
    stack_sub = stack.add_subparsers(dest="stack_command")

    stack_list = stack_sub.add_parser("list", help="List available stacks.")
    stack_list.set_defaults(handler=run_stack_list)
