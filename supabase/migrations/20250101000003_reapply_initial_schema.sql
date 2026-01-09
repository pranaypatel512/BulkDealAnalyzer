-- Re-apply Initial Schema After Rollback
-- This migration recreates the initial schema after a rollback test
-- Uses IF NOT EXISTS so it's safe to re-run

-- ============================================================================
-- USER PROFILES TABLE (Re-create)
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    subscription_tier VARCHAR(50) DEFAULT 'free' CHECK (subscription_tier IN ('free', 'premium', 'enterprise')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);

-- Indexes for user_profiles
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_subscription_tier ON user_profiles(subscription_tier);

-- ============================================================================
-- BULK DEALS TABLE (Re-create)
-- ============================================================================

CREATE TABLE IF NOT EXISTS bulk_deals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    security_name VARCHAR(255),
    client_name VARCHAR(255) NOT NULL,
    deal_type VARCHAR(10) NOT NULL CHECK (deal_type IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(15, 2) NOT NULL CHECK (price > 0),
    remarks VARCHAR(500),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for bulk_deals
CREATE INDEX IF NOT EXISTS idx_bulk_deals_date ON bulk_deals(date DESC);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_symbol ON bulk_deals(symbol);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_user_id ON bulk_deals(user_id);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_deal_type ON bulk_deals(deal_type);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_quantity ON bulk_deals(quantity DESC);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_date_symbol ON bulk_deals(date DESC, symbol);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_user_date_type ON bulk_deals(user_id, date DESC, deal_type);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE bulk_deals ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- RLS POLICIES - USER PROFILES
-- ============================================================================

-- Drop existing policies if they exist, then recreate
DO $$
BEGIN
    -- Drop user_profiles policies if they exist
    DROP POLICY IF EXISTS "Users can view own profile" ON user_profiles;
    DROP POLICY IF EXISTS "Users can insert own profile" ON user_profiles;
    DROP POLICY IF EXISTS "Users can update own profile" ON user_profiles;
    DROP POLICY IF EXISTS "Users can delete own profile" ON user_profiles;
END $$;

CREATE POLICY "Users can view own profile"
    ON user_profiles FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile"
    ON user_profiles FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own profile"
    ON user_profiles FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own profile"
    ON user_profiles FOR DELETE
    USING (auth.uid() = user_id);

-- ============================================================================
-- RLS POLICIES - BULK DEALS
-- ============================================================================

-- Drop existing policies if they exist, then recreate
DO $$
BEGIN
    -- Drop bulk_deals policies if they exist
    DROP POLICY IF EXISTS "Users can view own deals" ON bulk_deals;
    DROP POLICY IF EXISTS "Users can insert own deals" ON bulk_deals;
    DROP POLICY IF EXISTS "Users can update own deals" ON bulk_deals;
    DROP POLICY IF EXISTS "Users can delete own deals" ON bulk_deals;
END $$;

CREATE POLICY "Users can view own deals"
    ON bulk_deals FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own deals"
    ON bulk_deals FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own deals"
    ON bulk_deals FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own deals"
    ON bulk_deals FOR DELETE
    USING (auth.uid() = user_id);

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop existing triggers if they exist (to avoid conflicts)
DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON user_profiles;
DROP TRIGGER IF EXISTS update_bulk_deals_updated_at ON bulk_deals;

-- Recreate triggers
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bulk_deals_updated_at
    BEFORE UPDATE ON bulk_deals
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- VERIFICATION
-- ============================================================================

DO $$
DECLARE
    table_count INT;
    policy_count INT;
BEGIN
    -- Count tables
    SELECT COUNT(*) INTO table_count
    FROM pg_tables 
    WHERE schemaname = 'public' 
    AND tablename IN ('user_profiles', 'bulk_deals');
    
    -- Count policies
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies 
    WHERE schemaname = 'public'
    AND tablename IN ('user_profiles', 'bulk_deals');
    
    RAISE NOTICE '';
    RAISE NOTICE '✅ Schema re-applied successfully!';
    RAISE NOTICE 'Tables: % (expected: 2)', table_count;
    RAISE NOTICE 'Policies: % (expected: 8)', policy_count;
END $$;

