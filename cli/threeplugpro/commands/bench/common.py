from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile


def render_env_prefix(env_vars: dict[str, str]) -> str:
    parts = []
    for key, value in env_vars.items():
        escaped = value.replace('"', '\\"')
        parts.append(f'{key}="{escaped}"')
    return " ".join(parts)


def render_script_command(script_path: Path, env_vars: dict[str, str]) -> str:
    prefix = render_env_prefix(env_vars)
    if prefix:
        return f"sudo env {prefix} bash {script_path}"
    return f"sudo bash {script_path}"


def execute_script_with_fetch(script_path: Path, env_vars: dict[str, str], fetch_command: str) -> int:
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


def default_bench_path(root: Path, bench_name: str) -> Path:
    return root / "benches" / bench_name


def approved_bench_root(root: Path) -> Path:
    return root / "benches"


def path_is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False
