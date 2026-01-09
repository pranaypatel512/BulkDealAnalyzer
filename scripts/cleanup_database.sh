#!/bin/bash

# Cleanup Supabase Database
# Removes all tables and policies except those created by our migration
# USE WITH CAUTION - This will delete data!

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Cleanup Supabase Database                                     ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Tables to preserve (from our migration)
PRESERVE_TABLES=("user_profiles" "bulk_deals")

# Policies to preserve (from our migration)
PRESERVE_POLICIES=(
    "Users can view own profile"
    "Users can insert own profile"
    "Users can update own profile"
    "Users can delete own profile"
    "Users can view own deals"
    "Users can insert own deals"
    "Users can update own deals"
    "Users can delete own deals"
)

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    if [ -f ~/.local/bin/supabase ]; then
        export PATH="$HOME/.local/bin:$PATH"
    else
        echo -e "${RED}❌ Supabase CLI not found.${NC}"
        echo ""
        echo "Please install Supabase CLI first:"
        echo "  See: INSTALL_SUPABASE_CLI.md"
        exit 1
    fi
fi

# Check if project is linked
if [ ! -f "supabase/.temp/project-ref" ]; then
    echo -e "${YELLOW}⚠️  Project not linked.${NC}"
    echo ""
    echo "Link your project first:"
    echo "  supabase link --project-ref YOUR_PROJECT_REF"
    exit 1
fi

echo -e "${GREEN}✅ Supabase CLI found${NC}"
echo -e "${GREEN}✅ Project linked${NC}"
echo ""

# WARNING
echo -e "${RED}⚠️  WARNING: This will delete all tables and policies${NC}"
echo -e "${RED}    EXCEPT: user_profiles, bulk_deals, and their policies${NC}"
echo ""
echo -e "${YELLOW}This action cannot be undone!${NC}"
echo ""
echo "Tables that will be preserved:"
for table in "${PRESERVE_TABLES[@]}"; do
    echo "  ✅ ${table}"
done
echo ""
echo "Policies that will be preserved:"
for policy in "${PRESERVE_POLICIES[@]}"; do
    echo "  ✅ ${policy}"
done
echo ""

read -p "Do you want to continue? Type 'yes' to confirm: " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${YELLOW}Step 1: Preparing cleanup migration...${NC}"

# Check if cleanup migration exists
CLEANUP_MIGRATION="supabase/migrations/20250101000001_cleanup_database.sql"
if [ ! -f "$CLEANUP_MIGRATION" ]; then
    echo -e "${RED}❌ Cleanup migration not found: ${CLEANUP_MIGRATION}${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Cleanup migration found${NC}"
echo ""

echo -e "${YELLOW}Step 2: Previewing what will be deleted...${NC}"
echo ""

# Preview tables to be deleted using SQL file
echo -e "${BLUE}Tables that will be deleted:${NC}"
cat > /tmp/preview_tables.sql << 'EOF'
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename NOT IN ('user_profiles', 'bulk_deals')
ORDER BY tablename;
EOF

supabase db execute < /tmp/preview_tables.sql 2>/dev/null || echo "  (No tables to delete or connection issue)"

echo ""
echo -e "${BLUE}Policies that will be deleted:${NC}"
cat > /tmp/preview_policies.sql << 'EOF'
SELECT tablename, policyname 
FROM pg_policies 
WHERE schemaname = 'public'
AND policyname NOT IN (
    'Users can view own profile',
    'Users can insert own profile',
    'Users can update own profile',
    'Users can delete own profile',
    'Users can view own deals',
    'Users can insert own deals',
    'Users can update own deals',
    'Users can delete own deals'
)
ORDER BY tablename, policyname;
EOF

supabase db execute < /tmp/preview_policies.sql 2>/dev/null || echo "  (No policies to delete or connection issue)"
rm -f /tmp/preview_tables.sql /tmp/preview_policies.sql

echo ""
read -p "Continue with cleanup? Type 'yes' again: " confirm2

if [ "$confirm2" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo -e "${YELLOW}Step 3: Executing cleanup migration...${NC}"
echo ""

# Execute cleanup migration
if supabase db push --include-all; then
    echo ""
    echo -e "${GREEN}✅ Cleanup migration applied successfully!${NC}"
else
    echo ""
    echo -e "${RED}❌ Cleanup failed${NC}"
    echo "Check the error message above."
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 4: Verifying remaining tables...${NC}"
cat > /tmp/verify_tables.sql << 'EOF'
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;
EOF
supabase db execute < /tmp/verify_tables.sql
rm -f /tmp/verify_tables.sql

echo ""
echo -e "${YELLOW}Step 5: Verifying remaining policies...${NC}"
cat > /tmp/verify_policies.sql << 'EOF'
SELECT tablename, policyname 
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;
EOF
supabase db execute < /tmp/verify_policies.sql
rm -f /tmp/verify_policies.sql

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Database Cleanup Complete!                               ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "✅ Cleaned up database"
echo "✅ Preserved: user_profiles, bulk_deals, and their policies"
echo ""
echo "Next steps:"
echo "  1. Verify tables in Supabase Dashboard"
echo "  2. Run database connection test: python3 scripts/test_db_connection.py"

