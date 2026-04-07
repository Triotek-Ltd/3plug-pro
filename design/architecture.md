# 3plug Architecture

## What 3plug is

`3plug` is Triotek's proposed control plane for managing Frappe/ERPNext environments using our own repositories, our own workflows, and our own operational rules.

The simplest way to think about it is:

* `Bench` is the execution engine
* `3plug` is the control plane
* Triotek repos are the source of truth
* the UI is the operator interface
* workers and automation jobs are the orchestration layer

If built properly, `3plug` can replace a large part of what teams normally use Press or Docker-based operational stacks for.

It should not be treated as just a UI wrapper around Bench. It is a platform layer.

## What 3plug should do

3plug should manage the full lifecycle of Frappe-based systems:

* app source registration
* repository selection
* environment creation
* site creation
* app installation
* migrations
* updates
* backups
* restores
* config changes
* secrets handling
* user and tenant management
* monitoring hooks
* audit logging
* deployment workflows

## What 3plug can replace

If fully implemented, 3plug can replace:

* Press-style environment and site control
* shell-driven Bench operations
* parts of Docker-driven operational workflows
* manual deploy and update procedures
* ad hoc backup and restore handling

## What 3plug does not magically replace

Even with a strong UI, 3plug still needs real infrastructure and ops underneath it.

It still needs:

* server provisioning
* process supervision
* database operations
* storage management
* TLS and domain handling
* networking and firewall rules
* secrets protection
* backup storage
* monitoring
* failure recovery

The UI is only one layer. The real replacement comes from building the orchestration and governance behind it.

## Core design principle

Do not fork Bench heavily unless absolutely necessary.

The safer design is:

* keep Bench mostly standard
* keep business logic in 3plug
* keep app logic in Triotek apps
* keep orchestration in 3plug jobs and services
* call Bench as a managed execution backend

That reduces maintenance pain when Frappe changes upstream.

## Recommended system layers

## 1. Control Plane UI

This is the operator dashboard.

It should allow authorized users to:

* create environments
* create sites
* register repos
* choose app stacks
* install apps
* run migrations
* trigger backups
* restore from backups
* rotate secrets
* view job status
* review audit history
* manage customers or tenants

This UI should not perform heavy work directly. It should create jobs.

## 2. API Layer

This is the service used by the UI and automation.

It should:

* validate requests
* enforce permissions
* store job intents
* persist state
* expose status
* coordinate with workers

This layer becomes the formal interface for platform actions.

## 3. Job and Orchestration Layer

This is where real operations happen.

It should:

* dequeue jobs
* execute Bench actions
* call system scripts
* capture logs
* update job status
* apply retries where safe
* stop dangerous or conflicting operations

This layer is what turns the UI into an actual platform.

## 4. Bench Execution Layer

This is the managed runtime wrapper around Bench.

It should:

* run Bench commands in controlled contexts
* pin paths and environments
* isolate per environment or tenant where needed
* capture stdout and stderr
* attach audit metadata to every action

Bench should be treated like a controlled subsystem, not a free-form shell tool.

## 5. Repository and Release Layer

This handles Triotek-owned source control and app versions.

It should:

* register approved repos
* define allowed branches or tags
* pin versions per environment
* support release promotion
* track what code is deployed where

This is critical if 3plug is going to use Triotek repos instead of generic public stacks.

## 6. State and Metadata Layer

3plug needs its own database to track platform state.

It should store:

* tenants
* environments
* sites
* app stacks
* repo references
* releases
* jobs
* secrets references
* audit events
* backup records
* domain records
* user permissions

Without a strong state model, the UI becomes unreliable.

## 7. Secrets and Config Layer

This must manage:

* DB credentials
* app secrets
* API keys
* encryption keys
* callback secrets
* deployment tokens

Secrets should never be treated as plain configuration fields casually exposed to admins.

## 8. Audit and Forensics Layer

Every 3plug action should be auditable.

That includes:

* who triggered it
* when it was triggered
* what system object was affected
* what command or job ran
* what the result was
* what changed

This is especially important if 3plug becomes the system used to manage client production environments.

## 9. Backup and Recovery Layer

3plug should manage:

* scheduled backups
* backup verification
* restore requests
* restore approvals
* restore history

Backups should be first-class platform objects, not just files on disk.

## 10. Observability Layer

3plug should expose:

* job logs
* site health
* queue health
* backup status
* migration status
* failure alerts
* environment status

Without this, operators will still fall back to shell-based firefighting.

## Replacement model

## Replacing Press

3plug can replace Press for Triotek if it manages:

* multi-site lifecycle
* app deployment logic
* operational permissions
* backups and restores
* environment visibility
* update workflows
* auditability

Press is more than a dashboard. 3plug must match the operational control pattern, not just the appearance.

## Replacing Docker workflows

3plug can reduce or replace parts of Docker-driven workflows if Triotek chooses to run Bench environments directly on managed hosts or VMs.

If Docker remains useful for isolation or packaging, 3plug can still sit above Docker.

The real decision is not "Bench or Docker." The real decision is:

* what is the execution substrate
* what is the orchestration layer
* what is the operator interface

3plug should own orchestration and interface regardless of whether the runtime under it is native, containerized, or hybrid.

## Recommended implementation strategy

## Phase 1: Controlled Bench Wrapper

Build 3plug as a safe command and job runner for Bench.

Goals:

* approved actions only
* job history
* repo registration
* site creation
* app install/update
* logs and status

At this phase, 3plug is mainly a safer control layer.

## Phase 2: Environment and Tenant Manager

Add:

* environment records
* tenant/site inventory
* backup scheduling
* restore workflows
* release tracking
* permission controls

At this phase, 3plug becomes a platform manager.

## Phase 3: Full Control Plane

Add:

* secrets workflows
* domain management hooks
* deeper monitoring
* reconciliation and audit exports
* managed support actions
* environment health automation

At this phase, 3plug becomes a real internal Press replacement.

## Must-have non-functional requirements

If 3plug is going to manage production environments, it must have:

* role-based access control
* audit logging
* idempotent job execution where possible
* rollback-aware deployment logic
* concurrency protection
* secrets discipline
* environment isolation rules
* backup verification
* human-readable operational logs

## Questions 3plug must answer reliably

Before calling it a true platform, 3plug should always answer:

* What sites exist?
* What apps are installed on each site?
* Which repos and branches are deployed?
* Who deployed the latest change?
* What jobs ran recently?
* Which backups exist and were they verified?
* What failed and why?
* What changed in the environment?

If 3plug cannot answer these cleanly, it is still a tool, not yet a control plane.

## Recommended positioning

Internally, Triotek should describe 3plug like this:

3plug is Triotek's Bench control plane for managing Frappe-based systems, deployments, environments, backups, and operational workflows using our own repos, our own policies, and our own automation.
