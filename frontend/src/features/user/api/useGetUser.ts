import { type UserOutput, UserOutputSchema } from '@/features/user/types/user';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useQuery } from '@tanstack/react-query';

const getUserRequest = async (): Promise<UserOutput> => {
  // Sends the request and catches operational errors
  const response = await apiFetchProtected('/user/me');
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = UserOutputSchema.parse(rawData);
  return validatedData;
};

export const useGetUser = () => {
  return useQuery({
    queryKey: ['user'],
    queryFn: getUserRequest,
  });
};
