/**
 * Shared Type Definitions
 */

// API Response Types
export interface ApiResponse<T = unknown> {
  success: boolean;
  message?: string;
  data?: T;
  errors?: Array<{ field?: string; message: string }>;
}

// User Types
export interface User {
  id: string;
  email: string;
  displayName?: string;
  avatarUrl?: string;
  subscriptionTier: 'free' | 'basic' | 'premium' | 'enterprise';
  createdAt: string;
  updatedAt: string;
}

// Deal Types
export type DealType = 'BUY' | 'SELL';

export interface BulkDeal {
  id: string;
  date: string;
  symbol: string;
  securityName?: string;
  clientName: string;
  dealType: DealType;
  quantity: number;
  price: number;
  remarks?: string;
  userId?: string;
  createdAt: string;
  updatedAt: string;
}

export interface BulkDealFilter {
  symbol?: string;
  dealType?: DealType;
  dateFrom?: string;
  dateTo?: string;
  minQuantity?: number;
  maxQuantity?: number;
}

// Pagination Types
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasNext: boolean;
  hasPrevious: boolean;
}

// Navigation Types
export interface NavItem {
  label: string;
  href: string;
  icon?: React.ComponentType<{ className?: string }>;
  badge?: string | number;
  children?: NavItem[];
}

