#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_TARGET_STACK="${THREEPLUG_TARGET_STACK:-frappe-v16}"
THREEPLUG_INSTALL_PRODUCTION_TOOLS="${THREEPLUG_INSTALL_PRODUCTION_TOOLS:-0}"
THREEPLUG_GLOBAL_BIN_DIR="${THREEPLUG_GLOBAL_BIN_DIR:-/usr/local/bin}"
THREEPLUG_TARGET_PYTHON_VERSION="${THREEPLUG_TARGET_PYTHON_VERSION:-3.14}"

publish_global_binary() {
  local source_path="$1"
  local target_name="$2"
  local target_path="${THREEPLUG_GLOBAL_BIN_DIR}/${target_name}"
  if [ ! -x "${source_path}" ]; then
    return 0
  fi

  install -d "${THREEPLUG_GLOBAL_BIN_DIR}"
  if [ "${source_path}" = "${target_path}" ]; then
    return 0
  fi

  ln -sf "${source_path}" "${target_path}"
}

disable_apache_if_present() {
  if ! command -v systemctl >/dev/null 2>&1; then
    return 0
  fi

  if systemctl list-unit-files apache2.service >/dev/null 2>&1; then
    echo "Apache detected; stopping and disabling apache2 before enabling nginx"
    systemctl stop apache2 || true
    systemctl disable apache2 || true
  fi
}

find_uv_binary() {
  local candidate
  for candidate in \
    "${THREEPLUG_GLOBAL_BIN_DIR}/uv" \
    "/root/.local/bin/uv" \
    "/usr/local/bin/uv" \
    "/usr/bin/uv"
  do
    if [ -x "${candidate}" ]; then
      printf '%s\n' "${candidate}"
      return 0
    fi
  done
  return 1
}

find_uvx_binary() {
  local candidate
  for candidate in \
    "${THREEPLUG_GLOBAL_BIN_DIR}/uvx" \
    "/root/.local/bin/uvx" \
    "/usr/local/bin/uvx" \
    "/usr/bin/uvx"
  do
    if [ -x "${candidate}" ]; then
      printf '%s\n' "${candidate}"
      return 0
    fi
  done
  return 1
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
  disable_apache_if_present
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
    nginx \
    supervisor \
    fail2ban
  if command -v systemctl >/dev/null 2>&1; then
    systemctl enable nginx supervisor fail2ban || true
    systemctl restart nginx || true
    systemctl restart supervisor || true
    systemctl restart fail2ban || true
  fi
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv"
  env UV_INSTALL_DIR="${THREEPLUG_GLOBAL_BIN_DIR}" sh -c "$(curl -LsSf https://astral.sh/uv/install.sh)"
fi

if [ -L "${THREEPLUG_GLOBAL_BIN_DIR}/uv" ] && [ "$(readlink "${THREEPLUG_GLOBAL_BIN_DIR}/uv")" = "${THREEPLUG_GLOBAL_BIN_DIR}/uv" ]; then
  rm -f "${THREEPLUG_GLOBAL_BIN_DIR}/uv"
fi

if [ -L "${THREEPLUG_GLOBAL_BIN_DIR}/uvx" ] && [ "$(readlink "${THREEPLUG_GLOBAL_BIN_DIR}/uvx")" = "${THREEPLUG_GLOBAL_BIN_DIR}/uvx" ]; then
  rm -f "${THREEPLUG_GLOBAL_BIN_DIR}/uvx"
fi

if uv_path="$(find_uv_binary)"; then
  publish_global_binary "${uv_path}" "uv"
else
  echo "uv installation did not produce a usable uv binary." >&2
  exit 1
fi

if uvx_path="$(find_uvx_binary)"; then
  publish_global_binary "${uvx_path}" "uvx"
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is still not available on PATH after installation." >&2
  exit 1
fi

uv --version >/dev/null 2>&1 || {
  echo "uv was found but could not be executed successfully." >&2
  exit 1
}

echo "Installing managed Python ${THREEPLUG_TARGET_PYTHON_VERSION} with uv"
uv python install "${THREEPLUG_TARGET_PYTHON_VERSION}"
target_python_path="$(uv python find "${THREEPLUG_TARGET_PYTHON_VERSION}")"
if [ -z "${target_python_path}" ] || [ ! -x "${target_python_path}" ]; then
  echo "uv did not provide a usable Python ${THREEPLUG_TARGET_PYTHON_VERSION} interpreter." >&2
  exit 1
fi

publish_global_binary "${target_python_path}" "python${THREEPLUG_TARGET_PYTHON_VERSION}"

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
  - Python ${THREEPLUG_TARGET_PYTHON_VERSION} is installed through uv and linked as python${THREEPLUG_TARGET_PYTHON_VERSION}.
  - When production tools are requested, apache2 is stopped and disabled before nginx is enabled.
  - wkhtmltopdf is installed from the distro package here; verify the exact version and patched-Qt status from preflight.
  - Verify exact versions from preflight before creating a Bench runtime.

EOF
