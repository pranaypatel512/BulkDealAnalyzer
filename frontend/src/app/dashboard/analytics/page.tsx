'use client';

import { useCallback, useEffect, useState } from 'react';
import Link from 'next/link';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';
import { api } from '@/lib/api';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  AreaChart, Area, PieChart, Pie, Cell, ResponsiveContainer,
} from 'recharts';

interface TopSymbol {
  symbol: string;
  total_quantity: number;
  deal_count: number;
  buy_count: number;
  sell_count: number;
}

interface DailyTrend {
  date: string;
  total_deals: number;
  buy_deals: number;
  sell_deals: number;
  total_quantity: number;
  total_value: number;
}

interface PriceRange {
  range: string;
  count: number;
}

interface DealStats {
  total_deals: number;
  buy_deals: number;
  sell_deals: number;
}

const COLORS = ['#00d4aa', '#ff6b6b', '#ffa502', '#70a1ff', '#7bed9f', '#ff6348', '#5352ed', '#2ed573'];

export default function AnalyticsPage() {
  const { user, signOut, getAccessToken } = useAuth();
  const [topSymbols, setTopSymbols] = useState<TopSymbol[]>([]);
  const [dailyTrend, setDailyTrend] = useState<DailyTrend[]>([]);
  const [priceDistribution, setPriceDistribution] = useState<PriceRange[]>([]);
  const [stats, setStats] = useState<DealStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(30);

  const fetchAll = useCallback(async () => {
    try {
      setLoading(true);
      const token = await getAccessToken();
      const t = token ?? undefined;

      const [symbolsRes, trendRes, priceRes, statsRes] = await Promise.all([
        api.get<TopSymbol[]>('/bulk-deals/analytics/top-symbols?limit=10', t),
        api.get<DailyTrend[]>(`/bulk-deals/analytics/daily-trend?days=${days}`, t),
        api.get<PriceRange[]>('/bulk-deals/analytics/price-distribution', t),
        api.get<DealStats>('/bulk-deals/stats', t),
      ]);

      setTopSymbols(symbolsRes);
      setDailyTrend(trendRes);
      setPriceDistribution(priceRes);
      setStats(statsRes);
    } catch {
      // Graceful fallback with empty data
    } finally {
      setLoading(false);
    }
  }, [getAccessToken, days]);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  const formatValue = (val: number) => {
    if (val >= 10_000_000) return `${(val / 10_000_000).toFixed(1)}Cr`;
    if (val >= 100_000) return `${(val / 100_000).toFixed(1)}L`;
    if (val >= 1000) return `${(val / 1000).toFixed(1)}K`;
    return val.toString();
  };

  const pieData = stats
    ? [
        { name: 'Buy Deals', value: stats.buy_deals },
        { name: 'Sell Deals', value: stats.sell_deals },
      ]
    : [];

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
            <Link href="/dashboard/analytics" className="flex items-center gap-3 px-4 py-2.5 rounded-lg bg-[var(--color-bg-tertiary)] text-[var(--color-text-primary)]">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
              </svg>
              Analytics
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
              <h1 className="text-2xl font-bold">Analytics</h1>
              <p className="text-[var(--color-text-secondary)]">Visualize bulk deals data and trends</p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-[var(--color-text-muted)]">Period:</span>
              {[7, 30, 90, 180].map((d) => (
                <button
                  key={d}
                  onClick={() => setDays(d)}
                  className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                    days === d
                      ? 'bg-[#00d4aa] text-[#0a0e14] font-medium'
                      : 'border border-[var(--color-border)] text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)]'
                  }`}
                >
                  {d}d
                </button>
              ))}
            </div>
          </div>

          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="w-8 h-8 border-2 border-[#00d4aa] border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            <div className="space-y-6">
              {/* Row 1: Stats + Buy/Sell Pie */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Summary Cards */}
                {stats && (
                  <>
                    <div className="card p-5">
                      <div className="text-sm text-[var(--color-text-muted)] mb-1">Total Deals</div>
                      <div className="text-3xl font-bold font-mono">{stats.total_deals.toLocaleString()}</div>
                    </div>
                    <div className="card p-5">
                      <div className="text-sm text-[var(--color-text-muted)] mb-1">Buy vs Sell</div>
                      <div className="flex items-center gap-4">
                        <div>
                          <div className="text-xl font-bold font-mono text-[#00d4aa]">{stats.buy_deals.toLocaleString()}</div>
                          <div className="text-xs text-[var(--color-text-muted)]">Buy</div>
                        </div>
                        <div className="text-[var(--color-text-muted)]">:</div>
                        <div>
                          <div className="text-xl font-bold font-mono text-[#ff6b6b]">{stats.sell_deals.toLocaleString()}</div>
                          <div className="text-xs text-[var(--color-text-muted)]">Sell</div>
                        </div>
                      </div>
                    </div>
                    <div className="card p-5 flex items-center justify-center">
                      {pieData.some((d) => d.value > 0) ? (
                        <ResponsiveContainer width="100%" height={120}>
                          <PieChart>
                            <Pie
                              data={pieData}
                              cx="50%"
                              cy="50%"
                              innerRadius={30}
                              outerRadius={50}
                              paddingAngle={4}
                              dataKey="value"
                            >
                              <Cell fill="#00d4aa" />
                              <Cell fill="#ff6b6b" />
                            </Pie>
                            <Tooltip
                              contentStyle={{
                                backgroundColor: '#1a1e2e',
                                border: '1px solid #2a2e3e',
                                borderRadius: '8px',
                                color: '#e0e0e0',
                              }}
                            />
                          </PieChart>
                        </ResponsiveContainer>
                      ) : (
                        <span className="text-sm text-[var(--color-text-muted)]">No data</span>
                      )}
                    </div>
                  </>
                )}
              </div>

              {/* Row 2: Daily Trend */}
              <div className="card p-5">
                <h3 className="text-sm font-medium text-[var(--color-text-muted)] uppercase tracking-wider mb-4">
                  Daily Deal Trend (Last {days} Days)
                </h3>
                {dailyTrend.length > 0 ? (
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={dailyTrend}>
                      <defs>
                        <linearGradient id="buyGrad" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#00d4aa" stopOpacity={0.3} />
                          <stop offset="95%" stopColor="#00d4aa" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="sellGrad" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#ff6b6b" stopOpacity={0.3} />
                          <stop offset="95%" stopColor="#ff6b6b" stopOpacity={0} />
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#2a2e3e" />
                      <XAxis
                        dataKey="date"
                        stroke="#666"
                        fontSize={11}
                        tickFormatter={(v) => {
                          const d = new Date(v);
                          return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short' });
                        }}
                      />
                      <YAxis stroke="#666" fontSize={11} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: '#1a1e2e',
                          border: '1px solid #2a2e3e',
                          borderRadius: '8px',
                          color: '#e0e0e0',
                        }}
                        labelFormatter={(v) => new Date(v).toLocaleDateString('en-IN', {
                          day: '2-digit', month: 'short', year: 'numeric',
                        })}
                      />
                      <Legend />
                      <Area
                        type="monotone"
                        dataKey="buy_deals"
                        name="Buy"
                        stroke="#00d4aa"
                        fill="url(#buyGrad)"
                        strokeWidth={2}
                      />
                      <Area
                        type="monotone"
                        dataKey="sell_deals"
                        name="Sell"
                        stroke="#ff6b6b"
                        fill="url(#sellGrad)"
                        strokeWidth={2}
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-[300px] flex items-center justify-center text-[var(--color-text-muted)]">
                    No trend data available. Fetch some deals first.
                  </div>
                )}
              </div>

              {/* Row 3: Top Symbols + Price Distribution */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Top Symbols */}
                <div className="card p-5">
                  <h3 className="text-sm font-medium text-[var(--color-text-muted)] uppercase tracking-wider mb-4">
                    Top Symbols by Deal Count
                  </h3>
                  {topSymbols.length > 0 ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={topSymbols} layout="vertical">
                        <CartesianGrid strokeDasharray="3 3" stroke="#2a2e3e" />
                        <XAxis type="number" stroke="#666" fontSize={11} />
                        <YAxis
                          dataKey="symbol"
                          type="category"
                          stroke="#666"
                          fontSize={11}
                          width={80}
                        />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#1a1e2e',
                            border: '1px solid #2a2e3e',
                            borderRadius: '8px',
                            color: '#e0e0e0',
                          }}
                        />
                        <Legend />
                        <Bar dataKey="buy_count" name="Buy" fill="#00d4aa" stackId="a" />
                        <Bar dataKey="sell_count" name="Sell" fill="#ff6b6b" stackId="a" />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="h-[300px] flex items-center justify-center text-[var(--color-text-muted)]">
                      No symbol data available
                    </div>
                  )}
                </div>

                {/* Price Distribution */}
                <div className="card p-5">
                  <h3 className="text-sm font-medium text-[var(--color-text-muted)] uppercase tracking-wider mb-4">
                    Price Distribution
                  </h3>
                  {priceDistribution.some((d) => d.count > 0) ? (
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={priceDistribution}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#2a2e3e" />
                        <XAxis dataKey="range" stroke="#666" fontSize={11} />
                        <YAxis stroke="#666" fontSize={11} />
                        <Tooltip
                          contentStyle={{
                            backgroundColor: '#1a1e2e',
                            border: '1px solid #2a2e3e',
                            borderRadius: '8px',
                            color: '#e0e0e0',
                          }}
                        />
                        <Bar dataKey="count" name="Deals" fill="#70a1ff" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  ) : (
                    <div className="h-[300px] flex items-center justify-center text-[var(--color-text-muted)]">
                      No price data available
                    </div>
                  )}
                </div>
              </div>

              {/* Row 4: Volume Table */}
              {topSymbols.length > 0 && (
                <div className="card p-5">
                  <h3 className="text-sm font-medium text-[var(--color-text-muted)] uppercase tracking-wider mb-4">
                    Symbol Volume Summary
                  </h3>
                  <div className="overflow-x-auto">
                    <table className="w-full">
                      <thead>
                        <tr className="border-b border-[var(--color-border)]">
                          <th className="px-4 py-2 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase">#</th>
                          <th className="px-4 py-2 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase">Symbol</th>
                          <th className="px-4 py-2 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase">Deals</th>
                          <th className="px-4 py-2 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase">Buy</th>
                          <th className="px-4 py-2 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase">Sell</th>
                          <th className="px-4 py-2 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase">Total Qty</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-[var(--color-border)]">
                        {topSymbols.map((sym, i) => (
                          <tr key={sym.symbol} className="hover:bg-[var(--color-bg-secondary)] transition-colors">
                            <td className="px-4 py-2 text-sm text-[var(--color-text-muted)]">{i + 1}</td>
                            <td className="px-4 py-2 text-sm font-medium">{sym.symbol}</td>
                            <td className="px-4 py-2 text-sm font-mono text-right">{sym.deal_count}</td>
                            <td className="px-4 py-2 text-sm font-mono text-right text-[#00d4aa]">{sym.buy_count}</td>
                            <td className="px-4 py-2 text-sm font-mono text-right text-[#ff6b6b]">{sym.sell_count}</td>
                            <td className="px-4 py-2 text-sm font-mono text-right">{formatValue(sym.total_quantity)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}
