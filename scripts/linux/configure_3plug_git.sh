#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_USER="${THREEPLUG_USER:-threeplug}"
THREEPLUG_GIT_NAME="${THREEPLUG_GIT_NAME:-}"
THREEPLUG_GIT_EMAIL="${THREEPLUG_GIT_EMAIL:-}"

if [ "$(id -u)" -ne 0 ]; then
  echo "Run this script as root or with sudo." >&2
  exit 1
fi

if ! id "${THREEPLUG_USER}" >/dev/null 2>&1; then
  echo "Operator user does not exist: ${THREEPLUG_USER}" >&2
  echo "Run bootstrap first." >&2
  exit 1
fi

prompt_value() {
  local label="$1"
  local current="$2"
  local value="$current"
  while [ -z "${value}" ]; do
    read -r -p "${label}: " value
  done
  printf '%s' "${value}"
}

if [ -z "${THREEPLUG_GIT_NAME}" ]; then
  THREEPLUG_GIT_NAME="$(prompt_value "Git user.name for ${THREEPLUG_USER}" "")"
fi

if [ -z "${THREEPLUG_GIT_EMAIL}" ]; then
  THREEPLUG_GIT_EMAIL="$(prompt_value "Git user.email for ${THREEPLUG_USER}" "")"
fi

echo "Configuring Git identity for ${THREEPLUG_USER}"
sudo -H -u "${THREEPLUG_USER}" git config --global user.name "${THREEPLUG_GIT_NAME}"
sudo -H -u "${THREEPLUG_USER}" git config --global user.email "${THREEPLUG_GIT_EMAIL}"

cat <<EOF

Git configuration complete.

Configured values:

  user.name=${THREEPLUG_GIT_NAME}
  user.email=${THREEPLUG_GIT_EMAIL}

Verify as ${THREEPLUG_USER}:

  git config --global --get user.name
  git config --global --get user.email

EOF
