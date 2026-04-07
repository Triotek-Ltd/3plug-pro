# 3plug Server Dependency Plan

## Purpose

3plug is intentionally starting with a Bench-only model instead of Docker.

That means 3plug must own a server dependency phase before it installs Bench or creates Bench runtimes.

The flow should be:

```text
3plug server preflight
3plug install server-dependencies
3plug install bench
3plug bench create <bench-name>
```

## Source of truth

Use official Frappe documentation as the main source.

Community guides such as Code With Karani are useful for operational sequencing and common real-world Ubuntu steps, but 3plug should not treat older community version pins as current defaults.

## Triotek target

Triotek's 3plug platform target is Frappe v16 only.

Do not design 3plug dependency installation around v14 or v15 compatibility unless Triotek explicitly reopens older-version support later.

## Frappe v16 dependency matrix

Official current Frappe draft docs list these dependency expectations for v16/develop:

| Dependency | Required target |
| --- | --- |
| MariaDB | 11.8 |
| Python | 3.14 |
| Node.js | 24 |
| Redis / Valkey | 6+ |
| Yarn | 1.22+ |
| pip | 25.3+ |

Additional required tools:

* `git`
* `pkg-config`
* MariaDB client and development headers
* `wkhtmltopdf` 0.12.6 with patched Qt for PDF generation
* `xvfb`
* `libfontconfig`
* `cron` for scheduled jobs, certificate renewal, and scheduled backups

Production process and web-serving tools:

* `supervisor` or approved `systemd` configuration
* `nginx`
* `fail2ban` or equivalent hardening where policy requires it

## OS baseline

Official current Frappe draft docs say Debian 13+ or Ubuntu 24.04+ should be used for the current/develop path.

3plug should therefore default to:

* stack target: `frappe-v16`
* Frappe install branch: `main`
* ERPNext install branch: `main`
* upstream tracking branch where present: `upstream-v16`
* Bench source: Triotek-controlled `triotek-bench` aligned to v16

## Recommended preflight checks

`3plug server preflight` should check:

```text
uname -a
lsb_release -a
git --version
python --version
uv --version
pip --version
node --version
npm --version
yarn --version
redis-server --version
mariadb --version
mysql --version
wkhtmltopdf --version
crontab -l
nginx -v
supervisord --version
systemctl --version
```

The command should report missing checks as structured findings instead of failing on the first missing command.

## Recommended install groups

### Base packages

Purpose:

* install generic packages Bench and Frappe need before Python/Node work begins

Typical Debian/Ubuntu packages:

```text
git
curl
redis-server
mariadb-server
mariadb-client
libmariadb-dev
pkg-config
xvfb
libfontconfig
cron
```

### Python toolchain

Purpose:

* install the Python runtime and package tooling for Frappe v16

Preferred current approach:

```text
uv python install 3.14 --default
uv tool install frappe-bench
```

Older compatible approach:

```text
python3
python3-dev
python3-venv
python3-pip
python3-setuptools
```

3plug should keep older compatible approaches out of the default path unless Triotek explicitly needs a legacy support mode later.

### Node toolchain

Purpose:

* install the Node.js runtime needed for assets, socket.io, and frontend tooling

Preferred approach:

```text
nvm install 24
npm install -g yarn
```

### MariaDB configuration

Purpose:

* prepare database defaults required by Frappe sites

Required policy:

* run secure initialization when required
* configure UTF-8 / utf8mb4 defaults
* bind database to the correct interface for the deployment model
* never print or store root passwords in ordinary logs

For a single-server v1 deployment, default to local database access unless a remote database is explicitly configured.

### PDF tooling

Purpose:

* enable PDF generation from print formats

Current official expectation:

* `wkhtmltopdf` 0.12.6 with patched Qt

3plug should check the exact version and record whether the binary is distribution-provided or manually installed.

### Production web/process tooling

Purpose:

* run the bench after server restart and serve sites through HTTP/HTTPS without `bench start`

Bench production commands:

```text
sudo bench setup production <frappe-user>
bench setup supervisor
bench setup nginx
sudo bench setup sudoers <frappe-user>
bench setup reload-nginx
```

3plug should treat production setup as restricted because official Frappe docs now warn against bare-metal production installs and recommend Docker images for production.

## Code With Karani cross-check

The Code With Karani v14 guide is useful because it shows the practical native-server sequence many operators follow:

* update packages
* create a bench user with sudo privileges
* install Git
* install Python dev/pip/setuptools/distutils/venv packages
* install MariaDB server/client
* install Redis
* install `xvfb`, `libfontconfig`, `wkhtmltopdf`, and MariaDB client development headers
* configure MariaDB charset/collation
* install curl, Node through nvm, npm, and yarn
* install Frappe Bench
* initialize a Bench
* create a site
* get apps
* install apps
* optionally run production setup with scheduler, maintenance mode, production config, nginx, and supervisor

3plug should borrow the sequencing lesson, not blindly reuse the old package versions.

## 3plug install policy

3plug should use a layered install plan:

1. Detect OS and confirm the target Frappe stack is `frappe-v16`.
2. Check system dependencies.
3. Install missing base packages.
4. Configure MariaDB.
5. Install Python toolchain.
6. Install Node/Yarn toolchain.
7. Install PDF tooling.
8. Install process/web tools only when production mode is requested.
9. Install Bench from Triotek-controlled source or approved upstream package.
10. Create or register Bench runtimes.

## Important guardrails

* Do not add v14/v15 compatibility assumptions to the default path.
* Do not assume v16/develop dependencies are valid for older ERPNext apps, because older apps are not the current Triotek target.
* Do not log database root passwords.
* Do not open MariaDB remote access unless explicitly requested.
* Do not run production setup as part of a development bench creation.
* Do not make `bench update` run before the catalog approves app branches/tags.
* Do not expose raw shell operations as default 3plug actions.

## Source links

* Official Frappe draft installation docs: https://docs.frappe.io/framework-copy/user/en/installation
* Official Frappe production setup docs: https://docs.frappe.io/framework/user/en/bench/guides/setup-production
* Code With Karani ERPNext archive: https://codewithkarani.com/tag/erpnext/
