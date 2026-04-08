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

## Server Lifecycle

The current operator lifecycle is:

* bootstrap the server so `3plug` can run
* update the installed `3plug` CLI on existing servers
* uninstall the managed `3plug` footprint when a server is retired or rebuilt

This is intentionally shaped to become backend job actions for a future Press-like 3plug UI.

## First-Time Server Setup

After logging into a new Ubuntu/Debian server for the first time as `root` or a sudo-capable admin user, use this order.

### Step 1: Bootstrap The Server

This repository is public, so the normal download command is:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/bootstrap_3plug_server.sh -o /tmp/bootstrap_3plug_server.sh
sudo bash /tmp/bootstrap_3plug_server.sh
```

If you are using a private fork or private mirror instead, use a GitHub token with read access:

```bash
read -rsp "GitHub token: " GITHUB_TOKEN; echo
curl -fsSL -H "Authorization: Bearer ${GITHUB_TOKEN}" -H "Accept: application/vnd.github.raw" "https://api.github.com/repos/Triotek-Ltd/3plug-pro/contents/scripts/linux/bootstrap_3plug_server.sh?ref=main" -o /tmp/bootstrap_3plug_server.sh
sudo bash /tmp/bootstrap_3plug_server.sh
```

This script performs the pre-CLI server setup:

* installs minimal tools needed before `3plug` can run: Python, pip, venv, Git, curl, sudo, and UFW
* creates the `threeplug` operator user if it does not already exist
* requires an interactive password to be set for the operator user during bootstrap
* adds `threeplug` to the sudo group
* creates `/opt/3plug-pro`
* gives `threeplug` ownership of `/opt/3plug-pro`
* allows SSH in UFW before enabling the firewall

If the server uses a custom SSH firewall profile, read `design/server-bootstrap-guide.md` before enabling the firewall.

### Step 2: Switch To The Operator User

Then switch into the operator user and workspace:

```bash
su - threeplug
cd /opt/3plug-pro
```

This avoids running normal platform operations directly as `root`.

### Step 3: Configure Git Identity

Before installing `3plug`, configure Git identity for the operator user. Do this before any `pip install` step or other 3plug lifecycle command:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/configure_3plug_git.sh -o /tmp/configure_3plug_git.sh
sudo bash /tmp/configure_3plug_git.sh
```

Or inspect it first through the CLI once the updated command surface is available:

```bash
3plug server git-setup
```

This sets `git config --global user.name` and `git config --global user.email` for the operator user. The update/install flow should not proceed before this is configured.

### Step 4: Install The CLI

Then install the current 3plug-pro CLI from GitHub through the gated install script:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/install_3plug_cli.sh -o /tmp/install_3plug_cli.sh
sudo bash /tmp/install_3plug_cli.sh
```

If you are using the updated CLI surface already, you can inspect the same action first with:

```bash
3plug server install-cli
```

If you need a private fork or private mirror, pass a custom package URL into the script environment instead of bypassing the gate:

```bash
sudo THREEPLUG_PACKAGE_URL="git+https://x-access-token:${GITHUB_TOKEN}@github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli" bash /tmp/install_3plug_cli.sh
unset GITHUB_TOKEN
```

This uses a venv so the install does not modify the system Python environment, refuses to continue until Git identity is configured, and publishes `3plug` and `3plug-pro` into `/usr/local/bin` so the commands are available globally.

### Step 5: Run The First Checks

Run the first CLI checks in this order:

```bash
3plug --help
3plug init
3plug server preflight
```

What these commands do:

* `3plug --help` confirms the CLI is installed and available.
* `3plug init` creates local 3plug-pro state for this server.
* `3plug server preflight` checks the server OS, Python, Node, database, Redis, Nginx, Supervisor, PDF tooling, and related prerequisites before Bench installation.

Use the preflight output to confirm what the server already has and what still needs to be installed before Bench is provisioned.

For existing servers, custom firewall handling, or manual equivalent commands, see `design/server-bootstrap-guide.md`.

## Update Existing Server Install

If the last commands you already ran on a server were:

```bash
3plug --help
3plug init
3plug server preflight
```

then use this order.

### Step 1: Inspect The Update Command

The next safe action is to inspect the update command first:

```bash
3plug server update
```

That prints the exact server-side update command and records a local job entry.

The update flow now requires Git identity to be configured for the operator user before it will run.

### Step 2: Execute The Update

When you are ready to run the update on the server itself, use:

```bash
3plug server update --execute
```

This can be run from the `threeplug` operator shell after the CLI is installed. The install flow publishes `3plug` globally, so no venv path export should be needed during normal use.

On pip-installed servers, `--execute` will fetch the current script to the server temp directory if the local repo script is not present under the workspace path.

### Step 3: Use The Direct Script Path If Needed

Use the update script directly if you prefer the shell-script path on a server that already has the `threeplug` operator user and workspace:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/update_3plug_server.sh -o /tmp/update_3plug_server.sh
sudo bash /tmp/update_3plug_server.sh
```

This refreshes the installed `3plug` CLI in the operator user's virtual environment without removing local workspace state.

## Uninstall From a Server

Use this order.

### Step 1: Inspect The Uninstall Command

To inspect the uninstall command from the CLI first, run:

```bash
3plug server uninstall --remove-user
```

### Step 2: Run The Uninstall From An Admin Shell

When you are ready to actually run the uninstall on the server, use:

```bash
3plug server uninstall --remove-user --execute
```

If you are removing the `threeplug` user itself, do not run the uninstall from an active `threeplug` login shell. Exit that shell first, then run the uninstall as `root` or another sudo-capable admin user.

On pip-installed servers, `--execute` will fetch the current uninstall script to the server temp directory if the local repo script is not present under the workspace path.

Recommended safe sequence:

```bash
exit
sudo -i
cd /opt/3plug-pro
3plug server uninstall --remove-user --execute
```

### Step 3: Use The Direct Script Path If Needed

If you prefer to avoid relying on the `3plug` entrypoint after switching users, run the script directly:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/uninstall_3plug_server.sh -o /tmp/uninstall_3plug_server.sh
sudo env THREEPLUG_USER="threeplug" THREEPLUG_WORKDIR="/opt/3plug-pro" REMOVE_USER="1" REMOVE_WORKDIR="1" REMOVE_VENV="1" THREEPLUG_FORCE="0" bash /tmp/uninstall_3plug_server.sh
```

Use the uninstall script directly when retiring a server or removing the 3plug-managed footprint:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/uninstall_3plug_server.sh -o /tmp/uninstall_3plug_server.sh
sudo bash /tmp/uninstall_3plug_server.sh
```

By default this removes the workspace and CLI virtual environment but keeps the operator user.

To also remove the operator user:

```bash
sudo REMOVE_USER=1 bash /tmp/uninstall_3plug_server.sh
```

The compatibility command is also available:

```bash
3plug-pro --help
```

## Current Status

The foundation CLI is available and supports:

* `3plug --help`
* `3plug init`
* `3plug server preflight`
* `3plug server bootstrap`
* `3plug server git-setup`
* `3plug server install-cli`
* `3plug server update`
* `3plug server uninstall`
* `3plug app list`
* `3plug app show <app>`
* `3plug stack list`
* `3plug bench list`
* `3plug job list`
* `3plug job show <job-id>`

`3plug doctor` is currently a developer workspace check for this repository layout. Use `3plug server preflight` on pip-installed servers.

The next implementation phase will make these server lifecycle commands operational:

* `3plug install server-dependencies`
* `3plug install bench`
* `3plug bench create production`

Until that phase is complete, those lifecycle commands should be treated as planning/foundation commands rather than complete production installers. The bootstrap, update, and uninstall scripts remain the current shell-based server lifecycle helpers before those actions move behind the `3plug` control plane and UI.

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
* `design/server-operator-runbook.md`

The first production-like target is an actual Linux server or local Linux VM. The next milestone is to run `3plug server preflight` there and use the results to implement the real server dependency and Bench install handlers.
