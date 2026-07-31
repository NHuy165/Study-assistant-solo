/// <reference types="node" />
import { type APIRequestContext } from '@playwright/test';

type UserRegisterType = {
  username: string;
  email: string;
  password: string;
  description: string;
};

export const registerUser = async ({
  request,
  user,
}: {
  request: APIRequestContext;
  user: UserRegisterType;
}) => {
  try {
    const response = await request.post(
      `${process.env.BASE_URL}/api/user/register`,
      {
        data: { ...user },
      },
    );
    if (!response.ok()) {
      const errorBody = await response.text();
      throw new Error(`Failed to register user: ${errorBody}`);
    }
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    throw new Error(`Failed to connect to server: ${errorMessage}`, {
      cause: e,
    });
  }
};
