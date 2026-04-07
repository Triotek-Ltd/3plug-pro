from __future__ import annotations

import argparse

from threeplugpro.commands.bench.handlers import run_bench_list


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    bench = subparsers.add_parser("bench", help="Bench runtime helper commands.")
    bench_sub = bench.add_subparsers(dest="bench_command")

    bench_list = bench_sub.add_parser("list", help="List registered/discovered benches.")
    bench_list.set_defaults(handler=run_bench_list)
