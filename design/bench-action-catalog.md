# 3plug Bench Action Catalog

## Purpose

This document defines the Bench-backed actions that 3plug should support.

It is the implementation contract between:

```text
3plug operator command -> 3plug job -> controlled Bench/Frappe command plan
```

3plug should not expose arbitrary shell execution as a normal operator workflow.

## Benchmarks used

This catalog is benchmarked against:

* local `triotek-bench` docs and command code
* local `triotek-frappe` command code
* official Frappe Framework Bench docs
* local Frappe Press source as a control-plane reference
* the version-aware dependency plan in `server-dependency-plan.md`

Important upstream note:

Frappe's current production setup guide warns against bare-metal production installs and recommends Docker images for production. 3plug's Bench-only model is therefore a deliberate Triotek-managed operating model and must add guardrails around production setup, updates, backups, restores, and process management.

## Command ownership

Bench commands come from two places:

* `bench` project commands: Bench folder setup, app retrieval, update, config, production setup, process helpers, and dependency setup.
* Frappe Framework commands exposed through Bench: site creation, site migration, site backup, restore, installed app management, user and maintenance actions.

The 3plug runner should not care where the command is implemented internally, but the catalog should preserve this distinction for maintenance.

## Safety levels

Use these safety levels in the action registry:

* `read`: reads state only.
* `normal`: expected operator workflow; writes state but is routine.
* `elevated`: can affect uptime, data, security, or production configuration.
* `restricted`: destructive, secret-bearing, raw execution, or high-risk maintenance.

## Lock scopes

Each action must declare a lock scope:

* `none`: no lock required.
* `server`: affects system packages, services, or global server state.
* `bench`: affects a Bench folder, its apps, assets, or process config.
* `site`: affects one Frappe site.
* `app`: affects an app source inside a Bench folder.

When an action uses multiple scopes, lock the broadest needed scope.

## V1 actions

### `server_preflight`

Operator command:

```text
3plug server preflight
```

Bench mapping:

```text
python --version
node --version
npm --version
redis-server --version
mysql --version
wkhtmltopdf --version
```

Purpose:

* inspect whether the managed server has the dependencies needed for a non-Docker Bench setup
* report missing or incompatible dependencies before installing Bench or creating Bench runtimes
* compare installed dependency versions against the selected Frappe stack target

Safety level: `read`

Lock scope: `none`

State updates:

* record dependency check result
* record detected versions

Rules:

* do not install anything
* do not require sudo
* produce a clear remediation plan
* default to the Triotek target stack `frappe-v16`
* do not add v14/v15 compatibility checks unless Triotek explicitly reopens legacy support

### `install_server_dependencies`

Operator command:

```text
3plug install server-dependencies
```

Bench mapping:

```text
bench install prerequisites
bench install mariadb
bench install redis
bench install nodejs
bench install wkhtmltopdf
bench install supervisor
bench install nginx
bench install fail2ban
```

Alternative mapping:

```text
system package manager commands selected by OS policy
```

Purpose:

* install the system dependencies required before a non-Docker Bench runtime can work
* prepare the server for Bench installation and Bench runtime creation
* apply the layered dependency plan from `server-dependency-plan.md`

Safety level: `restricted`

Lock scope: `server`

Rules:

* run `server_preflight` first
* require explicit approval because this may install system packages and services
* production servers require a change note
* use the `frappe-v16` dependency targets before choosing Python, Node, MariaDB, and Yarn versions
* do not install v14/v15 dependency profiles by default
* record OS, package manager, dependency versions, and install method
* do not log database root passwords or service credentials
* prefer OS-specific Triotek install scripts once they exist

Output:

* dependency install job id
* installed versions
* services enabled or changed
* remaining manual actions

### `doctor`

Operator command:

```text
3plug doctor
```

Bench mapping:

```text
bench --version
bench find <root>
```

Purpose:

* check whether Bench is available
* check whether server dependencies appear available
* check whether configured Bench paths exist
* check whether required folders exist
* check whether catalog paths exist

Safety level: `read`

Lock scope: `none`

State updates:

* record environment health check
* optionally record discovered Bench paths

### `install_bench`

Operator command:

```text
3plug install bench
```

Bench mapping:

```text
pip install frappe-bench
```

or, for Triotek-controlled source:

```text
pip install <triotek-bench-source>
```

Purpose:

* install the Bench CLI on the managed server
* update the Bench CLI when explicitly requested
* make Bench available before any Bench runtime can be created or managed
* prefer Triotek-controlled Bench source where available

Safety level: `elevated`

Lock scope: `server`

Rules:

* require explicit confirmation for production servers
* run before `create_bench`, `register_bench`, or site actions when Bench is missing
* record installed Bench version
* record the install method, such as PyPI, local source path, or Triotek Git source
* do not log package index credentials or tokens

Output:

* installed Bench executable path
* installed Bench version
* install source
* install timestamp

### `create_bench`

Operator command:

```text
3plug bench create <bench-name> --path <path>
```

Bench mapping:

```text
bench init <path> --frappe-path https://github.com/Triotek-Ltd/triotek-frappe.git --frappe-branch main
```

Optional flags:

```text
--frappe-path <repo-or-path>
--python <python-executable>
--skip-assets
--no-backups
--dev
```

Purpose:

* create one managed Bench runtime
* default to the Triotek-supported Frappe v16 stack

Safety level: `normal`

Lock scope: `server`

State updates:

* create `Bench Runtime` record
* create `Job` record
* create `Audit Event`

Rules:

* do not allow path outside approved server work roots
* default to Triotek-controlled Frappe source on `main`
* treat `upstream-v16` as an upstream tracking branch only, not the install branch
* avoid `--ignore-exist` unless explicitly requested

### `register_bench`

Operator command:

```text
3plug bench register <bench-name> --path <path>
```

Bench mapping:

```text
bench --site all list-apps
bench version
```

Purpose:

* bring an existing Bench folder under 3plug management

Safety level: `read`

Lock scope: `bench`

State updates:

* create or update `Bench Runtime`
* discover apps and sites

### `list_benches`

Operator command:

```text
3plug bench list
```

Bench mapping:

```text
bench find <root>
```

Purpose:

* show registered and discovered benches

Safety level: `read`

Lock scope: `none`

### `bench_status`

Operator command:

```text
3plug bench status <bench-name>
```

Bench mapping:

```text
bench version
bench --site all list-apps --format json
bench show-config
```

Purpose:

* inspect app versions, sites, and common config

Safety level: `read`

Lock scope: `bench`

### `create_site`

Operator command:

```text
3plug site create <site-name> --bench <bench-name>
```

Bench/Frappe mapping:

```text
bench new-site <site-name>
```

Optional flags:

```text
--install-app <app>
--admin-password <secret-ref>
--mariadb-root-password <secret-ref>
```

Purpose:

* create a new Frappe site inside a managed Bench runtime

Safety level: `normal`

Lock scope: `bench`

State updates:

* create `Site` record
* create `Job`
* create `Audit Event`

Rules:

* use secret references, not raw passwords in logs
* validate site name and environment
* record site folder path

### `list_sites`

Operator command:

```text
3plug site list --bench <bench-name>
```

Bench/Frappe mapping:

```text
bench list-sites
```

Purpose:

* list sites in a Bench folder

Safety level: `read`

Lock scope: `bench`

### `get_app`

Operator command:

```text
3plug app get <app-name> --bench <bench-name>
```

Bench mapping:

```text
bench get-app <approved-repo-url-or-local-path> --branch <branch>
```

For Triotek-controlled repos, `<branch>` defaults to `main`.

`upstream-v16` is only an upstream tracking branch used for intake and review. It should not be used as the default install branch.

Purpose:

* add an approved app source into a Bench runtime

Safety level: `normal`

Lock scope: `bench`

Rules:

* production workflows must only use approved catalog sources
* allow arbitrary Git URLs only in development mode
* record app source, branch, and commit after retrieval
* prefer local source paths when working from Triotek repo workspace

### `install_app`

Operator command:

```text
3plug site install-app <site-name> <app-name> --bench <bench-name>
```

Bench/Frappe mapping:

```text
bench --site <site-name> install-app <app-name>
```

Optional precursor:

```text
bench get-app <approved-repo-url-or-local-path> --branch <branch>
```

Purpose:

* install an app already present in the Bench onto a site

Safety level: `normal`

Lock scope: `site`

Rules:

* validate app exists in catalog
* validate app branch compatibility with the Bench stack
* ensure app exists in `apps/` before install
* record installed app list after completion

### `list_site_apps`

Operator command:

```text
3plug site apps <site-name> --bench <bench-name>
```

Bench/Frappe mapping:

```text
bench --site <site-name> list-apps --format json
```

Purpose:

* show installed apps for one site

Safety level: `read`

Lock scope: `site`

### `migrate_site`

Operator command:

```text
3plug site migrate <site-name> --bench <bench-name>
```

Bench/Frappe mapping:

```text
bench --site <site-name> migrate
```

Purpose:

* apply patches, schema changes, and related migration work for one site

Safety level: `elevated`

Lock scope: `site`

Rules:

* require backup-before-migrate policy for production
* block concurrent site jobs
* record migration status and logs
* do not use skip-failing flags by default
* assume v16 migration compatibility unless a future legacy mode is explicitly added

### `backup_site`

Operator command:

```text
3plug site backup <site-name> --bench <bench-name>
```

Bench/Frappe mapping:

```text
bench --site <site-name> backup
```

Optional flags:

```text
--with-files
--backup-path <path>
--compress
```

Purpose:

* create database and optional file backups for a site

Safety level: `normal`

Lock scope: `site`

State updates:

* create `Backup` record
* record output paths
* record verification status

Rules:

* use approved backup storage roots
* capture backup metadata
* warn when backup encryption is enabled and key handling is unresolved

### `backup_bench`

Operator command:

```text
3plug bench backup <bench-name>
```

Bench mapping:

```text
bench backup-all-sites
```

Purpose:

* back up all sites in a Bench runtime

Safety level: `normal`

Lock scope: `bench`

Rules:

* not default for large production benches without schedule and storage planning
* record one parent job and one backup record per site where possible

### `restore_site`

Operator command:

```text
3plug site restore <site-name> --bench <bench-name> --database-backup <path>
```

Bench/Frappe mapping:

```text
bench --site <site-name> restore <database-backup>
```

Optional flags:

```text
--with-public-files <path>
--with-private-files <path>
--force
```

Purpose:

* restore a site database and optional files from a backup

Safety level: `restricted`

Lock scope: `site`

Rules:

* require elevated approval for production
* require pre-restore backup unless explicitly waived by elevated approval
* validate backup source belongs to the requested site or an approved migration workflow
* require restore dry-run or verification plan when available
* never run `--force` silently

### `partial_restore_site`

Operator command:

```text
3plug site partial-restore <site-name> --bench <bench-name> --database-backup <path>
```

Bench/Frappe mapping:

```text
bench --site <site-name> partial-restore <database-backup>
```

Purpose:

* restore a partial backup into an existing site

Safety level: `restricted`

Lock scope: `site`

Rules:

* not part of default V1 UI
* require elevated approval
* require explicit operator note

### `update_bench`

Operator command:

```text
3plug bench update <bench-name>
```

Bench mapping:

```text
bench update
```

Selective mappings:

```text
bench update --pull
bench update --requirements
bench update --build
bench update --patch
```

Purpose:

* update apps, requirements, assets, migrations, and process restarts for a Bench runtime

Safety level: `elevated`

Lock scope: `bench`

Rules:

* avoid one-shot `bench update` for production until 3plug has staged update plans
* prefer planned sequence: backup, pull, requirements, build, migrate, restart
* record exact app revisions before and after
* require branch/tag compatibility check from catalog

### `build_assets`

Operator command:

```text
3plug bench build <bench-name>
```

Bench/Frappe mapping:

```text
bench build
```

or:

```text
bench update --build
```

Purpose:

* rebuild JS/CSS assets

Safety level: `normal`

Lock scope: `bench`

### `setup_requirements`

Operator command:

```text
3plug bench setup-requirements <bench-name>
```

Bench mapping:

```text
bench setup requirements
```

Purpose:

* install Python and Node dependencies for apps in a Bench runtime

Safety level: `elevated`

Lock scope: `bench`

Rules:

* production requires maintenance window or approval
* capture dependency logs

### `restart_bench`

Operator command:

```text
3plug bench restart <bench-name>
```

Bench mapping:

```text
bench restart
```

Optional mappings:

```text
bench restart --supervisor
bench restart --systemd
bench restart --web
```

Purpose:

* restart managed Bench processes

Safety level: `elevated`

Lock scope: `bench`

Rules:

* production requires maintenance or explicit approval
* runner must know whether the bench uses supervisor or systemd

### `set_maintenance_mode`

Operator command:

```text
3plug site maintenance <site-name> on --bench <bench-name>
3plug site maintenance <site-name> off --bench <bench-name>
```

Bench/Frappe mapping:

```text
bench --site <site-name> set-maintenance-mode on
bench --site <site-name> set-maintenance-mode off
```

Purpose:

* put a site into or out of maintenance mode

Safety level: `elevated`

Lock scope: `site`

### `setup_production`

Operator command:

```text
3plug bench setup-production <bench-name> --user <system-user>
```

Bench mapping:

```text
sudo bench setup production <system-user>
```

Manual component mappings:

```text
bench setup supervisor
bench setup nginx
bench setup systemd
bench setup sudoers <system-user>
bench setup reload-nginx
```

Purpose:

* prepare process supervision and web serving for a Bench runtime

Safety level: `restricted`

Lock scope: `server`

Rules:

* not a default V1 happy-path command
* require explicit approval
* record whether supervisor or systemd is used
* record nginx config path
* document that upstream currently recommends Docker for production

### `setup_domains`

Operator command:

```text
3plug site domain add <site-name> <domain> --bench <bench-name>
3plug site domain remove <site-name> <domain> --bench <bench-name>
3plug site domain sync <site-name> --domain <domain> --bench <bench-name>
```

Bench mapping:

```text
bench setup add-domain <domain> --site <site-name>
bench setup remove-domain <domain> --site <site-name>
bench setup sync-domains --site <site-name> --domain <domain>
bench setup nginx
bench setup reload-nginx
```

Purpose:

* manage site domain mappings and regenerate/reload nginx config

Safety level: `elevated`

Lock scope: `bench`

Rules:

* production reloads require care
* domain changes should be audited
* SSL setup should be a separate action

### `setup_ssl`

Operator command:

```text
3plug site ssl lets-encrypt <site-name> --domain <domain> --bench <bench-name>
```

Bench mapping:

```text
bench setup lets-encrypt <site-name> --custom-domain <domain>
```

Wildcard mapping:

```text
bench setup wildcard-ssl <domain> --email <email>
```

Purpose:

* configure TLS certificates

Safety level: `elevated`

Lock scope: `bench`

Rules:

* require domain ownership/DNS readiness checks where possible
* record certificate workflow status
* do not store private key content in logs

### `drop_site`

Operator command:

```text
3plug site drop <site-name> --bench <bench-name>
```

Bench/Frappe mapping:

```text
bench drop-site <site-name>
```

Purpose:

* remove a site and its database from a Bench runtime

Safety level: `restricted`

Lock scope: `bench`

Rules:

* not exposed as a normal V1 workflow
* require elevated approval
* require backup unless explicitly waived
* never pass `--force` silently
* archive record before deleting state

### `uninstall_app`

Operator command:

```text
3plug site uninstall-app <site-name> <app-name> --bench <bench-name>
```

Bench/Frappe mapping:

```text
bench --site <site-name> uninstall-app <app-name>
```

Purpose:

* remove an installed app from a site

Safety level: `restricted`

Lock scope: `site`

Rules:

* require backup
* require dependency impact review
* not part of default V1 UI

### `remove_app_from_bench`

Operator command:

```text
3plug app remove <app-name> --bench <bench-name>
```

Bench mapping:

```text
bench remove-app <app-name>
```

Purpose:

* remove app source from a Bench runtime when not installed on any site

Safety level: `restricted`

Lock scope: `bench`

Rules:

* require proof it is not installed on any site
* require backup unless no site is affected

## Actions to defer

Do not expose these in the first normal operator workflow:

* raw `bench execute`
* raw `bench console`
* raw database console commands
* `bench reinstall`
* `bench trim-database`
* `bench trim-tables`
* `bench transform-database`
* `bench run-patch`
* `bench bypass-patch`
* `bench drop-site --force`
* system firewall and SSH port changes

These may exist later behind restricted break-glass workflows.

## Initial implementation priority

Build in this order:

1. `doctor`
2. `server_preflight`
3. `install_server_dependencies`
4. `install_bench`
5. `register_bench`
6. `create_bench`
7. `list_benches`
8. `bench_status`
9. `list_sites`
10. `create_site`
11. `get_app`
12. `install_app`
13. `list_site_apps`
14. `backup_site`
15. `migrate_site`
16. `build_assets`
17. `restart_bench`

Only after those are stable should 3plug expose restore, drop-site, uninstall-app, production setup, domain, and SSL workflows.

## Source links

Official docs:

* https://docs.frappe.io/framework/user/en/tutorial/install-and-setup-bench
* https://docs.frappe.io/framework/user/en/tutorial/create-a-site
* https://docs.frappe.io/framework/user/en/bench/guides/setup-production

Local source references:

* `3plug/repos/platform/triotek-bench/docs/bench_usage.md`
* `3plug/repos/platform/triotek-bench/docs/commands_and_usage.md`
* `3plug/repos/platform/triotek-bench/bench/commands/make.py`
* `3plug/repos/platform/triotek-bench/bench/commands/setup.py`
* `3plug/repos/apps-core/triotek-frappe/frappe/commands/site.py`
* `3plug/repos/apps-core/triotek-frappe/frappe/commands/scheduler.py`
* `3plug/repos/apps-core/triotek-frappe/frappe/commands/utils.py`
