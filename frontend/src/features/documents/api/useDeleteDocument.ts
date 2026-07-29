import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';

const deleteDocumentRequest = async (documentId: number): Promise<void> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'DELETE',
  };

  const response = await apiFetchProtected(`/document/${documentId}`, options);

  // Catches backend response errors
  if (!response.ok) {
    const rawData = await response.json();
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }
};

export const useDeleteDocument = () => {
  const queryClient = useQueryClient();
  const { interactionId } = useParams() as { interactionId: string };

  return useMutation({
    mutationFn: deleteDocumentRequest,
    onSuccess: (_data, param) => {
      queryClient.invalidateQueries({
        queryKey: ['documents', Number(interactionId)],
      });
      queryClient.invalidateQueries({
        queryKey: ['document', param],
      });
    },
  });
};
