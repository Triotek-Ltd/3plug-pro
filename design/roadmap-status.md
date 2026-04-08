# 3plug-pro Roadmap Status

## Current position

We are following `roadmap.md`.

Current build position:

* Phase 0: complete except commit decision
* Phase 1: complete for the server foundation and initial install flows
* Linux VM target: planned next with WSL Ubuntu 24.04
* Phase 2: started for local SQLite state and job recording
* Later bench/site lifecycle phases: not started

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

Status: started

Completed so far:

* `3plug init` creates the local state database
* server lifecycle commands create job records
* install commands create job records
* `3plug job list` reads recorded jobs
* `3plug job show <job-id>` reads job details and audit events

Remaining expected work:

* expand SQLite state beyond the current job/audit baseline
* add tables for servers, environments, benches, sites, app sources, stacks, and backups
* record real bench and site lifecycle state as those commands become operational

## Linux VM Target

Status: prepared, but WSL distro installation is blocked from the current terminal

Target:

* WSL Ubuntu 24.04
* install from the latest published release, or pin a stable tag explicitly
* run `3plug init`
* run `3plug server preflight`
* run and validate real Linux `install server-dependencies`
* run and validate real Linux `install bench`
* implement and test real Linux `bench create`

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

These are expected until the bench lifecycle commands are implemented on the managed server target.
