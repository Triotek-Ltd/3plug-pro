# 3plug Publishing Guidelines

## Purpose

This document is the canonical guide for publishing stable 3plug CLI releases from Git.

The release model is:

* `main` for active development
* Git tags such as `v0.2.0` for stable releases
* GitHub Actions for CI and release automation

Production-like installs should prefer tagged releases over moving `main`.

## Release Principles

* every release comes from a committed Git state
* every release is identified by a Git tag
* CI must pass before a release tag is pushed
* the version in `cli/pyproject.toml` and `cli/threeplugpro/__init__.py` must match the intended release tag
* release notes should exist in `design/` before the tag is pushed

## Automated Workflows

The repository includes two GitHub Actions workflows:

* `.github/workflows/ci.yml`
  * runs on pushes and pull requests
  * installs the CLI from `cli/`
  * runs the smoke suite with `python -m unittest discover -s cli/tests`
* `.github/workflows/release.yml`
  * runs when a tag matching `v*` is pushed
  * verifies the package version matches the tag
  * builds the CLI artifacts from `cli/`
  * creates a GitHub release
  * attaches the built wheel and source distribution

## Release Checklist

### Step 1: Finish And Verify The Change

Make sure:

* the code is committed or ready to commit
* tests pass locally
* docs are updated when operator commands changed

Recommended local check:

```powershell
python -m unittest discover -s cli\tests
```

### Step 2: Bump The Version

Update both of these files to the next version:

* `cli/pyproject.toml`
* `cli/threeplugpro/__init__.py`

Example:

* package version: `0.2.0`
* release tag: `v0.2.0`

These values must match.

### Step 3: Add Release Notes

Add a release note file under `design/` named like:

```text
design/release-notes-0.2.0.md
```

The release workflow will use this file automatically when the matching tag is published.

### Step 4: Commit And Push Main

Example:

```powershell
git add .
git commit -m "Release 0.2.0"
git push origin main
```

### Step 5: Create And Push The Tag

Example:

```powershell
git tag v0.2.0
git push origin v0.2.0
```

Pushing the tag triggers the automated release workflow.

## What The Release Workflow Enforces

When a tag like `v0.2.0` is pushed, the release workflow:

1. checks out the repository
2. reads the version from `cli/pyproject.toml`
3. fails if the tag and package version do not match
4. builds the package from `cli/`
5. uses `design/release-notes-<version>.md` when present
6. creates a GitHub release and uploads artifacts

## Stable Install Sources

For stable server installs or updates, prefer tag-based package URLs:

```text
git+https://github.com/Triotek-Ltd/3plug-pro.git@v0.2.0#subdirectory=cli
```

Use `main` only when you intentionally want the newest development state.

## Operator Upgrade Guidance

After a stable release is pushed, an existing server can update with:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/configure_3plug_git.sh -o /tmp/configure_3plug_git.sh
sudo bash /tmp/configure_3plug_git.sh

curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/update_3plug_server.sh -o /tmp/update_3plug_server.sh
sudo THREEPLUG_PACKAGE_URL="git+https://github.com/Triotek-Ltd/3plug-pro.git@v0.2.0#subdirectory=cli" bash /tmp/update_3plug_server.sh
```

For a first install from a stable release, use the same tag-based package URL with `install_3plug_cli.sh`.

## Maintainer Notes

* keep release notes concise and operator-oriented
* do not reuse a tag for a different commit
* if a release must be corrected, bump to a new version and tag
* prefer annotated communication through release notes instead of undocumented hotfixes
