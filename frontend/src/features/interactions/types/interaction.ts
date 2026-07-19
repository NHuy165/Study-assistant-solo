import { z } from 'zod';

// ----- INPUT ----- //

export const InteractionInputSchema = z.object({
  name: z.string().min(1),
  description: z.string(),
});

export type InteractionInput = z.infer<typeof InteractionInputSchema>;

// ----- BACKEND OUTPUT ----- //

export const InteractionOutputSchema = z.object({
  name: z.string().min(1),
  description: z.string(),
  id: z.int(),
  created_at: z.iso.datetime(),
});

export type InteractionOutput = z.infer<typeof InteractionOutputSchema>;

// ----- UPDATE ----- //

export const InteractionUpdateSchema = z.object({
  name: z.string().min(1),
  description: z.string(),
});

export type InteractionUpdate = z.infer<typeof InteractionUpdateSchema>;
