import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';

export function useAuth(requireAuth: boolean = true) {
  const { isAuthenticated, user, _hasHydrated } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    // Only redirect after hydration is complete
    if (_hasHydrated && requireAuth && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, requireAuth, router, _hasHydrated]);

  return { isAuthenticated, user, isLoading: !_hasHydrated };
}

export function useRequireRole(allowedRoles: string[]) {
  const { user, _hasHydrated } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (_hasHydrated && user && !allowedRoles.includes(user.role)) {
      router.push('/dashboard');
    }
  }, [user, allowedRoles, router, _hasHydrated]);

  return { user, isLoading: !_hasHydrated };
}

