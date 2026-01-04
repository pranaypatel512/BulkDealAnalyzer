#!/bin/bash

# Setup Branch Protection Rules for BulkDeal Analyzer
# This script configures branch protection rules via GitHub CLI or API

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
    
    # Required status checks (comma-separated)
    # Split by comma, trim whitespace, filter empty strings, create JSON array
    local checks_json=$(echo "$required_checks" | jq -R -r 'split(",") | map(select(length > 0) | gsub("^\\s+|\\s+$"; "")) | map(select(length > 0)) | @json')
    
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

# Define required status checks
# 
# IMPORTANT: These must match the actual job IDs (not display names) from .github/workflows/
# 
# Job IDs in workflows (NEW NAMING - clear and identifiable):
#   CI Tests: ci-backend-lint, ci-backend-test, ci-backend-integration-test, ci-test (aggregate)
#   Security Scan: security-secret-scan, security-dependency-scan, security-scan (aggregate)
# 
# Naming Convention:
#   - ci-* prefix for CI Tests workflow jobs
#   - security-* prefix for Security Scan workflow jobs
#   - Aggregate jobs: ci-test, security-scan
# 
# Strategy: Require both individual jobs AND aggregate jobs for:
#   - Individual jobs: Provide immediate feedback and granular control
#   - Aggregate jobs: Verify overall status and handle dependency logic
# 
# Note: We don't require security-secret-scan or security-dependency-scan individually because
#       security-scan (aggregate) already verifies their results.

# Dev branch checks (basic validation)
# NOTE: GitHub creates status check contexts as "{workflow_name} / {job_id} (event)"
# Required: CI Tests / ci-backend-lint, CI Tests / ci-backend-test, CI Tests / ci-test, Security Scan / security-scan
DEV_CHECKS="CI Tests / ci-backend-lint (pull_request),CI Tests / ci-backend-test (pull_request),CI Tests / ci-test (pull_request),Security Scan / security-scan (pull_request)"

# Staging branch checks (includes integration tests)
# Required: CI Tests / ci-backend-lint, CI Tests / ci-backend-test, CI Tests / ci-backend-integration-test, CI Tests / ci-test, Security Scan / security-scan
STAGING_CHECKS="CI Tests / ci-backend-lint (pull_request),CI Tests / ci-backend-test (pull_request),CI Tests / ci-backend-integration-test (pull_request),CI Tests / ci-test (pull_request),Security Scan / security-scan (pull_request)"

# Main branch checks (full validation including integration tests)
# Required: CI Tests / ci-backend-lint, CI Tests / ci-backend-test, CI Tests / ci-backend-integration-test, CI Tests / ci-test, Security Scan / security-scan
MAIN_CHECKS="CI Tests / ci-backend-lint (pull_request),CI Tests / ci-backend-test (pull_request),CI Tests / ci-backend-integration-test (pull_request),CI Tests / ci-test (pull_request),Security Scan / security-scan (pull_request)"

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
echo "  - ci-backend-lint: Backend code linting (Ruff)"
echo "  - ci-backend-test: Backend unit tests (Pytest)"
echo "  - ci-backend-integration-test: Backend integration tests (staging/main only)"
echo "  - ci-test: Combined test status check (aggregate)"
echo "  - security-scan: Secret and dependency scanning (aggregate)"
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

