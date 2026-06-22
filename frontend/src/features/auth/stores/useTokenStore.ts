import { type TokenState } from '@/features/auth/types/token';
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useTokenStore = create<TokenState>()(
  persist(
    (set) => ({
      token: null,
      setToken: (s: string | null) => set({ token: s }),
    }),
    {
      name: 'token-storage',
    },
  ),
);
