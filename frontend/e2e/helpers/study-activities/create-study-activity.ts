import { type Page, type APIRequestContext } from '@playwright/test';

type FlashcardCreationType = {
  name: string;
  description: string;
  subject_type: string;
};

export const createStudyActivities = async ({
  page,
  request,
  interactionId,
  flashcard,
}: {
  page: Page;
  request: APIRequestContext;
  interactionId: number;
  flashcard: FlashcardCreationType;
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
      `${process.env.VITE_API_URL}/study-activity/${interactionId}/flashcards`,
      {
        data: { ...flashcard },
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    if (!response.ok()) {
      const errorBody = await response.text();
      throw new Error(`Failed to create flashcard activity: ${errorBody}`);
    }
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    throw new Error(`Failed to connect to server: ${errorMessage}`, {
      cause: e,
    });
  }
};
