import { type Page, type APIRequestContext } from '@playwright/test';

type StudyActivityCreationType = {
  prompt: string;
  activity_format: string;
  subject_type: string;
  name: string;
  description: string;
  n_items: number;
};

export const createStudyActivity = async ({
  page,
  request,
  interactionId,
  studyActivity,
}: {
  page: Page;
  request: APIRequestContext;
  interactionId: number;
  studyActivity: StudyActivityCreationType;
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
      `${process.env.VITE_API_URL}/dev/study-activity/${interactionId}`,
      {
        data: { ...studyActivity },
        headers: { Authorization: `Bearer ${token}` },
      },
    );
    if (!response.ok()) {
      const errorBody = await response.text();
      throw new Error(`Failed to create study activity: ${errorBody}`);
    }
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    throw new Error(`Failed to connect to server: ${errorMessage}`, {
      cause: e,
    });
  }
};
