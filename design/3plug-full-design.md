# 3plug Full Design

## Product intent

3plug is Triotek's Bench control plane for Frappe systems.

It should give Triotek a Press-like operating experience while using Bench as the execution engine.

The first target is a single-server Frappe v16 platform that can manage multiple local Bench runtimes and many sites.

The later target is one central 3plug control plane that can manage multiple servers through lightweight runners.

## Non-negotiable principle

3plug should not become a free-form shell wrapper.

Every platform action should be:

* named
* validated
* authorized
* recorded as a job
* executed by a controlled runner
* logged
* auditable

## Top-level runtime model

```text
pip install 3plug
        |
        v
3plug CLI / API / UI
        |
        v
3plug control state
        |
        v
3plug jobs
        |
        v
local 3plug runner
        |
        v
triotek-bench
        |
        v
one server -> multiple benches -> many sites
```

## V1 server model

V1 assumes one physical or virtual server.

That server may have multiple Bench runtimes.

In this design, `local` means local to the managed server where 3plug's runner executes Bench commands.

For V1, the control plane, runner, Bench folders, and sites may all live on the same single server.

This does not mean `local` must always be the developer laptop. In production, `local` means the production server's own filesystem and runtime context.

Examples:

* `dev`
* `staging`
* `production`
* `client-acme`
* `frappe-v16`

3plug should not hard-code one `frappe-bench` path.

Every site action should either:

* specify a bench name
* specify a bench path
* or use a configured default bench

## Later multi-server model

The later model is:

```text
central 3plug control plane -> lightweight runner per server -> local Bench per server
```

Each server should run Bench locally.

Each server should only need a small runner service, not its own full 3plug UI and database, unless Triotek intentionally wants isolated deployments.

## Main components

### 1. 3plug CLI

The first user-facing interface should be a pip-installed command:

```text
pip install 3plug
3plug --help
```

Initial command groups:

```text
3plug doctor
3plug init
3plug server preflight
3plug install server-dependencies
3plug install bench
3plug bench list
3plug bench create
3plug bench status
3plug site list
3plug site create
3plug site install-app
3plug site migrate
3plug site backup
3plug app list
3plug stack list
3plug job list
3plug job show
```

The CLI may later call a local API, but at first it can use local config and a local job store.

### 2. 3plug Control

`3plug-control` is the main control plane.

Responsibilities:

* state model
* environment registry
* server registry
* bench registry
* site registry
* job submission
* audit records
* operator permissions
* API endpoints
* later UI

In V1, this can begin as a Python package with a CLI and local SQLite state.

Later, it can become a Frappe app or service if Triotek wants a web UI and richer permissions.

### 3. 3plug Ops

`3plug-ops` owns execution workflows.

Responsibilities:

* job runner
* command planning
* Bench command execution
* stdout and stderr capture
* retry policy
* maintenance windows
* migration workflows
* backup workflows
* restore workflows
* lock handling

V1 can run jobs synchronously from the CLI.

The next step should add a background worker.

### 4. 3plug Catalog

`3plug-catalog` owns approved source and stack definitions.

Responsibilities:

* approved repos
* app metadata
* stack manifests
* branch and tag rules
* compatibility notes
* default install sets
* environment-specific app rules

The catalog should be the reason 3plug knows which repos may be installed.

Operators should not normally pass arbitrary GitHub URLs for production workflows.

### 5. triotek-bench

`triotek-bench` remains Bench.

It should be Triotek-controlled, but not turned into the whole platform.

Use it for:

* Bench runtime commands
* Frappe site lifecycle
* app installation
* migrations
* backups
* production setup tasks where appropriate

Do not move 3plug's policy, audit, catalog, or UI responsibilities into Bench.

## Core data model

### Server

Tracks a machine that can run Bench.

Fields:

* name
* hostname
* mode: `local` or `remote`
* runner status
* root work directory
* OS metadata
* created at
* updated at

V1 should create one default server named `local`.

### Environment

Tracks a logical operating context.

Fields:

* name
* type: `development`, `staging`, `production`, or `client`
* server
* default bench
* policy template
* notes

### Bench Runtime

Tracks one Bench folder.

Fields:

* name
* server
* path
* Frappe repo
* Frappe branch
* ERPNext repo
* ERPNext branch
* Bench repo
* Bench branch
* Python version
* Node version
* Redis mode
* MariaDB target
* process mode
* default stack
* status

### Site

Tracks one Frappe site.

Fields:

* name
* bench
* environment
* domain
* installed apps
* site status
* maintenance mode
* backup policy
* last migration job
* last backup job

### App Source

Tracks an approved app repo.

Fields:

* app name
* internal repo name
* local path
* source type: `triotek-native`, `fork`, `mirror`, or `reference`
* upstream URL
* approved branches
* approved tags
* default branch
* catalog status

### Stack

Tracks an installable group of apps.

Fields:

* name
* Frappe branch
* ERPNext branch
* app list
* required apps
* optional apps
* compatibility notes
* environment rules

### Job

Tracks an operational action.

Fields:

* job id
* action
* requested by
* status
* server
* bench
* site
* input parameters
* planned commands
* started at
* finished at
* exit code
* log path

### Audit Event

Tracks the business-level action record.

Fields:

* actor
* action
* object type
* object name
* job id
* timestamp
* result
* summary

### Backup

Tracks backup artifacts.

Fields:

* backup id
* site
* bench
* server
* job id
* file paths
* includes files
* database backup path
* created at
* verified status
* restore eligibility

## Controlled Bench actions

V1 should support these approved actions first:

```text
install_bench
register_bench
create_bench
list_benches
bench_status
create_site
list_sites
install_app
migrate_site
backup_site
update_site_apps
set_maintenance_mode
```

Each action should map to one or more Bench commands, but the user should interact with the 3plug action, not raw shell.

## Example workflows

### Bootstrap

```text
pip install 3plug
3plug init
3plug server preflight
3plug install server-dependencies
3plug install bench
3plug bench create production
```

`3plug install bench` is a first-class bootstrap step.

3plug must be able to install Bench before it can create, register, or manage Bench runtimes.

The install source should prefer Triotek-controlled Bench source, while still allowing an explicit fallback to the upstream `frappe-bench` package when approved.

Because 3plug is intentionally not relying on Docker in the first model, server dependencies must be treated as their own lifecycle phase before Bench installation.

The dependency phase should check and install required services and tools such as:

* MariaDB
* Redis
* Python and Python build dependencies
* Node.js
* npm or yarn tooling
* wkhtmltopdf or the approved PDF rendering alternative
* supervisor or systemd process configuration support
* nginx where production web serving is enabled
* fail2ban or other approved hardening tools where production policy requires them

3plug should run `3plug server preflight` before installing system dependencies, and then run `3plug install server-dependencies` before `3plug install bench`.

The detailed dependency policy lives in `server-dependency-plan.md`.

Triotek's current target stack is `frappe-v16` only.

3plug should default to Triotek-controlled `main` branches for Frappe, ERPNext, and apps, while treating `upstream-v16` as the upstream tracking branch. It should not carry v14/v15 compatibility paths unless Triotek explicitly reopens legacy support later.

### Create a site

```text
3plug site create acme.local --bench production --stack erpnext-core
```

3plug should:

* validate the bench exists
* validate the stack exists
* create a job
* run `bench new-site`
* install required apps
* run migrations if needed
* record the site
* record audit events

### Install an app

```text
3plug site install-app acme.local triotek-payments --bench production
```

3plug should:

* confirm the app exists in the catalog
* confirm the app branch is allowed for the bench
* ensure the app exists in the bench apps folder
* run `bench get-app` if needed
* run `bench --site acme.local install-app triotek_payments`
* record the job and audit result

### Backup a site

```text
3plug site backup acme.local --bench production
```

3plug should:

* create a backup job
* run `bench --site acme.local backup`
* record the backup artifacts
* mark backup verification status

## Press reference mapping

Use Frappe Press as a reference for concepts, not as an exact runtime blueprint.

Useful Press concepts:

* Bench
* Bench App
* App Source
* App Release
* Agent Job
* Agent Job Step
* Bench Update
* Bench Site Update
* Bench Shell Log
* Backup Bucket
* Audit Log

3plug simplifications:

* replace remote agent first with local runner
* replace cloud server pools first with one local server record
* replace deploy/build farm first with direct Bench app install/update
* defer billing
* defer marketplace
* defer cloud provider provisioning
* defer autoscaling
* defer complex team subscription logic

## Safety rules

3plug should protect operators from risky accidental actions.

Rules:

* production restore requires elevated approval
* delete site requires elevated approval
* production app source changes require elevated approval
* failed migrations should not be force-rerun silently
* concurrent jobs on the same bench/site should be locked
* raw command execution should be disabled by default
* secrets should not be written into normal logs
* job logs should record commands without exposing secret values

## Implementation phases

### Phase 1: Local CLI and state

Build:

* pip-installable package
* `3plug` command
* local config
* local SQLite job/state database
* bench registry
* catalog reader
* controlled Bench command planner
* synchronous runner

### Phase 2: Multi-bench operations

Build:

* bench create/register/list/status
* site create/list/install-app/migrate/backup
* stack install flow
* job logs
* basic audit history

### Phase 3: Local service mode

Build:

* local API service
* background worker
* operator UI
* better permissions
* backup metadata
* restore workflow
* health checks

### Phase 4: Remote runner mode

Build:

* runner registration
* remote job dispatch
* runner heartbeat
* central server inventory
* per-server Bench inventory
* remote log streaming

## First build decision

The first implementation should happen in `3plug-control` as the pip-installable `3plug` package.

`3plug-ops` and `3plug-catalog` can remain separate planned repos, but V1 may keep small internal modules for ops and catalog until the split becomes valuable.

That avoids over-splitting before the first working Bench flow exists.
