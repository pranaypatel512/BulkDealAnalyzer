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
check_cmd python3 "python3"
check_cmd docker "docker"
check_cmd docker-compose "docker-compose"

# Check Node.js version (should be >= 25.2.1)
if command -v node >/dev/null 2>&1; then
  node_full_version=$(node --version | sed 's/v//')
  node_major=$(echo $node_full_version | cut -d'.' -f1)
  node_minor=$(echo $node_full_version | cut -d'.' -f2)
  node_patch=$(echo $node_full_version | cut -d'.' -f3)
  
  # Compare with 25.2.1
  if [ "$node_major" -lt 25 ]; then
    echo "[ERROR] Node.js version must be >= 25.2.1 (found v$node_full_version)"
    errors=$((errors+1))
  elif [ "$node_major" -eq 25 ]; then
    if [ "$node_minor" -lt 2 ]; then
      echo "[ERROR] Node.js version must be >= 25.2.1 (found v$node_full_version)"
      errors=$((errors+1))
    elif [ "$node_minor" -eq 2 ] && [ "$node_patch" -lt 1 ]; then
      echo "[ERROR] Node.js version must be >= 25.2.1 (found v$node_full_version)"
      errors=$((errors+1))
    fi
  fi
fi

# Check npm version (should be >= 11.7.0)
if command -v npm >/dev/null 2>&1; then
  npm_full_version=$(npm --version)
  npm_major=$(echo $npm_full_version | cut -d'.' -f1)
  npm_minor=$(echo $npm_full_version | cut -d'.' -f2)
  npm_patch=$(echo $npm_full_version | cut -d'.' -f3)
  
  # Compare with 11.7.0
  if [ "$npm_major" -lt 11 ]; then
    echo "[ERROR] npm version must be >= 11.7.0 (found $npm_full_version)"
    errors=$((errors+1))
  elif [ "$npm_major" -eq 11 ]; then
    if [ "$npm_minor" -lt 7 ]; then
      echo "[ERROR] npm version must be >= 11.7.0 (found $npm_full_version)"
      errors=$((errors+1))
    elif [ "$npm_minor" -eq 7 ] && [ -n "$npm_patch" ] && [ "$npm_patch" -lt 0 ]; then
      echo "[ERROR] npm version must be >= 11.7.0 (found $npm_full_version)"
      errors=$((errors+1))
    fi
  fi
fi

# Check Python version (should be >= 3.13, 3.14 doesn't exist yet - using 3.13+)
# Note: Python 3.14 doesn't exist yet. Latest is 3.13.x. Using 3.13+ as minimum.
if command -v python3 >/dev/null 2>&1; then
  python_version=$(python3 --version 2>&1 | awk '{print $2}')
  python_major=$(echo $python_version | cut -d'.' -f1)
  python_minor=$(echo $python_version | cut -d'.' -f2)
  python_patch=$(echo $python_version | cut -d'.' -f3)
  
  # Compare with 3.13.0 (since 3.14 doesn't exist, using 3.13+)
  if [ "$python_major" -lt 3 ]; then
    echo "[ERROR] Python version must be >= 3.13 (found $python_version)"
    echo "        Note: Python 3.14 doesn't exist yet. Latest is 3.13.x"
    errors=$((errors+1))
  elif [ "$python_major" -eq 3 ] && [ "$python_minor" -lt 13 ]; then
    echo "[ERROR] Python version must be >= 3.13 (found $python_version)"
    echo "        Note: Python 3.14 doesn't exist yet. Latest is 3.13.x"
    errors=$((errors+1))
  fi
fi

# Check Docker version (should be >= 20.10)
if command -v docker >/dev/null 2>&1; then
  docker_version=$(docker --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
  docker_major=$(echo $docker_version | cut -d'.' -f1)
  docker_minor=$(echo $docker_version | cut -d'.' -f2)
  if [ "$docker_major" -lt 20 ] || ([ "$docker_major" -eq 20 ] && [ "$docker_minor" -lt 10 ]); then
    echo "[ERROR] Docker version must be >= 20.10 (found $docker_version)"
    errors=$((errors+1))
  fi
fi

# Check Docker Compose version (should be >= 1.29 or v2.x)
if command -v docker-compose >/dev/null 2>&1; then
  compose_version=$(docker-compose --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
  compose_major=$(echo $compose_version | cut -d'.' -f1)
  compose_minor=$(echo $compose_version | cut -d'.' -f2)
  if [ "$compose_major" -lt 1 ] || ([ "$compose_major" -eq 1 ] && [ "$compose_minor" -lt 29 ]); then
    echo "[ERROR] Docker Compose version must be >= 1.29 (found $compose_version)"
    echo "        Alternatively, use Docker Compose v2.x (docker compose)"
    errors=$((errors+1))
  fi
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  echo "[OK] Docker Compose v2.x (docker compose) detected"
else
  echo "[ERROR] Docker Compose not found (docker-compose or 'docker compose')"
  errors=$((errors+1))
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


