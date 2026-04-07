from __future__ import annotations

import argparse

from threeplugpro.commands.planning.handlers import (
    run_auth_status,
    run_intake_batch,
    run_intake_plan,
    run_publish_plan,
    run_repos_list,
)
from threeplugpro.core import UPSTREAM_APPS


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
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

    intake = subparsers.add_parser("intake", help="Upstream intake helper commands.")
    intake_sub = intake.add_subparsers(dest="intake_command")

    intake_plan = intake_sub.add_parser("plan", help="Show upstream app intake plan.")
    intake_plan.add_argument(
        "--config",
        default=str(UPSTREAM_APPS),
        help="Path to upstream app manifest JSON.",
    )
    intake_plan.set_defaults(handler=run_intake_plan)

    intake_batch = intake_sub.add_parser("batch", help="Run batch upstream intake.")
    intake_batch.add_argument(
        "--config",
        default=str(UPSTREAM_APPS),
        help="Path to upstream app manifest JSON.",
    )
    intake_batch.add_argument(
        "--force-push",
        action="store_true",
        help="Force-push main and upstream-v16 to the org repos.",
    )
    intake_batch.set_defaults(handler=run_intake_batch)
