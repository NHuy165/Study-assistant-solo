import { z } from 'zod';

// ----- INPUT ----- //

export const InteractionInputSchema = z.object({
  name: z.string(),
  description: z.string().optional(),
});

export type InteractionInput = z.infer<typeof InteractionInputSchema>;

// ----- BACKEND OUTPUT ----- //

export const InteractionOutputSchema = z.object({
  name: z.string(),
  description: z.string(),
  id: z.int(),
  created_at: z.iso.datetime(),
});

export type InteractionOutput = z.infer<typeof InteractionOutputSchema>;

// ----- UPDATE ----- //

export const InteractionUpdateSchema = z.object({
  name: z.string(),
  description: z.string(),
});

export type InteractionUpdate = z.infer<typeof InteractionUpdateSchema>;

// ----- STORE STATE ----- //

export type InteractionFormState = {
  // Create
  createName: string;
  createDescription: string;

  setCreateName: (s: string) => void;
  setCreateDescription: (s: string) => void;
  resetCreate: () => void;

  // Update
  updateId: number | null;
  updateName: string;
  updateDescription: string;

  setUpdateName: (s: string) => void;
  setUpdateDescription: (s: string) => void;
  setUpdateId: (n: number | null) => void;
  resetUpdate: () => void;
};
