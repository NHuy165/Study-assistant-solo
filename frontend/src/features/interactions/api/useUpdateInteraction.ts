import { useInteractionStore } from '@/features/interactions/stores/useInteractionStore';
import {
  type InteractionOutput,
  InteractionOutputSchema,
  type InteractionUpdate,
  InteractionUpdateSchema,
} from '@/features/interactions/types/interaction';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const updateInteractionRequest = async ({
  id,
  interactionUpdate,
}: {
  id: number;
  interactionUpdate: InteractionUpdate;
}): Promise<InteractionOutput> => {
  // Validates form input
  const validatedInteractionUpdate =
    InteractionUpdateSchema.safeParse(interactionUpdate);

  if (!validatedInteractionUpdate.success) {
    const errorMessage = validatedInteractionUpdate.error.issues[0].message;
    throw new Error(errorMessage);
  }

  // Sends the request and catches operational errors
  const options = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(validatedInteractionUpdate.data),
  };

  const response = await apiFetchProtected(`/interaction/${id}`, options);
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = InteractionOutputSchema.parse(rawData);
  return validatedData;
};

export const useUpdateInteraction = () => {
  const queryClient = useQueryClient();
  const resetUpdate = useInteractionStore((state) => state.resetUpdate);

  return useMutation({
    mutationFn: updateInteractionRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['interactions'] });
      resetUpdate();
    },
  });
};
