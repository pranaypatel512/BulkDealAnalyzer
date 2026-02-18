'use client';

import { useCallback, useEffect, useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';

export interface UserProfile {
  id: string;
  user_id: string;
  email: string;
  full_name: string | null;
  subscription_tier: string;
  role: 'user' | 'admin';
  created_at?: string;
  updated_at?: string;
}

export function useProfile() {
  const { getAccessToken } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProfile = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const token = await getAccessToken();
      if (!token) {
        setProfile(null);
        return;
      }
      const data = await api.get<UserProfile>('/profile/', token);
      setProfile({
        ...data,
        role: (data.role === 'admin' ? 'admin' : 'user') as 'user' | 'admin',
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load profile');
      setProfile(null);
    } finally {
      setLoading(false);
    }
  }, [getAccessToken]);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  const isAdmin = profile?.role === 'admin';

  return { profile, loading, error, refetch: fetchProfile, isAdmin };
}
