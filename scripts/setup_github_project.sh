#!/bin/bash

# Setup GitHub Project for BulkDeal Analyzer
# This script creates GitHub Project, milestones, and initial issues

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Setup GitHub Project for BulkDeal Analyzer                  ║${NC}"
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

echo "Repository: ${REPO_FULL}"
echo ""

# Check if GitHub CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ GitHub CLI (gh) not found.${NC}"
    echo ""
    echo "Please install GitHub CLI:"
    echo "  https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${RED}❌ Not authenticated with GitHub CLI.${NC}"
    echo ""
    echo "Please authenticate:"
    echo "  gh auth login"
    exit 1
fi

echo -e "${GREEN}✅ GitHub CLI found and authenticated${NC}"
echo ""

# Step 1: Create Sprint Milestones
echo -e "${YELLOW}Step 1: Creating Sprint Milestones...${NC}"
echo ""

for sprint in "Sprint 1 - Core Infrastructure" "Sprint 2 - Authentication" "Sprint 3 - NSE Data Fetching"; do
    echo -n "Creating milestone '${sprint}'... "
    if gh api "repos/${REPO_FULL}/milestones" \
        -f title="${sprint}" \
        -f state="open" \
        &> /dev/null; then
        echo -e "${GREEN}✅${NC}"
    else
        echo -e "${YELLOW}ℹ️  May already exist${NC}"
    fi
done

echo ""

# Step 2: Create Labels
echo -e "${YELLOW}Step 2: Creating Labels...${NC}"
echo ""

# Function to create label if it doesn't exist
create_label() {
    local name=$1
    local description=$2
    local color=$3
    
    # Check if label exists
    if gh api "repos/${REPO_FULL}/labels/${name}" &> /dev/null; then
        echo -e "${YELLOW}ℹ️  Already exists${NC}"
        return 0
    fi
    
    # Create label
    if gh api "repos/${REPO_FULL}/labels" \
        -f name="${name}" \
        -f description="${description}" \
        -f color="${color}" \
        &> /dev/null; then
        echo -e "${GREEN}✅${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed${NC}"
        return 1
    fi
}

# Sprint labels
for sprint in sprint-1 sprint-2 sprint-3; do
    echo -n "Creating label '${sprint}'... "
    create_label "${sprint}" "Sprint ${sprint:6}" "0E8A16"
done

# Module labels
for module in backend frontend database auth user admin; do
    echo -n "Creating label '${module}'... "
    # Capitalize first letter for description
    desc="${module^} module"
    create_label "${module}" "${desc}" "1D76DB"
done

# Priority labels
echo -n "Creating label 'high-priority'... "
create_label "high-priority" "High priority task" "B60205"
echo -n "Creating label 'medium-priority'... "
create_label "medium-priority" "Medium priority task" "FBCA04"
echo -n "Creating label 'low-priority'... "
create_label "low-priority" "Low priority task" "0E8A16"

# Type labels
echo -n "Creating label 'feature'... "
create_label "feature" "New feature" "0E8A16"
echo -n "Creating label 'bugfix'... "
create_label "bugfix" "Bug fix" "B60205"
echo -n "Creating label 'enhancement'... "
create_label "enhancement" "Enhancement" "1D76DB"

echo ""

# Step 3: Create Sprint 1 Issues
echo -e "${YELLOW}Step 3: Creating Sprint 1 Issues...${NC}"
echo ""

# Issue 1: Database Schema
echo "Creating issue: Database Schema & Migrations..."
gh issue create \
    --title "Database Schema & Migrations" \
    --body "## Task
Complete database schema for all tables and create Supabase migrations.

## Acceptance Criteria
- [ ] All tables designed and documented
- [ ] Supabase migrations created
- [ ] RLS policies implemented
- [ ] Database connection tested
- [ ] Migration rollback tested

## Technical Details
- Reference: \`docs/database_schema_draft.md\`
- Branch: \`feature/database-schema-complete\`
- Estimate: 2-3 days

## Related
- Sprint 1 milestone
- Backend core module depends on this" \
    --milestone "Sprint 1 - Core Infrastructure" \
    --label "sprint-1,backend,database,high-priority,feature" \
    --repo "${REPO_FULL}"

echo ""

# Issue 2: Backend Core Module
echo "Creating issue: Backend Core Module..."
gh issue create \
    --title "Backend Core Module Complete" \
    --body "## Task
Complete backend core module structure with proper organization.

## Acceptance Criteria
- [ ] Module structure organized (auth, user, admin, shared)
- [ ] Database connection setup
- [ ] Models defined
- [ ] Basic API structure
- [ ] Tests written

## Technical Details
- Branch: \`feature/backend-core-complete\`
- Estimate: 2-3 days
- Depends on: Database Schema

## Related
- Sprint 1 milestone" \
    --milestone "Sprint 1 - Core Infrastructure" \
    --label "sprint-1,backend,high-priority,feature" \
    --repo "${REPO_FULL}"

echo ""

# Issue 3: Frontend Core Setup
echo "Creating issue: Frontend Core Setup..."
gh issue create \
    --title "Frontend Core Setup (Next.js)" \
    --body "## Task
Initialize Next.js 14+ with App Router and setup basic structure.

## Acceptance Criteria
- [ ] Next.js 14+ initialized with App Router
- [ ] TypeScript configured
- [ ] Tailwind CSS setup
- [ ] Module structure created
- [ ] Basic routing setup

## Technical Details
- Branch: \`feature/frontend-core-setup\`
- Estimate: 2-3 days

## Related
- Sprint 1 milestone" \
    --milestone "Sprint 1 - Core Infrastructure" \
    --label "sprint-1,frontend,high-priority,feature" \
    --repo "${REPO_FULL}"

echo ""

# Issue 4: Basic Authentication
echo "Creating issue: Basic Authentication Setup..."
gh issue create \
    --title "Basic Authentication (Supabase Auth)" \
    --body "## Task
Integrate Supabase Auth for basic authentication flow.

## Acceptance Criteria
- [ ] Supabase Auth integrated (backend)
- [ ] Supabase Auth integrated (frontend)
- [ ] Login/Signup pages created
- [ ] Protected routes implemented
- [ ] Auth context created

## Technical Details
- Branch: \`feature/auth-basic-setup\`
- Estimate: 2-3 days
- Depends on: Backend Core, Frontend Core

## Related
- Sprint 1 milestone" \
    --milestone "Sprint 1 - Core Infrastructure" \
    --label "sprint-1,auth,backend,frontend,high-priority,feature" \
    --repo "${REPO_FULL}"

echo ""

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              GitHub Project Setup Complete!                          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  1. Create GitHub Project board manually:"
echo "     https://github.com/${REPO_FULL}/projects/new"
echo ""
echo "  2. Suggested project structure:"
echo "     - 📋 Backlog"
echo "     - 📝 TODO"
echo "     - 🔄 In Progress"
echo "     - 👀 Review"
echo "     - 🧪 Testing"
echo "     - ✅ Done"
echo ""
echo "  3. View created issues:"
echo "     https://github.com/${REPO_FULL}/issues"
echo ""
echo "  4. Start development:"
echo "     git checkout dev"
echo "     git pull origin dev"
echo "     git checkout -b feature/database-schema-complete"
echo ""

