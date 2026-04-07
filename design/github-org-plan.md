# 3plug GitHub Organization Plan

## Organization

Use this GitHub organization for the governed 3plug source ecosystem:

* `https://github.com/Triotek-Ltd`

## Known available member

Current available member referenced for setup and ownership:

* email: `rexviscot44@gmail.com`
* display/use name: `Kim`
* username reference: `kimash-255`

## Purpose

This document maps the 3plug repo plan to the actual GitHub organization so repo creation, ownership, and maintenance can be handled consistently.

## Core rule

All production repos used by 3plug should live under:

* `Triotek-Ltd`

They should not be created as primary repos under personal accounts.

This includes:

* Triotek-controlled forks
* Triotek native platform repos
* Triotek native app repos
* stack-definition repos
* platform and controls documentation repos

## Recommended repo targets

## A. Core controlled forks

* `Triotek-Ltd/triotek-frappe`
* `Triotek-Ltd/triotek-erpnext`
* `Triotek-Ltd/triotek-bench`

## B. Platform repos

* `Triotek-Ltd/3plug-pro-control`
* `Triotek-Ltd/3plug-pro-catalog`
* `Triotek-Ltd/3plug-pro-ops`
* `Triotek-Ltd/3plug-pro-stacks`
* `Triotek-Ltd/3plug-pro-environment-templates`

## C. Core shared apps

* `Triotek-Ltd/triotek-ke`
* `Triotek-Ltd/triotek-payments`
* `Triotek-Ltd/triotek-recon`
* `Triotek-Ltd/triotek-forensics`

## D. Internalized official or community apps

* `Triotek-Ltd/triotek-hrms`
* `Triotek-Ltd/triotek-crm`
* `Triotek-Ltd/triotek-helpdesk`
* `Triotek-Ltd/triotek-insights`
* `Triotek-Ltd/triotek-wiki`
* `Triotek-Ltd/triotek-print-designer`
* `Triotek-Ltd/triotek-builder`
* `Triotek-Ltd/triotek-mail`
* `Triotek-Ltd/triotek-gameplan`
* `Triotek-Ltd/triotek-lending`
* `Triotek-Ltd/triotek-education`
* `Triotek-Ltd/triotek-lms`
* `Triotek-Ltd/triotek-webshop`
* `Triotek-Ltd/triotek-posawesome`
* `Triotek-Ltd/triotek-healthcare`
* `Triotek-Ltd/triotek-utility-billing`
* `Triotek-Ltd/triotek-frappe-mpesa-payments`

## E. Vertical apps

* `Triotek-Ltd/triotek-healthcare`
* `Triotek-Ltd/triotek-livestock-base`
* `Triotek-Ltd/triotek-construction-base`
* `Triotek-Ltd/triotek-logistics-base`
* `Triotek-Ltd/triotek-manufacturing-base`
* `Triotek-Ltd/triotek-trading-base`
* `Triotek-Ltd/triotek-services-base`
* `Triotek-Ltd/triotek-hospitality-base`
* `Triotek-Ltd/triotek-telecom-base`
* `Triotek-Ltd/triotek-aviation-base`
* `Triotek-Ltd/triotek-restaurant-base`
* `Triotek-Ltd/triotek-vehicle-trading-base`
* `Triotek-Ltd/triotek-public-procurement-base`

## F. Documentation repos

* `Triotek-Ltd/triotek-platform-docs`
* `Triotek-Ltd/triotek-controls-docs`

## Maintainer expectations

The available member, `kimash-255`, can be used as an initial maintainer/operator if that account has the right organization permissions.

Recommended responsibilities for the initial maintainer:

* create repos under the organization
* set branch protections
* assign repo descriptions
* configure default branch policy
* ensure the correct visibility level
* add additional maintainers as the platform team grows

This account can act as an organization maintainer, but the repos themselves should still remain organization-owned.

## Governance recommendation

Do not let all repos depend on a single personal account operationally for too long.

Even if `kimash-255` is the current available member, Triotek should still aim to establish:

* org-level ownership
* multiple maintainers
* branch protection rules
* release discipline
* documented access control

## Local development implication

The actual codebase should be worked on locally in a consistent source layout, but the canonical remotes should still point to organization repos under `Triotek-Ltd`.

## Practical note

This plan maps the repos to the organization, but actual GitHub repo creation requires:

* authenticated access to the organization
* sufficient permissions on the member account being used
* network access from the machine performing the setup
