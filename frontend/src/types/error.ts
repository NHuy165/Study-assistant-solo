import { z } from 'zod';

export const ResponseErrorSchema = z.object({
  exception_type: z.string(),
  message: z.string(),
});

export type ResponseError = z.infer<typeof ResponseErrorSchema>;
