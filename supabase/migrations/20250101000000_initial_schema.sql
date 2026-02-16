-- Initial Database Schema Migration
-- Creates core tables: user_profiles, bulk_deals
-- Enables RLS and creates policies
-- Creates indexes for optimal performance

-- ============================================================================
-- USER PROFILES TABLE
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
-- BULK DEALS TABLE
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

-- Indexes for bulk_deals (optimized for common queries)
CREATE INDEX IF NOT EXISTS idx_bulk_deals_date ON bulk_deals(date DESC);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_symbol ON bulk_deals(symbol);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_user_id ON bulk_deals(user_id);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_deal_type ON bulk_deals(deal_type);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_quantity ON bulk_deals(quantity DESC);
CREATE INDEX IF NOT EXISTS idx_bulk_deals_date_symbol ON bulk_deals(date DESC, symbol);

-- Composite index for common filter combinations
CREATE INDEX IF NOT EXISTS idx_bulk_deals_user_date_type ON bulk_deals(user_id, date DESC, deal_type);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE bulk_deals ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- RLS POLICIES - USER PROFILES
-- ============================================================================

-- Users can view their own profile
CREATE POLICY "Users can view own profile"
    ON user_profiles FOR SELECT
    USING (auth.uid() = user_id);

-- Users can insert their own profile
CREATE POLICY "Users can insert own profile"
    ON user_profiles FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile"
    ON user_profiles FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Users can delete their own profile
CREATE POLICY "Users can delete own profile"
    ON user_profiles FOR DELETE
    USING (auth.uid() = user_id);

-- ============================================================================
-- RLS POLICIES - BULK DEALS
-- ============================================================================

-- Anyone can view bulk deals (NSE bulk deal data is public information)
CREATE POLICY "Anyone can view bulk deals"
    ON bulk_deals FOR SELECT
    USING (true);

-- Users can insert their own deals
CREATE POLICY "Users can insert own deals"
    ON bulk_deals FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Users can update their own deals
CREATE POLICY "Users can update own deals"
    ON bulk_deals FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Users can delete their own deals
CREATE POLICY "Users can delete own deals"
    ON bulk_deals FOR DELETE
    USING (auth.uid() = user_id);

-- ============================================================================
-- FUNCTIONS & TRIGGERS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for user_profiles
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for bulk_deals
CREATE TRIGGER update_bulk_deals_updated_at
    BEFORE UPDATE ON bulk_deals
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- COMMENTS (Documentation)
-- ============================================================================

COMMENT ON TABLE user_profiles IS 'User profile information linked to Supabase Auth';
COMMENT ON TABLE bulk_deals IS 'Bulk deals data uploaded/imported by users';
COMMENT ON COLUMN user_profiles.subscription_tier IS 'User subscription level: free, premium, or enterprise';
COMMENT ON COLUMN bulk_deals.date IS 'Date of the bulk deal transaction';
COMMENT ON COLUMN bulk_deals.symbol IS 'Stock symbol (e.g., RELIANCE, TCS)';
COMMENT ON COLUMN bulk_deals.security_name IS 'Full name of the security';
COMMENT ON COLUMN bulk_deals.deal_type IS 'Type of deal: BUY or SELL';
COMMENT ON COLUMN bulk_deals.quantity IS 'Number of shares/units';
COMMENT ON COLUMN bulk_deals.price IS 'Price per share/unit';

