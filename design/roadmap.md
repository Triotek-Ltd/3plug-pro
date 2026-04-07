# 3plug-pro Roadmap

## Purpose

This roadmap turns the 3plug-pro design into a build order.

Current progress is tracked in `roadmap-status.md`.

3plug-pro is the git-tracked platform root.

The first product target is:

```text
pip install 3plug
3plug server preflight
3plug install server-dependencies
3plug install bench
3plug bench create production
3plug site create <site> --bench production
```

Triotek's target stack is Frappe v16 only.

## Phase 0: Repo Cleanup and Build Foundation

Goal:

* make the 3plug-pro repo safe and clear to build from

Deliverables:

* root `.gitignore`
* `design/` folder and design index
* root README updated to point to `design/` and `3plug/repos/`
* CLI paths updated from old `rnd/3plug/...` assumptions to current repo-root-relative paths
* package naming decision documented
* tests or smoke checks for the current CLI

Done when:

* `git status` shows only intentional project files
* source clones under `3plug/repos/` stay ignored by the main repo
* `3plug-pro doctor` works from the repo root

## Phase 1: 3plug CLI Package

Goal:

* create the pip-installable `3plug` operator CLI

Deliverables:

* package entry point for `3plug`
* keep or bridge the existing `3plug-pro` command during transition
* CLI command groups:

```text
3plug doctor
3plug init
3plug server preflight
3plug install bench
3plug bench list
3plug job list
```

* local config path
* local data path
* command output format that is readable and scriptable

Done when:

* `python -m threeplugpro.cli --help` works
* installed console command exposes `3plug`
* `3plug doctor` reports the repo and source workspace correctly

## Phase 2: Local State and Job Store

Goal:

* make every action recordable before it executes

Deliverables:

* SQLite state database
* tables or equivalent records for:

```text
servers
environments
benches
sites
app_sources
stacks
jobs
audit_events
backups
```

* `3plug init` creates local state
* `3plug job list`
* `3plug job show <job-id>`
* basic audit event creation

Done when:

* local state can be initialized repeatedly without corrupting data
* a dry-run job can be recorded and shown

## Phase 3: Server Preflight

Goal:

* inspect the managed server before installing Bench

Deliverables:

* `3plug server preflight`
* v16 checks for:

```text
OS baseline
git
Python 3.14
uv
pip 25.3+
Node.js 24
npm
Yarn 1.22+
MariaDB 11.8
Redis / Valkey 6+
wkhtmltopdf 0.12.6 with patched Qt
xvfb
libfontconfig
cron
nginx
supervisor or systemd
```

* structured pass/warn/fail output
* remediation summary

Done when:

* preflight can run without sudo
* missing tools are reported without crashing the whole command
* results are recorded as a job/audit event

## Phase 4: Server Dependency Installer

Goal:

* install the server-side dependencies needed for a non-Docker Frappe v16 Bench setup

Deliverables:

* `3plug install server-dependencies`
* OS detection and policy guardrails
* install plan preview
* explicit approval path for system package changes
* no secrets in logs
* record installed versions

Done when:

* command can show an install plan before changing the server
* command refuses unsupported OS/version combinations unless an override is explicitly added

## Phase 5: Bench Installer

Goal:

* make 3plug responsible for installing Bench before managing benches

Deliverables:

* `3plug install bench`
* install source selection:

```text
Triotek-controlled triotek-bench source
approved upstream fallback
```

* installed Bench executable path recorded
* installed Bench version recorded
* install method recorded

Done when:

* `3plug install bench` can detect an existing Bench install
* command can install or report the exact next action
* `3plug doctor` includes Bench install state

## Phase 6: Bench Registry and Multi-Bench Support

Goal:

* manage multiple Bench runtimes on one server

Deliverables:

* `3plug bench create <name>`
* `3plug bench register <name> --path <path>`
* `3plug bench list`
* `3plug bench status <name>`
* v16 defaults:

```text
Frappe install branch: main
ERPNext install branch: main
Upstream tracking branch: upstream-v16
Python: 3.14
Node.js: 24
```

* approved work-root validation
* default bench configuration

Done when:

* more than one bench can be registered
* commands can target a bench by name
* no command assumes only one `frappe-bench` path

## Phase 7: Catalog and Stack Reader

Goal:

* make app installation source-controlled and catalog-driven

Deliverables:

* read approved app sources from catalog config
* read stack definitions
* `3plug app list`
* `3plug stack list`
* default `erpnext-core` stack for v16
* block arbitrary production Git URLs by default

Done when:

* 3plug can resolve an app name to an approved local path or repo URL
* 3plug can resolve a stack to ordered app install steps

## Phase 8: Site Lifecycle V1

Goal:

* create and manage sites through controlled Bench jobs

Deliverables:

* `3plug site list --bench <name>`
* `3plug site create <site> --bench <name> --stack <stack>`
* `3plug site install-app <site> <app> --bench <name>`
* `3plug site apps <site> --bench <name>`
* `3plug site migrate <site> --bench <name>`
* `3plug site backup <site> --bench <name>`

Done when:

* site commands create job records
* site commands use locks
* site commands capture logs
* backups create backup records

## Phase 9: Production Guardrails

Goal:

* make risky operations explicit and safe before production use

Deliverables:

* production environment flag
* elevated approval flow
* backup-before-migrate policy
* restore request workflow
* drop-site disabled by default
* raw shell disabled by default
* command redaction for secrets
* concurrent job locks for server, bench, and site scopes

Done when:

* restricted actions cannot run accidentally
* production actions leave an audit trail

## Phase 10: Local Service and UI Path

Goal:

* move from CLI-only to Press-like control plane experience

Deliverables:

* local API service
* background worker
* job queue
* operator UI
* job log viewer
* bench/site inventory pages
* backup history pages

Done when:

* normal operators can use the UI instead of shell commands for common workflows

## Later: Multi-Server Runner

Goal:

* manage multiple servers from one central 3plug-pro control plane

Deliverables:

* lightweight runner per server
* runner registration
* runner heartbeat
* remote job dispatch
* remote log streaming
* per-server Bench inventory

Done when:

* one central 3plug-pro control plane can manage Bench runtimes on more than one server

## Immediate Next Step

Start with Phase 0 and Phase 1:

1. Fix existing CLI paths to match the new repo layout.
2. Add the `3plug` console command alongside `3plug-pro`.
3. Make `doctor` validate `design/`, `3plug/repos/`, and platform source folders.
4. Add the first smoke test for `doctor`.
