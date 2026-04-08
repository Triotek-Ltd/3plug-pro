# Server Bootstrap Guide

This guide explains the current shell-based server lifecycle around `3plug` before the full control plane and UI take over.

For the shortest operator path, use `server-operator-runbook.md`.

Use it for both:

* a new Linux server
* an existing Linux server that needs to become a 3plug-pro managed target
* an existing 3plug-managed server that needs update or uninstall actions

## Lifecycle Model

The current server lifecycle is:

1. `bootstrap` the server so `3plug` can run
2. `update` the installed `3plug` CLI on existing servers
3. `uninstall` the managed `3plug` footprint when a server is being retired, rebuilt, or moved

This naming is deliberate because these actions should eventually appear in the 3plug UI as Press-like backend jobs instead of stand-alone shell steps.

## Bootstrap Order of Operations

Run these steps in this order:

1. Log in as `root` or another admin user.
2. Run the bootstrap script or equivalent manual commands.
3. Switch to the 3plug operator user.
4. Configure Git identity for the operator user.
5. Install `3plug` from GitHub.
6. Run `3plug init`.
7. Run `3plug server preflight`.
8. Use the preflight output to implement or run server dependency and Bench installation.

## New Server Path

On a new Ubuntu/Debian server, start as `root` or with a sudo-capable admin user.

Download and run the bootstrap script.

The main 3plug-pro repository is public, so the normal download command is:

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

What this does:

* installs only the minimal host tools needed before `3plug` can run
* creates the `threeplug` operator user if it does not already exist
* requires an interactive password to be set for the operator user during bootstrap
* grants the operator user sudo access
* creates `/opt/3plug-pro`
* gives the operator user ownership of `/opt/3plug-pro`
* allows `OpenSSH` through `ufw`
* enables `ufw` by default after allowing SSH

If the server uses a custom UFW SSH profile, run:

```bash
sudo SSH_UFW_PROFILE=<profile-name> bash /tmp/bootstrap_3plug_server.sh
```

If you still need to change the password after bootstrap, use:

```bash
sudo passwd threeplug
```

Then switch to the operator user:

```bash
su - threeplug
```

What this does:

* starts a login shell as the dedicated 3plug operator user
* avoids running normal platform work directly as `root`

Move into the workspace:

```bash
cd /opt/3plug-pro
```

What this does:

* places generated 3plug local state and future server work under the intended workspace

Before installing `3plug`, configure Git identity for the operator user. Do this before any `pip install` step or other 3plug lifecycle command:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/configure_3plug_git.sh -o /tmp/configure_3plug_git.sh
sudo bash /tmp/configure_3plug_git.sh
```

What this does:

* sets `git config --global user.name` for the operator user
* sets `git config --global user.email` for the operator user
* establishes the minimum Git identity required before install/update flows continue

If the updated CLI command surface is already available, you can inspect the same action with:

```bash
3plug server git-setup
```

Then install `3plug` from GitHub through the gated install script:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/install_3plug_cli.sh -o /tmp/install_3plug_cli.sh
sudo bash /tmp/install_3plug_cli.sh
```

If the updated CLI command surface is already available, you can inspect the same action with:

```bash
3plug server install-cli
```

What this does:

* creates a dedicated virtual environment for the 3plug-pro CLI
* resolves and installs the latest published 3plug-pro CLI release by default
* uses the `cli/` package inside this repository
* avoids Ubuntu/Debian system Python restrictions for externally managed environments
* refuses to continue until Git identity is configured for the operator user
* publishes `3plug` and `3plug-pro` into `/usr/local/bin` so the commands are available globally

If you need a private fork or private mirror, pass a custom package URL into the script environment instead of bypassing the gate:

```bash
sudo THREEPLUG_PACKAGE_URL="git+https://x-access-token:${GITHUB_TOKEN}@github.com/Triotek-Ltd/3plug-pro.git@v0.2.0#subdirectory=cli" bash /tmp/install_3plug_cli.sh
unset GITHUB_TOKEN
```

The default install and update flows now resolve the latest published GitHub release automatically. Use a different package URL only when you intentionally want a specific older tag, a newer development branch, or a private mirror.

Verify the global commands are available:

```bash
which 3plug
which 3plug-pro
```

What this does:

* confirms the global command links were created successfully

Run the first 3plug checks:

```bash
3plug --help
3plug init
3plug server preflight
```

What these do:

* `3plug --help` confirms the CLI is installed and runnable
* `3plug init` creates local ignored 3plug state
* `3plug server preflight` checks what the Linux server already has before Bench installation

`3plug doctor` is currently a developer workspace check for the source repository layout. Do not use it as the first server-runtime check on a pip-installed server.

## Existing Server Path

On an existing server, first check whether there is already an appropriate operator user and workspace.

```bash
id threeplug
ls -ld /opt/3plug-pro
sudo ufw status verbose
```

What these do:

* `id threeplug` checks whether the operator user already exists
* `ls -ld /opt/3plug-pro` checks whether the 3plug workspace already exists and who owns it
* `sudo ufw status verbose` checks whether the firewall is enabled and which rules are active

If the user or workspace is missing, run the bootstrap script:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/bootstrap_3plug_server.sh -o /tmp/bootstrap_3plug_server.sh
sudo bash /tmp/bootstrap_3plug_server.sh
```

For private fork or mirror access, use the GitHub API download command from the new server path above.

If you do not want the script to enable `ufw` automatically, run:

```bash
sudo FIREWALL_AUTO_ENABLE=0 bash /tmp/bootstrap_3plug_server.sh
```

What this does:

* keeps the `OpenSSH` allow rule setup
* skips automatic firewall enablement
* lets the operator review and enable the firewall manually later

If SSH uses a custom UFW profile, combine both options:

```bash
sudo FIREWALL_AUTO_ENABLE=0 SSH_UFW_PROFILE=<profile-name> bash /tmp/bootstrap_3plug_server.sh
```

Manual firewall commands if needed:

```bash
sudo ufw allow OpenSSH
sudo ufw status verbose
sudo ufw --force enable
sudo ufw status verbose
```

What these do:

* `sudo ufw allow OpenSSH` prevents locking out SSH before enabling the firewall
* `sudo ufw status verbose` shows current firewall state
* `sudo ufw --force enable` enables the firewall without an interactive prompt
* the second status check confirms the final active rules

## Update Existing Server Install

If the last commands you already ran on a server were:

```bash
3plug --help
3plug init
3plug server preflight
```

then the next operator step is usually:

```bash
3plug server update
```

That shows the exact update command and records a local job entry.

The update flow now requires Git identity to be configured for the operator user before it will run.

When you are ready to run the update directly through the CLI, use:

```bash
3plug server update --execute
```

This can be run from the `threeplug` operator shell after the CLI is installed. The install flow publishes `3plug` globally, so no venv path export should be needed during normal use.

On pip-installed servers, `--execute` will fetch the current script to the server temp directory if the local repo script is not present under the workspace path.

Use the update script when the server already has the `threeplug` operator user and workspace and you want to refresh the installed CLI directly:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/update_3plug_server.sh -o /tmp/update_3plug_server.sh
sudo bash /tmp/update_3plug_server.sh
```

What this does:

* verifies that the operator user already exists
* verifies or creates the workspace path
* upgrades `pip` in the operator virtual environment
* upgrades the installed `3plug` CLI from the configured Git package URL
* preserves local workspace state under `/opt/3plug-pro`

## Uninstall 3plug From a Server

To inspect the uninstall action first through the CLI, run:

```bash
3plug server uninstall --remove-user
```

To run the uninstall through the CLI on the server itself, use:

```bash
3plug server uninstall --remove-user --execute
```

If you are removing the `threeplug` user itself, do not run this from an active `threeplug` login shell. Exit that shell first, then run the uninstall as `root` or another sudo-capable admin user.

On pip-installed servers, `--execute` will fetch the current uninstall script to the server temp directory if the local repo script is not present under the workspace path.

Recommended safe sequence:

```bash
exit
sudo -i
cd /opt/3plug-pro
3plug server uninstall --remove-user --execute
```

If you prefer to avoid relying on the `3plug` command after switching users, run the script directly:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/uninstall_3plug_server.sh -o /tmp/uninstall_3plug_server.sh
sudo env THREEPLUG_USER="threeplug" THREEPLUG_WORKDIR="/opt/3plug-pro" REMOVE_USER="1" REMOVE_WORKDIR="1" REMOVE_VENV="1" THREEPLUG_FORCE="0" bash /tmp/uninstall_3plug_server.sh
```

Use the uninstall script when you want to remove the managed 3plug footprint from a server directly:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/uninstall_3plug_server.sh -o /tmp/uninstall_3plug_server.sh
sudo bash /tmp/uninstall_3plug_server.sh
```

Default uninstall behavior:

* removes `/opt/3plug-pro`
* removes the operator CLI virtual environment
* keeps the `threeplug` operator user
* removes the operator user from `sudo` if the user is kept

To also remove the operator user and home directory:

```bash
sudo REMOVE_USER=1 bash /tmp/uninstall_3plug_server.sh
```

For non-interactive cleanup, add `THREEPLUG_FORCE=1`:

```bash
sudo THREEPLUG_FORCE=1 REMOVE_USER=1 bash /tmp/uninstall_3plug_server.sh
```

## Boundary Between Script and CLI

The bootstrap script handles only the minimum work needed before `3plug` can run:

* create or verify the operator user
* install minimal Python/Git tooling
* create the workspace directory
* protect SSH before enabling the firewall

The update and uninstall scripts currently extend that shell-based lifecycle until equivalent actions move behind the `3plug` control plane.

The `3plug` CLI should own the platform work after that:

* `3plug server preflight`
* `3plug install server-dependencies`
* `3plug install bench`
* `3plug bench create production`
* site and app lifecycle commands

## Current Implementation Status

Currently implemented:

* Git URL CLI install
* `3plug init`
* `3plug doctor` for source workspace checks
* `3plug server preflight`
* `3plug server bootstrap`
* `3plug server git-setup`
* `3plug server install-cli`
* `3plug server update`
* `3plug server uninstall`
* local job recording for server actions
* app and stack catalog inspection

Next implementation phase:

* make `3plug install server-dependencies` real on Ubuntu/Debian
* make `3plug install bench` real
* make `3plug bench create production` real
* move bootstrap, update, and uninstall flows behind auditable `3plug` server actions and the future UI
