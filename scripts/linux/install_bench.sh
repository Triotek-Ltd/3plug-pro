#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_USER="${THREEPLUG_USER:-threeplug}"
THREEPLUG_HOME="${THREEPLUG_HOME:-/home/${THREEPLUG_USER}}"
THREEPLUG_VENV="${THREEPLUG_VENV:-${THREEPLUG_HOME}/.local/share/3plug-pro/venv}"
THREEPLUG_BENCH_SOURCE="${THREEPLUG_BENCH_SOURCE:-git+ssh://git@github.com/Triotek-Ltd/triotek-bench.git}"
THREEPLUG_GLOBAL_BIN_DIR="${THREEPLUG_GLOBAL_BIN_DIR:-/usr/local/bin}"
THREEPLUG_BENCH_GIT_REMOTE="${THREEPLUG_BENCH_SOURCE#git+}"

detect_existing_bench_version() {
  if [ -x "${THREEPLUG_VENV}/bin/bench" ]; then
    sudo -H -u "${THREEPLUG_USER}" "${THREEPLUG_VENV}/bin/bench" --version 2>/dev/null || true
  fi
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
  echo "Run the Git setup step before installing Bench." >&2
  exit 1
fi

if [[ "${THREEPLUG_BENCH_SOURCE}" == git+ssh://* ]] || [[ "${THREEPLUG_BENCH_SOURCE}" == git@github.com:* ]]; then
  echo "Using SSH-based Bench source"
  echo "Make sure the ${THREEPLUG_USER} user has a GitHub SSH key configured and tested."
  sudo -H -u "${THREEPLUG_USER}" git ls-remote --heads "${THREEPLUG_BENCH_GIT_REMOTE}" >/dev/null 2>&1 || {
    echo "Repo access is not ready for ${THREEPLUG_USER}." >&2
    echo "Test with: sudo -H -u ${THREEPLUG_USER} git ls-remote --heads ${THREEPLUG_BENCH_GIT_REMOTE}" >&2
    exit 1
  }
fi

existing_bench_version="$(detect_existing_bench_version)"
if [ -n "${existing_bench_version}" ]; then
  echo "Existing Bench detected: ${existing_bench_version}"
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
  3plug server preflight

EOF
