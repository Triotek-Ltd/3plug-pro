# 3plug Community Best-Effort Pass

## Purpose

This note records the current best-effort public search outcome for the vertical repo universe.

It exists to answer one recurring question:

Are we missing obvious public/community Frappe apps for the remaining verticals?

## Bottom line

We have already captured most of the strong public bases that are clearly worth internalizing.

The strongest current bases are:

* `triotek-lending`
* `triotek-education`
* `triotek-lms`
* `triotek-webshop`
* `triotek-posawesome`
* `triotek-healthcare`
* `triotek-utility-billing`
* `triotek-agriculture`

We also have reference-first bases:

* `triotek-hospitality-base`
* `triotek-property-management-base`

And one archived reference-first base already internalized:

* `triotek-non-profit`

We also found meaningful community or niche references for:

* `triotek-logistics-base`
* `triotek-construction-base`
* `triotek-livestock-base`
* `triotek-services-base`
* `triotek-telecom-base`
* `triotek-manufacturing-base`
* `triotek-restaurant-base`
* `triotek-vehicle-trading-base`
* `triotek-aviation-base`
* `triotek-public-procurement-base`

For the rest, the public record still points more toward:

* ERPNext built-in modules
* partner/customer custom work
* marketplace/community fragments

not toward a clean maintained standalone app we should immediately internalize.

## What this means

We should not keep renaming or re-splitting the vertical universe based on hope that every category has a mature public app.

The current practical split is sound:

### Strong reusable base exists

* finance / lending
* education
* LMS
* commerce
* retail POS
* healthcare
* utility billing
* agriculture

### Reference-first only

* NGO / non-profit
* hospitality
* property management

### Still native-first overall from this pass

* public sector

But for public sector, we did find narrower procurement and tender references rather than a broad general-purpose public-service base.

## Duplicate rule

We now keep one repo per role:

* upstream-derived bases keep source-aligned names
* Triotek-owned product repos use `-ops`

Examples:

* `triotek-utility-billing` is the base
* `triotek-healthcare` is the healthcare base and current product repo
* there is no duplicate `triotek-health`

* `triotek-trading-base` is the broader trading and distribution layer
* `triotek-vehicle-trading-base` is only the narrower dealership-specific reference base

## Current best next moves

1. Keep the current strong base list stable.
2. Do not create more duplicate vertical names.
3. Treat `triotek-hospitality-base` and `triotek-property-management-base` as reference-first bases, not clean current upstreams.
4. Treat `triotek-non-profit` as the single NGO/non-profit base unless a real separate NGO ops layer becomes necessary later.
5. Keep using stronger candidates when they appear. For example, `triotek-services-base` should track the field-service app rather than the thinner SeMS shell.
6. Treat `triotek-manufacturing-base`, `triotek-restaurant-base`, and `triotek-vehicle-trading-base` as the public head starts for those narrower verticals rather than leaving duplicate placeholder ops repos in front of them.
7. Treat `triotek-public-procurement-base` as the strongest public-sector procurement head start we found for current public-sector intake work.
8. Move engineering energy toward actual business work in the retained bases, especially `triotek-trading-base`.

## Sources checked

* https://github.com/frappe
* https://github.com/erpnext-apps
* https://github.com/frappe/agriculture
* https://github.com/frappe/non_profit
* https://github.com/frappe/hospitality
* https://github.com/frappe/lending
* https://github.com/frappe/education
* https://github.com/frappe/lms
* https://github.com/frappe/webshop
* https://github.com/ESS-LLP/healthcare
* https://github.com/ucraft-com/POS-Awesome
* https://github.com/navariltd/utility-billing
* https://cloud.frappe.io/marketplace/apps/property_management
* https://discuss.frappe.io/t/property-management/21151
* https://github.com/aakvatech/PropMS
