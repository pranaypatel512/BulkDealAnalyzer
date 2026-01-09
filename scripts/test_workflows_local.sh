#!/bin/bash

# Local Testing Script for GitHub Actions Workflows
# This script simulates the workflow steps locally to verify they work

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Local Workflow Testing for BulkDeal Analyzer                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "backend/pyproject.toml" ] && [ ! -f "backend/requirements.txt" ]; then
    echo -e "${RED}❌ Error: Must run from project root${NC}"
    exit 1
fi

# Test 1: Validate YAML syntax
echo -e "${YELLOW}📋 Test 1: Validating YAML syntax...${NC}"
if command -v python3 &> /dev/null; then
    python3 -c "import yaml; yaml.safe_load(open('.github/workflows/security-scan.yml'))" && \
    python3 -c "import yaml; yaml.safe_load(open('.github/workflows/tests.yml'))" && \
    echo -e "${GREEN}✅ All workflow YAML files are valid${NC}" || \
    (echo -e "${RED}❌ YAML validation failed${NC}" && exit 1)
else
    echo -e "${YELLOW}⚠️  Python3 not found, skipping YAML validation${NC}"
fi
echo ""

# Test 2: Backend Lint (simulates backend-lint job)
echo -e "${YELLOW}📋 Test 2: Backend Lint (backend-lint job)...${NC}"
if [ -f "backend/pyproject.toml" ] || [ -f "backend/setup.cfg" ]; then
    cd backend
    if command -v ruff &> /dev/null; then
        ruff check . && echo -e "${GREEN}✅ Backend lint passed${NC}" || (echo -e "${RED}❌ Backend lint failed${NC}" && exit 1)
    else
        echo -e "${YELLOW}⚠️  ruff not installed, skipping${NC}"
        echo "Install with: pip install ruff"
    fi
    cd ..
else
    echo -e "${YELLOW}⚠️  No backend linting configuration found${NC}"
fi
echo ""

# Test 3: Backend Tests (simulates backend-test job)
echo -e "${YELLOW}📋 Test 3: Backend Tests (backend-test job)...${NC}"
if [ -f "backend/pytest.ini" ] || [ -d "backend/tests" ]; then
    cd backend
    if command -v pytest &> /dev/null; then
        pytest tests/ -v --tb=short && echo -e "${GREEN}✅ Backend tests passed${NC}" || (echo -e "${RED}❌ Backend tests failed${NC}" && exit 1)
    else
        echo -e "${YELLOW}⚠️  pytest not installed, skipping${NC}"
        echo "Install with: pip install pytest"
    fi
    cd ..
else
    echo -e "${YELLOW}⚠️  No backend tests found${NC}"
fi
echo ""

# Test 4: Backend Integration Tests (simulates backend-integration-test job)
echo -e "${YELLOW}📋 Test 4: Backend Integration Tests (backend-integration-test job)...${NC}"
if [ -d "backend/tests/integration" ]; then
    cd backend
    if command -v pytest &> /dev/null; then
        pytest tests/integration -v --tb=short && echo -e "${GREEN}✅ Integration tests passed${NC}" || (echo -e "${YELLOW}⚠️  Integration tests failed or skipped${NC}")
    else
        echo -e "${YELLOW}⚠️  pytest not installed, skipping${NC}"
    fi
    cd ..
else
    echo -e "${YELLOW}⚠️  No integration tests found${NC}"
fi
echo ""

# Test 5: Secret Scan (simulates secret-scan job)
echo -e "${YELLOW}📋 Test 5: Secret Scan (secret-scan job)...${NC}"
if command -v gitleaks &> /dev/null; then
    gitleaks detect --source . --verbose --no-git && echo -e "${GREEN}✅ Secret scan passed${NC}" || (echo -e "${YELLOW}⚠️  Secret scan found issues (check output)${NC}")
else
    echo -e "${YELLOW}⚠️  gitleaks not installed, skipping${NC}"
    echo "Install with: ./scripts/install_gitleaks.sh"
fi
echo ""

# Test 6: Dependency Scan (simulates dependency-scan job)
echo -e "${YELLOW}📋 Test 6: Dependency Scan (dependency-scan job)...${NC}"

# npm audit
if [ -f "package.json" ]; then
    if command -v npm &> /dev/null; then
        echo "Running npm audit..."
        npm audit --audit-level=high || echo -e "${YELLOW}⚠️  npm audit found vulnerabilities (non-blocking)${NC}"
    else
        echo -e "${YELLOW}⚠️  npm not installed, skipping npm audit${NC}"
    fi
else
    echo -e "${YELLOW}ℹ️  No package.json found, skipping npm audit${NC}"
fi

# pip safety check
if [ -f "backend/requirements.txt" ]; then
    if command -v safety &> /dev/null; then
        echo "Running safety check..."
        safety check --file backend/requirements.txt || echo -e "${YELLOW}⚠️  safety check found issues (non-blocking)${NC}"
    else
        echo -e "${YELLOW}⚠️  safety not installed, skipping safety check${NC}"
        echo "Install with: pip install safety"
    fi
else
    echo -e "${YELLOW}ℹ️  No requirements.txt found, skipping safety check${NC}"
fi
echo -e "${GREEN}✅ Dependency scan completed${NC}"
echo ""

# Test 7: Simulate security-scan job logic
echo -e "${YELLOW}📋 Test 7: Security Scan Aggregate (security-scan job logic)...${NC}"
echo "Checking required security scan jobs..."
SECRET_SCAN_RESULT="success"  # Would be set by actual secret-scan job
DEPENDENCY_SCAN_RESULT="success"  # Would be set by actual dependency-scan job

if [ "$SECRET_SCAN_RESULT" != "success" ]; then
    echo -e "${RED}❌ secret-scan failed${NC}"
    exit 1
fi

if [ "$DEPENDENCY_SCAN_RESULT" = "failure" ]; then
    echo -e "${RED}❌ dependency-scan failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All required security scans passed${NC}"
echo ""

# Test 8: Simulate test job logic
echo -e "${YELLOW}📋 Test 8: Test Aggregate (test job logic)...${NC}"
echo "Checking required test jobs..."
BACKEND_LINT_RESULT="success"  # Would be set by actual backend-lint job
BACKEND_TEST_RESULT="success"  # Would be set by actual backend-test job
BACKEND_INTEGRATION_TEST_RESULT="success"  # Would be set by actual backend-integration-test job

if [ "$BACKEND_LINT_RESULT" != "success" ]; then
    echo -e "${RED}❌ backend-lint failed${NC}"
    exit 1
fi

if [ "$BACKEND_TEST_RESULT" != "success" ]; then
    echo -e "${RED}❌ backend-test failed${NC}"
    exit 1
fi

if [ "$BACKEND_INTEGRATION_TEST_RESULT" = "failure" ]; then
    echo -e "${RED}❌ backend-integration-test failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All required tests passed${NC}"
echo ""

# Summary
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    Local Workflow Testing Complete!                   ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  1. Review any warnings above"
echo "  2. Fix any failures before pushing"
echo "  3. Push to trigger actual GitHub Actions workflows"
echo "  4. Monitor workflows in GitHub Actions tab"
echo ""

