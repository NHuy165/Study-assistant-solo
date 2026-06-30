import {
  type ExerciseItemAnswer,
  ExerciseItemOutputSchema,
} from '@/features/study-activities/types/study-activity';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const answerExerciseItemRequest = async ({
  exerciseItemId,
  exerciseItemAnswer,
}: {
  exerciseItemId: number;
  exerciseItemAnswer: ExerciseItemAnswer;
}) => {
  // Sends the request and catches operational errors
  const options = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(exerciseItemAnswer),
  };

  const response = await apiFetchProtected(
    `/study-activity/${exerciseItemId}/answer`,
    options,
  );
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = ExerciseItemOutputSchema.parse(rawData);
  return validatedData;
};

export const useAnswerExerciseItem = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: answerExerciseItemRequest,
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['study-activity', data.study_activity_id],
      });
    },
  });
};
