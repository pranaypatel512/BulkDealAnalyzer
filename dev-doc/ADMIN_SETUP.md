# Admin Role Setup (Sprint 8)

Admin access is determined by the `role` column on `user_profiles` (see migration `20250216000002_user_role.sql`). Only users with `role = 'admin'` can call admin API routes (e.g. `/api/v1/admin/status`).

## Prerequisites

- The user must have **signed up at least once** so a row exists in `user_profiles` (created on first login/signup via your app).

---

## If you get: column "role" of relation "user_profiles" does not exist

The `role` column is added by migration `20250216000002_user_role.sql`. If you haven’t applied it (e.g. via `supabase db push`), run this **once** in the Supabase Dashboard → **SQL Editor**:

```sql
-- Add role column (safe to run multiple times)
ALTER TABLE user_profiles
ADD COLUMN IF NOT EXISTS role VARCHAR(20) NOT NULL DEFAULT 'user'
CHECK (role IN ('user', 'admin'));

CREATE INDEX IF NOT EXISTS idx_user_profiles_role ON user_profiles(role);
COMMENT ON COLUMN user_profiles.role IS 'User role: user (default) or admin for admin panel access';
```

Then run the “Set admin by email” or “Set admin by user UUID” SQL below.

---

## Steps to perform (choose one)

### Option A: Script (recommended if you have backend env)

1. Ensure `backend/.env` has:
   - `SUPABASE_URL` (e.g. `https://xxxx.supabase.co`)
   - `SUPABASE_SERVICE_ROLE_KEY` (Supabase Dashboard → **Settings → API** → `service_role` secret)

2. From the **repo root** run:

```bash
python3 scripts/set_admin_by_email.py your-admin@example.com
```

3. You should see: `OK: Set role to 'admin' for: your-admin@example.com`

### Option B: Supabase Dashboard (SQL Editor)

1. Open your project in [Supabase Dashboard](https://supabase.com/dashboard) → **SQL Editor** → New query.

2. **Set admin by email** (use when the user has already signed up and has a `user_profiles` row):

```sql
UPDATE user_profiles
SET role = 'admin'
WHERE email = 'your-admin@example.com';
```

Replace `your-admin@example.com` with the user’s email. Check “Rows affected” (should be 1). If 0, the user has no profile yet—have them sign in once, or use the “By user UUID” method below.

3. **Set admin by user UUID** (use when there is no profile row yet, or you prefer to use the auth user id):

- Go to **Authentication** → **Users** and copy the user’s **UUID** (e.g. `a1b2c3d4-e5f6-7890-abcd-ef1234567890`).
- Run (replace the UUID and email):

```sql
INSERT INTO user_profiles (user_id, email, role)
VALUES ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'your-admin@example.com', 'admin')
ON CONFLICT (user_id) DO UPDATE SET role = 'admin';
```

This creates the profile if missing, or updates `role` to `admin` if the row already exists.

---

## RLS note

- `user_profiles` has RLS: users can only read/update their own row.
- The backend uses the **service role** (admin client) to read `user_profiles.role` for the current user, so the admin check is done server-side and is secure.
- Future admin-only tables (e.g. audit log) can use RLS policies that allow access when the user is an admin (e.g. via a helper that checks `user_profiles.role` for `auth.uid()`).

## Verifying admin access

- **In the app:** Log in as that user → you should see **Admin** in the sidebar → open it to see the admin dashboard and users table.
- **API:** Call `GET /api/v1/admin/status` with the user's Bearer token. If they are admin, you get `200` and `{"data": {"admin": true}}`. If not, you get `403 Forbidden`.
