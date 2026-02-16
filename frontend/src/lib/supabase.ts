/**
 * Supabase Client
 *
 * Browser-side Supabase client for authentication and data operations.
 */

import { createClient } from '@supabase/supabase-js';
import { env } from '@/config';

if (!env.supabaseUrl || !env.supabaseAnonKey) {
  console.warn(
    'Supabase URL or Anon Key not configured. Auth features will not work. ' +
    'Set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY in your .env.local file.'
  );
}

export const supabase = createClient(
  env.supabaseUrl || 'http://localhost:54321',
  env.supabaseAnonKey || 'placeholder-key',
  {
    auth: {
      autoRefreshToken: true,
      persistSession: true,
      detectSessionInUrl: true,
    },
  }
);
