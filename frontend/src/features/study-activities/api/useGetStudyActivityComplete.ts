import {
  StudyActivityOutputCompleteSchema,
  type StudyActivityOutputComplete,
} from '@/features/study-activities/types/study-activity';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useQuery } from '@tanstack/react-query';

const getStudyActivityCompleteRequest = async (
  studyActivityId: number,
): Promise<StudyActivityOutputComplete> => {
  // Sends the request and catches operational errors
  const response = await apiFetchProtected(
    `/study-activity/${studyActivityId}/complete`,
  );
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = StudyActivityOutputCompleteSchema.parse(rawData);
  return validatedData;
};

export const useGetStudyActivityComplete = (studyActivityId: number) => {
  return useQuery({
    queryKey: ['study-activity', studyActivityId],
    queryFn: () => getStudyActivityCompleteRequest(studyActivityId),
  });
};
