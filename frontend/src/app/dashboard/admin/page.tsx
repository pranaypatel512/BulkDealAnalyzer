'use client';

import Link from 'next/link';
import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';
import { useProfile } from '@/hooks/useProfile';
import { api } from '@/lib/api';
import { DashboardSidebar } from '@/components/dashboard/DashboardSidebar';

interface DealStats {
  total_deals: number;
  buy_deals: number;
  sell_deals: number;
}

export default function AdminPage() {
  const router = useRouter();
  const { user, signOut, getAccessToken } = useAuth();
  const { isAdmin, loading: profileLoading } = useProfile();
  const [stats, setStats] = useState<DealStats | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchStats = useCallback(async () => {
    try {
      const token = await getAccessToken();
      const data = await api.get<DealStats>('/bulk-deals/stats', token ?? undefined);
      setStats(data);
    } catch {
      setStats(null);
    } finally {
      setLoading(false);
    }
  }, [getAccessToken]);

  useEffect(() => {
    if (profileLoading) return;
    if (!isAdmin) {
      router.replace('/dashboard');
      return;
    }
    fetchStats();
  }, [isAdmin, profileLoading, router, fetchStats]);

  if (profileLoading || !isAdmin) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[var(--color-bg-primary)] flex items-center justify-center">
          <div className="w-10 h-10 border-2 border-[#00d4aa] border-t-transparent rounded-full animate-spin" />
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[var(--color-bg-primary)]">
        <DashboardSidebar user={user} signOut={signOut} />
        <main className="lg:ml-64 p-6">
          <div className="mb-8">
            <div className="flex items-center gap-2 mb-1">
              <h1 className="text-2xl font-bold">Admin</h1>
              <span className="px-2 py-0.5 rounded text-xs font-medium bg-amber-500/20 text-amber-400 border border-amber-500/30">
                Admin panel
              </span>
            </div>
            <p className="text-[var(--color-text-secondary)]">System overview and management.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            <div className="card p-5 border border-[var(--color-border)]">
              <div className="text-sm text-[var(--color-text-muted)] mb-1">Total deals</div>
              <div className="text-2xl font-bold font-mono">
                {loading ? '—' : stats ? stats.total_deals.toLocaleString() : '0'}
              </div>
            </div>
            <div className="card p-5 border border-[var(--color-border)]">
              <div className="text-sm text-[var(--color-text-muted)] mb-1">Buy deals</div>
              <div className="text-2xl font-bold font-mono text-[#00d4aa]">
                {loading ? '—' : stats ? stats.buy_deals.toLocaleString() : '0'}
              </div>
            </div>
            <div className="card p-5 border border-[var(--color-border)]">
              <div className="text-sm text-[var(--color-text-muted)] mb-1">Sell deals</div>
              <div className="text-2xl font-bold font-mono text-[#ff6b6b]">
                {loading ? '—' : stats ? stats.sell_deals.toLocaleString() : '0'}
              </div>
            </div>
            <div className="card p-5 border border-[var(--color-border)] flex items-center justify-center">
              <Link
                href="/dashboard/analytics"
                className="text-[#00d4aa] hover:underline font-medium"
              >
                View bulk deals →
              </Link>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Link
              href="/dashboard/analytics"
              className="card p-6 border border-[var(--color-border)] hover:border-[var(--color-border-hover)] transition-colors block"
            >
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-lg bg-[var(--color-bg-tertiary)] flex items-center justify-center">
                  <svg className="w-5 h-5 text-[var(--color-text-secondary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <h2 className="text-lg font-semibold">Bulk deals</h2>
              </div>
              <p className="text-sm text-[var(--color-text-secondary)]">Browse, filter, and manage bulk deals data. Fetch from NSE or upload CSV.</p>
            </Link>

            <Link
              href="/dashboard/analytics"
              className="card p-6 border border-[var(--color-border)] hover:border-[var(--color-border-hover)] transition-colors block"
            >
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-lg bg-[var(--color-bg-tertiary)] flex items-center justify-center">
                  <svg className="w-5 h-5 text-[var(--color-text-secondary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <h2 className="text-lg font-semibold">Fetch history</h2>
              </div>
              <p className="text-sm text-[var(--color-text-secondary)]">View NSE fetch history and import logs. Available in Analytics (Bulk Deals tab).</p>
            </Link>
          </div>

          <div className="mt-8 p-4 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-sm text-[var(--color-text-muted)]">
            <strong className="text-[var(--color-text-primary)]">Admin note:</strong> User management and system settings can be added here. For now, use Supabase Dashboard for user and database management.
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
