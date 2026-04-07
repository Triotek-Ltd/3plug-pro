# Server Bootstrap Guide

This guide explains what to run before `3plug` takes over server checks and Bench lifecycle work.

Use it for both:

* a new Linux server
* an existing Linux server that needs to become a 3plug-pro managed target

## Order of Operations

Run these steps in this order:

1. Log in as `root` or another admin user.
2. Run the bootstrap script or equivalent manual commands.
3. Switch to the 3plug operator user.
4. Install `3plug` from GitHub.
5. Run `3plug init`.
6. Run `3plug server preflight`.
7. Use the preflight output to implement or run server dependency and Bench installation.

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
* grants the operator user sudo access
* creates `/opt/3plug-pro`
* gives the operator user ownership of `/opt/3plug-pro`
* allows `OpenSSH` through `ufw`
* enables `ufw` by default after allowing SSH

If the server uses a custom UFW SSH profile, run:

```bash
sudo SSH_UFW_PROFILE=<profile-name> bash /tmp/bootstrap_3plug_server.sh
```

If the operator user needs direct SSH login or password-based sudo, set a password or install SSH keys after the bootstrap step:

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

Install `3plug` from GitHub:

```bash
python3 -m venv ~/.local/share/3plug-pro/venv
~/.local/share/3plug-pro/venv/bin/python -m pip install --upgrade pip
~/.local/share/3plug-pro/venv/bin/python -m pip install "git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli"
```

If you are installing from a private fork or private mirror, use the same token for the pip install:

```bash
read -rsp "GitHub token: " GITHUB_TOKEN; echo
~/.local/share/3plug-pro/venv/bin/python -m pip install "git+https://x-access-token:${GITHUB_TOKEN}@github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli"
unset GITHUB_TOKEN
```

What this does:

* creates a dedicated virtual environment for the 3plug-pro CLI
* installs the current 3plug-pro CLI from the `main` branch
* uses the `cli/` package inside this repository
* avoids Ubuntu/Debian system Python restrictions for externally managed environments

Ensure the 3plug-pro virtual environment bin path is active:

```bash
export PATH="$HOME/.local/share/3plug-pro/venv/bin:$PATH"
```

What this does:

* makes the `3plug` command available in the current shell

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

## Boundary Between Script and CLI

The bootstrap script handles only the minimum work needed before `3plug` can run:

* create or verify the operator user
* install minimal Python/Git tooling
* create the workspace directory
* protect SSH before enabling the firewall

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
* app and stack catalog inspection

Next implementation phase:

* make `3plug install server-dependencies` real on Ubuntu/Debian
* make `3plug install bench` real
* make `3plug bench create production` real
