'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import { getApiUrl } from '@/config/env';
import { DashboardSidebar } from '@/components/dashboard/DashboardSidebar';

type Segment = 'bulk_deals' | 'block_deals' | 'short_selling';
type DatePreset = '1D' | '1W' | '1M' | '3M' | '6M' | '1Y' | 'Custom';
type DealTypeFilter = '' | 'BUY' | 'SELL';

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

function getDateRange(preset: DatePreset, customFrom: string, customTo: string): { from: string; to: string } {
  const today = new Date();
  const to = new Date(today);
  const from = new Date(today);
  const fmt = (d: Date) => d.toISOString().slice(0, 10);

  if (preset === 'Custom' && customFrom && customTo) {
    return { from: customFrom, to: customTo };
  }

  switch (preset) {
    case '1D':
      return { from: fmt(to), to: fmt(to) };
    case '1W':
      from.setDate(from.getDate() - 6);
      return { from: fmt(from), to: fmt(to) };
    case '1M':
      from.setMonth(from.getMonth() - 1);
      return { from: fmt(from), to: fmt(to) };
    case '3M':
      from.setMonth(from.getMonth() - 3);
      return { from: fmt(from), to: fmt(to) };
    case '6M':
      from.setMonth(from.getMonth() - 6);
      return { from: fmt(from), to: fmt(to) };
    case '1Y':
      from.setFullYear(from.getFullYear() - 1);
      return { from: fmt(from), to: fmt(to) };
    default:
      from.setDate(from.getDate() - 6);
      return { from: fmt(from), to: fmt(to) };
  }
}

const DATE_PRESETS: { value: DatePreset; label: string }[] = [
  { value: '1D', label: '1D' },
  { value: '1W', label: '1W' },
  { value: '1M', label: '1M' },
  { value: '3M', label: '3M' },
  { value: '6M', label: '6M' },
  { value: '1Y', label: '1Y' },
  { value: 'Custom', label: 'Custom' },
];

const SEGMENT_TABS: { value: Segment; label: string }[] = [
  { value: 'bulk_deals', label: 'Bulk Deals' },
  { value: 'block_deals', label: 'Block Deals' },
  { value: 'short_selling', label: 'Short Selling' },
];

export default function AnalyticsPage() {
  const searchParams = useSearchParams();
  const { user, signOut, getAccessToken } = useAuth();
  const [segment, setSegment] = useState<Segment>('bulk_deals');
  const [symbol, setSymbol] = useState('');
  const [dealType, setDealType] = useState<DealTypeFilter>('');
  const [datePreset, setDatePreset] = useState<DatePreset>('1W');
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [data, setData] = useState<DealsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [applied, setApplied] = useState(false);
  const [fetching, setFetching] = useState(false);
  const [fetchMessage, setFetchMessage] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState<string | null>(null);
  const [exporting, setExporting] = useState(false);
  const [exportMessage, setExportMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { from, to } = getDateRange(datePreset, dateFrom, dateTo);
  const showCustomDateRange = datePreset === 'Custom';

  // Pre-fill symbol from URL (e.g. /dashboard/analytics?symbol=RELIANCE)
  useEffect(() => {
    const s = searchParams.get('symbol');
    if (s && typeof s === 'string') setSymbol(s.trim().toUpperCase());
  }, [searchParams]);

  const apiPathBySegment: Record<Segment, string> = {
    bulk_deals: '/bulk-deals/',
    block_deals: '/block-deals/',
    short_selling: '/short-selling/',
  };

  const runQuery = useCallback(async (pageNum: number = 1) => {
    try {
      setLoading(true);
      setError(null);
      const params = new URLSearchParams();
      params.set('page', String(pageNum));
      params.set('page_size', '25');
      params.set('sort_by', 'date');
      params.set('sort_order', 'desc');
      params.set('date_from', from);
      params.set('date_to', to);
      if (symbol.trim()) params.set('symbol', symbol.trim().toUpperCase());
      if (dealType) params.set('deal_type', dealType);

      const token = await getAccessToken();
      const path = apiPathBySegment[segment];
      const result = await api.get<DealsResponse>(
        `${path}?${params.toString()}`,
        token ?? undefined,
      );
      setData(result);
      setApplied(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [segment, symbol, dealType, from, to, getAccessToken]);

  // When switching tabs, load that segment's data if filters were already applied
  const prevSegmentRef = useRef<Segment>(segment);
  useEffect(() => {
    if (prevSegmentRef.current !== segment) {
      prevSegmentRef.current = segment;
      if (applied) runQuery(1);
    }
  }, [segment, applied, runQuery]);

  useEffect(() => {
    const { from: f, to: t } = getDateRange('1W', '', '');
    setDateFrom(f);
    setDateTo(t);
  }, []);

  const handleGo = (e: React.FormEvent) => {
    e.preventDefault();
    runQuery(1);
  };

  const handleClear = () => {
    setSymbol('');
    setDealType('');
    setDatePreset('1W');
    const { from: f, to: t } = getDateRange('1W', '', '');
    setDateFrom(f);
    setDateTo(t);
    setData(null);
    setError(null);
    setApplied(false);
  };

  const handlePresetChange = (preset: DatePreset) => {
    setDatePreset(preset);
    if (preset !== 'Custom') {
      const { from: f, to: t } = getDateRange(preset, '', '');
      setDateFrom(f);
      setDateTo(t);
    }
  };

  const fetchPathBySegment: Record<Segment, string> = {
    bulk_deals: '/bulk-deals/fetch',
    block_deals: '/block-deals/fetch',
    short_selling: '/short-selling/fetch',
  };

  const handleFetchFromNSE = useCallback(async () => {
    try {
      setFetching(true);
      setFetchMessage(null);
      setError(null);
      const token = await getAccessToken();
      const path = fetchPathBySegment[segment];
      const result = await api.post<{ message?: string; imported?: number; fetched?: number }>(
        path,
        {},
        token ?? undefined,
      );
      const msg = result?.message ?? `Fetched. Imported: ${result?.imported ?? 0}`;
      setFetchMessage(msg);
      setTimeout(() => setFetchMessage(null), 5000);
      runQuery(1);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch from NSE');
    } finally {
      setFetching(false);
    }
  }, [segment, getAccessToken, runQuery]);

  const handleUploadCSV = useCallback(
    async (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      e.target.value = '';
      if (!file) return;
      try {
        setUploading(true);
        setUploadMessage(null);
        setError(null);
        const text = await file.text();
        const token = await getAccessToken();
        const result = await api.post<{ message?: string; imported?: number }>(
          '/bulk-deals/upload-csv',
          { csv_content: text },
          token ?? undefined,
        );
        const msg = result?.message ?? `Imported ${result?.imported ?? 0} deals`;
        setUploadMessage(msg);
        setTimeout(() => setUploadMessage(null), 5000);
        runQuery(1);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'CSV upload failed');
      } finally {
        setUploading(false);
      }
    },
    [getAccessToken, runQuery],
  );

  const handleExportCSV = useCallback(() => {
    (async () => {
      try {
        setError(null);
        setExporting(true);
        setExportMessage(null);
        const params = new URLSearchParams();
        params.set('sort_by', 'date');
        params.set('sort_order', 'desc');
        params.set('date_from', from);
        params.set('date_to', to);
        params.set('max_rows', '50000');
        if (symbol.trim()) params.set('symbol', symbol.trim().toUpperCase());
        if (dealType) params.set('deal_type', dealType);

        const exportPathBySegment: Record<Segment, string> = {
          bulk_deals: '/bulk-deals/export-csv',
          block_deals: '/block-deals/export-csv',
          short_selling: '/short-selling/export-csv',
        };

        const token = await getAccessToken();
        const url = getApiUrl(`${exportPathBySegment[segment]}?${params.toString()}`);
        const res = await fetch(url, {
          method: 'GET',
          headers: token ? { Authorization: `Bearer ${token}` } : undefined,
          credentials: 'include',
        });

        if (!res.ok) {
          let msg = `Export failed (${res.status})`;
          try {
            const j = (await res.json()) as { detail?: string; message?: string };
            msg = j.detail || j.message || msg;
          } catch {
            try {
              const t = await res.text();
              if (t) msg = t;
            } catch {
              // ignore
            }
          }
          throw new Error(msg);
        }

        const blob = await res.blob();
        const blobUrl = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = blobUrl;
        a.download = `${segment.replace('_', '-')}-${new Date().toISOString().slice(0, 10)}.csv`;
        a.click();
        URL.revokeObjectURL(blobUrl);
        setExportMessage('CSV downloaded');
        setTimeout(() => setExportMessage(null), 4000);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Export failed');
      } finally {
        setExporting(false);
      }
    })();
  }, [segment, symbol, dealType, from, to, getAccessToken]);

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-[var(--color-bg-primary)]">
        <DashboardSidebar user={user} signOut={signOut} />
        <main className="lg:ml-64 p-6">
          <div className="mb-6">
            <h1 className="text-2xl font-bold">Analytics</h1>
            <p className="text-[var(--color-text-secondary)]">
              Bulk Deals, Block Deals & Short Selling — filter by symbol and date range
            </p>
          </div>

          {/* Segment tabs */}
          <div className="flex border-b border-[var(--color-border)] mb-6">
            {SEGMENT_TABS.map((tab) => (
              <button
                key={tab.value}
                type="button"
                onClick={() => setSegment(tab.value)}
                className={`px-5 py-3 text-sm font-medium border-b-2 transition-colors ${
                  segment === tab.value
                    ? 'border-[var(--color-accent-primary)] text-[var(--color-accent-primary)]'
                    : 'border-transparent text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:border-[var(--color-border-hover)]'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Filter bar */}
          <form onSubmit={handleGo} className="card p-5 mb-6">
            <div className="flex flex-wrap items-end gap-4">
              <div className="flex flex-col gap-1.5">
                <label htmlFor="symbol_search" className="text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
                  Symbol
                </label>
                <input
                  id="symbol_search"
                  type="text"
                  placeholder="Search by Symbol"
                  value={symbol}
                  onChange={(e) => setSymbol(e.target.value)}
                  className="min-w-[180px] px-4 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-sm placeholder:text-[var(--color-text-muted)] focus:outline-none focus:border-[var(--color-border-focus)] transition-colors"
                />
              </div>

              <div className="flex flex-col gap-1.5">
                <span className="text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
                  Deal type
                </span>
                <div className="flex gap-1">
                  {(['', 'BUY', 'SELL'] as const).map((value) => (
                    <button
                      key={value || 'all'}
                      type="button"
                      onClick={() => setDealType(value)}
                      className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        dealType === value
                          ? 'bg-[var(--color-accent-primary)] text-[var(--color-bg-primary)]'
                          : 'bg-[var(--color-bg-tertiary)] text-[var(--color-text-secondary)] border border-[var(--color-border)] hover:border-[var(--color-border-hover)] hover:text-[var(--color-text-primary)]'
                      }`}
                    >
                      {value || 'All'}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex flex-col gap-1.5 w-full sm:w-auto">
                <span className="text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">
                  Select date period
                </span>
                <div className="flex flex-wrap gap-2">
                  {DATE_PRESETS.map(({ value, label }) => (
                    <button
                      key={value}
                      type="button"
                      onClick={() => handlePresetChange(value)}
                      className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        datePreset === value
                          ? 'bg-[var(--color-accent-primary)] text-[var(--color-bg-primary)]'
                          : 'bg-[var(--color-bg-tertiary)] text-[var(--color-text-secondary)] border border-[var(--color-border)] hover:border-[var(--color-border-hover)] hover:text-[var(--color-text-primary)]'
                      }`}
                    >
                      {label}
                    </button>
                  ))}
                  <button
                    type="button"
                    onClick={handleClear}
                    className="px-3 py-2 rounded-lg text-sm text-[var(--color-text-secondary)] bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] hover:bg-[var(--color-bg-elevated)] transition-colors"
                  >
                    Clear
                  </button>
                </div>
              </div>
            </div>

            {/* Custom date range — only when Custom is selected */}
            {showCustomDateRange && (
              <div className="mt-4 flex flex-wrap items-center gap-4">
                <div className="flex items-center gap-2">
                  <label className="text-sm text-[var(--color-text-secondary)]">From</label>
                  <input
                    type="date"
                    value={dateFrom}
                    onChange={(e) => setDateFrom(e.target.value)}
                    className="px-3 py-2 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-sm focus:outline-none focus:border-[var(--color-border-focus)] transition-colors"
                  />
                </div>
                <div className="flex items-center gap-2">
                  <label className="text-sm text-[var(--color-text-secondary)]">To</label>
                  <input
                    type="date"
                    value={dateTo}
                    onChange={(e) => setDateTo(e.target.value)}
                    className="px-3 py-2 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-sm focus:outline-none focus:border-[var(--color-border-focus)] transition-colors"
                  />
                </div>
              </div>
            )}

            <div className="mt-4 flex flex-wrap items-center gap-3">
              <button
                type="submit"
                className="px-5 py-2.5 rounded-lg bg-[var(--color-accent-primary)] text-[var(--color-bg-primary)] font-medium hover:opacity-90 transition-opacity"
              >
                GO
              </button>
              <button
                type="button"
                onClick={handleFetchFromNSE}
                disabled={fetching}
                className="px-5 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-primary)] font-medium hover:bg-[var(--color-bg-secondary)] disabled:opacity-60 transition-colors"
              >
                {fetching ? 'Fetching…' : 'Fetch from NSE'}
              </button>
              {segment === 'bulk_deals' && (
                <>
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept=".csv"
                    className="hidden"
                    onChange={handleUploadCSV}
                  />
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={uploading}
                    className="px-5 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-primary)] font-medium hover:bg-[var(--color-bg-secondary)] disabled:opacity-60 transition-colors"
                  >
                    {uploading ? 'Uploading…' : 'Upload CSV'}
                  </button>
                </>
              )}
              <button
                type="button"
                onClick={handleExportCSV}
                disabled={exporting}
                className="px-5 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] text-[var(--color-text-primary)] font-medium hover:bg-[var(--color-bg-secondary)] disabled:opacity-60 transition-colors"
              >
                {exporting ? 'Exporting…' : 'Export CSV'}
              </button>
            </div>
          </form>

          {(fetchMessage || uploadMessage || exportMessage) && (
            <div className="mb-4 p-3 rounded-lg bg-[var(--color-accent-primary)]/10 border border-[var(--color-accent-primary)]/20 text-[var(--color-accent-primary)] text-sm">
              {exportMessage ?? fetchMessage ?? uploadMessage}
            </div>
          )}

          {error && (
            <div className="mb-6 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
              {error}
            </div>
          )}

          <div className="card overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-[var(--color-border)]">
                      <th className="px-4 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Date</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Symbol</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Client</th>
                      <th className="px-4 py-3 text-center text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Type</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Qty</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Price</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--color-border)]">
                    {loading ? (
                      <tr>
                        <td colSpan={6} className="px-4 py-12 text-center">
                          <div className="w-6 h-6 border-2 border-[var(--color-accent-primary)] border-t-transparent rounded-full animate-spin mx-auto mb-2" />
                          <span className="text-sm text-[var(--color-text-muted)]">Loading...</span>
                        </td>
                      </tr>
                    ) : !applied ? (
                      <tr>
                        <td colSpan={6} className="px-4 py-12 text-center text-[var(--color-text-muted)]">
                          Set filters and click <strong className="text-[var(--color-accent-primary)]">GO</strong> to load data.
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
                          No deals found for the selected period and filters.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
              {(data && (data.total_pages > 1 || data.total > 0)) && (
                <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 border-t border-[var(--color-border)]">
                  <div className="text-sm text-[var(--color-text-muted)]">
                    Page {data.page} of {data.total_pages} ({data.total.toLocaleString()} total)
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => runQuery(data.page - 1)}
                      disabled={loading || data.page <= 1}
                      className="px-3 py-1.5 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-tertiary)] text-sm font-medium text-[var(--color-text-primary)] hover:bg-[var(--color-bg-secondary)] disabled:opacity-50 disabled:pointer-events-none transition-colors"
                    >
                      Previous
                    </button>
                    <button
                      type="button"
                      onClick={() => runQuery(data.page + 1)}
                      disabled={loading || data.page >= data.total_pages}
                      className="px-3 py-1.5 rounded-lg border border-[var(--color-border)] bg-[var(--color-bg-tertiary)] text-sm font-medium text-[var(--color-text-primary)] hover:bg-[var(--color-bg-secondary)] disabled:opacity-50 disabled:pointer-events-none transition-colors"
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
