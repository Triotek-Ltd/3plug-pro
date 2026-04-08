from __future__ import annotations

import argparse

from threeplugpro.commands.server.common import execute_server_script_with_fetch, record_server_job, render_script_command, server_script_payload
from threeplugpro.core import output_json, resolve_root, update_job


def run_server_git_setup(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {"THREEPLUG_USER": args.user}
    if args.git_name:
        env_vars["THREEPLUG_GIT_NAME"] = args.git_name
    if args.git_email:
        env_vars["THREEPLUG_GIT_EMAIL"] = args.git_email
    command = render_script_command(root / "scripts" / "linux" / "configure_3plug_git.sh", env_vars)
    payload = server_script_payload(
        root,
        "configure_3plug_git.sh",
        "git-setup",
        {
            "operator_user": args.user,
            "execute": args.execute,
            "env": env_vars,
            "fetch_command": "curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/configure_3plug_git.sh -o /tmp/configure_3plug_git.sh",
            "run_command": command.replace(str(root / "scripts" / "linux" / "configure_3plug_git.sh"), "/tmp/configure_3plug_git.sh"),
            "local_execute_command": command,
            "requires_git_identity": True,
        },
    )
    job_id = record_server_job(root, args, action="git-setup", summary="Configure Git identity for the operator user before install/update flows.", payload=payload)
    payload["job_id"] = job_id
    if output_json(args, payload):
        return 0
    print("3plug server git-setup")
    print(f"job {job_id}")
    print(f"script {payload['script_path']}")
    print("Use this to configure Git identity before installing or updating 3plug.")
    print(f"Fetch: {payload['fetch_command']}")
    print(f"Run: {payload['run_command']}")
    print(f"Local execute command: {payload['local_execute_command']}")
    if args.execute:
        print("Executing git setup script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = execute_server_script_with_fetch(payload["script_path"], env_vars, str(payload["fetch_command"]))
        update_job(root, args, job_id=job_id, status="completed" if code == 0 else "failed", details={**payload, "exit_code": code})
        return code
    return 0


__all__ = ["run_server_git_setup"]
