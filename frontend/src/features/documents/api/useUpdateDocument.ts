import {
  DocumentOutputSchema,
  type DocumentOutput,
  type DocumentUpdate,
} from '@/features/documents/types/document';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const updateDocumentRequest = async ({
  documentId,
  documentUpdate,
}: {
  documentId: number;
  documentUpdate: DocumentUpdate;
}): Promise<DocumentOutput> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(documentUpdate),
  };

  const response = await apiFetchProtected(`/document/${documentId}`, options);
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = DocumentOutputSchema.parse(rawData);
  return validatedData;
};

export const useUpdateDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateDocumentRequest,
    onSuccess: (data, params) => {
      queryClient.invalidateQueries({
        queryKey: ['documents', data.interaction_id],
      });
      queryClient.invalidateQueries({
        queryKey: ['document', params.documentId],
      });
    },
  });
};
