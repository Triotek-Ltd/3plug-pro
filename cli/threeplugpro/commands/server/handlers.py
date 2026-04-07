from __future__ import annotations

import argparse
import platform

from threeplugpro.core import run_command


def run_server_preflight(_args: argparse.Namespace) -> int:
    checks = [
        ("os", ["cmd", "/c", "ver"] if platform.system() == "Windows" else ["uname", "-a"]),
        ("git", ["git", "--version"]),
        ("python", ["python", "--version"]),
        ("uv", ["uv", "--version"]),
        ("pip", ["pip", "--version"]),
        ("node", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
        ("yarn", ["yarn", "--version"]),
        ("redis", ["redis-server", "--version"]),
        ("mariadb", ["mariadb", "--version"]),
        ("mysql", ["mysql", "--version"]),
        ("wkhtmltopdf", ["wkhtmltopdf", "--version"]),
        ("nginx", ["nginx", "-v"]),
        ("supervisord", ["supervisord", "--version"]),
    ]

    print("3plug-pro server preflight")
    print("target stack frappe-v16")
    print("install branch main")
    print("upstream tracking branch upstream-v16")

    missing = 0
    for label, command in checks:
        code, output = run_command(command)
        if code == 127:
            missing += 1
            print(f"MISSING {label}")
        elif code == 0:
            print(f"OK {label} {output}")
        else:
            missing += 1
            print(f"WARN {label} {output}")

    return 1 if missing else 0
