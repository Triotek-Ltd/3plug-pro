from __future__ import annotations

import argparse

from threeplugpro.commands.server.common import execute_server_script_with_fetch, record_server_job, render_script_command, server_script_payload
from threeplugpro.core import output_json, resolve_root, update_job


def run_server_bootstrap(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_USER": args.user,
        "THREEPLUG_WORKDIR": args.workdir,
        "SSH_UFW_PROFILE": args.ssh_ufw_profile,
        "FIREWALL_AUTO_ENABLE": "0" if args.no_firewall_enable else "1",
    }
    command = render_script_command(root / "scripts" / "linux" / "bootstrap_3plug_server.sh", env_vars)
    payload = server_script_payload(
        root,
        "bootstrap_3plug_server.sh",
        "bootstrap",
        {
            "workspace": args.workdir,
            "operator_user": args.user,
            "requires_interactive_password_prompt": True,
            "execute": args.execute,
            "env": env_vars,
            "fetch_command": "curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/bootstrap_3plug_server.sh -o /tmp/bootstrap_3plug_server.sh",
            "run_command": command.replace(str(root / "scripts" / "linux" / "bootstrap_3plug_server.sh"), "/tmp/bootstrap_3plug_server.sh"),
            "local_execute_command": command,
        },
    )
    job_id = record_server_job(root, args, action="bootstrap", summary="Prepare a server so 3plug can run.", payload=payload)
    payload["job_id"] = job_id
    if output_json(args, payload):
        return 0
    print("3plug server bootstrap")
    print(f"job {job_id}")
    print(f"script {payload['script_path']}")
    print("Use this to prepare a new Ubuntu/Debian server so 3plug can run.")
    print(f"Fetch: {payload['fetch_command']}")
    print(f"Run: {payload['run_command']}")
    print(f"Local execute command: {payload['local_execute_command']}")
    if args.execute:
        print("Executing bootstrap script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = execute_server_script_with_fetch(payload["script_path"], env_vars, str(payload["fetch_command"]))
        update_job(root, args, job_id=job_id, status="completed" if code == 0 else "failed", details={**payload, "exit_code": code})
        return code
    return 0


__all__ = ["run_server_bootstrap"]
