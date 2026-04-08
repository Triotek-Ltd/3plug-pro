from __future__ import annotations

import argparse
import json
import shutil

from threeplugpro.core import (
    APP_CATALOG,
    ensure_state_db,
    local_config_path,
    local_data_dir,
    local_state_dir,
    output_json,
    print_check,
    resolve_root,
)


def run_doctor(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    expected = [
        ("repo root", root / "README.md"),
        ("design folder", root / "design"),
        ("roadmap", root / "design" / "roadmap.md"),
        ("app catalog", root / APP_CATALOG),
        ("source workspace", root / "3plug" / "repos"),
        ("platform sources", root / "3plug" / "repos" / "platform"),
        ("triotek-bench source", root / "3plug" / "repos" / "platform" / "triotek-bench"),
        ("press reference", root / "3plug" / "repos" / "platform" / "frappe-press"),
        ("apps-core sources", root / "3plug" / "repos" / "apps-core"),
        ("apps-vertical sources", root / "3plug" / "repos" / "apps-vertical"),
    ]

    print("3plug-pro doctor")
    print(f"root {root}")
    results = [print_check(label, path.exists(), path) for label, path in expected]

    bench = shutil.which("bench")
    print_check("bench executable", bench is not None, bench or "not on PATH")

    return 0 if all(results) else 1


def run_init(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    state_dir = local_state_dir(root)
    config_path = local_config_path(root, args)
    data_dir = local_data_dir(root, args)

    state_dir.mkdir(exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = ensure_state_db(root, args)

    if not config_path.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(
            json.dumps(
                {
                    "version": 1,
                    "target_stack": "frappe-v16",
                    "install_branch": "main",
                    "upstream_tracking_branch": "upstream-v16",
                    "data_dir": str(data_dir),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    (state_dir / "README.md").write_text(
        "# Local 3plug-pro State\n\nThis folder is generated locally and ignored by git.\n",
        encoding="utf-8",
    )

    payload = {
        "state_dir": state_dir,
        "config_path": config_path,
        "data_dir": data_dir,
        "state_db": db_path,
    }
    if output_json(args, payload):
        return 0

    print(f"Initialized local state at {state_dir}")
    print(f"Local config: {config_path}")
    print(f"Local data: {data_dir}")
    print(f"Local state DB: {db_path}")
    return 0
