import { z } from 'zod';

// ----- INPUT ----- //

export const ChatInputSchema = z.object({
  prompt: z.string(),
  document_id: z.int().nullable(),
});

export type ChatInput = z.infer<typeof ChatInputSchema>;

// ----- BACKEND OUTPUT ----- //

export const ChatOutputSchema = z.object({
  id: z.int(),
  interaction_id: z.int(),
  prompt: z.string(),
  answer: z.string(),
  created_at: z.iso.datetime(),
});

export type ChatOutput = z.infer<typeof ChatOutputSchema>;
