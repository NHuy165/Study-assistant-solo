import { z } from 'zod';

// ----- BACKEND OUTPUT ----- //

export const UserOutputSchema = z.object({
  id: z.number(),

  username: z.string(),
  email: z.email(),
  description: z.string(),

  created_at: z.iso.datetime(),
  login_streak: z.int(),
  longest_login_streak: z.int(),
});

export type UserOutput = z.infer<typeof UserOutputSchema>;

// ----- UPDATE ----- //

export const UserUpdateSchema = z.object({
  username: z.string(),
  email: z.email(),
  description: z.string(),
});

export type UserUpdate = z.infer<typeof UserUpdateSchema>;

export const UserPasswordChangeSchema = z.object({
  old_password: z.string().min(1),
  new_password: z.string().min(1),
});

export type UserPasswordChange = z.infer<typeof UserPasswordChangeSchema>;
