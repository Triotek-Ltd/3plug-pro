from __future__ import annotations

import argparse

from threeplugpro.commands.bench.create.parser import register as register_bench_create
from threeplugpro.commands.bench.list.parser import register as register_bench_list


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    bench = subparsers.add_parser("bench", help="Bench runtime helper commands.")
    bench_sub = bench.add_subparsers(dest="bench_command")
    register_bench_create(bench_sub)
    register_bench_list(bench_sub)
