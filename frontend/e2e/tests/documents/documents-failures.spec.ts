import test, { expect } from '@playwright/test';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';
import { InteractionPage } from '@e2e/pages/interaction/InteractionPage';
import path from 'path';

test.describe('Documents - Failure tests', () => {
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

    await page.route(`/api/document/${interactionId}*`, async (route) => {
      if (route.request().method() !== 'POST') {
        await route.continue();
        return;
      }

      const requestUrl = new URL(route.request().url());

      // Route redirect
      await route.continue({
        url: `${process.env.BASE_URL}/api/dev/document/${interactionId}${requestUrl.search}`,
      });
    });
  });

  test('Fail to upload without a file', async ({ page }) => {
    const documentSection = new InteractionPage(page).documentsSection;

    await documentSection.creationButton.click();

    const fileError = documentSection.creationForm
      .locator('label')
      .filter({ hasText: 'File' })
      .getByRole('alert');

    await expect(fileError).toBeVisible();
    await expect(fileError).toContainText('A file is required.');
  });

  test('Fail to update a document with an empty name.', async ({ page }) => {
    const documentSection = new InteractionPage(page).documentsSection;

    const filepath = path.join(
      import.meta.dirname,
      '../../data/document/test-file.txt',
    );

    // Fills inputs
    const newName = 'newName';
    const newSubject = 'Literature';

    await documentSection.fillCreationInputs({
      filepath,
      name: newName,
      subjectType: newSubject,
      automaticSubject: 'No',
    });

    // Submits
    await documentSection.creationButton.click();

    // Finds the update form
    await documentSection.documentItem
      .getByRole('button', {
        name: 'newName (Literature)',
      })
      .click();

    const detailsPanel = documentSection.documentItem
      .locator('section')
      .filter({ hasText: 'Details' });
    const showUpdateButton = detailsPanel.getByRole('button', {
      name: 'Show update',
    });

    await showUpdateButton.click();

    const updatePanel = documentSection.documentItem
      .locator('form')
      .filter({ hasText: 'Update' });
    const nameUpdateField = updatePanel.getByRole('textbox', {
      name: 'New name',
    });
    const updateButton = updatePanel.getByRole('button', { name: 'Update' });

    // Updates with empty name
    await nameUpdateField.clear();

    await updateButton.click();

    const nameError = updatePanel
      .locator('label')
      .filter({ hasText: 'new name' })
      .getByRole('alert');
    await expect(nameError).toBeVisible();
    await expect(nameError).toContainText('Too small');
  });
});
