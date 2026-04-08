from __future__ import annotations

import argparse

from threeplugpro.commands.server.common import execute_server_script_with_fetch, record_server_job, render_script_command, server_script_payload
from threeplugpro.core import output_json, resolve_root, update_job


def run_server_uninstall(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_USER": args.user,
        "THREEPLUG_WORKDIR": args.workdir,
        "REMOVE_USER": "1" if args.remove_user else "0",
        "REMOVE_WORKDIR": "0" if args.keep_workdir else "1",
        "REMOVE_VENV": "0" if args.keep_venv else "1",
        "THREEPLUG_FORCE": "1" if args.force else "0",
    }
    command = render_script_command(root / "scripts" / "linux" / "uninstall_3plug_server.sh", env_vars)
    payload = server_script_payload(
        root,
        "uninstall_3plug_server.sh",
        "uninstall",
        {
            "operator_user": args.user,
            "workspace": args.workdir,
            "execute": args.execute,
            "env": env_vars,
            "fetch_command": "curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/uninstall_3plug_server.sh -o /tmp/uninstall_3plug_server.sh",
            "run_command": command.replace(str(root / "scripts" / "linux" / "uninstall_3plug_server.sh"), "/tmp/uninstall_3plug_server.sh"),
            "local_execute_command": command,
            "requires_confirmation": not args.force,
        },
    )
    job_id = record_server_job(root, args, action="uninstall", summary="Remove the managed 3plug footprint from a server.", payload=payload)
    payload["job_id"] = job_id
    if output_json(args, payload):
        return 0
    print("3plug server uninstall")
    print(f"job {job_id}")
    print(f"script {payload['script_path']}")
    print("Use this to remove the managed 3plug footprint from a server.")
    print(f"Fetch: {payload['fetch_command']}")
    print(f"Run: {payload['run_command']}")
    print(f"Local execute command: {payload['local_execute_command']}")
    if args.execute:
        print("Executing uninstall script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = execute_server_script_with_fetch(payload["script_path"], env_vars, str(payload["fetch_command"]))
        update_job(root, args, job_id=job_id, status="completed" if code == 0 else "failed", details={**payload, "exit_code": code})
        return code
    return 0


__all__ = ["run_server_uninstall"]
