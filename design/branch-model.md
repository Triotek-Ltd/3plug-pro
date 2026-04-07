# 3plug Branch Model

## Purpose

This document defines how Triotek should structure branches, tags, and release flow across all repositories used by 3plug.

The goal is to make version control predictable, secure, and compatible with the decision to run only Triotek-controlled repositories.

## Core rule

Every production repo used by 3plug must have:

* one clear default working branch
* one clear upstream-tracking branch if the repo is upstream-derived
* tagged releases for approved deployments

3plug should provision from approved tags or approved compatibility branches, not from ad hoc commits.

## Recommended naming model

### Default development branch

Use:

* `main`

This is where active Triotek development happens.

### Upstream-tracking branches

Use:

* `upstream-v16`
* `upstream-v17`

These branches track the chosen upstream release line only.

### Triotek working branch

Use:

* `main`

This is the branch Triotek actually works from and releases from.

## Recommended release tags

Use a predictable format like:

* `v16.0.0-triotek.1`
* `v16.0.0-triotek.2`
* `v16.1.0-triotek.1`

For app repos:

* `v16.0.0-app.1`
* `v16.0.1-app.2`

The exact style can be refined later, but it should always communicate:

* compatibility base
* Triotek release identity
* release order

## Release flow

Recommended flow:

1. upstream changes are fetched into `upstream-v16`
2. Triotek reviews the delta
3. approved changes are merged into `main`
4. a release tag is created from `main`
5. 3plug catalog marks that tag as deployable

This avoids dragging the whole upstream branch graph into the Triotek repo.

## Rule for upstream-based repos

For repos like:

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`
* `triotek-hrms`
* `triotek-crm`
* `triotek-helpdesk`
* `triotek-insights`
* `triotek-lending`

Use:

* `upstream-v16` for tracked upstream intake
* `main` for Triotek engineering and releases

## Rule for Triotek-native repos

For repos like:

* `3plug-control`
* `3plug-catalog`
* `3plug-ops`
* `triotek-payments`
* `triotek-recon`
* `triotek-forensics`
* `triotek-trading-base`

Use:

* `main` for active development
* `v16-compatible` only if a dedicated compatibility line is actually needed

If the app is early and only supports one major stack, keeping only `main` is acceptable for a while.

## Emergency patch rule

For urgent production fixes:

* branch from `main` or the current release tag
* fix and review quickly
* tag a new release
* keep `upstream-v16` as upstream-only intake state when possible

Do not hotfix production with untracked direct commits.

## 3plug deployment rule

3plug should deploy only from:

* approved release tags
* or explicitly approved compatibility branches in non-production environments

Production should not track raw development commits without approved release tags.

## Minimum metadata every repo should carry

Every repo should clearly state:

* supported Frappe/ERPNext major version
* compatibility branch name
* current approved release tag
* owner or team
* whether it is native, forked, or mirrored

## Bottom line

The cleanest starting model is:

* `upstream-v16` for tracked upstream intake
* `main` for Triotek-controlled work
* versioned release tags for deployment

That gives Triotek discipline without making the branch strategy too heavy too early.
