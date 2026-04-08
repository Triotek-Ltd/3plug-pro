# 3plug-pro CLI

This folder contains the first Python CLI for 3plug-pro.

The operator-facing command is:

```text
3plug
```

The compatibility/project command is:

```text
3plug-pro
```

The first implementation focuses on:

* workspace checks
* design and repo-plan reporting
* catalog listing
* server preflight checks
* server bootstrap, update, and uninstall commands
* local job recording and job inspection
* safe planning before Bench install and site operations

Current server commands include:

```text
3plug server preflight
3plug server bootstrap
3plug server git-setup
3plug server install-cli
3plug server update
3plug server uninstall
3plug job list
3plug job show <job-id>
```

Run the local smoke tests from the repo root with:

```text
python -m unittest discover -s cli/tests
```
