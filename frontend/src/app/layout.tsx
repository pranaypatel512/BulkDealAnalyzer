import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: 'BulkDeal Analyzer | NSE Bulk Deals Intelligence',
  description: 'Analyze NSE bulk deals data with powerful insights, real-time tracking, and institutional investor patterns.',
  keywords: ['NSE', 'bulk deals', 'stock market', 'trading', 'analytics', 'institutional investors'],
  authors: [{ name: 'BulkDeal Analyzer Team' }],
  openGraph: {
    title: 'BulkDeal Analyzer',
    description: 'Professional NSE bulk deals analysis platform',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="min-h-screen antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
