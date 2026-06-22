import {
  type InteractionOutput,
  InteractionOutputSchema,
} from '@/features/interactions/types/interaction';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';

const getInteractionsRequest = async (): Promise<InteractionOutput[]> => {
  // Sends the request and catches operational errors
  const response = await apiFetchProtected('/interaction/');
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = z.array(InteractionOutputSchema).parse(rawData);
  return validatedData;
};

export const useGetInteractions = () => {
  return useQuery({
    queryKey: ['interactions'],
    queryFn: getInteractionsRequest,
  });
};
