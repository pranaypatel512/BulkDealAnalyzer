#!/bin/bash

# Verify Workflow Job IDs Match Branch Protection Rules
# This script ensures workflow job IDs match what's configured in branch protection

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Workflow Job ID Verification                                 ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Extract job IDs from workflows
echo -e "${YELLOW}📋 Extracting job IDs from workflows...${NC}"
echo ""

SECURITY_SCAN_JOBS=$(grep -E "^  [a-z-]+:" .github/workflows/security-scan.yml | grep -v "^  on:" | sed 's/:$//' | sed 's/^  //' | grep -v "^push$" | sort)
TESTS_JOBS=$(grep -E "^  [a-z-]+:" .github/workflows/tests.yml | grep -v "^  on:" | sed 's/:$//' | sed 's/^  //' | grep -v "^push$" | sort)

echo -e "${GREEN}Security Scan Workflow Jobs:${NC}"
echo "$SECURITY_SCAN_JOBS" | sed 's/^/  - /'
echo ""

echo -e "${GREEN}Tests Workflow Jobs:${NC}"
echo "$TESTS_JOBS" | sed 's/^/  - /'
echo ""

# Extract required checks from branch protection script
echo -e "${YELLOW}📋 Extracting required checks from branch protection script...${NC}"
echo ""

DEV_CHECKS=$(grep '^DEV_CHECKS=' scripts/setup_branch_protection.sh | cut -d'"' -f2 | tr ',' '\n' | sort)
STAGING_CHECKS=$(grep '^STAGING_CHECKS=' scripts/setup_branch_protection.sh | cut -d'"' -f2 | tr ',' '\n' | sort)
MAIN_CHECKS=$(grep '^MAIN_CHECKS=' scripts/setup_branch_protection.sh | cut -d'"' -f2 | tr ',' '\n' | sort)

echo -e "${GREEN}Dev Branch Required Checks:${NC}"
echo "$DEV_CHECKS" | sed 's/^/  - /'
echo ""

echo -e "${GREEN}Staging Branch Required Checks:${NC}"
echo "$STAGING_CHECKS" | sed 's/^/  - /'
echo ""

echo -e "${GREEN}Main Branch Required Checks:${NC}"
echo "$MAIN_CHECKS" | sed 's/^/  - /'
echo ""

# Verify all required checks exist in workflows
echo -e "${YELLOW}📋 Verifying all required checks exist in workflows...${NC}"
echo ""

ALL_WORKFLOW_JOBS=$(echo -e "$SECURITY_SCAN_JOBS\n$TESTS_JOBS" | sort -u)
ALL_REQUIRED_CHECKS=$(echo -e "$DEV_CHECKS\n$STAGING_CHECKS\n$MAIN_CHECKS" | sort -u)

ERRORS=0

for check in $ALL_REQUIRED_CHECKS; do
    if echo "$ALL_WORKFLOW_JOBS" | grep -q "^${check}$"; then
        echo -e "${GREEN}✅ ${check} exists in workflows${NC}"
    else
        echo -e "${RED}❌ ${check} NOT FOUND in workflows${NC}"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""

# Check for jobs in workflows that aren't required
echo -e "${YELLOW}📋 Checking for workflow jobs not in branch protection...${NC}"
echo ""

for job in $ALL_WORKFLOW_JOBS; do
    if echo "$ALL_REQUIRED_CHECKS" | grep -q "^${job}$"; then
        echo -e "${GREEN}✅ ${job} is required${NC}"
    else
        echo -e "${YELLOW}⚠️  ${job} exists in workflows but is not required in branch protection${NC}"
    fi
done

echo ""

# Summary
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    ✅ Verification Passed!                            ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "All required checks match workflow job IDs."
    exit 0
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                    ❌ Verification Failed!                            ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Found $ERRORS mismatch(es). Please update branch protection rules."
    exit 1
fi

