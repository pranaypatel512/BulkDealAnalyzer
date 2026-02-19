'use client';

import Link from 'next/link';
import { useCallback, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { ProtectedRoute } from '@/components/auth';
import { useAuth } from '@/contexts/AuthContext';
import { useProfile } from '@/hooks/useProfile';
import { api } from '@/lib/api';
import { DashboardSidebar } from '@/components/dashboard/DashboardSidebar';

interface AdminStats {
  users: number;
  bulk_deals: number;
  block_deals: number;
}

interface AdminUser {
  id: string;
  user_id: string;
  email: string | null;
  full_name: string | null;
  role: string;
  created_at: string;
}

interface AdminUsersResponse {
  items: AdminUser[];
  total: number;
  page: number;
  page_size: number;
}

export default function AdminPage() {
  const router = useRouter();
  const { user, signOut, getAccessToken } = useAuth();
  const { isAdmin, loading: profileLoading, refetch: refetchProfile } = useProfile();
  const [adminStatusOk, setAdminStatusOk] = useState<boolean | null>(null);
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [usersData, setUsersData] = useState<AdminUsersResponse | null>(null);
  const [usersPage, setUsersPage] = useState(1);
  const [usersRoleFilter, setUsersRoleFilter] = useState<string>('');
  const [loadingStats, setLoadingStats] = useState(true);
  const [loadingUsers, setLoadingUsers] = useState(true);
  const [updatingRoleFor, setUpdatingRoleFor] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const pageSize = 20;

  const fetchAdminStatus = useCallback(async () => {
    try {
      const token = await getAccessToken();
      const data = await api.get<{ admin: boolean }>('/admin/status', token ?? undefined);
      setAdminStatusOk(data?.admin === true);
    } catch {
      setAdminStatusOk(false);
    }
  }, [getAccessToken]);

  const fetchStats = useCallback(async () => {
    try {
      setLoadingStats(true);
      const token = await getAccessToken();
      const data = await api.get<AdminStats>('/admin/stats', token ?? undefined);
      setStats(data ?? null);
    } catch {
      setStats(null);
    } finally {
      setLoadingStats(false);
    }
  }, [getAccessToken]);

  const fetchUsers = useCallback(async () => {
    try {
      setLoadingUsers(true);
      setError(null);
      const token = await getAccessToken();
      const params = new URLSearchParams({ page: String(usersPage), page_size: String(pageSize) });
      if (usersRoleFilter === 'user' || usersRoleFilter === 'admin') params.set('role', usersRoleFilter);
      const data = await api.get<AdminUsersResponse>(`/admin/users?${params.toString()}`, token ?? undefined);
      setUsersData(data ?? null);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load users');
      setUsersData(null);
    } finally {
      setLoadingUsers(false);
    }
  }, [getAccessToken, usersPage, usersRoleFilter]);

  const updateRole = useCallback(
    async (userId: string, role: 'user' | 'admin') => {
      try {
        setUpdatingRoleFor(userId);
        const token = await getAccessToken();
        await api.patch<AdminUser>(`/admin/users/${userId}/role`, { role }, token ?? undefined);
        await fetchUsers();
        refetchProfile();
      } catch (e) {
        setError(e instanceof Error ? e.message : 'Failed to update role');
      } finally {
        setUpdatingRoleFor(null);
      }
    },
    [getAccessToken, fetchUsers, refetchProfile]
  );

  useEffect(() => {
    if (profileLoading) return;
    if (!isAdmin) {
      router.replace('/dashboard');
      return;
    }
    fetchAdminStatus();
  }, [isAdmin, profileLoading, router, fetchAdminStatus]);

  useEffect(() => {
    if (adminStatusOk !== true) return;
    fetchStats();
  }, [adminStatusOk, fetchStats]);

  useEffect(() => {
    if (adminStatusOk !== true) return;
    fetchUsers();
  }, [adminStatusOk, fetchUsers]);

  if (profileLoading || !isAdmin) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[var(--color-bg-primary)] flex items-center justify-center">
          <div className="w-10 h-10 border-2 border-[#00d4aa] border-t-transparent rounded-full animate-spin" />
        </div>
      </ProtectedRoute>
    );
  }

  if (adminStatusOk === null) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-[var(--color-bg-primary)] flex items-center justify-center">
          <div className="w-10 h-10 border-2 border-[#00d4aa] border-t-transparent rounded-full animate-spin" />
        </div>
      </ProtectedRoute>
    );
  }

  if (adminStatusOk === false) {
    router.replace('/dashboard');
    return null;
  }

  const totalPages = usersData ? Math.max(1, Math.ceil(usersData.total / pageSize)) : 1;

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
            <p className="text-[var(--color-text-secondary)]">System overview and user management.</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div className="card p-5 border border-[var(--color-border)]">
              <div className="text-sm text-[var(--color-text-muted)] mb-1">Users</div>
              <div className="text-2xl font-bold font-mono">
                {loadingStats ? '—' : stats ? stats.users.toLocaleString() : '0'}
              </div>
            </div>
            <div className="card p-5 border border-[var(--color-border)]">
              <div className="text-sm text-[var(--color-text-muted)] mb-1">Bulk deals</div>
              <div className="text-2xl font-bold font-mono text-[#00d4aa]">
                {loadingStats ? '—' : stats ? stats.bulk_deals.toLocaleString() : '0'}
              </div>
            </div>
            <div className="card p-5 border border-[var(--color-border)]">
              <div className="text-sm text-[var(--color-text-muted)] mb-1">Block deals</div>
              <div className="text-2xl font-bold font-mono text-[#00d4aa]">
                {loadingStats ? '—' : stats ? stats.block_deals.toLocaleString() : '0'}
              </div>
            </div>
          </div>

          <div className="card border border-[var(--color-border)] overflow-hidden">
            <div className="p-4 border-b border-[var(--color-border)] flex flex-wrap items-center gap-4">
              <h2 className="text-lg font-semibold">Users</h2>
              <select
                value={usersRoleFilter}
                onChange={(e) => {
                  setUsersRoleFilter(e.target.value);
                  setUsersPage(1);
                }}
                className="bg-[var(--color-bg-tertiary)] border border-[var(--color-border)] rounded px-3 py-1.5 text-sm text-[var(--color-text-primary)]"
              >
                <option value="">All roles</option>
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
              {error && (
                <span className="text-sm text-red-400">{error}</span>
              )}
            </div>
            <div className="overflow-x-auto">
              {loadingUsers ? (
                <div className="p-8 flex justify-center">
                  <div className="w-8 h-8 border-2 border-[#00d4aa] border-t-transparent rounded-full animate-spin" />
                </div>
              ) : usersData?.items?.length ? (
                <>
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="border-b border-[var(--color-border)] text-left text-[var(--color-text-muted)]">
                        <th className="p-3 font-medium">Email</th>
                        <th className="p-3 font-medium">Name</th>
                        <th className="p-3 font-medium">Role</th>
                        <th className="p-3 font-medium">Created</th>
                        <th className="p-3 font-medium">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {usersData.items.map((u) => (
                        <tr key={u.id} className="border-b border-[var(--color-border)]">
                          <td className="p-3 text-[var(--color-text-primary)]">{u.email ?? '—'}</td>
                          <td className="p-3 text-[var(--color-text-secondary)]">{u.full_name ?? '—'}</td>
                          <td className="p-3">
                            <span
                              className={
                                u.role === 'admin'
                                  ? 'px-2 py-0.5 rounded text-xs font-medium bg-amber-500/20 text-amber-400 border border-amber-500/30'
                                  : 'text-[var(--color-text-secondary)]'
                              }
                            >
                              {u.role}
                            </span>
                          </td>
                          <td className="p-3 text-[var(--color-text-muted)]">
                            {u.created_at ? new Date(u.created_at).toLocaleDateString() : '—'}
                          </td>
                          <td className="p-3">
                            {u.role === 'admin' ? (
                              <button
                                type="button"
                                onClick={() => updateRole(u.user_id, 'user')}
                                disabled={updatingRoleFor === u.user_id}
                                className="text-amber-400 hover:underline disabled:opacity-50 text-xs"
                              >
                                {updatingRoleFor === u.user_id ? 'Updating…' : 'Set User'}
                              </button>
                            ) : (
                              <button
                                type="button"
                                onClick={() => updateRole(u.user_id, 'admin')}
                                disabled={updatingRoleFor === u.user_id}
                                className="text-[#00d4aa] hover:underline disabled:opacity-50 text-xs"
                              >
                                {updatingRoleFor === u.user_id ? 'Updating…' : 'Set Admin'}
                              </button>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                  <div className="p-3 border-t border-[var(--color-border)] flex items-center justify-between flex-wrap gap-2">
                    <span className="text-sm text-[var(--color-text-muted)]">
                      {usersData.total} user{usersData.total !== 1 ? 's' : ''}
                    </span>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setUsersPage((p) => Math.max(1, p - 1))}
                        disabled={usersPage <= 1}
                        className="px-3 py-1 rounded border border-[var(--color-border)] text-sm disabled:opacity-50 hover:bg-[var(--color-bg-tertiary)]"
                      >
                        Previous
                      </button>
                      <span className="px-3 py-1 text-sm text-[var(--color-text-secondary)]">
                        Page {usersData.page} of {totalPages}
                      </span>
                      <button
                        type="button"
                        onClick={() => setUsersPage((p) => Math.min(totalPages, p + 1))}
                        disabled={usersPage >= totalPages}
                        className="px-3 py-1 rounded border border-[var(--color-border)] text-sm disabled:opacity-50 hover:bg-[var(--color-bg-tertiary)]"
                      >
                        Next
                      </button>
                    </div>
                  </div>
                </>
              ) : (
                <div className="p-8 text-center text-[var(--color-text-muted)]">No users found.</div>
              )}
            </div>
          </div>

          <div className="mt-6 flex gap-4">
            <Link
              href="/dashboard/analytics"
              className="text-[#00d4aa] hover:underline font-medium text-sm"
            >
              View Analytics →
            </Link>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}
