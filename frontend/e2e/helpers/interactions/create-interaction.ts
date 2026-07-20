import { type APIRequestContext, type Page } from '@playwright/test';

type InteractionCreationType = {
  name: string;
  description: string;
};

export const createInteraction = async ({
  page,
  request,
  interaction,
}: {
  page: Page;
  request: APIRequestContext;
  interaction: InteractionCreationType;
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
      `${process.env.VITE_API_URL}/interaction`,
      {
        data: { ...interaction },
        headers: { Authorization: `Bearer ${token}` },
      },
    );

    if (!response.ok()) {
      const errorBody = await response.text();
      throw new Error(`Failed to create interaction: ${errorBody}`);
    }
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    throw new Error(`Failed to connect to server: ${errorMessage}`, {
      cause: e,
    });
  }
};
