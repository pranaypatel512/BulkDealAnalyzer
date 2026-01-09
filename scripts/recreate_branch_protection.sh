#!/bin/bash

# Recreate Branch Protection Rules for BulkDeal Analyzer
# This script clears existing rules and recreates them with correct job IDs

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║      Recreate Branch Protection Rules for BulkDeal Analyzer         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Verify workflows
echo -e "${YELLOW}Step 1: Verifying workflows...${NC}"
if ! ./scripts/verify_workflow_jobs.sh; then
    echo -e "${RED}❌ Workflow verification failed. Please fix issues before proceeding.${NC}"
    exit 1
fi
echo ""

# Step 2: Clear existing rules
echo -e "${YELLOW}Step 2: Clearing existing branch protection rules...${NC}"
if ! ./scripts/clear_branch_protection.sh; then
    echo -e "${RED}❌ Failed to clear existing rules${NC}"
    exit 1
fi
echo ""

# Step 3: Wait a moment for GitHub to process
echo -e "${YELLOW}Step 3: Waiting for GitHub to process changes...${NC}"
sleep 2
echo ""

# Step 4: Recreate rules
echo -e "${YELLOW}Step 4: Recreating branch protection rules...${NC}"
if ! ./scripts/setup_branch_protection.sh; then
    echo -e "${RED}❌ Failed to recreate branch protection rules${NC}"
    exit 1
fi
echo ""

# Step 5: Final verification
echo -e "${YELLOW}Step 5: Final verification...${NC}"
echo ""
echo "Verifying branch protection rules via GitHub API..."
echo ""

for branch in main dev staging; do
    echo -n "Checking ${branch}... "
    if gh api "repos/pranaypatel512/BulkDealAnalyzer/branches/${branch}/protection" &> /dev/null; then
        echo -e "${GREEN}✅ Protected${NC}"
    else
        echo -e "${RED}❌ Not protected${NC}"
    fi
done

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Branch Protection Rules Recreated!                      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  1. Create a test PR to trigger workflows"
echo "  2. Verify status checks appear with job IDs (not full format)"
echo "  3. Check: https://github.com/pranaypatel512/BulkDealAnalyzer/settings/branches"
echo ""

