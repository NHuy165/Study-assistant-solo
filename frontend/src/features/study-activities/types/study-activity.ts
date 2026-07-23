import {
  ExerciseItemContentType,
  ReviewItemContentType,
  StudyActivityFormat,
  StudyActivityType,
  SubjectType,
} from '@/types/constants';
import { z } from 'zod';

// ----- INPUT ----- //

export const StudyActivityInputSchema = z.object({
  prompt: z.string(),
  activity_format: z.enum(StudyActivityFormat),
  subject_type: z.enum(SubjectType),
  document_id: z.int().nullable(),
});

export type StudyActivityInput = z.infer<typeof StudyActivityInputSchema>;

export const FlashcardsActivityInputSchema = z.object({
  subject_type: z.enum(SubjectType),
  name: z.string().min(1),
  description: z.string(),
});

export type FlashcardsActivityInput = z.infer<
  typeof FlashcardsActivityInputSchema
>;

export const FlashcardInputSingleSchema = z.object({
  front: z.string(),
  back: z.string(),
});

export type FlashcardInputSingle = z.infer<typeof FlashcardInputSingleSchema>;

export const FlashcardsInputSchema = z.array(FlashcardInputSingleSchema);

export type FlashcardsInput = z.infer<typeof FlashcardsInputSchema>;

// ----- BACKEND OUTPUT ----- //

// === Basic output === //

export const StudyActivityOutputSchema = z.object({
  id: z.int(),
  interaction_id: z.int(),
  name: z.string(),
  description: z.string(),
  subject_type: z.enum(SubjectType),
  is_submitted: z.boolean(),
  created_at: z.iso.datetime(),
  submitted_at: z.iso.datetime().nullable(),

  prompt: z.string().nullable(),
  activity_type: z.enum(StudyActivityType),
  activity_format: z.enum(StudyActivityFormat),
});

export type StudyActivityOutput = z.infer<typeof StudyActivityOutputSchema>;

// === Exercise === //

const ExerciseItemContentOutputSchema = z.object({
  id: z.int(),
  type: z.enum(ExerciseItemContentType),
  content: z.string().nullable(),
  is_correct: z.boolean().nullable(),
});

export const ExerciseItemOutputSchema = z.object({
  id: z.int(),
  study_activity_id: z.int(),
  question: z.string(),
  max_score: z.float64(),

  user_score: z.float64().nullable(),
  explanation: z.string().nullable(),
  attempt: z.string().nullable(),

  contents: z.array(ExerciseItemContentOutputSchema),
});

export type ExerciseItemOutput = z.infer<typeof ExerciseItemOutputSchema>;

// === Review === //

const ReviewItemContentOutputSchema = z.object({
  id: z.int(),
  type: z.enum(ReviewItemContentType),
  content: z.string(),
});

export const ReviewItemOutputSchema = z.object({
  id: z.int(),
  study_activity_id: z.int(),
  contents: z.array(ReviewItemContentOutputSchema),
});

export type ReviewItemOutput = z.infer<typeof ReviewItemOutputSchema>;

// === Complete output === //

export const StudyActivityOutputCompleteSchema =
  StudyActivityOutputSchema.extend({
    items: z.array(z.union([ExerciseItemOutputSchema, ReviewItemOutputSchema])),
  });

export type StudyActivityOutputComplete = z.infer<
  typeof StudyActivityOutputCompleteSchema
>;

// ----- UPDATE ----- //

export const StudyActivityUpdateSchema = z.object({
  name: z.string().min(1),
  description: z.string(),
});

export type StudyActivityUpdate = z.infer<typeof StudyActivityUpdateSchema>;

export const ExerciseItemAnswerSchema = z.object({
  attempt: z.union([z.int(), z.string()]),
});

export type ExerciseItemAnswer = z.infer<typeof ExerciseItemAnswerSchema>;

export const FlashcardUpdateSchema = z.object({
  front: z.string(),
  back: z.string(),
});

export type FlashcardUpdate = z.infer<typeof FlashcardUpdateSchema>;
