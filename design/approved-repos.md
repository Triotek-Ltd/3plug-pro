# 3plug Approved Repos

## Purpose

This is the shortlist of repositories that Triotek can actively approve as part of the initial 3plug ecosystem.

Under the current strategy, production use should come from Triotek-controlled repositories only.

So this file should be read as:

* approved upstream bases to fork or mirror
* approved optional apps to internalize under Triotek control
* approved source families

## Approval classes

### Class A: Core upstream bases to internalize

These are the upstream foundations Triotek should fork or mirror and then treat as controlled internal sources.

| Repo | Owner | Why approved |
| --- | --- | --- |
| `https://github.com/frappe/frappe` | Frappe | Main framework base. Internal target: `triotek-frappe`. |
| `https://github.com/frappe/erpnext` | Frappe | Main ERP base. Internal target: `triotek-erpnext`. |
| `https://github.com/frappe/bench` | Frappe | Required because 3plug wraps Bench operations. Internal target: `triotek-bench`. |

### Class B: Platform reference upstreams

These are approved as deployment and operational references.

| Repo | Owner | Why approved |
| --- | --- | --- |
| `https://github.com/frappe/frappe_docker` | Frappe | Useful as operational and deployment reference. |
| `https://github.com/frappe/helm` | Frappe | Useful if 3plug later grows into cluster or managed environment operations. |

### Class C: Official optional apps to internalize if adopted

These are approved for selective use depending on project needs, but should still be brought under Triotek-controlled repos before production use.

| Repo | Owner | Category |
| --- | --- | --- |
| `https://github.com/frappe/hrms` | Frappe | HR / Payroll |
| `https://github.com/frappe/crm` | Frappe | CRM |
| `https://github.com/frappe/helpdesk` | Frappe | Helpdesk |
| `https://github.com/frappe/insights` | Frappe | BI / Analytics |
| `https://github.com/frappe/lms` | Frappe | Learning / Education |
| `https://github.com/frappe/mail` | Frappe | Mail |
| `https://github.com/frappe/wiki` | Frappe | Knowledge base |
| `https://github.com/frappe/print_designer` | Frappe | Print and forms |
| `https://github.com/frappe/builder` | Frappe | Website builder |
| `https://github.com/frappe/webshop` | Frappe | Ecommerce |
| `https://github.com/frappe/lending` | Frappe | Lending / credit |
| `https://github.com/frappe/education` | Frappe | Education |

### Class D: Curated community candidates to internalize if adopted

These are approved for evaluation, not blind default dependency, and should only be used through Triotek-controlled forks.

| Repo | Owner | Category | Notes |
| --- | --- | --- | --- |
| `https://github.com/ESS-LLP/healthcare` | ESS LLP | Healthcare | High relevance, but version compatibility must be checked per stack. |
| `https://github.com/navariltd/utility-billing` | Navari | Utility / property | Strong Kenya-relevant candidate. |
| `https://github.com/navariltd/frappe-mpsa-payments` | Navari | M-Pesa / Daraja | Strong Kenya-relevant candidate. |

## Initial approved baseline for real use

This is the practical baseline Triotek should start with:

### Mandatory controlled base

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`

### Approved optional first-party apps

* `hrms`
* `crm`
* `helpdesk`
* `insights`
* `print_designer`
* `wiki`
* `lending`

### Curated evaluation candidates

* `triotek-healthcare`
* `triotek-utility-billing`
* `triotek-frappe-mpesa-payments`

## Approval policy

A repo should only move into approved status if:

* the license is acceptable
* maintenance is active enough
* compatibility is known
* the code solves a repeated Triotek problem
* we can support it if upstream slows down

## Important rule

Approved does not mean "always install."

It means "acceptable for controlled use through Triotek-controlled source."

3plug should still provision app stacks intentionally, not automatically pull every approved repo into every site.
