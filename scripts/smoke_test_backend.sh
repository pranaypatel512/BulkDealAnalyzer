#!/usr/bin/env bash
# Smoke test backend over HTTP (server must be running).
# Usage: BASE_URL=http://localhost:8000 ./scripts/smoke_test_backend.sh
# Or: ./scripts/smoke_test_backend.sh  (defaults to http://localhost:8000)

set -e
BASE_URL="${BASE_URL:-http://localhost:8000}"
errors=0

check() {
  local method="$1"
  local path="$2"
  local want_status="${3:-200}"
  local desc="${4:-$path}"
  local url="${BASE_URL}${path}"
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url" 2>/dev/null || echo "000")
  if [ "$status" = "$want_status" ]; then
    echo "[OK] $desc -> $status"
  else
    echo "[FAIL] $desc -> got $status, want $want_status"
    errors=$((errors + 1))
  fi
}

echo "Smoke testing backend at $BASE_URL"
echo ""

check GET "/" 200 "root"
check GET "/api/v1/health/" 200 "health"
check GET "/api/v1/bulk-deals/?page=1&page_size=5" 200 "bulk-deals list"
check GET "/api/v1/bulk-deals/export-csv?max_rows=10" 200 "bulk-deals export-csv"

echo ""
if [ $errors -eq 0 ]; then
  echo "All smoke checks passed."
  exit 0
else
  echo "$errors check(s) failed."
  exit 1
fi
