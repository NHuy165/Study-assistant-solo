import {
  type InteractionInput,
  type InteractionOutput,
  InteractionOutputSchema,
} from '@/features/interactions/types/interaction';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const createInteractionRequest = async (
  interactionInput: InteractionInput,
): Promise<InteractionOutput> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(interactionInput),
  };

  const response = await apiFetchProtected('/interaction', options);
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

  return useMutation({
    mutationFn: createInteractionRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['interactions'] });
    },
  });
};
