import { useTokenStore } from '@/features/auth/stores/useTokenStore';
import { ResponseErrorSchema } from '@/types/error';

const API_URL: string = import.meta.env.VITE_API_URL;

export const apiFetch = async (
  url: string,
  options?: RequestInit,
): Promise<Response> => {
  let response: Response;

  // Tries connecting to the server
  try {
    response = await fetch(`${API_URL}${url}`, options);
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    throw new Error(`Failed to connect to server: ${errorMessage}`, {
      cause: e,
    });
  }

  // Checks if the response really contains json
  const isJson = response.headers
    .get('content-type')
    ?.includes('application/json');
  if (!isJson && response.status !== 204) {
    throw new Error('Invalid response data.');
  }

  return response;
};

export const apiFetchProtected = async (
  url: string,
  options?: RequestInit,
): Promise<Response> => {
  const token = useTokenStore.getState().token;

  // If token is missing
  if (!token) {
    window.location.href = '/auth/login';
    return new Promise(() => {});
  }

  // Auto injects token
  const headers = new Headers(options?.headers);
  headers.set('Authorization', `Bearer ${token}`);

  const updatedOptions: RequestInit = {
    ...options,
    headers,
  };

  const response = await apiFetch(url, updatedOptions);

  // If status code is 401
  if (response.status === 401) {
    // If exception type is AUTHENTICATION (user authentication problems)
    const clonedResponse = response.clone();

    const rawData = await clonedResponse.json();
    const validatedError = ResponseErrorSchema.parse(rawData);

    if (validatedError.exception_type === 'AUTHENTICATION') {
      useTokenStore.getState().setToken(null);
      window.location.href = '/auth/login';

      // Returns a frozen promise so more code doesn't execute when being redirected
      return new Promise(() => {});
    }
  }

  return response;
};
