# 3plug-pro Publishing

## Current publish reality

This local root scaffold is ready to be pushed once GitHub authentication for an authorized `Triotek-Ltd` maintainer is valid.

Current known constraint:

* the configured GitHub CLI token for `kimash-255` is invalid on this machine

## Before publishing

* authenticate GitHub CLI successfully
* confirm org permissions on `Triotek-Ltd`
* create the `3plug-pro` repo in the organization
* initialize and push this scaffold

## Recommended first push

```powershell
git init
git branch -M main
git remote add origin https://github.com/Triotek-Ltd/3plug-pro.git
git add .
git commit -m "Initialize 3plug-pro coordination repo"
git push -u origin main
```
