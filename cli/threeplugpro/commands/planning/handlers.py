from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from threeplugpro.core import load_json, resolve_root


def run_repos_list(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    print("See repo plan files:")
    for path in [
        root / "design" / "repo-plan.md",
        root / "design" / "app-catalog.md",
        root / "design" / "github-org-plan.md",
        root / "design" / "remote-repo-verification.md",
    ]:
        print(f" - {path}")
    return 0


def run_publish_plan(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    print("See publish files:")
    for path in [
        root / "design" / "github-publish-checklist.md",
        root / "design" / "publish-status.md",
        root / "PUBLISHING.md",
    ]:
        print(f" - {path}")
    return 0


def run_auth_status(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    print("See auth guidance:")
    print(f" - {root / 'CLI_AUTH.md'}")
    return 0


def run_intake_plan(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    config = Path(args.config)
    data = load_json(root, config)
    print("Upstream intake plan:")
    for entry in data:
        group = entry.get("repo_group", "apps-core")
        name = entry["name"]
        upstream = entry["upstream_url"]
        local_path = root / "3plug" / "repos" / group / name
        print(f"- {name}")
        print(f"  group: {group}")
        print(f"  upstream: {upstream}")
        print(f"  working-tree: {local_path}")
    return 0


def run_intake_batch(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    script = root / "scripts" / "intake_upstream_batch.ps1"
    config = Path(args.config)
    config_path = config if config.is_absolute() else root / config
    command = [
        "powershell",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        "-ConfigPath",
        str(config_path),
    ]
    if args.force_push:
        command.append("-ForcePush")
    completed = subprocess.run(command, check=False)
    return completed.returncode
