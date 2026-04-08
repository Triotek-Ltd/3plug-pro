from __future__ import annotations

import argparse

from threeplugpro.commands.install.common import execute_script_with_fetch, record_install_job, render_script_command
from threeplugpro.core import output_json, resolve_root, update_job


def run_install_bench(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_USER": args.user,
        "THREEPLUG_BENCH_SOURCE": args.bench_source,
    }
    script_path = root / "scripts" / "linux" / "install_bench.sh"
    command = render_script_command(script_path, env_vars)
    payload = {
        "implemented": True,
        "command_family": "install",
        "action": "bench",
        "script_path": script_path,
        "script_exists": script_path.exists(),
        "execute": args.execute,
        "env": env_vars,
        "fetch_command": "curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/install_bench.sh -o /tmp/install_bench.sh",
        "run_command": command.replace(str(script_path), "/tmp/install_bench.sh"),
        "local_execute_command": command,
        "requires_explicit_execution": True,
        "requires_git_identity": True,
        "requires_github_ssh_for_private_source": args.bench_source.startswith("git+ssh://"),
    }
    job_id = record_install_job(
        root,
        args,
        action="bench",
        summary="Install Bench before creating managed bench runtimes.",
        payload=payload,
    )
    payload["job_id"] = job_id
    if output_json(args, payload):
        return 0

    print("3plug install bench")
    print(f"job {job_id}")
    print(f"script {script_path}")
    print("Use this to install Bench before bench create/register actions.")
    print(f"Fetch: {payload['fetch_command']}")
    print(f"Run: {payload['run_command']}")
    print(f"Local execute command: {payload['local_execute_command']}")
    if args.execute:
        print("Executing bench install script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = execute_script_with_fetch(script_path, env_vars, str(payload["fetch_command"]))
        update_job(root, args, job_id=job_id, status="completed" if code == 0 else "failed", details={**payload, "exit_code": code})
        return code
    return 0


__all__ = ["run_install_bench"]
