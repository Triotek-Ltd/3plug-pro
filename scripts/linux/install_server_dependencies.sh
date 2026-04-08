#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_TARGET_STACK="${THREEPLUG_TARGET_STACK:-frappe-v16}"
THREEPLUG_INSTALL_PRODUCTION_TOOLS="${THREEPLUG_INSTALL_PRODUCTION_TOOLS:-0}"
THREEPLUG_GLOBAL_BIN_DIR="${THREEPLUG_GLOBAL_BIN_DIR:-/usr/local/bin}"

publish_global_binary() {
  local source_path="$1"
  local target_name="$2"
  if [ -x "${source_path}" ]; then
    install -d "${THREEPLUG_GLOBAL_BIN_DIR}"
    ln -sf "${source_path}" "${THREEPLUG_GLOBAL_BIN_DIR}/${target_name}"
  fi
}

if [ "$(id -u)" -ne 0 ]; then
  echo "Run this script as root or with sudo." >&2
  exit 1
fi

if [ -r /etc/os-release ]; then
  . /etc/os-release
else
  echo "Cannot detect Linux distribution because /etc/os-release is missing." >&2
  exit 1
fi

case "${ID:-}" in
  ubuntu|debian)
    ;;
  *)
    echo "This dependency installer currently supports Ubuntu/Debian only. Detected: ${PRETTY_NAME:-unknown}" >&2
    exit 1
    ;;
esac

echo "Installing 3plug server dependencies for ${THREEPLUG_TARGET_STACK}"
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  build-essential \
  curl \
  git \
  python3-dev \
  python3-pip \
  python3-venv \
  redis-server \
  mariadb-server \
  mariadb-client \
  libmariadb-dev \
  pkg-config \
  xvfb \
  libfontconfig1 \
  cron \
  wkhtmltopdf

if [ "${THREEPLUG_INSTALL_PRODUCTION_TOOLS}" = "1" ]; then
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
    nginx \
    supervisor \
    fail2ban
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv"
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi
publish_global_binary "/root/.local/bin/uv" "uv"
publish_global_binary "/root/.local/bin/uvx" "uvx"

if ! command -v node >/dev/null 2>&1 && ! command -v nodejs >/dev/null 2>&1; then
  echo "Installing distro nodejs and npm"
  DEBIAN_FRONTEND=noninteractive apt-get install -y nodejs npm
fi

if ! command -v yarn >/dev/null 2>&1; then
  echo "Installing yarn globally with npm"
  npm install -g yarn
fi

cat <<EOF

Dependency install complete.

Recommended verification:

  3plug server preflight

Notes:

  - This script installs the current 3plug dependency foundation for Ubuntu/Debian.
  - wkhtmltopdf is installed from the distro package here; verify the exact version and patched-Qt status from preflight.
  - Verify exact versions from preflight before creating a Bench runtime.

EOF
