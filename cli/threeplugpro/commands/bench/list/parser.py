from __future__ import annotations

import argparse

from threeplugpro.commands.bench.list.handlers import run_bench_list


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    bench_list = subparsers.add_parser("list", help="List registered/discovered benches.")
    bench_list.set_defaults(handler=run_bench_list)
