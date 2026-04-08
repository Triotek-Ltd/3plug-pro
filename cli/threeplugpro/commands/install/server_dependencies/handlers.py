from __future__ import annotations

import argparse

from threeplugpro.commands.install.common import execute_script_with_fetch, record_install_job, render_script_command
from threeplugpro.core import output_json, resolve_root, update_job


def run_install_server_dependencies(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_TARGET_STACK": "frappe-v16",
        "THREEPLUG_INSTALL_PRODUCTION_TOOLS": "1" if args.production_tools else "0",
    }
    script_path = root / "scripts" / "linux" / "install_server_dependencies.sh"
    command = render_script_command(script_path, env_vars)
    payload = {
        "implemented": True,
        "command_family": "install",
        "action": "server-dependencies",
        "script_path": script_path,
        "script_exists": script_path.exists(),
        "execute": args.execute,
        "env": env_vars,
        "fetch_command": "curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/install_server_dependencies.sh -o /tmp/install_server_dependencies.sh",
        "run_command": command.replace(str(script_path), "/tmp/install_server_dependencies.sh"),
        "local_execute_command": command,
        "requires_explicit_execution": True,
        "target_stack": "frappe-v16",
        "production_conflicts_checked": ["apache2"],
        "installs": [
            "build-essential",
            "redis-server",
            "mariadb-server",
            "mariadb-client",
            "libmariadb-dev",
            "pkg-config",
            "python3-dev",
            "python3-pip",
            "python3-venv",
            "xvfb",
            "libfontconfig1",
            "cron",
            "wkhtmltopdf",
            "uv",
            "nodejs",
            "npm",
            "yarn",
        ],
        "production_installs": ["nginx", "supervisor", "fail2ban"],
    }
    job_id = record_install_job(
        root,
        args,
        action="server-dependencies",
        summary="Install server dependencies needed before Bench installation.",
        payload=payload,
    )
    payload["job_id"] = job_id
    if output_json(args, payload):
        return 0

    print("3plug install server-dependencies")
    print(f"job {job_id}")
    print(f"script {script_path}")
    print("Use this to install the current dependency foundation before Bench installation.")
    print(f"Fetch: {payload['fetch_command']}")
    print(f"Run: {payload['run_command']}")
    print(f"Local execute command: {payload['local_execute_command']}")
    if args.execute:
        print("Executing server dependency install script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = execute_script_with_fetch(script_path, env_vars, str(payload["fetch_command"]))
        update_job(root, args, job_id=job_id, status="completed" if code == 0 else "failed", details={**payload, "exit_code": code})
        return code
    return 0


__all__ = ["run_install_server_dependencies"]
