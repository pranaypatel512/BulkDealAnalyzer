-- Cleanup Database - Remove all tables and policies except our migration ones
-- This migration removes old tables/policies from previous projects

-- ============================================================================
-- STEP 1: DROP POLICIES NOT IN OUR MIGRATION
-- ============================================================================

DO $$
DECLARE
    pol RECORD;
    preserve_policies TEXT[] := ARRAY[
        'Users can view own profile',
        'Users can insert own profile',
        'Users can update own profile',
        'Users can delete own profile',
        'Users can view own deals',
        'Users can insert own deals',
        'Users can update own deals',
        'Users can delete own deals'
    ];
BEGIN
    FOR pol IN 
        SELECT schemaname, tablename, policyname 
        FROM pg_policies 
        WHERE schemaname = 'public'
    LOOP
        IF NOT (pol.policyname = ANY(preserve_policies)) THEN
            EXECUTE format('DROP POLICY IF EXISTS %I ON %I.%I', 
                pol.policyname, pol.schemaname, pol.tablename);
            RAISE NOTICE 'Dropped policy: % on %.%', pol.policyname, pol.schemaname, pol.tablename;
        END IF;
    END LOOP;
END $$;

-- ============================================================================
-- STEP 2: DROP TRIGGERS NOT IN OUR MIGRATION
-- ============================================================================

DO $$
DECLARE
    trig RECORD;
BEGIN
    FOR trig IN 
        SELECT tgname, tgrelid::regclass as table_name
        FROM pg_trigger 
        WHERE tgisinternal = false
        AND tgrelid::regclass::text NOT IN ('user_profiles', 'bulk_deals')
        AND tgname NOT IN ('update_user_profiles_updated_at', 'update_bulk_deals_updated_at')
    LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS %I ON %s CASCADE', 
            trig.tgname, trig.table_name);
        RAISE NOTICE 'Dropped trigger: % on %', trig.tgname, trig.table_name;
    END LOOP;
END $$;

-- ============================================================================
-- STEP 3: DROP FUNCTIONS NOT IN OUR MIGRATION
-- ============================================================================

DO $$
DECLARE
    func RECORD;
BEGIN
    FOR func IN 
        SELECT proname, oidvectortypes(proargtypes) as args
        FROM pg_proc 
        WHERE pronamespace = 'public'::regnamespace
        AND proname != 'update_updated_at_column'
    LOOP
        BEGIN
            EXECUTE format('DROP FUNCTION IF EXISTS %I(%s) CASCADE', 
                func.proname, func.args);
            RAISE NOTICE 'Dropped function: %(%)', func.proname, func.args;
        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE 'Could not drop function %(%)', func.proname, func.args;
        END;
    END LOOP;
END $$;

-- ============================================================================
-- STEP 4: DROP TABLES NOT IN OUR MIGRATION
-- ============================================================================

DO $$
DECLARE
    tbl RECORD;
    preserve_tables TEXT[] := ARRAY['user_profiles', 'bulk_deals'];
BEGIN
    FOR tbl IN 
        SELECT tablename 
        FROM pg_tables 
        WHERE schemaname = 'public'
    LOOP
        IF NOT (tbl.tablename = ANY(preserve_tables)) THEN
            BEGIN
                EXECUTE format('DROP TABLE IF EXISTS %I CASCADE', tbl.tablename);
                RAISE NOTICE 'Dropped table: %', tbl.tablename;
            EXCEPTION
                WHEN OTHERS THEN
                    RAISE NOTICE 'Could not drop table %: %', tbl.tablename, SQLERRM;
            END;
        END IF;
    END LOOP;
END $$;

-- ============================================================================
-- STEP 5: DROP VIEWS IN PUBLIC SCHEMA
-- ============================================================================

DO $$
DECLARE
    view_rec RECORD;
BEGIN
    FOR view_rec IN 
        SELECT table_name 
        FROM information_schema.views 
        WHERE table_schema = 'public'
    LOOP
        BEGIN
            EXECUTE format('DROP VIEW IF EXISTS %I CASCADE', view_rec.table_name);
            RAISE NOTICE 'Dropped view: %', view_rec.table_name;
        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE 'Could not drop view %: %', view_rec.table_name, SQLERRM;
        END;
    END LOOP;
END $$;

-- ============================================================================
-- STEP 6: DROP CUSTOM TYPES (if any)
-- ============================================================================

DO $$
DECLARE
    typ RECORD;
BEGIN
    FOR typ IN 
        SELECT typname 
        FROM pg_type 
        WHERE typnamespace = 'public'::regnamespace
        AND typtype = 'c'  -- composite types
        AND typname NOT LIKE 'pg_%'  -- exclude system types
    LOOP
        BEGIN
            EXECUTE format('DROP TYPE IF EXISTS %I CASCADE', typ.typname);
            RAISE NOTICE 'Dropped type: %', typ.typname;
        EXCEPTION
            WHEN OTHERS THEN
                RAISE NOTICE 'Could not drop type %: %', typ.typname, SQLERRM;
        END;
    END LOOP;
END $$;

-- ============================================================================
-- VERIFICATION
-- ============================================================================

DO $$
DECLARE
    tbl_count INT;
    pol_count INT;
BEGIN
    -- Count remaining tables
    SELECT COUNT(*) INTO tbl_count
    FROM pg_tables 
    WHERE schemaname = 'public';
    
    -- Count remaining policies
    SELECT COUNT(*) INTO pol_count
    FROM pg_policies 
    WHERE schemaname = 'public';
    
    RAISE NOTICE '';
    RAISE NOTICE '✅ Cleanup completed!';
    RAISE NOTICE 'Remaining tables: %', tbl_count;
    RAISE NOTICE 'Remaining policies: %', pol_count;
    RAISE NOTICE '';
    RAISE NOTICE 'Expected: 2 tables (user_profiles, bulk_deals)';
    RAISE NOTICE 'Expected: 8 policies (4 per table)';
END $$;

