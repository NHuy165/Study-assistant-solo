import { type LoginInput } from '@/features/auth/types/login';
import { LoginInputSchema } from '@/features/auth/types/login';
import { apiFetch } from '@/lib/api';
import { ResponseErrorSchema } from '@/types/error';
import { TokenSchema, type Token } from '@/features/auth/types/token';
import { useMutation } from '@tanstack/react-query';
import { useTokenStore } from '@/features/auth/stores/useTokenStore';
import { useNavigate } from 'react-router-dom';

const loginUserRequest = async (loginInput: LoginInput): Promise<Token> => {
  // Validates form input
  const validatedLoginInput = LoginInputSchema.safeParse(loginInput);

  if (!validatedLoginInput.success) {
    const errorMessage = validatedLoginInput.error.issues[0].message;
    throw new Error(errorMessage);
  }

  // Sends the request and catches operational errors
  const options = {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams(validatedLoginInput.data).toString(),
  };

  const response = await apiFetch('/login', options);
  const rawData = await response.json();

  // Catches backend response errors
  if (!response.ok) {
    const validatedError = ResponseErrorSchema.parse(rawData);
    throw new Error(validatedError.message);
  }

  // Returns
  const validatedData = TokenSchema.parse(rawData);
  return validatedData;
};

export const useLogin = () => {
  const setToken = useTokenStore((state) => state.setToken);
  const navigate = useNavigate();

  return useMutation({
    mutationFn: loginUserRequest,
    onSuccess: (data) => {
      setToken(data.access_token);
      navigate('/home', { replace: true });
    },
  });
};
