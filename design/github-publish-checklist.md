# 3plug-pro GitHub Publish Checklist

## Purpose

This document gives the exact practical steps for publishing `3plug-pro` into the `Triotek-Ltd` organization once GitHub access is working.

Primary target member for setup:

* `kimash-255`

Target organization:

* `Triotek-Ltd`

## Step 1: Re-authenticate GitHub CLI

Run:

```powershell
gh auth logout -h github.com -u kimash-255
gh auth login -h github.com
```

Recommended choices during login:

* GitHub.com
* HTTPS
* authenticate via browser

## Step 2: Verify org access

Run:

```powershell
gh auth status
gh repo list Triotek-Ltd --limit 5
```

If the second command fails due to permissions, stop and fix org access first.

## Step 3: Create the root project repo

Recommended repo:

* `Triotek-Ltd/3plug-pro`

Run:

```powershell
gh repo create Triotek-Ltd/3plug-pro --private --description "Triotek 3plug-pro platform coordination, architecture, standards, and bootstrap repo"
```

## Step 4: Create the first platform repos

Run:

```powershell
gh repo create Triotek-Ltd/triotek-frappe --private --description "Triotek-controlled Frappe framework base"
gh repo create Triotek-Ltd/triotek-erpnext --private --description "Triotek-controlled ERPNext base"
gh repo create Triotek-Ltd/triotek-bench --private --description "Triotek-controlled Bench base"
gh repo create Triotek-Ltd/3plug-pro-control --private --description "3plug-pro control plane"
gh repo create Triotek-Ltd/3plug-pro-catalog --private --description "3plug-pro catalog and stack registry"
gh repo create Triotek-Ltd/3plug-pro-ops --private --description "3plug-pro operations and job automation"
gh repo create Triotek-Ltd/3plug-pro-stacks --private --description "3plug-pro stack definitions"
gh repo create Triotek-Ltd/3plug-pro-environment-templates --private --description "3plug-pro environment templates"
```

## Step 5: Create the first app repos

Run:

```powershell
gh repo create Triotek-Ltd/triotek-ke --private --description "Triotek Kenya localization app"
gh repo create Triotek-Ltd/triotek-payments --private --description "Triotek payments integration layer"
gh repo create Triotek-Ltd/triotek-recon --private --description "Triotek reconciliation engine"
gh repo create Triotek-Ltd/triotek-forensics --private --description "Triotek forensic controls app"
gh repo create Triotek-Ltd/triotek-trading-base --private --description "Triotek trading and distribution vertical app"
```

## Step 6: Set default branch policy

For each repo, set default branch to:

* `main`

Then create controlled compatibility branches later, such as:

* `v16-triotek`

## Step 7: Push the root project repo

Once the local root scaffold exists, from that folder run:

```powershell
git init
git branch -M main
git remote add origin https://github.com/Triotek-Ltd/3plug-pro.git
git add .
git commit -m "Initialize 3plug-pro coordination repo"
git push -u origin main
```

## Step 8: Configure branch protections

At minimum, protect:

* `main`
* later also `v16-triotek`

Recommended protections:

* require pull request before merge
* require at least one review
* restrict force pushes
* restrict deletions

## Step 9: Configure repo metadata

For each repo:

* confirm description
* confirm visibility
* add topics if useful
* confirm maintainers

## Step 10: Publish in waves

Do not try to push all repos with full code immediately.

Use this order:

1. `3plug-pro`
2. `triotek-frappe`
3. `triotek-erpnext`
4. `triotek-bench`
5. `3plug-pro-control`
6. `3plug-pro-catalog`
7. `triotek-payments`
8. `triotek-recon`
9. `triotek-forensics`
10. `triotek-ke`
11. `triotek-trading-base`

## Final note

This checklist assumes the org access is available and valid.

If `gh auth status` shows an invalid token, fix auth first before trying to publish anything.
