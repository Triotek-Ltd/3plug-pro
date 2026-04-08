#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_USER="${THREEPLUG_USER:-threeplug}"
THREEPLUG_WORKDIR="${THREEPLUG_WORKDIR:-/opt/3plug-pro}"
THREEPLUG_HOME="${THREEPLUG_HOME:-/home/${THREEPLUG_USER}}"
THREEPLUG_VENV="${THREEPLUG_VENV:-${THREEPLUG_HOME}/.local/share/3plug-pro/venv}"
THREEPLUG_PACKAGE_URL="${THREEPLUG_PACKAGE_URL:-latest}"
THREEPLUG_GLOBAL_BIN_DIR="${THREEPLUG_GLOBAL_BIN_DIR:-/usr/local/bin}"

resolve_latest_package_url() {
  local latest_tag
  latest_tag="$(curl -fsSL https://api.github.com/repos/Triotek-Ltd/3plug-pro/releases/latest | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])')"
  printf 'git+https://github.com/Triotek-Ltd/3plug-pro.git@%s#subdirectory=cli' "${latest_tag}"
}

if [ "$(id -u)" -ne 0 ]; then
  echo "Run this script as root or with sudo." >&2
  exit 1
fi

if ! id "${THREEPLUG_USER}" >/dev/null 2>&1; then
  echo "Operator user does not exist: ${THREEPLUG_USER}" >&2
  echo "Run bootstrap first." >&2
  exit 1
fi

GIT_USER_NAME="$(sudo -H -u "${THREEPLUG_USER}" git config --global --get user.name || true)"
GIT_USER_EMAIL="$(sudo -H -u "${THREEPLUG_USER}" git config --global --get user.email || true)"

if [ -z "${GIT_USER_NAME}" ] || [ -z "${GIT_USER_EMAIL}" ]; then
  echo "Git identity is not configured for ${THREEPLUG_USER}." >&2
  echo "Run the Git setup step before updating or installing 3plug." >&2
  echo "Suggested command:" >&2
  echo "  curl -fsSL https://raw.githubusercontent.com/Triotek-Ltd/3plug-pro/main/scripts/linux/configure_3plug_git.sh -o /tmp/configure_3plug_git.sh" >&2
  echo "  sudo bash /tmp/configure_3plug_git.sh" >&2
  exit 1
fi

if [ "${THREEPLUG_PACKAGE_URL}" = "latest" ]; then
  echo "Resolving latest published 3plug release"
  THREEPLUG_PACKAGE_URL="$(resolve_latest_package_url)"
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

echo "Refreshing global 3plug commands in ${THREEPLUG_GLOBAL_BIN_DIR}"
install -d "${THREEPLUG_GLOBAL_BIN_DIR}"
ln -sf "${THREEPLUG_VENV}/bin/3plug" "${THREEPLUG_GLOBAL_BIN_DIR}/3plug"
ln -sf "${THREEPLUG_VENV}/bin/3plug-pro" "${THREEPLUG_GLOBAL_BIN_DIR}/3plug-pro"

cat <<EOF

Update complete.

Updated package source:

  ${THREEPLUG_PACKAGE_URL}

Recommended verification as ${THREEPLUG_USER}:

  git config --global --get user.name
  git config --global --get user.email
  3plug --help
  3plug server preflight

EOF
