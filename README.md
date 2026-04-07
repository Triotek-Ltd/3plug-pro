# 3plug-pro

3plug-pro is Triotek's governed platform layer for operating Frappe-based systems through company-controlled repositories, controlled releases, stack manifests, and operational automation.

This repository is intended to be the coordination and standards root for the wider 3plug-pro ecosystem under `Triotek-Ltd`.

3plug-pro is the platform we are building in this git repository.

Current design notes live in:

* `design/`

Start implementation planning from:

* `design/roadmap.md`

The local source workspace lives in:

* `3plug/repos/`

## What belongs here

* architecture and planning
* platform standards
* source-governance rules
* branch and release model
* stack and repo strategy
* developer onboarding
* bootstrap scripts
* workspace conventions

## What does not belong here

This repo should not contain all platform and app code directly.

Component code should live in dedicated repos such as:

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`
* `3plug-pro-control`
* `3plug-pro-catalog`
* `3plug-pro-ops`
* `triotek-payments`
* `triotek-recon`
* `triotek-forensics`

## Ecosystem intent

3plug-pro exists to ensure that:

* Triotek owns the source of truth
* 3plug-pro provisions only from governed sources
* upstream changes are absorbed intentionally
* platform operations are traceable and auditable
