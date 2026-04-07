# 3plug-pro Roadmap Status

## Current position

We are following `roadmap.md`.

Current build position:

* Phase 0: complete except commit decision
* Phase 1: complete for the pre-server foundation; bench lifecycle commands still start next
* Linux VM target: planned next with WSL Ubuntu 24.04
* Phase 2 and later: not started

## Phase 0: Repo Cleanup and Build Foundation

Status: complete except commit decision

Deliverable checklist:

* done: root `.gitignore`
* done: `design/` folder and design index
* done: root README updated to point to `design/` and `3plug/repos/`
* done: CLI paths updated from old `rnd/3plug/...` assumptions to current repo-root-relative paths
* done: package naming decision documented through `3plug` and `3plug-pro` console entries
* done: formal tests or scripted smoke checks for the current CLI

Remaining:

* decide when to commit the current repo foundation

## Phase 1: 3plug CLI Package

Status: pre-server foundation complete

Deliverable checklist:

* done: package entry point for `3plug`
* done: existing `3plug-pro` command retained during transition
* done: command group `3plug doctor`
* done: command group `3plug init`
* done: command group `3plug server preflight`
* done: command group `3plug install bench`
* done: command group `3plug install server-dependencies`
* done: command group `3plug bench list`
* done: command group `3plug job list`
* done: command group `3plug app list`
* done: command group `3plug app show <app>`
* done: command group `3plug stack list`
* done: command output is readable for current commands
* done: local config path handling
* done: local data path handling
* done: scriptable output format such as JSON mode
* done: installed-package smoke test

Remaining:

* start `bench register`, `bench create`, and `bench status`

## Phase 2: Local State and Job Store

Status: not started

Next expected work:

* create SQLite state layer
* add tables for servers, environments, benches, sites, app sources, stacks, jobs, audit events, and backups
* make `3plug init` initialize the local state database
* make plan-only commands create dry-run job records

## Linux VM Target

Status: prepared, but WSL distro installation is blocked from the current terminal

Target:

* WSL Ubuntu 24.04
* install from `git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli`
* run `3plug init`
* run `3plug server preflight`
* implement and test real Linux `install server-dependencies`, `install bench`, and `bench create`

Important:

* Git URL install will only include the current foundation after it is committed and pushed.
* Until then, local editable install is the only way to test the current working tree.
* `wsl.exe --install Ubuntu-24.04` timed out twice from this terminal, and `wsl.exe -l -v` still reports no installed distributions.
* `3plug doctor` is currently a source workspace check; use `3plug server preflight` as the first runtime check on a pip-installed server.

## Current smoke checks

Last manual checks run:

```text
python -m compileall threeplugpro
python -m unittest discover -s cli/tests
python cli/threeplugpro/cli.py doctor
python cli/threeplugpro/cli.py app list
python cli/threeplugpro/cli.py stack list
python cli/threeplugpro/cli.py install bench
python cli/threeplugpro/cli.py install server-dependencies
python cli/threeplugpro/cli.py server preflight
tmp/package-smoke-venv/Scripts/3plug.exe --help
tmp/package-smoke-venv/Scripts/3plug-pro.exe --help
tmp/package-smoke-venv/Scripts/3plug.exe --root . --format json app show erpnext
```

The temporary package-smoke venv was removed after validation.

Expected current warning:

* `bench` is not on PATH in the current Windows development shell
* several Linux/server dependencies are missing in the current Windows development shell

These are expected until Phase 4 and Phase 5 are implemented on the managed server target.
