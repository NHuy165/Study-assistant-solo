import { useInteractionStore } from '@/features/interactions/stores/useInteractionStore';
import {
  type InteractionInput,
  InteractionInputSchema,
  type InteractionOutput,
  InteractionOutputSchema,
} from '@/features/interactions/types/interaction';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const createInteractionRequest = async (
  interactionInput: InteractionInput,
): Promise<InteractionOutput> => {
  // Validates form input
  const validatedInteractionInput =
    InteractionInputSchema.safeParse(interactionInput);

  if (!validatedInteractionInput.success) {
    const errorMessage = validatedInteractionInput.error.issues[0].message;
    throw new Error(errorMessage);
  }

  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(validatedInteractionInput.data),
  };

  const response = await apiFetchProtected('/interaction/create', options);
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

export const useCreateInteraction = () => {
  const queryClient = useQueryClient();
  const resetCreate = useInteractionStore((state) => state.resetCreate);

  return useMutation({
    mutationFn: createInteractionRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['interactions'] });
      resetCreate();
    },
  });
};
