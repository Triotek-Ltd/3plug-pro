from __future__ import annotations

import argparse
import os
import platform
import subprocess

from threeplugpro.core import create_job, output_json, resolve_root, run_command, update_job


def _server_script_payload(root, script_name: str, purpose: str, extra: dict[str, object] | None = None) -> dict[str, object]:
    script_path = root / "scripts" / "linux" / script_name
    payload: dict[str, object] = {
        "implemented": True,
        "command_family": "server",
        "action": purpose,
        "script_path": script_path,
        "script_exists": script_path.exists(),
    }
    if extra:
        payload.update(extra)
    return payload


def _render_env_prefix(env_vars: dict[str, str]) -> str:
    parts = []
    for key, value in env_vars.items():
        escaped = value.replace('"', '\\"')
        parts.append(f'{key}="{escaped}"')
    return " ".join(parts)


def _render_script_command(script_path, env_vars: dict[str, str]) -> str:
    prefix = _render_env_prefix(env_vars)
    if prefix:
        return f"sudo env {prefix} bash {script_path}"
    return f"sudo bash {script_path}"


def _execute_server_script(script_path, env_vars: dict[str, str]) -> int:
    command_env = {**env_vars}
    completed = subprocess.run(
        ["bash", str(script_path)],
        check=False,
        env={**os.environ, **command_env},
    )
    return completed.returncode


def _record_server_job(
    root,
    args: argparse.Namespace,
    *,
    action: str,
    summary: str,
    payload: dict[str, object],
) -> str:
    return create_job(
        root,
        args,
        command_family="server",
        action=action,
        status="planned",
        summary=summary,
        details=payload,
    )


def run_server_bootstrap(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_USER": args.user,
        "THREEPLUG_WORKDIR": args.workdir,
        "SSH_UFW_PROFILE": args.ssh_ufw_profile,
        "FIREWALL_AUTO_ENABLE": "0" if args.no_firewall_enable else "1",
        "THREEPLUG_SET_PASSWORD": "1" if args.set_password else "0",
    }
    command = _render_script_command(root / "scripts" / "linux" / "bootstrap_3plug_server.sh", env_vars)
    payload = _server_script_payload(
        root,
        "bootstrap_3plug_server.sh",
        "bootstrap",
        {
            "workspace": args.workdir,
            "operator_user": args.user,
            "supports_interactive_password_prompt": True,
            "password_prompt_env": "THREEPLUG_SET_PASSWORD=1",
            "execute": args.execute,
            "env": env_vars,
            "fetch_command": "curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/bootstrap_3plug_server.sh -o /tmp/bootstrap_3plug_server.sh",
            "run_command": command.replace(str(root / "scripts" / "linux" / "bootstrap_3plug_server.sh"), "/tmp/bootstrap_3plug_server.sh"),
            "local_execute_command": command,
        },
    )
    job_id = _record_server_job(
        root,
        args,
        action="bootstrap",
        summary="Prepare a server so 3plug can run.",
        payload=payload,
    )
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
        print("Executing local bootstrap script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = _execute_server_script(payload["script_path"], env_vars)
        update_job(
            root,
            args,
            job_id=job_id,
            status="completed" if code == 0 else "failed",
            details={**payload, "exit_code": code},
        )
        return code
    return 0


def run_server_update(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_USER": args.user,
        "THREEPLUG_WORKDIR": args.workdir,
        "THREEPLUG_PACKAGE_URL": args.package_url,
    }
    command = _render_script_command(root / "scripts" / "linux" / "update_3plug_server.sh", env_vars)
    payload = _server_script_payload(
        root,
        "update_3plug_server.sh",
        "update",
        {
            "operator_user": args.user,
            "workspace": args.workdir,
            "execute": args.execute,
            "env": env_vars,
            "fetch_command": "curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/update_3plug_server.sh -o /tmp/update_3plug_server.sh",
            "run_command": command.replace(str(root / "scripts" / "linux" / "update_3plug_server.sh"), "/tmp/update_3plug_server.sh"),
            "local_execute_command": command,
            "preserves_workspace_state": True,
        },
    )
    job_id = _record_server_job(
        root,
        args,
        action="update",
        summary="Update the installed 3plug CLI on an existing server.",
        payload=payload,
    )
    payload["job_id"] = job_id
    if output_json(args, payload):
        return 0

    print("3plug server update")
    print(f"job {job_id}")
    print(f"script {payload['script_path']}")
    print("Use this to refresh the installed 3plug CLI on an existing server.")
    print(f"Fetch: {payload['fetch_command']}")
    print(f"Run: {payload['run_command']}")
    print(f"Local execute command: {payload['local_execute_command']}")
    if args.execute:
        print("Executing local update script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = _execute_server_script(payload["script_path"], env_vars)
        update_job(
            root,
            args,
            job_id=job_id,
            status="completed" if code == 0 else "failed",
            details={**payload, "exit_code": code},
        )
        return code
    return 0


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
    command = _render_script_command(root / "scripts" / "linux" / "uninstall_3plug_server.sh", env_vars)
    payload = _server_script_payload(
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
    job_id = _record_server_job(
        root,
        args,
        action="uninstall",
        summary="Remove the managed 3plug footprint from a server.",
        payload=payload,
    )
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
        print("Executing local uninstall script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = _execute_server_script(payload["script_path"], env_vars)
        update_job(
            root,
            args,
            job_id=job_id,
            status="completed" if code == 0 else "failed",
            details={**payload, "exit_code": code},
        )
        return code
    return 0


def run_server_preflight(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    checks = [
        ("os", ["cmd", "/c", "ver"] if platform.system() == "Windows" else ["uname", "-a"]),
        ("git", ["git", "--version"]),
        ("python", ["python", "--version"]),
        ("uv", ["uv", "--version"]),
        ("pip", ["pip", "--version"]),
        ("node", ["node", "--version"]),
        ("npm", ["npm", "--version"]),
        ("yarn", ["yarn", "--version"]),
        ("redis", ["redis-server", "--version"]),
        ("mariadb", ["mariadb", "--version"]),
        ("mysql", ["mysql", "--version"]),
        ("wkhtmltopdf", ["wkhtmltopdf", "--version"]),
        ("nginx", ["nginx", "-v"]),
        ("supervisord", ["supervisord", "--version"]),
    ]

    payload: dict[str, object] = {
        "implemented": True,
        "command_family": "server",
        "action": "preflight",
        "target_stack": "frappe-v16",
        "checks": [],
    }
    job_id = _record_server_job(
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
    for label, command in checks:
        code, output = run_command(command)
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
                "command": command,
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
