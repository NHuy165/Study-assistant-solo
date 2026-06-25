import {
  DocumentOutputSchema,
  type DocumentOutput,
} from '@/features/documents/types/document';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useQuery } from '@tanstack/react-query';
import { z } from 'zod';

const getDocumentsRequest = async (
  interactionId: number,
): Promise<DocumentOutput[]> => {
  // Sends the request and catches operational errors
  const response = await apiFetchProtected(`/document/${interactionId}/`);
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = z.array(DocumentOutputSchema).parse(rawData);
  return validatedData;
};

export const useGetDocuments = (interactionId: number) => {
  return useQuery({
    queryKey: ['documents', interactionId],
    queryFn: () => getDocumentsRequest(interactionId),
  });
};
