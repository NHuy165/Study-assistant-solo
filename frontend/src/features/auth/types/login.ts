import { z } from 'zod';

// ----- INPUT ----- //

export const LoginInputSchema = z.object({
  username: z.email(), // username receives the registered email, not the registered username
  password: z.string(),
});

export type LoginInput = z.infer<typeof LoginInputSchema>;

// ----- STORE STATE ----- //

export type LoginFormState = LoginInput & {
  username: string;
  password: string;

  setUsername: (s: string) => void;
  setPassword: (s: string) => void;
};
