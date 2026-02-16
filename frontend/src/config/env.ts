/**
 * Environment Configuration
 * 
 * Centralized environment variable management with type safety.
 */

export const env = {
  // Application
  appName: process.env.NEXT_PUBLIC_APP_NAME || 'BulkDeal Analyzer',
  appVersion: process.env.NEXT_PUBLIC_APP_VERSION || '0.1.0',
  environment: process.env.NODE_ENV || 'development',

  // API
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  apiVersion: process.env.NEXT_PUBLIC_API_VERSION || 'v1',

  // Supabase
  supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL || '',
  supabaseAnonKey: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '',

  // Feature Flags
  features: {
    analytics: process.env.NEXT_PUBLIC_ENABLE_ANALYTICS === 'true',
    darkMode: true,
  },
} as const;

// Type-safe API URL builder
export const getApiUrl = (path: string): string => {
  const baseUrl = env.apiUrl.replace(/\/$/, '');
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${baseUrl}/api/${env.apiVersion}${cleanPath}`;
};

