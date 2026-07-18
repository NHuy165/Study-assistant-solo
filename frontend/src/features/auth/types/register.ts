import { z } from 'zod';

// ----- INPUT ----- //

export const RegisterInputSchema = z.object({
  username: z.string().min(1),
  email: z.email().min(1),
  description: z.string(),
  password: z.string().min(1),
});

export type RegisterInput = z.infer<typeof RegisterInputSchema>;
