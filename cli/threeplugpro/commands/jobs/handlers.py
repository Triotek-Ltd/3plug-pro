from __future__ import annotations

import argparse

from threeplugpro.core import output_json


def run_job_list(args: argparse.Namespace) -> int:
    payload = {"implemented": False, "jobs": []}
    if output_json(args, payload):
        return 0
    print("Local job store is not implemented yet.")
    return 0
