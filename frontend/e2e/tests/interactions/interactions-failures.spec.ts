import test, { expect } from '@playwright/test';
import { HomePage } from '@e2e/pages/home/HomePage';
import { createInteraction } from '@e2e/helpers/interactions/create-interaction';
import interactionData from '@e2e/data/interactions/interaction.json' with { type: 'json' };
import userData from '@e2e/data/auth/user.json' with { type: 'json' };
import { resetDatabase } from '@e2e/helpers/database';
import { registerUser } from '@e2e/helpers/auth/register-user';
import { loginUser } from '@e2e/helpers/auth/login-user';

test.describe('Interactions - Failure tests', () => {
  test.beforeEach(async ({ page, request }) => {
    await resetDatabase(request);

    const user = userData.user;

    await registerUser({ request, user });
    await loginUser({ user, page });
  });

  test('Create an interaction using empty inputs.', async ({ page }) => {
    const interactionSection = new HomePage(page).interactionsSection;

    await interactionSection.creationButton.click();

    const nameError = interactionSection.creationForm
      .locator('label')
      .filter({ hasText: 'Name' })
      .getByRole('alert');

    await expect(nameError).toBeVisible();
    await expect(nameError).toContainText('Too small');
  });

  test('Update an interaction using empty inputs.', async ({
    page,
    request,
  }) => {
    const interaction = interactionData.interaction;

    await createInteraction({ page, request, interaction });
    await page.reload();

    const interactionSection = new HomePage(page).interactionsSection;

    // Shows update
    await interactionSection.interactionItem
      .getByRole('button', {
        name: 'Update',
      })
      .click();

    // Clears name and confirms update
    const updatePanel = interactionSection.interactionItem
      .locator('form')
      .filter({ hasText: 'Update' });
    await updatePanel.getByRole('textbox', { name: 'New name' }).clear();
    await updatePanel.getByRole('button', { name: 'Update' }).click();

    // Errors
    const nameError = updatePanel
      .locator('label')
      .filter({ hasText: 'Name' })
      .getByRole('alert');
    await expect(nameError).toBeVisible();
    await expect(nameError).toContainText('Too small');
  });
});
