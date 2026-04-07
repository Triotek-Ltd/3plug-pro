# 3plug Project Repo Model

## Short answer

Yes.

Triotek should have a repo for the whole project as well as the individual repos for apps, forks, platform services, and stack definitions.

## Why both are needed

The per-repo model is necessary because:

* each app or platform component should have its own lifecycle
* 3plug will provision from specific controlled repos
* maintenance, permissions, releases, and compatibility are easier to manage per repo

The whole-project repo is still useful because it can act as:

* the master architecture and planning repo
* the onboarding repo for developers
* the documentation root
* the place that links all platform repos together
* the place for workspace bootstrap scripts and environment setup guidance

## Recommended whole-project repo

Use a dedicated organization-owned repo such as:

* `Triotek-Ltd/3plug-pro`

## What should live in the whole-project repo

The whole-project repo should contain:

* architecture docs
* roadmap docs
* standards and governance docs
* repo catalog references
* developer setup guides
* workspace bootstrap scripts
* local orchestration helpers
* non-secret configuration templates

It should not become a dumping ground for all app code.

## What should stay in separate repos

These should remain separate:

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`
* `3plug-pro-control`
* `3plug-pro-catalog`
* `3plug-pro-ops`
* every Triotek app repo

## Best structure

The cleanest model is:

* one whole-project repo for coordination
* many controlled component repos for actual platform and app code

## Local workspace interpretation

The current `rnd/3plug` area behaves like the planning and coordination root.

Later, the real organization-owned `3plug-pro` repo can hold:

* the documents from this planning phase
* source bootstrap conventions
* repo maps
* branch model docs
* operating standards

## Bottom line

Yes, if you ask now, the answer is that Triotek should have:

* a repo for the whole 3plug-pro project
* separate repos for each major app or component

That gives you both strategic coordination and clean engineering boundaries.
