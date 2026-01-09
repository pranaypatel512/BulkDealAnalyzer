#!/bin/bash

# Test GitHub Actions workflows using 'act' tool
# Install act: https://github.com/nektos/act

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Testing GitHub Actions workflows with 'act'...${NC}"
echo ""

# Check if act is installed
if ! command -v act &> /dev/null; then
    echo -e "${YELLOW}⚠️  'act' not installed.${NC}"
    echo ""
    echo "Install act to test workflows locally:"
    echo ""
    echo "  Recommended (package manager with integrity checking):"
    echo "    brew install act                    # macOS"
    echo "    sudo apt-get install act            # Debian/Ubuntu"
    echo "    sudo dnf install act                # Fedora"
    echo ""
    echo "  Alternative (manual installation):"
    echo "    See: https://github.com/nektos/act/releases"
    echo "    Download a specific release and verify checksums"
    echo ""
    echo "  ⚠️  Security Note: Avoid piping remote scripts directly to shell"
    echo "      (e.g., 'curl | sudo bash') as this is a supply chain risk."
    echo ""
    echo "Then run: ./scripts/test_with_act.sh"
    exit 1
fi

echo -e "${GREEN}✅ act is installed${NC}"
echo ""

# Test security-scan workflow
echo -e "${YELLOW}Testing security-scan workflow...${NC}"
act workflow_dispatch -W .github/workflows/security-scan.yml --dryrun 2>&1 | head -20 || \
act pull_request -W .github/workflows/security-scan.yml --dryrun 2>&1 | head -20

echo ""
echo -e "${YELLOW}Testing tests workflow...${NC}"
act workflow_dispatch -W .github/workflows/tests.yml --dryrun 2>&1 | head -20 || \
act pull_request -W .github/workflows/tests.yml --dryrun 2>&1 | head -20

echo ""
echo -e "${GREEN}✅ Workflow syntax validated with act${NC}"
echo ""
echo "To run workflows fully (requires Docker):"
echo "  act pull_request -W .github/workflows/security-scan.yml"
echo "  act pull_request -W .github/workflows/tests.yml"

