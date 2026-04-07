# 3plug Implementation App Universe

## Purpose

This document expands the 3plug app catalog beyond named public apps.

It answers a more practical implementation question:

What app and vertical solution families must Triotek have in scope if we want to implement serious Frappe-based systems across the real industries where custom work actually happens?

This matters because the public Frappe ecosystem does not expose every real solution as a neat reusable app.

A lot of real deployment value lives in:

* custom apps
* workflow packs
* localization layers
* portals
* industry-specific doctypes
* integration bundles

So if Triotek wants to start correctly, the repo and app universe must include both:

* public reusable apps
* planned internal apps for the private/custom verticals we know exist in the market

## Rule of interpretation

This is not the list of apps every customer gets.

This is the list of app families Triotek should be structurally ready to support, internalize, or build during implementation work.

## A. Core implementation universe

These are the baseline app families every serious Triotek implementation ecosystem should be able to draw from.

### Platform and core

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`
* `3plug-control`
* `3plug-catalog`
* `3plug-ops`
* `3plug-stacks`
* `3plug-environment-templates`

### Shared control and integration layer

* `triotek-ke`
* `triotek-payments`
* `triotek-recon`
* `triotek-forensics`

### General official apps

* `triotek-hrms`
* `triotek-crm`
* `triotek-helpdesk`
* `triotek-insights`
* `triotek-wiki`
* `triotek-print-designer`
* `triotek-mail`
* `triotek-gameplan`
* `triotek-builder`
* `triotek-webshop`
* `triotek-lending`
* `triotek-education`
* `triotek-lms`

### Internalized community apps

* `triotek-posawesome`
* `triotek-healthcare`
* `triotek-utility-billing`
* `triotek-frappe-mpesa-payments`

## B. Vertical solution families Triotek should plan for

These are the main implementation verticals evidenced by public Frappe stories, partner pages, and ecosystem patterns, even where the exact reusable apps are private or not published.

## 1. Agriculture and agribusiness

### Internal repo

* `triotek-agriculture`

### Typical hidden solution shape

* produce collection workflows
* outgrower management
* agrovet distribution
* procurement and payout controls
* processing and traceability extensions

## 2. Livestock

### Internal repo

* `triotek-livestock-base`

### Typical hidden solution shape

* flock or herd records
* feed and veterinary workflows
* production tracking
* farm operations controls

## 3. Food and beverages

### Internal repo

* `triotek-restaurant-base`

### Typical hidden solution shape

* batch and lot tracking
* repacking workflows
* distribution controls
* route-to-market operations
* beverage and FMCG processing workflows

## 4. Healthcare

### Internal repos

* `triotek-healthcare`

### Typical hidden solution shape

* clinic and hospital operations
* diagnostics and lab workflows
* pharmacy workflows
* claims and billing controls
* veterinary and animal-health variations

## 5. Education

### Internal repos

* `triotek-education`
* `triotek-lms`

### Typical hidden solution shape

* school administration
* higher education operations
* training center workflows
* student and parent portals

## 6. NGO / nonprofit

### Internal repo

* `triotek-non-profit`

### Typical hidden solution shape

* donor and grant workflows
* field-program tracking
* procurement controls
* approval and compliance extensions
* MEL-oriented reporting patterns

## 7. Real estate / property / estates

### Internal repos

* `triotek-property-management-base`
* `triotek-utility-billing`

### Typical hidden solution shape

* tenant and unit workflows
* rent and service charge
* utility billing
* maintenance management
* project and estate-level operations

## 8. Engineering and construction

### Internal repo

* `triotek-construction-base`

### Typical hidden solution shape

* BOQ and project cost controls
* subcontractor billing
* site procurement
* project reporting
* progress certification workflows

## 9. Logistics / transport / distribution

### Internal repo

* `triotek-logistics-base`

### Typical hidden solution shape

* route and dispatch workflows
* branch transfer visibility
* stock-in-transit controls
* freight and delivery workflows
* proof-of-delivery patterns

## 10. Government / public-service operations

### Internal repo

* `triotek-public-procurement-base`

### Typical hidden solution shape

* service request workflows
* controlled approvals
* field or public-service operational workflows
* audit-heavy reporting

## 11. Manufacturing

### Internal repo

* `triotek-manufacturing-base`

### Typical hidden solution shape

* process manufacturing extensions
* discrete manufacturing controls
* quality, lot, and compliance extensions
* highly specific factory workflows

## 12. Retail / POS / multi-branch commerce

### Internal repos

* `triotek-posawesome`

### Typical hidden solution shape

* outlet and cashier workflows
* branch sales controls
* stock and transfer visibility
* till and reconciliation support

## 13. Ecommerce

### Internal repos

* `triotek-webshop`

### Typical hidden solution shape

* ERP + store sync
* B2B/B2C order workflows
* warehouse and fulfillment controls
* customer portal and order status layers

## 14. Banking / insurance / broking / fintech

### Internal repos

* `triotek-lending`

### Typical hidden solution shape

* lending and collections
* brokerage workflows
* claims and policy administration patterns
* regulated operational audit trails

## 15. Professional services / consulting / software services

### Internal repo

* `triotek-services-base`

### Typical hidden solution shape

* timesheets and SLA workflows
* client billing
* service project controls
* internal resource planning

## 16. Hospitality

### Internal repo

* `triotek-hospitality-base`

### Typical hidden solution shape

* guest and booking operations
* service billing
* restaurant and hotel workflows
* housekeeping or service-task extensions

## 17. Telecommunications

### Internal repo

* `triotek-telecom-base`

### Typical hidden solution shape

* subscription-like workflows
* service operations
* field and support controls
* billing integration layers

## 18. Aviation

### Internal repo

* `triotek-aviation-base`

### Typical hidden solution shape

* niche service workflows
* maintenance or operational tracking
* highly controlled service records

## 19. Goods trading / trading and distribution

### Internal repo

* `triotek-trading-base`
* `triotek-vehicle-trading-base`

### Typical hidden solution shape

* price-list controls
* branch and distributor operations
* stock, approvals, and purchasing rules
* heavy trading and distribution workflows

## C. Full implementation-ready repo universe

This is the broad repo universe Triotek should account for if we want to be implementation-ready across the real market:

### Core base

* `triotek-frappe`
* `triotek-erpnext`
* `triotek-bench`

### 3plug platform

* `3plug-control`
* `3plug-catalog`
* `3plug-ops`
* `3plug-stacks`
* `3plug-environment-templates`

### Shared apps

* `triotek-ke`
* `triotek-payments`
* `triotek-recon`
* `triotek-forensics`

### Internalized official and ecosystem apps

* `triotek-hrms`
* `triotek-crm`
* `triotek-helpdesk`
* `triotek-insights`
* `triotek-wiki`
* `triotek-print-designer`
* `triotek-builder`
* `triotek-mail`
* `triotek-gameplan`
* `triotek-webshop`
* `triotek-lending`
* `triotek-education`
* `triotek-lms`
* `triotek-posawesome`
* `triotek-healthcare`
* `triotek-utility-billing`
* `triotek-frappe-mpesa-payments`

### Vertical native apps

* `triotek-agriculture`
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
* `triotek-non-profit`
* `triotek-public-procurement-base`

## D. Practical rollout rule

Being implementation-ready does not mean creating every app in full immediately.

The correct model is:

* reserve the full universe
* create the highest-priority repos first
* create lightweight placeholders for the rest
* build each vertical deeply only when it becomes commercially active

## E. Bottom line

Yes, if Triotek wants to start correctly, the implementation universe must include the hidden/custom verticals too, not just the publicly named apps.

That means agriculture, NGO, logistics, construction, retail, trading, hospitality, telecom, aviation, government, food, and livestock all belong in the planned repo and app universe, even if they start as reserved or lightweight repos before they become major products.
