#!/bin/bash

# Create Branch Protection Rules for BulkDeal Analyzer
# This script ONLY creates branch protection rules (fails if rules already exist)

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

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}⚠️  GitHub CLI (gh) not found.${NC}"
    echo ""
    echo "Please install GitHub CLI:"
    echo "  https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not authenticated with GitHub CLI.${NC}"
    echo ""
    echo "Please authenticate:"
    echo "  gh auth login"
    exit 1
fi

# Check if branch protection already exists
echo -e "${YELLOW}Checking for existing branch protection rules...${NC}"
echo ""

EXISTING_PROTECTION=0
for branch in main dev staging; do
    if gh api "repos/${REPO_FULL}/branches/${branch}/protection" &> /dev/null; then
        echo -e "${RED}❌ '${branch}' branch already has protection rules${NC}"
        EXISTING_PROTECTION=1
    else
        echo -e "${GREEN}✅ '${branch}' branch has no protection rules${NC}"
    fi
done

echo ""

if [ $EXISTING_PROTECTION -eq 1 ]; then
    echo -e "${RED}❌ Cannot create: Branch protection rules already exist${NC}"
    echo ""
    echo "To update existing rules, use:"
    echo "  ./scripts/recreate_branch_protection.sh  (clears and recreates)"
    echo ""
    echo "Or manually update via GitHub Web UI:"
    echo "  https://github.com/${REPO_FULL}/settings/branches"
    exit 1
fi

# Create branch protection rules
echo -e "${YELLOW}Creating branch protection rules...${NC}"
if ! ./scripts/setup_branch_protection.sh; then
    echo -e "${RED}❌ Failed to create branch protection rules${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Branch Protection Rules Created!                        ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

