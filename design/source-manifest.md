# 3plug Source Manifest

## Purpose

This manifest is the concrete source intake list for the 3plug ecosystem.

Target GitHub organization:

* `Triotek-Ltd`

It answers:

* which upstream sources exist
* what the Triotek-controlled repo should be called
* whether the code should be forked, mirrored, or built natively

## Important source-control rule

For upstream-derived repos, Triotek should **not** strip `.git` history and start from a blank repo.

The correct approach is:

* preserve upstream history through a fork or mirror
* create Triotek-controlled release branches
* restrict 3plug to Triotek-approved tags and branches

For Triotek-native apps, fresh repos are correct.

## A. Core upstream-derived repos

| Upstream Source | Triotek Repo | Intake Type |
| --- | --- | --- |
| `https://github.com/frappe/frappe` | `triotek-frappe` | Fork or mirror |
| `https://github.com/frappe/erpnext` | `triotek-erpnext` | Fork or mirror |
| `https://github.com/frappe/bench` | `triotek-bench` | Fork or mirror |

## B. Official optional apps to internalize

| Upstream Source | Triotek Repo | Intake Type |
| --- | --- | --- |
| `https://github.com/frappe/hrms` | `triotek-hrms` | Fork or mirror |
| `https://github.com/frappe/crm` | `triotek-crm` | Fork or mirror |
| `https://github.com/frappe/helpdesk` | `triotek-helpdesk` | Fork or mirror |
| `https://github.com/frappe/insights` | `triotek-insights` | Fork or mirror |
| `https://github.com/frappe/wiki` | `triotek-wiki` | Fork or mirror |
| `https://github.com/frappe/print_designer` | `triotek-print-designer` | Fork or mirror |
| `https://github.com/frappe/builder` | `triotek-builder` | Fork or mirror |
| `https://github.com/frappe/mail` | `triotek-mail` | Fork or mirror |
| `https://github.com/frappe/gameplan` | `triotek-gameplan` | Fork or mirror |
| `https://github.com/frappe/lending` | `triotek-lending` | Fork or mirror |
| `https://github.com/frappe/education` | `triotek-education` | Fork or mirror |
| `https://github.com/frappe/lms` | `triotek-lms` | Fork or mirror |
| `https://github.com/frappe/webshop` | `triotek-webshop` | Fork or mirror |

## C. Community apps to internalize if adopted

| Upstream Source | Triotek Repo | Intake Type |
| --- | --- | --- |
| `https://github.com/ucraft-com/POS-Awesome` | `triotek-posawesome` | Fork or mirror |
| `https://github.com/ESS-LLP/healthcare` | `triotek-healthcare` | Fork or mirror |
| `https://github.com/navariltd/utility-billing` | `triotek-utility-billing` | Fork or mirror |
| `https://github.com/navariltd/frappe-mpsa-payments` | `triotek-frappe-mpesa-payments` | Fork or mirror |

## D. Triotek-native repos

These should be created as fresh Triotek repos.

### Platform

* `3plug-pro-control`
* `3plug-pro-catalog`
* `3plug-pro-ops`
* `3plug-pro-stacks`
* `3plug-pro-environment-templates`

### Shared apps

* `triotek-ke`
* `triotek-payments`
* `triotek-recon`
* `triotek-forensics`

### Vertical apps

* `triotek-healthcare`
* `triotek-livestock-base`
* `triotek-construction-base`
* `triotek-logistics-base`
* `triotek-manufacturing-base`
* `triotek-trading-base`
* `triotek-services-base`
* `triotek-hospitality-base`
* `triotek-telecom-base`
* `triotek-aviation-base`
* `triotek-restaurant-base`
* `triotek-vehicle-trading-base`
* `triotek-public-procurement-base`

## Recommended local source layout

The active local working area should be:

* `rnd/3plug/repos/platform/`
* `rnd/3plug/repos/apps-core/`
* `rnd/3plug/repos/apps-vertical/`
* `rnd/3plug/repos/stacks/`
* `rnd/3plug/repos/docs/`

That keeps the workspace aligned with what Bench and 3plug-pro should actually use day to day.
