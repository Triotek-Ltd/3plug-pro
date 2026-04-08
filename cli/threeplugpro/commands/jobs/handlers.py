from __future__ import annotations

import argparse
import json
import sys

from threeplugpro.core import get_job, list_jobs, output_json, resolve_root


def run_job_list(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    jobs = list_jobs(root, args)
    payload = {"implemented": True, "jobs": jobs}
    if output_json(args, payload):
        return 0
    print("3plug jobs")
    if not jobs:
        print("No jobs recorded yet.")
        return 0
    for job in jobs:
        print(
            f"- {job['id']} {job['command_family']}/{job['action']} "
            f"status={job['status']} created={job['created_at']}"
        )
    return 0


def run_job_show(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    job = get_job(root, args, args.job_id)
    if job is None:
        print(f"No job found for {args.job_id}", file=sys.stderr)
        return 1
    if output_json(args, job):
        return 0
    print(f"Job {job['id']}")
    print(f"Command: {job['command_family']} {job['action']}")
    print(f"Status: {job['status']}")
    print(f"Created: {job['created_at']}")
    print(f"Updated: {job['updated_at']}")
    print("Details:")
    print(json.dumps(job["details"], indent=2))
    print("Audit events:")
    for event in job["audit_events"]:
        print(f"- {event['created_at']} {event['event_type']} {json.dumps(event['payload'])}")
    return 0
