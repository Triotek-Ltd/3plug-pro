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

## First Server Target

The first production-like target can be an actual Linux server. Install the current CLI from GitHub with:

```bash
python3 -m pip install "git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli"
```

Then run:

```bash
3plug --help
3plug init
3plug doctor
3plug server preflight
```

At the current stage, these commands are expected to work:

* `3plug --help`
* `3plug init`
* `3plug doctor`
* `3plug server preflight`
* `3plug app show erpnext`
* `3plug stack list`

These commands are present but still plan/foundation commands until the Linux server phase is implemented:

* `3plug install server-dependencies`
* `3plug install bench`
* `3plug bench create production`

Use `3plug server preflight` on the actual server first, then use its output to finish the real server dependency and Bench install handlers.

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
