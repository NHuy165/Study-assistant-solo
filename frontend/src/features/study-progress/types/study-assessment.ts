import { z } from 'zod';

// ----- BACKEND OUTPUT ----- //

export const StudyAssessmentOutputSchema = z.object({
  assessment_of: z.iso.date(),
  content: z.string(),
  created_at: z.iso.datetime(),
});

export type StudyAssessmentOutput = z.infer<typeof StudyAssessmentOutputSchema>;
