# 3plug Source Strategy

## Decision

3plug will use Triotek-controlled repositories only.

That means:

* no direct production dependency on `github.com/frappe/*`
* no direct production dependency on random community repos
* all approved source code must exist under Triotek-controlled repositories
* upstream changes are reviewed, merged, adapted, or rejected by Triotek

This is the source-governance model for 3plug.

## Core rule

Triotek will intake only the upstream branch it actually wants to follow and operate from a controlled source base built around that.

In practice:

* Triotek keeps its own `frappe` repo
* Triotek keeps its own `erpnext` repo
* Triotek keeps its own `bench` repo
* Triotek keeps its own copies of any official or community apps it chooses to support
* each upstream-derived repo tracks only the chosen upstream branch, not the full upstream branch universe
* 3plug provisions only from the Triotek catalog of Triotek-controlled repos

## Versioning strategy

Triotek should choose a major-version baseline and stay disciplined around it.

Recommended starting approach:

* pick a stable Frappe major version, such as `v16`
* standardize the Triotek stack on that major version
* avoid rushing minor updates unless they are required
* selectively backport security fixes and critical patches into the Triotek forks
* move to the next major version only through a planned upgrade program

## Branch simplification policy

For upstream-derived repos, Triotek should not mirror everything.

The preferred branch model is:

* `upstream-v16`
* `main`

Where:

* `upstream-v16` tracks the chosen upstream release line, such as `version-16-hotfix`
* `main` is the Triotek-controlled working and release branch

This is the default model unless there is a strong reason to add more branches.

## Intentional divergence policy

Triotek is allowed to diverge from upstream.

That divergence should be intentional, documented, and governed.

Examples of acceptable divergence:

* security hardening
* Kenya-specific localization
* reconciliation architecture
* forensic controls
* operational tooling for 3plug
* UI and workflow decisions
* version pinning and dependency control

## Important warning

Diverging completely from upstream is possible, but it increases maintenance cost.

The safest version of this strategy is:

* own the repos fully
* control merges strictly
* diverge where there is business value
* avoid unnecessary deep framework edits unless there is a strong reason

So the operating mindset should be:

* controlled fork, not careless drift

## Repo classes under this model

Every repo used by 3plug falls into one of these classes:

### 1. Triotek platform forks

Examples:

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`

### 2. Triotek curated forks

Examples:

* `triotek-hrms`
* `triotek-crm`
* `triotek-helpdesk`
* `triotek-healthcare`
* `triotek-utility-billing`

### 3. Triotek native repos

Examples:

* `3plug-control`
* `3plug-catalog`
* `triotek-payments`
* `triotek-recon`
* `triotek-forensics`

## Upstream intake policy

No upstream change should go straight into the production source base.

The process should be:

1. fetch upstream changes for the tracked upstream branch
2. update `upstream-v16`
3. review the delta into `main`
4. test the change in the Triotek stack
5. approve and merge intentionally
6. release through the 3plug catalog

## Update policy

Triotek should not behave like a passive downstream consumer.

Recommended policy:

* review upstream monthly
* patch for security as needed
* bundle compatibility updates deliberately
* avoid unnecessary minor-version churn
* keep release notes per Triotek repo

## 3plug provisioning rule

3plug should provision only from:

* Triotek-controlled repos
* Triotek-approved branches or tags
* Triotek-defined stack manifests

Operators should not be able to type arbitrary upstream repo URLs into production workflows.

## Bottom line

Yes, 3plug can and should be built around Triotek-owned repositories if that is the chosen governance model.

The right way is:

* own the source
* control updates
* pin the version base
* absorb only what Triotek approves
* let 3plug provision from that governed source ecosystem
