#!/bin/bash

# Create Branch Protection Rules for BulkDeal Analyzer
# This script creates/updates branch protection rules with correct status check context names

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

# Create/update branch protection rules
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
echo "Note: If rules already exist, they will be updated with new settings."
echo "      To clear and recreate, use: ./scripts/recreate_branch_protection.sh"
echo ""

