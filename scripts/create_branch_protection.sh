#!/bin/bash

# Create Branch Protection Rules for BulkDeal Analyzer
# This script creates branch protection rules with correct status check context names

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Create Branch Protection Rules for BulkDeal Analyzer        ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Verify workflows
echo -e "${YELLOW}Step 1: Verifying workflows...${NC}"
if ! ./scripts/verify_workflow_jobs.sh; then
    echo -e "${RED}❌ Workflow verification failed. Please fix issues before proceeding.${NC}"
    exit 1
fi
echo ""

# Step 2: Create rules
echo -e "${YELLOW}Step 2: Creating branch protection rules...${NC}"
if ! ./scripts/setup_branch_protection.sh; then
    echo -e "${RED}❌ Failed to create branch protection rules${NC}"
    exit 1
fi
echo ""

# Step 3: Final verification
echo -e "${YELLOW}Step 3: Final verification...${NC}"
echo ""
echo "Verifying branch protection rules via GitHub API..."
echo ""

# Auto-detect repository from git remote
if git remote get-url origin &> /dev/null; then
    REPO_URL=$(git remote get-url origin)
    if [[ "$REPO_URL" =~ github\.com[:/]([^/]+)/([^/]+)(\.git)?$ ]]; then
        REPO_OWNER="${BASH_REMATCH[1]}"
        REPO_NAME="${BASH_REMATCH[2]%.git}"
        REPO_FULL="${REPO_OWNER}/${REPO_NAME}"
    else
        REPO_FULL="pranaypatel512/BulkDealAnalyzer"
    fi
else
    REPO_FULL="pranaypatel512/BulkDealAnalyzer"
fi

for branch in main dev staging; do
    echo -n "Checking ${branch}... "
    if gh api "repos/${REPO_FULL}/branches/${branch}/protection" &> /dev/null; then
        echo -e "${GREEN}✅ Protected${NC}"
        # Show required checks
        gh api "repos/${REPO_FULL}/branches/${branch}/protection" 2>/dev/null | \
            jq -r '.required_status_checks.contexts[]' 2>/dev/null | \
            sed 's/^/   - /' || true
    else
        echo -e "${RED}❌ Not protected${NC}"
    fi
    echo ""
done

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Branch Protection Rules Created!                        ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  1. Create a test PR to trigger workflows"
echo "  2. Verify status checks appear with correct context names"
echo "  3. Check: https://github.com/${REPO_FULL}/settings/branches"
echo ""
echo "Note: If rules already exist, they will be updated with new settings."
echo "      To clear and recreate, use: ./scripts/recreate_branch_protection.sh"
echo ""

