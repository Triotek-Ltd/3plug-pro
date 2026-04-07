# 3plug-pro Two-Branch Policy

## Decision

Yes.

For upstream-derived repos, Triotek should keep the branch model minimal.

Instead of carrying the whole upstream branch universe, the practical model should be:

* one upstream-tracking branch
* one Triotek working branch

## Recommended branch pair

For each upstream-derived repo:

* `upstream-v16` = the tracked upstream baseline branch we choose to follow
* `main` = the Triotek-controlled branch we actually use

## What this means

Triotek does not need to mirror hundreds of upstream feature branches, PR branches, or temporary maintenance branches.

We only need:

* the specific upstream release line we care about
* our own controlled branch built from it

That is enough for:

* controlled updates
* code review
* PR-based intake
* release discipline

## Practical workflow

### Step 1

Choose the upstream branch we want to track.

Example:

* `version-16-hotfix`

### Step 2

Create a local tracking branch in the Triotek repo:

* `upstream-v16`

### Step 3

Create or refresh the Triotek working branch:

* `main`

### Step 4

When upstream changes matter:

* fetch upstream
* update `upstream-v16`
* open a PR or controlled merge into `main`
* test
* release

## Why this is better

This model is cleaner because:

* the repo stays understandable
* default branches stay sane
* GitHub views stay usable
* the team reviews only what matters
* 3plug only depends on controlled branches

## What to avoid

Avoid:

* mirroring every upstream branch
* pushing `refs/pull/*`
* keeping noisy maintenance branches in the Triotek org
* using upstream `develop` directly in production

## For Triotek repos

The intended branch model becomes:

### Upstream-derived repos

* `upstream-v16`
* `main`

Examples:

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`
* `triotek-hrms`
* `triotek-crm`

### Triotek-native repos

Usually just:

* `main`

Optionally later:

* `release-v16`

if a separate release line is needed.

## Intake model

Yes, the correct operational pattern is:

* clone the upstream branch we care about
* keep that as the upstream-tracking branch
* make Triotek changes on `main`
* use PRs or controlled merges from `upstream-v16` into `main`

That is much better than dragging the full upstream branch graph into the company org.
