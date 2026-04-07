from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any, Iterable


PROJECT_MARKERS = ("README.md", "design", "config", "cli")
APP_CATALOG = Path("config") / "app-catalog.json"
UPSTREAM_APPS = Path("config") / "upstream-apps.json"
LOCAL_STATE_DIR = ".3plug"
LOCAL_CONFIG_FILE = "config.json"
LOCAL_DATA_DIR = "data"


def resolve_root(args: argparse.Namespace) -> Path:
    if args.root is not None:
        return args.root.resolve()

    candidates = [Path.cwd(), *Path(__file__).resolve().parents]
    for candidate in candidates:
        if all((candidate / marker).exists() for marker in PROJECT_MARKERS):
            return candidate

    return Path.cwd()


def load_json(root: Path, path: Path) -> Any:
    manifest = path if path.is_absolute() else root / path
    return json.loads(manifest.read_text(encoding="utf-8"))


def local_state_dir(root: Path) -> Path:
    return root / LOCAL_STATE_DIR


def local_config_path(root: Path, args: argparse.Namespace) -> Path:
    if getattr(args, "config_path", None) is not None:
        return args.config_path.resolve()
    return local_state_dir(root) / LOCAL_CONFIG_FILE


def local_data_dir(root: Path, args: argparse.Namespace) -> Path:
    if getattr(args, "data_dir", None) is not None:
        return args.data_dir.resolve()
    return local_state_dir(root) / LOCAL_DATA_DIR


def output_json(args: argparse.Namespace, payload: Any) -> bool:
    if getattr(args, "output_format", "text") != "json":
        return False
    print(json.dumps(payload, indent=2, default=str))
    return True


def print_check(label: str, ok: bool, detail: str | Path = "") -> bool:
    state = "OK" if ok else "MISSING"
    suffix = f" {detail}" if detail else ""
    print(f"{state} {label}{suffix}")
    return ok


def run_command(args: Iterable[str]) -> tuple[int, str]:
    command = list(args)
    executable = shutil.which(command[0])
    if executable is None:
        return 127, ""
    command[0] = executable
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return 127, ""
    output = (completed.stdout or completed.stderr).strip()
    return completed.returncode, output.splitlines()[0] if output else ""
