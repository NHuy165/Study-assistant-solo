import {
  ReviewItemOutputSchema,
  type FlashcardUpdate,
  type ReviewItemOutput,
} from '@/features/study-activities/types/study-activity';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const updateFlashcardRequest = async ({
  reviewItemId,
  flashcardUpdate,
}: {
  reviewItemId: number;
  flashcardUpdate: FlashcardUpdate;
}): Promise<ReviewItemOutput> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(flashcardUpdate),
  };

  const response = await apiFetchProtected(
    `/study-activity/flashcards/${reviewItemId}`,
    options,
  );
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = ReviewItemOutputSchema.parse(rawData);
  return validatedData;
};

export const useUpdateFlashcard = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateFlashcardRequest,
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ['study-activity', data.study_activity_id],
      });
    },
  });
};
