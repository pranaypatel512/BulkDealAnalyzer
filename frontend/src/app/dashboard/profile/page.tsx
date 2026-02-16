'use client';

import { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';

interface UserProfile {
  id: string;
  user_id: string;
  email: string;
  full_name: string | null;
  subscription_tier: string;
  created_at: string;
  updated_at: string;
}

export default function ProfilePage() {
  const { user, getAccessToken, signOut } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Form state
  const [fullName, setFullName] = useState('');

  const fetchProfile = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const token = await getAccessToken();
      if (!token) return;

      const data = await api.get<UserProfile>('/profile/', token);
      setProfile(data);
      setFullName(data.full_name ?? '');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load profile');
    } finally {
      setLoading(false);
    }
  }, [getAccessToken]);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSaving(true);
      setError(null);
      setSuccess(null);
      const token = await getAccessToken();
      if (!token) return;

      const data = await api.put<UserProfile>(
        '/profile/',
        { full_name: fullName || null },
        token,
      );
      setProfile(data);
      setSuccess('Profile updated successfully');
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update profile');
    } finally {
      setSaving(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[var(--color-bg-primary)]">
        {/* Sidebar */}
        <aside className="fixed left-0 top-0 bottom-0 w-64 bg-[var(--color-bg-secondary)] border-r border-[var(--color-border)] p-4 hidden lg:block">
          <div className="flex items-center gap-2 mb-8">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#00d4aa] to-[#00b894] flex items-center justify-center">
              <svg className="w-5 h-5 text-[#0a0e14]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <span className="font-bold">BulkDeal<span className="text-[#00d4aa]">Analyzer</span></span>
          </div>

          <nav className="space-y-2">
            <Link href="/dashboard" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Dashboard
            </Link>
            <Link href="/dashboard/deals" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Bulk Deals
            </Link>
          </nav>

          <div className="absolute bottom-4 left-4 right-4 space-y-1">
            {user && (
              <div className="px-4 py-2 text-xs text-[var(--color-text-muted)] truncate">
                {user.email}
              </div>
            )}
            <Link href="/dashboard/profile" className="flex items-center gap-3 px-4 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)]">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Profile
            </Link>
            <button
              onClick={signOut}
              className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-colors w-full"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Sign out
            </button>
          </div>
        </aside>

        {/* Main Content */}
        <main className="lg:ml-64 p-6">
          <div className="max-w-2xl">
            <div className="mb-8">
              <h1 className="text-2xl font-bold">Profile</h1>
              <p className="text-[var(--color-text-secondary)]">Manage your account settings</p>
            </div>

            {/* Alerts */}
            {error && (
              <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
                {error}
              </div>
            )}
            {success && (
              <div className="mb-6 p-4 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400">
                {success}
              </div>
            )}

            {loading ? (
              <div className="card p-8 text-center">
                <div className="w-8 h-8 border-2 border-[#00d4aa] border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                <p className="text-[var(--color-text-secondary)]">Loading profile...</p>
              </div>
            ) : (
              <>
                {/* Account Info (read-only) */}
                <div className="card p-6 mb-6">
                  <h2 className="text-lg font-semibold mb-4">Account Information</h2>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm text-[var(--color-text-muted)] mb-1">Email</label>
                      <div className="px-4 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] text-[var(--color-text-secondary)]">
                        {user?.email}
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm text-[var(--color-text-muted)] mb-1">Plan</label>
                        <div className="px-4 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)]">
                          <span className="inline-flex items-center gap-1.5">
                            <span className={`w-2 h-2 rounded-full ${profile?.subscription_tier === 'premium' ? 'bg-yellow-400' : profile?.subscription_tier === 'enterprise' ? 'bg-purple-400' : 'bg-[#00d4aa]'}`} />
                            <span className="capitalize">{profile?.subscription_tier ?? 'free'}</span>
                          </span>
                        </div>
                      </div>
                      <div>
                        <label className="block text-sm text-[var(--color-text-muted)] mb-1">Member since</label>
                        <div className="px-4 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] text-[var(--color-text-secondary)]">
                          {profile?.created_at
                            ? new Date(profile.created_at).toLocaleDateString('en-IN', { year: 'numeric', month: 'short', day: 'numeric' })
                            : '—'}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Editable Profile */}
                <form onSubmit={handleSave} className="card p-6">
                  <h2 className="text-lg font-semibold mb-4">Personal Information</h2>
                  <div className="space-y-4">
                    <div>
                      <label htmlFor="fullName" className="block text-sm text-[var(--color-text-muted)] mb-1">
                        Full Name
                      </label>
                      <input
                        id="fullName"
                        type="text"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        placeholder="Enter your full name"
                        maxLength={255}
                        className="w-full px-4 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-muted)] focus:outline-none focus:ring-2 focus:ring-[#00d4aa]/50 focus:border-[#00d4aa] transition-colors"
                      />
                    </div>
                  </div>

                  <div className="mt-6 flex items-center gap-3">
                    <button
                      type="submit"
                      disabled={saving}
                      className="px-6 py-2.5 rounded-lg bg-[#00d4aa] text-[#0a0e14] font-medium hover:bg-[#00b894] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {saving ? 'Saving...' : 'Save Changes'}
                    </button>
                    <button
                      type="button"
                      onClick={() => setFullName(profile?.full_name ?? '')}
                      className="px-6 py-2.5 rounded-lg border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] transition-colors"
                    >
                      Reset
                    </button>
                  </div>
                </form>
              </>
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
