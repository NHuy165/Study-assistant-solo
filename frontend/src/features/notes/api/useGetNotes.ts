import { useQuery } from '@tanstack/react-query';
import { NoteSchema } from '../types';
import type { NoteType } from '../types';
import { z } from 'zod';

const baseUrl = 'http://localhost:8000';

const getNotesRequest = async (): Promise<NoteType[]> => {
  const response = await fetch(`${baseUrl}/api/notes`);
  if (!response.ok) {
    throw new Error('Failed to fetch notes');
  }
  const rawData = await response.json();
  const validatedData: NoteType[] = z.array(NoteSchema).parse(rawData);

  return validatedData;
};

export const useGetNotes = () => {
  return useQuery({
    queryKey: ['notes'],
    queryFn: getNotesRequest,
    refetchOnWindowFocus: false,
  });
};
