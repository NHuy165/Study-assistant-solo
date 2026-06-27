import {
  DocumentOutputCompleteSchema,
  type DocumentInput,
  type DocumentOutputComplete,
} from '@/features/documents/types/document';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const uploadDocumentRequest = async ({
  interactionId,
  documentInput,
}: {
  interactionId: number;
  documentInput: DocumentInput;
}): Promise<DocumentOutputComplete> => {
  // Sends the request and catches operational errors
  const { file, ...queryParams } = documentInput;

  const fileData = new FormData();
  fileData.append('file', file[0]);

  // Blank and null values get tossed
  const validEntries = Object.entries(queryParams)
    .filter(([, value]) => value !== null && value !== '')
    .map(([key, value]) => [key, String(value)]);

  const formattedQueryParams = new URLSearchParams(validEntries).toString();

  const options = {
    method: 'POST',
    body: fileData,
  };

  const response = await apiFetchProtected(
    `/document/${interactionId}${formattedQueryParams ? '?' + formattedQueryParams : ''}`,
    options,
  );
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

export const useUploadDocument = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: uploadDocumentRequest,
    onSuccess: (data, params) => {
      queryClient.invalidateQueries({
        queryKey: ['documents', params.interactionId],
      });
    },
  });
};
