import { create } from 'zustand';
import { type RegisterFormState } from '@/features/auth/types/register';

export const useRegisterStore = create<RegisterFormState>((set) => ({
  username: '',
  email: '',
  description: '',
  password: '',

  setUsername: (s: string) => set({ username: s }),
  setEmail: (s: string) => set({ email: s }),
  setDescription: (s: string) => set({ description: s }),
  setPassword: (s: string) => set({ password: s }),
}));
