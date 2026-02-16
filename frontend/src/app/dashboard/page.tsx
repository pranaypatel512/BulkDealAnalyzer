'use client';

import Link from 'next/link';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';

// Sample data - will be replaced with real API data
const recentDeals = [
  { id: '1', symbol: 'RELIANCE', client: 'HDFC AMC', type: 'BUY', quantity: 150000, price: 2456.75, change: 2.34 },
  { id: '2', symbol: 'TCS', client: 'SBI MF', type: 'SELL', quantity: 85000, price: 3789.50, change: -1.12 },
  { id: '3', symbol: 'INFY', client: 'ICICI PRUD', type: 'BUY', quantity: 200000, price: 1567.25, change: 0.89 },
  { id: '4', symbol: 'HDFCBANK', client: 'MORGAN STANLEY', type: 'BUY', quantity: 120000, price: 1678.00, change: 1.56 },
  { id: '5', symbol: 'BAJFINANCE', client: 'GOLDMAN SACHS', type: 'SELL', quantity: 45000, price: 6890.75, change: -2.45 },
];

const topGainers = [
  { symbol: 'TATAMOTORS', change: 5.67, volume: '₹45.2 Cr' },
  { symbol: 'ADANIENT', change: 4.23, volume: '₹38.9 Cr' },
  { symbol: 'COALINDIA', change: 3.89, volume: '₹22.1 Cr' },
];

const topLosers = [
  { symbol: 'HINDALCO', change: -4.12, volume: '₹28.5 Cr' },
  { symbol: 'JSWSTEEL', change: -3.78, volume: '₹31.2 Cr' },
  { symbol: 'TATASTEEL', change: -2.91, volume: '₹19.8 Cr' },
];

export default function DashboardPage() {
  const { user, signOut } = useAuth();

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
          <Link href="/dashboard/deals" className="flex items-center gap-3 px-4 py-2.5 rounded-lg text-[var(--color-text-secondary)] hover:bg-[var(--color-bg-tertiary)] hover:text-[var(--color-text-primary)] transition-colors">
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Bulk Deals
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
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <p className="text-[var(--color-text-secondary)]">Welcome back! Here&apos;s what&apos;s happening today.</p>
          </div>
          <div className="flex items-center gap-4">
            <button className="p-2 rounded-lg hover:bg-[var(--color-bg-secondary)] text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] transition-colors">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </button>
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#00d4aa] to-[#4dabf7]" />
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[var(--color-text-secondary)] text-sm">Today&apos;s Deals</span>
              <span className="badge badge-success">+12.5%</span>
            </div>
            <div className="text-3xl font-bold font-mono">1,247</div>
          </div>
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[var(--color-text-secondary)] text-sm">Total Volume</span>
              <span className="badge badge-info">₹ INR</span>
            </div>
            <div className="text-3xl font-bold font-mono">₹847 Cr</div>
          </div>
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[var(--color-text-secondary)] text-sm">Buy Deals</span>
              <span className="badge badge-success">BUY</span>
            </div>
            <div className="text-3xl font-bold font-mono text-[#00d4aa]">687</div>
          </div>
          <div className="card p-6">
            <div className="flex items-center justify-between mb-4">
              <span className="text-[var(--color-text-secondary)] text-sm">Sell Deals</span>
              <span className="badge badge-danger">SELL</span>
            </div>
            <div className="text-3xl font-bold font-mono text-[#ff6b6b]">560</div>
          </div>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Deals Table */}
          <div className="lg:col-span-2 card">
            <div className="p-6 border-b border-[var(--color-border)]">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold">Recent Bulk Deals</h2>
                <Link href="/dashboard/deals" className="text-sm text-[#00d4aa] hover:text-[#00b894] transition-colors">
                  View all →
                </Link>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-[var(--color-border)]">
                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Symbol</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Client</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Type</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Qty</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Price</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-[var(--color-text-muted)] uppercase tracking-wider">Change</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[var(--color-border)]">
                  {recentDeals.map((deal) => (
                    <tr key={deal.id} className="hover:bg-[var(--color-bg-secondary)] transition-colors">
                      <td className="px-6 py-4 text-sm font-medium">{deal.symbol}</td>
                      <td className="px-6 py-4 text-sm text-[var(--color-text-secondary)]">{deal.client}</td>
                      <td className="px-6 py-4">
                        <span className={`badge ${deal.type === 'BUY' ? 'badge-success' : 'badge-danger'}`}>
                          {deal.type}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm font-mono text-right">{deal.quantity.toLocaleString()}</td>
                      <td className="px-6 py-4 text-sm font-mono text-right">₹{deal.price.toFixed(2)}</td>
                      <td className={`px-6 py-4 text-sm font-mono text-right ${deal.change >= 0 ? 'text-[#00d4aa]' : 'text-[#ff6b6b]'}`}>
                        {deal.change >= 0 ? '+' : ''}{deal.change.toFixed(2)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Top Movers */}
          <div className="space-y-6">
            {/* Gainers */}
            <div className="card">
              <div className="p-4 border-b border-[var(--color-border)]">
                <h3 className="font-semibold text-[#00d4aa]">📈 Top Gainers</h3>
              </div>
              <div className="p-4 space-y-3">
                {topGainers.map((stock) => (
                  <div key={stock.symbol} className="flex items-center justify-between">
                    <div>
                      <div className="font-medium text-sm">{stock.symbol}</div>
                      <div className="text-xs text-[var(--color-text-muted)]">{stock.volume}</div>
                    </div>
                    <div className="text-[#00d4aa] font-mono text-sm">+{stock.change}%</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Losers */}
            <div className="card">
              <div className="p-4 border-b border-[var(--color-border)]">
                <h3 className="font-semibold text-[#ff6b6b]">📉 Top Losers</h3>
              </div>
              <div className="p-4 space-y-3">
                {topLosers.map((stock) => (
                  <div key={stock.symbol} className="flex items-center justify-between">
                    <div>
                      <div className="font-medium text-sm">{stock.symbol}</div>
                      <div className="text-xs text-[var(--color-text-muted)]">{stock.volume}</div>
                    </div>
                    <div className="text-[#ff6b6b] font-mono text-sm">{stock.change}%</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
    </ProtectedRoute>
  );
}

