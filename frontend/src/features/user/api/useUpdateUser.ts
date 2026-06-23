import {
  type UserOutput,
  UserOutputSchema,
  type UserUpdate,
} from '@/features/user/types/user';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation, useQueryClient } from '@tanstack/react-query';

const updateUserRequest = async (
  userUpdate: UserUpdate,
): Promise<UserOutput> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userUpdate),
  };

  const response = await apiFetchProtected('/user/me', options);
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

export const useUpdateUser = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: updateUserRequest,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['user'] }),
  });
};
