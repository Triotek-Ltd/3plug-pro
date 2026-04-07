from __future__ import annotations

import argparse

from threeplugpro.commands.workspace.handlers import run_doctor, run_init


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    doctor = subparsers.add_parser("doctor", help="Check workspace expectations.")
    doctor.set_defaults(handler=run_doctor)

    init_cmd = subparsers.add_parser("init", help="Initialize local 3plug-pro state.")
    init_cmd.set_defaults(handler=run_init)
