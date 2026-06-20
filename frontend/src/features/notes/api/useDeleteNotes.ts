import { useMutation, useQueryClient } from '@tanstack/react-query';

const baseUrl = 'http://localhost:8000';

const deleteNoteRequest = async (id: number): Promise<void> => {
  const options = {
    method: 'DELETE',
  };

  const response = await fetch(`${baseUrl}/notes/${id}`, options);
  if (!response.ok) {
    throw new Error('Failed to create note');
  }
};

export const useCreateNotes = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteNoteRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notes'] });
    },
  });
};
