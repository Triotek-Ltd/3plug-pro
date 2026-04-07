# 3plug-pro Naming Standard

## Decision

The project-facing and organization-facing name is:

* `3plug-pro`

## Local planning folder

The local planning folder may remain:

* `rnd/3plug`

for continuity during planning, but the intended published repo names and platform names should use `3plug-pro`.

## Platform repo naming

Use:

* `3plug-pro`
* `3plug-pro-control`
* `3plug-pro-catalog`
* `3plug-pro-ops`
* `3plug-pro-stacks`
* `3plug-pro-environment-templates`

## Vertical repo naming

Use this split consistently:

* upstream-derived vertical bases keep source-aligned names
* Triotek-native vertical solution repos use the suffix `-ops`

Examples:

* base repos:
  * `triotek-healthcare`
  * `triotek-lending`
  * `triotek-webshop`
  * `triotek-utility-billing`
* native solution repos:
  * `triotek-trading-base`

This rule exists to prevent confusion between:

* a reusable upstream-derived base app
* and a Triotek-owned business solution built on top of that base

## Split discipline

Do not create both a base repo and an `-ops` repo unless the split is already real.

Example:

* keep `triotek-agriculture` alone until there is a proven need for a separate agribusiness product layer
* do not keep a placeholder `triotek-agri-ops` just because it might be useful later

## Internal reference rule

When docs refer to the published platform or repo names, prefer `3plug-pro`.

When docs refer to the existing local planning directory, `rnd/3plug` is acceptable until the planning material is moved.
