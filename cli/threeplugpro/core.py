from __future__ import annotations

import argparse
from importlib import resources
import json
from pathlib import Path
import sqlite3
import shutil
import subprocess
from datetime import datetime, timezone
from typing import Any, Iterable
from uuid import uuid4


PROJECT_MARKERS = ("README.md", "design", "config", "cli")
APP_CATALOG = Path("config") / "app-catalog.json"
UPSTREAM_APPS = Path("config") / "upstream-apps.json"
LOCAL_STATE_DIR = ".3plug"
LOCAL_CONFIG_FILE = "config.json"
LOCAL_DATA_DIR = "data"
STATE_DB_FILE = "state.db"


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
    if manifest.exists():
        return json.loads(manifest.read_text(encoding="utf-8"))

    fallback = {
        APP_CATALOG: "app-catalog.json",
        UPSTREAM_APPS: "upstream-apps.json",
    }.get(path)
    if fallback is None:
        return json.loads(manifest.read_text(encoding="utf-8"))

    data = resources.files("threeplugpro.data").joinpath(fallback).read_text(encoding="utf-8")
    return json.loads(data)


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


def state_db_path(root: Path, args: argparse.Namespace) -> Path:
    return local_data_dir(root, args) / STATE_DB_FILE


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_state_db(root: Path, args: argparse.Namespace) -> Path:
    data_dir = local_data_dir(root, args)
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = state_db_path(root, args)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                command_family TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT NOT NULL,
                summary TEXT NOT NULL,
                details_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS audit_events (
                id TEXT PRIMARY KEY,
                job_id TEXT,
                event_type TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(job_id) REFERENCES jobs(id)
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS benches (
                name TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                status TEXT NOT NULL,
                frappe_path TEXT NOT NULL,
                frappe_branch TEXT NOT NULL,
                bench_source TEXT NOT NULL,
                python_executable TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()
    return db_path


def create_job(
    root: Path,
    args: argparse.Namespace,
    *,
    command_family: str,
    action: str,
    status: str,
    summary: str,
    details: dict[str, Any],
) -> str:
    db_path = ensure_state_db(root, args)
    now = utc_now()
    job_id = uuid4().hex
    payload = json.dumps(details, default=str)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO jobs (id, command_family, action, status, summary, details_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (job_id, command_family, action, status, summary, payload, now, now),
        )
        conn.execute(
            """
            INSERT INTO audit_events (id, job_id, event_type, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                uuid4().hex,
                job_id,
                "job.created",
                json.dumps({"status": status, "summary": summary}, default=str),
                now,
            ),
        )
        conn.commit()
    finally:
        conn.close()
    return job_id


def update_job(
    root: Path,
    args: argparse.Namespace,
    *,
    job_id: str,
    status: str,
    details: dict[str, Any],
) -> None:
    db_path = ensure_state_db(root, args)
    now = utc_now()
    payload = json.dumps(details, default=str)
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            UPDATE jobs
            SET status = ?, details_json = ?, updated_at = ?
            WHERE id = ?
            """,
            (status, payload, now, job_id),
        )
        conn.execute(
            """
            INSERT INTO audit_events (id, job_id, event_type, payload_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                uuid4().hex,
                job_id,
                "job.updated",
                json.dumps({"status": status}, default=str),
                now,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def list_jobs(root: Path, args: argparse.Namespace) -> list[dict[str, Any]]:
    db_path = ensure_state_db(root, args)
    conn = sqlite3.connect(db_path)
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, command_family, action, status, summary, details_json, created_at, updated_at
            FROM jobs
            ORDER BY created_at DESC
            """
        ).fetchall()
    finally:
        conn.close()
    jobs: list[dict[str, Any]] = []
    for row in rows:
        jobs.append(
            {
                "id": row["id"],
                "command_family": row["command_family"],
                "action": row["action"],
                "status": row["status"],
                "summary": row["summary"],
                "details": json.loads(row["details_json"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
            }
        )
    return jobs


def get_job(root: Path, args: argparse.Namespace, job_id: str) -> dict[str, Any] | None:
    db_path = ensure_state_db(root, args)
    conn = sqlite3.connect(db_path)
    try:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT id, command_family, action, status, summary, details_json, created_at, updated_at
            FROM jobs
            WHERE id = ?
            """,
            (job_id,),
        ).fetchone()
        if row is None:
            return None
        audit_rows = conn.execute(
            """
            SELECT id, event_type, payload_json, created_at
            FROM audit_events
            WHERE job_id = ?
            ORDER BY created_at ASC
            """,
            (job_id,),
        ).fetchall()
    finally:
        conn.close()
    return {
        "id": row["id"],
        "command_family": row["command_family"],
        "action": row["action"],
        "status": row["status"],
        "summary": row["summary"],
        "details": json.loads(row["details_json"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "audit_events": [
            {
                "id": audit_row["id"],
                "event_type": audit_row["event_type"],
                "payload": json.loads(audit_row["payload_json"]),
                "created_at": audit_row["created_at"],
            }
            for audit_row in audit_rows
        ],
    }


def upsert_bench(
    root: Path,
    args: argparse.Namespace,
    *,
    name: str,
    path: Path,
    status: str,
    frappe_path: str,
    frappe_branch: str,
    bench_source: str,
    python_executable: str | None,
) -> None:
    db_path = ensure_state_db(root, args)
    now = utc_now()
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO benches (
                name, path, status, frappe_path, frappe_branch, bench_source, python_executable, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                path = excluded.path,
                status = excluded.status,
                frappe_path = excluded.frappe_path,
                frappe_branch = excluded.frappe_branch,
                bench_source = excluded.bench_source,
                python_executable = excluded.python_executable,
                updated_at = excluded.updated_at
            """,
            (
                name,
                str(path),
                status,
                frappe_path,
                frappe_branch,
                bench_source,
                python_executable,
                now,
                now,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def list_bench_records(root: Path, args: argparse.Namespace) -> list[dict[str, Any]]:
    db_path = ensure_state_db(root, args)
    conn = sqlite3.connect(db_path)
    try:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT name, path, status, frappe_path, frappe_branch, bench_source, python_executable, created_at, updated_at
            FROM benches
            ORDER BY name ASC
            """
        ).fetchall()
    finally:
        conn.close()
    return [
        {
            "name": row["name"],
            "path": row["path"],
            "status": row["status"],
            "frappe_path": row["frappe_path"],
            "frappe_branch": row["frappe_branch"],
            "bench_source": row["bench_source"],
            "python_executable": row["python_executable"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
        for row in rows
    ]


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
    except OSError as exc:
        return 126, str(exc)
    output = (completed.stdout or completed.stderr).strip()
    return completed.returncode, output.splitlines()[0] if output else ""
