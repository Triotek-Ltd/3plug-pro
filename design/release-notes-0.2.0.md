# 3plug-pro 0.2.0 Release Notes

## Summary

This release turns the server lifecycle into a more usable operator flow for real Linux hosts.

## Included

* `3plug server bootstrap`
* `3plug server git-setup`
* `3plug server install-cli`
* `3plug server update`
* `3plug server uninstall`
* local job recording for server lifecycle actions
* global `3plug` and `3plug-pro` commands through `/usr/local/bin`
* Git identity gate before install and update flows
* safer uninstall handling for active operator sessions and distro differences
* preflight fallback handling for common Linux command-name differences such as `python3`

## Operator impact

Use the runbook in `design/server-operator-runbook.md` for:

* new server bootstrap
* upgrade from earlier server installs
* uninstall and operator-user removal

## Upgrade note

After this release is pushed, older server installs should refresh with:

```bash
curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/configure_3plug_git.sh -o /tmp/configure_3plug_git.sh
sudo bash /tmp/configure_3plug_git.sh

curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/update_3plug_server.sh -o /tmp/update_3plug_server.sh
sudo bash /tmp/update_3plug_server.sh
```
