from __future__ import annotations

import argparse

from threeplugpro.commands.server.handlers import (
    run_server_bootstrap,
    run_server_git_setup,
    run_server_install_cli,
    run_server_preflight,
    run_server_uninstall,
    run_server_update,
)


def register(subparsers: argparse._SubParsersAction[argparse.ArgumentParser]) -> None:
    server = subparsers.add_parser("server", help="Managed server helper commands.")
    server_sub = server.add_subparsers(dest="server_command")

    server_preflight = server_sub.add_parser(
        "preflight",
        help="Check Frappe v16 non-Docker server prerequisites without installing.",
    )
    server_preflight.set_defaults(handler=run_server_preflight)

    server_bootstrap = server_sub.add_parser(
        "bootstrap",
        help="Show or execute the bootstrap flow for onboarding a server.",
    )
    server_bootstrap.add_argument(
        "--execute",
        action="store_true",
        help="Execute the local Linux bootstrap script instead of only printing guidance.",
    )
    server_bootstrap.add_argument("--user", default="threeplug", help="Operator user name.")
    server_bootstrap.add_argument(
        "--workdir",
        default="/opt/3plug-pro",
        help="Server workspace path managed by 3plug.",
    )
    server_bootstrap.add_argument(
        "--set-password",
        action="store_true",
        help="Prompt interactively for the operator password during bootstrap.",
    )
    server_bootstrap.add_argument(
        "--no-firewall-enable",
        action="store_true",
        help="Skip automatic UFW enablement in the bootstrap script.",
    )
    server_bootstrap.add_argument(
        "--ssh-ufw-profile",
        default="OpenSSH",
        help="UFW SSH profile to allow before firewall enablement.",
    )
    server_bootstrap.set_defaults(handler=run_server_bootstrap)

    server_git_setup = server_sub.add_parser(
        "git-setup",
        help="Show or execute Git identity setup for the operator user before install/update flows.",
    )
    server_git_setup.add_argument(
        "--execute",
        action="store_true",
        help="Execute the local Linux Git setup script instead of only printing guidance.",
    )
    server_git_setup.add_argument("--user", default="threeplug", help="Operator user name.")
    server_git_setup.add_argument("--git-name", default="", help="Git user.name to configure.")
    server_git_setup.add_argument("--git-email", default="", help="Git user.email to configure.")
    server_git_setup.set_defaults(handler=run_server_git_setup)

    server_install_cli = server_sub.add_parser(
        "install-cli",
        help="Show or execute the first 3plug CLI install flow after Git identity is configured.",
    )
    server_install_cli.add_argument(
        "--execute",
        action="store_true",
        help="Execute the local Linux install script instead of only printing guidance.",
    )
    server_install_cli.add_argument("--user", default="threeplug", help="Operator user name.")
    server_install_cli.add_argument(
        "--package-url",
        default="git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli",
        help="Package URL used to install the 3plug CLI.",
    )
    server_install_cli.set_defaults(handler=run_server_install_cli)

    server_update = server_sub.add_parser(
        "update",
        help="Show or execute the update flow for an existing server install.",
    )
    server_update.add_argument(
        "--execute",
        action="store_true",
        help="Execute the local Linux update script instead of only printing guidance.",
    )
    server_update.add_argument("--user", default="threeplug", help="Operator user name.")
    server_update.add_argument(
        "--workdir",
        default="/opt/3plug-pro",
        help="Server workspace path managed by 3plug.",
    )
    server_update.add_argument(
        "--package-url",
        default="git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli",
        help="Package URL used to update the installed 3plug CLI.",
    )
    server_update.set_defaults(handler=run_server_update)

    server_uninstall = server_sub.add_parser(
        "uninstall",
        help="Show or execute the uninstall flow for removing 3plug from a server.",
    )
    server_uninstall.add_argument(
        "--execute",
        action="store_true",
        help="Execute the local Linux uninstall script instead of only printing guidance.",
    )
    server_uninstall.add_argument("--user", default="threeplug", help="Operator user name.")
    server_uninstall.add_argument(
        "--workdir",
        default="/opt/3plug-pro",
        help="Server workspace path managed by 3plug.",
    )
    server_uninstall.add_argument(
        "--remove-user",
        action="store_true",
        help="Also remove the operator user and home directory.",
    )
    server_uninstall.add_argument(
        "--keep-workdir",
        action="store_true",
        help="Keep the managed workspace instead of removing it.",
    )
    server_uninstall.add_argument(
        "--keep-venv",
        action="store_true",
        help="Keep the operator virtual environment instead of removing it.",
    )
    server_uninstall.add_argument(
        "--force",
        action="store_true",
        help="Skip the uninstall confirmation prompt.",
    )
    server_uninstall.set_defaults(handler=run_server_uninstall)
