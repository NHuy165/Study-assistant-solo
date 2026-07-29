import {
  StudyActivityOutputCompleteSchema,
  type StudyActivityOutputComplete,
} from '@/features/study-activities/types/study-activity';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const submitExerciseRequest = async (
  exerciseId: number,
): Promise<StudyActivityOutputComplete> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'PATCH',
  };

  const response = await apiFetchProtected(
    `/study-activity/${exerciseId}/submit`,
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

export const useSubmitExercise = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: submitExerciseRequest,
    onSuccess: (_data, param) => {
      queryClient.invalidateQueries({
        queryKey: ['study-activity', param],
      });
    },
  });
};
