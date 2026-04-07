# 3plug Scope

## Product statement

`3plug` is Triotek's internal and potentially client-facing control plane for operating Frappe-based systems with our own repositories, our own workflows, and our own governance model.

## Primary goal

Turn Bench from a shell-driven admin tool into a managed platform capability with UI, API, jobs, auditability, and repeatable operational workflows.

## What 3plug v1 should include

## Repository management

* register approved repos
* define branch or tag rules
* assign repos to app stacks
* track what is allowed in each environment

## Environment management

* create environment records
* attach environment metadata
* show environment status
* restrict actions by environment

## Site management

* create site
* list sites
* install app stack
* update site apps
* run migrate
* set maintenance mode
* archive or disable site workflows

## Job execution

* queue actions from UI/API
* run controlled Bench commands
* store logs
* store result status
* support retries where safe

## Audit history

* who triggered an action
* what action ran
* when it ran
* what site or environment it affected
* whether it succeeded or failed

## Backups

* trigger backup
* list backups
* record backup metadata
* trigger restore with controlled flow

## Permissions

* role-based access to actions
* action restrictions by environment
* audit visibility for administrators

## What 3plug v2 should include

* app release promotion
* secrets workflows
* environment templates
* health checks
* scheduler visibility
* worker visibility
* backup verification
* restore approvals
* domain management hooks
* notification system

## What 3plug v3 should include

* multi-tenant customer management
* billing hooks if needed
* usage tracking
* managed support workflows
* support tickets linked to site state
* policy engine for compliance and controls
* evidence export tooling
* advanced drift detection

## What should stay outside 3plug at first

To avoid overbuilding too early, 3plug should not own everything on day one.

Keep these separate initially unless truly needed:

* low-level infrastructure provisioning
* full observability stack
* deep cloud networking
* custom container orchestration
* enterprise billing engine
* general-purpose DevOps unrelated to Frappe operations

## Functional boundaries

3plug should own:

* Frappe platform operations
* Bench-controlled workflows
* environment metadata
* deployment jobs
* operational audit trail

3plug should not become:

* a generic CI/CD replacement for every company system
* a full cloud platform from day one
* a dumping ground for unrelated admin tools

## Recommended v1 operator actions

The UI should expose only controlled actions.

Recommended initial actions:

* create environment
* register repo
* create site
* install apps
* update apps
* run migrate
* run backup
* request restore
* toggle maintenance mode
* view job logs
* view audit history

## Actions that should require higher privilege

* restore production site
* rotate secrets
* delete site
* change production app source
* force rerun failed migration
* modify environment-level configuration

## Non-goals

3plug is not trying to:

* replace Frappe itself
* replace custom business apps
* become a generic hosting company immediately
* eliminate all shell access on day one

It is trying to make Frappe operations safer, clearer, and more repeatable.

## Success criteria for v1

3plug v1 is successful if Triotek can:

* manage site lifecycle without ad hoc shell work for normal tasks
* use Triotek repos as approved app sources
* track operational actions through UI/API
* run updates and migrations with job history
* handle backups and restore workflows more safely
* explain who changed what and when

## Naming and identity

Yes, if Triotek is calling this platform `3plug`, then internal documents, code, UI labels, repos, and service language should use that name consistently.

Recommended internal meaning:

`3plug` = Triotek Platform Layer for Unified Governance

That expansion can be revised later, but the important thing is consistency.
