import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { InteractionPage } from '@e2e/pages/interaction/InteractionPage';
import { createStudyActivities } from '@e2e/helpers/study-activities/create-study-activity';

test.describe('Interactions - Failure tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    // Registers and logs in
    const user = userData.user;

    await registerUser({ request, user });
    await loginUser({ user, page });

    // Creates and goes inside interaction
    const interaction = interactionData.interaction;

    const interactionId = await createInteraction({
      page,
      request,
      interaction,
    });
    await page.reload();

    const interactionPage = new InteractionPage(page);
    await interactionPage.goto(interactionId);
  });

  test('Create a flashcards activity manually using empty inputs.', async ({
    page,
  }) => {
    const studyActivitiesSection = new InteractionPage(page)
      .studyActivitiesSection;

    await studyActivitiesSection.flashcardCreationButton.click();

    const nameError = studyActivitiesSection.flashcardCreationForm
      .locator('label')
      .filter({ hasText: 'Name' })
      .getByRole('alert')
      .first(); // First because Vietnamese has name in it, therefore this results in 2 elements

    await expect(nameError).toBeVisible();
    await expect(nameError).toContainText('Too small');
  });

  test('Update an activity name to be empty.', async ({ page, request }) => {
    const studyActivitiesSection = new InteractionPage(page)
      .studyActivitiesSection;

    const interactionId = Number(page.url().split('/').pop());

    const flashcardActivity = {
      name: 'test-name',
      description: 'test-description',
      subject_type: 'MATHS',
    };

    await createStudyActivities({
      page,
      request,
      interactionId,
      flashcard: flashcardActivity,
    });
    await page.reload();

    // Clicks update button
    await studyActivitiesSection.studyActivity
      .getByRole('button', {
        name: 'Update',
      })
      .click();

    // Updates
    const updatePanel = studyActivitiesSection.studyActivity
      .locator('form')
      .filter({ hasText: 'Update' });
    const nameUpdateField = updatePanel.getByRole('textbox', {
      name: 'New name',
    });

    await nameUpdateField.clear();

    await updatePanel.getByRole('button', { name: 'Update' }).click();

    // Verifies result
    const nameError = updatePanel
      .locator('label')
      .filter({ hasText: 'New name' })
      .getByRole('alert');

    await expect(nameError).toBeVisible();
    await expect(nameError).toContainText('Too small');
  });
});
