#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_USER="${THREEPLUG_USER:-threeplug}"
THREEPLUG_WORKDIR="${THREEPLUG_WORKDIR:-/opt/3plug-pro}"
THREEPLUG_HOME="${THREEPLUG_HOME:-/home/${THREEPLUG_USER}}"
THREEPLUG_VENV="${THREEPLUG_VENV:-${THREEPLUG_HOME}/.local/share/3plug-pro/venv}"
THREEPLUG_PACKAGE_URL="${THREEPLUG_PACKAGE_URL:-git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli}"

if [ "$(id -u)" -ne 0 ]; then
  echo "Run this script as root or with sudo." >&2
  exit 1
fi

if ! id "${THREEPLUG_USER}" >/dev/null 2>&1; then
  echo "Operator user does not exist: ${THREEPLUG_USER}" >&2
  echo "Run bootstrap first." >&2
  exit 1
fi

echo "Ensuring workspace exists: ${THREEPLUG_WORKDIR}"
mkdir -p "${THREEPLUG_WORKDIR}"
chown -R "${THREEPLUG_USER}:${THREEPLUG_USER}" "${THREEPLUG_WORKDIR}"

echo "Updating 3plug CLI for ${THREEPLUG_USER}"
sudo -H -u "${THREEPLUG_USER}" bash -lc "
  set -euo pipefail
  mkdir -p \"$(dirname "${THREEPLUG_VENV}")\"
  python3 -m venv \"${THREEPLUG_VENV}\"
  \"${THREEPLUG_VENV}/bin/python\" -m pip install --upgrade pip
  \"${THREEPLUG_VENV}/bin/python\" -m pip install --upgrade \"${THREEPLUG_PACKAGE_URL}\"
"

cat <<EOF

Update complete.

Recommended verification as ${THREEPLUG_USER}:

  export PATH="${THREEPLUG_VENV}/bin:\$PATH"
  3plug --help
  3plug server preflight

EOF
