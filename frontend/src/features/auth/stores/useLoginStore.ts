import { create } from 'zustand';
import { type LoginFormState } from '@/features/auth/types/login';

export const useLoginStore = create<LoginFormState>((set) => ({
  username: '',
  password: '',
  setUsername: (s: string) => set({ username: s }),
  setPassword: (s: string) => set({ password: s }),
}));
