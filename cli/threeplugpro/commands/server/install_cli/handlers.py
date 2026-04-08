from __future__ import annotations

import argparse

from threeplugpro.commands.server.common import execute_server_script_with_fetch, record_server_job, render_script_command, server_script_payload
from threeplugpro.core import output_json, resolve_root, update_job


def run_server_install_cli(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {"THREEPLUG_USER": args.user, "THREEPLUG_PACKAGE_URL": args.package_url}
    command = render_script_command(root / "scripts" / "linux" / "install_3plug_cli.sh", env_vars)
    payload = server_script_payload(
        root,
        "install_3plug_cli.sh",
        "install-cli",
        {
            "operator_user": args.user,
            "execute": args.execute,
            "env": env_vars,
            "fetch_command": "curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/install_3plug_cli.sh -o /tmp/install_3plug_cli.sh",
            "run_command": command.replace(str(root / "scripts" / "linux" / "install_3plug_cli.sh"), "/tmp/install_3plug_cli.sh"),
            "local_execute_command": command,
            "requires_git_identity": True,
            "uses_prerelease_source": args.package_url.endswith("@main#subdirectory=cli"),
        },
    )
    job_id = record_server_job(root, args, action="install-cli", summary="Install the 3plug CLI after Git identity is configured.", payload=payload)
    payload["job_id"] = job_id
    if output_json(args, payload):
        return 0
    print("3plug server install-cli")
    print(f"job {job_id}")
    print(f"script {payload['script_path']}")
    print("Use this to install 3plug after Git identity is configured.")
    print(f"Fetch: {payload['fetch_command']}")
    print(f"Run: {payload['run_command']}")
    print(f"Local execute command: {payload['local_execute_command']}")
    if args.execute:
        print("Executing CLI install script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = execute_server_script_with_fetch(payload["script_path"], env_vars, str(payload["fetch_command"]))
        update_job(root, args, job_id=job_id, status="completed" if code == 0 else "failed", details={**payload, "exit_code": code})
        return code
    return 0


__all__ = ["run_server_install_cli"]
