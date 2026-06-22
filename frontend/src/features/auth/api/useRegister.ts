import { apiFetch } from '@/lib/api';
import {
  RegisterInputSchema,
  type RegisterInput,
} from '@/features/auth/types/register';
import { ResponseErrorSchema } from '@/types/error';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';

const registerUserRequest = async (
  registerInput: RegisterInput,
): Promise<void> => {
  // Validates form input
  const validatedRegisterInput = RegisterInputSchema.safeParse(registerInput);

  if (!validatedRegisterInput.success) {
    const errorMessage = validatedRegisterInput.error.issues[0].message;
    throw new Error(errorMessage);
  }

  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(validatedRegisterInput.data),
  };

  const response = await apiFetch('/user/register', options);

  // Catches backend response errors
  if (!response.ok) {
    const rawData = await response.json();
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }
};

export const useRegister = () => {
  const navigate = useNavigate();

  return useMutation({
    mutationFn: registerUserRequest,
    onSuccess: () => navigate('/auth/login', { replace: true }),
  });
};
