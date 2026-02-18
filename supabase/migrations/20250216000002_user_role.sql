-- Add role to user_profiles for admin vs user experience
-- Single app: admins see admin panel; users see focused dashboard with watchlist/alerts

ALTER TABLE user_profiles
ADD COLUMN IF NOT EXISTS role VARCHAR(20) NOT NULL DEFAULT 'user'
CHECK (role IN ('user', 'admin'));

CREATE INDEX IF NOT EXISTS idx_user_profiles_role ON user_profiles(role);
COMMENT ON COLUMN user_profiles.role IS 'User role: user (default) or admin for admin panel access';
