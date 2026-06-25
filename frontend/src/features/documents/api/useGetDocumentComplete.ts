import {
  DocumentOutputCompleteSchema,
  type DocumentOutputComplete,
} from '@/features/documents/types/document';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useQuery } from '@tanstack/react-query';

const getDocumentCompleteRequest = async (
  documentId: number,
): Promise<DocumentOutputComplete> => {
  // Sends the request and catches operational errors
  const response = await apiFetchProtected(`/document/${documentId}/complete`);
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = DocumentOutputCompleteSchema.parse(rawData);
  return validatedData;
};

export const useGetDocumentComplete = (
  documentId: number,
  enabled: boolean,
) => {
  return useQuery({
    queryKey: ['document', documentId],
    queryFn: () => getDocumentCompleteRequest(documentId),
    enabled: enabled,
  });
};
