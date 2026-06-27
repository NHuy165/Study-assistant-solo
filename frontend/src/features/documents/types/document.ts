import { SubjectType, DocumentType } from '@/types/constants';
import { z } from 'zod';

// ----- INPUT ----- //

export const DocumentInputSchema = z
  .object({
    file: z
      .custom<FileList>()
      .refine((files) => files && files.length === 1, 'A file is required.'),
    name: z.string().nullable(),
    page_starts_at: z.int().nullable(),
    subject_type: z.enum(SubjectType).nullable(),
    subject_type_overwrite: z.boolean().nullable(),
  })
  .refine(
    (data) => {
      if (data.subject_type !== null && data.subject_type_overwrite === true) {
        return false;
      }
      return true;
    },
    {
      error: 'Overwrite not available when a subject type is already selected.',
      path: ['subject_type_overwrite'],
    },
  );

export type DocumentInput = z.infer<typeof DocumentInputSchema>;

// ----- BACKEND OUTPUT ----- //

// === Simple Output === //

export const DocumentOutputSchema = z.object({
  id: z.int(),
  name: z.string(),
  page_starts_at: z.int(),
  created_at: z.iso.datetime(),
  subject_type: z.enum(SubjectType).nullable(),
  type: z.enum(DocumentType),
});

export type DocumentOutput = z.infer<typeof DocumentOutputSchema>;

// === Material Recommendation === //

const MaterialRecommendationSchema = z.object({
  prompt: z.string(),
  activity_format: z.string(),
  subject_type: z.enum(SubjectType),
});

// === Question Recommendaion === //

const QuestionRecommendationSchema = z.object({
  prompt: z.string(),
});

// === Document Analysis === //

const DocumentAnalysisOutputSchema = z.object({
  summary: z.string(),
  material_recommendations: z.array(MaterialRecommendationSchema),
  question_recommendations: z.array(QuestionRecommendationSchema),
});

// === Complete Output === //

export const DocumentOutputCompleteSchema = z.tuple([
  DocumentOutputSchema,
  DocumentAnalysisOutputSchema.nullable(),
]);

export type DocumentOutputComplete = z.infer<
  typeof DocumentOutputCompleteSchema
>;

// ----- UPDATE ----- //

export const DocumentUpdateSchema = z.object({
  name: z.string(),
  page_starts_at: z.int(),
  subject_type: z.enum(SubjectType),
});

export type DocumentUpdate = z.infer<typeof DocumentUpdateSchema>;
