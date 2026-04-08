#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_TARGET_STACK="${THREEPLUG_TARGET_STACK:-frappe-v16}"
THREEPLUG_INSTALL_PRODUCTION_TOOLS="${THREEPLUG_INSTALL_PRODUCTION_TOOLS:-0}"

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
  curl \
  git \
  redis-server \
  mariadb-server \
  mariadb-client \
  libmariadb-dev \
  pkg-config \
  xvfb \
  libfontconfig1 \
  cron

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
  - Verify exact versions from preflight before creating a Bench runtime.

EOF
