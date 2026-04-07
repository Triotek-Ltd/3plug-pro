# 3plug Upstream Intake Policy

## Purpose

This document defines the strict rules for Triotek engineers who maintain the Triotek-controlled forks and mirrors used by 3plug.

It applies to:

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`
* all internalized official apps
* all internalized community apps

## Core rule

No upstream change enters the Triotek-controlled source base automatically.

Every upstream change must be:

* reviewed
* classified
* tested
* merged intentionally

## What maintainers are responsible for

Maintainers are responsible for:

* tracking upstream security issues
* reviewing upstream bug fixes
* evaluating compatibility impact
* protecting the Triotek version baseline
* documenting every intake decision

## Version baseline rule

Triotek will standardize on a chosen major version baseline, such as `v16`.

Maintainers must:

* keep Triotek release lines pinned to that baseline
* avoid casual minor-version churn
* prefer selective backports over unnecessary upgrade drift
* move to a new major version only through a planned migration program

## Allowed reasons to intake upstream changes

Upstream changes may be accepted for:

* security fixes
* critical bug fixes
* dependency risk reduction
* compatibility with Triotek-owned apps
* clearly valuable platform improvements

## Reasons to reject or defer upstream changes

Changes should be deferred or rejected when they:

* create unnecessary churn
* break Triotek compatibility assumptions
* introduce operational risk
* conflict with Triotek hardening or control requirements
* do not add meaningful value to the governed stack

## Mandatory intake workflow

For each upstream candidate change:

1. identify the upstream change or release
2. classify it as security, bug fix, feature, dependency, or breaking change
3. record the target Triotek repo and branch
4. review compatibility with the `v16-triotek` line
5. test it in a controlled non-production stack
6. approve, defer, or reject it
7. document the result
8. tag a Triotek release if accepted

## Documentation required for each accepted intake

Maintainers must record:

* upstream source reference
* reason for intake
* risk notes
* affected repos
* target release branch
* test status
* release tag created

## Security rule

Security-related fixes should be prioritized even when general feature updates are paused.

But even security fixes must still be:

* reviewed
* tested
* documented

## No-shortcut rules

Maintainers must not:

* pull directly from upstream into production branches without review
* let `main` become the production source
* mix unrelated feature work into security intake branches
* strip provenance from upstream-derived code
* make undocumented fork changes to core repos

## Production release rule

3plug should deploy only from:

* approved Triotek tags
* or explicitly approved compatibility branches in non-production environments

Never deploy raw upstream code through 3plug.

## Internal expectation

By choosing this model, Triotek is taking ownership of the stack.

That means maintainers are not just developers. They are stewards of the platform baseline.
