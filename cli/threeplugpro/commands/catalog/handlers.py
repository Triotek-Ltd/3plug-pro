from __future__ import annotations

import argparse
import json
import sys

from threeplugpro.core import APP_CATALOG, load_json, output_json, resolve_root


def run_app_list(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    catalog = load_json(root, APP_CATALOG)
    apps = [
        app
        for app in catalog["apps"]
        if args.all or app.get("installable_with_get_app", False)
    ]
    if output_json(args, apps):
        return 0

    print("3plug-pro app catalog")
    for app in apps:
        status = app.get("status", "")
        branch = app.get("branch", catalog["defaults"]["branch"])
        print(f"- {app['key']}: {app['repo']} [{branch}] app={app['app_name']} status={status}")
    return 0


def run_app_show(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    catalog = load_json(root, APP_CATALOG)
    target = args.app
    for app in catalog["apps"]:
        if target in {app["key"], app["repo"], app["app_name"]}:
            if output_json(args, app):
                return 0
            print(json.dumps(app, indent=2))
            return 0
    print(f"No app found for {target}", file=sys.stderr)
    return 1


def run_stack_list(args: argparse.Namespace) -> int:
    root = resolve_root(args)
    catalog = load_json(root, APP_CATALOG)
    stacks = catalog.get("stacks", [])
    if output_json(args, stacks):
        return 0

    print("3plug-pro stacks")
    for stack in stacks:
        apps = ", ".join(stack.get("apps", []))
        print(f"- {stack['key']}: {stack['label']} [{apps}]")
    return 0
