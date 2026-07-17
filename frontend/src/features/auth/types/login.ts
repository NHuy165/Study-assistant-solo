import { z } from 'zod';

// ----- INPUT ----- //

export const LoginInputSchema = z.object({
  username: z.email().min(1), // username receives the registered email, not the registered username
  password: z.string().min(1),
});

export type LoginInput = z.infer<typeof LoginInputSchema>;
