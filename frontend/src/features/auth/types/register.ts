import { z } from 'zod';

// ----- INPUT ----- //

export const RegisterInputSchema = z.object({
  username: z.string(),
  email: z.email(),
  description: z.string(),
  password: z.string().min(1),
});

export type RegisterInput = z.infer<typeof RegisterInputSchema>;

// ----- STORE STATE ----- //

export type RegisterFormState = {
  username: string;
  email: string;
  description: string;
  password: string;

  setUsername: (s: string) => void;
  setEmail: (s: string) => void;
  setDescription: (s: string) => void;
  setPassword: (s: string) => void;
};
