import test, { expect } from '@playwright/test';
import { HomePage } from '@e2e/pages/home/HomePage';
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc.js';
import { mockCreateStudyAssessment } from '@e2e/helpers/study-assessments/mock-create-study-assessment';

dayjs.extend(utc);

test.describe('Study assessments - Success tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    const user = userData.user;

    await registerUser({ request, user });
    await loginUser({ user, page });
  });

  test("View yesterday's assessment", async ({ page, request }) => {
    const studyAssessmentsSection = new HomePage(page).studyAssessmentsSection;

    // Without assessment
    await expect(studyAssessmentsSection.yesterdayAssessmentContent).toHaveText(
      "User didn't log in yesterday.",
    );

    // With assessment
    const now = dayjs.utc();
    const yesterday = now.subtract(1, 'day');

    const studyAssessment = {
      assessment_of: yesterday.format('YYYY-MM-DD'),
      content: 'Mock assessment content - yesterday',
    };

    await mockCreateStudyAssessment({ page, request, studyAssessment });
    await page.reload();

    await expect(studyAssessmentsSection.yesterdayAssessmentContent).toHaveText(
      studyAssessment.content,
    );
  });

  test('View study assessments history, tries searching for an existing study assessment and a non-existing one', async ({
    page,
    request,
  }) => {
    const studyAssessmentsSection = new HomePage(page).studyAssessmentsSection;

    // Without assessment
    await expect(studyAssessmentsSection.infoNoItem).toBeVisible();

    // With assessment
    const now = dayjs.utc();

    const yesterday = now.subtract(1, 'day');
    const dayBeforeYesterday = now.subtract(2, 'day');

    const studyAssessment1 = {
      assessment_of: yesterday.format('YYYY-MM-DD'),
      content: 'Mock assessment content - yesterday',
    };
    const studyAssessment2 = {
      assessment_of: dayBeforeYesterday.format('YYYY-MM-DD'),
      content: 'Mock assessment content - day before yesterday',
    };

    await mockCreateStudyAssessment({
      page,
      request,
      studyAssessment: studyAssessment1,
    });
    await mockCreateStudyAssessment({
      page,
      request,
      studyAssessment: studyAssessment2,
    });
    await page.reload();

    await expect(studyAssessmentsSection.assessmentItem).toHaveCount(2);

    // Verifies order: earliest first
    const assessmentItem1 = studyAssessmentsSection.assessmentItem.first();
    const assessmentItem2 = studyAssessmentsSection.assessmentItem.last();

    await expect(assessmentItem1).toHaveText(
      `Assessment date: ${studyAssessment1.assessment_of}`,
    );
    await expect(assessmentItem2).toHaveText(
      `Assessment date: ${studyAssessment2.assessment_of}`,
    );

    // Verifies content
    await assessmentItem1.getByRole('button').click();
    await expect(assessmentItem1.locator('p')).toContainText(
      studyAssessment1.content,
    );

    await assessmentItem2.getByRole('button').click();
    await expect(assessmentItem2.locator('p')).toContainText(
      studyAssessment2.content,
    );
  });
});
