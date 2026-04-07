# 3plug-pro Upstream Intake Workflow

## Purpose

This document defines the exact workflow Triotek should use for upstream-derived repos.

The goal is to keep upstream intake simple, reviewable, and repeatable so the team can focus on building the real platform and apps instead of wrestling with source chaos.

## Standard branch model

For every upstream-derived repo, keep only:

* `upstream-v16`
* `main`

## Meaning of the branches

### `upstream-v16`

This is the tracked upstream branch.

It should map to the chosen upstream release line, for example:

* `version-16-hotfix`

This branch is not for normal Triotek feature work.

### `main`

This is the Triotek-controlled branch used for:

* approved platform work
* Triotek fixes
* controlled local changes
* release tags

## Standard local workflow

### 1. Clone the repo locally

For upstream-derived repos, clone or update the local controlled mirror or working copy.

### 2. Refresh upstream branch

Fetch the chosen upstream branch and update:

* `upstream-v16`

### 3. Review differences

Compare:

* `upstream-v16`
* `main`

This is the real intake review surface.

### 4. Merge through PR

Open a PR inside the Triotek repo:

* `upstream-v16` -> `main`

If accepted:

* merge into `main`
* run tests
* tag release when ready

## Initial intake shortcut for a new controlled repo

When Triotek is creating a controlled upstream-derived repo for the first time, the simplest model is:

1. fetch only the upstream branch we care about
2. create `upstream-v16`
3. create `main`
4. force-push only those two branches into the Triotek repo

That gives us a clean controlled repo immediately instead of importing upstream branch clutter.

## Practical rule

Yes, for our standard setup we should prefer:

* fetch the repo we want upstream from
* keep the chosen upstream line locally
* force-push only `upstream-v16` and `main`

That is the cleanest way to start.

### 5. Keep `main` clean

Do not treat `main` like a random scratch branch.

It is the Triotek-controlled release branch.

## Why this matters

This workflow gives Triotek:

* provenance
* small review surface
* cleaner GitHub repos
* predictable updates
* easier onboarding

## What to avoid

Avoid:

* importing hundreds of upstream branches
* mirroring `refs/pull/*`
* using upstream `develop` directly for production
* mixing experimental work into the upstream tracking branch

## Recommended rule for all upstream-derived repos

Apply this to:

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`
* internalized official apps
* internalized community apps

## Recommended helper tooling

3plug-pro should eventually provide a helper command that:

* clones the chosen upstream repo
* tracks one chosen upstream branch
* creates `upstream-v16`
* creates or refreshes `main`
* wires the Triotek remote

That will make intake for future apps much easier.
