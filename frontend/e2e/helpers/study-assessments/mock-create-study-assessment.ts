import { type APIRequestContext, type Page } from '@playwright/test';

type StudyAssessmentCreationType = {
  assessment_of: string;
  content: string;
};

export const mockCreateStudyAssessment = async ({
  page,
  request,
  studyAssessment,
}: {
  page: Page;
  request: APIRequestContext;
  studyAssessment: StudyAssessmentCreationType;
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
      `${process.env.VITE_API_URL}/dev/study-assessment`,
      {
        data: { ...studyAssessment },
        headers: { Authorization: `Bearer ${token}` },
      },
    );

    if (!response.ok()) {
      const errorBody = await response.text();
      throw new Error(`Failed to create study assessment: ${errorBody}`);
    }
  } catch (e) {
    const errorMessage = e instanceof Error ? e.message : String(e);
    throw new Error(`Failed to connect to server: ${errorMessage}`, {
      cause: e,
    });
  }
};
