import {
  ChatOutputSchema,
  type ChatInput,
  type ChatOutput,
} from '@/features/chat/types/chat';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const createChatRequest = async ({
  interactionId,
  chatInput,
}: {
  interactionId: number;
  chatInput: ChatInput;
}): Promise<ChatOutput> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(chatInput),
  };

  const response = await apiFetchProtected(
    `/llm-response/${interactionId}`,
    options,
  );
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = ChatOutputSchema.parse(rawData);
  return validatedData;
};

export const useCreateChat = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createChatRequest,
    onSuccess: (_data, variables) =>
      queryClient.invalidateQueries({
        queryKey: ['chats', variables.interactionId],
      }),
  });
};
