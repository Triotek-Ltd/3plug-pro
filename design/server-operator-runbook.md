# Server Operator Runbook

This runbook is the shortest practical path for operating `3plug` on a Linux server today.

Use it when:

* onboarding a new server
* updating an existing 3plug-managed server
* uninstalling 3plug from a server

## New Server

### Step 1: Run Bootstrap

Run as `root` or another sudo-capable admin user:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/bootstrap_3plug_server.sh -o /tmp/bootstrap_3plug_server.sh
sudo bash /tmp/bootstrap_3plug_server.sh
```

### Step 2: Configure Git Identity

Configure Git identity for the operator user before any install or update action:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/configure_3plug_git.sh -o /tmp/configure_3plug_git.sh
sudo bash /tmp/configure_3plug_git.sh
```

### Step 3: Install The CLI

Install the CLI through the gated install script:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/install_3plug_cli.sh -o /tmp/install_3plug_cli.sh
sudo bash /tmp/install_3plug_cli.sh
```

### Step 4: Run The First Checks

Switch to the operator shell and run the first checks:

```bash
su - threeplug
cd /opt/3plug-pro
3plug --help
3plug init
3plug server preflight
```

### Step 5: Install Server Dependencies

Use the preflight result to confirm what is missing, then install the server dependency foundation:

```bash
3plug install server-dependencies
3plug install server-dependencies --execute
3plug server preflight
```

If you also want the current production-oriented extras:

```bash
3plug install server-dependencies --production-tools --execute
```

When `--production-tools` is used, the installer checks for `apache2` and stops/disables it before enabling Nginx.

### Step 6: Install Bench

For private Bench sources, use SSH as the default access model for the `threeplug` operator user.

Create and add the SSH key if needed:

```bash
ls -la ~/.ssh
ssh-keygen -t ed25519 -C "threeplug@$(hostname)"
cat ~/.ssh/id_ed25519.pub
```

Then add that public key in GitHub under:

1. `Settings`
2. `SSH and GPG keys`
3. `New SSH key`

Test the connection:

```bash
ssh -T git@github.com
```

After dependency installation, install Bench:

```bash
3plug install bench
3plug install bench --execute
bench --version
```

The default Bench source now uses the SSH repo URL for the private `triotek-bench` repository and follows the repo default branch unless you override `--bench-source`.

The Bench install script checks GitHub SSH access for the `threeplug` user before attempting the install.

This is the current stopping point before future `3plug bench create`, `3plug bench register`, and `3plug bench status` work.

## Existing Server Update

### Step 1: Inspect First

```bash
3plug server update
3plug job list
```

### Step 2: Run The Update

```bash
3plug server update --execute
```

Run the update first when you want the server to pick up the newest CLI behavior before continuing to the next operator step.

If `--execute` reports that the script must be run as root or with sudo, use the printed `Run:` command directly instead.

### Step 3: Verify Global Command Availability

The install and update flows publish `3plug` and `3plug-pro` into `/usr/local/bin`, so no venv path export should be needed during normal use.

```bash
which 3plug
which 3plug-pro
```

### Step 4: Continue To Server Dependencies

After update, continue from the confirmed baseline into the next operator action:

```bash
3plug install server-dependencies
3plug install server-dependencies --execute
3plug server preflight
```

If you want the current production-oriented extras too:

```bash
3plug install server-dependencies --production-tools --execute
3plug server preflight
```

If `--execute` reports that the script must be run as root or with sudo, use the direct script path instead:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/install_server_dependencies.sh -o /tmp/install_server_dependencies.sh
sudo env THREEPLUG_TARGET_STACK="frappe-v16" THREEPLUG_INSTALL_PRODUCTION_TOOLS="0" bash /tmp/install_server_dependencies.sh
3plug server preflight
```

## Existing Server Uninstall

### Step 1: Inspect First

```bash
3plug server uninstall --remove-user
3plug job list
```

### Step 2: Switch To An Admin Shell

If removing the operator user, exit the `threeplug` shell and switch to `root` or another sudo-capable admin user before running the uninstall.

Safe sequence:

```bash
exit
sudo -i
3plug server uninstall --remove-user --execute
```

### Step 3: Use The Direct Script Path If Needed

If you want the direct script path instead:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/uninstall_3plug_server.sh -o /tmp/uninstall_3plug_server.sh
sudo env THREEPLUG_USER="threeplug" THREEPLUG_WORKDIR="/opt/3plug-pro" REMOVE_USER="1" REMOVE_WORKDIR="1" REMOVE_VENV="1" THREEPLUG_FORCE="0" bash /tmp/uninstall_3plug_server.sh
```

## Git Identity Rule

### Step 1: Require Git Identity

Do not run the first install or update flow before Git identity is configured for the operator user.

Required values:

* `git config --global user.name`
* `git config --global user.email`

### Step 2: Run Git Setup

The supported setup action is:

```bash
3plug server git-setup
```

Or direct script:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/configure_3plug_git.sh -o /tmp/configure_3plug_git.sh
sudo bash /tmp/configure_3plug_git.sh
```
