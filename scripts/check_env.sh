#!/usr/bin/env bash
set -e

errors=0

check_cmd() {
  cmd=$1
  name=$2
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[ERROR] $name ($cmd) not found in PATH"
    errors=$((errors+1))
  else
    version_output=$($cmd --version 2>&1 | head -n1)
    echo "[OK] $name: $version_output"
  fi
}

echo "Checking required developer tools..."
echo ""

check_cmd git "git"
check_cmd node "node"
check_cmd npm "npm"
check_cmd python "python"
check_cmd docker "docker"
check_cmd docker-compose "docker-compose"

# Check Node.js version (should be >= 18)
if command -v node >/dev/null 2>&1; then
  node_version=$(node --version | sed 's/v//' | cut -d'.' -f1)
  if [ "$node_version" -lt 18 ]; then
    echo "[ERROR] Node.js version must be >= 18 (found v$node_version)"
    errors=$((errors+1))
  fi
fi

# Check Python version (should be >= 3.10)
if command -v python >/dev/null 2>&1; then
  python_version=$(python --version 2>&1 | awk '{print $2}' | cut -d'.' -f1,2)
  python_major=$(echo $python_version | cut -d'.' -f1)
  python_minor=$(echo $python_version | cut -d'.' -f2)
  if [ "$python_major" -lt 3 ] || ([ "$python_major" -eq 3 ] && [ "$python_minor" -lt 10 ]); then
    echo "[ERROR] Python version must be >= 3.10 (found $python_version)"
    errors=$((errors+1))
  fi
fi

echo ""
if [ $errors -gt 0 ]; then
  echo "❌ Please install the missing tools listed above."
  echo "See PREREQUISITES.md for installation instructions."
  exit 2
else
  echo "✅ All required tools present."
  exit 0
fi


