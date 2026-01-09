#!/usr/bin/env python3
"""
Test Database Connection Script

This script tests the database connection to Supabase PostgreSQL database.
Run this after applying migrations to verify everything is working.
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("❌ psycopg2 not installed. Install it with:")
    print("   pip install psycopg2-binary")
    sys.exit(1)


def test_connection():
    """Test database connection and verify schema."""
    
    # Get connection string from environment
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL environment variable not set")
        print("\nSet it in your .env file:")
        print("   DATABASE_URL=postgresql://user:password@host:port/database")
        sys.exit(1)
    
    try:
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(database_url)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        print("✅ Connected successfully!")
        print()
        
        # Test 1: Check if tables exist
        print("📋 Checking tables...")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('user_profiles', 'bulk_deals')
            ORDER BY table_name;
        """)
        tables = [row['table_name'] for row in cur.fetchall()]
        
        expected_tables = ['bulk_deals', 'user_profiles']
        missing_tables = set(expected_tables) - set(tables)
        
        if missing_tables:
            print(f"❌ Missing tables: {', '.join(missing_tables)}")
            return False
        else:
            print(f"✅ All tables exist: {', '.join(tables)}")
        
        # Test 2: Check RLS is enabled
        print("\n🔒 Checking Row Level Security...")
        cur.execute("""
            SELECT tablename, rowsecurity 
            FROM pg_tables 
            WHERE schemaname = 'public' 
            AND tablename IN ('user_profiles', 'bulk_deals');
        """)
        rls_status = cur.fetchall()
        
        all_rls_enabled = all(row['rowsecurity'] for row in rls_status)
        if all_rls_enabled:
            print("✅ RLS is enabled on all tables")
        else:
            print("❌ RLS is not enabled on all tables")
            for row in rls_status:
                status = "✅" if row['rowsecurity'] else "❌"
                print(f"   {status} {row['tablename']}")
            return False
        
        # Test 3: Check policies exist
        print("\n🛡️  Checking RLS policies...")
        cur.execute("""
            SELECT tablename, policyname 
            FROM pg_policies 
            WHERE schemaname = 'public' 
            AND tablename IN ('user_profiles', 'bulk_deals')
            ORDER BY tablename, policyname;
        """)
        policies = cur.fetchall()
        
        if policies:
            print(f"✅ Found {len(policies)} policies:")
            for policy in policies:
                print(f"   - {policy['tablename']}: {policy['policyname']}")
        else:
            print("❌ No RLS policies found")
            return False
        
        # Test 4: Check indexes
        print("\n📊 Checking indexes...")
        cur.execute("""
            SELECT tablename, indexname 
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename IN ('user_profiles', 'bulk_deals')
            ORDER BY tablename, indexname;
        """)
        indexes = cur.fetchall()
        
        if indexes:
            print(f"✅ Found {len(indexes)} indexes:")
            for idx in indexes:
                print(f"   - {idx['tablename']}: {idx['indexname']}")
        else:
            print("⚠️  No indexes found")
        
        # Test 5: Check triggers
        print("\n⚙️  Checking triggers...")
        cur.execute("""
            SELECT tgname, tgrelid::regclass as table_name
            FROM pg_trigger 
            WHERE tgname LIKE '%updated_at%'
            AND tgisinternal = false;
        """)
        triggers = cur.fetchall()
        
        if triggers:
            print(f"✅ Found {len(triggers)} triggers:")
            for trigger in triggers:
                print(f"   - {trigger['table_name']}: {trigger['tgname']}")
        else:
            print("⚠️  No updated_at triggers found")
        
        cur.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ All database checks passed!")
        print("="*60)
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

