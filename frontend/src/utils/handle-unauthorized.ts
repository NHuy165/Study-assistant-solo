import { useTokenStore } from '@/features/auth/stores/useTokenStore';

export const handleUnauthorized = () => {
  useTokenStore.getState().setToken(null);

  window.location.href = '/auth/login';
};
