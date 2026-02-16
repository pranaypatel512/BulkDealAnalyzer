-- Fetch History Table
-- Tracks all data fetch operations (NSE API, CSV uploads, etc.)

CREATE TABLE IF NOT EXISTS fetch_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source VARCHAR(50) NOT NULL DEFAULT 'nse_api',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    deals_fetched INTEGER NOT NULL DEFAULT 0,
    deals_imported INTEGER NOT NULL DEFAULT 0,
    deals_skipped INTEGER NOT NULL DEFAULT 0,
    error_message TEXT,
    date_from DATE,
    date_to DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_fetch_history_created_at ON fetch_history(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_fetch_history_status ON fetch_history(status);
CREATE INDEX IF NOT EXISTS idx_fetch_history_source ON fetch_history(source);

-- RLS - service_role can do everything, authenticated users can view
ALTER TABLE fetch_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Anyone can view fetch history"
    ON fetch_history FOR SELECT
    USING (true);

CREATE POLICY "Service role can insert fetch history"
    ON fetch_history FOR INSERT
    WITH CHECK (true);

-- Comments
COMMENT ON TABLE fetch_history IS 'Tracks data fetch operations from NSE/BSE and CSV uploads';
COMMENT ON COLUMN fetch_history.source IS 'Source of data: nse_api, bse_api, csv_upload';
COMMENT ON COLUMN fetch_history.status IS 'Status: pending, success, error';
