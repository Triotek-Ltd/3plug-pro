# 3plug Developer Source Layout

## Purpose

This document defines how the real 3plug codebase should exist locally on a developer machine.

The goal is consistency.

Every Triotek developer working on the ERP platform should see the same source layout pattern, the same repo naming pattern, and the same relationship between:

* local source folders
* Triotek-Ltd organization repos
* 3plug stack definitions

## Core rule

The source of truth belongs to the GitHub organization:

* `Triotek-Ltd`

Not to personal GitHub accounts.

Personal accounts may be members, maintainers, or contributors, but the repos themselves should live in the organization.

## What the local machine is

The local machine is the working copy of the Triotek-controlled source ecosystem.

That means:

* the real codebase is what we keep locally and sync with `Triotek-Ltd`
* the local folders should reflect the governed repo structure
* developers should not invent random layouts per machine

## Recommended local layout

Under the ERP workspace, keep the source tree in a stable structure like this:

* `rnd/3plug/repos/`

## Meaning of each folder

### `repos`

This is the main working tree layout that developers and Bench should use directly.

Recommended groups:

* `rnd/3plug/repos/platform/`
* `rnd/3plug/repos/apps-core/`
* `rnd/3plug/repos/apps-vertical/`
* `rnd/3plug/repos/stacks/`
* `rnd/3plug/repos/docs/`

## Recommended developer setup rule

Every developer setup should follow the same basic pattern:

1. clone the ERP workspace
2. sync or clone the Triotek-Ltd repos into the expected local working folders under `rnd/3plug/repos`
3. work only against the Triotek-controlled source tree
4. never treat personal forks as the long-term source of truth

## Organization-first rule

When a repo is ready to exist officially, it should be created under:

* `Triotek-Ltd`

Then developer machines should connect to that repo as the canonical remote.

Personal remotes can exist for contribution convenience, but they should not be treated as the primary ownership location.

## Practical repo mapping example

### Local working tree path

`rnd/3plug/repos/apps-core/triotek-erpnext`

### Intended canonical remote

`Triotek-Ltd/triotek-erpnext`

### Same idea for native repos

#### Local path

`rnd/3plug/repos/platform/3plug-pro-control`

#### Intended canonical remote

`Triotek-Ltd/3plug-pro-control`

## Final rule

Yes, the real codebase is exactly what we are aiming for.

The planning documents are only the setup layer.

The end state is:

* organization-owned repos under `Triotek-Ltd`
* local source trees that mirror that governed structure
* 3plug provisioning only from that controlled Triotek source ecosystem
