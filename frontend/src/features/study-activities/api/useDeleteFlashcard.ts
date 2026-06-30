import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';

const deleteFlashcardRequest = async (reviewItemId: number): Promise<void> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'DELETE',
  };

  const response = await apiFetchProtected(
    `/study-activity/flashcards/${reviewItemId}`,
    options,
  );

  // Catches backend response errors
  if (!response.ok) {
    const rawData = await response.json();
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }
};

export const useDeleteFlashcard = () => {
  const queryClient = useQueryClient();
  const { studyActivityId } = useParams();

  return useMutation({
    mutationFn: deleteFlashcardRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['study-activity', Number(studyActivityId)],
      });
    },
  });
};
