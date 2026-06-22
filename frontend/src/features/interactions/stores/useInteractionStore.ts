import { type InteractionFormState } from '@/features/interactions/types/interaction';
import { create } from 'zustand';

export const useInteractionStore = create<InteractionFormState>((set) => ({
  // Create
  createName: '',
  createDescription: '',

  setCreateName: (s: string) => set({ createName: s }),
  setCreateDescription: (s: string) => set({ createDescription: s }),
  resetCreate: () =>
    set({
      createName: '',
      createDescription: '',
    }),

  // Update
  updateId: null,
  updateName: '',
  updateDescription: '',

  setUpdateName: (s: string) => set({ updateName: s }),
  setUpdateDescription: (s: string) => set({ updateDescription: s }),
  setUpdateId: (n: number | null) => set({ updateId: n }),
  resetUpdate: () =>
    set({
      updateId: null,
      updateName: '',
      updateDescription: '',
    }),
}));
