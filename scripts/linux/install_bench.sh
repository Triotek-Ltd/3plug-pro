#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_USER="${THREEPLUG_USER:-threeplug}"
THREEPLUG_HOME="${THREEPLUG_HOME:-/home/${THREEPLUG_USER}}"
THREEPLUG_VENV="${THREEPLUG_VENV:-${THREEPLUG_HOME}/.local/share/3plug-pro/venv}"
THREEPLUG_BENCH_SOURCE="${THREEPLUG_BENCH_SOURCE:-git+https://github.com/Triotek-Ltd/triotek-bench.git@main}"
THREEPLUG_GLOBAL_BIN_DIR="${THREEPLUG_GLOBAL_BIN_DIR:-/usr/local/bin}"

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
  echo "Run the Git setup step before installing Bench." >&2
  exit 1
fi

echo "Installing Bench for ${THREEPLUG_USER} from ${THREEPLUG_BENCH_SOURCE}"
sudo -H -u "${THREEPLUG_USER}" bash -lc "
  set -euo pipefail
  \"${THREEPLUG_VENV}/bin/python\" -m pip install --upgrade \"${THREEPLUG_BENCH_SOURCE}\"
"

echo "Publishing global bench command in ${THREEPLUG_GLOBAL_BIN_DIR}"
install -d "${THREEPLUG_GLOBAL_BIN_DIR}"
ln -sf "${THREEPLUG_VENV}/bin/bench" "${THREEPLUG_GLOBAL_BIN_DIR}/bench"

cat <<EOF

Bench install complete.

Recommended verification:

  bench --version
  3plug doctor

EOF
