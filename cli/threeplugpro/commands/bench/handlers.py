from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import tempfile

from threeplugpro.core import (
    create_job,
    list_bench_records,
    output_json,
    resolve_root,
    update_job,
    upsert_bench,
)


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


def _default_bench_path(root: Path, bench_name: str) -> Path:
    return root / "benches" / bench_name


def _approved_bench_root(root: Path) -> Path:
    return root / "benches"


def _path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def run_bench_create(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    bench_path = Path(args.path).resolve() if args.path else _default_bench_path(root, args.name).resolve()
    bench_root = _approved_bench_root(root).resolve()

    payload = {
        "implemented": True,
        "command_family": "bench",
        "action": "create",
        "bench_name": args.name,
        "bench_path": bench_path,
        "bench_root": bench_root,
        "operator_user": args.user,
        "workdir": args.workdir,
        "frappe_path": args.frappe_path,
        "frappe_branch": args.frappe_branch,
        "python_executable": args.python_executable,
        "skip_assets": args.skip_assets,
        "no_backups": args.no_backups,
        "dev": args.dev,
        "execute": args.execute,
        "path_is_within_approved_root": _path_is_within(bench_path, bench_root),
    }

    env_vars = {
        "THREEPLUG_USER": args.user,
        "THREEPLUG_WORKDIR": args.workdir,
        "THREEPLUG_BENCH_NAME": args.name,
        "THREEPLUG_BENCH_PATH": str(bench_path),
        "THREEPLUG_BENCH_ROOT": str(bench_root),
        "THREEPLUG_FRAPPE_PATH": args.frappe_path,
        "THREEPLUG_FRAPPE_BRANCH": args.frappe_branch,
        "THREEPLUG_BENCH_SKIP_ASSETS": "1" if args.skip_assets else "0",
        "THREEPLUG_BENCH_NO_BACKUPS": "1" if args.no_backups else "0",
        "THREEPLUG_BENCH_DEV": "1" if args.dev else "0",
    }
    if args.python_executable:
        env_vars["THREEPLUG_BENCH_PYTHON"] = args.python_executable

    script_path = root / "scripts" / "linux" / "create_bench.sh"
    command = _render_script_command(script_path, env_vars)
    payload.update(
        {
            "script_path": script_path,
            "script_exists": script_path.exists(),
            "env": env_vars,
            "fetch_command": "curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/create_bench.sh -o /tmp/create_bench.sh",
            "run_command": command.replace(str(script_path), "/tmp/create_bench.sh"),
            "local_execute_command": command,
            "requires_bench_install": True,
            "requires_git_identity": True,
        }
    )

    job_id = create_job(
        root,
        args,
        command_family="bench",
        action="create",
        status="planned",
        summary=f"Create managed bench {args.name}.",
        details=payload,
    )
    payload["job_id"] = job_id

    if output_json(args, payload):
        return 0

    print(f"3plug bench create {args.name}")
    print(f"job {job_id}")
    print(f"script {script_path}")
    if not payload["path_is_within_approved_root"]:
        print(f"Bench path must stay within the approved bench root: {bench_root}")
        return 1
    print("Use this to create one managed Bench runtime.")
    print(f"Fetch: {payload['fetch_command']}")
    print(f"Run: {payload['run_command']}")
    print(f"Local execute command: {payload['local_execute_command']}")
    if args.execute:
        print("Executing bench create script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = _execute_script_with_fetch(script_path, env_vars, str(payload["fetch_command"]))
        if code == 0:
            upsert_bench(
                root,
                args,
                name=args.name,
                path=bench_path,
                status="created",
                frappe_path=args.frappe_path,
                frappe_branch=args.frappe_branch,
                bench_source="triotek-bench",
                python_executable=args.python_executable,
            )
        update_job(root, args, job_id=job_id, status="completed" if code == 0 else "failed", details={**payload, "exit_code": code})
        return code
    return 0


def run_bench_list(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    benches = list_bench_records(root, args)
    payload = {
        "implemented": True,
        "benches": benches,
        "future_local_bench_root": _approved_bench_root(root),
    }
    if output_json(args, payload):
        return 0
    if not benches:
        print("No managed benches are recorded yet.")
        print(f"Expected bench root: {_approved_bench_root(root)}")
        return 0
    print("Managed benches")
    for bench in benches:
        print(f"- {bench['name']} {bench['status']} {bench['path']}")
    return 0
