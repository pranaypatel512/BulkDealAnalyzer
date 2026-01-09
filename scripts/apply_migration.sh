#!/bin/bash

# Apply Database Migration using Supabase CLI
# This script applies the initial schema migration to Supabase

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Apply Database Migration - Supabase CLI                      ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo -e "${RED}❌ Supabase CLI not found.${NC}"
    echo ""
    echo "Install Supabase CLI:"
    echo ""
    echo "  macOS:"
    echo "    brew install supabase/tap/supabase"
    echo ""
    echo "  Linux:"
    echo "    # Download from: https://github.com/supabase/cli/releases"
    echo "    # Or use npm: npm install -g supabase"
    echo ""
    echo "  Windows:"
    echo "    # Download from: https://github.com/supabase/cli/releases"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Supabase CLI found${NC}"
echo ""

# Check if logged in
if ! supabase projects list &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Supabase CLI.${NC}"
    echo ""
    echo "Please login first:"
    echo "  supabase login"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Logged in to Supabase CLI${NC}"
echo ""

# Check if project is linked
if [ ! -f "supabase/.temp/project-ref" ] && [ -z "$SUPABASE_PROJECT_ID" ]; then
    echo -e "${YELLOW}⚠️  Project not linked.${NC}"
    echo ""
    echo "Link your Supabase project:"
    echo "  supabase link --project-ref your-project-ref"
    echo ""
    echo "You can find your project ref in:"
    echo "  - Supabase dashboard URL: https://supabase.com/dashboard/project/YOUR_PROJECT_REF"
    echo "  - Project settings → General → Reference ID"
    echo ""
    read -p "Enter your project ref (or press Enter to exit): " project_ref
    
    if [ -z "$project_ref" ]; then
        echo "Exiting. Run: supabase link --project-ref YOUR_PROJECT_REF"
        exit 1
    fi
    
    echo ""
    echo "Linking project..."
    supabase link --project-ref "$project_ref"
    echo ""
fi

echo -e "${YELLOW}Step 1: Checking migration status...${NC}"
supabase migration list
echo ""

# Check if migration file exists
MIGRATION_FILE="supabase/migrations/20250101000000_initial_schema.sql"
if [ ! -f "$MIGRATION_FILE" ]; then
    echo -e "${RED}❌ Migration file not found: ${MIGRATION_FILE}${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Migration file found${NC}"
echo ""

# Prompt for confirmation
echo -e "${YELLOW}⚠️  This will apply the migration to your Supabase database.${NC}"
echo ""
read -p "Do you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ] && [ "$confirm" != "y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${YELLOW}Step 2: Applying migration...${NC}"
echo ""

# Apply migration
if supabase db push; then
    echo ""
    echo -e "${GREEN}✅ Migration applied successfully!${NC}"
    echo ""
    
    echo -e "${YELLOW}Step 3: Verifying migration...${NC}"
    echo ""
    
    # List migrations to verify
    supabase migration list
    
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              Migration Applied Successfully!                          ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Verify tables in Supabase dashboard: Table Editor"
    echo "  2. Check RLS policies: Authentication → Policies"
    echo "  3. Test connection: python scripts/test_db_connection.py"
    echo ""
else
    echo ""
    echo -e "${RED}❌ Migration failed${NC}"
    echo ""
    echo "Check the error message above for details."
    echo ""
    echo "Common issues:"
    echo "  - Migration already applied (check migration list)"
    echo "  - Permission errors (check project access)"
    echo "  - SQL syntax errors (check migration file)"
    exit 1
fi

