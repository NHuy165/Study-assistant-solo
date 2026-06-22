import { z } from 'zod';

// ----- BACKEND OUTPUT ----- //

export const TokenSchema = z.object({
  access_token: z.string(),
  token_type: z.string(),
});

export type Token = z.infer<typeof TokenSchema>;

// ----- STORE STATE ----- //

export type TokenState = {
  token: string | null;
  setToken: (s: string | null) => void;
};
