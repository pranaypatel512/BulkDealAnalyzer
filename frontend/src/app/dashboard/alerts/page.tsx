'use client';

import { useCallback, useEffect, useState } from 'react';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import { DashboardSidebar } from '@/components/dashboard/DashboardSidebar';

interface AlertItem {
  id: string;
  user_id: string;
  watchlist_id: string | null;
  deal_id: string | null;
  symbol: string;
  alert_type: string;
  title: string;
  message: string | null;
  is_read: boolean;
  created_at: string;
}

export default function AlertsPage() {
  const { user, signOut, getAccessToken } = useAuth();
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'unread'>('all');

  const fetchAlerts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const token = await getAccessToken();
      const [list, countRes] = await Promise.all([
        api.get<AlertItem[]>(
          `/alerts/?limit=50${filter === 'unread' ? '&is_read=false' : ''}`,
          token ?? undefined,
        ),
        api.get<{ count: number }>('/alerts/unread-count', token ?? undefined),
      ]);
      setAlerts(Array.isArray(list) ? list : []);
      setUnreadCount(countRes?.count ?? 0);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load alerts');
      setAlerts([]);
    } finally {
      setLoading(false);
    }
  }, [getAccessToken, filter]);

  useEffect(() => {
    fetchAlerts();
  }, [fetchAlerts]);

  const markRead = async (alertId: string) => {
    try {
      const token = await getAccessToken();
      await api.post(`/alerts/${alertId}/read`, {}, token ?? undefined);
      setAlerts((prev) => prev.map((a) => (a.id === alertId ? { ...a, is_read: true } : a)));
      setUnreadCount((c) => Math.max(0, c - 1));
    } catch {
      // Non-blocking
    }
  };

  const markAllRead = async () => {
    try {
      const token = await getAccessToken();
      await api.post('/alerts/mark-all-read', {}, token ?? undefined);
      setAlerts((prev) => prev.map((a) => ({ ...a, is_read: true })));
      setUnreadCount(0);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to mark all read');
    }
  };

  const formatDate = (s: string) => {
    const d = new Date(s);
    const now = new Date();
    const sameDay = d.toDateString() === now.toDateString();
    if (sameDay) return d.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
    return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[var(--color-bg-primary)]">
        <DashboardSidebar user={user} signOut={signOut} />
        <main className="lg:ml-64 p-6">
          <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
            <div>
              <h1 className="text-2xl font-bold">Alerts</h1>
              <p className="text-[var(--color-text-secondary)]">Notifications for your watchlist symbols.</p>
            </div>
            <div className="flex items-center gap-2">
              {unreadCount > 0 && (
                <button
                  type="button"
                  onClick={markAllRead}
                  className="px-4 py-2 rounded-lg border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] text-sm transition-colors"
                >
                  Mark all read
                </button>
              )}
              <div className="flex rounded-lg border border-[var(--color-border)] overflow-hidden">
                <button
                  type="button"
                  onClick={() => setFilter('all')}
                  className={`px-4 py-2 text-sm transition-colors ${filter === 'all' ? 'bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)]' : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]'}`}
                >
                  All
                </button>
                <button
                  type="button"
                  onClick={() => setFilter('unread')}
                  className={`px-4 py-2 text-sm transition-colors flex items-center gap-1.5 ${filter === 'unread' ? 'bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)]' : 'text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]'}`}
                >
                  Unread
                  {unreadCount > 0 && (
                    <span className="bg-[#00d4aa] text-[#0a0e14] text-xs font-bold px-1.5 py-0.5 rounded">
                      {unreadCount}
                    </span>
                  )}
                </button>
              </div>
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 flex items-center justify-between">
              <span>{error}</span>
              <button type="button" onClick={() => setError(null)} className="text-sm underline">Dismiss</button>
            </div>
          )}

          <div className="card">
            {loading ? (
              <div className="p-8 space-y-4">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="shimmer h-16 w-full rounded-lg" />
                ))}
              </div>
            ) : alerts.length === 0 ? (
              <div className="p-12 text-center text-[var(--color-text-muted)]">
                <p className="mb-2">No alerts yet.</p>
                <p className="text-sm">Add symbols to your <a href="/dashboard/watchlist" className="text-[#00d4aa] hover:underline">watchlist</a> to receive alerts when bulk deals are detected.</p>
              </div>
            ) : (
              <ul className="divide-y divide-[var(--color-border)]">
                {alerts.map((alert) => (
                  <li
                    key={alert.id}
                    className={`px-6 py-4 flex items-start justify-between gap-4 ${!alert.is_read ? 'bg-[var(--color-bg-tertiary)]/50' : ''}`}
                  >
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="font-medium">{alert.title}</span>
                        <span className="text-xs px-2 py-0.5 rounded bg-[#00d4aa]/20 text-[#00d4aa]">{alert.symbol}</span>
                        {!alert.is_read && (
                          <span className="w-2 h-2 rounded-full bg-[#00d4aa] shrink-0" title="Unread" />
                        )}
                      </div>
                      {alert.message && (
                        <p className="text-sm text-[var(--color-text-secondary)] mt-1">{alert.message}</p>
                      )}
                      <p className="text-xs text-[var(--color-text-muted)] mt-2">{formatDate(alert.created_at)}</p>
                    </div>
                    {!alert.is_read && (
                      <button
                        type="button"
                        onClick={() => markRead(alert.id)}
                        className="shrink-0 text-sm text-[#00d4aa] hover:underline"
                      >
                        Mark read
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
