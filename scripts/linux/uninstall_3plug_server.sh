#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_USER="${THREEPLUG_USER:-threeplug}"
THREEPLUG_WORKDIR="${THREEPLUG_WORKDIR:-/opt/3plug-pro}"
THREEPLUG_HOME="${THREEPLUG_HOME:-/home/${THREEPLUG_USER}}"
THREEPLUG_VENV="${THREEPLUG_VENV:-${THREEPLUG_HOME}/.local/share/3plug-pro/venv}"
REMOVE_WORKDIR="${REMOVE_WORKDIR:-1}"
REMOVE_VENV="${REMOVE_VENV:-1}"
REMOVE_USER="${REMOVE_USER:-0}"
THREEPLUG_FORCE="${THREEPLUG_FORCE:-0}"

if [ "$(id -u)" -ne 0 ]; then
  echo "Run this script as root or with sudo." >&2
  exit 1
fi

confirm() {
  local prompt="$1"
  if [ "${THREEPLUG_FORCE}" = "1" ]; then
    return 0
  fi

  local response
  read -r -p "${prompt} [y/N]: " response
  case "${response}" in
    y|Y|yes|YES)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

echo "3plug server uninstall plan"
echo "- operator user: ${THREEPLUG_USER}"
echo "- workspace: ${THREEPLUG_WORKDIR}"
echo "- venv: ${THREEPLUG_VENV}"
echo "- remove workspace: ${REMOVE_WORKDIR}"
echo "- remove venv: ${REMOVE_VENV}"
echo "- remove user: ${REMOVE_USER}"

if ! confirm "Continue with uninstall?"; then
  echo "Uninstall cancelled."
  exit 0
fi

if [ "${REMOVE_WORKDIR}" = "1" ] && [ -e "${THREEPLUG_WORKDIR}" ]; then
  echo "Removing workspace: ${THREEPLUG_WORKDIR}"
  rm -rf "${THREEPLUG_WORKDIR}"
fi

if [ "${REMOVE_VENV}" = "1" ] && [ -e "${THREEPLUG_VENV}" ]; then
  echo "Removing virtual environment: ${THREEPLUG_VENV}"
  rm -rf "${THREEPLUG_VENV}"
fi

if id "${THREEPLUG_USER}" >/dev/null 2>&1; then
  if [ "${REMOVE_USER}" = "1" ]; then
    echo "Removing operator user: ${THREEPLUG_USER}"
    deluser --remove-home "${THREEPLUG_USER}"
  else
    echo "Keeping operator user: ${THREEPLUG_USER}"
    if id -nG "${THREEPLUG_USER}" | tr ' ' '\n' | grep -qx "sudo"; then
      echo "Removing ${THREEPLUG_USER} from sudo group."
      deluser "${THREEPLUG_USER}" sudo
    fi
  fi
fi

cat <<EOF

Uninstall complete.

Manual follow-up to consider:

  ufw status verbose
  git config --global --list

EOF
