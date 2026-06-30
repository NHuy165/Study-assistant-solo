import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams } from 'react-router-dom';

const deleteStudyActivityRequest = async (
  studyActivityId: number,
): Promise<void> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'DELETE',
  };

  const response = await apiFetchProtected(
    `/study-activity/${studyActivityId}`,
    options,
  );

  // Catches backend response errors
  if (!response.ok) {
    const rawData = await response.json();
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }
};

export const useDeleteStudyActivity = () => {
  const queryClient = useQueryClient();
  const { interactionId } = useParams();

  return useMutation({
    mutationFn: deleteStudyActivityRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ['study-activities', Number(interactionId)],
      });
    },
  });
};
