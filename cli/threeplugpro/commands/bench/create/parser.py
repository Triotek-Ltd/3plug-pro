from __future__ import annotations

import argparse

from threeplugpro.commands.bench.create.handlers import run_bench_create


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    bench_create = subparsers.add_parser("create", help="Create one managed Bench runtime.")
    bench_create.add_argument("name", help="Bench runtime name, for example production.")
    bench_create.add_argument("--path", help="Bench path. Defaults to <root>/benches/<name>.")
    bench_create.add_argument(
        "--frappe-path",
        default="https://github.com/Triotek-Ltd/triotek-frappe.git",
        help="Frappe source used during bench init.",
    )
    bench_create.add_argument(
        "--frappe-branch",
        default="main",
        help="Frappe branch used during bench init.",
    )
    bench_create.add_argument("--python", dest="python_executable", help="Python executable to pass to bench init.")
    bench_create.add_argument("--skip-assets", action="store_true", help="Pass --skip-assets to bench init.")
    bench_create.add_argument("--no-backups", action="store_true", help="Pass --no-backups to bench init.")
    bench_create.add_argument("--dev", action="store_true", help="Pass --dev to bench init.")
    bench_create.add_argument("--user", default="threeplug", help="Operator user that owns the bench.")
    bench_create.add_argument("--workdir", default="/opt/3plug-pro", help="Server workspace root.")
    bench_create.add_argument("--execute", action="store_true", help="Execute the bench create script immediately.")
    bench_create.set_defaults(handler=run_bench_create)
