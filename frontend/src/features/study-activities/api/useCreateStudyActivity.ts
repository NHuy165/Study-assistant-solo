import {
  StudyActivityOutputCompleteSchema,
  type StudyActivityInput,
  type StudyActivityOutputComplete,
} from '@/features/study-activities/types/study-activity';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const createStudyActivityRequest = async ({
  interactionId,
  studyActivityInput,
}: {
  interactionId: number;
  studyActivityInput: StudyActivityInput;
}): Promise<StudyActivityOutputComplete> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(studyActivityInput),
  };

  const response = await apiFetchProtected(
    `/study-activity/${interactionId}`,
    options,
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

export const useCreateStudyActivity = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createStudyActivityRequest,
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['study-activities', data.interaction_id],
      });
    },
  });
};
