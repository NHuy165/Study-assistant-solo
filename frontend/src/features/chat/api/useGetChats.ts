import { ChatOutputSchema, type ChatOutput } from '@/features/chat/types/chat';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';

const getChatsRequest = async (
  interactionId: number,
): Promise<ChatOutput[]> => {
  // Sends the request and catches operational errors
  const response = await apiFetchProtected(`/llm-response/${interactionId}`);
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = z.array(ChatOutputSchema).parse(rawData);
  return validatedData;
};

export const useGetChats = (interactionId: number) => {
  return useQuery({
    queryKey: ['chats', interactionId],
    queryFn: () => getChatsRequest(interactionId),
  });
};
