'use client';

import { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';

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

interface DealStats {
  total_deals: number;
  buy_deals: number;
  sell_deals: number;
}

interface FetchResult {
  status: string;
  fetched: number;
  imported: number;
  skipped: number;
  errors: string[];
  message: string;
}

interface FetchHistoryItem {
  id: string;
  source: string;
  status: string;
  deals_fetched: number;
  deals_imported: number;
  deals_skipped: number;
  error_message: string | null;
  created_at: string;
}

export default function BulkDealsPage() {
  const { user, signOut, getAccessToken } = useAuth();
  const [data, setData] = useState<DealsResponse | null>(null);
  const [stats, setStats] = useState<DealStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [fetching, setFetching] = useState(false);
  const [fetchResult, setFetchResult] = useState<FetchResult | null>(null);
  const [fetchHistory, setFetchHistory] = useState<FetchHistoryItem[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  // Filters
  const [symbol, setSymbol] = useState('');
  const [dealType, setDealType] = useState('');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const pageSize = 15;

  const fetchDeals = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const params = new URLSearchParams();
      params.set('page', String(page));
      params.set('page_size', String(pageSize));
      params.set('sort_by', sortBy);
      params.set('sort_order', sortOrder);
      if (symbol) params.set('symbol', symbol);
      if (dealType) params.set('deal_type', dealType);
      if (dateFrom) params.set('date_from', dateFrom);
      if (dateTo) params.set('date_to', dateTo);

      const token = await getAccessToken();
      const result = await api.get<DealsResponse>(
        `/bulk-deals/?${params.toString()}`,
        token ?? undefined,
      );
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load deals');
    } finally {
      setLoading(false);
    }
  }, [page, sortBy, sortOrder, symbol, dealType, dateFrom, dateTo, getAccessToken]);

  const fetchStats = useCallback(async () => {
    try {
      const token = await getAccessToken();
      const result = await api.get<DealStats>(
        '/bulk-deals/stats',
        token ?? undefined,
      );
      setStats(result);
    } catch {
      // Stats are non-critical
    }
  }, [getAccessToken]);

  useEffect(() => {
    fetchDeals();
    fetchStats();
  }, [fetchDeals, fetchStats]);

  const handleSort = (field: string) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
    setPage(1);
  };

  const handleFilter = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    fetchDeals();
  };

  const clearFilters = () => {
    setSymbol('');
    setDealType('');
    setDateFrom('');
    setDateTo('');
    setPage(1);
  };

  const handleFetchFromNSE = useCallback(async () => {
    try {
      setFetching(true);
      setFetchResult(null);
      setError(null);
      const token = await getAccessToken();
      const result = await api.post<FetchResult>(
        '/bulk-deals/fetch',
        {},
        token ?? undefined,
      );
      setFetchResult(result);
      // Refresh deals and stats after fetch
      fetchDeals();
      fetchStats();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch from NSE');
    } finally {
      setFetching(false);
    }
  }, [getAccessToken, fetchDeals, fetchStats]);

  const loadFetchHistory = useCallback(async () => {
    try {
      const token = await getAccessToken();
      const result = await api.get<FetchHistoryItem[]>(
        '/bulk-deals/fetch-history?limit=10',
        token ?? undefined,
      );
      setFetchHistory(result);
    } catch {
      // Non-critical
    }
  }, [getAccessToken]);

  const SortIcon = ({ field }: { field: string }) => {
    if (sortBy !== field) return <span className="text-[var(--color-text-muted)] ml-1">&#8597;</span>;
    return <span className="text-[#00d4aa] ml-1">{sortOrder === 'asc' ? '&#9650;' : '&#9660;'}</span>;
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
            <Link href="/dashboard/deals" className="flex items-center gap-3 px-4 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)]">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Bulk Deals
            </Link>
            <Link href="/dashboard/profile" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              Profile
            </Link>
          </nav>

          <div className="absolute bottom-4 left-4 right-4 space-y-1">
            {user && (
              <div className="px-4 py-2 text-xs text-[var(--color-text-muted)] truncate">
                {user.email}
              </div>
            )}
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
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold">Bulk Deals</h1>
              <p className="text-[var(--color-text-secondary)]">Browse and filter NSE bulk deals data</p>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={() => {
                  setShowHistory(!showHistory);
                  if (!showHistory) loadFetchHistory();
                }}
                className="px-3 py-2 rounded-lg border border-[var(--color-border)] text-sm text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] transition-colors"
              >
                {showHistory ? 'Hide History' : 'Fetch History'}
              </button>
              <button
                onClick={handleFetchFromNSE}
                disabled={fetching}
                className="px-4 py-2 rounded-lg bg-[#00d4aa] text-[#0a0e14] text-sm font-medium hover:bg-[#00b894] transition-colors disabled:opacity-50 flex items-center gap-2"
              >
                {fetching ? (
                  <>
                    <div className="w-4 h-4 border-2 border-[#0a0e14] border-t-transparent rounded-full animate-spin" />
                    Fetching...
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Fetch from NSE
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Fetch Result Banner */}
          {fetchResult && (
            <div className={`mb-4 p-4 rounded-lg border ${
              fetchResult.status === 'success'
                ? 'bg-[#00d4aa]/10 border-[#00d4aa]/20 text-[#00d4aa]'
                : 'bg-red-500/10 border-red-500/20 text-red-400'
            }`}>
              <div className="flex items-center justify-between">
                <div>
                  <span className="font-medium">{fetchResult.message}</span>
                  {fetchResult.status === 'success' && fetchResult.fetched > 0 && (
                    <span className="ml-3 text-sm opacity-80">
                      Fetched: {fetchResult.fetched} | Imported: {fetchResult.imported} | Skipped: {fetchResult.skipped}
                    </span>
                  )}
                </div>
                <button
                  onClick={() => setFetchResult(null)}
                  className="text-current opacity-60 hover:opacity-100"
                >
                  &times;
                </button>
              </div>
              {fetchResult.errors.length > 0 && (
                <div className="mt-2 text-sm opacity-80">
                  {fetchResult.errors.slice(0, 3).map((e, i) => (
                    <div key={i}>{e}</div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Fetch History Panel */}
          {showHistory && (
            <div className="card p-4 mb-6">
              <h3 className="text-sm font-medium text-[var(--color-text-muted)] uppercase tracking-wider mb-3">
                Recent Fetch History
              </h3>
              {fetchHistory.length === 0 ? (
                <p className="text-sm text-[var(--color-text-muted)]">No fetch history yet.</p>
              ) : (
                <div className="space-y-2">
                  {fetchHistory.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between py-2 px-3 rounded-lg bg-[var(--color-bg-tertiary)]"
                    >
                      <div className="flex items-center gap-3">
                        <span className={`inline-block w-2 h-2 rounded-full ${
                          item.status === 'success' ? 'bg-[#00d4aa]' : 'bg-red-500'
                        }`} />
                        <span className="text-sm font-mono">
                          {item.source === 'nse_api' ? 'NSE API' : 'CSV Upload'}
                        </span>
                        <span className="text-xs text-[var(--color-text-muted)]">
                          +{item.deals_imported} imported, {item.deals_skipped} skipped
                        </span>
                      </div>
                      <span className="text-xs text-[var(--color-text-muted)]">
                        {new Date(item.created_at).toLocaleString('en-IN', {
                          day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit',
                        })}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Stats Cards */}
          {stats && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="card p-4">
                <div className="text-sm text-[var(--color-text-muted)]">Total Deals</div>
                <div className="text-2xl font-bold font-mono">{stats.total_deals.toLocaleString()}</div>
              </div>
              <div className="card p-4">
                <div className="text-sm text-[var(--color-text-muted)]">Buy Deals</div>
                <div className="text-2xl font-bold font-mono text-[#00d4aa]">{stats.buy_deals.toLocaleString()}</div>
              </div>
              <div className="card p-4">
                <div className="text-sm text-[var(--color-text-muted)]">Sell Deals</div>
                <div className="text-2xl font-bold font-mono text-[#ff6b6b]">{stats.sell_deals.toLocaleString()}</div>
              </div>
            </div>
          )}

          {/* Filters */}
          <form onSubmit={handleFilter} className="card p-4 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
              <input
                type="text"
                placeholder="Symbol (e.g. RELIANCE)"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value)}
                className="px-3 py-2 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-sm placeholder:text-[var(--color-text-muted)] focus:outline-none focus:border-[#00d4aa] transition-colors"
              />
              <select
                value={dealType}
                onChange={(e) => setDealType(e.target.value)}
                className="px-3 py-2 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-sm focus:outline-none focus:border-[#00d4aa] transition-colors"
              >
                <option value="">All Types</option>
                <option value="BUY">BUY</option>
                <option value="SELL">SELL</option>
              </select>
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="px-3 py-2 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-sm focus:outline-none focus:border-[#00d4aa] transition-colors"
              />
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="px-3 py-2 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-sm focus:outline-none focus:border-[#00d4aa] transition-colors"
              />
              <div className="flex gap-2">
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 rounded-lg bg-[#00d4aa] text-[#0a0e14] text-sm font-medium hover:bg-[#00b894] transition-colors"
                >
                  Filter
                </button>
                <button
                  type="button"
                  onClick={clearFilters}
                  className="px-3 py-2 rounded-lg border border-[var(--color-border)] text-sm text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] transition-colors"
                >
                  Clear
                </button>
              </div>
            </div>
          </form>

          {/* Error */}
          {error && (
            <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
              {error}
            </div>
          )}

          {/* Table */}
          <div className="card overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[var(--color-border)]">
                    <th className="px-4 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider cursor-pointer hover:text-[var(--color-text-primary)]" onClick={() => handleSort('date')}>
                      Date<SortIcon field="date" />
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider cursor-pointer hover:text-[var(--color-text-primary)]" onClick={() => handleSort('symbol')}>
                      Symbol<SortIcon field="symbol" />
                    </th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
                      Client
                    </th>
                    <th className="px-4 py-3 text-center text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider cursor-pointer hover:text-[var(--color-text-primary)]" onClick={() => handleSort('quantity')}>
                      Quantity<SortIcon field="quantity" />
                    </th>
                    <th className="px-4 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider cursor-pointer hover:text-[var(--color-text-primary)]" onClick={() => handleSort('price')}>
                      Price<SortIcon field="price" />
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--color-border)]">
                  {loading ? (
                    <tr>
                      <td colSpan={6} className="px-4 py-12 text-center">
                        <div className="w-6 h-6 border-2 border-[#00d4aa] border-t-transparent rounded-full animate-spin mx-auto mb-2" />
                        <span className="text-sm text-[var(--color-text-muted)]">Loading deals...</span>
                      </td>
                    </tr>
                  ) : data && data.deals.length > 0 ? (
                    data.deals.map((deal) => (
                      <tr key={deal.id} className="hover:bg-[var(--color-bg-secondary)] transition-colors">
                        <td className="px-4 py-3 text-sm font-mono text-[var(--color-text-secondary)]">
                          {new Date(deal.date).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })}
                        </td>
                        <td className="px-4 py-3 text-sm font-medium">{deal.symbol}</td>
                        <td className="px-4 py-3 text-sm text-[var(--color-text-secondary)] max-w-[200px] truncate">{deal.client_name}</td>
                        <td className="px-4 py-3 text-center">
                          <span className={`inline-block px-2 py-0.5 rounded text-xs font-bold ${deal.deal_type === 'BUY' ? 'bg-[#00d4aa]/10 text-[#00d4aa]' : 'bg-[#ff6b6b]/10 text-[#ff6b6b]'}`}>
                            {deal.deal_type}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm font-mono text-right">{deal.quantity.toLocaleString()}</td>
                        <td className="px-4 py-3 text-sm font-mono text-right">{deal.price.toFixed(2)}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={6} className="px-4 py-12 text-center text-[var(--color-text-muted)]">
                        No deals found. Try adjusting your filters.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {data && data.total_pages > 1 && (
              <div className="flex items-center justify-between px-4 py-3 border-t border-[var(--color-border)]">
                <div className="text-sm text-[var(--color-text-muted)]">
                  Page {data.page} of {data.total_pages} ({data.total.toLocaleString()} total)
                </div>
                <div className="flex gap-2">
                  <button
                    disabled={page <= 1}
                    onClick={() => setPage(page - 1)}
                    className="px-3 py-1.5 rounded text-sm border border-[var(--color-border)] disabled:opacity-30 hover:bg-[var(--color-bg-tertiary)] transition-colors"
                  >
                    Previous
                  </button>
                  <button
                    disabled={page >= data.total_pages}
                    onClick={() => setPage(page + 1)}
                    className="px-3 py-1.5 rounded text-sm border border-[var(--color-border)] disabled:opacity-30 hover:bg-[var(--color-bg-tertiary)] transition-colors"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
