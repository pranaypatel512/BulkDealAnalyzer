# Install Supabase CLI

## Option 1: Using npm (Recommended for Linux)

If you have Node.js/npm installed:

```bash
npm install -g supabase
```

Verify installation:
```bash
supabase --version
```

## Option 2: Using Homebrew (macOS/Linux)

If you have Homebrew installed:

```bash
brew install supabase/tap/supabase
```

Verify installation:
```bash
supabase --version
```

## Option 3: Download Binary (Linux)

1. Visit: https://github.com/supabase/cli/releases
2. Download the latest `supabase_*_linux_amd64.tar.gz`
3. Extract and move to PATH:

```bash
tar -xzf supabase_*_linux_amd64.tar.gz
sudo mv supabase /usr/local/bin/
chmod +x /usr/local/bin/supabase
```

## Option 4: Using Script (Linux)

```bash
curl -fsSL https://github.com/supabase/cli/releases/latest/download/supabase_linux_amd64.tar.gz -o supabase.tar.gz
tar -xzf supabase.tar.gz
sudo mv supabase /usr/local/bin/
chmod +x /usr/local/bin/supabase
```

## After Installation

1. **Login**:
   ```bash
   supabase login
   ```

2. **Link your project**:
   ```bash
   supabase link --project-ref YOUR_PROJECT_REF
   ```
   
   Find project ref:
   - Dashboard URL: `https://supabase.com/dashboard/project/YOUR_PROJECT_REF`
   - Settings → General → Reference ID

3. **Apply migration**:
   ```bash
   supabase db push
   ```

4. **Or use the helper script**:
   ```bash
   ./scripts/apply_migration.sh
   ```

## Alternative: Use Supabase Dashboard

If you prefer not to install CLI, you can apply the migration via the Supabase Dashboard:

1. Go to: https://supabase.com/dashboard
2. Select your project
3. Navigate to: **SQL Editor**
4. Copy contents of: `supabase/migrations/20250101000000_initial_schema.sql`
5. Paste and click **Run**

