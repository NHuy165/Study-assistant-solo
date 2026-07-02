import {
  CriterionAttribute,
  CriterionOperator,
} from '@/features/study-progress/types/constants';
import {
  StudyActivityFormat,
  StudyActivityFormatExercise,
  SubjectType,
} from '@/types/constants';
import { z } from 'zod';

// ----- INPUT ----- //

export const CriterionInputSchema = z.object({
  attribute: z.enum(CriterionAttribute),
  value: z
    .union([z.iso.datetime(), z.boolean(), z.int(), z.string()])
    .nullable(),
  operator: z.enum(CriterionOperator),
});

export type CriterionInput = z.infer<typeof CriterionInputSchema>;

export const CriteriaInputSchema = z.array(CriterionInputSchema);

export type CriteriaInput = z.infer<typeof CriteriaInputSchema>;

// ----- BACKEND OUTPUT ----- //

export const StudyProgressOutputSchema = z.array(
  z.array(z.union([z.iso.datetime(), z.boolean(), z.int(), z.string()])),
);

export type StudyProgressOutput = z.infer<typeof StudyProgressOutputSchema>;

// ----- REFORMAT ----- //

// === Objects by subject === //

const objectsGroupBySubjectShape = Object.fromEntries(
  Object.values(SubjectType).map((subject) => [subject, z.int()]),
);

export const ObjectsGroupBySubjectSchema = z.object(
  objectsGroupBySubjectShape as Record<SubjectType, z.ZodInt>,
);

export type ObjectsGroupBySubject = z.infer<typeof ObjectsGroupBySubjectSchema>;

// === Objects by format === //

const objectsGroupByFormatShape = Object.fromEntries(
  Object.values(StudyActivityFormat).map((format) => [format, z.int()]),
);

export const ObjectsGroupByFormatSchema = z.object(
  objectsGroupByFormatShape as Record<StudyActivityFormat, z.ZodInt>,
);

export type ObjectsGroupByFormat = z.infer<typeof ObjectsGroupByFormatSchema>;

// === Scores by subject === //

const scoresGroupBySubjectShape = Object.fromEntries(
  Object.values(SubjectType).map((subject) => [
    subject,
    z.tuple([z.float64(), z.float64()]),
  ]),
);

export const ScoresGroupBySubjectSchema = z.object(
  scoresGroupBySubjectShape as Record<
    SubjectType,
    z.ZodTuple<[z.ZodFloat64, z.ZodFloat64]>
  >,
);

export type ScoresGroupBySubject = z.infer<typeof ScoresGroupBySubjectSchema>;

// === Scores by format === //

const scoresGroupByFormatShape = Object.fromEntries(
  Object.values(StudyActivityFormatExercise).map((format) => [
    format,
    z.tuple([z.float64(), z.float64()]),
  ]),
);

export const ScoresGroupByFormatSchema = z.object(
  scoresGroupByFormatShape as Record<
    StudyActivityFormatExercise,
    z.ZodTuple<[z.ZodFloat64, z.ZodFloat64]>
  >,
);

export type ScoresGroupByFormat = z.infer<typeof ScoresGroupByFormatSchema>;
