from __future__ import annotations

import argparse
import platform

from threeplugpro.commands.server.common import record_server_job
from threeplugpro.core import resolve_root, run_command, update_job


def _run_first_available(commands: list[list[str]]) -> tuple[int, str, list[str]]:
    for command in commands:
        code, output = run_command(command)
        if code != 127:
            return code, output, command
    return 127, "", commands[0]


def run_server_preflight(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    checks = [
        ("os", [["cmd", "/c", "ver"]] if platform.system() == "Windows" else [["uname", "-a"]]),
        ("git", [["git", "--version"]]),
        ("python", [["python", "--version"], ["python3", "--version"]]),
        ("uv", [["uv", "--version"]]),
        ("pip", [["pip", "--version"], ["pip3", "--version"]]),
        ("node", [["node", "--version"], ["nodejs", "--version"]]),
        ("npm", [["npm", "--version"]]),
        ("yarn", [["yarn", "--version"]]),
        ("redis", [["redis-server", "--version"], ["redis-cli", "--version"]]),
        ("mariadb", [["mariadb", "--version"], ["mariadb-admin", "--version"]]),
        ("mysql", [["mysql", "--version"]]),
        ("wkhtmltopdf", [["wkhtmltopdf", "--version"]]),
        ("nginx", [["nginx", "-v"]]),
        ("supervisord", [["supervisord", "--version"], ["supervisorctl", "--version"], ["systemctl", "--version"]]),
    ]

    payload: dict[str, object] = {
        "implemented": True,
        "command_family": "server",
        "action": "preflight",
        "target_stack": "frappe-v16",
        "checks": [],
    }
    job_id = record_server_job(
        root,
        args,
        action="preflight",
        summary="Inspect the current server prerequisites for Frappe v16.",
        payload=payload,
    )
    payload["job_id"] = job_id

    print("3plug-pro server preflight")
    print(f"job {job_id}")
    print("target stack frappe-v16")
    print("install branch main")
    print("upstream tracking branch upstream-v16")

    missing = 0
    for label, commands in checks:
        code, output, used_command = _run_first_available(commands)
        check_status = "missing"
        if code == 127:
            missing += 1
            print(f"MISSING {label}")
        elif code == 0:
            check_status = "ok"
            print(f"OK {label} {output}")
        else:
            missing += 1
            check_status = "warn"
            print(f"WARN {label} {output}")
        payload["checks"].append(
            {
                "label": label,
                "command": used_command,
                "candidates": commands,
                "status": check_status,
                "output": output,
            }
        )

    payload["result"] = "failed" if missing else "passed"
    update_job(
        root,
        args,
        job_id=job_id,
        status="failed" if missing else "completed",
        details=payload,
    )

    return 1 if missing else 0


__all__ = ["_run_first_available", "run_server_preflight"]
