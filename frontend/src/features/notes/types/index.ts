import { z } from 'zod';

export const NoteInputSchema = z.object({
  title: z.string(),
  content: z.string(),
});

export type NoteInputType = z.infer<typeof NoteInputSchema>;

export const NoteSchema = z.object({
  id: z.number(),
  title: z.string(),
  content: z.string(),
  created_at: z.iso.datetime(),
});

export type NoteType = z.infer<typeof NoteSchema>;

export type NotesState = {
  searchQuery: string;
  setSearchQuery: (s: string) => void;
};

export type NotesFormState = {
  title: string;
  setTitle: (s: string) => void;
  content: string;
  setContent: (s: string) => void;
};
