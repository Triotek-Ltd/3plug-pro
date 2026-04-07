# Triotek-Owned Apps

## Purpose

This file defines the app and service areas Triotek should own directly instead of relying on the public ecosystem.

These are the places where:

* Kenya and East Africa needs are strong
* the public ecosystem is fragmented
* product differentiation matters
* forensic and control needs are too important to outsource casually

## Core Triotek-owned platform

### 0. `triotek_frappe`

Triotek-controlled framework base.

Responsibilities:

* controlled upstream framework intake
* security patching
* version pinning
* Triotek-specific hardening

### 0b. `triotek_erpnext`

Triotek-controlled ERP base.

Responsibilities:

* controlled upstream ERP intake
* version pinning
* Triotek-approved customizations
* compatibility base for all Triotek apps

### 0c. `triotek_bench`

Triotek-controlled Bench base.

Responsibilities:

* controlled operational behavior
* 3plug-compatible execution patterns
* Triotek-approved command and workflow changes

### 1. `3plug_control`

Primary control-plane app or service layer for 3plug.

Responsibilities:

* environment state
* site lifecycle orchestration
* app stack management
* job management
* operator actions
* audit history
* integration with Bench execution

### 2. `3plug_ops`

Operational automation layer.

Responsibilities:

* background jobs
* migrations orchestration
* backup workflows
* restore workflows
* health checks
* deployment actions

### 3. `3plug_catalog`

Repo and app registry layer.

Responsibilities:

* approved repo catalog
* stack definitions
* release references
* compatibility metadata
* provisioning rules

## Kenya and finance-specific apps

### 4. `triotek_ke`

Kenya localization app.

Responsibilities:

* Kenya-specific business defaults
* tax and document conventions where needed
* local reporting helpers
* integrations registry for Kenya-facing workflows

Public ecosystem note:

* no public official Kenya-specific app was found in the Frappe org

### 5. `triotek_payments`

Triotek payment integration layer.

Responsibilities:

* M-Pesa workflows
* payment normalization
* callback handling
* payment event storage
* settlement reference mapping

This should not just be a thin integration wrapper. It should be the stable base for Triotek-owned payment logic.

Public ecosystem note:

* a related official upstream exists in `frappe/payments`
* Triotek should still own the final Kenya-first abstraction and control layer

### 6. `triotek_recon`

Reconciliation and discrepancy engine.

Responsibilities:

* POS to payment reconciliation
* payment to bank reconciliation
* discrepancy detection
* nightly clerk jobs
* reconciliation reports
* unmatched transaction review

Public ecosystem note:

* no public official standalone reconciliation app was found in the Frappe org

### 7. `triotek_forensics`

Forensic controls and evidence layer.

Responsibilities:

* append-only audit events
* evidence capture
* raw payload preservation
* traceability views
* evidence export
* archive verification logic

Public ecosystem note:

* no public official standalone forensic-controls app was found in the Frappe org

## Vertical product apps

### 8. `triotek_utility`

Utility billing vertical.

Responsibilities:

* billing cycles
* meter-linked billing
* arrears management
* service charge logic
* estate and campus billing extensions

### 9. `triotek_property`

Property operations vertical.

Responsibilities:

* tenant and unit workflows
* rent and service charge
* maintenance ticketing
* property operations reporting
* collections and arrears views

### 10. `triotek_health`

Healthcare operational extensions.

Responsibilities:

* Triotek-specific workflows on top of healthcare base
* billing controls
* multi-branch support patterns
* operational reporting

### 11. `triotek_agri`

Agribusiness and value-chain workflows.

Responsibilities:

* produce collection
* outgrower workflows
* payout flows
* traceability support
* stock and procurement extensions

### 12. `triotek_ngo`

NGO and donor controls pack.

Responsibilities:

* grant workflows
* approval controls
* reporting support
* compliance-oriented audit structures

## Initial ownership rule

Triotek should not try to build all of these at once.

The first ownership priority should be:

1. `triotek_frappe`
2. `triotek_erpnext`
3. `triotek_bench`
4. `3plug_control`
5. `3plug_catalog`
6. `triotek_payments`
7. `triotek_recon`
8. `triotek_forensics`
9. `triotek_utility`
10. `triotek_property`

That sequence aligns with the strongest commercial opportunities.

## Why this matters for 3plug

Yes, the intention should be that 3plug points only to Triotek-owned repos, not directly to arbitrary upstream repos in uncontrolled ways.

That means:

* Triotek controls the stack definition
* Triotek controls what is provisioned
* Triotek can pin releases
* Triotek can keep custom logic in its own repos
* 3plug becomes a governed platform, not just a pass-through to random GitHub sources
