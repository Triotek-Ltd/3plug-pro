# 3plug Repo Base

## Purpose

This document is the verified starting base for repositories and code that Triotek can use while building `3plug`, our Bench control plane and Frappe-based delivery stack.

The goal is not to list every repo in the ecosystem.

The goal is to define:

* what we should depend on directly
* what we should treat as optional official apps
* what community repos are credible enough to watch or evaluate
* where we should expect to build our own apps instead of depending on public code

This is a practical baseline, not a vanity catalog.

## How to read this

Each repo is marked as one of:

* `Core` = direct foundation for 3plug and our main stack
* `Official Optional` = official Frappe app that we may use depending on solution type
* `Curated Community` = public community repo worth reviewing, but not a default dependency
* `Reference Only` = useful to learn from, but not something we should assume as a production dependency
* `Custom Required` = area where Triotek should expect to build and own the solution

## A. Core platform repos

These are the repos we should treat as the real base of our platform.

| Repo | Owner | Use | Status | Notes |
| --- | --- | --- | --- | --- |
| `https://github.com/frappe/frappe` | Frappe | Framework | Core | Main application framework. |
| `https://github.com/frappe/erpnext` | Frappe | ERP core | Core | Main business system foundation. |
| `https://github.com/frappe/bench` | Frappe | Bench CLI | Core | Critical for 3plug since 3plug is wrapping Bench behavior. |
| `https://github.com/frappe/frappe_docker` | Frappe | Docker orchestration reference | Core | Useful even if 3plug replaces parts of Docker-driven operations. |
| `https://github.com/frappe/helm` | Frappe | Kubernetes/Helm reference | Reference Only | Useful as deployment reference, especially if 3plug later supports K8s or managed clusters. |

## B. Official Frappe apps we should treat as first-party options

These are credible official repos in the public Frappe ecosystem and can be part of our solution library.

| Repo | App | Category | Status | Notes |
| --- | --- | --- | --- | --- |
| `https://github.com/frappe/hrms` | HRMS | HR / Payroll | Official Optional | Strong official app, mature and active. |
| `https://github.com/frappe/crm` | CRM | Sales / CRM | Official Optional | Good official app for standalone or integrated CRM use. |
| `https://github.com/frappe/helpdesk` | Helpdesk | Customer support | Official Optional | Useful for client support desks and internal support workflows. |
| `https://github.com/frappe/insights` | Insights | BI / Analytics | Official Optional | Useful for dashboards and reporting layers. |
| `https://github.com/frappe/lms` | LMS | Education | Official Optional | Relevant for training and education solutions. |
| `https://github.com/frappe/mail` | Mail | Email platform | Official Optional | Strong but heavier operational dependency because of mail infrastructure. |
| `https://github.com/frappe/gameplan` | Gameplan | Collaboration | Reference Only | Interesting, but not part of our main ERP platform base. |
| `https://github.com/frappe/wiki` | Wiki | Documentation | Official Optional | Useful for docs, KB, and internal portals. |
| `https://github.com/frappe/print_designer` | Print Designer | Print / document design | Official Optional | Very useful in client delivery. |
| `https://github.com/frappe/builder` | Builder | Website builder | Official Optional | Useful where visual site-building matters. |
| `https://github.com/frappe/webshop` | Webshop | Ecommerce | Official Optional | Useful for ecommerce extensions around ERPNext. |

## C. Industry apps with official or near-official standing

These are industry-specific apps worth including in the baseline, but with some nuance.

| Repo | App | Category | Status | Notes |
| --- | --- | --- | --- | --- |
| `https://github.com/frappe/lending` | Lending | Finance / lending | Official Optional | Strong official option for loan workflows. Relevant for MFI and lending operations. |
| `https://github.com/frappe/education` | Education | School management | Official Optional | Still a valid official education app. |
| `https://github.com/ESS-LLP/healthcare` | Healthcare | Healthcare / HIS | Official Optional | Public repo exists and maps to Frappe Healthcare docs, but it is not currently under the `frappe` GitHub org. Treat as important but verify branch compatibility before use. |

## D. Regional and localization repos

Your earlier list used `erpnext_regional`, but that is not the best current baseline.

What appears more real today is country-specific repos.

| Repo | Region | Status | Notes |
| --- | --- | --- | --- |
| `https://github.com/frappe/erpnext_usa` | USA | Official Optional | Official regional app. |
| `https://github.com/frappe/erpnext_france` | France | Official Optional | Official regional app. |

### Important correction

Do not assume there is one canonical public `erpnext_regional` repo that solves regionalization broadly.

For Kenya and East Africa, Triotek should expect:

* some localization from ERPNext core
* some payment support in ERPNext and community apps
* some tax and compliance work to be custom
* country-specific vertical modules to be mostly custom or private

That means Kenya localization should be treated as `Custom Required`.

## E. Payments and mobile money

This is critical for Triotek.

| Repo / Source | Use | Status | Notes |
| --- | --- | --- | --- |
| `https://docs.frappe.io/erpnext/user/manual/en/mpesa-integration` | ERPNext M-Pesa integration docs | Official Optional | ERPNext already has documented M-Pesa integration support, especially around POS/payment gateway usage. |
| `https://github.com/navariltd/frappe-mpsa-payments` | Extended Daraja integration | Curated Community | Strong Kenya-relevant repo for STK Push, C2B, B2C, and transaction status flows. Worth evaluating seriously. |

### Recommendation

For Kenya-facing work, Triotek should not rely on one payment repo blindly.

We should maintain our own payment integration strategy:

* use official ERPNext capability where it fits
* evaluate community M-Pesa apps carefully
* build and own the forensic/reconciliation layer ourselves

For high-control client projects, payment and reconciliation should be treated as `Custom Required`.

## F. Utility billing and property operations

This is one of Triotek's highest-priority verticals.

| Repo | Use | Status | Notes |
| --- | --- | --- | --- |
| `https://github.com/navariltd/utility-billing` | Utility billing + property management | Curated Community | One of the most relevant public repos in this category. Strong candidate for evaluation. |
| `https://github.com/frappe/erpnext` | ERPNext property/accounting modules | Reference Only | Some property-related capability exists inside ERPNext, but not enough to treat as a complete vertical solution. |

### Recommendation

Utility billing and property operations should be treated as:

* `Curated Community` for initial review
* `Custom Required` for serious Triotek productization

This is a prime area for Triotek-owned apps.

## G. Logistics and transport

| Repo | Use | Status | Notes |
| --- | --- | --- | --- |
| `https://github.com/alyf-de/erpnext_logistics` | Logistics extension | Reference Only | Mentioned in ecosystem lists, but should be evaluated carefully before any production use. |
| `https://github.com/frappe/erpnext` | Fleet / transport modules | Official Optional | ERPNext already has some built-in transport/fleet capability. |

### Recommendation

Treat logistics as `Custom Required` unless a specific public repo is actively validated by our team.

## H. Agriculture

| Repo | Use | Status | Notes |
| --- | --- | --- | --- |
| `https://github.com/baun/firefly-farm` | Farm management example | Reference Only | Useful as ecosystem signal, not a default dependency. |

### Recommendation

Agriculture should be treated as `Custom Required`.

Triotek should expect to build around:

* ERPNext core
* custom value-chain modules
* custom collection, payout, and traceability logic

## I. Manufacturing

| Repo | Use | Status | Notes |
| --- | --- | --- | --- |
| `https://github.com/frappe/erpnext` | Manufacturing | Core | Manufacturing is already a strong built-in ERPNext area. |

### Recommendation

Start with ERPNext built-ins first.

Only add community manufacturing forks after strict evaluation.

## J. Hospitality

There is no strong official hospitality repo in the same class as ERPNext, HRMS, CRM, or Lending.

### Recommendation

Hospitality should be treated as:

* ERPNext core where useful
* `Custom Required` for serious hotel or hospitality operations

## K. NGO / nonprofit

There is no single strong official NGO app repo that should be treated as our default dependency.

ERPNext already covers some relevant functions such as:

* finance
* procurement
* grants/donations style workflows
* approvals
* reporting

### Recommendation

NGO and donor operations should be treated as `Custom Required` on top of ERPNext core.

## L. Frontend and developer ecosystem repos

These repos matter more for 3plug and custom app development than for client ERP features directly.

| Repo | Use | Status | Notes |
| --- | --- | --- | --- |
| `https://github.com/frappe/frappe-ui` | UI toolkit | Official Optional | Useful when building modern interfaces around Frappe apps or 3plug-style dashboards. |

## M. What Triotek should own directly

These are areas where public repos are helpful, but Triotek should still plan to own the final implementation.

Treat these as `Custom Required`:

* Kenya localization
* forensic logging and audit layer
* reconciliation layer
* utility billing productization
* property operations productization
* SACCO workflows
* MFI-specific controls
* NGO compliance packs
* agribusiness value-chain modules
* 3plug itself

## N. Initial default stack for Triotek

If we want a realistic default build base, this should be our first stack:

### Platform base

* `frappe`
* `erpnext`
* `bench`

### Operational references

* `frappe_docker`
* `helm`

### Optional first-party apps

* `hrms`
* `crm`
* `helpdesk`
* `insights`
* `print_designer`
* `wiki`

### Vertical candidates for serious review

* `lending`
* `education`
* `healthcare`
* `navariltd/utility-billing`
* `navariltd/frappe-mpsa-payments`

### Triotek-owned app layer

* Kenya localization app
* forensic controls app
* reconciliation app
* utility/property vertical app
* 3plug control-plane app/services

## O. Decision rule for adding new repos

Before adding any repo to the approved Triotek base, we should check:

* Is it public and active?
* Is the owner credible?
* Is the license acceptable for our use?
* Is branch compatibility clear?
* Is the code quality reasonable?
* Does it solve a real repeated problem?
* Can we maintain it if the upstream stops moving?

If the answer is weak on most of these, the repo should stay in `Reference Only`.

## P. Recommended repo classes for 3plug

3plug should maintain an internal catalog with these classes:

* `core`
* `official_optional`
* `curated_community`
* `reference_only`
* `triotek_owned`

This will make repo governance and environment provisioning much cleaner later.

## Q. Bottom line

The real starting base is not huge.

Triotek does not need dozens of repos to start.

It needs:

* a small trusted core
* a few carefully selected official apps
* a short watchlist of community repos
* a clear commitment to building the Kenya-critical pieces ourselves

That is the practical repo base for 3plug and for Triotek's ERP product direction.

## Verified source links

Official and primary sources used for this baseline:

* `https://github.com/frappe`
* `https://github.com/frappe/frappe`
* `https://github.com/frappe/erpnext`
* `https://github.com/frappe/bench`
* `https://github.com/frappe/frappe_docker`
* `https://github.com/frappe/helm`
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
* `https://github.com/ESS-LLP/healthcare`
* `https://github.com/frappe/erpnext_usa`
* `https://github.com/frappe/erpnext_france`
* `https://docs.frappe.io/erpnext/user/manual/en/mpesa-integration`
* `https://github.com/navariltd/frappe-mpsa-payments`
* `https://github.com/navariltd/utility-billing`
