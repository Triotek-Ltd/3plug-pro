from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import tomllib
import unittest
from unittest import mock
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_ROOT = REPO_ROOT / "cli"
if str(CLI_ROOT) not in sys.path:
    sys.path.insert(0, str(CLI_ROOT))

from threeplugpro.cli import main  # noqa: E402
from threeplugpro.commands.server.handlers import _run_first_available  # noqa: E402


class CliSmokeTests(unittest.TestCase):
    def run_cli(self, *args: str) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = main(["--root", str(REPO_ROOT), *args])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_console_entry_points_are_declared(self) -> None:
        pyproject = tomllib.loads((CLI_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        scripts = pyproject["project"]["scripts"]

        self.assertEqual(scripts["3plug"], "threeplugpro.cli:main")
        self.assertEqual(scripts["3plug-pro"], "threeplugpro.cli:main")

    def test_doctor_smoke(self) -> None:
        code, stdout, stderr = self.run_cli("doctor")

        self.assertEqual(code, 0, stderr)
        self.assertIn("3plug-pro doctor", stdout)
        self.assertIn("app catalog", stdout)

    def test_json_app_show_smoke(self) -> None:
        code, stdout, stderr = self.run_cli("--format", "json", "app", "show", "erpnext")

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["repo"], "triotek-erpnext")
        self.assertEqual(payload["branch"], "main")
        self.assertEqual(payload["upstream_tracking_branch"], "upstream-v16")

    def test_json_app_show_uses_packaged_catalog_without_repo_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = main(
                    [
                        "--root",
                        tmp,
                        "--format",
                        "json",
                        "app",
                        "show",
                        "erpnext",
                    ]
                )

            self.assertEqual(code, 0, stderr.getvalue())
            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["repo"], "triotek-erpnext")

    def test_json_stack_list_smoke(self) -> None:
        code, stdout, stderr = self.run_cli("--format", "json", "stack", "list")

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertTrue(any(stack["key"] == "erpnext-core" for stack in payload))

    def test_server_bootstrap_smoke(self) -> None:
        code, stdout, stderr = self.run_cli("server", "bootstrap")

        self.assertEqual(code, 0, stderr)
        self.assertIn("3plug server bootstrap", stdout)
        self.assertIn("bootstrap_3plug_server.sh", stdout)
        self.assertIn("Local execute command:", stdout)

    def test_json_server_update_smoke(self) -> None:
        code, stdout, stderr = self.run_cli("--format", "json", "server", "update")

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["action"], "update")
        self.assertTrue(payload["script_exists"])
        self.assertTrue(payload["preserves_workspace_state"])
        self.assertIn("THREEPLUG_PACKAGE_URL", payload["env"])
        self.assertTrue(payload["requires_git_identity"])

    def test_json_server_uninstall_smoke(self) -> None:
        code, stdout, stderr = self.run_cli("--format", "json", "server", "uninstall")

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["action"], "uninstall")
        self.assertTrue(payload["script_exists"])
        self.assertTrue(payload["requires_confirmation"])

    def test_json_server_bootstrap_with_options_smoke(self) -> None:
        code, stdout, stderr = self.run_cli(
            "--format",
            "json",
            "server",
            "bootstrap",
            "--no-firewall-enable",
            "--user",
            "ops",
        )

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["operator_user"], "ops")
        self.assertEqual(payload["env"]["FIREWALL_AUTO_ENABLE"], "0")
        self.assertTrue(payload["requires_interactive_password_prompt"])

    def test_json_server_git_setup_smoke(self) -> None:
        code, stdout, stderr = self.run_cli(
            "--format",
            "json",
            "server",
            "git-setup",
            "--user",
            "ops",
            "--git-name",
            "Ops User",
            "--git-email",
            "ops@example.com",
        )

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["action"], "git-setup")
        self.assertTrue(payload["script_exists"])
        self.assertEqual(payload["operator_user"], "ops")
        self.assertEqual(payload["env"]["THREEPLUG_GIT_NAME"], "Ops User")
        self.assertEqual(payload["env"]["THREEPLUG_GIT_EMAIL"], "ops@example.com")

    def test_json_server_install_cli_smoke(self) -> None:
        code, stdout, stderr = self.run_cli(
            "--format",
            "json",
            "server",
            "install-cli",
            "--user",
            "ops",
        )

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["action"], "install-cli")
        self.assertTrue(payload["script_exists"])
        self.assertEqual(payload["operator_user"], "ops")
        self.assertTrue(payload["requires_git_identity"])
        self.assertIn("THREEPLUG_PACKAGE_URL", payload["env"])

    def test_json_install_server_dependencies_smoke(self) -> None:
        code, stdout, stderr = self.run_cli("--format", "json", "install", "server-dependencies")

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["action"], "server-dependencies")
        self.assertTrue(payload["script_exists"])
        self.assertTrue(payload["requires_explicit_execution"])
        self.assertIn("wkhtmltopdf", payload["installs"])
        self.assertIn("python3-venv", payload["installs"])
        self.assertIn("apache2", payload["production_conflicts_checked"])

    def test_json_install_server_dependencies_with_production_tools_smoke(self) -> None:
        code, stdout, stderr = self.run_cli(
            "--format",
            "json",
            "install",
            "server-dependencies",
            "--production-tools",
        )

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["env"]["THREEPLUG_INSTALL_PRODUCTION_TOOLS"], "1")
        self.assertIn("nginx", payload["production_installs"])

    def test_json_install_bench_smoke(self) -> None:
        code, stdout, stderr = self.run_cli("--format", "json", "install", "bench", "--user", "ops")

        self.assertEqual(code, 0, stderr)
        payload = json.loads(stdout)
        self.assertEqual(payload["action"], "bench")
        self.assertTrue(payload["script_exists"])
        self.assertEqual(payload["env"]["THREEPLUG_USER"], "ops")
        self.assertTrue(payload["requires_git_identity"])

    def test_init_uses_config_and_data_overrides(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config_path = root / "local-config.json"
            data_dir = root / "local-data"
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = main(
                    [
                        "--root",
                        str(root),
                        "--config-path",
                        str(config_path),
                        "--data-dir",
                        str(data_dir),
                        "--format",
                        "json",
                        "init",
                    ]
                )

            self.assertEqual(code, 0, stderr.getvalue())
            self.assertTrue(config_path.exists())
            self.assertTrue(data_dir.exists())
            payload = json.loads(stdout.getvalue())
            self.assertEqual(Path(payload["config_path"]).resolve(), config_path.resolve())
            self.assertEqual(Path(payload["data_dir"]).resolve(), data_dir.resolve())
            self.assertTrue(Path(payload["state_db"]).exists())

    def test_server_commands_create_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                init_code = main(["--root", str(root), "--format", "json", "init"])
            self.assertEqual(init_code, 0, stderr.getvalue())

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                code = main(["--root", str(root), "--format", "json", "server", "update"])
            self.assertEqual(code, 0, stderr.getvalue())
            payload = json.loads(stdout.getvalue())
            self.assertIn("job_id", payload)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                list_code = main(["--root", str(root), "--format", "json", "job", "list"])
            self.assertEqual(list_code, 0, stderr.getvalue())
            list_payload = json.loads(stdout.getvalue())
            self.assertTrue(any(job["id"] == payload["job_id"] for job in list_payload["jobs"]))

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                show_code = main(["--root", str(root), "--format", "json", "job", "show", payload["job_id"]])
            self.assertEqual(show_code, 0, stderr.getvalue())
            show_payload = json.loads(stdout.getvalue())
            self.assertEqual(show_payload["id"], payload["job_id"])
            self.assertEqual(show_payload["action"], "update")
            self.assertTrue(len(show_payload["audit_events"]) >= 1)

    def test_preflight_command_fallback_uses_python3_when_python_missing(self) -> None:
        def fake_run_command(command: list[str]) -> tuple[int, str]:
            if command == ["python", "--version"]:
                return 127, ""
            if command == ["python3", "--version"]:
                return 0, "Python 3.12.3"
            return 127, ""

        with mock.patch("threeplugpro.commands.server.handlers.run_command", side_effect=fake_run_command):
            code, output, used_command = _run_first_available(
                [["python", "--version"], ["python3", "--version"]]
            )

        self.assertEqual(code, 0)
        self.assertEqual(output, "Python 3.12.3")
        self.assertEqual(used_command, ["python3", "--version"])


if __name__ == "__main__":
    unittest.main()
