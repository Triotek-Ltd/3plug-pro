# 3plug Bench Control Plane Starting Point

## Decision

3plug will start as a single-server Bench control plane.

The first version should behave like a Press-style operator layer, but without trying to copy the full Frappe Cloud / Press multi-server model on day one.

In this note, `local` means local to the managed server where Bench runs. For V1, the 3plug control plane, runner, Bench runtimes, and Frappe sites can all live on that same single server.

Triotek's current platform target is Frappe v16 only.

3plug should default to Triotek-controlled `main` branches for Frappe, ERPNext, and apps, while treating `upstream-v16` as the upstream tracking branch. Older v14/v15 support should not be included unless Triotek explicitly adds a legacy mode later.

## Core model

```text
3plug UI/API/jobs -> local 3plug runner -> triotek-bench -> local benches -> many Frappe sites
```

Bench remains the execution engine.

3plug owns the control plane responsibilities:

* approved actions
* site lifecycle
* app stack selection
* migrations
* backups
* restore requests
* job history
* audit history
* environment and server metadata

## Single-server v1

The first working version should assume:

* one server
* one or more local Bench runtimes
* many Frappe sites managed by Bench
* approved app sources from the 3plug repo catalog
* Triotek-controlled Bench source under `triotek-bench`
* operations executed as controlled jobs, not free-form shell commands

This gives Triotek the practical benefit of a Press-like workflow while keeping the runtime simple.

## Multiple benches on one server

3plug should support multiple Bench folders on the same server.

Each Bench runtime should be tracked as a managed platform object with its own:

* name
* filesystem path
* Frappe branch or version
* app stack
* site list
* process mode
* backup policy
* job history

This lets one server host different benches for different purposes, such as:

* development benches
* staging benches
* production benches
* client-specific benches
* version-specific benches

The early CLI should therefore avoid assuming there is only one hard-coded `frappe-bench` path.

Commands should either accept a bench name/path or use a configured default bench.

## Multi-server later

3plug should still be designed so multi-server support can be added later.

The later model should be:

```text
central 3plug control plane -> lightweight 3plug runner per server -> local Bench per server
```

Each server should not need its own full 3plug control plane unless Triotek intentionally wants isolated deployments.

The central 3plug control plane should eventually track:

* servers
* environments
* Bench paths
* sites per server
* jobs per server
* backups per server
* deployed app versions per site

## What to borrow from Press

Frappe Press should be used as a reference for:

* site lifecycle concepts
* bench or group concepts
* app/source models
* job tracking
* backup records
* update and migration flows
* audit and operational visibility

## What to defer from Press

The first version should not start with:

* billing
* marketplace
* cloud provider provisioning
* Docker build farms
* multi-server scheduling
* complex team subscription flows
* full remote agent orchestration

Those can be revisited after the local Bench control plane is working.

## First implementation target

The first concrete implementation target is a controlled Bench wrapper that can record intent and run approved commands such as:

* create site
* install app
* migrate site
* backup site
* update apps
* list sites
* inspect site state

Every action should create a job record and an audit trail before 3plug becomes responsible for production use.

## Install and operator workflow

3plug should be usable as a Python-installed command-line tool first.

The intended entry point is:

```text
pip install 3plug
```

After installation, operators should use the `3plug` command to bootstrap the local platform:

```text
3plug server preflight
3plug install server-dependencies
3plug install bench
```

That command should install or prepare the Triotek-controlled Bench runtime instead of requiring operators to manually assemble the Bench environment.

Because 3plug is not using Docker in this first model, server dependencies are part of the 3plug lifecycle.

The server must be checked and prepared for MariaDB, Redis, Python, Node.js, package/build dependencies, PDF tooling, process supervision, and nginx before Bench is expected to work reliably.

This dependency setup is v16-first and should use the v16 dependency plan for Python, Node.js, MariaDB, Yarn, and pip.

The detailed dependency plan lives in `server-dependency-plan.md`.

This is not only a setup helper. It is the first Bench lifecycle action 3plug owns.

3plug should be able to install Bench onto the managed server, record the Bench executable path and version, and then use that Bench installation to create or manage multiple Bench runtimes.

The early workflow should then continue through controlled 3plug commands such as:

```text
3plug bench status
3plug site create
3plug app install
3plug site migrate
3plug site backup
```

The command names can be refined during implementation, but the principle should stay the same:

* install 3plug with pip
* use 3plug as the operator command
* let 3plug install and manage Bench
* let Bench manage the Frappe sites
* avoid free-form shell operations for normal platform tasks
