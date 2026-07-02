import {
  StudyAssessmentOutputSchema,
  type StudyAssessmentOutput,
} from '@/features/study-progress/types/study-assessment';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';

const getStudyAssessmentsRequest = async (): Promise<
  StudyAssessmentOutput[]
> => {
  // Sends the request and catches operational errors
  const response = await apiFetchProtected('/study-progress/study-assessment');
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = z.array(StudyAssessmentOutputSchema).parse(rawData);
  return validatedData;
};

export const useGetStudyAssessments = () => {
  return useQuery({
    queryKey: ['study-assessments'],
    queryFn: getStudyAssessmentsRequest,
  });
};
