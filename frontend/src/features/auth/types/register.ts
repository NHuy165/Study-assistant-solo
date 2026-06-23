import { z } from 'zod';

// ----- INPUT ----- //

export const RegisterInputSchema = z.object({
  username: z.string(),
  email: z.email(),
  description: z.string().optional(),
  password: z.string().min(1),
});

export type RegisterInput = z.infer<typeof RegisterInputSchema>;
