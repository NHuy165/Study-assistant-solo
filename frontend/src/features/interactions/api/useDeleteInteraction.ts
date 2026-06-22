import { useInteractionStore } from '@/features/interactions/stores/useInteractionStore';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const deleteInteractionRequest = async (id: number): Promise<void> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'DELETE',
  };

  const response = await apiFetchProtected(`/interaction/${id}`, options);

  // Catches backend response errors
  if (!response.ok) {
    const rawData = await response.json();
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }
};

export const useDeleteInteraction = () => {
  const queryClient = useQueryClient();
  const resetUpdate = useInteractionStore((state) => state.resetUpdate);

  return useMutation({
    mutationFn: deleteInteractionRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['interactions'] });
      resetUpdate();
    },
  });
};
