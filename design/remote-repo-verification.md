# 3plug-pro Remote Repo Verification

## Purpose

This file records the current remote presence check for Triotek-controlled repositories that 3plug-pro will use as governed sources.

The check was run with:

```text
git ls-remote --heads https://github.com/Triotek-Ltd/<repo>.git
```

## Result

All planned repos checked below exist remotely or are accessible through Git.

## Core base repos

| Repo | Remote status | Branches seen |
| --- | --- | --- |
| `triotek-frappe` | OK | `main`, `upstream-v16` |
| `triotek-erpnext` | OK | `main`, `upstream-v16` |
| `triotek-bench` | OK | `build_clutter`, `calculate-cache-checksum`, `coerce-url`, `copilot/add-command-line-parameters-non-interactive`, `copilot/avoid-using-apps-txt`, `develop`, `fix-bench-deploy-2nd-try`, `fix-org-check`, `mprocs`, `staging`, `userforsecurity`, `v1.x`, `v3.x`, `v5.x` |

## 3plug-pro platform repos

| Repo | Remote status | Branches seen |
| --- | --- | --- |
| `3plug-pro-control` | OK | `main` |
| `3plug-pro-catalog` | OK | `main` |
| `3plug-pro-ops` | OK | `main` |
| `3plug-pro-stacks` | OK | `main` |
| `3plug-pro-environment-templates` | OK | No heads returned |

## Apps core repos

| Repo | Remote status | Branches seen |
| --- | --- | --- |
| `triotek-builder` | OK | `main`, `upstream-v16` |
| `triotek-crm` | OK | `main`, `upstream-v16` |
| `triotek-forensics` | OK | `main` |
| `triotek-frappe-mpesa-payments` | OK | `main`, `upstream-v16` |
| `triotek-gameplan` | OK | `main`, `upstream-v16` |
| `triotek-helpdesk` | OK | `main`, `upstream-v16` |
| `triotek-hrms` | OK | `main`, `upstream-v16` |
| `triotek-insights` | OK | `main`, `upstream-v16` |
| `triotek-ke` | OK | `main` |
| `triotek-mail` | OK | `main`, `upstream-v16` |
| `triotek-payments` | OK | `main`, `upstream-v16` |
| `triotek-print-designer` | OK | `main`, `upstream-v16` |
| `triotek-recon` | OK | `main` |
| `triotek-wiki` | OK | `main`, `upstream-v16` |

## Apps vertical repos

| Repo | Remote status | Branches seen |
| --- | --- | --- |
| `triotek-agriculture` | OK | `main`, `upstream-v16` |
| `triotek-aviation-base` | OK | `main`, `upstream-v16` |
| `triotek-construction-base` | OK | `main`, `upstream-v16` |
| `triotek-education` | OK | `main`, `upstream-v16` |
| `triotek-healthcare` | OK | `main`, `upstream-v16` |
| `triotek-hospitality-base` | OK | `main`, `upstream-v16` |
| `triotek-lending` | OK | `main`, `upstream-v16` |
| `triotek-livestock-base` | OK | `main`, `upstream-v16` |
| `triotek-lms` | OK | `main`, `upstream-v16` |
| `triotek-logistics-base` | OK | `main`, `upstream-v16` |
| `triotek-manufacturing-base` | OK | `main`, `upstream-v16` |
| `triotek-non-profit` | OK | `main`, `upstream-v16` |
| `triotek-posawesome` | OK | `main`, `upstream-v16` |
| `triotek-property-management-base` | OK | `main`, `upstream-v16` |
| `triotek-public-procurement-base` | OK | `main`, `upstream-v16` |
| `triotek-restaurant-base` | OK | `main`, `upstream-v16` |
| `triotek-services-base` | OK | `main`, `upstream-v16` |
| `triotek-telecom-base` | OK | `main`, `upstream-v16` |
| `triotek-trading-base` | OK | `main` |
| `triotek-utility-billing` | OK | `main`, `upstream-v16` |
| `triotek-vehicle-trading-base` | OK | `main`, `upstream-v16` |
| `triotek-webshop` | OK | `main`, `upstream-v16` |

## Follow-up notes

* `triotek-bench` needs branch-policy review because it does not currently show `main` or `upstream-v16`.
* `3plug-pro-environment-templates` exists but returned no branch heads, so it may be empty.
* Triotek-native repos with only `main` are acceptable if they are not upstream-derived.
* Upstream-derived repos should generally keep `main` and `upstream-v16` unless a repo-specific policy says otherwise.
* 3plug-pro should install from Triotek-controlled `main` by default. `upstream-v16` is an upstream tracking branch, not the default install branch.
