from __future__ import annotations

import argparse
import os
import platform
from pathlib import Path
import subprocess
import tempfile

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


def _execute_server_script_with_fetch(script_path: Path, env_vars: dict[str, str], fetch_command: str) -> int:
    if script_path.exists():
        return _execute_server_script(script_path, env_vars)

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
    return _execute_server_script(tmp_script, env_vars)


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


def _run_first_available(commands: list[list[str]]) -> tuple[int, str, list[str]]:
    for command in commands:
        code, output = run_command(command)
        if code != 127:
            return code, output, command
    return 127, "", commands[0]


def run_server_bootstrap(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_USER": args.user,
        "THREEPLUG_WORKDIR": args.workdir,
        "SSH_UFW_PROFILE": args.ssh_ufw_profile,
        "FIREWALL_AUTO_ENABLE": "0" if args.no_firewall_enable else "1",
    }
    command = _render_script_command(root / "scripts" / "linux" / "bootstrap_3plug_server.sh", env_vars)
    payload = _server_script_payload(
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
        print("Executing bootstrap script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = _execute_server_script_with_fetch(payload["script_path"], env_vars, str(payload["fetch_command"]))
        update_job(
            root,
            args,
            job_id=job_id,
            status="completed" if code == 0 else "failed",
            details={**payload, "exit_code": code},
        )
        return code
    return 0


def run_server_git_setup(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_USER": args.user,
    }
    if args.git_name:
        env_vars["THREEPLUG_GIT_NAME"] = args.git_name
    if args.git_email:
        env_vars["THREEPLUG_GIT_EMAIL"] = args.git_email
    command = _render_script_command(root / "scripts" / "linux" / "configure_3plug_git.sh", env_vars)
    payload = _server_script_payload(
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
    job_id = _record_server_job(
        root,
        args,
        action="git-setup",
        summary="Configure Git identity for the operator user before install/update flows.",
        payload=payload,
    )
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
        code = _execute_server_script_with_fetch(payload["script_path"], env_vars, str(payload["fetch_command"]))
        update_job(
            root,
            args,
            job_id=job_id,
            status="completed" if code == 0 else "failed",
            details={**payload, "exit_code": code},
        )
        return code
    return 0


def run_server_install_cli(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    env_vars = {
        "THREEPLUG_USER": args.user,
        "THREEPLUG_PACKAGE_URL": args.package_url,
    }
    command = _render_script_command(root / "scripts" / "linux" / "install_3plug_cli.sh", env_vars)
    payload = _server_script_payload(
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
            "resolves_latest_release": args.package_url == "latest",
        },
    )
    job_id = _record_server_job(
        root,
        args,
        action="install-cli",
        summary="Install the 3plug CLI after Git identity is configured.",
        payload=payload,
    )
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
        code = _execute_server_script_with_fetch(payload["script_path"], env_vars, str(payload["fetch_command"]))
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
            "requires_git_identity": True,
            "resolves_latest_release": args.package_url == "latest",
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
        print("Executing update script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = _execute_server_script_with_fetch(payload["script_path"], env_vars, str(payload["fetch_command"]))
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
        print("Executing uninstall script.")
        update_job(root, args, job_id=job_id, status="running", details=payload)
        code = _execute_server_script_with_fetch(payload["script_path"], env_vars, str(payload["fetch_command"]))
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
        ("os", [["cmd", "/c", "ver"]] if platform.system() == "Windows" else [["uname", "-a"]]),
        ("git", [["git", "--version"]]),
        ("python", [["python", "--version"], ["python3", "--version"]]),
        ("uv", [["uv", "--version"]]),
        ("pip", [["pip", "--version"], ["pip3", "--version"]]),
        ("node", [["node", "--version"], ["nodejs", "--version"]]),
        ("npm", [["npm", "--version"]]),
        ("yarn", [["yarn", "--version"]]),
        ("redis", [["redis-server", "--version"], ["redis-cli", "--version"]]),
        ("mariadb", [["mariadb", "--version"], ["mariadb-admin", "--version"]]),
        ("mysql", [["mysql", "--version"]]),
        ("wkhtmltopdf", [["wkhtmltopdf", "--version"]]),
        ("nginx", [["nginx", "-v"]]),
        ("supervisord", [["supervisord", "--version"], ["supervisorctl", "--version"], ["systemctl", "--version"]]),
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
    for label, commands in checks:
        code, output, used_command = _run_first_available(commands)
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
                "command": used_command,
                "candidates": commands,
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
