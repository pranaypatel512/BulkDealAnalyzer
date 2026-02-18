-- Watchlist & Alerts Tables
-- Users can track symbols and set up alerts for bulk deal activity

-- Watchlist items
CREATE TABLE IF NOT EXISTS watchlist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    notes TEXT,
    alert_on_buy BOOLEAN NOT NULL DEFAULT true,
    alert_on_sell BOOLEAN NOT NULL DEFAULT true,
    min_quantity INTEGER,
    min_value NUMERIC(18,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, symbol)
);

-- Alerts (triggered notifications)
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    watchlist_id UUID REFERENCES watchlist(id) ON DELETE CASCADE,
    deal_id UUID,
    symbol VARCHAR(20) NOT NULL,
    alert_type VARCHAR(20) NOT NULL DEFAULT 'deal_detected',
    title VARCHAR(255) NOT NULL,
    message TEXT,
    is_read BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_watchlist_user_id ON watchlist(user_id);
CREATE INDEX IF NOT EXISTS idx_watchlist_symbol ON watchlist(symbol);
CREATE INDEX IF NOT EXISTS idx_alerts_user_id ON alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_alerts_is_read ON alerts(user_id, is_read);
CREATE INDEX IF NOT EXISTS idx_alerts_created_at ON alerts(created_at DESC);

-- RLS
ALTER TABLE watchlist ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Users select own watchlist" ON watchlist;
DROP POLICY IF EXISTS "Users insert own watchlist" ON watchlist;
DROP POLICY IF EXISTS "Users update own watchlist" ON watchlist;
DROP POLICY IF EXISTS "Users delete own watchlist" ON watchlist;
DROP POLICY IF EXISTS "Users select own alerts" ON alerts;
DROP POLICY IF EXISTS "Users insert own alerts" ON alerts;
DROP POLICY IF EXISTS "Users update own alerts" ON alerts;
DROP POLICY IF EXISTS "Users delete own alerts" ON alerts;

-- Watchlist: users can only see/modify their own items
CREATE POLICY "Users select own watchlist"
    ON watchlist FOR SELECT
    USING (auth.uid() = user_id);
CREATE POLICY "Users insert own watchlist"
    ON watchlist FOR INSERT
    WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users update own watchlist"
    ON watchlist FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users delete own watchlist"
    ON watchlist FOR DELETE
    USING (auth.uid() = user_id);

-- Alerts: users can only see/modify their own alerts
CREATE POLICY "Users select own alerts"
    ON alerts FOR SELECT
    USING (auth.uid() = user_id);
CREATE POLICY "Users insert own alerts"
    ON alerts FOR INSERT
    WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users update own alerts"
    ON alerts FOR UPDATE
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users delete own alerts"
    ON alerts FOR DELETE
    USING (auth.uid() = user_id);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_watchlist_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS watchlist_updated_at ON watchlist;
CREATE TRIGGER watchlist_updated_at
    BEFORE UPDATE ON watchlist
    FOR EACH ROW
    EXECUTE FUNCTION update_watchlist_timestamp();

COMMENT ON TABLE watchlist IS 'User watchlists for tracking specific stock symbols';
COMMENT ON TABLE alerts IS 'Triggered alerts when watchlist conditions are met';
