import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { mockCreateStudyActivity } from '@e2e/helpers/study-activities/mock-create-study-activity';
import { StudyActivityPage } from '@e2e/pages/study-activity/StudyActivityPage';
import { mockSubmitStudyActivity } from '@e2e/helpers/study-activities/mock-submit-study-activity';

test.describe('Multiple choice questions - Success tests', () => {
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
      prompt: 'test-MCQ-prompt',
      activity_format: 'MULTIPLE_CHOICE_QUESTIONS',
      subject_type: 'MATHS',
      name: 'test-MCQ-name',
      description: 'test-MCQ-description',
      n_items: 2,
    };
    const studyActivityId = (
      await mockCreateStudyActivity({
        page,
        request,
        interactionId,
        studyActivity,
      })
    ).id as number;

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
    const MCQActivity = new StudyActivityPage(page).MCQActivity;

    const question1 = MCQActivity.exerciseItem.filter({
      hasText: 'Test question 1',
    });
    const question2 = MCQActivity.exerciseItem.filter({
      hasText: 'Test question 2',
    });

    const choice1_1 = question1.getByRole('radio', {
      name: 'Test choice 1-1',
    });
    const choice2_3 = question2.getByRole('radio', {
      name: 'Test choice 2-3',
    });

    // Checks the choices and reloads to see if they persist
    await choice1_1.check();
    await choice2_3.check();

    await page.reload();

    await expect(choice1_1).toBeChecked();
    await expect(choice2_3).toBeChecked();

    // Submits
    await MCQActivity.submitButton.click();

    // Checks submit button and all radio buttons
    await expect(MCQActivity.submitButton).toHaveText('Submitted');
    await expect(MCQActivity.submitButton).toBeDisabled;
    await expect(
      MCQActivity.exerciseItem.getByRole('radio', { disabled: false }),
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

    // Checks correct / wrong answer notations
    const label1_1 = question1
      .locator('label')
      .filter({ hasText: 'Test choice 1-1' });
    await expect(label1_1).toContainText('Correct answer');

    const label2_2 = question2
      .locator('label')
      .filter({ hasText: 'Test choice 2-2' });
    await expect(label2_2).toContainText('Correct answer');

    const label2_3 = question2
      .locator('label')
      .filter({ hasText: 'Test choice 2-3' });
    await expect(label2_3).toContainText('Wrong answer');
  });
});
