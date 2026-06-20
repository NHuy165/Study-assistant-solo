import { useMutation, useQueryClient } from '@tanstack/react-query';
import type { NoteInputType, NoteType } from '../types';
import { NoteSchema } from '../types';

const baseUrl = 'http://localhost:8000';

const createNoteRequest = async (data: NoteInputType): Promise<NoteType> => {
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  };

  const response = await fetch(`${baseUrl}/notes`, options);
  if (!response.ok) {
    throw new Error('Failed to create note');
  }

  const raw_data = await response.json();
  const validatedData = NoteSchema.parse(raw_data);

  return validatedData;
};

export const useCreateNotes = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createNoteRequest,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['notes'] });
    },
  });
};
