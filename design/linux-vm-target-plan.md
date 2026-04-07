# Linux VM Target Plan

This is the first production-like target for 3plug-pro.

## Purpose

Use a local Linux environment as the first managed server target before testing on a remote server.

Initial host model:

```text
Windows development machine
-> WSL Ubuntu 24.04 local Linux target
-> 3plug installed from Git URL
-> server preflight
-> server dependency installer
-> Bench installer
-> first managed bench
```

## Install Source

The production-like install source is the Git URL:

```text
python3 -m venv ~/.local/share/3plug-pro/venv
~/.local/share/3plug-pro/venv/bin/python -m pip install --upgrade pip
~/.local/share/3plug-pro/venv/bin/python -m pip install "git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli"
export PATH="$HOME/.local/share/3plug-pro/venv/bin:$PATH"
```

Until the current foundation is committed and pushed, the Git URL will install the last pushed version on GitHub, not the current working tree.

For a test branch, use:

```text
~/.local/share/3plug-pro/venv/bin/python -m pip install "git+https://github.com/Triotek-Ltd/3plug-pro.git@<branch>#subdirectory=cli"
```

## First Commands

The first Linux target commands should be:

```text
3plug --help
3plug init
3plug server preflight
3plug install server-dependencies
3plug install bench
```

At this stage, `install server-dependencies` and `install bench` may still be plan-only until we implement the real Linux handlers.

`3plug doctor` is currently a source workspace check. Use `3plug server preflight` as the first runtime check on a pip-installed Linux target.

## Local VM Choice

On the current Windows machine:

* WSL is installed.
* No WSL distributions are installed yet.
* WSL default version is 2.
* Ubuntu 24.04 is available.
* Multipass, VirtualBox, and Vagrant are not currently on PATH.

Therefore the first local Linux target should be:

```text
wsl.exe --install Ubuntu-24.04
```

## Current VM Setup Status

Status: blocked on WSL distro installation from the terminal.

Observed:

* `wsl.exe --list --online` shows Ubuntu 24.04 as available.
* `wsl.exe --status` shows WSL default version 2.
* `wsl.exe --install Ubuntu-24.04` timed out twice from this terminal.
* `wsl.exe -l -v` still reports no installed distributions.

Next local step:

```text
wsl.exe --install Ubuntu-24.04
```

If it still does not complete, install Ubuntu 24.04 from the Windows WSL install flow or Microsoft Store, then rerun:

```text
wsl.exe -l -v
```

## Guardrails

* Keep the Windows dev repo as the source workspace.
* Treat WSL Ubuntu as the managed server target.
* Do not use random app URLs for `bench get-app`; use the Triotek catalog and `main` branch.
* Keep `upstream-v16` as intake/tracking only.
* Do not mark production ready until `3plug install server-dependencies`, `3plug install bench`, and `3plug bench create production` are implemented and tested on Linux.
