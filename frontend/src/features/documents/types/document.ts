import { StudyActivityFormat, SubjectType } from '@/types/constants';
import { DocumentType } from '@/features/documents/types/constants';
import { z } from 'zod';

// ----- INPUT ----- //

export const DocumentInputSchema = z.object({
  file: z
    .custom<FileList>()
    .refine((files) => files && files.length === 1, 'A file is required.'),
  name: z.string().nullable(),
  subject_type: z.enum(SubjectType).nullable(),
  subject_type_overwrite: z.preprocess(
    (value) => typeof value === 'string' && value === 'true',
    z.boolean(),
  ),
});

export type DocumentInput = z.output<typeof DocumentInputSchema>;
export type DocumentInputForm = z.input<typeof DocumentInputSchema>;

// ----- BACKEND OUTPUT ----- //

// === Simple Output === //

export const DocumentOutputSchema = z.object({
  id: z.int(),
  interaction_id: z.int(),
  name: z.string().min(1),
  created_at: z.iso.datetime(),
  subject_type: z.enum(SubjectType),
  type: z.enum(DocumentType),
});

export type DocumentOutput = z.infer<typeof DocumentOutputSchema>;

// === Material Recommendation === //

const MaterialRecommendationSchema = z.object({
  prompt: z.string(),
  activity_format: z.enum(StudyActivityFormat),
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
  name: z.string().min(1),
  subject_type: z.enum(SubjectType),
});

export type DocumentUpdate = z.infer<typeof DocumentUpdateSchema>;
