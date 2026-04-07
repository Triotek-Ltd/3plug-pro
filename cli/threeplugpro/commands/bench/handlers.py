from __future__ import annotations

import argparse

from threeplugpro.core import output_json, resolve_root


def run_bench_list(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    benches_root = root / "benches"
    payload = {
        "implemented": False,
        "benches": [],
        "future_local_bench_root": benches_root,
    }
    if output_json(args, payload):
        return 0
    print("Registered bench state is not implemented yet.")
    print(f"Expected future local bench root: {benches_root}")
    return 0
