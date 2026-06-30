import {
  StudyActivityOutputSchema,
  type FlashcardsActivityInput,
  type StudyActivityOutput,
} from '@/features/study-activities/types/study-activity';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const createFlashcardsActivity = async ({
  interactionId,
  flashcardsActivityInput,
}: {
  interactionId: number;
  flashcardsActivityInput: FlashcardsActivityInput;
}): Promise<StudyActivityOutput> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(flashcardsActivityInput),
  };

  const response = await apiFetchProtected(
    `/study-activity/${interactionId}/flashcards`,
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

export const useCreateFlashcardsActivity = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createFlashcardsActivity,
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['study-activities', data.interaction_id],
      });
    },
  });
};
