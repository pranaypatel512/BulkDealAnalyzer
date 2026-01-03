#!/bin/bash

# Verify Workflow Job IDs Match Branch Protection Rules
# This script ensures workflow job IDs match what's configured in branch protection
# Also verifies that jobs don't have 'name' fields (which would change status check context)

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

# Extract job IDs: lines that match job pattern, exclude workflow triggers
SECURITY_SCAN_JOBS=$(grep -E "^  [a-z-]+:" .github/workflows/security-scan.yml | \
    sed 's/:$//' | sed 's/^  //' | \
    grep -v "^on$" | grep -v "^push$" | grep -v "^pull_request$" | grep -v "^branches$" | \
    sort)

TESTS_JOBS=$(grep -E "^  [a-z-]+:" .github/workflows/tests.yml | \
    sed 's/:$//' | sed 's/^  //' | \
    grep -v "^on$" | grep -v "^push$" | grep -v "^pull_request$" | grep -v "^branches$" | \
    sort)

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

# Check for jobs with 'name' fields (which would break status check matching)
echo -e "${YELLOW}📋 Checking for jobs with 'name' fields (should be removed)...${NC}"
echo ""

NAME_ERRORS=0

# Function to check if a job has a name field
check_job_has_name() {
    local workflow_file=$1
    local job_id=$2
    
    # Check if job has a 'name:' field on the line after the job ID
    if awk "/^  ${job_id}:/{getline; if (/\s+name:/) exit 0; else exit 1}" "$workflow_file" 2>/dev/null; then
        return 0  # Has name field
    else
        return 1  # No name field
    fi
}

# Check each required job
for job in $ALL_REQUIRED_CHECKS; do
    HAS_NAME=false
    
    # Check in security-scan workflow
    if grep -q "^  ${job}:" .github/workflows/security-scan.yml; then
        if check_job_has_name ".github/workflows/security-scan.yml" "$job"; then
            HAS_NAME=true
        fi
    fi
    
    # Check in tests workflow
    if grep -q "^  ${job}:" .github/workflows/tests.yml; then
        if check_job_has_name ".github/workflows/tests.yml" "$job"; then
            HAS_NAME=true
        fi
    fi
    
    if [ "$HAS_NAME" = true ]; then
        echo -e "${RED}❌ ${job} has 'name' field - this will break status check matching!${NC}"
        echo -e "   Status check will be '{workflow} / {name} (event)' instead of '${job}'"
        NAME_ERRORS=$((NAME_ERRORS + 1))
    else
        echo -e "${GREEN}✅ ${job} has no 'name' field${NC}"
    fi
done

if [ $NAME_ERRORS -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ All required jobs correctly configured (no 'name' fields)${NC}"
fi

echo ""

# Summary
TOTAL_ERRORS=$((ERRORS + NAME_ERRORS))

if [ $TOTAL_ERRORS -eq 0 ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    ✅ Verification Passed!                            ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "✅ All required checks match workflow job IDs"
    echo "✅ No required jobs have 'name' fields"
    echo ""
    echo "Status check contexts will be:"
    echo "  - backend-lint"
    echo "  - backend-test"
    echo "  - backend-integration-test"
    echo "  - test"
    echo "  - security-scan"
    exit 0
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                    ❌ Verification Failed!                            ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    if [ $ERRORS -gt 0 ]; then
        echo "❌ Found $ERRORS job ID mismatch(es)"
    fi
    if [ $NAME_ERRORS -gt 0 ]; then
        echo "❌ Found $NAME_ERRORS job(s) with 'name' fields that should be removed"
    fi
    echo ""
    echo "Please fix the issues above and run verification again."
    exit 1
fi

