#!/bin/bash

# Clear Branch Protection Rules for BulkDeal Analyzer
# This script removes existing branch protection rules via GitHub CLI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Auto-detect repository from git remote
if git remote get-url origin &> /dev/null; then
    REPO_URL=$(git remote get-url origin)
    # Extract owner/repo from URL (handles both https and ssh formats)
    if [[ "$REPO_URL" =~ github\.com[:/]([^/]+)/([^/]+)(\.git)?$ ]]; then
        REPO_OWNER="${BASH_REMATCH[1]}"
        REPO_NAME="${BASH_REMATCH[2]%.git}"
        REPO_FULL="${REPO_OWNER}/${REPO_NAME}"
    else
        echo -e "${RED}❌ Could not parse repository from git remote${NC}"
        echo "Remote URL: $REPO_URL"
        exit 1
    fi
else
    # Fallback to hardcoded values
    REPO_OWNER="pranaypatel512"
    REPO_NAME="BulkDealAnalyzer"
    REPO_FULL="${REPO_OWNER}/${REPO_NAME}"
fi

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Clear Branch Protection Rules for BulkDeal Analyzer           ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

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

echo -e "${GREEN}✅ GitHub CLI found and authenticated${NC}"
echo ""

# Function to clear branch protection
clear_branch_protection() {
    local branch=$1
    
    echo -e "${YELLOW}Clearing protection for '${branch}' branch...${NC}"
    
    # Delete branch protection
    if gh api -X DELETE "repos/${REPO_FULL}/branches/${branch}/protection" &> /dev/null; then
        echo -e "${GREEN}✅ '${branch}' branch protection removed${NC}"
        return 0
    else
        # Check if protection exists
        if gh api "repos/${REPO_FULL}/branches/${branch}/protection" &> /dev/null; then
            echo -e "${RED}❌ Failed to remove '${branch}' branch protection${NC}"
            return 1
        else
            echo -e "${YELLOW}ℹ️  '${branch}' branch has no protection rules${NC}"
            return 0
        fi
    fi
}

# Verify repository access
echo "Verifying repository access..."
echo "Repository: ${REPO_FULL}"
if ! gh repo view "${REPO_FULL}" &> /dev/null; then
    echo -e "${RED}❌ Cannot access repository: ${REPO_FULL}${NC}"
    echo ""
    echo "Please check:"
    echo "  1. Repository exists: https://github.com/${REPO_FULL}"
    echo "  2. You have admin access to the repository"
    echo "  3. GitHub CLI is authenticated: gh auth status"
    echo "  4. Try: gh auth login"
    echo ""
    echo "If repository name is different, update git remote:"
    echo "  git remote set-url origin https://github.com/OWNER/REPO.git"
    exit 1
fi

echo -e "${GREEN}✅ Repository access verified${NC}"
echo ""

# Clear protection for all branches
echo "Clearing branch protection rules..."
echo ""

clear_branch_protection "main"
echo ""

clear_branch_protection "dev"
echo ""

clear_branch_protection "staging"
echo ""

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Branch Protection Rules Cleared!                         ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  1. Run: ./scripts/setup_branch_protection.sh"
echo "  2. Verify: https://github.com/${REPO_FULL}/settings/branches"
echo ""

