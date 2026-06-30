import {
  StudyActivityOutputSchema,
  type StudyActivityOutput,
} from '@/features/study-activities/types/study-activity';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';

const getStudyActivitiesRequest = async (
  interactionId: number,
): Promise<StudyActivityOutput[]> => {
  // Sends the request and catches operational errors
  const response = await apiFetchProtected(`/study-activity/${interactionId}`);
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = z.array(StudyActivityOutputSchema).parse(rawData);
  return validatedData;
};

export const useGetStudyActivities = (interactionId: number) => {
  return useQuery({
    queryKey: ['study-activities', interactionId],
    queryFn: () => getStudyActivitiesRequest(interactionId),
  });
};
