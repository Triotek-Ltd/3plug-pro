#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_USER="${THREEPLUG_USER:-threeplug}"
THREEPLUG_WORKDIR="${THREEPLUG_WORKDIR:-/opt/3plug-pro}"
THREEPLUG_HOME="${THREEPLUG_HOME:-/home/${THREEPLUG_USER}}"
THREEPLUG_VENV="${THREEPLUG_VENV:-${THREEPLUG_HOME}/.local/share/3plug-pro/venv}"
THREEPLUG_GLOBAL_BIN_DIR="${THREEPLUG_GLOBAL_BIN_DIR:-/usr/local/bin}"
REMOVE_WORKDIR="${REMOVE_WORKDIR:-1}"
REMOVE_VENV="${REMOVE_VENV:-1}"
REMOVE_USER="${REMOVE_USER:-0}"
THREEPLUG_FORCE="${THREEPLUG_FORCE:-0}"

if [ "$(id -u)" -ne 0 ]; then
  echo "Run this script as root or with sudo." >&2
  exit 1
fi

terminate_user_processes() {
  local user="$1"
  if ! id "${user}" >/dev/null 2>&1; then
    return 0
  fi

  if command -v loginctl >/dev/null 2>&1; then
    loginctl terminate-user "${user}" >/dev/null 2>&1 || true
  fi

  pkill -TERM -u "${user}" >/dev/null 2>&1 || true
  sleep 2
  if pgrep -u "${user}" >/dev/null 2>&1; then
    pkill -KILL -u "${user}" >/dev/null 2>&1 || true
    sleep 1
  fi
}

remove_operator_user() {
  local user="$1"

  terminate_user_processes "${user}"

  if command -v userdel >/dev/null 2>&1; then
    userdel -r "${user}" && return 0
    userdel -f "${user}" && return 0
  fi

  if command -v deluser >/dev/null 2>&1; then
    deluser --remove-home "${user}" && return 0
  fi

  echo "Failed to remove operator user: ${user}" >&2
  return 1
}

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

for global_cmd in 3plug 3plug-pro; do
  global_path="${THREEPLUG_GLOBAL_BIN_DIR}/${global_cmd}"
  if [ -L "${global_path}" ] || [ -f "${global_path}" ]; then
    resolved_path="$(readlink -f "${global_path}" 2>/dev/null || true)"
    case "${resolved_path}" in
      "${THREEPLUG_VENV}"/*)
        echo "Removing global command link: ${global_path}"
        rm -f "${global_path}"
        ;;
    esac
  fi
done

if id "${THREEPLUG_USER}" >/dev/null 2>&1; then
  if [ "${REMOVE_USER}" = "1" ]; then
    echo "Removing operator user: ${THREEPLUG_USER}"
    remove_operator_user "${THREEPLUG_USER}"
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
