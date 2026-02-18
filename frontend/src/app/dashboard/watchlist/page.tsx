'use client';

import { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import { DashboardSidebar } from '@/components/dashboard/DashboardSidebar';

interface WatchlistItem {
  id: string;
  user_id: string;
  symbol: string;
  notes: string | null;
  alert_on_buy: boolean;
  alert_on_sell: boolean;
  min_quantity: number | null;
  min_value: number | null;
  created_at: string;
  updated_at: string;
}

export default function WatchlistPage() {
  const { user, signOut, getAccessToken } = useAuth();
  const [items, setItems] = useState<WatchlistItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [symbol, setSymbol] = useState('');
  const [notes, setNotes] = useState('');
  const [adding, setAdding] = useState(false);

  const fetchList = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const token = await getAccessToken();
      const data = await api.get<WatchlistItem[]>('/watchlist/', token ?? undefined);
      setItems(Array.isArray(data) ? data : []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load watchlist');
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [getAccessToken]);

  useEffect(() => {
    fetchList();
  }, [fetchList]);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    const s = symbol.trim().toUpperCase();
    if (!s) return;
    try {
      setAdding(true);
      setError(null);
      const token = await getAccessToken();
      await api.post('/watchlist/', { symbol: s, notes: notes.trim() || undefined }, token ?? undefined);
      setSymbol('');
      setNotes('');
      fetchList();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add symbol');
    } finally {
      setAdding(false);
    }
  };

  const handleRemove = async (itemId: string) => {
    try {
      const token = await getAccessToken();
      await api.delete(`/watchlist/${itemId}`, token ?? undefined);
      fetchList();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to remove');
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[var(--color-bg-primary)]">
        <DashboardSidebar user={user} signOut={signOut} />
        <main className="lg:ml-64 p-6">
          <div className="mb-8">
            <h1 className="text-2xl font-bold">Watchlist</h1>
            <p className="text-[var(--color-text-secondary)]">Track symbols and get notified on bulk deal activity.</p>
          </div>

          {error && (
            <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 flex items-center justify-between">
              <span>{error}</span>
              <button type="button" onClick={() => setError(null)} className="text-sm underline">Dismiss</button>
            </div>
          )}

          <div className="card p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4">Add symbol</h2>
            <form onSubmit={handleAdd} className="flex flex-wrap items-end gap-4">
              <div>
                <label htmlFor="symbol" className="block text-sm text-[var(--color-text-muted)] mb-1">Symbol</label>
                <input
                  id="symbol"
                  type="text"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                  placeholder="e.g. RELIANCE"
                  className="w-40 px-3 py-2 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] focus:outline-none focus:border-[#00d4aa]"
                  maxLength={20}
                />
              </div>
              <div className="flex-1 min-w-[200px]">
                <label htmlFor="notes" className="block text-sm text-[var(--color-text-muted)] mb-1">Notes (optional)</label>
                <input
                  id="notes"
                  type="text"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Optional notes"
                  className="w-full px-3 py-2 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-primary)] placeholder-[var(--color-text-muted)] focus:outline-none focus:border-[#00d4aa]"
                />
              </div>
              <button
                type="submit"
                disabled={adding || !symbol.trim()}
                className="px-4 py-2 rounded-lg bg-[#00d4aa] text-[#0a0e14] font-medium hover:bg-[#00b894] disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {adding ? 'Adding…' : 'Add'}
              </button>
            </form>
          </div>

          <div className="card">
            <div className="p-6 border-b border-[var(--color-border)]">
              <h2 className="text-lg font-semibold">Your watchlist</h2>
              <p className="text-sm text-[var(--color-text-muted)] mt-0.5">Alerts for BUY and SELL are on by default.</p>
            </div>
            {loading ? (
              <div className="p-8 space-y-4">
                {[1, 2, 3].map((i) => (
                  <div key={i} className="shimmer h-12 w-full rounded-lg" />
                ))}
              </div>
            ) : items.length === 0 ? (
              <div className="p-8 text-center text-[var(--color-text-muted)]">
                <p className="mb-2">No symbols in your watchlist yet.</p>
                <p className="text-sm">Add a symbol above to start tracking bulk deal activity.</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-[var(--color-border)]">
                      <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Symbol</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Notes</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Alerts</th>
                      <th className="px-6 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--color-border)]">
                    {items.map((item) => (
                      <tr key={item.id} className="hover:bg-[var(--color-bg-secondary)] transition-colors">
                        <td className="px-6 py-4">
                          <Link href={`/dashboard/analytics?symbol=${encodeURIComponent(item.symbol)}`} className="font-medium text-[#00d4aa] hover:underline">
                            {item.symbol}
                          </Link>
                        </td>
                        <td className="px-6 py-4 text-sm text-[var(--color-text-secondary)] max-w-[200px] truncate">{item.notes || '—'}</td>
                        <td className="px-6 py-4 text-sm">
                          <span className={item.alert_on_buy ? 'text-[#00d4aa]' : 'text-[var(--color-text-muted)]'}>BUY</span>
                          <span className="text-[var(--color-text-muted)] mx-1">/</span>
                          <span className={item.alert_on_sell ? 'text-[#ff6b6b]' : 'text-[var(--color-text-muted)]'}>SELL</span>
                        </td>
                        <td className="px-6 py-4 text-right">
                          <button
                            type="button"
                            onClick={() => handleRemove(item.id)}
                            className="text-sm text-red-400 hover:text-red-300 hover:underline"
                          >
                            Remove
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
