import { type Page, type APIRequestContext } from '@playwright/test';

type ChatCreationType = {
  prompt: string;
};

export const mockCreateLlmResponse = async ({
  page,
  request,
  interactionId,
  chat,
}: {
  page: Page;
  request: APIRequestContext;
  interactionId: number;
  chat: ChatCreationType;
}) => {
  try {
    const token = await page.evaluate(() => {
      const storageData = window.localStorage.getItem('token-storage');
      const parsedStorageData = JSON.parse(storageData || 'null');
      return parsedStorageData?.state?.token as string | null;
    });

    if (!token) {
      throw new Error('Could not find token in Playwright store state.');
    }

    const response = await request.post(
      `${process.env.BASE_URL}/api/dev/llm-response/${interactionId}`,
      {
        data: { ...chat },
        headers: { Authorization: `Bearer ${token}` },
      },
    );

    if (!response.ok()) {
      const errorBody = await response.text();
      throw new Error(`Failed to create LLM response: ${errorBody}`);
    }

    const body = await response.json();

    return body;
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    throw new Error(`Failed to connect to server: ${errorMessage}`, {
      cause: e,
    });
  }
};
