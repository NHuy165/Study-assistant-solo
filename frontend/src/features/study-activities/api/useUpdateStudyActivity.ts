import {
  StudyActivityOutputSchema,
  type StudyActivityOutput,
  type StudyActivityUpdate,
} from '@/features/study-activities/types/study-activity';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const updateStudyActivityRequest = async ({
  studyActivityId,
  studyActivityUpdate,
}: {
  studyActivityId: number;
  studyActivityUpdate: StudyActivityUpdate;
}): Promise<StudyActivityOutput> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(studyActivityUpdate),
  };

  const response = await apiFetchProtected(
    `/study-activity/${studyActivityId}`,
    options,
  );
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = StudyActivityOutputSchema.parse(rawData);
  return validatedData;
};

export const useUpdateStudyActivity = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateStudyActivityRequest,
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['study-activities', data.interaction_id],
      });
    },
  });
};
