import { create } from 'zustand';
import type { NotesState } from '../types';

export const useNotesStore = create<NotesState>((set) => ({
  searchQuery: '',
  setSearchQuery: (s: string) => set({ searchQuery: s }),
}));
