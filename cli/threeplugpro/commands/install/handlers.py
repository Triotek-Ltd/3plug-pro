from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import tempfile

from threeplugpro.core import create_job, output_json, resolve_root, update_job


def _render_env_prefix(env_vars: dict[str, str]) -> str:
    parts = []
    for key, value in env_vars.items():
        escaped = value.replace('"', '\\"')
        parts.append(f'{key}="{escaped}"')
    return " ".join(parts)


def _render_script_command(script_path: Path, env_vars: dict[str, str]) -> str:
    prefix = _render_env_prefix(env_vars)
    if prefix:
        return f"sudo env {prefix} bash {script_path}"
    return f"sudo bash {script_path}"


def _execute_script_with_fetch(script_path: Path, env_vars: dict[str, str], fetch_command: str) -> int:
    if script_path.exists():
        completed = subprocess.run(["bash", str(script_path)], check=False, env={**os.environ, **env_vars})
        return completed.returncode

    tmp_script = Path(tempfile.gettempdir()) / script_path.name
    fetch_completed = subprocess.run(
        [
            "curl",
            "-fsSL",
            f"https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/{script_path.name}",
            "-o",
            str(tmp_script),
        ],
        check=False,
        env=os.environ.copy(),
    )
    if fetch_completed.returncode != 0:
        print(f"Failed to fetch script via: {fetch_command}")
        return fetch_completed.returncode
    completed = subprocess.run(["bash", str(tmp_script)], check=False, env={**os.environ, **env_vars})
    return completed.returncode


def _record_install_job(root, args: argparse.Namespace, *, action: str, summary: str, payload: dict[str, object]) -> str:
    return create_job(
        root,
        args,
        command_family="install",
        action=action,
        status="planned",
        summary=summary,
        details=payload,
    )


def run_install_server_dependencies(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_TARGET_STACK": "frappe-v16",
        "THREEPLUG_INSTALL_PRODUCTION_TOOLS": "1" if args.production_tools else "0",
    }
    script_path = root / "scripts" / "linux" / "install_server_dependencies.sh"
    command = _render_script_command(script_path, env_vars)
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
    job_id = _record_install_job(
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
        code = _execute_script_with_fetch(script_path, env_vars, str(payload["fetch_command"]))
        update_job(root, args, job_id=job_id, status="completed" if code == 0 else "failed", details={**payload, "exit_code": code})
        return code
    return 0


def run_install_bench(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_USER": args.user,
        "THREEPLUG_BENCH_SOURCE": args.bench_source,
    }
    script_path = root / "scripts" / "linux" / "install_bench.sh"
    command = _render_script_command(script_path, env_vars)
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
    job_id = _record_install_job(
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
        code = _execute_script_with_fetch(script_path, env_vars, str(payload["fetch_command"]))
        update_job(root, args, job_id=job_id, status="completed" if code == 0 else "failed", details={**payload, "exit_code": code})
        return code
    return 0
