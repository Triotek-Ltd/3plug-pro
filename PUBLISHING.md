# 3plug Publishing Guidelines

## Purpose

This document is the canonical guide for publishing stable 3plug CLI releases from Git.

The release model is:

* `main` for active development
* automatic patch releases from pushes to `main`
* Git tags such as `v0.2.1` for stable releases
* GitHub Actions for CI and release automation

Production-like installs should prefer tagged releases over moving `main`.

## Release Principles

* every release comes from a committed Git state
* every release is identified by a Git tag
* CI should pass before code is merged or pushed to `main`
* the version in `cli/pyproject.toml` and `cli/threeplugpro/__init__.py` is automatically bumped by the release workflow
* release notes are generated automatically for each patch release

## Automated Workflows

The repository includes two GitHub Actions workflows:

* `.github/workflows/ci.yml`
  * runs on pushes and pull requests
  * installs the CLI from `cli/`
  * runs the smoke suite with `python -m unittest discover -s cli/tests`
* `.github/workflows/release.yml`
  * runs on pushes to `main`
  * automatically bumps the patch version
  * writes the version into `cli/pyproject.toml` and `cli/threeplugpro/__init__.py`
  * generates release notes under `design/`
  * commits the release bump back to `main`
  * creates and pushes a Git tag
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

### Step 2: Confirm The Current Release Base Version

Keep these two files aligned with the current release line:

* `cli/pyproject.toml`
* `cli/threeplugpro/__init__.py`

Example:

* checked-in package version before the next push: `0.2.0`
* next automatic release from `main`: `v0.2.1`

The release workflow will automatically bump the patch version on the next push to `main`.

### Step 3: Commit And Push Main

Example:

```powershell
git add .
git commit -m "Add bench readiness commands"
git push origin main
```

The release workflow will then:

1. bump `0.2.0` to `0.2.1`
2. commit the release version files
3. create `design/release-notes-0.2.1.md`
4. tag `v0.2.1`
5. publish the GitHub release automatically

### Step 4: Review The Published Release

After the workflow completes, GitHub should show:

* a new release tag like `v0.2.1`
* built artifacts attached to the release
* generated release notes for that patch release

## What The Release Workflow Enforces

When code is pushed to `main`, the release workflow:

1. checks out the repository
2. reads the version from `cli/pyproject.toml`
3. increments the patch version
4. updates `cli/threeplugpro/__init__.py`
5. generates `design/release-notes-<version>.md`
6. commits the release bump to `main`
7. creates a matching Git tag
8. builds the package from `cli/`
9. creates a GitHub release and uploads artifacts

## Stable Install Sources

For stable server installs or updates later, prefer explicit release tags. Until regular releases are actually being published, the scripts default to the current pre-release source on `main`.

```text
git+https://github.com/Triotek-Ltd/3plug-pro.git@v0.2.1#subdirectory=cli
```

Use `main` only when you intentionally want the newest development state.

## Operator Upgrade Guidance

After a stable release is pushed, an existing server can update with:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/configure_3plug_git.sh -o /tmp/configure_3plug_git.sh
sudo bash /tmp/configure_3plug_git.sh

curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/update_3plug_server.sh -o /tmp/update_3plug_server.sh
sudo THREEPLUG_PACKAGE_URL="git+https://github.com/Triotek-Ltd/3plug-pro.git@v0.2.1#subdirectory=cli" bash /tmp/update_3plug_server.sh
```

For a first install from a stable release later, use the same tag-based package URL with `install_3plug_cli.sh`. For now, if you do not provide `THREEPLUG_PACKAGE_URL`, the scripts default to `main` as the current pre-release source.

## Maintainer Notes

* keep release notes concise and operator-oriented
* do not reuse a tag for a different commit
* if a release must be corrected, push a new commit to `main` and let the next patch release be created automatically
* prefer annotated communication through release notes instead of undocumented hotfixes
* this auto-release model is appropriate for the current `0.x` line; revisit it before the project reaches `1.x` and again before `3.x`
