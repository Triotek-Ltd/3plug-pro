# 3plug Repo Structure

## Purpose

This document defines the recommended repository structure for Triotek's 3plug ecosystem.

The goal is to make it easy for 3plug to use Triotek-owned repos as the only production app source for `get-app` style workflows.

## Core principle

Yes, the intended direction is:

* 3plug should use Triotek-owned repositories only
* Triotek should fork, wrap, and govern the stack
* upstream Frappe repos should be source inputs for Triotek engineering, not direct runtime sources for 3plug

In plain terms:

upstream Frappe provides the original base.

Triotek provides the controlled base that 3plug actually uses.

## Recommended top-level repo groups

Triotek should group repos like this:

### 1. `platform`

For platform and control-plane repos.

Recommended repos:

* `3plug-pro-control`
* `3plug-pro-ops`
* `3plug-pro-catalog`
* `triotek-bench`

### 2. `apps-core`

For Triotek-owned shared foundation apps.

Recommended repos:

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-ke`
* `triotek-payments`
* `triotek-recon`
* `triotek-forensics`

### 3. `apps-vertical`

For industry apps.

Recommended repos:

* `triotek-trading-base`
* `triotek-healthcare`

### 4. `stacks`

For stack definitions and provisioning manifests used by 3plug.

Recommended repos:

* `3plug-pro-stacks`
* `3plug-pro-environment-templates`

### 5. `docs`

For internal standards and public product/service docs.

Recommended repos:

* `triotek-platform-docs`
* `triotek-controls-docs`

## Local workspace mapping

The local workspace should expose the same groups under:

* `rnd/3plug/repos/platform`
* `rnd/3plug/repos/apps-core`
* `rnd/3plug/repos/apps-vertical`
* `rnd/3plug/repos/stacks`
* `rnd/3plug/repos/docs`

Bench and 3plug-pro should work against these checked-out working trees.

## Recommended stack source model for 3plug

3plug should provision from a controlled Triotek catalog only, not from arbitrary raw repo URLs typed by operators.

Recommended source policy:

1. Triotek-owned native repos
2. Triotek-controlled forks of official Frappe repos
3. Triotek-controlled forks of curated community repos

This should be enforced in the repo catalog.

## Example stack definition model

3plug should eventually define stacks like:

* `base-erp`
* `finance-ops-ke`
* `utility-billing-ke`
* `property-ops-ke`
* `healthcare-ops`

Each stack should specify:

* required repos
* optional repos
* supported branches or tags
* compatibility notes
* migration requirements

## Proposed initial repo creation order

1. `triotek-frappe`
2. `triotek-erpnext`
3. `triotek-bench`
4. `3plug-control`
5. `3plug-catalog`
6. `triotek-payments`
7. `triotek-recon`
8. `triotek-forensics`
9. `triotek-trading-base`
10. `triotek-ke`

## Naming rule

Use consistent public repo naming:

* `3plug-*` for platform repos
* `triotek-*` for apps and extensions

That will make the source model much cleaner for 3plug and easier for operators to understand.
