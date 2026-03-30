from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="3plug-pro",
        description="3plug-pro CLI for Triotek platform setup and governance tasks.",
    )
    subparsers = parser.add_subparsers(dest="command")

    doctor = subparsers.add_parser("doctor", help="Check local workspace expectations.")
    doctor.set_defaults(handler=run_doctor)

    repos = subparsers.add_parser("repos", help="Repo-plan helper commands.")
    repos_sub = repos.add_subparsers(dest="repos_command")

    repos_list = repos_sub.add_parser("list", help="List planned repo documents.")
    repos_list.set_defaults(handler=run_repos_list)

    publish = subparsers.add_parser("publish", help="Publishing helper commands.")
    publish_sub = publish.add_subparsers(dest="publish_command")

    publish_plan = publish_sub.add_parser("plan", help="Show publish-plan files.")
    publish_plan.set_defaults(handler=run_publish_plan)

    auth = subparsers.add_parser("auth", help="Auth helper commands.")
    auth_sub = auth.add_subparsers(dest="auth_command")

    auth_status = auth_sub.add_parser("status", help="Show auth guidance file.")
    auth_status.set_defaults(handler=run_auth_status)

    return parser


def run_doctor(_args: argparse.Namespace) -> int:
    base = Path.cwd()
    expected = [
        base / "rnd" / "3plug",
        base / "rnd" / "3plug-pro-root",
        base / "rnd" / "3plug" / "sources" / "upstream-mirrors",
        base / "rnd" / "3plug" / "sources" / "triotek-native",
        base / "rnd" / "3plug" / "sources" / "catalog",
    ]
    print("3plug-pro doctor")
    for path in expected:
        state = "OK" if path.exists() else "MISSING"
        print(f"{state} {path}")
    return 0


def run_repos_list(_args: argparse.Namespace) -> int:
    print("See repo plan files:")
    print(" - rnd/3plug/repo-plan.md")
    print(" - rnd/3plug/app-catalog.md")
    print(" - rnd/3plug/github-org-plan.md")
    return 0


def run_publish_plan(_args: argparse.Namespace) -> int:
    print("See publish files:")
    print(" - rnd/3plug/github-publish-checklist.md")
    print(" - rnd/3plug/publish-status.md")
    print(" - rnd/3plug-pro-root/PUBLISHING.md")
    return 0


def run_auth_status(_args: argparse.Namespace) -> int:
    print("See auth guidance:")
    print(" - rnd/3plug-pro-root/CLI_AUTH.md")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 1
    return handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
