/// <reference types="node" />
import { APIRequestContext } from '@playwright/test';

export const resetDatabase = async (request: APIRequestContext) => {
  try {
    const response = await request.post(
      `${process.env.VITE_API_URL}/dev/wipe-db`,
    );
    if (!response.ok()) {
      const errorBody = await response.text();
      throw new Error(`Failed to reset database: ${errorBody}`);
    }
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    throw new Error(`Failed to connect to server: ${errorMessage}`, {
      cause: e,
    });
  }
};
