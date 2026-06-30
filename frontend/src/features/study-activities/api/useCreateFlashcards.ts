import {
  StudyActivityOutputCompleteSchema,
  type FlashcardsInput,
  type StudyActivityOutputComplete,
} from '@/features/study-activities/types/study-activity';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const createFlashcardsRequest = async ({
  reviewActivityId,
  flashcardsInput,
}: {
  reviewActivityId: number;
  flashcardsInput: FlashcardsInput;
}): Promise<StudyActivityOutputComplete> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(flashcardsInput),
  };

  const response = await apiFetchProtected(
    `/study-activity/${reviewActivityId}/add-cards`,
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

export const useCreateFlashcards = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createFlashcardsRequest,
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['study-activity', data.id],
      });
    },
  });
};
