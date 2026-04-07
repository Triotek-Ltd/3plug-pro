# 3plug Reuse Policy

## Purpose

This policy tells the team when to:

* internalize an existing public Frappe app
* extend an internalized base
* use a public app as reference only
* build natively from scratch

The goal is simple:

Do not redo work that already gives Triotek a legitimate head start, but do not let weak or abandoned codebases become the product by default.

## Core rule

For every solution area, decide first whether the public ecosystem gives us:

* a strong maintained base
* a weak or archived base
* no meaningful base

Then act accordingly.

## 1. Internalize when a strong base exists

If a public app is real, maintained enough, and close to the workflow we want, Triotek should internalize it into the governed source ecosystem instead of rebuilding it.

Examples:

* `triotek-lending`
* `triotek-education`
* `triotek-lms`
* `triotek-webshop`
* `triotek-posawesome`
* `triotek-healthcare`
* `triotek-utility-billing`

Rule:

* do not rebuild these from zero
* intake them into Triotek-controlled repos
* keep only the clean branch model we support
* adapt them through Triotek-owned extension layers

## 2. Build native ops layers on top of reused bases

If Triotek is selling a business solution rather than just redistributing a base app, the product repo should be our own ops layer.

Examples:

* a future Triotek product layer on top of `triotek-utility-billing`
* a future Triotek product layer on top of `triotek-lending`
* a future Triotek product layer on top of `triotek-webshop`

Rule:

* base repo stays close to upstream-derived structure
* Triotek-specific workflows, controls, and product behavior belong in the ops repo

## 3. Reference first when the base is weak or archived

Some public repos are useful as reference material or starting points, but they should not be treated like healthy upstream dependencies.

Examples:

* `triotek-non-profit`
* `triotek-hospitality-base`
* `triotek-property-management-base`

Rule:

* review the code before intake
* do not assume long-term maintainability
* prefer native Triotek product layers even if some structures are borrowed

## 4. Build natively when no solid base exists

If there is no strong public app, build the solution natively on top of:

* `triotek-frappe`
* `triotek-erpnext`
* shared Triotek apps
* any carefully reused patterns from related bases

Examples:

* `triotek-livestock-base`
* `triotek-construction-base`
* `triotek-logistics-base`
* `triotek-manufacturing-base`
* `triotek-services-base`
* `triotek-telecom-base`
* `triotek-aviation-base`
* `triotek-vehicle-trading-base`

## 5. Never confuse base repos with product repos

This is a hard naming and architecture rule.

* upstream-derived bases keep source-aligned names
* Triotek-native solution repos use `-ops`

Examples:

* `triotek-healthcare` is a base
* there is no second `triotek-health` repo unless we later prove we truly need a split

* `triotek-hospitality-base` is a base
* there is no second `triotek-hospitality-ops` repo unless we later prove we truly need a split

## 6. Team obligations

When adopting a public base, the team must:

* document why it is being reused
* document what Triotek will own on top
* confirm the license is acceptable
* confirm the major-version fit
* decide whether the repo is intake-now or reference-only

When building natively, the team must:

* confirm there is no stronger base worth reusing
* document the decision in the repo plan or intake decision note

## 7. Default decision order

For every new vertical:

1. Search for a real public Frappe base.
2. If strong, intake it.
3. If weak or archived, mark it reference-first.
4. Build the Triotek ops layer separately.
5. If no real base exists, build natively.
