import { type Page, type APIRequestContext } from '@playwright/test';
import { type StudyActivityOutputComplete } from '@/features/study-activities/types/study-activity';

export const mockSubmitStudyActivity = async ({
  page,
  request,
  studyActivityId,
}: {
  page: Page;
  request: APIRequestContext;
  studyActivityId: number;
}): Promise<StudyActivityOutputComplete> => {
  try {
    const token = await page.evaluate(() => {
      const storageData = window.localStorage.getItem('token-storage');
      const parsedStorageData = JSON.parse(storageData || 'null');
      return parsedStorageData?.state?.token as string | null;
    });

    if (!token) {
      throw new Error('Could not find token in Playwright store state.');
    }

    const response = await request.patch(
      `${process.env.VITE_API_URL}/dev/study-activity/${studyActivityId}/submit`,
      {
        headers: { Authorization: `Bearer ${token}` },
      },
    );

    if (!response.ok()) {
      const errorBody = await response.text();
      throw new Error(`Failed to create study activity: ${errorBody}`);
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
