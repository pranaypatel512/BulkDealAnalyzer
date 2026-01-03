# Database Schema Draft

**Status**: Draft (Sprint 0)  
**Note**: This is an initial draft. Schema will be finalized before Sprint 1.

## Core Tables

### user_profiles

```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    subscription_tier VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id)
);
```

### bulk_deals

```sql
CREATE TABLE bulk_deals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    deal_type VARCHAR(10) NOT NULL CHECK (deal_type IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(15, 2) NOT NULL CHECK (price > 0),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bulk_deals_date ON bulk_deals(date);
CREATE INDEX idx_bulk_deals_symbol ON bulk_deals(symbol);
CREATE INDEX idx_bulk_deals_user_id ON bulk_deals(user_id);
CREATE INDEX idx_bulk_deals_deal_type ON bulk_deals(deal_type);
```

## Row Level Security (RLS)

**Critical**: Enable RLS on all tables from day one.

```sql
-- Enable RLS
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE bulk_deals ENABLE ROW LEVEL SECURITY;

-- User profiles: Users can only see their own profile
CREATE POLICY "Users can view own profile"
    ON user_profiles FOR SELECT
    USING (auth.uid() = user_id);

-- Bulk deals: Users can only see their own deals
CREATE POLICY "Users can view own deals"
    ON bulk_deals FOR SELECT
    USING (auth.uid() = user_id);
```

## Backup Strategy

**Sprint 0**: Manual backup strategy

1. **Daily**: Export critical tables to CSV
2. **Weekly**: Full database dump
3. **Before migrations**: Snapshot current state

**Future**: Automated backups via Supabase dashboard

## Notes

- Schema will be expanded in Sprint 1
- Additional tables: watchlists, alerts, subscriptions, etc.
- RLS policies will be comprehensive
- Indexes will be optimized based on query patterns


