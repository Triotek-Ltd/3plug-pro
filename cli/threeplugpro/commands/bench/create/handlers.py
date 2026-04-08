from __future__ import annotations

import argparse
from pathlib import Path

from threeplugpro.commands.bench.common import approved_bench_root, default_bench_path, execute_script_with_fetch, path_is_within, render_script_command
from threeplugpro.core import create_job, output_json, resolve_root, update_job, upsert_bench


def run_bench_create(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    bench_path = Path(args.path).resolve() if args.path else default_bench_path(root, args.name).resolve()
    bench_root = approved_bench_root(root).resolve()

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
        "path_is_within_approved_root": path_is_within(bench_path, bench_root),
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
    command = render_script_command(script_path, env_vars)
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
        code = execute_script_with_fetch(script_path, env_vars, str(payload["fetch_command"]))
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


__all__ = ["run_bench_create"]
