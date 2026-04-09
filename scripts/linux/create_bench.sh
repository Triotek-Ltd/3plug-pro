#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_USER="${THREEPLUG_USER:-threeplug}"
THREEPLUG_WORKDIR="${THREEPLUG_WORKDIR:-/opt/3plug-pro}"
THREEPLUG_BENCH_NAME="${THREEPLUG_BENCH_NAME:-production}"
THREEPLUG_BENCH_PATH="${THREEPLUG_BENCH_PATH:-${THREEPLUG_WORKDIR}/benches/${THREEPLUG_BENCH_NAME}}"
THREEPLUG_BENCH_ROOT="${THREEPLUG_BENCH_ROOT:-${THREEPLUG_WORKDIR}/benches}"
THREEPLUG_FRAPPE_PATH="${THREEPLUG_FRAPPE_PATH:-git@github.com:Triotek-Ltd/triotek-frappe.git}"
THREEPLUG_FRAPPE_BRANCH="${THREEPLUG_FRAPPE_BRANCH:-main}"
THREEPLUG_BENCH_PYTHON="${THREEPLUG_BENCH_PYTHON:-/usr/local/bin/python3.14}"
THREEPLUG_BENCH_SKIP_ASSETS="${THREEPLUG_BENCH_SKIP_ASSETS:-0}"
THREEPLUG_BENCH_NO_BACKUPS="${THREEPLUG_BENCH_NO_BACKUPS:-0}"
THREEPLUG_BENCH_DEV="${THREEPLUG_BENCH_DEV:-0}"

if [ "$(id -u)" -ne 0 ]; then
  echo "Run this script as root or with sudo." >&2
  exit 1
fi

if ! id "${THREEPLUG_USER}" >/dev/null 2>&1; then
  echo "Operator user does not exist: ${THREEPLUG_USER}" >&2
  echo "Run bootstrap first." >&2
  exit 1
fi

if ! command -v bench >/dev/null 2>&1; then
  echo "Bench is not installed or not on PATH." >&2
  echo "Run the Bench install step first." >&2
  exit 1
fi

if [ ! -x "${THREEPLUG_BENCH_PYTHON}" ]; then
  echo "Required bench Python is not available: ${THREEPLUG_BENCH_PYTHON}" >&2
  echo "Run the dependency install step again so Python 3.14 is installed through uv." >&2
  exit 1
fi

case "${THREEPLUG_BENCH_PATH}" in
  "${THREEPLUG_BENCH_ROOT}"/*) ;;
  *)
    echo "Bench path must stay within the approved bench root: ${THREEPLUG_BENCH_ROOT}" >&2
    exit 1
    ;;
esac

if [ -e "${THREEPLUG_BENCH_PATH}" ]; then
  echo "Bench path already exists: ${THREEPLUG_BENCH_PATH}" >&2
  echo "Use bench register when bringing an existing bench under 3plug management." >&2
  exit 1
fi

echo "Preparing bench root: ${THREEPLUG_BENCH_ROOT}"
install -d -o "${THREEPLUG_USER}" -g "${THREEPLUG_USER}" "${THREEPLUG_BENCH_ROOT}"

echo "Creating bench ${THREEPLUG_BENCH_NAME} at ${THREEPLUG_BENCH_PATH}"
sudo -H -u "${THREEPLUG_USER}" env \
  BENCH_PATH="${THREEPLUG_BENCH_PATH}" \
  FRAPPE_PATH="${THREEPLUG_FRAPPE_PATH}" \
  FRAPPE_BRANCH="${THREEPLUG_FRAPPE_BRANCH}" \
  BENCH_PYTHON="${THREEPLUG_BENCH_PYTHON}" \
  BENCH_SKIP_ASSETS="${THREEPLUG_BENCH_SKIP_ASSETS}" \
  BENCH_NO_BACKUPS="${THREEPLUG_BENCH_NO_BACKUPS}" \
  BENCH_DEV="${THREEPLUG_BENCH_DEV}" \
  bash -lc '
    set -euo pipefail
    cmd=(bench init "$BENCH_PATH" --frappe-path "$FRAPPE_PATH" --frappe-branch "$FRAPPE_BRANCH" --python "$BENCH_PYTHON")
    if [ "${BENCH_SKIP_ASSETS}" = "1" ]; then
      cmd+=(--skip-assets)
    fi
    if [ "${BENCH_NO_BACKUPS}" = "1" ]; then
      cmd+=(--no-backups)
    fi
    if [ "${BENCH_DEV}" = "1" ]; then
      cmd+=(--dev)
    fi
    "${cmd[@]}"
  '

cat <<EOF

Bench creation complete.

Recommended verification:

  bench --version
  cd ${THREEPLUG_BENCH_PATH}
  bench version

EOF
