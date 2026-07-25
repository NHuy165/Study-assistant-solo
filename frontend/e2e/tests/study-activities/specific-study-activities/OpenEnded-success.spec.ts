import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { createStudyActivity } from '@e2e/helpers/study-activities/create-study-activity';
import { StudyActivityPage } from '@e2e/pages/study-activity/StudyActivityPage';
import { mockSubmitStudyActivity } from '@e2e/helpers/study-activities/mock-submit-study-activity';

test.describe('Open ended - Success tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    // Registers and logs in
    const user = userData.user;

    await registerUser({ request, user });
    await loginUser({ user, page });

    // Creates interaction
    const interaction = interactionData.interaction;

    const interactionId = await createInteraction({
      page,
      request,
      interaction,
    });

    // Creates study activity
    const studyActivity = {
      prompt: 'test-OpenEnded-prompt',
      activity_format: 'OPEN_ENDED',
      subject_type: 'VIETNAMESE',
      name: 'test-OpenEnded-name',
      description: 'test-OpenEnded-description',
      n_items: 2,
    };
    const studyActivityId = await createStudyActivity({
      page,
      request,
      interactionId,
      studyActivity,
    });

    // Mocks submit response
    await page.route(
      `**/api/study-activity/${studyActivityId}/submit`,
      async (route) => {
        const mockData = await mockSubmitStudyActivity({
          page,
          request,
          studyActivityId,
        });
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          json: mockData,
        });
      },
    );

    const studyActivityPage = new StudyActivityPage(page);
    await studyActivityPage.goto(studyActivityId);
  });

  test('Attempt the questions, check whether answers are saved properly, then submit the activity and check the gradings.', async ({
    page,
  }) => {
    const OpenEndedActivity = new StudyActivityPage(page).OpenEndedActivity;

    const question1 = OpenEndedActivity.exerciseItem.filter({
      hasText: 'Test question 1',
    });
    const question2 = OpenEndedActivity.exerciseItem.filter({
      hasText: 'Test question 2',
    });

    // Writes the answer and reloads to see if they persist
    const test_answer_1 = 'Test answer 1';
    await question1.getByRole('textbox').fill(test_answer_1);
    await expect(question1.getByText('Autosave')).toHaveText(
      'Autosave successful',
    );

    await page.reload();

    await expect(question1.getByRole('textbox')).toHaveValue(test_answer_1);

    // Submits
    await OpenEndedActivity.submitButton.click();

    // Checks submit button and all radio buttons
    await expect(OpenEndedActivity.submitButton).toHaveText('Submitted');
    await expect(OpenEndedActivity.submitButton).toBeDisabled;
    await expect(
      OpenEndedActivity.exerciseItem.getByRole('textbox', { disabled: false }),
    ).not.toBeVisible();

    // Checks explanations
    const explanation1 = question1
      .locator('p')
      .filter({ hasText: 'Explanation:' });
    await expect(explanation1).toContainText('Test question 1: CORRECT');

    const explanation2 = question2
      .locator('p')
      .filter({ hasText: 'Explanation:' });
    await expect(explanation2).toContainText('Test question 2: WRONG');

    // Checks scores
    await expect(question1).toContainText('Score: 50/50');
    await expect(question2).toContainText('Score: 0/50');
  });
});
