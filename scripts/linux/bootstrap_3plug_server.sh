#!/usr/bin/env bash
set -euo pipefail

THREEPLUG_USER="${THREEPLUG_USER:-threeplug}"
THREEPLUG_WORKDIR="${THREEPLUG_WORKDIR:-/opt/3plug-pro}"
THREEPLUG_HOME="${THREEPLUG_HOME:-/home/${THREEPLUG_USER}}"
FIREWALL_AUTO_ENABLE="${FIREWALL_AUTO_ENABLE:-1}"
SSH_UFW_PROFILE="${SSH_UFW_PROFILE:-OpenSSH}"

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
    echo "This bootstrap script currently supports Ubuntu/Debian only. Detected: ${PRETTY_NAME:-unknown}" >&2
    exit 1
    ;;
esac

echo "Preparing minimal host tools."
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y \
  ca-certificates \
  curl \
  git \
  python3 \
  python3-pip \
  python3-venv \
  sudo \
  ufw

if ! id "${THREEPLUG_USER}" >/dev/null 2>&1; then
  echo "Creating operator user: ${THREEPLUG_USER}"
  adduser --disabled-password --gecos "" "${THREEPLUG_USER}"
else
  echo "Operator user already exists: ${THREEPLUG_USER}"
fi

echo "Granting sudo access to ${THREEPLUG_USER}."
usermod -aG sudo "${THREEPLUG_USER}"
echo "If this user needs direct SSH or password-based sudo, set a password or install SSH keys for ${THREEPLUG_USER}."

echo "Creating 3plug workspace: ${THREEPLUG_WORKDIR}"
mkdir -p "${THREEPLUG_WORKDIR}"
chown -R "${THREEPLUG_USER}:${THREEPLUG_USER}" "${THREEPLUG_WORKDIR}"

if command -v ufw >/dev/null 2>&1; then
  echo "Checking firewall."
  ufw allow "${SSH_UFW_PROFILE}"
  if [ "${FIREWALL_AUTO_ENABLE}" = "1" ]; then
    ufw --force enable
  else
    echo "Skipping firewall enable because FIREWALL_AUTO_ENABLE=${FIREWALL_AUTO_ENABLE}."
  fi
  ufw status verbose
fi

cat <<EOF

Bootstrap complete.

Next commands:

  su - ${THREEPLUG_USER}
  cd ${THREEPLUG_WORKDIR}
  python3 -m pip install --user "git+https://github.com/Triotek-Ltd/3plug-pro.git@main#subdirectory=cli"
  export PATH="\$HOME/.local/bin:\$PATH"
  3plug --help
  3plug init
  3plug doctor
  3plug server preflight

EOF
