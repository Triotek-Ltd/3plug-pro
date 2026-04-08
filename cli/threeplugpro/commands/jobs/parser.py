from __future__ import annotations

import argparse

from threeplugpro.commands.jobs.handlers import run_job_list, run_job_show


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    job = subparsers.add_parser("job", help="Job helper commands.")
    job_sub = job.add_subparsers(dest="job_command")

    job_list = job_sub.add_parser("list", help="List local jobs.")
    job_list.set_defaults(handler=run_job_list)

    job_show = job_sub.add_parser("show", help="Show one local job.")
    job_show.add_argument("job_id")
    job_show.set_defaults(handler=run_job_show)
