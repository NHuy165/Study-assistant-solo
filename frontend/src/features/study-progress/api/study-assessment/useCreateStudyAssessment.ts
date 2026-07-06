import {
  StudyAssessmentOutputSchema,
  type StudyAssessmentOutput,
} from '@/features/study-progress/types/study-assessment';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { z } from 'zod';

const createStudyAssessmentRequest = async (): Promise<
  StudyAssessmentOutput[]
> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
  };

  const response = await apiFetchProtected(
    '/study-progress/study-assessment',
    options,
  );
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

export const useCreateStudyAssessment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createStudyAssessmentRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['study-assessments'],
      });
    },
  });
};
