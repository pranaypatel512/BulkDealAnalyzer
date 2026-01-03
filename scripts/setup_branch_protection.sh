#!/bin/bash

# Setup Branch Protection Rules for BulkDeal Analyzer
# This script configures branch protection rules via GitHub CLI or API

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Repository information
REPO_OWNER="pranaypatel512"
REPO_NAME="BulkDealAnalyzer"
REPO_FULL="${REPO_OWNER}/${REPO_NAME}"

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Branch Protection Setup for BulkDeal Analyzer                ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}⚠️  GitHub CLI (gh) not found.${NC}"
    echo ""
    echo "Please install GitHub CLI:"
    echo "  https://cli.github.com/"
    echo ""
    echo "Or configure branch protection manually via GitHub Web UI:"
    echo "  https://github.com/${REPO_FULL}/settings/branches"
    echo ""
    echo "See .github/BRANCH_PROTECTION.md for detailed instructions."
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

# Function to setup branch protection
setup_branch_protection() {
    local branch=$1
    local approvals=$2
    local required_checks=$3
    
    echo -e "${YELLOW}Setting up protection for '${branch}' branch...${NC}"
    
    # Build the protection command
    local cmd="gh api repos/${REPO_FULL}/branches/${branch}/protection"
    local method="PUT"
    
    # Required status checks (comma-separated)
    local checks_json=$(echo "$required_checks" | jq -R -s -c 'split(",") | map(select(length > 0))')
    
    # Build JSON payload
    local payload=$(cat <<EOF
{
  "required_status_checks": {
    "strict": true,
    "contexts": ${checks_json}
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": ${approvals},
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false,
    "require_last_push_approval": false
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "required_linear_history": true,
  "allow_squash_merge": true,
  "allow_merge_commit": false,
  "allow_rebase_merge": true,
  "required_conversation_resolution": true
}
EOF
)
    
    # Make API call
    if gh api -X PUT "repos/${REPO_FULL}/branches/${branch}/protection" \
        --input - <<< "$payload" &> /dev/null; then
        echo -e "${GREEN}✅ '${branch}' branch protection configured${NC}"
        echo "   - Require PR: Yes"
        echo "   - Required approvals: ${approvals}"
        echo "   - Required checks: ${required_checks}"
        echo "   - Force push: Disabled"
        echo "   - Deletion: Disabled"
        return 0
    else
        echo -e "${RED}❌ Failed to configure '${branch}' branch protection${NC}"
        return 1
    fi
}

# Check if jq is installed (needed for JSON processing)
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️  jq not found. Installing...${NC}"
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y jq
    elif command -v brew &> /dev/null; then
        brew install jq
    else
        echo -e "${RED}❌ Please install jq manually: https://stedolan.github.io/jq/download/${NC}"
        exit 1
    fi
fi

# Verify repository access
echo "Verifying repository access..."
if ! gh repo view "${REPO_FULL}" &> /dev/null; then
    echo -e "${RED}❌ Cannot access repository: ${REPO_FULL}${NC}"
    echo "Please check:"
    echo "  1. Repository exists"
    echo "  2. You have admin access"
    echo "  3. GitHub CLI is authenticated"
    exit 1
fi

echo -e "${GREEN}✅ Repository access verified${NC}"
echo ""

# Define required status checks
# Note: These should match your actual CI/CD workflow job names from .github/workflows/tests.yml

# Dev branch checks (basic validation)
DEV_CHECKS="backend-lint,backend-test,test,security-scan"

# Staging branch checks (includes integration tests)
STAGING_CHECKS="backend-lint,backend-test,backend-integration-test,test,security-scan"

# Main branch checks (full validation including integration tests)
MAIN_CHECKS="backend-lint,backend-test,backend-integration-test,test,security-scan"

echo "Setting up branch protection rules..."
echo ""

# Setup main branch (2 approvals, full checks)
setup_branch_protection "main" 2 "${MAIN_CHECKS}"

echo ""

# Setup dev branch (1 approval, basic checks)
setup_branch_protection "dev" 1 "${DEV_CHECKS}"

echo ""

# Setup staging branch (1 approval, includes integration tests)
setup_branch_protection "staging" 1 "${STAGING_CHECKS}"

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    Branch Protection Setup Complete!                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Summary:"
echo "  ✅ main:    2 approvals, checks: ${MAIN_CHECKS}"
echo "  ✅ dev:     1 approval,  checks: ${DEV_CHECKS}"
echo "  ✅ staging: 1 approval,  checks: ${STAGING_CHECKS}"
echo ""
echo "Required Status Checks:"
echo "  - backend-lint: Backend code linting (Ruff)"
echo "  - backend-test: Backend unit tests (Pytest)"
echo "  - backend-integration-test: Backend integration tests (staging/main only)"
echo "  - test: Combined test status check"
echo "  - security-scan: Secret and dependency scanning"
echo ""
echo "Next steps:"
echo "  1. Verify protection rules: https://github.com/${REPO_FULL}/settings/branches"
echo "  2. Create a test PR to trigger CI workflows (checks will appear after first run)"
echo "  3. Verify CODEOWNERS file exists: .github/CODEOWNERS"
echo ""
echo "Note: The status checks will only appear in GitHub after the first PR"
echo "      triggers the CI/CD workflows. You may need to create a test PR"
echo "      and wait for workflows to complete before all checks are available."
echo ""

