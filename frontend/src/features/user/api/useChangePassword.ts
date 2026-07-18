import { type UserPasswordChange } from '@/features/user/types/user';
import { apiFetchProtected } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation } from '@tanstack/react-query';

const changePasswordRequest = async (
  passwordChange: UserPasswordChange,
): Promise<void> => {
  // Sends the request and catches operational errors
  const options = {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(passwordChange),
  };

  const response = await apiFetchProtected('/user/change-password', options);

  // Catches backend response errors
  if (!response.ok) {
    const rawData = await response.json();
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }
};

export const useChangePassword = () => {
  return useMutation({
    mutationFn: changePasswordRequest,
  });
};
