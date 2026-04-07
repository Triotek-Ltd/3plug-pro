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
* safe planning before Bench install and site operations

Run the local smoke tests from the repo root with:

```text
python -m unittest discover -s cli/tests
```
