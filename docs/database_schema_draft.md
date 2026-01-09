# Database Schema

**Status**: ✅ Complete (Sprint 1)  
**Last Updated**: Sprint 1  
**Migration**: `supabase/migrations/20250101000000_initial_schema.sql`

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

-- Indexes (optimized for common queries)
CREATE INDEX idx_bulk_deals_date ON bulk_deals(date DESC);
CREATE INDEX idx_bulk_deals_symbol ON bulk_deals(symbol);
CREATE INDEX idx_bulk_deals_user_id ON bulk_deals(user_id);
CREATE INDEX idx_bulk_deals_deal_type ON bulk_deals(deal_type);
CREATE INDEX idx_bulk_deals_quantity ON bulk_deals(quantity DESC);
CREATE INDEX idx_bulk_deals_date_symbol ON bulk_deals(date DESC, symbol);
CREATE INDEX idx_bulk_deals_user_date_type ON bulk_deals(user_id, date DESC, deal_type);
```

## Row Level Security (RLS)

**Critical**: RLS is enabled on all tables from day one.

### RLS Policies - User Profiles

- ✅ **SELECT**: Users can view their own profile
- ✅ **INSERT**: Users can insert their own profile
- ✅ **UPDATE**: Users can update their own profile
- ✅ **DELETE**: Users can delete their own profile

### RLS Policies - Bulk Deals

- ✅ **SELECT**: Users can view their own deals
- ✅ **INSERT**: Users can insert their own deals
- ✅ **UPDATE**: Users can update their own deals
- ✅ **DELETE**: Users can delete their own deals

See migration file for complete policy definitions.

## Backup Strategy

**Sprint 0**: Manual backup strategy

1. **Daily**: Export critical tables to CSV
2. **Weekly**: Full database dump
3. **Before migrations**: Snapshot current state

**Future**: Automated backups via Supabase dashboard

## Triggers

### Automatic Timestamp Updates

- `update_updated_at_column()` function updates `updated_at` timestamp on UPDATE
- Applied to both `user_profiles` and `bulk_deals` tables

## Applying Migrations

### Using Supabase CLI

```bash
# Link to your project
supabase link --project-ref your-project-ref

# Apply migrations
supabase db push
```

### Using Supabase Dashboard

1. Go to SQL Editor
2. Copy migration SQL from `supabase/migrations/20250101000000_initial_schema.sql`
3. Paste and execute

### Testing Connection

```bash
# Set DATABASE_URL in .env file first
python scripts/test_db_connection.py
```

## Future Tables (Future Sprints)

These tables will be added in later sprints:

- **watchlists** - User watchlists for tracking symbols
- **watchlist_symbols** - Many-to-many relationship for symbols in watchlists
- **alerts** - User alerts for specific conditions
- **alert_history** - Alert trigger history
- **subscriptions** - Subscription management
- **ai_chat_sessions** - AI analyzer chat sessions
- **ai_chat_messages** - AI analyzer chat messages
- **referrals** - Referral tracking
- **admin_audit_log** - Admin action audit log

## Verification Checklist

After applying migrations, verify:

- [ ] Tables `user_profiles` and `bulk_deals` exist
- [ ] RLS is enabled on both tables
- [ ] All RLS policies are created (8 policies total)
- [ ] All indexes are created (10+ indexes)
- [ ] Triggers for `updated_at` are working
- [ ] Database connection test passes: `python scripts/test_db_connection.py`


