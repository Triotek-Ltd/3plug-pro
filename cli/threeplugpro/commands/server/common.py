from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile

from threeplugpro.core import create_job


def server_script_payload(root, script_name: str, purpose: str, extra: dict[str, object] | None = None) -> dict[str, object]:
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


def render_env_prefix(env_vars: dict[str, str]) -> str:
    parts = []
    for key, value in env_vars.items():
        escaped = value.replace('"', '\\"')
        parts.append(f'{key}="{escaped}"')
    return " ".join(parts)


def render_script_command(script_path, env_vars: dict[str, str]) -> str:
    prefix = render_env_prefix(env_vars)
    if prefix:
        return f"sudo env {prefix} bash {script_path}"
    return f"sudo bash {script_path}"


def execute_server_script(script_path, env_vars: dict[str, str]) -> int:
    completed = subprocess.run(
        ["bash", str(script_path)],
        check=False,
        env={**os.environ, **env_vars},
    )
    return completed.returncode


def execute_server_script_with_fetch(script_path: Path, env_vars: dict[str, str], fetch_command: str) -> int:
    if script_path.exists():
        return execute_server_script(script_path, env_vars)

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
    return execute_server_script(tmp_script, env_vars)


def record_server_job(root, args, *, action: str, summary: str, payload: dict[str, object]) -> str:
    return create_job(
        root,
        args,
        command_family="server",
        action=action,
        status="planned",
        summary=summary,
        details=payload,
    )
