'use client';

import Link from 'next/link';
import { useCallback, useEffect, useState } from 'react';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';

interface DealStats {
  total_deals: number;
  buy_deals: number;
  sell_deals: number;
}

interface BulkDeal {
  id: string;
  date: string;
  symbol: string;
  security_name: string | null;
  client_name: string;
  deal_type: 'BUY' | 'SELL';
  quantity: number;
  price: number;
  remarks: string | null;
}

interface DealsResponse {
  deals: BulkDeal[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

interface TopSymbol {
  symbol: string;
  total_quantity: number;
  deal_count: number;
  buy_count: number;
  sell_count: number;
}

export default function DashboardPage() {
  const { user, signOut, getAccessToken } = useAuth();
  const [stats, setStats] = useState<DealStats | null>(null);
  const [recentDeals, setRecentDeals] = useState<BulkDeal[]>([]);
  const [topSymbols, setTopSymbols] = useState<TopSymbol[]>([]);
  const [watchlistCount, setWatchlistCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboard = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const token = await getAccessToken();
      const t = token ?? undefined;

      const [statsRes, dealsRes, symbolsRes, watchlistRes] = await Promise.all([
        api.get<DealStats>('/bulk-deals/stats', t),
        api.get<DealsResponse>(
          '/bulk-deals/?page=1&page_size=5&sort_by=date&sort_order=desc',
          t,
        ),
        api.get<TopSymbol[]>('/bulk-deals/analytics/top-symbols?limit=5', t),
        api.get<unknown[]>('/watchlist/', t).catch(() => []),
      ]);

      setStats(statsRes);
      setRecentDeals(dealsRes.deals ?? []);
      setTopSymbols(symbolsRes ?? []);
      setWatchlistCount(Array.isArray(watchlistRes) ? watchlistRes.length : 0);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dashboard');
      setStats(null);
      setRecentDeals([]);
      setTopSymbols([]);
    } finally {
      setLoading(false);
    }
  }, [getAccessToken]);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  const showEncourage = watchlistCount === 0;

  const formatValue = (qty: number, price: number) => {
    const val = qty * price;
    if (val >= 10_000_000) return `₹${(val / 10_000_000).toFixed(1)}Cr`;
    if (val >= 100_000) return `₹${(val / 100_000).toFixed(1)}L`;
    if (val >= 1000) return `₹${(val / 1000).toFixed(1)}K`;
    return `₹${val.toFixed(0)}`;
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
            <Link href="/dashboard" className="flex items-center gap-3 px-4 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)]">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Dashboard
            </Link>
            <Link href="/dashboard/analytics" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
              </svg>
              Analytics
            </Link>
            <Link href="/dashboard/watchlist" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
              Watchlist
            </Link>
            <Link href="/dashboard/alerts" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              Alerts
            </Link>
          </nav>

          <div className="absolute bottom-4 left-4 right-4 space-y-1">
            {user && (
              <div className="px-4 py-2 text-xs text-[var(--color-text-muted)] truncate">
                {user.email}
              </div>
            )}
            <Link href="/dashboard/profile" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Profile
            </Link>
            <Link href="/dashboard/settings" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Settings
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
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold">Dashboard</h1>
              <p className="text-[var(--color-text-secondary)]">Welcome back! Here&apos;s your bulk deals overview.</p>
            </div>
            <Link
              href="/dashboard/analytics"
              className="px-4 py-2 rounded-lg bg-[#00d4aa] text-[#0a0e14] text-sm font-medium hover:bg-[#00b894] transition-colors"
            >
              Fetch from NSE
            </Link>
          </div>

          {error && (
            <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 flex items-center justify-between">
              <span>{error}</span>
              <button onClick={fetchDashboard} className="text-sm underline">Retry</button>
            </div>
          )}

          {!loading && showEncourage && (
            <div className="mb-6 p-6 rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-secondary)]">
              <h2 className="text-lg font-semibold mb-2">Get more from the app</h2>
              <p className="text-sm text-[var(--color-text-secondary)] mb-4">
                Track symbols and get notified when bulk deals match your watchlist.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <Link
                  href="/dashboard/watchlist"
                  className="flex items-center gap-4 p-4 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] hover:border-[#00d4aa] hover:bg-[#00d4aa]/5 transition-colors group"
                >
                  <div className="w-12 h-12 rounded-lg bg-[#00d4aa]/20 flex items-center justify-center group-hover:bg-[#00d4aa]/30 transition-colors">
                    <svg className="w-6 h-6 text-[#00d4aa]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                    </svg>
                  </div>
                  <div>
                    <div className="font-medium">Add to watchlist</div>
                    <div className="text-sm text-[var(--color-text-muted)]">Track symbols you care about</div>
                  </div>
                  <span className="ml-auto text-[#00d4aa] text-sm font-medium group-hover:underline">Set up →</span>
                </Link>
                <Link
                  href="/dashboard/alerts"
                  className="flex items-center gap-4 p-4 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] hover:border-[#00d4aa] hover:bg-[#00d4aa]/5 transition-colors group"
                >
                  <div className="w-12 h-12 rounded-lg bg-[#00d4aa]/20 flex items-center justify-center group-hover:bg-[#00d4aa]/30 transition-colors">
                    <svg className="w-6 h-6 text-[#00d4aa]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                    </svg>
                  </div>
                  <div>
                    <div className="font-medium">Alerts</div>
                    <div className="text-sm text-[var(--color-text-muted)]">Get notified when deals match your watchlist</div>
                  </div>
                  <span className="ml-auto text-[#00d4aa] text-sm font-medium group-hover:underline">View →</span>
                </Link>
              </div>
            </div>
          )}

          {loading ? (
            <>
              {/* Shimmer: stats cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="card p-6">
                    <div className="shimmer h-4 w-24 mb-4" />
                    <div className="shimmer h-9 w-20" />
                  </div>
                ))}
              </div>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Shimmer: recent deals table */}
                <div className="lg:col-span-2 card">
                  <div className="p-6 border-b border-[var(--color-border)]">
                    <div className="shimmer h-5 w-40" />
                  </div>
                  <div className="p-6 space-y-4">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <div key={i} className="flex gap-4">
                        <div className="shimmer h-4 flex-1 max-w-[80px]" />
                        <div className="shimmer h-4 flex-1 max-w-[100px]" />
                        <div className="shimmer h-4 flex-1 max-w-[140px]" />
                        <div className="shimmer h-4 w-12" />
                        <div className="shimmer h-4 w-16" />
                        <div className="shimmer h-4 w-14" />
                      </div>
                    ))}
                  </div>
                </div>
                {/* Shimmer: top symbols */}
                <div className="card">
                  <div className="p-4 border-b border-[var(--color-border)]">
                    <div className="shimmer h-5 w-36 mb-2" />
                    <div className="shimmer h-3 w-28" />
                  </div>
                  <div className="p-4 space-y-3">
                    {[1, 2, 3, 4, 5].map((i) => (
                      <div key={i} className="flex items-center justify-between">
                        <div className="space-y-1">
                          <div className="shimmer h-4 w-24" />
                          <div className="shimmer h-3 w-20" />
                        </div>
                        <div className="shimmer h-4 w-12" />
                      </div>
                    ))}
                  </div>
                  <div className="p-4 border-t border-[var(--color-border)]">
                    <div className="shimmer h-4 w-24" />
                  </div>
                </div>
              </div>
            </>
          ) : (
            <>
              {/* Stats Cards - real data */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="card p-6">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-[var(--color-text-secondary)] text-sm">Total Deals</span>
                  </div>
                  <div className="text-3xl font-bold font-mono">
                    {stats ? stats.total_deals.toLocaleString() : '0'}
                  </div>
                </div>
                <div className="card p-6">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-[var(--color-text-secondary)] text-sm">Buy Deals</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-[#00d4aa]/20 text-[#00d4aa]">BUY</span>
                  </div>
                  <div className="text-3xl font-bold font-mono text-[#00d4aa]">
                    {stats ? stats.buy_deals.toLocaleString() : '0'}
                  </div>
                </div>
                <div className="card p-6">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-[var(--color-text-secondary)] text-sm">Sell Deals</span>
                    <span className="text-xs px-2 py-0.5 rounded bg-[#ff6b6b]/20 text-[#ff6b6b]">SELL</span>
                  </div>
                  <div className="text-3xl font-bold font-mono text-[#ff6b6b]">
                    {stats ? stats.sell_deals.toLocaleString() : '0'}
                  </div>
                </div>
                <div className="card p-6">
                  <div className="flex items-center justify-between mb-4">
                    <span className="text-[var(--color-text-secondary)] text-sm">Data source</span>
                  </div>
                  <div className="text-sm font-medium text-[var(--color-text-primary)]">NSE Bulk Deals</div>
                  <Link href="/dashboard/analytics" className="text-xs text-[#00d4aa] hover:underline mt-1 inline-block">
                    View analytics →
                  </Link>
                </div>
              </div>

              {/* Main Grid */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Recent Deals - real data */}
                <div className="lg:col-span-2 card">
                  <div className="p-6 border-b border-[var(--color-border)]">
                    <div className="flex items-center justify-between">
                      <h2 className="text-lg font-semibold">Recent Bulk Deals</h2>
                      <Link href="/dashboard/analytics" className="text-sm text-[#00d4aa] hover:text-[#00b894] transition-colors">
                        View all →
                      </Link>
                    </div>
                  </div>
                  <div className="overflow-x-auto">
                    {recentDeals.length === 0 ? (
                      <div className="p-8 text-center text-[var(--color-text-muted)]">
                        <p className="mb-2">No deals yet.</p>
                        <Link href="/dashboard/analytics" className="text-[#00d4aa] hover:underline">
                          Fetch from NSE
                        </Link>
                        {' '}or upload CSV to get started.
                      </div>
                    ) : (
                      <table className="w-full">
                        <thead>
                          <tr className="border-b border-[var(--color-border)]">
                            <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Date</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Symbol</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Client</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Type</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Qty</th>
                            <th className="px-6 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Value</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-[var(--color-border)]">
                          {recentDeals.map((deal) => (
                            <tr key={deal.id} className="hover:bg-[var(--color-bg-secondary)] transition-colors">
                              <td className="px-6 py-4 text-sm text-[var(--color-text-secondary)]">
                                {new Date(deal.date).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })}
                              </td>
                              <td className="px-6 py-4 text-sm font-medium">{deal.symbol}</td>
                              <td className="px-6 py-4 text-sm text-[var(--color-text-secondary)] max-w-[140px] truncate">{deal.client_name}</td>
                              <td className="px-6 py-4">
                                <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${deal.deal_type === 'BUY' ? 'bg-[#00d4aa]/10 text-[#00d4aa]' : 'bg-[#ff6b6b]/10 text-[#ff6b6b]'}`}>
                                  {deal.deal_type}
                                </span>
                              </td>
                              <td className="px-6 py-4 text-sm font-mono text-right">{deal.quantity.toLocaleString()}</td>
                              <td className="px-6 py-4 text-sm font-mono text-right">{formatValue(deal.quantity, deal.price)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    )}
                  </div>
                </div>

                {/* Top Symbols by deal count - real data */}
                <div className="space-y-6">
                  <div className="card">
                    <div className="p-4 border-b border-[var(--color-border)]">
                      <h3 className="font-semibold text-[#00d4aa]">Top symbols by deals</h3>
                      <p className="text-xs text-[var(--color-text-muted)] mt-0.5">From your imported data</p>
                    </div>
                    <div className="p-4 space-y-3">
                      {topSymbols.length === 0 ? (
                        <p className="text-sm text-[var(--color-text-muted)]">No data. Fetch deals first.</p>
                      ) : (
                        topSymbols.map((s) => (
                          <Link key={s.symbol} href={`/dashboard/analytics?symbol=${encodeURIComponent(s.symbol)}`} className="flex items-center justify-between hover:bg-[var(--color-bg-tertiary)] rounded-lg px-2 py-1.5 -mx-2 transition-colors">
                            <div>
                              <div className="font-medium text-sm">{s.symbol}</div>
                              <div className="text-xs text-[var(--color-text-muted)]">
                                {s.deal_count} deals · {s.total_quantity.toLocaleString()} qty
                              </div>
                            </div>
                            <div className="text-xs">
                              <span className="text-[#00d4aa]">{s.buy_count}B</span>
                              <span className="text-[var(--color-text-muted)] mx-1">/</span>
                              <span className="text-[#ff6b6b]">{s.sell_count}S</span>
                            </div>
                          </Link>
                        ))
                      )}
                    </div>
                    <div className="p-4 border-t border-[var(--color-border)]">
                      <Link href="/dashboard/analytics" className="text-sm text-[#00d4aa] hover:underline">
                        Full analytics →
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}
