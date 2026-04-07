from __future__ import annotations

import argparse


def run_install_server_dependencies_plan(_args: argparse.Namespace) -> int:
    print("3plug-pro server dependency install plan")
    print("target stack: frappe-v16")
    print("This command is plan-only for now; no packages were installed.")
    for item in [
        "MariaDB 11.8",
        "Python 3.14",
        "pip 25.3+",
        "uv",
        "Node.js 24",
        "Yarn 1.22+",
        "Redis / Valkey 6+",
        "wkhtmltopdf 0.12.6 with patched Qt",
        "xvfb and libfontconfig",
        "cron",
        "nginx for production serving",
        "supervisor or systemd for production process management",
    ]:
        print(f"- {item}")
    return 0


def run_install_bench_plan(_args: argparse.Namespace) -> int:
    print("3plug-pro Bench install plan")
    print("This command is plan-only for now; Bench was not installed.")
    print("preferred source: https://github.com/Triotek-Ltd/triotek-bench.git")
    print("install branch: main or approved triotek-bench v16 branch")
    print("fallback source: approved upstream frappe-bench package")
    return 0
