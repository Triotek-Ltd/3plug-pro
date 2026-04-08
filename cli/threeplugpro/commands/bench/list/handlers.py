from __future__ import annotations

import argparse

from threeplugpro.commands.bench.common import approved_bench_root
from threeplugpro.core import list_bench_records, output_json, resolve_root


def run_bench_list(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    benches = list_bench_records(root, args)
    payload = {
        "implemented": True,
        "benches": benches,
        "future_local_bench_root": approved_bench_root(root),
    }
    if output_json(args, payload):
        return 0
    if not benches:
        print("No managed benches are recorded yet.")
        print(f"Expected bench root: {approved_bench_root(root)}")
        return 0
    print("Managed benches")
    for bench in benches:
        print(f"- {bench['name']} {bench['status']} {bench['path']}")
    return 0


__all__ = ["run_bench_list"]
