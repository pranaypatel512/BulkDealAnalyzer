# Admin Role Setup (Sprint 8)

Admin access is determined by the `role` column on `user_profiles` (see migration `20250216000002_user_role.sql`). Only users with `role = 'admin'` can call admin API routes (e.g. `/api/v1/admin/status`).

## How to set a user as admin

### Option 1: Supabase Dashboard (SQL Editor)

1. Open your project → **SQL Editor**.
2. Run (replace `YOUR_USER_UUID` with the auth user's UUID from **Authentication → Users**):

```sql
-- Ensure user_profiles row exists, then set role to admin
INSERT INTO user_profiles (user_id, email, role)
VALUES ('YOUR_USER_UUID', 'admin@example.com', 'admin')
ON CONFLICT (user_id) DO UPDATE SET role = 'admin';
```

### Option 2: By email (if you have a function)

If you prefer to look up by email (from `auth.users`):

```sql
UPDATE user_profiles
SET role = 'admin'
WHERE user_id = (SELECT id FROM auth.users WHERE email = 'admin@example.com' LIMIT 1);
```

(Ensure the user has already signed up so a row in `user_profiles` exists, or use the INSERT ... ON CONFLICT above after resolving user_id from auth.users.)

## RLS note

- `user_profiles` has RLS: users can only read/update their own row.
- The backend uses the **service role** (admin client) to read `user_profiles.role` for the current user, so the admin check is done server-side and is secure.
- Future admin-only tables (e.g. audit log) can use RLS policies that allow access when the user is an admin (e.g. via a helper that checks `user_profiles.role` for `auth.uid()`).

## Verifying admin access

- Call `GET /api/v1/admin/status` with the user's Bearer token. If they are admin, you get `200` and `{"data": {"admin": true}}`. If not, you get `403 Forbidden`.
