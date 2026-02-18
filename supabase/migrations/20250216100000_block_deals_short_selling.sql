-- Block Deals and Short Selling tables
-- Same structure as bulk_deals; data from NSE snapshot API (BLOCK_DEALS_DATA, short selling)

-- ============================================================================
-- BLOCK DEALS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS block_deals (
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

CREATE INDEX IF NOT EXISTS idx_block_deals_date ON block_deals(date DESC);
CREATE INDEX IF NOT EXISTS idx_block_deals_symbol ON block_deals(symbol);
CREATE INDEX IF NOT EXISTS idx_block_deals_user_id ON block_deals(user_id);
CREATE INDEX IF NOT EXISTS idx_block_deals_deal_type ON block_deals(deal_type);
CREATE INDEX IF NOT EXISTS idx_block_deals_date_symbol ON block_deals(date DESC, symbol);

ALTER TABLE block_deals ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view block deals" ON block_deals;
DROP POLICY IF EXISTS "Users can insert own block deals" ON block_deals;
DROP POLICY IF EXISTS "Users can update own block deals" ON block_deals;
DROP POLICY IF EXISTS "Users can delete own block deals" ON block_deals;

CREATE POLICY "Anyone can view block deals"
    ON block_deals FOR SELECT USING (true);
CREATE POLICY "Users can insert own block deals"
    ON block_deals FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own block deals"
    ON block_deals FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own block deals"
    ON block_deals FOR DELETE USING (auth.uid() = user_id);

DROP TRIGGER IF EXISTS update_block_deals_updated_at ON block_deals;
CREATE TRIGGER update_block_deals_updated_at
    BEFORE UPDATE ON block_deals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- SHORT SELLING DEALS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS short_selling_deals (
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

CREATE INDEX IF NOT EXISTS idx_short_selling_deals_date ON short_selling_deals(date DESC);
CREATE INDEX IF NOT EXISTS idx_short_selling_deals_symbol ON short_selling_deals(symbol);
CREATE INDEX IF NOT EXISTS idx_short_selling_deals_user_id ON short_selling_deals(user_id);
CREATE INDEX IF NOT EXISTS idx_short_selling_deals_date_symbol ON short_selling_deals(date DESC, symbol);

ALTER TABLE short_selling_deals ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Anyone can view short selling deals" ON short_selling_deals;
DROP POLICY IF EXISTS "Users can insert own short selling deals" ON short_selling_deals;
DROP POLICY IF EXISTS "Users can update own short selling deals" ON short_selling_deals;
DROP POLICY IF EXISTS "Users can delete own short selling deals" ON short_selling_deals;

CREATE POLICY "Anyone can view short selling deals"
    ON short_selling_deals FOR SELECT USING (true);
CREATE POLICY "Users can insert own short selling deals"
    ON short_selling_deals FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own short selling deals"
    ON short_selling_deals FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can delete own short selling deals"
    ON short_selling_deals FOR DELETE USING (auth.uid() = user_id);

DROP TRIGGER IF EXISTS update_short_selling_deals_updated_at ON short_selling_deals;
CREATE TRIGGER update_short_selling_deals_updated_at
    BEFORE UPDATE ON short_selling_deals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE block_deals IS 'Block deals data from NSE India (large single trades)';
COMMENT ON TABLE short_selling_deals IS 'Short selling / large deal data from NSE India';
