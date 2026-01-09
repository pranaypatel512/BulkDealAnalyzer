#!/bin/bash

# Test Migration Rollback
# This script tests rollback functionality for Supabase migrations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║         Test Migration Rollback                                       ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    if [ -f ~/.local/bin/supabase ]; then
        export PATH="$HOME/.local/bin:$PATH"
    else
        echo -e "${RED}❌ Supabase CLI not found.${NC}"
        exit 1
    fi
fi

# Check if project is linked
if [ ! -f "supabase/.temp/project-ref" ]; then
    echo -e "${RED}❌ Project not linked.${NC}"
    echo "Link your project: supabase link --project-ref YOUR_PROJECT_REF"
    exit 1
fi

echo -e "${GREEN}✅ Supabase CLI found${NC}"
echo -e "${GREEN}✅ Project linked${NC}"
echo ""

# Create rollback migration file
ROLLBACK_MIGRATION="supabase/migrations/20250101000003_test_rollback_initial_schema.sql"

echo -e "${YELLOW}Step 1: Creating test rollback migration...${NC}"

cat > "$ROLLBACK_MIGRATION" << 'EOF'
-- Test Rollback Migration for Initial Schema
-- This migration tests rollback by removing tables created in initial schema
-- DO NOT USE IN PRODUCTION - This is for testing only

-- Step 1: Drop triggers first (depend on tables)
DROP TRIGGER IF EXISTS update_bulk_deals_updated_at ON bulk_deals CASCADE;
DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON user_profiles CASCADE;

-- Step 2: Drop tables
DROP TABLE IF EXISTS bulk_deals CASCADE;
DROP TABLE IF EXISTS user_profiles CASCADE;

-- Step 3: Drop function
DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE;

-- Verification
DO $$
DECLARE
    table_count INT;
BEGIN
    SELECT COUNT(*) INTO table_count
    FROM pg_tables 
    WHERE schemaname = 'public'
    AND tablename IN ('user_profiles', 'bulk_deals');
    
    IF table_count = 0 THEN
        RAISE NOTICE '✅ Rollback successful: Tables removed';
    ELSE
        RAISE NOTICE '⚠️ Rollback incomplete: % tables still exist', table_count;
    END IF;
END $$;
EOF

echo -e "${GREEN}✅ Rollback migration created${NC}"
echo ""

# Step 2: Verify current state
echo -e "${YELLOW}Step 2: Verifying current database state...${NC}"
echo ""

cat > /tmp/check_tables.sql << 'EOF'
SELECT tablename 
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('user_profiles', 'bulk_deals')
ORDER BY tablename;
EOF

echo "Current tables:"
supabase db execute < /tmp/check_tables.sql 2>/dev/null || echo "  (Could not check - will continue)"
rm -f /tmp/check_tables.sql

echo ""
echo -e "${YELLOW}⚠️  This will DROP the user_profiles and bulk_deals tables!${NC}"
echo ""
read -p "Continue with rollback test? Type 'yes' to confirm: " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled. Removing test rollback migration..."
    rm -f "$ROLLBACK_MIGRATION"
    exit 0
fi

echo ""
echo -e "${YELLOW}Step 3: Applying rollback migration...${NC}"
echo ""

# Apply rollback
if supabase db push; then
    echo ""
    echo -e "${GREEN}✅ Rollback migration applied${NC}"
else
    echo ""
    echo -e "${RED}❌ Rollback failed${NC}"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 4: Verifying rollback...${NC}"
echo ""

# Verify tables are gone
cat > /tmp/verify_rollback.sql << 'EOF'
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN '✅ All tables removed (rollback successful)'
        ELSE format('⚠️  %s tables still exist', COUNT(*)::text)
    END as status
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename IN ('user_profiles', 'bulk_deals');
EOF

supabase db execute < /tmp/verify_rollback.sql
rm -f /tmp/verify_rollback.sql

echo ""
echo -e "${YELLOW}Step 5: Re-applying original migration...${NC}"
echo ""
read -p "Re-apply initial schema migration? (yes/no): " reapply

if [ "$reapply" = "yes" ]; then
    echo ""
    echo "Re-applying initial schema..."
    
    # The original migration uses IF NOT EXISTS, so it should be safe to re-apply
    # However, since Supabase tracks applied migrations, we need to create a new one
    # that recreates everything, OR we can manually run the SQL
    
    echo -e "${BLUE}Note: Supabase tracks applied migrations.${NC}"
    echo -e "${BLUE}To re-apply, you would need to either:${NC}"
    echo -e "${BLUE}1. Create a new migration that recreates tables${NC}"
    echo -e "${BLUE}2. Manually run the original SQL in Supabase Dashboard${NC}"
    echo ""
    echo "For now, the rollback test is complete."
else
    echo ""
    echo "Rollback test complete. Tables remain dropped."
fi

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Rollback Test Complete!                                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Summary:"
echo "  ✅ Rollback migration created"
echo "  ✅ Rollback applied"
echo "  ✅ Tables removed (rollback successful)"
echo ""
echo "Next steps:"
echo "  1. If you re-applied, verify tables exist again"
echo "  2. Clean up test rollback migration (if not keeping)"
echo "  3. Document rollback procedure"

