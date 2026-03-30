# 3plug-pro CLI Plan

## Purpose

This document defines the role of the `3plug-pro` CLI.

The CLI should exist so Triotek can reuse the same operational commands in the future instead of relying on ad hoc shell steps every time.

## Why the CLI matters

The CLI gives Triotek:

* repeatable setup flows
* safer publishing flows
* standard repo/bootstrap actions
* controlled source-sync actions
* easier onboarding for developers and operators

## Initial CLI goals

The first version of the CLI does not need to control the whole platform.

It should start with project and source-governance tasks such as:

* validate local workspace structure
* list expected repos
* print publish checklist
* print source-manifest summary
* prepare local repo folders
* verify GitHub CLI auth status
* verify organization access assumptions

## Recommended command groups

### `3plug-pro doctor`

Checks:

* expected local directories exist
* Git is available
* GitHub CLI is available
* GitHub CLI auth status
* current workspace shape

### `3plug-pro repos list`

Shows:

* all planned repos
* repo class
* whether local folder exists

### `3plug-pro repos init`

Initializes local native repo folders if needed.

### `3plug-pro publish plan`

Prints:

* organization repo targets
* publish order
* required auth status

### `3plug-pro auth status`

Wraps:

* GitHub CLI auth checks
* current user
* org visibility checks where possible

## Future command groups

Later, the CLI can grow into:

* source intake helpers
* stack validation
* release preparation
* environment bootstrap
* 3plug-pro catalog validation

## Important security rule

The CLI should never require users to paste tokens into project files or chat history.

Authentication should happen through:

* `gh auth login`
* browser-based login
* or secure environment-driven token usage

## Suggested implementation choice

A Python CLI is a good fit because:

* it is easy to ship
* it is readable
* it can wrap Git and `gh`
* it can later grow into richer automation

## Initial package name

Recommended local package or tool name:

* `threeplugpro`

User-facing command:

* `3plug-pro`
