# 3plug-pro

3plug-pro is Triotek's managed operations layer for Frappe and ERPNext environments.

It is designed to give teams a safer, governed way to operate multiple Frappe sites through Bench while keeping source control, app selection, lifecycle actions, and auditability under Triotek control.

## What It Does

3plug-pro is being built as a Bench-first control plane:

```text
3plug-pro -> Bench -> multiple benches -> multiple Frappe/ERPNext sites
```

The goal is to support practical platform operations such as:

* preparing a Linux server for Frappe/ERPNext
* installing and managing Bench
* creating and registering multiple Bench environments
* installing approved Triotek apps from governed repositories
* creating, migrating, backing up, and restoring sites
* recording operational actions as jobs and audit history

## Install

Install the current CLI directly from GitHub:

```bash
python3 -m venv ~/.local/share/3plug-pro/venv
~/.local/share/3plug-pro/venv/bin/python -m pip install --upgrade pip
~/.local/share/3plug-pro/venv/bin/python -m pip install "git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli"
export PATH="$HOME/.local/share/3plug-pro/venv/bin:$PATH"
```

Then verify the CLI:

```bash
3plug --help
```

The compatibility command is also available:

```bash
3plug-pro --help
```

## First Server Check

On a new Ubuntu/Debian server, bootstrap the operator user and workspace first:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/bootstrap_3plug_server.sh -o /tmp/bootstrap_3plug_server.sh
sudo bash /tmp/bootstrap_3plug_server.sh
```

This prepares the server before normal 3plug work by installing minimal Python/Git tooling, creating the `threeplug` operator user, creating `/opt/3plug-pro`, and allowing SSH before enabling the firewall.

If the server uses a custom SSH firewall profile, see `design/server-bootstrap-guide.md` before enabling the firewall.

Then switch to the operator user:

```bash
su - threeplug
cd /opt/3plug-pro
```

Install the CLI and run the first checks:

```bash
python3 -m venv ~/.local/share/3plug-pro/venv
~/.local/share/3plug-pro/venv/bin/python -m pip install --upgrade pip
~/.local/share/3plug-pro/venv/bin/python -m pip install "git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli"
export PATH="$HOME/.local/share/3plug-pro/venv/bin:$PATH"
3plug init
3plug server preflight
```

Use the preflight output to confirm what the server already has and what still needs to be installed before Bench is provisioned.

For existing servers or manual firewall handling, see `design/server-bootstrap-guide.md`.

## Current Status

The foundation CLI is available and supports:

* `3plug --help`
* `3plug init`
* `3plug server preflight`
* `3plug app list`
* `3plug app show <app>`
* `3plug stack list`
* `3plug bench list`
* `3plug job list`

`3plug doctor` is currently a developer workspace check for this repository layout. Use `3plug server preflight` on pip-installed servers.

The next implementation phase will make these server lifecycle commands operational:

* `3plug install server-dependencies`
* `3plug install bench`
* `3plug bench create production`

Until that phase is complete, those lifecycle commands should be treated as planning/foundation commands rather than complete production installers.

## Source Policy

3plug-pro is designed to provision from Triotek-controlled repositories by default.

For Frappe v16 work:

* `main` is the Triotek-controlled install branch.
* `upstream-v16` is used for upstream tracking and intake review.
* production app installs should resolve through the approved catalog, not random Git URLs.

## Repository Layout

Important paths:

* `cli/` contains the installable Python CLI package.
* `config/app-catalog.json` contains the approved app and stack catalog.
* `design/` contains architecture notes, roadmap, and implementation planning.
* `3plug/repos/` is the local source workspace for Bench, Frappe, ERPNext, Press reference code, and app repos. It is intentionally ignored by this repository.

## Roadmap

Start with:

* `design/roadmap.md`
* `design/roadmap-status.md`
* `design/linux-vm-target-plan.md`
* `design/server-bootstrap-guide.md`

The first production-like target is an actual Linux server or local Linux VM. The next milestone is to run `3plug server preflight` there and use the results to implement the real server dependency and Bench install handlers.
