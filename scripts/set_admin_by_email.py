#!/usr/bin/env python3
"""
Set a user as admin by email (user_profiles.role = 'admin').

Requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (e.g. from backend/.env).
Run from repo root:
  python scripts/set_admin_by_email.py user@example.com
"""

import os
import sys
from pathlib import Path

# Load backend .env so SUPABASE_* are set
backend_dir = Path(__file__).resolve().parent.parent / "backend"
env_file = backend_dir / ".env"
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v

sys.path.insert(0, str(backend_dir))

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/set_admin_by_email.py <email>")
        print("Example: python3 scripts/set_admin_by_email.py admin@example.com")
        sys.exit(1)

    email = sys.argv[1].strip()
    if not email:
        print("Error: provide a non-empty email.")
        sys.exit(1)

    try:
        from app.core.database import get_supabase_admin_client
    except Exception as e:
        print("Error: could not load backend (run from repo root):", e)
        print("Ensure backend/.env has SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.")
        sys.exit(1)

    try:
        client = get_supabase_admin_client()
    except ValueError as e:
        print("Error:", e)
        print("Set SUPABASE_SERVICE_ROLE_KEY in backend/.env (Supabase Dashboard → Settings → API → service_role).")
        sys.exit(1)

    table = client.table("user_profiles")
    result = table.update({"role": "admin"}).eq("email", email).execute()

    if not result.data or len(result.data) == 0:
        print("No user_profiles row found for email:", email)
        print("Have the user sign up once so a profile row exists, then run this again.")
        print("Or set admin via Supabase Dashboard → SQL Editor (see dev-doc/ADMIN_SETUP.md).")
        sys.exit(1)

    print("OK: Set role to 'admin' for:", email)
    print("They can now use the Admin panel and GET /api/v1/admin/status.")

if __name__ == "__main__":
    main()
