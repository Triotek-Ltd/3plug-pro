# 3plug App Catalog

## Purpose

This document is the full starting app catalog for the Triotek-controlled 3plug ecosystem.

It answers one question:

What apps do we want in scope from the beginning so we build the repo strategy correctly?

This is broader than the first deployment stack.

It includes:

* core framework and ERP base
* official ecosystem apps we may internalize
* strategically important community apps we may internalize
* Triotek-native apps we know we need

## Important rule

This is the app universe, not the default install list.

Not every app here should be installed on every site.

Instead:

* this defines what belongs in the governed source ecosystem
* 3plug will later decide what stack uses which apps

## Status labels

* `Base` = mandatory foundation
* `Internalize` = worth bringing into Triotek-controlled source
* `Build` = Triotek-native app we should create
* `Evaluate` = useful to keep in scope, but not default for every deployment

## A. Foundation and platform base

| App | Internal Repo | Source | Status | Notes |
| --- | --- | --- | --- | --- |
| Frappe Framework | `triotek-frappe` | Frappe upstream | Base | Main framework base. |
| ERPNext | `triotek-erpnext` | ERPNext upstream | Base | Main ERP base. |
| Bench | `triotek-bench` | Bench upstream | Base | Required for 3plug orchestration. |
| 3plug-pro Control | `3plug-pro-control` | Triotek native | Build | Main control plane. |
| 3plug-pro Catalog | `3plug-pro-catalog` | Triotek native | Build | Repo and stack registry. |
| 3plug-pro Ops | `3plug-pro-ops` | Triotek native | Build | Jobs and automation layer. |
| 3plug-pro Stacks | `3plug-pro-stacks` | Triotek native | Build | Stack manifests and compatibility sets. |
| 3plug-pro Environment Templates | `3plug-pro-environment-templates` | Triotek native | Build | Environment policy templates. |

## B. Official general-purpose apps to internalize

These are useful enough that Triotek should decide early whether to internalize them into the governed ecosystem.

| App | Internal Repo | Source | Status | Notes |
| --- | --- | --- | --- | --- |
| HRMS | `triotek-hrms` | `frappe/hrms` | Internalize | Strong official HR/payroll app. |
| CRM | `triotek-crm` | `frappe/crm` | Internalize | Useful for sales and lead workflows. |
| Helpdesk | `triotek-helpdesk` | `frappe/helpdesk` | Internalize | Useful for support and ticketing. |
| Insights | `triotek-insights` | `frappe/insights` | Internalize | Useful for analytics and BI. |
| Wiki | `triotek-wiki` | `frappe/wiki` | Internalize | Useful for internal and client docs. |
| Print Designer | `triotek-print-designer` | `frappe/print_designer` | Internalize | Useful for forms and print-heavy operations. |
| Builder | `triotek-builder` | `frappe/builder` | Evaluate | Useful if visual page building matters. |
| Mail | `triotek-mail` | `frappe/mail` | Evaluate | Useful for self-contained communication stack, but operationally heavier. |
| Gameplan | `triotek-gameplan` | `frappe/gameplan` | Evaluate | Useful if Triotek wants internal collaboration under the same governed source. |

## C. General business apps to internalize

| App | Internal Repo | Source | Status | Notes |
| --- | --- | --- | --- | --- |
| Lending Integration Base | `triotek-lending` | `frappe/lending` | Internalize | Kept as a vertical base for finance and credit solutions. |
| Education Base | `triotek-education` | `frappe/education` | Evaluate | Better treated as a vertical base than shared core. |
| LMS Base | `triotek-lms` | `frappe/lms` | Evaluate | Better treated as a vertical base than shared core. |
| Webshop Base | `triotek-webshop` | `frappe/webshop` | Evaluate | Better treated as a commerce vertical base than shared core. |

## D. Vertical base apps to internalize under Triotek control

These are not installed everywhere. They are vertical accelerators that live under `apps-vertical` locally even when their code comes from Frappe or the community.

| App | Internal Repo | Public Source | Status | Notes |
| --- | --- | --- | --- | --- |
| Lending | `triotek-lending` | `frappe/lending` | Internalize | Finance and SACCO base for `triotek-finserv`. |
| Education | `triotek-education` | `frappe/education` | Evaluate | School and institutional base. |
| LMS | `triotek-lms` | `frappe/lms` | Evaluate | Training and learning base. |
| Webshop | `triotek-webshop` | `frappe/webshop` | Evaluate | Commerce base. |
| POS Awesome | `triotek-posawesome` | `ucraft-com/POS-Awesome` or maintained version-specific fork | Internalize | Retail and mart base. |
| Healthcare | `triotek-healthcare` | `ESS-LLP/healthcare` | Internalize | Use as the single healthcare base for now. |
| Utility Billing | `triotek-utility-billing` | `navariltd/utility-billing` | Internalize | Utility and real-estate support base. |
| Frappe M-Pesa Payments | `triotek-frappe-mpesa-payments` | `navariltd/frappe-mpsa-payments` | Internalize | Relevant for Kenya payments, but Triotek should still own payment abstraction. |

## E. Triotek-native core apps

These are the most important apps Triotek should build itself.

| App | Internal Repo | Status | Notes |
| --- | --- | --- | --- |
| Kenya Localization | `triotek-ke` | Build | Kenya-specific defaults and local patterns. No public official Kenya-specific app was found in the Frappe org. |
| Payments Layer | `triotek-payments` | Build | Stable payment abstraction and callback handling. Related official upstream exists in `frappe/payments`, but Triotek should still own the Kenya-first abstraction layer. |
| Reconciliation Engine | `triotek-recon` | Build | Matching, discrepancy detection, and settlement review. No public official standalone reconciliation app was found in the Frappe org. |
| Forensic Controls | `triotek-forensics` | Build | Audit events, evidence preservation, and export. No public official standalone forensic-controls app was found in the Frappe org. |

## F. Triotek-native vertical apps

These reflect the strongest business opportunities.

| App | Internal Repo | Status | Notes |
| --- | --- | --- | --- |
| Trading Base | `triotek-trading-base` | Build | Broader trading and distribution workflows that sit above narrower dealership or niche trading bases. |

## G. Candidate public vertical bases under review

These are not yet part of the standard governed stack, but the public ecosystem is strong enough that Triotek should track them deliberately.

| App | Proposed Internal Repo | Source | Status | Notes |
| --- | --- | --- | --- | --- |
| Agriculture Base | `triotek-agriculture` | `frappe/agriculture` | Internalize carefully | Intake has started; keep reviewing version fit and maintenance. |
| Non Profit Base | `triotek-non-profit` | `frappe/non_profit` | Internalize carefully | Intake has started; the repo is archived and should remain reference-first. |
| Hospitality Base | `triotek-hospitality-base` | `frappe/hospitality` | Internalize carefully | Intake has started; the repo is archived and should remain reference-first. |
| Property Management Base | `triotek-property-management-base` | `aakvatech/PropMS` | Internalize carefully | Intake has started; keep it reference-first and separate from the main Triotek real-estate repo. |
| Logistics Base | `triotek-logistics-base` | `hrgadeha/logistics` | Internalize carefully | Intake has started; keep it reference-first and separate from any later Triotek logistics product layer. |
| Construction Base | `triotek-construction-base` | `aidgoc/fibertrack-pro` | Internalize carefully | Intake has started; keep it reference-first because the upstream is niche and implementation-specific. |
| Telecom Base | `triotek-telecom-base` | `macrobian88/frappe_zain_subscriptions` | Internalize carefully | Intake has started; keep it reference-first and treat it as a telecom-adjacent base rather than the final product. |
| Livestock Base | `triotek-livestock-base` | `Janviere-dev/Livestock_Management` | Internalize carefully | Intake has started; keep it reference-first and treat it as an agriculture-adjacent base rather than the final product. |
| Services Base | `triotek-services-base` | `j4ptl/FSM-field_service_management` | Internalize carefully | Intake has started; we replaced `efeone/sems` because it was too thin, and chose the field-service app because it has real service, technician, visit-log, and SLA doctypes. |
| Aviation Base | `triotek-aviation-base` | `RohanRks23/airplane_mode` | Internalize carefully | Intake has started; keep it reference-first because the community apps currently look niche or implementation-specific rather than like a mature shared base. |
| Manufacturing Base | `triotek-manufacturing-base` | `efeone/aumms` | Internalize carefully | Intake has started; this is meaningfully different from ERPNext manufacturing because it adds jewellery and process-specific doctypes, metal ledger flows, stage templates, design requests, and domain settings. |
| Restaurant Base | `triotek-restaurant-base` | `alialiens/erpnext_restaurant` | Internalize carefully | Intake has started; use it as the food-service head start rather than leaving restaurant workflows only as a generic food placeholder. |
| Vehicle Trading Base | `triotek-vehicle-trading-base` | `AddonSolutionsForERPnext/Custom_Car_Trading_App` | Internalize carefully | Intake has started, but it is narrower than general trading/distribution. Keep it reference-first and use it specifically for vehicle-dealership workflows. |
| Public Procurement Base | `triotek-public-procurement-base` | `buff0k/procurement` | Internalize carefully | Intake has started; use it as the public-sector procurement head start for current government procurement workflows. |

## H. Full in-scope app universe

This is the combined list of apps in scope for the governed Triotek source ecosystem:

### Platform and base

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`
* `3plug-pro-control`
* `3plug-pro-catalog`
* `3plug-pro-ops`
* `3plug-pro-stacks`
* `3plug-pro-environment-templates`

### General official apps

* `triotek-hrms`
* `triotek-crm`
* `triotek-helpdesk`
* `triotek-insights`
* `triotek-wiki`
* `triotek-print-designer`
* `triotek-builder`
* `triotek-mail`
* `triotek-gameplan`

### Vertical base apps

* `triotek-lending`
* `triotek-education`
* `triotek-lms`
* `triotek-webshop`

### Internalized community apps

* `triotek-posawesome`
* `triotek-healthcare`
* `triotek-utility-billing`
* `triotek-frappe-mpesa-payments`

### Triotek-native apps

* `triotek-ke`
* `triotek-payments`
* `triotek-recon`
* `triotek-forensics`
* `triotek-trading-base`

## I. Recommended first-wave app set

This is the first set Triotek should focus on structurally.

### Required now

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`
* `3plug-pro-control`
* `3plug-pro-catalog`
* `3plug-pro-stacks`
* `triotek-payments`
* `triotek-recon`
* `triotek-forensics`
* `triotek-ke`
* `triotek-trading-base`

### Strong next wave

* `triotek-posawesome`
* `triotek-frappe-mpesa-payments`
* `triotek-utility-billing`
* `triotek-hrms`
* `triotek-crm`
* `triotek-helpdesk`
* `triotek-insights`
* `triotek-lending`
* `triotek-print-designer`
* `triotek-wiki`

### Useful later

* `triotek-mail`
* `triotek-gameplan`
* `triotek-builder`
* `triotek-webshop`
* `triotek-education`
* `triotek-lms`
* `triotek-healthcare`

## J. Strategic note on communication apps

If Triotek wants customers to have fewer external communication dependencies, then:

* `triotek-mail`
* `triotek-helpdesk`
* `triotek-crm`
* `triotek-gameplan`
* `triotek-wiki`

become strategically important, even if they are not all first-wave repos.

That does not mean they all belong in the first technical rollout.

It means they belong in the governed app universe.

## K. Rule before repo creation

Before creating real repos, Triotek should confirm for each app:

* do we want it in the governed source universe?
* do we want it in the first deployment wave?
* is it a direct fork, a mirror, or a native repo?
* what branch model will it follow?

Once that is confirmed, the real repo creation can begin cleanly.

## Verified public source references used for this catalog

* `https://github.com/frappe/frappe`
* `https://github.com/frappe/erpnext`
* `https://github.com/frappe/payments`
* `https://github.com/frappe/bench`
* `https://github.com/frappe/hrms`
* `https://github.com/frappe/crm`
* `https://github.com/frappe/helpdesk`
* `https://github.com/frappe/insights`
* `https://github.com/frappe/lms`
* `https://github.com/frappe/mail`
* `https://github.com/frappe/gameplan`
* `https://github.com/frappe/wiki`
* `https://github.com/frappe/print_designer`
* `https://github.com/frappe/builder`
* `https://github.com/frappe/webshop`
* `https://github.com/frappe/lending`
* `https://github.com/frappe/education`
* `https://github.com/frappe/erpnext_usa`
* `https://github.com/ESS-LLP/healthcare`
* `https://github.com/ucraft-com/POS-Awesome`
* `https://github.com/defendicon/POS-Awesome-V15`
* `https://github.com/navariltd/utility-billing`
* `https://github.com/navariltd/frappe-mpsa-payments`
