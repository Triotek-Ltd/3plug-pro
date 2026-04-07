# 3plug Repo Plan

## Purpose

This document lists the initial Triotek-controlled repositories that should exist if 3plug is going to operate fully from a governed source ecosystem.

Target GitHub organization:

* `Triotek-Ltd`

It covers:

* core forks
* curated optional forks
* Triotek-native apps
* vertical apps
* platform repos

## A. Core Triotek-controlled forks

These should exist first because they define the base stack.

| Planned Repo | Type | Source Base | Priority |
| --- | --- | --- | --- |
| `triotek-frappe` | Fork / mirror | Frappe | Highest |
| `triotek-erpnext` | Fork / mirror | ERPNext | Highest |
| `triotek-bench` | Fork / mirror | Bench | Highest |

## B. Core Triotek platform repos

These are native Triotek repos.

| Planned Repo | Type | Purpose | Priority |
| --- | --- | --- | --- |
| `3plug-pro-control` | Native | Main control plane | Highest |
| `3plug-pro-catalog` | Native | Repo and stack registry | Highest |
| `3plug-pro-ops` | Native | Job and automation layer | High |
| `3plug-pro-stacks` | Native | Stack manifests | High |
| `3plug-pro-environment-templates` | Native | Environment templates | Medium |

## C. Core shared Triotek apps

These are the first reusable business and platform extensions.

| Planned Repo | Type | Purpose | Priority |
| --- | --- | --- | --- |
| `triotek-ke` | Native | Kenya localization | High |
| `triotek-payments` | Native with upstream reference | Payment integration layer | Highest |
| `triotek-recon` | Native | Reconciliation engine | Highest |
| `triotek-forensics` | Native | Forensic controls layer | Highest |

## D. Vertical Triotek apps

These align with the strongest commercial opportunities.

| Planned Repo | Type | Purpose | Priority |
| --- | --- | --- | --- |
| `triotek-livestock-base` | Reference-first community base | Livestock workflows | Medium |
| `triotek-construction-base` | Reference-first community base | Construction and engineering workflows | Medium |
| `triotek-logistics-base` | Reference-first community base | Logistics and transport workflows | Medium |
| `triotek-manufacturing-base` | Reference-first community base | Advanced manufacturing workflows | Medium |
| `triotek-trading-base` | Native informed by niche trading references | Broader trading and distribution workflows | High |
| `triotek-services-base` | Reference-first community base | Professional services workflows | Later |
| `triotek-telecom-base` | Reference-first community base | Telecom workflows | Later |
| `triotek-aviation-base` | Reference-first community base | Aviation workflows | Later |
| `triotek-restaurant-base` | Reference-first community base | Restaurant and food-service workflows | Medium |
| `triotek-vehicle-trading-base` | Reference-first community base | Vehicle trading and dealership workflows | Medium |
| `triotek-public-procurement-base` | Reference-first community base | Public-sector procurement workflows | Medium |

## E. Optional shared apps to internalize

These should be internalized only if Triotek actually wants them in the governed catalog.

| Planned Repo | Upstream Source | Why it may matter |
| --- | --- | --- |
| `triotek-hrms` | HRMS | HR / payroll delivery |
| `triotek-crm` | CRM | CRM and customer operations |
| `triotek-helpdesk` | Helpdesk | Support and service desks |
| `triotek-insights` | Insights | BI and analytics |
| `triotek-mail` | Mail | Internal communications and mail services |
| `triotek-gameplan` | Gameplan | Internal collaboration and task planning |
| `triotek-wiki` | Wiki | Docs and knowledge base |
| `triotek-print-designer` | Print Designer | Forms and print workflows |
| `triotek-builder` | Builder | Site-builder workflows |

## F. Vertical base repos to internalize

These are upstream-derived repos, but they belong under `apps-vertical` because they support specific industry or solution families rather than the shared stack.

| Planned Repo | Upstream Source | Why it may matter |
| --- | --- | --- |
| `triotek-lending` | Lending | Finance, lending, SACCO, and credit operations |
| `triotek-education` | Education | Education-specific delivery |
| `triotek-lms` | LMS | Training and education |
| `triotek-webshop` | Webshop | Ecommerce and commerce workflows |
| `triotek-posawesome` | POS Awesome | Retail, mart, and modern POS workflows |
| `triotek-healthcare` | ESS LLP Healthcare | Healthcare base |
| `triotek-utility-billing` | Navari Utility Billing | Utility and property acceleration |

## G. Candidate vertical bases under review

These have public codebases, but they should not be treated like clean current upstreams until Triotek reviews maintenance status and version fit.

| Planned Repo | Upstream Source | Current stance |
| --- | --- | --- |
| `triotek-agriculture` | Frappe Agriculture | Intake started; continue under version-fit review |
| `triotek-non-profit` | Frappe Non Profit | Intake started as a reference-first base because upstream is archived |
| `triotek-hospitality-base` | Frappe Hospitality | Intake started as a reference-first base because upstream is archived |
| `triotek-property-management-base` | `aakvatech/PropMS` | Intake started as a reference-first community base |
| `triotek-logistics-base` | `hrgadeha/logistics` | Intake started as a reference-first community base |
| `triotek-construction-base` | `aidgoc/fibertrack-pro` | Intake started as a reference-first community base |
| `triotek-telecom-base` | `macrobian88/frappe_zain_subscriptions` | Intake started as a reference-first community base |
| `triotek-livestock-base` | `Janviere-dev/Livestock_Management` | Intake started as a reference-first community base |
| `triotek-services-base` | `j4ptl/FSM-field_service_management` | Intake started as a reference-first community base after replacing the weaker SeMS candidate |
| `triotek-aviation-base` | `RohanRks23/airplane_mode` | Intake started as a reference-first community base |
| `triotek-manufacturing-base` | `efeone/aumms` | Intake started as a reference-first community base with real manufacturing-specific extensions beyond ERPNext core |
| `triotek-restaurant-base` | `alialiens/erpnext_restaurant` | Intake started as a reference-first community base for restaurant workflows |
| `triotek-vehicle-trading-base` | `AddonSolutionsForERPnext/Custom_Car_Trading_App` | Intake started as a reference-first community base for vehicle-trading workflows |
| `triotek-public-procurement-base` | `buff0k/procurement` | Intake started as a reference-first community base for public-sector procurement workflows |

## H. Optional curated community support apps

These should only exist if Triotek decides to support them under its own control.

| Planned Repo | Upstream Source | Why it may matter |
| --- | --- | --- |
| `triotek-frappe-mpesa-payments` | Navari M-Pesa app | Kenya payment acceleration |

## I. Suggested initial creation order

### Phase 1: base and control plane

1. `triotek-frappe`
2. `triotek-erpnext`
3. `triotek-bench`
4. `3plug-pro-control`
5. `3plug-pro-catalog`
6. `3plug-pro-stacks`

### Phase 2: controls and payments

7. `triotek-payments`
8. `triotek-recon`
9. `triotek-forensics`
10. `triotek-ke`

### Phase 3: first commercial verticals

11. `triotek-trading-base`

### Phase 4: optional shared ecosystem apps

13. `triotek-hrms`
14. `triotek-crm`
15. `triotek-helpdesk`
16. `triotek-insights`
17. `triotek-wiki`
18. `triotek-print-designer`
19. `triotek-frappe-mpesa-payments`

### Phase 5: vertical base repos

20. `triotek-lending`
21. `triotek-posawesome`
22. `triotek-utility-billing`
23. `triotek-healthcare`
24. `triotek-webshop`
25. `triotek-lms`
26. `triotek-education`

### Phase 6: candidate public vertical bases under review

27. `triotek-agriculture`
28. `triotek-non-profit`
29. `triotek-hospitality-base`

### Phase 7: broader native vertical suite if desired

30. `triotek-mail`
31. `triotek-gameplan`
32. `triotek-builder`
33. `triotek-livestock-base`
34. `triotek-construction-base`
35. `triotek-logistics-base`
36. `triotek-services-base`
37. `triotek-telecom-base`
38. `triotek-aviation-base`
39. `triotek-manufacturing-base`
46. `triotek-restaurant-base`
47. `triotek-vehicle-trading-base`
48. `triotek-public-procurement-base`

## J. Operational rule

Just because Triotek can internalize all these apps does not mean all of them should be installed everywhere.

The repo base can be broad while the actual deployed stack stays narrow and deliberate.

## K. Practical recommendation

Yes, create the repo plan first, then create the real repos from that plan.

That sequence is safer because:

* naming stays consistent
* ownership stays clear
* 3plug catalog rules can be defined cleanly
* the team avoids random repo sprawl
