from threeplugpro.commands.server.bootstrap.handlers import run_server_bootstrap
from threeplugpro.commands.server.git_setup.handlers import run_server_git_setup
from threeplugpro.commands.server.install_cli.handlers import run_server_install_cli
from threeplugpro.commands.server.preflight.handlers import run_server_preflight
from threeplugpro.commands.server.uninstall.handlers import run_server_uninstall
from threeplugpro.commands.server.update.handlers import run_server_update
from threeplugpro.core import run_command


def _run_first_available(commands: list[list[str]]) -> tuple[int, str, list[str]]:
    for command in commands:
        code, output = run_command(command)
        if code != 127:
            return code, output, command
    return 127, "", commands[0]

__all__ = [
    "_run_first_available",
    "run_command",
    "run_server_bootstrap",
    "run_server_git_setup",
    "run_server_install_cli",
    "run_server_preflight",
    "run_server_uninstall",
    "run_server_update",
]
